# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão Geral do Projeto

Dashboard financeiro pessoal fullstack para gerenciamento de despesas, receitas e projeções futuras. O sistema permite:

- Upload mensal de extratos bancários com categorização automática via LLM
- Visualização de gastos por categoria e análise de tendências
- Previsões de investimento e sobra futura
- **Aba especial de projeções manuais** para simulação de cenários futuros (isolada dos dados reais)
- Chat conversacional com LLM para análise de dados financeiros

## Stack Tecnológica (2025)

### Frontend
- **Next.js 15+** com React 19 (App Router, Server Components, Server Actions)
- **TypeScript 5+**
- **Tailwind CSS v4** (nova engine)
- **shadcn/ui v2** ou Magic UI para componentes
- **TanStack Query v5** para gerenciamento de estado servidor
- **Zustand v4** para estado local
- **Recharts v2** ou **Tremor v3** para visualizações financeiras

### Backend
- **Python 3.12+**
- **FastAPI 0.110+** com Pydantic v2
- **SQLAlchemy 2.0+** (async) para ORM
- **Alembic** para migrations
- **Poetry** ou **uv** para gerenciamento de dependências
- **pandas + numpy** para análise de dados
- **uvicorn** como servidor ASGI

### LLM Local
- **Ollama** com modelos locais:
  - **LLaMA 3.2/3.3** para categorização e chat
  - **Mistral 7B** como alternativa rápida
  - **Qwen 2.5** para melhor suporte ao português
- **LangChain** ou **LlamaIndex** para orquestração (opcional)

### Database
- **PostgreSQL 16+**
- Desenvolvimento: Docker local
- Produção: **Neon** (serverless) ou **Supabase** (free tier)

### Deploy
- Frontend: **Vercel** (free tier)
- Backend: **Render** ou **Railway** (free tier)
- Database: **Neon** ou **Supabase**
- LLM: Ollama local (dev), considerar Groq/OpenRouter para produção

## Estrutura do Projeto (Monorepo)

```
dashboard_mateus/
├── frontend/                   # Next.js 15 Application
│   ├── src/
│   │   ├── app/                # App Router
│   │   │   ├── (dashboard)/
│   │   │   │   ├── page.tsx              # Dashboard overview
│   │   │   │   ├── transactions/         # Lista de transações
│   │   │   │   ├── categories/           # Análise por categoria
│   │   │   │   ├── projections/          # 🎯 Aba de projeções manuais
│   │   │   │   ├── chat/                 # Chat com LLM
│   │   │   │   └── settings/             # Configurações
│   │   │   └── api/            # Server Actions (proxy para backend)
│   │   ├── components/
│   │   │   ├── ui/             # shadcn components
│   │   │   ├── charts/         # Gráficos financeiros
│   │   │   └── forms/
│   │   ├── lib/
│   │   │   ├── api-client.ts   # Cliente HTTP para backend
│   │   │   └── utils/
│   │   └── types/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── next.config.js
│
├── backend/                    # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── api/                # API routes
│   │   │   ├── transactions.py
│   │   │   ├── categories.py
│   │   │   ├── projections.py  # 🎯 Endpoints para aba manual
│   │   │   ├── upload.py       # Upload de extratos
│   │   │   └── ai.py           # Endpoints LLM
│   │   ├── models/             # SQLAlchemy models
│   │   │   ├── transaction.py
│   │   │   ├── category.py
│   │   │   ├── projection.py   # Modelo para cenários manuais
│   │   │   └── user.py
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/
│   │   │   ├── llm_service.py       # Integração Ollama
│   │   │   ├── parser_service.py    # Parse de extratos (CSV/OFX/PDF)
│   │   │   └── analysis_service.py  # Cálculos e previsões
│   │   ├── core/
│   │   │   ├── config.py       # Configurações
│   │   │   └── security.py     # Auth JWT
│   │   └── db/
│   │       ├── base.py
│   │       └── session.py
│   ├── alembic/                # Database migrations
│   │   └── versions/
│   ├── tests/
│   ├── pyproject.toml
│   └── requirements.txt
│
├── docker-compose.yml          # PostgreSQL + Ollama local
└── CLAUDE.md                   # Este arquivo
```

