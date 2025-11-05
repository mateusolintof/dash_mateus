from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from uuid import UUID


class ProjectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True


class ProjectionCreate(ProjectionBase):
    pass


class ProjectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class ProjectionResponse(ProjectionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectionWithStats(ProjectionResponse):
    total_transactions: int
    total_income: float
    total_expenses: float
    balance: float
