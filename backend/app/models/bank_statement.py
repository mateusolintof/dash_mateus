from sqlalchemy import Column, String, DateTime, Date, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class BankStatement(Base):
    """Histórico de uploads de extratos bancários"""
    __tablename__ = "bank_statements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=True)  # Caminho no storage
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    bank_name = Column(String, nullable=True)
    period_start = Column(Date, nullable=True)
    period_end = Column(Date, nullable=True)
    total_transactions = Column(Integer, default=0)
    status = Column(String, default="processing")  # 'processing', 'completed', 'error'

    # Relationships
    user = relationship("User", back_populates="bank_statements")
    transactions = relationship("Transaction", back_populates="bank_statement")
