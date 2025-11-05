# 📖 Explicação para Leigos - Dashboard Financeiro

Este documento explica **em linguagem simples** o que é este projeto, o que foi feito e como funciona.

---

## 🤔 O que é este projeto?

Este é um **sistema completo de gerenciamento financeiro pessoal** que você pode acessar pelo navegador (como acessar Facebook ou Gmail).

**Imagine um aplicativo como:**
- 💚 **Mobills** (controle financeiro)
- 💙 **GuiaBolso** (organização de gastos)
- 🟣 **Organizze** (planejamento financeiro)

...mas que você mesmo **controla**, **personaliza** e roda no seu computador ou na internet!

---

## 🎯 O que ele faz?

### 1. Controle Financeiro Básico ✅

- **Registrar receitas** (salário, freelance, vendas)
- **Registrar despesas** (aluguel, supermercado, Uber)
- **Ver saldo** (quanto você tem disponível)

### 2. Organização por Categorias 📊

- Criar categorias personalizadas (Alimentação, Transporte, Lazer, etc.)
- Ver quanto você gasta em cada categoria
- Definir limites de gastos por categoria

### 3. Importação de Extratos 📄

- Fazer upload do extrato do banco (arquivo CSV)
- O sistema lê automaticamente e registra todas as transações
- Uma **inteligência artificial** categoriza cada gasto automaticamente
- Você revisa e confirma antes de salvar

### 4. Projeções Futuras 🔮

Essa é a **funcionalidade mais legal**!

Você pode criar "cenários" para simular o futuro:
- "E se eu comprasse um carro?"
- "Como ficaria meu orçamento com 20% menos gastos?"
- "Se eu mudar de apartamento, quanto sobra?"

Essas simulações **não afetam seus dados reais** - é como ter um "bloco de rascunho" para testar ideias!

### 5. Chat com Inteligência Artificial 🤖

Um botão flutuante aparece em todas as telas.

Você pode perguntar coisas como:
- "Quanto gastei com alimentação este mês?"
- "Onde posso economizar?"
- "Estou gastando muito?"

A IA analisa seus dados e responde!

### 6. Gráficos e Visualizações 📈

- Ver receitas vs despesas em gráficos de barras
- Acompanhar tendências ao longo do tempo
- Identificar padrões de gastos

---

## 🏗️ Como foi construído?

O projeto é dividido em **3 partes principais**:

### 1. Frontend (O que você vê) 👁️

**O que é:** A "cara" do sistema - as telas, botões, formulários que você clica.

**Tecnologias usadas:**
- **Next.js 16** - Framework moderno para criar sites rápidos
- **React 19** - Biblioteca para criar interfaces interativas
- **Tailwind CSS v4** - Ferramenta para deixar tudo bonito
- **shadcn/ui** - Componentes prontos (botões, cards, modais)

**Analogia:** É como a pintura, decoração e móveis de uma casa.

---

### 2. Backend (O cérebro) 🧠

**O que é:** A parte que processa tudo, guarda dados, faz cálculos.

**Tecnologias usadas:**
- **Python 3.12** - Linguagem de programação popular
- **FastAPI** - Framework rápido para criar APIs (sistemas que fornecem dados)
- **SQLAlchemy** - Ferramenta para conversar com o banco de dados
- **Ollama** - Sistema para rodar IA localmente

**Analogia:** É como a estrutura, encanamento e fiação elétrica de uma casa.

---

### 3. Banco de Dados (A memória) 💾

**O que é:** Onde todos os seus dados são guardados de forma organizada.

**Tecnologia usada:**
- **PostgreSQL 16** - Sistema profissional de banco de dados

**O que é guardado:**
- Suas contas (usuário e senha criptografada)
- Todas as transações (receitas e despesas)
- Categorias criadas por você
- Cenários de projeção
- Histórico de conversas com a IA

**Analogia:** É como um arquivo gigante e super organizado.

---

## 🔄 Como tudo funciona junto?

Vamos usar um **exemplo real** para entender:

### Exemplo: Você adiciona uma despesa de R$ 50,00 no supermercado