## Comandos de Desenvolvimento

### Setup Inicial

```bash
# Clonar e instalar dependências
git clone <repo>
cd dashboard_mateus

# Frontend
cd frontend
npm install
# ou
pnpm install

# Backend
cd ../backend
poetry install
# ou
pip install -r requirements.txt

# Docker (PostgreSQL + Ollama)
docker-compose up -d
```

### Ollama Setup

```bash
# Instalar Ollama (se ainda não instalado)
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelos recomendados
ollama pull llama3.2:3b           # Leve e rápido
ollama pull mistral:7b            # Alternativa robusta
ollama pull qwen2.5:7b            # Melhor suporte português

# Testar
ollama run llama3.2:3b
```

### Desenvolvimento

```bash
# Frontend (porta 3000)
cd frontend
npm run dev

# Backend (porta 8000)
cd backend
uvicorn app.main:app --reload

# Ou com Poetry
poetry run uvicorn app.main:app --reload

# Database migrations
cd backend
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Build e Deploy

```bash
# Frontend build
cd frontend
npm run build
npm start

# Backend (production)
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Docker (tudo junto)
docker-compose -f docker-compose.prod.yml up --build
```

## Arquitetura e Comunicação

### Fluxo de Dados

```
Frontend (Next.js 15) ↔ Backend API (FastAPI) ↔ PostgreSQL
                            ↓
                        Ollama (LLM Local)
```

### API Communication
- **REST API** entre frontend e backend
- Base URL: `http://localhost:8000/api` (dev)
- Autenticação: JWT tokens via headers
- CORS configurado no FastAPI

### Principais Endpoints

```
POST   /api/auth/login
POST   /api/auth/register

GET    /api/transactions              # Lista todas transações
POST   /api/transactions              # Criar manual
GET    /api/transactions/{id}
PUT    /api/transactions/{id}
DELETE /api/transactions/{id}

GET    /api/categories                # Lista categorias
POST   /api/categories                # Criar categoria

POST   /api/upload/statement          # Upload extrato bancário
GET    /api/upload/history

POST   /api/ai/categorize             # Categorizar transação via LLM
POST   /api/ai/chat                   # Chat conversacional
POST   /api/ai/analyze                # Análise de dados

GET    /api/projections               # 🎯 Cenários de projeção
POST   /api/projections               # Criar cenário
PUT    /api/projections/{id}          # Editar cenário
POST   /api/projections/{id}/duplicate # Duplicar para simular
```

## Modelo de Dados (PostgreSQL)

### Principais Tabelas

```sql
-- Usuários e autenticação
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  hashed_password VARCHAR NOT NULL,
  name VARCHAR,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Transações (despesas e receitas)
transactions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  date DATE NOT NULL,
  description TEXT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,  -- Negativo = despesa, Positivo = receita
  category_id UUID REFERENCES categories(id),
  is_manual BOOLEAN DEFAULT false,      -- Entrada manual vs automática
  is_projection BOOLEAN DEFAULT false,  -- 🎯 Pertence à aba de projeções
  projection_id UUID REFERENCES projections(id),
  bank_statement_id UUID REFERENCES bank_statements(id),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Categorias customizáveis
categories (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR NOT NULL,
  color VARCHAR,
  icon VARCHAR,
  budget_limit DECIMAL(10,2),  -- Limite mensal opcional
  created_at TIMESTAMP
)

-- Histórico de uploads de extratos
bank_statements (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  filename VARCHAR NOT NULL,
  file_path VARCHAR,
  upload_date TIMESTAMP,
  bank_name VARCHAR,
  period_start DATE,
  period_end DATE,
  total_transactions INTEGER,
  status VARCHAR  -- 'processing', 'completed', 'error'
)

-- 🎯 Cenários de projeção (aba manual)
projections (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR NOT NULL,           -- "Cenário Conservador", "Se comprar carro"
  description TEXT,
  start_date DATE,
  end_date DATE,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Histórico de chat com LLM
ai_chat_history (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  message TEXT NOT NULL,
  response TEXT NOT NULL,
  model VARCHAR,
  created_at TIMESTAMP
)
```

