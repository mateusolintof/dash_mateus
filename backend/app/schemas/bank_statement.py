from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from uuid import UUID


class BankStatementUploadResponse(BaseModel):
    id: UUID
    filename: str
    bank_name: Optional[str]
    total_transactions: int
    status: str
    period_start: Optional[date]
    period_end: Optional[date]
    upload_date: datetime

    class Config:
        from_attributes = True


class BankStatementResponse(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    bank_name: Optional[str]
    total_transactions: int
    status: str
    period_start: Optional[date]
    period_end: Optional[date]
    upload_date: datetime

    class Config:
        from_attributes = True


class TransactionReviewItem(BaseModel):
    temp_id: int
    date: date
    description: str
    amount: float
    suggested_category: Optional[str] = None
    category_id: Optional[UUID] = None


class TransactionBatchCreate(BaseModel):
    bank_statement_id: UUID
    transactions: list[dict]  # Lista de transações aprovadas
