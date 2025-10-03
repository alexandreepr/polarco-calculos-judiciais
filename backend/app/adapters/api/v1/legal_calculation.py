from typing import Optional
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, Request, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.orm.database import get_async_db
from app.adapters.orm.security.auth import get_current_user
from app.adapters.orm.models.user import User

from app.core.use_cases.legal_calculation import (
    create_legal_calculation_use_case,
    get_legal_calculation_use_case,
    list_legal_calculations_use_case,
    update_legal_calculation_use_case,
    delete_legal_calculation_use_case,
)
from app.core.value_objects.legal_calculation import (
    LegalCalculationCreate,
    LegalCalculationUpdate,
    LegalCalculationResponse,
)

legal_calculation_router = APIRouter(prefix="/legal-calculations", tags=["Legal Calculations"])


@legal_calculation_router.post("/", response_model=LegalCalculationResponse, status_code=status.HTTP_201_CREATED)
async def create_legal_calculation(
    calculation_in: LegalCalculationCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    calculation = await create_legal_calculation_use_case(calculation_in, background_tasks, request, db, current_user)
    return LegalCalculationResponse.model_validate(calculation)


@legal_calculation_router.get("/", response_model=list[LegalCalculationResponse])
async def list_legal_calculations(
    db: AsyncSession = Depends(get_async_db),
):
    items = await list_legal_calculations_use_case(db)
    return [LegalCalculationResponse.model_validate(i) for i in items]


@legal_calculation_router.get("/{calculation_id}", response_model=LegalCalculationResponse)
async def get_legal_calculation(
    calculation_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db),
):
    item = await get_legal_calculation_use_case(calculation_id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Legal calculation not found")
    return LegalCalculationResponse.model_validate(item)

@legal_calculation_router.get("/calculations-by-legal-case/{legal_case_id}", response_model=list[LegalCalculationResponse])
async def get_legal_calculations_by_legal_case(
    legal_case_id: uuid.UUID,
    db: AsyncSession = Depends(get_async_db),
):
    items = await list_legal_calculations_use_case(db, legal_case_id=legal_case_id)

    return [LegalCalculationResponse.model_validate(i) for i in items]

@legal_calculation_router.put("/{calculation_id}", response_model=LegalCalculationResponse)
async def update_legal_calculation(
    calculation_id: uuid.UUID,
    calculation_update: LegalCalculationUpdate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    updated = await update_legal_calculation_use_case(
        calculation_id, calculation_update, background_tasks, current_user, db, request
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Legal calculation not found")
    return LegalCalculationResponse.model_validate(updated)


@legal_calculation_router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_legal_calculation(
    calculation_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    await delete_legal_calculation_use_case(calculation_id, background_tasks, db, current_user, request)