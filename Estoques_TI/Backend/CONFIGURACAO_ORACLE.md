# 🔧 Configuração do Banco de Dados Oracle

Este documento descreve como configurar a conexão com o banco de dados Oracle para o sistema de Gestão de Estoque TI.

---

## 📋 Pré-requisitos

1. **Oracle Database** instalado e rodando (versão 11g ou superior)
2. **Python 3.8+** instalado
3. **Dependências Python** instaladas (veja `requirements.txt`)

---

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas no Oracle:

| Tabela | Descrição |
|--------|-----------|
| `ESTOQUES_TI_USUARIOS` | Usuários do sistema |
| `ESTOQUES_TI_LOCAIS` | Locais físicos (almoxarifados, salas, etc) |
| `ESTOQUES_TI_TIPOS_ITEM` | Tipos de itens (PC, Monitor, Cabo, etc) |
| `ESTOQUES_TI_ITENS` | Catálogo de itens |
| `ESTOQUES_TI_ESTOQUE_SALDO` | Saldo de estoque por local |
| `ESTOQUES_TI_MOVIMENTACOES` | Histórico de movimentações |
| `ESTOQUES_TI_PATRIMONIOS` | Itens serializados (patrimônio) |
| `ESTOQUES_TI_PATRIMONIO_ATR` | Atributos flexíveis dos patrimônios |
| `ESTOQUES_TI_SOFTWARES` | Catálogo de softwares |
| `ESTOQUES_TI_SOFTWARE_LICENCAS` | Pools de licenças |
| `ESTOQUES_TI_ATRIBUICOES` | Atribuições de licenças |
| `ESTOQUES_TI_OCORRENCIAS` | Sistema de chamados/ocorrências |

---

## ⚙️ Configuração Passo a Passo

### 1️⃣ Criar o Schema no Oracle

Execute o script SQL fornecido em `DB/Banco de Dados Sistema Controle de Estoque.sql` no seu banco Oracle:

```sql
-- Conecte-se ao Oracle como usuário com privilégios
sqlplus usuario/senha@host:porta/servico

-- Execute o script
@"caminho/para/Banco de Dados Sistema Controle de Estoque.sql"
```

Isso criará:
- ✅ Todas as tabelas
- ✅ Sequences para auto-incremento
- ✅ Triggers para IDs automáticos
- ✅ Constraints e índices

### 2️⃣ Configurar Variáveis de Ambiente

Edite o arquivo `.env` na pasta `Backend/`:

```env
# Configurações do Oracle Database
ORACLE_USER=seu_usuario_oracle
ORACLE_PASSWORD=sua_senha_oracle
ORACLE_DSN=host:1521/nome_servico

# Configurações do Pool de Conexões
ORACLE_POOL_MIN=1
ORACLE_POOL_MAX=5
ORACLE_POOL_INC=1

# Configurações da API
API_TITLE=Estoque TI API
API_VERSION=1.0.0
API_PREFIX=/api
```

**Formato do DSN:**
- `localhost:1521/XEPDB1` - Para Oracle XE local
- `192.168.1.100:1521/ORCL` - Para Oracle remoto
- `servidor.empresa.com:1521/PROD` - Para servidor de produção

### 3️⃣ Testar a Conexão

Execute o script de teste:

```bash
cd Backend
python test_connection.py
```

**Saída esperada:**
```
================================================================================
🔍 TESTE DE CONEXÃO COM ORACLE DATABASE
================================================================================

📋 Verificando configurações...
   ORACLE_USER: seu_usuario
   ORACLE_PASSWORD: **********
   ORACLE_DSN: localhost:1521/XEPDB1

🔌 Tentando conectar ao banco de dados...
✅ Conexão estabelecida com sucesso!

📊 Versão do Oracle: Oracle Database 19c Enterprise Edition...
👤 Usuário conectado: SEU_USUARIO

================================================================================
📦 VERIFICANDO TABELAS
================================================================================

   ✅ ESTOQUES_TI_USUARIOS              (0 registros)
   ✅ ESTOQUES_TI_LOCAIS                (0 registros)
   ✅ ESTOQUES_TI_TIPOS_ITEM            (0 registros)
   ...

================================================================================
📊 RESUMO
================================================================================
   Tabelas encontradas: 12/12
   Sequences encontradas: 10/10

✅ TODAS AS TABELAS E SEQUENCES ESTÃO PRESENTES!
🎉 Banco de dados configurado corretamente!
```

