# 🚀 Guia Completo - Setup Backend com Poetry (100%)

## 📋 Pré-requisitos

Antes de começar, certifique-se que tem instalado:
- ✅ Python 3.12+
- ✅ Docker Desktop (rodando)
- ✅ Git

---

## 🎯 Passo 1: Instalar Poetry

### macOS/Linux:

```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Adicionar ao PATH permanentemente
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Recarregar shell
source ~/.zshrc

# Verificar instalação
poetry --version
```

**Saída esperada:** `Poetry (version 1.8.0)` ou superior

### Windows:

```powershell
# PowerShell (executar como administrador)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Adicionar ao PATH manualmente ou reiniciar terminal

# Verificar
poetry --version
```

---

## 🐳 Passo 2: Iniciar Docker (PostgreSQL e Ollama)

```bash
# Navegar para pasta raiz do projeto
cd /Users/mateusolinto/IA\ -\ Projetos\ Pessoais/dashboard_mateus

# Verificar se Docker está rodando
docker --version

# Iniciar containers em segundo plano
docker-compose up -d

# Verificar se subiram corretamente
docker-compose ps
```

**Saída esperada:**
```
NAME                 STATUS          PORTS
dashboard_postgres   Up 10 seconds   0.0.0.0:5432->5432/tcp
dashboard_ollama     Up 10 seconds   0.0.0.0:11434->11434/tcp
```

**Aguarde 10-15 segundos** para os serviços iniciarem completamente.

---

## 🐍 Passo 3: Configurar Backend com Poetry

### 3.1 Navegar para pasta backend

```bash
cd backend
```

**Seu caminho atual deve ser:**
`/Users/mateusolinto/IA - Projetos Pessoais/dashboard_mateus/backend`

### 3.2 Remover venv antigo (se existir)

```bash
# Remover ambiente virtual antigo
rm -rf venv/

# Limpar cache Python
rm -rf __pycache__/
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

### 3.3 Configurar Poetry para criar venv dentro do projeto (opcional)

```bash
# Configurar Poetry para criar .venv dentro do projeto
poetry config virtualenvs.in-project true

# Verificar configuração
poetry config --list | grep virtualenvs
```

**Saída esperada:**
```
virtualenvs.in-project = true
```

### 3.4 Instalar todas as dependências

```bash
# Instalar dependências de produção + desenvolvimento
poetry install
```

**O que acontece:**
- Poetry cria ambiente virtual automaticamente
- Instala todas as dependências do `pyproject.toml`
- Resolve conflitos de versão
- Gera `poetry.lock` para reprodutibilidade

**Saída esperada (final):**
```
Installing dependencies from lock file

Package operations: 50 installs, 0 updates, 0 removals

  • Installing fastapi (0.121.0)
  • Installing sqlalchemy (2.0.44)
  • Installing pydantic (2.12.4)
  • Installing pytest (8.3.0)
  ...

Installing the current project: dashboard-backend (0.1.0)
```

**Tempo estimado:** 2-5 minutos

### 3.5 Verificar instalação

```bash
# Ver todas as dependências instaladas
poetry show

# Ver dependências principais
poetry show --tree

# Verificar versões específicas
poetry show fastapi sqlalchemy pydantic httpx
```

**Saída esperada:**
```
fastapi       0.121.0
sqlalchemy    2.0.44
pydantic      2.12.4
httpx         0.27.2
```

---

## 🔐 Passo 4: Configurar Variáveis de Ambiente

### 4.1 Criar arquivo .env

```bash
# Gerar SECRET_KEY aleatória e criar .env
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dashboard_db
SECRET_KEY=$(openssl rand -hex 32)
OLLAMA_BASE_URL=http://localhost:11434
EOF
```

### 4.2 Verificar arquivo criado

```bash
# Ver conteúdo
cat .env
```

**Saída esperada:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dashboard_db
SECRET_KEY=a1b2c3d4e5f6...
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 🗄️ Passo 5: Criar Banco de Dados

### 5.1 Verificar conexão com PostgreSQL

```bash
# Testar conexão
docker exec -it dashboard_postgres psql -U postgres -c "SELECT version();"
```

**Saída esperada:** Versão do PostgreSQL

### 5.2 Executar migrations

```bash
# Aplicar migrations (criar todas as tabelas)
poetry run alembic upgrade head
```

**Saída esperada:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, initial migration
```

### 5.3 Verificar tabelas criadas

```bash
# Listar tabelas
docker exec -it dashboard_postgres psql -U postgres -d dashboard_db -c "\dt"
```

**Saída esperada:**
```
              List of relations
 Schema |        Name        | Type  |  Owner
--------+--------------------+-------+----------
 public | alembic_version    | table | postgres
 public | users              | table | postgres
 public | transactions       | table | postgres
 public | categories         | table | postgres
 public | projections        | table | postgres
 public | bank_statements    | table | postgres
 public | ai_chat_history    | table | postgres
```

