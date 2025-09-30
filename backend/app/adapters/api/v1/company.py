import uuid
from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.adapters.orm.database import get_async_db
from app.adapters.orm.models.user import User
from app.adapters.orm.security.permissions import require_permission
from app.adapters.orm.security.auth import get_current_user
from app.core.value_objects.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.core.use_cases.company import (
    create_company_use_case,
    get_companies_use_case,
    get_company_use_case,
    get_my_companies_use_case,
    update_company_use_case,
    delete_company_use_case
)

company_router = APIRouter(prefix="/companies", tags=["Company Management"])

@company_router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("companies", "create"))
):
    company = await create_company_use_case(company, background_tasks, request, db, current_user)

    return CompanyResponse.model_validate(company)

@company_router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("companies", "list"))
):
    companies = await get_companies_use_case(db, skip, limit)

    return [CompanyResponse.model_validate(c) for c in companies]

@company_router.get("/me", response_model=List[CompanyResponse])
async def get_my_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    companies = await get_my_companies_use_case(db, skip, limit, current_user)
    return [CompanyResponse.model_validate(c) for c in companies]

@company_router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("companies", "list"))
    current_user: User = Depends(get_current_user)
):
    return await get_company_use_case(company_id, db)

@company_router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID,
    company_update: CompanyUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("companies", "update"))
    current_user: User = Depends(get_current_user)
):
    company = await update_company_use_case(company_id, company_update, background_tasks, request, db, current_user)
    return CompanyResponse.model_validate(company)

@company_router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    # current_user: User = Depends(require_permission("companies", "delete"))
    current_user: User = Depends(get_current_user)
):
    return await delete_company_use_case(company_id, background_tasks, request, db, current_user)
