from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


class TransactionBase(BaseModel):
    date: date
    description: str
    amount: condecimal(max_digits=10, decimal_places=2)  # type: ignore
    category_id: Optional[UUID] = None
    is_manual: bool = True
    is_projection: bool = False
    projection_id: Optional[UUID] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    category_id: Optional[UUID] = None


class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    bank_statement_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    total: int
    transactions: list[TransactionResponse]