#### **Passo 1: Você preenche o formulário (Frontend)**
- Abre a tela de "Transações"
- Clica em "Nova Transação"
- Preenche: Data, Descrição: "Supermercado", Valor: 50,00
- Escolhe "Despesa"
- Clica em "Salvar"

#### **Passo 2: O Frontend manda para o Backend**
- O Next.js pega os dados do formulário
- Envia via internet para o Backend
- É como enviar uma carta pelo correio

#### **Passo 3: O Backend processa**
- FastAPI recebe os dados
- Valida se está tudo certo (data válida, valor numérico, etc.)
- Transforma a despesa em número negativo (-50,00)

#### **Passo 4: Salva no Banco de Dados**
- SQLAlchemy pega os dados processados
- Insere uma nova linha na tabela "transactions"
- PostgreSQL salva permanentemente

#### **Passo 5: Confirmação volta para você**
- Backend manda resposta: "Salvo com sucesso!"
- Frontend recebe e mostra: "Transação adicionada!"
- Atualiza a lista automaticamente

**Tudo isso acontece em menos de 1 segundo!** ⚡

---

## 🤖 Como funciona a Inteligência Artificial?

### O que é Ollama?

**Ollama** é um programa que roda **modelos de IA** (como ChatGPT) **no seu computador**.

**Vantagens:**
- ✅ Totalmente privado (seus dados não saem do seu PC)
- ✅ Grátis (não paga por uso de API)
- ✅ Funciona offline

**Modelo usado:** LLaMA 3.2 (criado pela Meta/Facebook)

### Exemplo 1: Categorização Automática

Quando você importa um extrato:

```
Entrada: "UBER *TRIP SAO PAULO"
```

O sistema pergunta para a IA:

```
"Olá IA, esta transação 'UBER *TRIP SAO PAULO'
de R$ -25,00 se encaixa em qual categoria?

Categorias disponíveis:
- Alimentação
- Transporte
- Moradia
- Lazer

Responda apenas o nome da categoria."
```

IA responde:
```
"Transporte"
```

### Exemplo 2: Chat Conversacional

Você pergunta no chat:

```
"Quanto gastei com alimentação este mês?"
```

O sistema:
1. Busca todas as transações do mês da categoria "Alimentação"
2. Soma os valores
3. Monta um resumo
4. Envia para a IA junto com sua pergunta
5. IA responde de forma natural:

```
"Você gastou R$ 850,00 com alimentação este mês.
Isso representa 17% do seu orçamento total.
Comparado ao mês passado, você gastou R$ 100,00 a mais."
```

---

## 📁 Estrutura de Arquivos (O que cada pasta faz)

```
dashboard_mateus/
├── frontend/           # Telas e interface
│   ├── src/
│   │   ├── app/        # Páginas (Dashboard, Login, Transações...)
│   │   ├── components/ # Pedaços reutilizáveis (Botões, Cards...)
│   │   └── lib/        # Ferramentas auxiliares
│   └── package.json    # Lista de dependências (bibliotecas)
│
├── backend/            # Lógica e processamento
│   ├── app/
│   │   ├── api/        # Rotas (pontos de entrada da API)
│   │   ├── models/     # Definição das tabelas do banco
│   │   ├── services/   # Lógica de negócio (IA, parser, etc.)
│   │   └── core/       # Configurações e segurança
│   └── alembic/        # Histórico de mudanças no banco
│
├── docker-compose.yml  # Receita para rodar PostgreSQL e Ollama
│
├── README.md           # Introdução ao projeto
├── CLAUDE.md           # Guia técnico detalhado
├── GUIA_IMPLEMENTACAO.md   # Como instalar e rodar
└── EXPLICACAO_LEIGOS.md    # Este arquivo!
```

---

## 🔐 Como a Segurança Funciona?

### 1. Senha Criptografada 🔒

Quando você cria uma conta com senha "senha123":
- O sistema **não guarda** "senha123" literalmente
- Usa um algoritmo chamado **bcrypt**
- Transforma em algo como: `$2b$12$KIXxX8...` (impossível reverter)

