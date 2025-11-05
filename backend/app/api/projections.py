from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date, timedelta
from calendar import monthrange

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.projection import Projection
from app.models.transaction import Transaction
from app.schemas.projection import (
    ProjectionCreate,
    ProjectionUpdate,
    ProjectionResponse,
    ProjectionWithStats
)

router = APIRouter()


@router.get("/", response_model=List[ProjectionWithStats])
async def list_projections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os cenários de projeção do usuário"""
    projections = db.query(Projection).filter(
        Projection.user_id == current_user.id
    ).order_by(Projection.created_at.desc()).all()

    result = []
    for proj in projections:
        # Calcular estatísticas
        transactions = db.query(Transaction).filter(
            Transaction.projection_id == proj.id,
            Transaction.is_projection == True
        ).all()

        total_income = sum(t.amount for t in transactions if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)

        result.append({
            **proj.__dict__,
            "total_transactions": len(transactions),
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "balance": float(total_income - total_expenses)
        })

    return result


@router.get("/{projection_id}", response_model=ProjectionWithStats)
async def get_projection(
    projection_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um cenário de projeção"""
    projection = db.query(Projection).filter(
        Projection.id == projection_id,
        Projection.user_id == current_user.id
    ).first()

    if not projection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeção não encontrada"
        )

    # Calcular estatísticas
    transactions = db.query(Transaction).filter(
        Transaction.projection_id == projection.id,
        Transaction.is_projection == True
    ).all()

    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)

    return {
        **projection.__dict__,
        "total_transactions": len(transactions),
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(total_income - total_expenses)
    }


@router.post("/", response_model=ProjectionResponse, status_code=status.HTTP_201_CREATED)
async def create_projection(
    projection_data: ProjectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria novo cenário de projeção"""
    new_projection = Projection(
        user_id=current_user.id,
        **projection_data.model_dump()
    )

    db.add(new_projection)
    db.commit()
    db.refresh(new_projection)

    return new_projection


@router.post("/from-month/{year}/{month}", response_model=ProjectionResponse)
async def create_projection_from_month(
    year: int,
    month: int,
    name: str = Query(..., description="Nome do cenário"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria cenário de projeção duplicando transações de um mês real.
    Útil para simular "E se o próximo mês fosse igual a este?"
    """
    # Validar mês
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mês inválido"
        )

    # Criar projeção
    _, last_day = monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    projection = Projection(
        user_id=current_user.id,
        name=name,
        description=f"Projeção baseada em {month:02d}/{year}",
        start_date=start_date,
        end_date=end_date,
        is_active=True
    )

    db.add(projection)
    db.commit()
    db.refresh(projection)

    # Buscar transações do mês real
    real_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_projection == False,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    # Duplicar transações para a projeção
    for trans in real_transactions:
        proj_transaction = Transaction(
            user_id=current_user.id,
            projection_id=projection.id,
            date=trans.date,
            description=trans.description,
            amount=trans.amount,
            category_id=trans.category_id,
            is_manual=True,
            is_projection=True
        )
        db.add(proj_transaction)

    db.commit()

    return projection


@router.put("/{projection_id}", response_model=ProjectionResponse)
async def update_projection(
    projection_id: UUID,
    projection_data: ProjectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza cenário de projeção"""
    projection = db.query(Projection).filter(
        Projection.id == projection_id,
        Projection.user_id == current_user.id
    ).first()

    if not projection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeção não encontrada"
        )

    update_data = projection_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(projection, field, value)

    db.commit()
    db.refresh(projection)

    return projection


@router.delete("/{projection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_projection(
    projection_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta cenário de projeção e todas as transações associadas"""
    projection = db.query(Projection).filter(
        Projection.id == projection_id,
        Projection.user_id == current_user.id
    ).first()

    if not projection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeção não encontrada"
        )

    db.delete(projection)
    db.commit()

    return None


@router.get("/{projection_id}/compare")
async def compare_projection_with_real(
    projection_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Compara projeção com dados reais do mesmo período.
    Útil para ver "Projetado vs Real".
    """
    projection = db.query(Projection).filter(
        Projection.id == projection_id,
        Projection.user_id == current_user.id
    ).first()

    if not projection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeção não encontrada"
        )

    # Transações da projeção
    proj_transactions = db.query(Transaction).filter(
        Transaction.projection_id == projection.id,
        Transaction.is_projection == True
    ).all()

    proj_income = sum(t.amount for t in proj_transactions if t.amount > 0)
    proj_expenses = sum(abs(t.amount) for t in proj_transactions if t.amount < 0)

    # Transações reais do mesmo período
    real_transactions = []
    real_income = 0
    real_expenses = 0

    if projection.start_date and projection.end_date:
        real_transactions = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.is_projection == False,
            Transaction.date >= projection.start_date,
            Transaction.date <= projection.end_date
        ).all()

        real_income = sum(t.amount for t in real_transactions if t.amount > 0)
        real_expenses = sum(abs(t.amount) for t in real_transactions if t.amount < 0)

    return {
        "projection": {
            "name": projection.name,
            "total_income": float(proj_income),
            "total_expenses": float(proj_expenses),
            "balance": float(proj_income - proj_expenses),
            "transactions_count": len(proj_transactions)
        },
        "real": {
            "total_income": float(real_income),
            "total_expenses": float(real_expenses),
            "balance": float(real_income - real_expenses),
            "transactions_count": len(real_transactions)
        },
        "difference": {
            "income": float(proj_income - real_income),
            "expenses": float(proj_expenses - real_expenses),
            "balance": float((proj_income - proj_expenses) - (real_income - real_expenses))
        }
    }
