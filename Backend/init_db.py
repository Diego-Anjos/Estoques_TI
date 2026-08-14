"""
Inicializa o schema Oracle do Sistema Estoques TI.

Cria sequences, tabelas (prefixo ESTOQUES_TI_), triggers de ID e constraints.
Idempotente: ignora objetos que já existem (ORA-00955 / ORA-02260 etc.).

Uso (na pasta Backend, com venv ativo):
    python init_db.py
"""
from __future__ import annotations

import os
import sys

# Evita UnicodeEncodeError no console Windows (cp1252) com emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import oracledb
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

# ---------------------------------------------------------------------------
# DDL — ordem respeita FKs
# ---------------------------------------------------------------------------

SEQUENCES = [
    ("ESTOQUES_TI_SEQ_USR", "Sequence de ID_USUARIO"),
    ("ESTOQUES_TI_SEQ_LOC", "Sequence de ID_LOCAL"),
    ("ESTOQUES_TI_SEQ_TPI", "Sequence de ID_TIPO_ITEM"),
    ("ESTOQUES_TI_SEQ_IT", "Sequence de ID_ITEM"),
    ("ESTOQUES_TI_SEQ_EMV", "Sequence de ID_MOVIMENTACAO"),
    ("ESTOQUES_TI_SEQ_PAT", "Sequence de ID_PATRIMONIO"),
    ("ESTOQUES_TI_SEQ_SW", "Sequence de ID_SOFTWARE"),
    ("ESTOQUES_TI_SEQ_SLP", "Sequence de ID_POOL"),
    ("ESTOQUES_TI_SEQ_SAT", "Sequence de ID_ATRIBUICAO"),
    ("ESTOQUES_TI_SEQ_OCO", "Sequence de ID_OCORRENCIA"),
]

