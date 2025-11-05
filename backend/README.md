# Dashboard Financeiro - Backend API

Backend FastAPI para o Dashboard Financeiro Pessoal.

## Setup Rápido

### 1. Instalar dependências

```bash
# Com pip
pip install -r requirements.txt

# Ou com Poetry
poetry install
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Iniciar PostgreSQL e Ollama

```bash
# Na raiz do projeto
docker-compose up -d
```

### 4. Criar database e executar migrations

```bash
# Criar primeira migration
alembic revision --autogenerate -m "initial_migration"

# Executar migrations
alembic upgrade head
```

### 5. Iniciar servidor

```bash
uvicorn app.main:app --reload

# Ou com Poetry
poetry run uvicorn app.main:app --reload
```

API estará disponível em: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

## Endpoints Disponíveis

### Autenticação
- POST `/api/auth/register` - Registrar novo usuário
- POST `/api/auth/login` - Login (retorna JWT token)
- GET `/api/auth/me` - Informações do usuário autenticado

### Transações
- GET `/api/transactions/` - Listar transações
- GET `/api/transactions/{id}` - Obter transação
- POST `/api/transactions/` - Criar transação
- PUT `/api/transactions/{id}` - Atualizar transação
- DELETE `/api/transactions/{id}` - Deletar transação
- GET `/api/transactions/stats/summary` - Resumo financeiro

### Categorias
- GET `/api/categories/` - Listar categorias
- GET `/api/categories/{id}` - Obter categoria
- POST `/api/categories/` - Criar categoria
- PUT `/api/categories/{id}` - Atualizar categoria
- DELETE `/api/categories/{id}` - Deletar categoria

## Estrutura do Projeto

```
backend/
├── app/
│   ├── api/              # Endpoints da API
│   ├── core/             # Config, security, deps
│   ├── db/               # Database session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
├── alembic/              # Database migrations
└── tests/                # Testes
```

## Desenvolvimento

```bash
# Criar nova migration após modificar models
alembic revision --autogenerate -m "description"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```
