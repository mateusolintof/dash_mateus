import ollama
from typing import Optional, List, Dict
from app.core.config import settings


class LLMService:
    def __init__(self, model: str = None):
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = settings.OLLAMA_BASE_URL

    async def categorize_transaction(
        self,
        description: str,
        amount: float,
        available_categories: List[str]
    ) -> str:
        """
        Categoriza uma transação usando LLM.

        Args:
            description: Descrição da transação
            amount: Valor (negativo = despesa, positivo = receita)
            available_categories: Lista de categorias disponíveis

        Returns:
            Nome da categoria sugerida
        """
        category_list = "\n".join(f"- {cat}" for cat in available_categories)

        prompt = f"""Você é um assistente financeiro que categoriza transações.

Categorias disponíveis:
{category_list}

Transação:
- Descrição: {description}
- Valor: R$ {abs(amount):.2f} ({'despesa' if amount < 0 else 'receita'})

Analise a descrição e retorne APENAS o nome exato de UMA categoria da lista acima.
Não adicione explicações, apenas o nome da categoria.

Categoria:"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            category = response['message']['content'].strip()

            # Validar se a categoria existe na lista
            if category in available_categories:
                return category

            # Tentar encontrar correspondência aproximada
            category_lower = category.lower()
            for cat in available_categories:
                if cat.lower() == category_lower:
                    return cat

            # Se não encontrou, retornar a primeira categoria (fallback)
            return available_categories[0] if available_categories else "Outros"

        except Exception as e:
            print(f"Erro ao categorizar com LLM: {e}")
            return available_categories[0] if available_categories else "Outros"

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Conversa com o LLM sobre dados financeiros.

        Args:
            message: Mensagem do usuário
            conversation_history: Histórico de mensagens anteriores

        Returns:
            Resposta do LLM
        """
        messages = conversation_history or []

        # Sistema: contexto do assistente financeiro
        system_message = {
            "role": "system",
            "content": """Você é um assistente financeiro pessoal inteligente.
Ajude o usuário a:
- Entender seus gastos e receitas
- Analisar padrões de consumo
- Fazer previsões financeiras
- Sugerir formas de economizar
- Responder dúvidas sobre finanças pessoais

Seja objetivo, claro e útil. Use português do Brasil."""
        }

        messages.insert(0, system_message)
        messages.append({"role": "user", "content": message})

        try:
            response = ollama.chat(
                model=self.model,
                messages=messages
            )

            return response['message']['content']

        except Exception as e:
            return f"Desculpe, não consegui processar sua mensagem. Erro: {str(e)}"

    async def analyze_transactions(
        self,
        transactions_summary: str,
        user_question: str
    ) -> str:
        """
        Analisa transações e responde pergunta do usuário.

        Args:
            transactions_summary: Resumo das transações em texto
            user_question: Pergunta do usuário

        Returns:
            Análise do LLM
        """
        prompt = f"""Você é um analista financeiro. Com base nos dados abaixo, responda a pergunta do usuário.

DADOS FINANCEIROS:
{transactions_summary}

PERGUNTA DO USUÁRIO:
{user_question}

Forneça uma resposta detalhada e útil, com insights práticos."""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            return response['message']['content']

        except Exception as e:
            return f"Erro ao analisar: {str(e)}"

    def check_availability(self) -> bool:
        """Verifica se o Ollama está disponível"""
        try:
            ollama.list()
            return True
        except:
            return False


# Instância global do serviço
llm_service = LLMService()