---

## 🌱 Passo 6: Popular com Dados de Teste (Opcional)

```bash
# Executar script de seed
poetry run python seed_data.py
```

**O que isso faz:**
- ✅ Cria usuário: `teste@exemplo.com` / senha: `senha123`
- ✅ Cria 10 categorias padrão (Alimentação, Transporte, etc.)
- ✅ Gera ~200-300 transações dos últimos 90 dias
- ✅ Distribui valores realistas por categoria

**Saída esperada:**
```
Criando usuário de teste...
Criando categorias...
Criando transações...
✓ Seed completo!
  - 1 usuário criado
  - 10 categorias criadas
  - 287 transações criadas
```

---

## 🧪 Passo 7: Executar Testes (Opcional)

```bash
# Executar todos os testes
poetry run pytest tests/ -v

# Com cobertura
poetry run pytest tests/ --cov=app --cov-report=html

# Ver relatório de cobertura
open htmlcov/index.html  # macOS
```

**Saída esperada:**
```
tests/test_auth.py::test_register_user PASSED
tests/test_auth.py::test_login_success PASSED
tests/test_transactions.py::test_create_transaction PASSED
...

============ 17 passed in 2.34s ============
```

---

## 🚀 Passo 8: Iniciar Servidor Backend

```bash
# Iniciar servidor de desenvolvimento
poetry run uvicorn app.main:app --reload
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Servidor rodando em:** http://localhost:8000
**Documentação da API:** http://localhost:8000/docs

### 8.1 Testar API

Abra outro terminal e teste:

```bash
# Testar endpoint de health check
curl http://localhost:8000/

# Resultado esperado: {"message": "Dashboard API"}
```

Ou acesse no navegador: http://localhost:8000/docs

---

## ✅ Verificação Final

### Checklist de Sucesso:

```bash
# 1. Poetry instalado?
poetry --version
# ✅ Deve mostrar versão

# 2. Docker rodando?
docker-compose ps
# ✅ Ambos containers "Up"

# 3. Dependências instaladas?
poetry show | wc -l
# ✅ Deve mostrar ~50 pacotes

# 4. Banco criado?
docker exec dashboard_postgres psql -U postgres -d dashboard_db -c "\dt" | grep users
# ✅ Deve mostrar tabela users

# 5. Servidor rodando?
curl -s http://localhost:8000/ | grep "Dashboard"
# ✅ Deve retornar JSON

# 6. Usuário de teste existe?
docker exec dashboard_postgres psql -U postgres -d dashboard_db -c "SELECT email FROM users;"
# ✅ Deve mostrar teste@exemplo.com
```

---

## 🔄 Comandos Úteis do Dia-a-Dia

### Gerenciar Dependências:

```bash
# Adicionar nova dependência
poetry add requests

# Adicionar dependência de desenvolvimento
poetry add --group dev black

# Atualizar todas as dependências
poetry update

# Atualizar dependência específica
poetry update fastapi

# Remover dependência
poetry remove requests
```

### Ambiente Virtual:

```bash
# Ativar shell do Poetry (opcional)
poetry shell

# Executar comando no ambiente virtual (sem ativar shell)
poetry run python script.py

# Desativar shell
exit
```

### Testes:

```bash
# Rodar todos os testes
poetry run pytest tests/

# Teste específico
poetry run pytest tests/test_auth.py::test_login_success

# Com mais detalhes
poetry run pytest tests/ -v -s

# Parar no primeiro erro
poetry run pytest tests/ -x
```

### Migrations:

```bash
# Criar nova migration
poetry run alembic revision --autogenerate -m "add new field"

# Aplicar migrations
poetry run alembic upgrade head

# Reverter última migration
poetry run alembic downgrade -1

# Ver histórico
poetry run alembic history
```

### Docker:

```bash
# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Reiniciar apenas PostgreSQL
docker-compose restart postgres
```

---

## 🛑 Para Parar Tudo

```bash
# 1. Parar servidor backend (no terminal do uvicorn)
Ctrl + C

# 2. Parar Docker
docker-compose down

# 3. Sair do Poetry shell (se estiver dentro)
exit
```

---

## 🔄 Próximas Vezes - Iniciar Rápido

Quando voltar a trabalhar no projeto:

```bash
# 1. Ir para pasta backend
cd /Users/mateusolinto/IA\ -\ Projetos\ Pessoais/dashboard_mateus/backend

# 2. Subir Docker (da pasta raiz)
cd .. && docker-compose up -d && cd backend

