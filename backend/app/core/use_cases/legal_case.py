from datetime import datetime, timezone
import uuid
from fastapi import BackgroundTasks, HTTPException, Request, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from typing import Optional, List

from app.adapters.orm.models.legal_case import LegalCase
from app.adapters.orm.security import create_audit_log
from app.core.value_objects.legal_case import LegalCaseCreate, LegalCaseResponse, LegalCaseUpdate
from app.adapters.orm.models.user import User
from sqlalchemy.inspection import inspect

async def create_legal_case_use_case(
    legal_case_in: LegalCaseCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
) -> LegalCaseResponse:
    try:
        legal_case = LegalCase(
            id=uuid.uuid4(),
            **legal_case_in.model_dump()
        )
        legal_case.created_by_id = current_user.id

        db.add(legal_case)
        await db.commit()
        await db.refresh(legal_case)

        background_tasks.add_task(
            create_audit_log,
            db=db,
            action="create",
            user_id=current_user.id,
            resource_type="legal_cases",
            resource_id=legal_case.id,
            details=legal_case_in.model_dump(),
            ip_address=request.client.host if request and request.client else None
        )

        print(
            "Created legal case:",
            {c.key: getattr(legal_case, c.key) for c in inspect(legal_case).mapper.column_attrs}
        )
        return LegalCaseResponse.model_validate(legal_case)
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Legal case already exists"
        )

async def get_legal_case_use_case(
    legal_case_id: uuid.UUID,
    db: AsyncSession,
) -> LegalCase:
    stmt = select(LegalCase).where(LegalCase.id == legal_case_id)
    result = await db.execute(stmt)
    legal_case = result.scalars().first()
    if legal_case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Legal case not found")
    return legal_case

async def list_legal_cases_use_case(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[LegalCase]:
    result = await db.execute(select(LegalCase).offset(skip).limit(limit))
    return result.scalars().all()

async def update_legal_case_use_case(
    legal_case_id: uuid.UUID,
    legal_case_update: LegalCaseUpdate,
    background_tasks: BackgroundTasks,
    current_user: User,
    db: AsyncSession,
    request: Optional[Request] = None,
) -> LegalCase:
    stmt = select(LegalCase).where(LegalCase.id == legal_case_id)
    result = await db.execute(stmt)
    legal_case = result.scalars().first()

    if legal_case is None:
        raise HTTPException(status_code=404, detail="Legal case not found")

    update_data = legal_case_update.model_dump(exclude_unset=True)

    try:
        if update_data:
            stmt = (
                update(LegalCase)
                .where(LegalCase.id == legal_case_id)
                .values(**update_data)
            )
            await db.execute(stmt)
            await db.commit()

        # Refresh legal case data
        stmt = select(LegalCase).where(LegalCase.id == legal_case_id)
        result = await db.execute(stmt)
        legal_case = result.scalars().first()

        background_tasks.add_task(
            create_audit_log,
            db=db,
            user_id=current_user.id,
            action="update",
            resource_type="legal_cases",
            resource_id=legal_case_id,
            details=update_data,
            ip_address=request.client.host if request and request.client else None
        )

        return legal_case
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Legal case already exists"
        )

async def delete_legal_case_use_case(
    legal_case_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession,
    current_user: User,
    request: Optional[Request] = None,
):
    stmt = select(LegalCase).where(LegalCase.id == legal_case_id)
    result = await db.execute(stmt)
    legal_case = result.scalars().first()

    if legal_case is None:
        raise HTTPException(status_code=404, detail="Legal case not found")

    stmt = delete(LegalCase).where(LegalCase.id == legal_case_id)
    await db.execute(stmt)
    await db.commit()

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="delete",
        resource_type="legal_cases",
        resource_id=legal_case_id,
        details={"legal_case_number": legal_case.legal_case_number},
        ip_address=request.client.host if request and request.client else None
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)