### Separação de Dados: Real vs Projeções

**Importante**: O sistema distingue três tipos de transações:

1. **Automáticas** (`is_manual=false, is_projection=false`):
   - Vindas de upload de extratos
   - Categorizadas por LLM
   - Base para análises reais

2. **Manuais** (`is_manual=true, is_projection=false`):
   - Entrada manual do usuário
   - Parte dos dados reais

3. **🎯 Projeções** (`is_projection=true`):
   - Exclusivas da aba de projeções manuais
   - Isoladas dos dados reais
   - Usadas para simulações "what-if"
   - Sempre associadas a um `projection_id`

**Queries devem sempre filtrar** por `is_projection` para evitar misturar dados reais com simulações!

## Integração com LLM Local (Ollama)

### Configuração (backend/app/services/llm_service.py)

```python
import ollama

class LLMService:
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model

    async def categorize_transaction(self, description: str, amount: float) -> str:
        """Categoriza transação usando LLM"""
        prompt = f"""
        Categorize esta transação financeira em uma das categorias abaixo.

        Categorias disponíveis:
        - Alimentação
        - Transporte
        - Moradia
        - Saúde
        - Lazer
        - Educação
        - Outros

        Transação: {description}
        Valor: R$ {amount:.2f}

        Responda APENAS com o nome da categoria, sem explicações.
        """

        response = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": prompt}
        ])

        return response['message']['content'].strip()
```

### Casos de Uso do LLM

1. **Categorização de Transações**:
   - Prompt com few-shot learning das categorias do usuário
   - Batch processing ao importar extrato

2. **Chat Conversacional**:
   - RAG (Retrieval Augmented Generation) sobre dados financeiros
   - Exemplos: "Quanto gastei com alimentação em setembro?", "Onde posso economizar?"

3. **Detecção de Anomalias**:
   - Identificar gastos fora do padrão
   - Sugerir ajustes no orçamento

4. **Correção de Categorias**:
   - Interface permite usuário corrigir categoria sugerida pela IA
   - Sistema aprende com correções (future: fine-tuning)

### Considerações de Performance

- **Ollama local**: Ótimo para dev, mas requer GPU/recursos
- **Produção free tier**: Considerar alternativas:
  - **Groq**: Inferência muito rápida, tem tier gratuito
  - **OpenRouter**: Agregador, pay-as-you-go barato
  - **Together AI**: Modelos open-source, preços baixos

## Processamento de Extratos Bancários

### Formatos Suportados

1. **CSV** (mais comum em bancos brasileiros):
   - Nubank, Inter, C6, Itaú
   - Parse com `pandas.read_csv()`

2. **OFX** (Open Financial Exchange):
   - Padrão universal
   - Biblioteca: `ofxparse`

3. **PDF** (futuro):
   - Alguns bancos tradicionais
   - OCR com `pdfplumber` + `pytesseract`

### Pipeline de Importação (backend/app/services/parser_service.py)

```python
async def process_bank_statement(file_path: str, user_id: str):
    # 1. Parse arquivo → DataFrame
    df = parse_csv_statement(file_path)

    # 2. Normalizar colunas (data, descrição, valor)
    transactions = normalize_transactions(df)

    # 3. Batch categorização com LLM
    for tx in transactions:
        tx.category = await llm_service.categorize(tx.description, tx.amount)

    # 4. Salvar no banco com flag is_manual=False
    await db.bulk_insert(transactions)

    # 5. Retornar para interface de revisão
    return transactions
```

