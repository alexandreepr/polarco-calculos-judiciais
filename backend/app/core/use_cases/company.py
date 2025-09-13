from typing import Any
from fastapi import HTTPException, status, BackgroundTasks, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from backend.app.adapters.orm.models.company import Company
from backend.app.adapters.orm.models.user import User
from backend.app.adapters.orm.security.audit import create_audit_log
from backend.app.core.value_objects.company import CompanyCreate, CompanyUpdate

async def create_company_use_case(
    company: CompanyCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    try:
        db_company = Company(**company.model_dump())
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CNPJ already exists")

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="create",
        resource_type="companies",
        resource_id=db_company.id,
        details=company.model_dump(),
        ip_address=request.client.host if request and request.client else None
    )
    return db_company

async def get_companies_use_case(
    db: AsyncSession,
    skip: int,
    limit: int
):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()

async def get_company_use_case(
    company_id: int,
    db: AsyncSession
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

async def update_company_use_case(
    company_id: int,
    company_update: CompanyUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    db_company = result.scalars().first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    update_data = company_update.model_dump(exclude_unset=True)
    try:
        for field, value in update_data.items():
            setattr(db_company, field, value)
        await db.commit()
        await db.refresh(db_company)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CNPJ already exists")

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="update",
        resource_type="companies",
        resource_id=company_id,
        details=update_data,
        ip_address=request.client.host if request and request.client else None
    )
    return db_company

async def delete_company_use_case(
    company_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    db_company = result.scalars().first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    company_details: dict[str, Any] = {
        "name": db_company.name,
        "cnpj": db_company.cnpj,
        "is_active": db_company.is_active
    }
    try:
        await db.delete(db_company)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not delete company")

    background_tasks.add_task(
        create_audit_log,
        db=db,
        user_id=current_user.id,
        action="delete",
        resource_type="companies",
        resource_id=company_id,
        details=company_details,
        ip_address=request.client.host if request and request.client else None
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)