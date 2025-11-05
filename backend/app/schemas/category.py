from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class CategoryBase(BaseModel):
    name: str
    color: Optional[str] = None
    icon: Optional[str] = None
    budget_limit: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    budget_limit: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore


class CategoryResponse(CategoryBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