# 3. Iniciar servidor
poetry run uvicorn app.main:app --reload
```

**Em um único comando:**

```bash
cd /Users/mateusolinto/IA\ -\ Projetos\ Pessoais/dashboard_mateus && docker-compose up -d && cd backend && poetry run uvicorn app.main:app --reload
```

---

## 🐛 Troubleshooting

### Erro: `poetry: command not found`

```bash
# Adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Erro: `Port 8000 is already in use`

```bash
# Encontrar processo usando a porta
lsof -ti:8000

# Matar processo
lsof -ti:8000 | xargs kill -9
```

### Erro: `Connection refused` ao PostgreSQL

```bash
# Verificar se container está rodando
docker-compose ps

# Reiniciar PostgreSQL
docker-compose restart postgres

# Aguardar 10 segundos
sleep 10
```

### Erro: Conflito de dependências

```bash
# Limpar cache do Poetry
poetry cache clear pypi --all

# Remover lock
rm poetry.lock

# Reinstalar
poetry install
```

### Erro: `ModuleNotFoundError: No module named 'app'`

```bash
# Certifique-se de estar na pasta backend
cd backend

# Reinstalar com Poetry
poetry install

# Executar com poetry run
poetry run uvicorn app.main:app --reload
```

---

## 📚 Resumo de Arquivos Importantes

```
backend/
├── pyproject.toml          # Configuração Poetry + Dependências
├── poetry.lock            # Lock file (gerado automaticamente)
├── .env                   # Variáveis de ambiente (você cria)
├── alembic/               # Migrations do banco
├── app/                   # Código da aplicação
├── tests/                 # Testes automatizados
└── seed_data.py          # Script para popular DB
```

---

## 🎉 Próximo Passo: Frontend

Após o backend configurado, configure o frontend:

```bash
# Abrir NOVO terminal
cd /Users/mateusolinto/IA\ -\ Projetos\ Pessoais/dashboard_mateus/frontend

# Instalar dependências
npm install

# Iniciar servidor
npm run dev
```

**Frontend:** http://localhost:3000
**Login:** teste@exemplo.com / senha123

---

## 🧪 Testando a Integração Completa

Com backend e frontend rodando:

1. **Acesse:** http://localhost:3000
2. **Login:** teste@exemplo.com / senha123
3. **Explore:**
   - Dashboard com gráficos
   - Transações (criar, editar, deletar)
   - Categorias
   - Upload de extratos
   - Chat com IA (botão flutuante)

---

## 📊 Status do Projeto

### ✅ Funcionalidades Implementadas

- [x] Autenticação JWT
- [x] CRUD de Transações com paginação
- [x] CRUD de Categorias
- [x] Upload de extratos bancários
- [x] Categorização automática com IA
- [x] Dashboard com visualizações avançadas (Pie, Line, Bar)
- [x] Chat flutuante com IA
- [x] Projeções (cenários what-if)
- [x] Testes automatizados
- [x] Skeleton loaders
- [x] Toast notifications
- [x] Docker setup completo

### 📦 Tecnologias

**Backend:**
- Python 3.12+ / Poetry
- FastAPI 0.121.0
- SQLAlchemy 2.0.44
- PostgreSQL 16
- Ollama (IA local)
- Pytest (testes)

**Frontend:**
- Next.js 16
- React 19
- TypeScript 5
- Tailwind CSS v4
- shadcn/ui
- Recharts

---

## 📝 Notas Importantes

### Sobre o Poetry

- **Poetry** é o gerenciador de dependências padrão Python em 2025 (PEP 621)
- Substitui `pip` + `requirements.txt` por `pyproject.toml`
- Resolve conflitos de dependências automaticamente
- Cria ambiente virtual isolado automaticamente
- `poetry.lock` garante reprodutibilidade

### Sobre Testes

- Dependências de teste estão em `[tool.poetry.group.dev.dependencies]`
- **Não precisa** de `requirements-test.txt` separado
- `poetry install` instala **tudo** (produção + dev)
- `poetry install --only main` instala apenas produção

### Sobre Migrations

- Alembic gerencia schema do banco de dados
- Sempre criar migration após alterar models
- **Nunca** editar migrations geradas manualmente
- Usar `upgrade head` para aplicar, `downgrade -1` para reverter

### Sobre Docker

- PostgreSQL: dados persistem em volume
- Ollama: baixa modelos na primeira vez (demorado)
- `docker-compose down -v` **apaga todos os dados**

---

## 🆘 Precisa de Ajuda?

**Documentação:**
- [Poetry](https://python-poetry.org/docs/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Next.js](https://nextjs.org/docs)

**Arquivos do Projeto:**
- `CLAUDE.md` - Detalhes técnicos para IA
- `GUIA_IMPLEMENTACAO.md` - Guia técnico completo
- `EXPLICACAO_LEIGOS.md` - Explicação para não-técnicos

---

**Pronto! Seu ambiente está 100% configurado! 🎉**

Se encontrar qualquer erro, copie a mensagem completa e peça ajuda com o contexto!
