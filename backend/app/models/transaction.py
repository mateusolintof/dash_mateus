from sqlalchemy import Column, String, Text, DateTime, Date, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class Transaction(Base):
    """
    Transações financeiras (despesas e receitas).

    Tipos de transação:
    1. Automáticas: is_manual=False, is_projection=False (vem de extrato)
    2. Manuais: is_manual=True, is_projection=False (entrada manual do usuário)
    3. Projeções: is_projection=True (exclusivo da aba de projeções manuais)

    IMPORTANTE: Queries devem sempre filtrar por is_projection para evitar
    misturar dados reais com simulações!
    """
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)  # Negativo = despesa, Positivo = receita

    # Relacionamentos
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    projection_id = Column(UUID(as_uuid=True), ForeignKey("projections.id", ondelete="CASCADE"), nullable=True)
    bank_statement_id = Column(UUID(as_uuid=True), ForeignKey("bank_statements.id", ondelete="SET NULL"), nullable=True)

    # Flags de controle
    is_manual = Column(Boolean, default=False, index=True)         # Entrada manual vs automática
    is_projection = Column(Boolean, default=False, index=True)     # Pertence à aba de projeções

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    projection = relationship("Projection", back_populates="transactions")
    bank_statement = relationship("BankStatement", back_populates="transactions")
