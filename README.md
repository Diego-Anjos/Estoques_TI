# Estoques TI

Sistema de gestão de estoque e ativos de TI — monorepo com API REST, banco Oracle e interface web.

Controle de itens, locais, patrimônios, licenças de software, ocorrências e usuários, com auditoria de criação e alteração.

---

## Tecnologias

| Camada | Stack |
|--------|--------|
| **Backend** | Python, **FastAPI**, Uvicorn, Pydantic, Passlib (bcrypt) |
| **Banco de dados** | **Oracle Database** (Oracle XE via Docker) |
| **Frontend** | **Vite** + páginas estáticas (HTML / CSS / JavaScript) |

---

## Estrutura do monorepo

```text
Estoques TI/
├── Backend/          # API FastAPI + scripts Oracle
│   ├── app/          # Código da aplicação
│   ├── docker-compose.yml
│   ├── init_db.py
│   ├── requirements.txt
│   └── .env.example
├── FrontEnd/         # Interface Vite (páginas estáticas)
│   ├── pages/
│   ├── shared/
│   ├── package.json
│   └── .env.example
└── README.md         # Este arquivo
```

---

## Pré-requisitos

- **Docker** e Docker Compose
- **Python** 3.11+ (ou superior)
- **Node.js** 18+ (com npm)
- Git (opcional)

---

## Como rodar o projeto localmente

Siga as **3 etapas** abaixo, nesta ordem.

### Passo 1: Banco de Dados

Suba o Oracle XE com Docker e inicialize as tabelas.

**1.1.** Entre na pasta do backend e inicie o container:

```bash
cd Backend
docker-compose up -d
```

Aguarde o Oracle ficar pronto (na primeira vez pode levar alguns minutos). O serviço expõe a porta **1521**.

**1.2.** Configure as variáveis de ambiente do backend (valores alinhados ao `docker-compose.yml`):

```bash
# Ainda em Backend/
cp .env.example .env
```

Confira se o `.env` contém algo equivalente a:

```env
ORACLE_USER=estoque_user
ORACLE_PASSWORD=estoque_senha
ORACLE_DSN=localhost:1521/XEPDB1
```

**1.3.** Crie (ou atualize) as tabelas, sequences e triggers:

```bash
# Com o ambiente virtual do Passo 2 já ativo, ou após instalar as deps:
python init_db.py
```

> **Dica:** se preferir, execute o `init_db.py` logo após instalar as dependências do Passo 2 (precisa do `oracledb` e do `.env`).

---

### Passo 2: Backend

**2.1.** Na pasta `Backend`, crie e ative o ambiente virtual:

**Windows (PowerShell):**

```powershell
cd Backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
cd Backend
python3 -m venv .venv
source .venv/bin/activate
```

**2.2.** Instale as dependências:

```bash
pip install -r requirements.txt
```

**2.3.** (Se ainda não rodou) inicialize o schema Oracle:

```bash
python init_db.py
```

**2.4.** Inicie a API com Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará em:

- **API:** http://localhost:8000  
- **Swagger:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  

---

### Passo 3: Frontend

Em **outro terminal**, configure e suba o Vite.

**3.1.** Entre na pasta do frontend e instale as dependências:

```bash
cd FrontEnd
npm install
```

**3.2.** Configure a URL da API:

```bash
cp .env.example .env
```

O padrão aponta para o backend local:

```env
VITE_API_URL=http://localhost:8000/api
```

**3.3.** Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

O frontend abre em **http://localhost:5173** (login em `/pages/auth/login/index.html`).

---

## Resumo rápido

| Etapa | Comando principal | URL / porta |
|-------|-------------------|-------------|
| **1. Banco** | `docker-compose up -d` + `python init_db.py` | `1521` |
| **2. Backend** | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | http://localhost:8000 |
| **3. Frontend** | `npm run dev` | http://localhost:5173 |

---

## Documentação adicional

- Backend: pasta `Backend/` (API, Oracle, migrações)
- Frontend: `FrontEnd/README.md` e `FrontEnd/docs/STRUCTURE.md`

---

**Versão:** 1.0.0 · Uso interno