Quando você faz login:
- Digita sua senha
- Sistema transforma novamente
- Compara as duas versões transformadas
- Se bater, você entra!

### 2. Token de Autenticação 🎫

Após login, o sistema gera um **token JWT** (como um ingresso de cinema):
- Válido por 30 minutos
- Contém seu ID de usuário
- É enviado em toda requisição
- Backend verifica se é válido

### 3. Isolamento de Dados 🏰

Todas as queries do banco incluem seu `user_id`:
```sql
SELECT * FROM transactions WHERE user_id = seu_id
```

**Resultado:** Você **nunca** vê dados de outro usuário!

---

## ❓ Perguntas Frequentes

### P: Meus dados ficam no meu computador?

**R:** Sim e não.
- Em **desenvolvimento** (localhost): Tudo no seu PC
- Em **produção** (deploy): No servidor que você escolher (Vercel, Render)

Mas você tem controle total - pode hospedar onde quiser!

---

### P: Preciso pagar para usar?

**R:** Não! Tudo é gratuito:
- Código: Open source
- Hospedagem: Há opções gratuitas (Vercel, Render, Railway)
- IA: Roda localmente (Ollama)

---

### P: É seguro para dados financeiros reais?

**R:** Sim, seguindo boas práticas:
- ✅ Senhas criptografadas
- ✅ Comunicação HTTPS
- ✅ Tokens de autenticação
- ✅ Validação de dados
- ⚠️ Troque o `SECRET_KEY` em produção!

---

### P: Funciona no celular?

**R:** Sim! O site é **responsivo** (se adapta a qualquer tela):
- ✅ Desktop
- ✅ Tablet
- ✅ Smartphone

Para app nativo, seria necessário criar versão mobile (React Native).

---

### P: Posso modificar o código?

**R:** Sim! Todo o código é seu. Pode:
- Adicionar novas funcionalidades
- Mudar cores e layout
- Criar novas categorias padrão
- Integrar com outros sistemas

---

### P: E se eu não tenho Ollama instalado?

**R:** O sistema funciona normalmente!
- ✅ Todas as funcionalidades principais funcionam
- ❌ Apenas o chat com IA fica indisponível
- ❌ Categorização automática não funciona

Você pode instalar depois quando quiser.

---

## 🎓 O que você aprendeu com este projeto?

Este projeto demonstra conceitos importantes:

### 1. Arquitetura de Software
- Separação Frontend/Backend
- API REST
- Banco de dados relacional
- Docker containers

### 2. Segurança
- Criptografia de senhas
- Autenticação JWT
- Proteção de rotas
- Validação de dados

### 3. Inteligência Artificial
- Modelos LLM
- Processamento de linguagem natural
- Categorização automática
- RAG (Retrieval Augmented Generation)

### 4. Boas Práticas
- Código organizado
- Documentação completa
- Testes automatizados
- Versionamento (Git)

---

## 🚀 Tecnologias por Analogia

Para entender melhor, compare com coisas do dia a dia:

| Tecnologia | Analogia |
|------------|----------|
| **Next.js** | Motor do carro (faz tudo rodar) |
| **React** | Painel do carro (interface) |
| **Tailwind CSS** | Pintura e acabamento |
| **FastAPI** | Mecânico (processa tudo) |
| **PostgreSQL** | Baú do tesouro (guarda tudo) |
| **Ollama/LLM** | Assistente pessoal (IA) |
| **Docker** | Container de carga (isola cada peça) |
| **Alembic** | Diário de reformas (histórico) |

---

## 🎉 Conclusão

Este é um **projeto profissional completo** que demonstra:

✅ Frontend moderno e responsivo
✅ Backend robusto e escalável
✅ Banco de dados bem estruturado
✅ Integração com IA
✅ Segurança adequada
✅ Documentação detalhada

**Você pode usar para:**
- Controlar suas finanças pessoais
- Aprender desenvolvimento web
- Adicionar ao seu portfólio
- Base para outros projetos
- Mostrar em entrevistas de emprego

---

**Divirta-se explorando seu dashboard financeiro!** 🎊💰📊
