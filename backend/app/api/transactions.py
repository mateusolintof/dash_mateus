from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from uuid import UUID

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse
)

router = APIRouter()


@router.get("/", response_model=TransactionListResponse)
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_projection: bool = Query(False, description="Filtrar transações de projeção"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar transações do usuário com filtros"""
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_projection == is_projection
    )

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    total = query.count()
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()

    return {"total": total, "transactions": transactions}


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter transação por ID"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    return transaction


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar nova transação"""
    new_transaction = Transaction(
        user_id=current_user.id,
        **transaction_data.model_dump()
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar transação"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Atualizar apenas campos fornecidos
    update_data = transaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar transação"""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return None


@router.get("/stats/summary")
async def get_transaction_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_projection: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter resumo de transações (receitas, despesas, saldo)"""
    from sqlalchemy import func
    from decimal import Decimal

    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_projection == is_projection
    )

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.all()

    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)
    balance = total_income - total_expenses

    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(balance),
        "total_transactions": len(transactions)
    }


@router.get("/stats/monthly")
async def get_monthly_stats(
    months: int = Query(6, ge=1, le=12, description="Número de meses para retornar"),
    is_projection: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter estatísticas mensais (receitas e despesas por mês)"""
    from sqlalchemy import func, extract
    from datetime import datetime, timedelta
    from calendar import month_abbr
    import locale

    # Define locale para português
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except:
        pass

    # Calcular data de início (X meses atrás)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=months * 30)

    # Buscar transações no período
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_projection == is_projection,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()

    # Agrupar por mês
    monthly_data = {}
    for trans in transactions:
        month_key = trans.date.strftime("%Y-%m")
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "income": 0,
                "expenses": 0
            }

        if trans.amount > 0:
            monthly_data[month_key]["income"] += float(trans.amount)
        else:
            monthly_data[month_key]["expenses"] += float(abs(trans.amount))

    # Formatar resposta
    result = []
    current_date = start_date
    while current_date <= end_date:
        month_key = current_date.strftime("%Y-%m")
        month_name = current_date.strftime("%b").capitalize()

        result.append({
            "month": month_name,
            "month_key": month_key,
            "income": monthly_data.get(month_key, {}).get("income", 0),
            "expenses": monthly_data.get(month_key, {}).get("expenses", 0),
            "balance": monthly_data.get(month_key, {}).get("income", 0) - monthly_data.get(month_key, {}).get("expenses", 0)
        })

        # Próximo mês
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)

    return result[-months:]


@router.get("/stats/by-category")
async def get_stats_by_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_projection: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter gastos agrupados por categoria"""
    from app.models.category import Category

    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_projection == is_projection,
        Transaction.amount < 0  # Apenas despesas
    )

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    transactions = query.all()

    # Agrupar por categoria
    category_totals = {}
    for trans in transactions:
        if trans.category_id:
            category = db.query(Category).filter(Category.id == trans.category_id).first()
            category_name = category.name if category else "Sem Categoria"
            category_color = category.color if category else "#999999"
        else:
            category_name = "Sem Categoria"
            category_color = "#999999"

        if category_name not in category_totals:
            category_totals[category_name] = {
                "name": category_name,
                "value": 0,
                "color": category_color
            }

        category_totals[category_name]["value"] += float(abs(trans.amount))

    # Ordenar por valor
    result = sorted(category_totals.values(), key=lambda x: x["value"], reverse=True)

    return result
