from datetime import datetime, timezone
import uuid
from fastapi import BackgroundTasks, HTTPException, Request, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from typing import Optional, List

from app.adapters.orm.models.legal_calculation import LegalCalculation
from app.adapters.orm.security import create_audit_log
from app.core.value_objects.legal_calculation import (
    LegalCalculationCreate,
    LegalCalculationResponse,
    LegalCalculationUpdate,
)
from app.adapters.orm.models.user import User
from sqlalchemy.inspection import inspect


async def create_legal_calculation_use_case(
    calculation_in: LegalCalculationCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User,
) -> LegalCalculationResponse:
    try:
        calculation = LegalCalculation(
            id=uuid.uuid4(),
            **calculation_in.model_dump()
        )
        calculation.created_by_id = current_user.id

        db.add(calculation)
        await db.commit()
        await db.refresh(calculation)

        background_tasks.add_task(
            create_audit_log,
            db=db,
            action="create",
            user_id=current_user.id,
            resource_type="legal_calculations",
            resource_id=calculation.id,
            details=calculation_in.model_dump(),
            ip_address=request.client.host if request and request.client else None,
        )

        return LegalCalculationResponse.model_validate(calculation)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Legal calculation already exists",
        )


async def get_legal_calculation_use_case(
    calculation_id: uuid.UUID,
    db: AsyncSession,
) -> LegalCalculation:
    stmt = select(LegalCalculation).where(LegalCalculation.id == calculation_id)
    result = await db.execute(stmt)
    calculation = result.scalars().first()
    if calculation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Legal calculation not found")
    return calculation


async def list_legal_calculations_use_case(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[LegalCalculation]:
    result = await db.execute(select(LegalCalculation).offset(skip).limit(limit))
    return result.scalars().all()


async def update_legal_calculation_use_case(
    calculation_id: uuid.UUID,
    calculation_update: LegalCalculationUpdate,
    background_tasks: BackgroundTasks,
    current_user: User,
    db: AsyncSession,
    request: Optional[Request] = None,
) -> LegalCalculation:
    stmt = select(LegalCalculation).where(LegalCalculation.id == calculation_id)
    result = await db.execute(stmt)
    calculation = result.scalars().first()

    if calculation is None:
        raise HTTPException(status_code=404, detail="Legal calculation not found")

    update_data = calculation_update.model_dump(exclude_unset=True)

    try:
        if update_data:
            stmt = (
                update(LegalCalculation)
                .where(LegalCalculation.id == calculation_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()

        # Refresh
        stmt = select(LegalCalculation).where(LegalCalculation.id == calculation_id)
        result = await db.execute(stmt)
        calculation = result.scalars().first()

        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="update",
            resource_type="legal_calculations",
            resource_id=calculation_id,
            details=update_data,
            ip_address=request.client.host if request and request.client else None,
        )

        return calculation
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Legal calculation already exists",
        )


async def delete_legal_calculation_use_case(
    calculation_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession,
    current_user: User,
    request: Optional[Request] = None,
):
    stmt = select(LegalCalculation).where(LegalCalculation.id == calculation_id)
    result = await db.execute(stmt)
    calculation = result.scalars().first()

    if calculation is None:
        raise HTTPException(status_code=404, detail="Legal calculation not found")

    stmt = delete(LegalCalculation).where(LegalCalculation.id == calculation_id)
    await db.execute(stmt)
    await db.commit()

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="delete",
        resource_type="legal_calculations",
        resource_id=calculation_id,
        details={"legal_calculation_id": calculation.id},
        ip_address=request.client.host if request and request.client else None,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)