from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.ai_chat import AIChatHistory
from app.models.transaction import Transaction
from app.services.llm_service import llm_service
from app.schemas.ai_chat import ChatRequest, ChatResponse, AIChatHistoryResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat com LLM sobre dados financeiros.
    O LLM tem contexto das transações do usuário.
    """
    try:
        # Verificar disponibilidade do LLM
        if not llm_service.check_availability():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de IA não disponível. Certifique-se de que o Ollama está rodando."
            )

        # Preparar histórico de conversação
        conversation_history = []
        if chat_request.conversation_history:
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.conversation_history
            ]

        # Obter resposta do LLM
        response = await llm_service.chat(
            message=chat_request.message,
            conversation_history=conversation_history
        )

        # Salvar no histórico
        chat_history = AIChatHistory(
            user_id=current_user.id,
            message=chat_request.message,
            response=response,
            model=llm_service.model
        )
        db.add(chat_history)
        db.commit()

        return {
            "message": response,
            "timestamp": datetime.utcnow()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar chat: {str(e)}"
        )


@router.post("/analyze")
async def analyze_transactions(
    question: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Análise de transações com pergunta específica.
    O LLM recebe um resumo das transações e responde a pergunta.
    """
    try:
        if not llm_service.check_availability():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de IA não disponível"
            )

        # Buscar transações do usuário (últimos 3 meses)
        from datetime import date, timedelta
        three_months_ago = date.today() - timedelta(days=90)

        transactions = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            Transaction.is_projection == False,
            Transaction.date >= three_months_ago
        ).all()

        # Criar resumo das transações
        if not transactions:
            summary = "Nenhuma transação registrada nos últimos 3 meses."
        else:
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = sum(abs(t.amount) for t in transactions if t.amount < 0)

            # Agrupar por categoria
            by_category = {}
            for t in transactions:
                cat_name = t.category.name if t.category else "Sem categoria"
                if cat_name not in by_category:
                    by_category[cat_name] = {"count": 0, "total": 0}
                by_category[cat_name]["count"] += 1
                by_category[cat_name]["total"] += abs(t.amount)

            summary = f"""
RESUMO FINANCEIRO (Últimos 3 meses):
- Total de transações: {len(transactions)}
- Receitas totais: R$ {total_income:.2f}
- Despesas totais: R$ {total_expenses:.2f}
- Saldo: R$ {total_income - total_expenses:.2f}

GASTOS POR CATEGORIA:
"""
            for cat, data in sorted(by_category.items(), key=lambda x: x[1]["total"], reverse=True):
                summary += f"- {cat}: R$ {data['total']:.2f} ({data['count']} transações)\n"

        # Obter análise do LLM
        response = await llm_service.analyze_transactions(
            transactions_summary=summary,
            user_question=question
        )

        return {
            "question": question,
            "answer": response,
            "timestamp": datetime.utcnow()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao analisar: {str(e)}"
        )


@router.get("/chat/history", response_model=List[AIChatHistoryResponse])
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna histórico de conversas com a IA"""
    history = db.query(AIChatHistory).filter(
        AIChatHistory.user_id == current_user.id
    ).order_by(AIChatHistory.created_at.desc()).limit(limit).all()

    return history


@router.get("/status")
async def get_ai_status():
    """Verifica se o serviço de IA está disponível"""
    available = llm_service.check_availability()

    return {
        "available": available,
        "model": llm_service.model if available else None,
        "message": "Serviço de IA disponível" if available else "Ollama não está rodando"
    }
