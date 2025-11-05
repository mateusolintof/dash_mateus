"""
Testes para transações
"""
import pytest
from fastapi import status
from datetime import date
from decimal import Decimal


@pytest.fixture
def test_transaction(db, test_user):
    """Criar transação de teste"""
    from app.models.transaction import Transaction

    transaction = Transaction(
        user_id=test_user.id,
        date=date(2025, 1, 15),
        description="Test Transaction",
        amount=Decimal("-100.00"),
        is_manual=True,
        is_projection=False
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def test_create_transaction(client, auth_headers):
    """Testar criação de transação"""
    response = client.post(
        "/api/transactions",
        headers=auth_headers,
        json={
            "date": "2025-01-20",
            "description": "New Transaction",
            "amount": -50.00,
            "is_manual": True,
            "is_projection": False
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["description"] == "New Transaction"
    assert float(data["amount"]) == -50.00
    assert "id" in data


def test_list_transactions(client, auth_headers, test_transaction):
    """Testar listagem de transações"""
    response = client.get(
        "/api/transactions?is_projection=false",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "transactions" in data
    assert "total" in data
    assert data["total"] >= 1
    assert len(data["transactions"]) >= 1


def test_get_transaction(client, auth_headers, test_transaction):
    """Testar obter transação por ID"""
    response = client.get(
        f"/api/transactions/{test_transaction.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["description"] == "Test Transaction"


def test_get_nonexistent_transaction(client, auth_headers):
    """Testar obter transação inexistente"""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        f"/api/transactions/{fake_uuid}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_transaction(client, auth_headers, test_transaction):
    """Testar atualização de transação"""
    response = client.put(
        f"/api/transactions/{test_transaction.id}",
        headers=auth_headers,
        json={
            "description": "Updated Transaction",
            "amount": -150.00
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["description"] == "Updated Transaction"
    assert float(data["amount"]) == -150.00


def test_delete_transaction(client, auth_headers, test_transaction):
    """Testar deleção de transação"""
    response = client.delete(
        f"/api/transactions/{test_transaction.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar se foi deletada
    get_response = client.get(
        f"/api/transactions/{test_transaction.id}",
        headers=auth_headers
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_transaction_summary(client, auth_headers, test_transaction):
    """Testar resumo de transações"""
    response = client.get(
        "/api/transactions/stats/summary?is_projection=false",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_income" in data
    assert "total_expenses" in data
    assert "balance" in data
    assert "total_transactions" in data


def test_transaction_pagination(client, auth_headers, test_transaction):
    """Testar paginação de transações"""
    # Criar mais transações
    for i in range(15):
        client.post(
            "/api/transactions",
            headers=auth_headers,
            json={
                "date": "2025-01-20",
                "description": f"Transaction {i}",
                "amount": -10.00,
                "is_manual": True,
                "is_projection": False
            }
        )

    # Testar paginação
    response = client.get(
        "/api/transactions?skip=0&limit=10&is_projection=false",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["transactions"]) == 10
    assert data["total"] > 10


def test_unauthorized_access(client):
    """Testar acesso não autorizado"""
    response = client.get("/api/transactions")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
