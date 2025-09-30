from typing import Any
import uuid
from fastapi import HTTPException, status, BackgroundTasks, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone

from app.adapters.orm.models.company import Company
from app.adapters.orm.models.user import User
from app.adapters.orm.security.audit import create_audit_log
from app.core.value_objects.company import CompanyCreate, CompanyResponse, CompanyUpdate


async def create_company_use_case(
    company: CompanyCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    try:
        db_company = Company(**company.model_dump())
        
        db_company.owner_id = current_user.id
        db_company.created_by_id = current_user.id
        db_company.cnpj = company.cnpj
        db_company.name = company.name
        db_company.members = [current_user]
        db_company.created_by = current_user
        
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
    skip: int = 0,
    limit: int = 10,
    filters: list[Any] = []
):
    query = select(Company).where(*filters).offset(skip).limit(limit)
    result = await db.execute(query)

    return result.scalars().all()

async def get_my_companies_use_case(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    current_user: User = None,
) -> list[CompanyResponse]:
    await db.refresh(current_user, attribute_names=["companies"])

    companies = current_user.companies[skip : skip + limit]

    return [CompanyResponse.model_validate(company) for company in companies]

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
    company_id: uuid.UUID,
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
    company_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    db_company = result.scalars().first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    try:
        db_company.is_deleted = True
        db_company.deleted_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(db_company)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not delete company")
    
    company_details: dict[str, Any] = {
        "name": db_company.name,
        "cnpj": db_company.cnpj,
        "deleted_at": db_company.deleted_at,
        "deleted_by_id": db_company.deleted_by_id,
    }

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