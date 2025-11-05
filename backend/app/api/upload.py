from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.bank_statement import BankStatement
from app.models.transaction import Transaction
from app.models.category import Category
from app.services.parser_service import parser_service
from app.services.llm_service import llm_service
from app.schemas.bank_statement import (
    BankStatementUploadResponse,
    BankStatementResponse,
    TransactionReviewItem,
    TransactionBatchCreate
)

router = APIRouter()


@router.post("/statement", response_model=dict)
async def upload_bank_statement(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload de extrato bancário (CSV).
    Retorna transações parseadas para revisão antes de salvar.
    """
    # Validar tipo de arquivo
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos CSV são suportados"
        )

    try:
        # Ler conteúdo do arquivo
        content = await file.read()

        # Detectar banco
        bank_name = parser_service.detect_bank(content)

        # Parse do CSV
        parsed_transactions = parser_service.parse_csv(content)

        if not parsed_transactions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhuma transação encontrada no arquivo"
            )

        # Criar registro de bank statement
        bank_statement = BankStatement(
            user_id=current_user.id,
            filename=file.filename,
            bank_name=bank_name,
            total_transactions=len(parsed_transactions),
            status="pending_review"
        )

        # Calcular período
        if parsed_transactions:
            dates = [datetime.strptime(t["date"], "%Y-%m-%d").date() for t in parsed_transactions]
            bank_statement.period_start = min(dates)
            bank_statement.period_end = max(dates)

        db.add(bank_statement)
        db.commit()
        db.refresh(bank_statement)

        # Buscar categorias do usuário para sugerir
        user_categories = db.query(Category).filter(
            Category.user_id == current_user.id
        ).all()

        category_names = [cat.name for cat in user_categories]

        # Se não tem categorias, criar padrão
        if not category_names:
            default_categories = [
                "Alimentação", "Transporte", "Moradia", "Saúde",
                "Lazer", "Educação", "Compras", "Outros"
            ]
            category_names = default_categories

        # Categorizar transações usando LLM (se disponível)
        transactions_for_review = []
        for idx, trans in enumerate(parsed_transactions):
            suggested_category = None

            # Tentar categorizar com LLM
            try:
                if llm_service.check_availability():
                    suggested_category = await llm_service.categorize_transaction(
                        description=trans["description"],
                        amount=trans["amount"],
                        available_categories=category_names
                    )
            except Exception as e:
                print(f"Erro ao categorizar com LLM: {e}")

            transactions_for_review.append({
                "temp_id": idx,
                "date": trans["date"],
                "description": trans["description"],
                "amount": trans["amount"],
                "suggested_category": suggested_category
            })

        return {
            "bank_statement_id": str(bank_statement.id),
            "filename": file.filename,
            "bank_name": bank_name,
            "total_transactions": len(parsed_transactions),
            "transactions": transactions_for_review,
            "available_categories": category_names
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )


@router.post("/statement/{statement_id}/confirm")
async def confirm_bank_statement(
    statement_id: UUID,
    batch: TransactionBatchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Confirma e salva transações revisadas do extrato.
    """
    # Buscar bank statement
    bank_statement = db.query(BankStatement).filter(
        BankStatement.id == statement_id,
        BankStatement.user_id == current_user.id
    ).first()

    if not bank_statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Extrato não encontrado"
        )

    try:
        # Criar transações em batch
        for trans_data in batch.transactions:
            transaction = Transaction(
                user_id=current_user.id,
                bank_statement_id=bank_statement.id,
                date=trans_data.get("date"),
                description=trans_data.get("description"),
                amount=trans_data.get("amount"),
                category_id=trans_data.get("category_id"),
                is_manual=False,
                is_projection=False
            )
            db.add(transaction)

        # Atualizar status do bank statement
        bank_statement.status = "completed"
        bank_statement.total_transactions = len(batch.transactions)

        db.commit()

        return {
            "message": "Transações importadas com sucesso",
            "total": len(batch.transactions)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar transações: {str(e)}"
        )


@router.get("/statements", response_model=List[BankStatementResponse])
async def list_bank_statements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todos os extratos importados pelo usuário"""
    statements = db.query(BankStatement).filter(
        BankStatement.user_id == current_user.id
    ).order_by(BankStatement.upload_date.desc()).all()

    return statements


@router.delete("/statement/{statement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bank_statement(
    statement_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta um extrato e suas transações associadas"""
    statement = db.query(BankStatement).filter(
        BankStatement.id == statement_id,
        BankStatement.user_id == current_user.id
    ).first()

    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Extrato não encontrado"
        )

    db.delete(statement)
    db.commit()

    return None
