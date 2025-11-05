"""
Script para popular o banco de dados com dados mock para demonstração.

IMPORTANTE: Este script cria um usuário de teste e adiciona dados fictícios.
Use apenas em ambiente de desenvolvimento!

Uso:
    python seed_data.py
"""

from datetime import date, timedelta
from decimal import Decimal
import random

from app.db.session import SessionLocal
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.core.security import get_password_hash


def seed_database():
    db = SessionLocal()

    try:
        print("🌱 Iniciando seed do banco de dados...")

        # 1. Criar usuário de teste
        print("\n1. Criando usuário de teste...")
        test_user = db.query(User).filter(User.email == "teste@exemplo.com").first()

        if test_user:
            print("   ⚠️  Usuário teste@exemplo.com já existe!")
            user_id = test_user.id
        else:
            test_user = User(
                email="teste@exemplo.com",
                name="Usuário Teste",
                hashed_password=get_password_hash("senha123")
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            user_id = test_user.id
            print("   ✅ Usuário criado: teste@exemplo.com / senha123")

        # 2. Criar categorias
        print("\n2. Criando categorias...")
        categories_data = [
            {"name": "Alimentação", "color": "#10b981", "budget_limit": 800},
            {"name": "Transporte", "color": "#3b82f6", "budget_limit": 300},
            {"name": "Moradia", "color": "#8b5cf6", "budget_limit": 1500},
            {"name": "Saúde", "color": "#ef4444", "budget_limit": 400},
            {"name": "Lazer", "color": "#f59e0b", "budget_limit": 500},
            {"name": "Educação", "color": "#06b6d4", "budget_limit": 600},
            {"name": "Compras", "color": "#ec4899", "budget_limit": 700},
            {"name": "Salário", "color": "#22c55e", "budget_limit": None},
            {"name": "Freelance", "color": "#84cc16", "budget_limit": None},
            {"name": "Outros", "color": "#64748b", "budget_limit": 200},
        ]

        categories = {}
        for cat_data in categories_data:
            existing = db.query(Category).filter(
                Category.user_id == user_id,
                Category.name == cat_data["name"]
            ).first()

            if not existing:
                category = Category(user_id=user_id, **cat_data)
                db.add(category)
                db.commit()
                db.refresh(category)
                categories[cat_data["name"]] = category.id
                print(f"   ✅ Categoria criada: {cat_data['name']}")
            else:
                categories[cat_data["name"]] = existing.id
                print(f"   ⚠️  Categoria já existe: {cat_data['name']}")

        # 3. Criar transações dos últimos 3 meses
        print("\n3. Criando transações...")

        # Limpar transações antigas do usuário teste (opcional)
        # db.query(Transaction).filter(Transaction.user_id == user_id).delete()
        # db.commit()

        hoje = date.today()
        transactions_created = 0

        # Gerar transações para os últimos 90 dias
        for i in range(90):
            data_transacao = hoje - timedelta(days=i)

            # Salário mensal (dia 5 de cada mês)
            if data_transacao.day == 5:
                trans = Transaction(
                    user_id=user_id,
                    date=data_transacao,
                    description="Salário",
                    amount=Decimal("5000.00"),
                    category_id=categories["Salário"],
                    is_manual=False,
                    is_projection=False
                )
                db.add(trans)
                transactions_created += 1

            # Freelance (aleatório, ~2x por mês)
            if random.random() < 0.067:  # ~2 vezes por mês
                trans = Transaction(
                    user_id=user_id,
                    date=data_transacao,
                    description=f"Projeto Freelance - {random.choice(['Website', 'App', 'Consultoria', 'Design'])}",
                    amount=Decimal(str(random.randint(800, 2500))),
                    category_id=categories["Freelance"],
                    is_manual=False,
                    is_projection=False
                )
                db.add(trans)
                transactions_created += 1

            # Aluguel (dia 10)
            if data_transacao.day == 10:
                trans = Transaction(
                    user_id=user_id,
                    date=data_transacao,
                    description="Aluguel",
                    amount=Decimal("-1200.00"),
                    category_id=categories["Moradia"],
                    is_manual=False,
                    is_projection=False
                )
                db.add(trans)
                transactions_created += 1

            # Despesas diárias aleatórias
            num_transacoes_dia = random.randint(0, 3)

            for _ in range(num_transacoes_dia):
                categoria_random = random.choice([
                    ("Alimentação", ["Supermercado", "Restaurante", "Padaria", "Delivery", "Feira"], (10, 150)),
                    ("Transporte", ["Uber", "Combustível", "Estacionamento", "Pedágio"], (15, 80)),
                    ("Saúde", ["Farmácia", "Consulta", "Exames", "Academia"], (30, 200)),
                    ("Lazer", ["Cinema", "Show", "Bar", "Netflix", "Spotify"], (20, 150)),
                    ("Educação", ["Livro", "Curso Online", "Material"], (50, 300)),
                    ("Compras", ["Roupas", "Eletrônicos", "Casa", "Amazon"], (50, 500)),
                    ("Outros", ["Presente", "Pet Shop", "Cabelereiro"], (30, 200)),
                ])

                cat_nome, descricoes, faixa_valor = categoria_random
                descricao = random.choice(descricoes)
                valor = Decimal(str(random.randint(*faixa_valor)))

                trans = Transaction(
                    user_id=user_id,
                    date=data_transacao,
                    description=descricao,
                    amount=-valor,
                    category_id=categories[cat_nome],
                    is_manual=False,
                    is_projection=False
                )
                db.add(trans)
                transactions_created += 1

        db.commit()
        print(f"   ✅ {transactions_created} transações criadas!")

        # 4. Estatísticas
        print("\n4. Resumo dos dados:")
        total_income = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.is_projection == False,
            Transaction.amount > 0
        ).count()

        total_expenses = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.is_projection == False,
            Transaction.amount < 0
        ).count()

        print(f"   📊 Total de receitas: {total_income}")
        print(f"   📊 Total de despesas: {total_expenses}")
        print(f"   📊 Total de transações: {total_income + total_expenses}")

        print("\n✅ Seed concluído com sucesso!")
        print("\n🔑 Credenciais para login:")
        print("   Email: teste@exemplo.com")
        print("   Senha: senha123")

    except Exception as e:
        print(f"\n❌ Erro durante seed: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
