from typing import Optional
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, Request, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.orm.database import get_async_db
from app.core.use_cases.legal_case import (
    create_legal_case_use_case,
    get_legal_case_use_case,
    list_legal_cases_use_case,
    update_legal_case_use_case,
    delete_legal_case_use_case,
)
from app.core.value_objects.legal_case import (
    LegalCaseCreate,
    LegalCaseUpdate,
    LegalCaseResponse,
)
from app.adapters.orm.models.legal_case import LegalCase
from app.adapters.orm.security.auth import get_current_user
from app.adapters.orm.models.user import User

legal_case_router = APIRouter(prefix="/legal-cases", tags=["Legal Cases"])

@legal_case_router.post("/", response_model=LegalCaseResponse, status_code=status.HTTP_201_CREATED)
async def create_legal_case(
    legal_case_in: LegalCaseCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    legal_case = await create_legal_case_use_case(legal_case_in, background_tasks, request, db, current_user)
    return LegalCaseResponse.model_validate(legal_case)


@legal_case_router.get("/", response_model=list[LegalCaseResponse])
async def get_legal_cases(
    db: AsyncSession = Depends(get_async_db),
):
    cases = await list_legal_cases_use_case(db)
    return [LegalCaseResponse.model_validate(case) for case in cases]

@legal_case_router.get("/{legal_case_id}", response_model=LegalCaseResponse)
async def get_legal_case(
    legal_case_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db),
):
    case = await get_legal_case_use_case(legal_case_id, db)
    if not case:
        raise HTTPException(status_code=404, detail="Legal case not found")
    return LegalCaseResponse.model_validate(case)

@legal_case_router.put("/{legal_case_id}", response_model=LegalCaseResponse)
async def update_legal_case(
    legal_case_id: uuid.UUID,
    legal_case_update: LegalCaseUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    case = await update_legal_case_use_case(legal_case_id, legal_case_update, background_tasks, current_user, db, request)
    if not case:
        raise HTTPException(status_code=404, detail="Legal case not found")
    return LegalCaseResponse.model_validate(case)

@legal_case_router.delete("/{legal_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_legal_case(
    legal_case_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    await delete_legal_case_use_case(legal_case_id, background_tasks, db, current_user, request)