---

## 🚀 Iniciar a API

Após configurar o banco de dados:

```bash
cd Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔍 Troubleshooting

### ❌ Erro: "ORA-12154: TNS:could not resolve the connect identifier"

**Causa:** DSN incorreto ou serviço Oracle não encontrado

**Solução:**
1. Verifique se o Oracle está rodando
2. Confirme o nome do serviço: `lsnrctl status`
3. Teste a conexão: `tnsping nome_servico`

### ❌ Erro: "ORA-01017: invalid username/password"

**Causa:** Credenciais incorretas

**Solução:**
1. Verifique usuário e senha no `.env`
2. Teste login manual: `sqlplus usuario/senha@dsn`

### ❌ Erro: "ORA-00942: table or view does not exist"

**Causa:** Tabelas não foram criadas ou usuário sem permissão

**Solução:**
1. Execute o script SQL de criação das tabelas
2. Verifique permissões: `GRANT SELECT, INSERT, UPDATE, DELETE ON tabela TO usuario;`

### ❌ Erro: "DPI-1047: Cannot locate a 64-bit Oracle Client library"

**Causa:** Oracle Instant Client não instalado

**Solução:**
1. Baixe o Oracle Instant Client: https://www.oracle.com/database/technologies/instant-client/downloads.html
2. Extraia e configure a variável de ambiente `PATH`
3. Reinicie o terminal/IDE

---

## 📚 Recursos Adicionais

### Estrutura de Conexão

O sistema usa um **pool de conexões** gerenciado pelo `oracledb`:

```python
# app/core/database.py
pool = oracledb.create_pool(
    user=settings.ORACLE_USER,
    password=settings.ORACLE_PASSWORD,
    dsn=settings.ORACLE_DSN,
    min=1,  # Mínimo de conexões
    max=5,  # Máximo de conexões
    increment=1  # Incremento
)
```

### Context Managers

Use os context managers para operações no banco:

```python
# Para obter uma conexão
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ESTOQUES_TI_USUARIOS")
    
# Para obter um cursor (com commit automático)
with get_cursor() as cursor:
    cursor.execute("INSERT INTO ESTOQUES_TI_USUARIOS ...")
    # commit automático ao sair do bloco
```

### Nomenclatura das Tabelas

Todos os repositories usam constantes para nomes de tabelas:

```python
# app/repositories/usuario_repo.py
TABLE_NAME = "ESTOQUES_TI_USUARIOS"

# Uso em queries
sql = f"SELECT * FROM {TABLE_NAME} WHERE ID_USUARIO = :id"
```

---

## 🔐 Segurança

### Boas Práticas

1. ✅ **Nunca commite o arquivo `.env`** com credenciais reais
2. ✅ Use **variáveis de ambiente** em produção
3. ✅ Crie um **usuário específico** para a aplicação (não use SYS/SYSTEM)
4. ✅ Conceda apenas as **permissões necessárias**
5. ✅ Use **senhas fortes** e rotacione periodicamente

### Permissões Mínimas

```sql
-- Criar usuário para a aplicação
CREATE USER estoque_ti_app IDENTIFIED BY senha_forte;

-- Conceder permissões
GRANT CONNECT, RESOURCE TO estoque_ti_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON estoques_ti_usuarios TO estoque_ti_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON estoques_ti_locais TO estoque_ti_app;
-- ... repita para todas as tabelas
```

---

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs da aplicação
2. Execute `python test_connection.py` para diagnóstico
3. Consulte a documentação do Oracle: https://docs.oracle.com/en/database/
4. Verifique os logs do Oracle: `$ORACLE_HOME/diag/rdbms/`

---

**Última atualização:** 12/02/2026
