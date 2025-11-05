# 🚀 Guia de Implementação - Dashboard Financeiro

Este guia detalha **passo a passo** como configurar e executar o projeto em sua máquina.

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

### Obrigatórios:
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
- **Git** ([Download](https://git-scm.com/downloads))

### Opcional (para funcionalidade de IA):
- **Ollama** ([Download](https://ollama.com/download))

---

## 🔧 Passo 1: Clonar o Projeto

```bash
# Clone o repositório (substitua pela URL real)
git clone <url-do-repositorio>
cd dashboard_mateus
```

---

## 🐳 Passo 2: Iniciar Serviços (Docker)

O projeto usa Docker para rodar PostgreSQL e Ollama localmente.

```bash
# Iniciar containers em segundo plano
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

**O que isso faz:**
- Inicia PostgreSQL na porta `5432`
- Inicia Ollama na porta `11434`

**Aguarde 10-15 segundos** para os serviços iniciarem completamente.

---

## 🐍 Passo 3: Configurar o Backend (Python/FastAPI)

### 3.1 Instalar Poetry

O projeto usa **Poetry** para gerenciamento de dependências (padrão Python 2025).

```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Verificar instalação
poetry --version

# Adicionar ao PATH (se necessário)
export PATH="$HOME/.local/bin:$PATH"
```

**Windows:**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### 3.2 Instalar Dependências

```bash
cd backend

# Instalar todas as dependências
poetry install

# Ativar ambiente virtual (opcional - Poetry cria automaticamente)
poetry shell
```

**O que isso faz:**
- Cria ambiente virtual isolado automaticamente
- Instala todas as dependências do `pyproject.toml`
- Resolve conflitos de versão automaticamente
- Gera `poetry.lock` para reprodutibilidade

### 3.3 Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# O arquivo .env já está configurado para desenvolvimento
# Você pode editá-lo se necessário:
# - DATABASE_URL (default: localhost:5432)
# - SECRET_KEY (trocar em produção!)
# - OLLAMA_BASE_URL (default: localhost:11434)
```

### 3.3 Criar Banco de Dados

```bash
# Criar migration inicial
alembic revision --autogenerate -m "initial_migration"

# Aplicar migration (cria tabelas)
alembic upgrade head
```

**O que isso faz:**
- Cria todas as tabelas no PostgreSQL (users, transactions, categories, etc.)

### 3.5 Popular com Dados Mock (Opcional)

```bash
# Executar script de seed
poetry run python seed_data.py
```

**Resultado:**
- Cria usuário: `teste@exemplo.com` / senha: `senha123`
- Adiciona ~200-300 transações fictícias dos últimos 3 meses
- Cria 10 categorias padrão

### 3.6 Iniciar Servidor Backend

```bash
# Iniciar servidor de desenvolvimento
poetry run uvicorn app.main:app --reload
```

**Servidor rodando em:** http://localhost:8000

**Documentação da API:** http://localhost:8000/docs

---

## ⚛️ Passo 4: Configurar o Frontend (Next.js)

Abra um **novo terminal** (deixe o backend rodando no anterior).

### 4.1 Instalar Dependências

```bash
cd frontend

# Instalar pacotes
npm install
```

### 4.2 Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.local.example .env.local

# O arquivo já está configurado:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4.3 Iniciar Servidor Frontend

```bash
# Iniciar servidor de desenvolvimento
npm run dev
```

**Aplicação rodando em:** http://localhost:3000

---

## 🤖 Passo 5: Configurar Ollama (IA - Opcional)

A funcionalidade de chat com IA requer o Ollama rodando localmente.

### 5.1 Instalar Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Baixe o instalador em https://ollama.com/download
```

### 5.2 Baixar Modelo

```bash
# Baixar modelo recomendado (leve e rápido)
ollama pull llama3.2:3b

# Verificar se foi instalado
ollama list
```

### 5.3 Testar

```bash
# Teste rápido
ollama run llama3.2:3b

# Digite uma mensagem e veja a resposta
# Pressione Ctrl+D para sair
```

**Nota:** O Ollama roda automaticamente em background após a instalação.

---

## ✅ Passo 6: Testar o Sistema

### 6.1 Acessar a Aplicação

Abra o navegador em: **http://localhost:3000**

### 6.2 Fazer Login

Se você executou o seed (Passo 3.4):
- **Email:** teste@exemplo.com
- **Senha:** senha123

Caso contrário, clique em "Criar Conta" e registre-se.

### 6.3 Funcionalidades Disponíveis

Após login, você terá acesso a:

1. **Dashboard** - Visão geral com gráficos
2. **Transações** - Adicionar/visualizar receitas e despesas
3. **Categorias** - Criar e gerenciar categorias
4. **Projeções** - Criar cenários "what-if"
5. **Chat IA** (botão flutuante no canto inferior direito)

---

## 🔄 Comandos Úteis

### Backend (Poetry)

```bash
# Criar nova migration após alterar models
poetry run alembic revision --autogenerate -m "descricao"

# Aplicar migrations
poetry run alembic upgrade head

# Reverter última migration
poetry run alembic downgrade -1

# Executar todos os testes
poetry run pytest tests/

# Executar testes específicos
poetry run pytest tests/test_auth.py
poetry run pytest tests/test_transactions.py

# Executar com cobertura
poetry run pytest tests/ --cov=app --cov-report=html

# Executar com mais detalhes
poetry run pytest tests/ -v -s

# Adicionar nova dependência
poetry add requests

# Adicionar dependência de desenvolvimento
poetry add --group dev black

# Atualizar todas as dependências
poetry update

# Atualizar dependência específica
poetry update fastapi

# Ver dependências instaladas
poetry show

# Ativar shell do ambiente virtual
poetry shell
```

### Frontend

```bash
# Build de produção
npm run build

# Rodar build
npm start

# Lint
npm run lint
```

### Docker

```bash
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Reiniciar apenas PostgreSQL
docker-compose restart postgres

# Acessar PostgreSQL diretamente
docker exec -it dashboard_postgres psql -U postgres -d dashboard_db
```

---

## 🐛 Troubleshooting

### Backend não inicia

**Erro:** `ModuleNotFoundError: No module named 'app'`

**Solução:**
```bash
cd backend
poetry install
```

**Erro:** `poetry: command not found`

**Solução:**
```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"
```

---

### PostgreSQL não conecta

**Erro:** `FATAL:  database "dashboard_db" does not exist`

**Solução:**
```bash
# Parar containers
docker-compose down

# Remover volumes
docker-compose down -v

# Subir novamente
docker-compose up -d

# Aguardar 10 segundos e criar database
cd backend
alembic upgrade head
```

---

### Ollama não responde

**Erro:** `Serviço de IA não disponível`

**Solução:**
```bash
# Verificar se Ollama está rodando
ollama list

# Se não estiver:
ollama serve

# Ou reiniciar
pkill ollama
ollama serve
```

---

### CORS Error no Frontend

**Erro:** `Access to fetch at 'http://localhost:8000' has been blocked by CORS`

**Solução:**
Certifique-se que:
1. Backend está rodando em `localhost:8000`
2. Frontend está rodando em `localhost:3000`
3. O arquivo `backend/app/core/config.py` tem:
   ```python
   CORS_ORIGINS: List[str] = ["http://localhost:3000"]
   ```

---

### Port já está em uso

**Erro:** `Port 3000 is already in use`

**Solução:**
```bash
# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

## 📦 Deploy (Produção)

### Backend (Render / Railway)

1. Criar conta no [Render](https://render.com) ou [Railway](https://railway.app)
2. Conectar repositório Git
3. Configurar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Adicionar PostgreSQL database addon
5. Configurar variáveis de ambiente:
   - `DATABASE_URL` (auto-gerado pelo addon)
   - `SECRET_KEY` (gerar novo: `openssl rand -hex 32`)
   - `CORS_ORIGINS` (URL do frontend em produção)

### Frontend (Vercel)

1. Criar conta no [Vercel](https://vercel.com)
2. Importar repositório
3. Configurar:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
4. Adicionar variável de ambiente:
   - `NEXT_PUBLIC_API_URL` = URL do backend em produção

---

## 📚 Recursos Adicionais

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação Next.js 15](https://nextjs.org/docs)
- [Documentação Ollama](https://ollama.ai/docs)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

---

## ❓ Precisa de Ajuda?

- Leia o `README.md` para visão geral
- Leia o `CLAUDE.md` para detalhes técnicos
- Leia o `EXPLICACAO_LEIGOS.md` para entender o projeto
- Verifique os logs: `docker-compose logs -f`

---

## ✨ Próximos Passos

Após configurar tudo:

1. ✅ Teste todas as funcionalidades
2. ✅ Explore a documentação da API em `/docs`
3. ✅ Experimente o chat com IA
4. ✅ Crie suas próprias categorias
5. ✅ Adicione suas transações reais
6. ✅ Crie cenários de projeção

**Divirta-se usando seu dashboard financeiro! 🎉**
