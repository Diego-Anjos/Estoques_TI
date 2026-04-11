# 🚀 Estoque TI API

Sistema completo de gestão de TI com API REST desenvolvida em Python com FastAPI e Oracle Database.

## 📋 Funcionalidades

- **Controle de Estoque** - Gerenciamento de itens por quantidade (cabos, mousepad, etc.)
- **Controle de Patrimônio** - Itens serializados (PC, Notebook, Monitor, Impressora, Switch, etc.)
- **Controle de Licenças** - Gerenciamento de software (Office, CoopSys, etc.)
- **Sistema de Ocorrências** - Chamados com rastreamento completo
- **Gestão de Usuários** - Autenticação e controle de acesso
- **Auditoria Completa** - Registro de quem criou/alterou cada registro

## 🛠️ Tecnologias

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **Oracle Database** - Banco de dados corporativo
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **Bcrypt** - Hash de senhas

## 📁 Estrutura do Projeto

```
estoque-ti-api/
├── app/
│   ├── main.py                 # Aplicação principal
│   ├── core/                   # Configurações centrais
│   │   ├── config.py          # Configurações (.env)
│   │   ├── database.py        # Pool de conexão Oracle
│   │   └── security.py        # Segurança (hash de senha)
│   ├── schemas/               # DTOs Pydantic
│   │   ├── usuario.py
│   │   ├── item.py
│   │   ├── patrimonio.py
│   │   ├── software.py
│   │   └── ocorrencia.py
│   ├── repositories/          # Acesso ao banco de dados
│   │   ├── usuario_repo.py
│   │   ├── item_repo.py
│   │   ├── estoque_repo.py
│   │   ├── patrimonio_repo.py
│   │   ├── software_repo.py
│   │   └── ocorrencia_repo.py
│   ├── services/              # Lógica de negócio
│   │   ├── usuario_service.py
│   │   ├── estoque_service.py
│   │   ├── patrimonio_service.py
│   │   ├── software_service.py
│   │   └── ocorrencia_service.py
│   └── routers/               # Endpoints da API
│       ├── usuario_router.py
│       ├── item_router.py
│       ├── estoque_router.py
│       ├── patrimonio_router.py
│       ├── software_router.py
│       └── ocorrencia_router.py
├── .env                       # Variáveis de ambiente
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.11 ou superior
- Oracle Database (com as tabelas criadas)
- Git (opcional)

### 2. Clone ou baixe o projeto

```bash
cd estoque-ti-api
```

### 3. Crie o ambiente virtual

**Windows (PowerShell):**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o arquivo .env

Edite o arquivo `.env` na raiz do projeto com suas credenciais do Oracle:

```env
# Configurações do Oracle Database
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=host:1521/servico
ORACLE_POOL_MIN=1
ORACLE_POOL_MAX=5
ORACLE_POOL_INC=1

# Configurações da API
API_TITLE=Estoque TI API
API_VERSION=1.0.0
API_PREFIX=/api
```

**Exemplo de DSN:**
- `192.168.0.10:1521/ORCLPDB1`
- `localhost:1521/XE`

### 6. Crie as tabelas no Oracle

Você precisa criar as seguintes tabelas no Oracle Database:

- `USUARIOS` - Usuários do sistema
- `ITENS` - Catálogo de itens
- `ESTOQUE` - Controle de quantidade
- `PATRIMONIO` - Itens serializados
- `SOFTWARE` - Licenças de software
- `OCORRENCIAS` - Chamados

**Estrutura básica das tabelas:**

Cada tabela deve ter os campos de auditoria:
- `CRIADO_EM` (TIMESTAMP)
- `CRIADO_POR` (NUMBER)
- `ALTERADO_EM` (TIMESTAMP)
- `ALTERADO_POR` (NUMBER)

## ▶️ Executando a API

### Modo desenvolvimento (com reload automático):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Ou simplesmente:

```bash
python -m app.main
```

### Modo produção:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI (interativo):** http://localhost:8000/docs
- **ReDoc (documentação):** http://localhost:8000/redoc

## 🔌 Endpoints Principais

### Usuários (`/api/usuarios`)
- `POST /` - Criar usuário
- `POST /login` - Login
- `GET /` - Listar usuários
- `GET /{id}` - Buscar usuário
- `PUT /{id}` - Atualizar usuário
- `DELETE /{id}` - Deletar usuário

### Itens (`/api/itens`)
- `POST /` - Criar item
- `GET /` - Listar itens (filtro por tipo)
- `GET /{id}` - Buscar item
- `PUT /{id}` - Atualizar item
- `DELETE /{id}` - Deletar item

### Estoque (`/api/estoque`)
- `POST /` - Criar registro de estoque
- `GET /` - Listar estoque
- `GET /{id}` - Buscar estoque
- `POST /entrada` - Entrada de itens
- `POST /saida` - Saída de itens
- `DELETE /{id}` - Deletar estoque

### Patrimônio (`/api/patrimonio`)
- `POST /` - Criar patrimônio
- `GET /` - Listar patrimônios (filtro por status)
- `GET /{id}` - Buscar patrimônio
- `PUT /{id}` - Atualizar patrimônio
- `DELETE /{id}` - Deletar patrimônio

### Software/Licenças (`/api/software`)
- `POST /` - Criar software
- `GET /` - Listar softwares
- `GET /{id}` - Buscar software
- `PUT /{id}` - Atualizar software
- `POST /{id}/alocar` - Alocar licenças
- `POST /{id}/liberar` - Liberar licenças
- `DELETE /{id}` - Deletar software

### Ocorrências (`/api/ocorrencias`)
- `POST /` - Criar ocorrência
- `GET /` - Listar ocorrências (filtros por status/tipo)
- `GET /{id}` - Buscar ocorrência
- `PUT /{id}` - Atualizar ocorrência
- `POST /{id}/fechar` - Fechar ocorrência
- `DELETE /{id}` - Deletar ocorrência

## ✅ Validações Implementadas

- ✅ **Estoque não fica negativo** - Validação na saída de itens
- ✅ **Licenças não excedem pool** - Validação ao alocar licenças
- ✅ **Número de série único** - Validação no patrimônio
- ✅ **Email único** - Validação de usuários
- ✅ **Senhas com hash bcrypt** - Segurança

## 🔒 Segurança

- Senhas armazenadas com hash bcrypt
- Validação de dados com Pydantic
- Tratamento de erros apropriado
- Pool de conexões gerenciado

## 🐛 Troubleshooting

### Erro de conexão com Oracle

Verifique:
1. Credenciais no arquivo `.env`
2. Oracle Database está rodando
3. Firewall/rede permite conexão
4. DSN está correto (formato: `host:porta/servico`)

### Erro ao importar módulos

```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de permissão no PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📝 Licença

Este projeto é de uso interno.

## 👨‍💻 Desenvolvido com

- FastAPI
- Python
- Oracle Database
- ❤️ e ☕

---

**Versão:** 1.0.0  
**Data:** 2026
