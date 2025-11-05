# Dashboard Financeiro Pessoal

Dashboard fullstack para gerenciamento financeiro pessoal com análise inteligente via LLM local.

## Stack Tecnológica

### Frontend
- **Next.js 16** com React 19 e TypeScript
- **Tailwind CSS v4**
- **shadcn/ui** para componentes
- **TanStack Query** para estado do servidor

### Backend
- **FastAPI** (Python 3.12+)
- **SQLAlchemy 2.0** (ORM assíncrono)
- **PostgreSQL 16**
- **JWT** para autenticação
- **Ollama** para LLM local

## Setup Rápido

### Pré-requisitos

- Node.js 18+ e npm/pnpm
- Python 3.12+
- Docker e Docker Compose
- Ollama (para LLM local)

### 1. Clonar e Configurar

```bash
git clone <repo-url>
cd dashboard_mateus
```

### 2. Iniciar Serviços (PostgreSQL + Ollama)

```bash
docker-compose up -d
```

Aguarde os serviços iniciarem:
- PostgreSQL: `localhost:5432`
- Ollama: `localhost:11434`

### 3. Setup do Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt
# ou com Poetry
poetry install

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env se necessário

# Criar e executar migrations
alembic revision --autogenerate -m "initial_migration"
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

Backend estará em: http://localhost:8000
Documentação Swagger: http://localhost:8000/docs

### 4. Setup do Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.local.example .env.local

# Iniciar servidor de desenvolvimento
npm run dev
```

Frontend estará em: http://localhost:3000

### 5. Configurar Ollama (Opcional para Fase 1)

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo recomendado
ollama pull llama3.2:3b

# Verificar se está rodando
ollama list
```

## Estrutura do Projeto

```
dashboard_mateus/
├── frontend/              # Next.js 16 App
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/    # Rotas autenticadas
│   │   │   └── login/          # Login/Register
│   │   ├── components/         # Componentes React
│   │   └── lib/               # Utilitários e API client
│   └── package.json
│
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── core/          # Config, security
│   │   └── services/      # Business logic
│   ├── alembic/           # Migrations
│   └── requirements.txt
│
├── docker-compose.yml     # PostgreSQL + Ollama
├── CLAUDE.md             # Guia para Claude Code
└── README.md             # Este arquivo
```

## Uso

### 1. Criar Conta

Acesse http://localhost:3000 e será redirecionado para `/login`.
Clique em "Criar Conta" e registre-se.

### 2. Adicionar Transações

- Vá para "Transações" no menu
- Clique em "Nova Transação"
- Preencha os dados e escolha Receita ou Despesa
- Salve!

### 3. Próximos Passos

- **Fase 2**: Upload de extratos bancários + categorização automática via LLM
- **Fase 3**: Aba de projeções manuais para simulações
- **Fase 4**: Chat com LLM para análise de dados
- **Fase 5**: Gráficos avançados e previsões

## Endpoints da API

### Autenticação
- `POST /api/auth/register` - Criar conta
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Usuário atual

### Transações
- `GET /api/transactions/` - Listar transações
- `POST /api/transactions/` - Criar transação
- `PUT /api/transactions/{id}` - Atualizar
- `DELETE /api/transactions/{id}` - Deletar
- `GET /api/transactions/stats/summary` - Resumo financeiro

### Categorias
- `GET /api/categories/` - Listar categorias
- `POST /api/categories/` - Criar categoria
- `PUT /api/categories/{id}` - Atualizar
- `DELETE /api/categories/{id}` - Deletar

## Desenvolvimento

### Backend

```bash
# Criar nova migration
cd backend
alembic revision --autogenerate -m "description"

# Aplicar migrations
alembic upgrade head

# Testes
pytest tests/
```

### Frontend

```bash
cd frontend

# Build de produção
npm run build

# Iniciar produção
npm start

# Lint
npm run lint
```

## Troubleshooting

### PostgreSQL não conecta
```bash
docker-compose down
docker-compose up -d postgres
# Aguarde 10 segundos
docker-compose logs postgres
```

### Ollama não responde
```bash
# Verificar status
ollama list

# Reiniciar
pkill ollama
ollama serve
```

### CORS errors no frontend
Certifique-se que o backend está rodando em `localhost:8000` e o frontend em `localhost:3000`.

## Licença

Projeto pessoal - Mateus Olinto

## Próximas Features

- [ ] Upload de extratos bancários (CSV, OFX, PDF)
- [ ] Categorização automática via LLM
- [ ] Aba de projeções manuais ("what-if" scenarios)
- [ ] Chat conversacional com LLM
- [ ] Gráficos avançados (Recharts/Tremor)
- [ ] Previsões de investimento
- [ ] Análise de comprometimento futuro
- [ ] Exportar relatórios PDF
- [ ] Notificações de orçamento
- [ ] Suporte a múltiplas moedas