### Interface de Revisão (Frontend)

- Após upload, mostrar tabela com transações e categorias sugeridas
- Usuário pode aceitar todas ou corrigir individualmente
- Botão "Confirmar importação" salva definitivamente

## Aba de Projeções Manuais 🎯

### Funcionalidade Especial

Esta é a **aba mais importante** do sistema. Diferente de outras abas que mostram dados reais, aqui o usuário pode:

- Criar cenários "what-if" isolados dos dados reais
- Editar valores livremente sem afetar histórico real
- Simular: "E se eu comprar um carro?", "E se eu economizar 20% a mais?"
- Comparar cenários: Conservador vs Agressivo
- Projetar meses/anos futuros com diferentes premissas

### Implementação

**Frontend** (`app/(dashboard)/projections/page.tsx`):
- Lista de cenários criados
- Botão "Novo Cenário" ou "Duplicar Mês Atual"
- Editor de transações futuras (adicionar/editar/remover)
- Gráficos comparativos: Projetado vs Real

**Backend** (endpoints especiais):
```
GET    /api/projections                    # Lista cenários
POST   /api/projections                    # Criar novo
POST   /api/projections/from-month/{month} # Duplicar mês real
PUT    /api/projections/{id}/transactions  # Editar transações do cenário
GET    /api/projections/{id}/compare       # Comparar com dados reais
```

**Database**:
- Todas transações de projeção têm `is_projection=true`
- Nunca aparecem em queries de dados reais
- Associadas a um `projection_id`

### Visualizações Importantes

- Gráfico de linha: Saldo projetado vs real ao longo do tempo
- Waterfall chart: Como cada categoria afeta o saldo final
- Tabela comparativa: Categoria | Real | Projetado | Diferença

## Segurança e Privacidade

### Dados Financeiros Sensíveis

- **Sempre usar HTTPS** em produção
- JWT tokens com expiração curta (15 min) + refresh tokens
- Senhas com bcrypt (min 10 rounds)
- Rate limiting em endpoints de upload e LLM
- Validação rigorosa de inputs (Pydantic schemas)

### Isolamento de Dados

- Queries sempre filtram por `user_id`
- Foreign keys com ON DELETE CASCADE
- Row Level Security (RLS) no PostgreSQL (se usar Supabase)

### Backups

- PostgreSQL: backups automáticos (Neon/Supabase proveem)
- Permitir usuário exportar dados (CSV/JSON) via API

## Testes

### Backend (pytest)
```bash
cd backend
pytest tests/
pytest tests/test_transactions.py -v
pytest --cov=app tests/
```

### Frontend (Vitest + Testing Library)
```bash
cd frontend
npm test
npm run test:coverage
```

## Troubleshooting Comum

### Ollama não responde
```bash
# Verificar se está rodando
ollama list
curl http://localhost:11434/api/tags

# Reiniciar
pkill ollama
ollama serve
```

### Migrations falhando
```bash
# Reset database (dev only!)
cd backend
alembic downgrade base
alembic upgrade head

# Ou recriar do zero
docker-compose down -v
docker-compose up -d
```

### CORS errors frontend → backend
Verificar `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Recursos e Documentação

- Next.js 15: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- Ollama: https://ollama.ai/docs
- SQLAlchemy 2.0: https://docs.sqlalchemy.org
- Tailwind v4: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com

## Próximas Features (Backlog)

- [ ] Suporte a múltiplas moedas
- [ ] Integração direta com APIs de bancos (Open Banking)
- [ ] Exportar relatórios em PDF
- [ ] App mobile (React Native ou PWA)
- [ ] Notificações de orçamento excedido
- [ ] Gráficos de investimento (rendimento de ações, FIIs)
- [ ] Multi-tenancy (compartilhar com família)