TABLES_DDL = [
    # 1. Usuários
    """
    CREATE TABLE ESTOQUES_TI_USUARIOS (
        ID_USUARIO      NUMBER          NOT NULL,
        NOME            VARCHAR2(150)   NOT NULL,
        EMAIL           VARCHAR2(200)   NOT NULL,
        SENHA_HASH      VARCHAR2(255)   NOT NULL,
        CARGO           VARCHAR2(100),
        ATIVO           CHAR(1)         DEFAULT 'S' NOT NULL,
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_USR PRIMARY KEY (ID_USUARIO),
        CONSTRAINT UK_EST_USR_EMAIL UNIQUE (EMAIL),
        CONSTRAINT CK_EST_USR_ATIVO CHECK (ATIVO IN ('S', 'N'))
    )
    """,
    # 2. Locais
    """
    CREATE TABLE ESTOQUES_TI_LOCAIS (
        ID_LOCAL        NUMBER          NOT NULL,
        NOME            VARCHAR2(120)   NOT NULL,
        SETOR           VARCHAR2(80),
        DESCRICAO       VARCHAR2(300),
        STATUS          VARCHAR2(20)    DEFAULT 'Ativo',
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_LOC PRIMARY KEY (ID_LOCAL)
    )
    """,
    # 3. Tipos de item
    """
    CREATE TABLE ESTOQUES_TI_TIPOS_ITEM (
        ID_TIPO_ITEM    NUMBER          NOT NULL,
        CODIGO          VARCHAR2(40)    NOT NULL,
        NOME            VARCHAR2(120)   NOT NULL,
        CATEGORIA       VARCHAR2(80),
        DESCRICAO       VARCHAR2(400),
        STATUS          VARCHAR2(20)    DEFAULT 'Ativo',
        SERIALIZADO     CHAR(1)         DEFAULT 'N' NOT NULL,
        UNIDADE         VARCHAR2(30)    DEFAULT 'UN' NOT NULL,
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_TPI PRIMARY KEY (ID_TIPO_ITEM),
        CONSTRAINT UK_EST_TPI_COD UNIQUE (CODIGO),
        CONSTRAINT CK_EST_TPI_SER CHECK (SERIALIZADO IN ('S', 'N'))
    )
    """,
    # 4. Itens (catálogo)
    """
    CREATE TABLE ESTOQUES_TI_ITENS (
        ID_ITEM         NUMBER          NOT NULL,
        ID_TIPO_ITEM    NUMBER,
        NOME            VARCHAR2(200)   NOT NULL,
        TIPO            VARCHAR2(120),
        MARCA           VARCHAR2(120),
        MODELO          VARCHAR2(120),
        DESCRICAO       VARCHAR2(400),
        QUANTIDADE      NUMBER          DEFAULT 0 NOT NULL,
        UNIDADE         VARCHAR2(30)    DEFAULT 'UN' NOT NULL,
        ID_LOCAL        NUMBER,
        STATUS          VARCHAR2(20)    DEFAULT 'Ativo',
        ESTOQUE_MINIMO  NUMBER          DEFAULT 0 NOT NULL,
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_IT PRIMARY KEY (ID_ITEM),
        CONSTRAINT FK_EST_IT_TIPO FOREIGN KEY (ID_TIPO_ITEM)
            REFERENCES ESTOQUES_TI_TIPOS_ITEM (ID_TIPO_ITEM),
        CONSTRAINT FK_EST_IT_LOC FOREIGN KEY (ID_LOCAL)
            REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL),
        CONSTRAINT CK_EST_IT_MIN CHECK (ESTOQUE_MINIMO >= 0),
        CONSTRAINT CK_EST_IT_QTD CHECK (QUANTIDADE >= 0)
    )
    """,
    # 5. Saldo de estoque (PK composta — sem sequence)
    """
    CREATE TABLE ESTOQUES_TI_ESTOQUE_SALDO (
        ID_ITEM         NUMBER          NOT NULL,
        ID_LOCAL        NUMBER          NOT NULL,
        QUANTIDADE      NUMBER          DEFAULT 0 NOT NULL,
        DATA_ALTERACAO  TIMESTAMP       DEFAULT SYSTIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_SAL PRIMARY KEY (ID_ITEM, ID_LOCAL),
        CONSTRAINT FK_EST_SAL_ITEM FOREIGN KEY (ID_ITEM)
            REFERENCES ESTOQUES_TI_ITENS (ID_ITEM),
        CONSTRAINT FK_EST_SAL_LOC FOREIGN KEY (ID_LOCAL)
            REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL),
        CONSTRAINT CK_EST_SAL_QTD CHECK (QUANTIDADE >= 0)
    )
    """,
    # 6. Movimentações
    """
    CREATE TABLE ESTOQUES_TI_MOVIMENTACOES (
        ID_MOVIMENTACAO     NUMBER          NOT NULL,
        ID_ITEM             NUMBER          NOT NULL,
        ID_LOCAL_ORIGEM     NUMBER,
        ID_LOCAL_DESTINO    NUMBER,
        QUANTIDADE          NUMBER          NOT NULL,
        TIPO_MOVIMENTACAO   VARCHAR2(20)    NOT NULL,
        MOTIVO              VARCHAR2(300),
        SETOR_DESTINO       VARCHAR2(80),
        SETOR_ORIGEM        VARCHAR2(80),
        DOCUMENTO_REF       VARCHAR2(80),
        DATA_CRIACAO        TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR          NUMBER,
        CONSTRAINT PK_EST_EMV PRIMARY KEY (ID_MOVIMENTACAO),
        CONSTRAINT FK_EST_EMV_ITEM FOREIGN KEY (ID_ITEM)
            REFERENCES ESTOQUES_TI_ITENS (ID_ITEM),
        CONSTRAINT FK_EST_EMV_ORIG FOREIGN KEY (ID_LOCAL_ORIGEM)
            REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL),
        CONSTRAINT FK_EST_EMV_DEST FOREIGN KEY (ID_LOCAL_DESTINO)
            REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL),
        CONSTRAINT FK_EST_EMV_USR FOREIGN KEY (CRIADO_POR)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT CK_EST_EMV_TIPO CHECK (
            TIPO_MOVIMENTACAO IN ('ENTRADA', 'SAIDA', 'TRANSFERENCIA', 'AJUSTE', 'DEVOLUCAO')
        ),
        CONSTRAINT CK_EST_EMV_QTD CHECK (QUANTIDADE > 0)
    )
    """,
    # 7. Patrimônios
    """
    CREATE TABLE ESTOQUES_TI_PATRIMONIOS (
        ID_PATRIMONIO       NUMBER          NOT NULL,
        ID_ITEM             NUMBER          NOT NULL,
        NUMERO_SERIE        VARCHAR2(120),
        NUMERO_PATRIMONIO   VARCHAR2(120),
        STATUS              VARCHAR2(20)    DEFAULT 'EM_ESTOQUE' NOT NULL,
        ID_LOCAL            NUMBER          NOT NULL,
        ID_USUARIO_ALOCADO  NUMBER,
        DATA_COMPRA         DATE,
        DATA_FIM_GARANTIA   DATE,
        OBSERVACOES         VARCHAR2(400),
        DATA_CRIACAO        TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR          NUMBER,
        DATA_ALTERACAO      TIMESTAMP,
        ALTERADO_POR        NUMBER,
        CONSTRAINT PK_EST_PAT PRIMARY KEY (ID_PATRIMONIO),
        CONSTRAINT FK_EST_PAT_ITEM FOREIGN KEY (ID_ITEM)
            REFERENCES ESTOQUES_TI_ITENS (ID_ITEM),
        CONSTRAINT FK_EST_PAT_LOC FOREIGN KEY (ID_LOCAL)
            REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL),
        CONSTRAINT FK_EST_PAT_USR FOREIGN KEY (ID_USUARIO_ALOCADO)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT UK_EST_PAT_SERIE UNIQUE (NUMERO_SERIE),
        CONSTRAINT CK_EST_PAT_ST CHECK (
            STATUS IN ('EM_ESTOQUE', 'EM_USO', 'MANUTENCAO', 'EXTRAVIADO', 'DESCARTADO')
        )
    )
    """,
    # 8. Atributos de patrimônio (PK composta — sem sequence)
    """
    CREATE TABLE ESTOQUES_TI_PATRIMONIO_ATR (
        ID_PATRIMONIO   NUMBER          NOT NULL,
        NOME_ATRIBUTO   VARCHAR2(60)    NOT NULL,
        VALOR_ATRIBUTO  VARCHAR2(200)   NOT NULL,
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP,
        CRIADO_POR      NUMBER,
        CONSTRAINT PK_EST_PAT_ATR PRIMARY KEY (ID_PATRIMONIO, NOME_ATRIBUTO),
        CONSTRAINT FK_EST_PAT_ATR FOREIGN KEY (ID_PATRIMONIO)
            REFERENCES ESTOQUES_TI_PATRIMONIOS (ID_PATRIMONIO)
    )
    """,
    # 9. Softwares (catálogo)
    """
    CREATE TABLE ESTOQUES_TI_SOFTWARES (
        ID_SOFTWARE     NUMBER          NOT NULL,
        NOME            VARCHAR2(120)   NOT NULL,
        FABRICANTE      VARCHAR2(120),
        DESCRICAO       VARCHAR2(300),
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_SW PRIMARY KEY (ID_SOFTWARE)
    )
    """,
    # 10. Pools de licenças
    """
    CREATE TABLE ESTOQUES_TI_SOFTWARE_LICENCAS (
        ID_POOL         NUMBER          NOT NULL,
        ID_SOFTWARE     NUMBER          NOT NULL,
        TOTAL_LICENCAS  NUMBER          NOT NULL,
        CONTRATO_REF    VARCHAR2(100),
        DATA_EXPIRACAO  DATE,
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER,
        DATA_ALTERACAO  TIMESTAMP,
        ALTERADO_POR    NUMBER,
        CONSTRAINT PK_EST_SLP PRIMARY KEY (ID_POOL),
        CONSTRAINT FK_EST_SLP_SW FOREIGN KEY (ID_SOFTWARE)
            REFERENCES ESTOQUES_TI_SOFTWARES (ID_SOFTWARE),
        CONSTRAINT CK_EST_SLP_TOT CHECK (TOTAL_LICENCAS >= 0)
    )
    """,
    # 11. Atribuições de licença
    """
    CREATE TABLE ESTOQUES_TI_ATRIBUICOES (
        ID_ATRIBUICAO   NUMBER          NOT NULL,
        ID_POOL         NUMBER          NOT NULL,
        ID_USUARIO      NUMBER,
        ID_PATRIMONIO   NUMBER,
        DATA_ATRIBUICAO DATE            NOT NULL,
        DATA_REMOCAO    DATE,
        OBSERVACOES     VARCHAR2(300),
        DATA_CRIACAO    TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        CRIADO_POR      NUMBER          NOT NULL,
        CONSTRAINT PK_EST_SAT PRIMARY KEY (ID_ATRIBUICAO),
        CONSTRAINT FK_EST_SAT_POOL FOREIGN KEY (ID_POOL)
            REFERENCES ESTOQUES_TI_SOFTWARE_LICENCAS (ID_POOL),
        CONSTRAINT FK_EST_SAT_USR FOREIGN KEY (ID_USUARIO)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT FK_EST_SAT_PAT FOREIGN KEY (ID_PATRIMONIO)
            REFERENCES ESTOQUES_TI_PATRIMONIOS (ID_PATRIMONIO),
        CONSTRAINT FK_EST_SAT_CRIADO FOREIGN KEY (CRIADO_POR)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT CK_EST_SAT_ALVO CHECK (
            ID_USUARIO IS NOT NULL OR ID_PATRIMONIO IS NOT NULL
        )
    )
    """,
    # 12. Ocorrências
    """
    CREATE TABLE ESTOQUES_TI_OCORRENCIAS (
        ID_OCORRENCIA               NUMBER          NOT NULL,
        TITULO                      VARCHAR2(200)   NOT NULL,
        DESCRICAO                   VARCHAR2(2000),
        SEVERIDADE                  VARCHAR2(20)    DEFAULT 'MEDIA' NOT NULL,
        STATUS                      VARCHAR2(20)    DEFAULT 'ABERTA' NOT NULL,
        ID_USUARIO_ABRIU            NUMBER          NOT NULL,
        ID_USUARIO_SOLICITANTE      NUMBER          NOT NULL,
        ID_USUARIO_RELACIONADO      NUMBER,
        ID_PATRIMONIO_RELACIONADO   NUMBER,
        DATA_ABERTURA               TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
        DATA_FECHAMENTO             TIMESTAMP,
        DATA_ALTERACAO              TIMESTAMP,
        ALTERADO_POR                NUMBER,
        CONSTRAINT PK_EST_OCO PRIMARY KEY (ID_OCORRENCIA),
        CONSTRAINT FK_EST_OCO_ABRIU FOREIGN KEY (ID_USUARIO_ABRIU)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT FK_EST_OCO_SOL FOREIGN KEY (ID_USUARIO_SOLICITANTE)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT FK_EST_OCO_REL FOREIGN KEY (ID_USUARIO_RELACIONADO)
            REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO),
        CONSTRAINT FK_EST_OCO_PAT FOREIGN KEY (ID_PATRIMONIO_RELACIONADO)
            REFERENCES ESTOQUES_TI_PATRIMONIOS (ID_PATRIMONIO),
        CONSTRAINT CK_EST_OCO_SEV CHECK (
            SEVERIDADE IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')
        ),
        CONSTRAINT CK_EST_OCO_ST CHECK (
            STATUS IN ('ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'FECHADA')
        )
    )
    """,
    # 13. Configurações do sistema (singleton)
    """
    CREATE TABLE ESTOQUES_TI_CONFIGURACOES (
        ID_CONFIG               NUMBER          NOT NULL,
        NOME_EMPRESA            VARCHAR2(150)   DEFAULT 'Controle de Estoque' NOT NULL,
        MODO_ESCURO             CHAR(1)         DEFAULT 'N' NOT NULL,
        ALERTA_ESTOQUE_MINIMO   NUMBER          DEFAULT 5 NOT NULL,
        CONSTRAINT PK_EST_CFG PRIMARY KEY (ID_CONFIG),
        CONSTRAINT CK_EST_CFG_MODO CHECK (MODO_ESCURO IN ('S', 'N')),
        CONSTRAINT CK_EST_CFG_ALERTA CHECK (ALERTA_ESTOQUE_MINIMO >= 0)
    )
    """,
]

