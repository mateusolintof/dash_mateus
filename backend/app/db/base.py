from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importar todos os modelos aqui para que o Alembic possa detectá-los
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.projection import Projection
from app.models.bank_statement import BankStatement
from app.models.ai_chat import AIChatHistory