# FKs de auditoria em USUARIOS (self-ref) — aplicadas após CREATE TABLE
ALTER_FK_DDL = [
    """
    ALTER TABLE ESTOQUES_TI_USUARIOS ADD CONSTRAINT FK_EST_USR_CRIADO
        FOREIGN KEY (CRIADO_POR) REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO)
    """,
    """
    ALTER TABLE ESTOQUES_TI_USUARIOS ADD CONSTRAINT FK_EST_USR_ALT
        FOREIGN KEY (ALTERADO_POR) REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO)
    """,
    """
    ALTER TABLE ESTOQUES_TI_LOCAIS ADD CONSTRAINT FK_EST_LOC_CRIADO
        FOREIGN KEY (CRIADO_POR) REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO)
    """,
    """
    ALTER TABLE ESTOQUES_TI_TIPOS_ITEM ADD CONSTRAINT FK_EST_TPI_CRIADO
        FOREIGN KEY (CRIADO_POR) REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO)
    """,
    """
    ALTER TABLE ESTOQUES_TI_ITENS ADD CONSTRAINT FK_EST_IT_CRIADO
        FOREIGN KEY (CRIADO_POR) REFERENCES ESTOQUES_TI_USUARIOS (ID_USUARIO)
    """,
]

# Triggers BEFORE INSERT → sequence (padrão usado pelos testes com RETURNING)
TRIGGERS = [
    (
        "ESTOQUES_TI_TRG_USR",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_USR
        BEFORE INSERT ON ESTOQUES_TI_USUARIOS
        FOR EACH ROW
        WHEN (NEW.ID_USUARIO IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_USR.NEXTVAL INTO :NEW.ID_USUARIO FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_LOC",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_LOC
        BEFORE INSERT ON ESTOQUES_TI_LOCAIS
        FOR EACH ROW
        WHEN (NEW.ID_LOCAL IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_LOC.NEXTVAL INTO :NEW.ID_LOCAL FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_TPI",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_TPI
        BEFORE INSERT ON ESTOQUES_TI_TIPOS_ITEM
        FOR EACH ROW
        WHEN (NEW.ID_TIPO_ITEM IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_TPI.NEXTVAL INTO :NEW.ID_TIPO_ITEM FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_IT",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_IT
        BEFORE INSERT ON ESTOQUES_TI_ITENS
        FOR EACH ROW
        WHEN (NEW.ID_ITEM IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_IT.NEXTVAL INTO :NEW.ID_ITEM FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_EMV",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_EMV
        BEFORE INSERT ON ESTOQUES_TI_MOVIMENTACOES
        FOR EACH ROW
        WHEN (NEW.ID_MOVIMENTACAO IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_EMV.NEXTVAL INTO :NEW.ID_MOVIMENTACAO FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_PAT",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_PAT
        BEFORE INSERT ON ESTOQUES_TI_PATRIMONIOS
        FOR EACH ROW
        WHEN (NEW.ID_PATRIMONIO IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_PAT.NEXTVAL INTO :NEW.ID_PATRIMONIO FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_SW",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_SW
        BEFORE INSERT ON ESTOQUES_TI_SOFTWARES
        FOR EACH ROW
        WHEN (NEW.ID_SOFTWARE IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_SW.NEXTVAL INTO :NEW.ID_SOFTWARE FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_SLP",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_SLP
        BEFORE INSERT ON ESTOQUES_TI_SOFTWARE_LICENCAS
        FOR EACH ROW
        WHEN (NEW.ID_POOL IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_SLP.NEXTVAL INTO :NEW.ID_POOL FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_SAT",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_SAT
        BEFORE INSERT ON ESTOQUES_TI_ATRIBUICOES
        FOR EACH ROW
        WHEN (NEW.ID_ATRIBUICAO IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_SAT.NEXTVAL INTO :NEW.ID_ATRIBUICAO FROM DUAL;
        END;
        """,
    ),
    (
        "ESTOQUES_TI_TRG_OCO",
        """
        CREATE OR REPLACE TRIGGER ESTOQUES_TI_TRG_OCO
        BEFORE INSERT ON ESTOQUES_TI_OCORRENCIAS
        FOR EACH ROW
        WHEN (NEW.ID_OCORRENCIA IS NULL)
        BEGIN
            SELECT ESTOQUES_TI_SEQ_OCO.NEXTVAL INTO :NEW.ID_OCORRENCIA FROM DUAL;
        END;
        """,
    ),
]

# Códigos Oracle de "já existe" / redundante
IGNORE_ORACLE_ERRORS = {
    955,   # name is already used by an existing object
    2260,  # table can have only one primary key
    2261,  # unique/primary keys already exist
    2264,  # name already used by an existing constraint
    2275,  # referential constraint already exists
    1442,  # column already has a NOT NULL constraint (raro)
}


def _short_name(sql: str) -> str:
    text = " ".join(sql.split())
    for prefix in ("CREATE TABLE ", "CREATE SEQUENCE ", "ALTER TABLE ", "CREATE OR REPLACE TRIGGER "):
        if text.upper().startswith(prefix):
            rest = text[len(prefix) :]
            return rest.split()[0].split("(")[0]
    return text[:60]


def _execute_ignore_exists(cursor, sql: str, label: str | None = None) -> str:
    name = label or _short_name(sql)
    try:
        cursor.execute(sql)
        return f"  ✅ criado: {name}"
    except oracledb.DatabaseError as exc:
        (error,) = exc.args
        if error.code in IGNORE_ORACLE_ERRORS:
            return f"  ⏭️  já existe: {name}"
        raise


def _validate_env() -> None:
    missing = [k for k, v in {
        "ORACLE_USER": ORACLE_USER,
        "ORACLE_PASSWORD": ORACLE_PASSWORD,
        "ORACLE_DSN": ORACLE_DSN,
    }.items() if not v or v.startswith("seu_")]
    if missing:
        print("❌ Configure o arquivo Backend/.env antes de continuar.")
        print(f"   Variáveis inválidas/ausentes: {', '.join(missing)}")
        print()
        print("   Para o Docker (docker-compose.yml), use por exemplo:")
        print("   ORACLE_USER=estoque_user")
        print("   ORACLE_PASSWORD=estoque_senha")
        print("   ORACLE_DSN=localhost:1521/XEPDB1")
        sys.exit(1)


def init_db() -> bool:
    print("=" * 72)
    print("🗄️  INIT DB — Estoques TI (Oracle)")
    print("=" * 72)
    _validate_env()

    print(f"\n📋 USER: {ORACLE_USER}")
    print(f"📋 DSN:  {ORACLE_DSN}\n")

    # Thin mode funciona com Oracle XE 21 (Docker gvenzl). Thick é opcional.
    try:
        oracledb.init_oracle_client()
        print("ℹ️  Modo thick (Instant Client) ativo\n")
    except Exception:
        print("ℹ️  Modo thin (python-oracledb) — OK para Oracle 12.1+\n")

    try:
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
        )
    except oracledb.Error as exc:
        print(f"❌ Falha na conexão: {exc}")
        print("   Confirme se o container oracle-estoques está UP e o .env correto.")
        return False

    cursor = connection.cursor()
    try:
        print("─" * 72)
        print("1) Sequences")
        print("─" * 72)
        for seq_name, _desc in SEQUENCES:
            sql = f"CREATE SEQUENCE {seq_name} START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE"
            print(_execute_ignore_exists(cursor, sql, seq_name))

        print()
        print("─" * 72)
        print("2) Tabelas")
        print("─" * 72)
        for ddl in TABLES_DDL:
            print(_execute_ignore_exists(cursor, ddl))

        print()
        print("─" * 72)
        print("3) Foreign keys de auditoria")
        print("─" * 72)
        for ddl in ALTER_FK_DDL:
            print(_execute_ignore_exists(cursor, ddl))

        print()
        print("─" * 72)
        print("4) Triggers de ID (BEFORE INSERT)")
        print("─" * 72)
        for trg_name, ddl in TRIGGERS:
            print(_execute_ignore_exists(cursor, ddl, trg_name))

        connection.commit()

        # Resumo
        print()
        print("─" * 72)
        print("5) Verificação")
        print("─" * 72)
        cursor.execute(
            """
            SELECT table_name FROM user_tables
            WHERE table_name LIKE 'ESTOQUES_TI_%'
            ORDER BY table_name
            """
        )
        tables = [r[0] for r in cursor.fetchall()]
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {t:<32} ({count} registros)")

        cursor.execute(
            """
            SELECT sequence_name FROM user_sequences
            WHERE sequence_name LIKE 'ESTOQUES_TI_%'
            ORDER BY sequence_name
            """
        )
        seqs = [r[0] for r in cursor.fetchall()]
        print(f"\n📊 Tabelas: {len(tables)}/12 | Sequences: {len(seqs)}/10")
        print()
        if len(tables) >= 12 and len(seqs) >= 10:
            print("🎉 Schema criado/verificado com sucesso!")
        else:
            print("⚠️  Schema incompleto — revise os erros acima.")
        return True
    except oracledb.DatabaseError as exc:
        connection.rollback()
        print(f"\n❌ Erro ao criar schema: {exc}")
        return False
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    ok = init_db()
    sys.exit(0 if ok else 1)
