"""
Migração: cria ESTOQUES_TI_CONFIGURACOES (singleton) se não existir.

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_create_configuracoes.py
"""
from app.core.database import init_pool, close_pool, get_cursor


def tabela_existe(cursor, table_name: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM USER_TABLES
        WHERE TABLE_NAME = :tabela
        """,
        {"tabela": table_name.upper()},
    )
    return cursor.fetchone()[0] > 0


def main() -> None:
    print("Conectando ao Oracle...")
    init_pool()
    try:
        with get_cursor() as cursor:
            tabela = "ESTOQUES_TI_CONFIGURACOES"
            if tabela_existe(cursor, tabela):
                print(f"Tabela {tabela} já existe.")
            else:
                print(f"Criando tabela {tabela}...")
                cursor.execute(
                    f"""
                    CREATE TABLE {tabela} (
                        ID_CONFIG               NUMBER          NOT NULL,
                        NOME_EMPRESA            VARCHAR2(150)   DEFAULT 'Controle de Estoque' NOT NULL,
                        MODO_ESCURO             CHAR(1)         DEFAULT 'N' NOT NULL,
                        ALERTA_ESTOQUE_MINIMO   NUMBER          DEFAULT 5 NOT NULL,
                        CONSTRAINT PK_EST_CFG PRIMARY KEY (ID_CONFIG),
                        CONSTRAINT CK_EST_CFG_MODO CHECK (MODO_ESCURO IN ('S', 'N')),
                        CONSTRAINT CK_EST_CFG_ALERTA CHECK (ALERTA_ESTOQUE_MINIMO >= 0)
                    )
                    """
                )
                print("Tabela criada.")

            cursor.execute(
                f"SELECT COUNT(*) FROM {tabela} WHERE ID_CONFIG = 1"
            )
            if cursor.fetchone()[0] == 0:
                print("Inserindo registro singleton (ID=1)...")
                cursor.execute(
                    f"""
                    INSERT INTO {tabela}
                        (ID_CONFIG, NOME_EMPRESA, MODO_ESCURO, ALERTA_ESTOQUE_MINIMO)
                    VALUES
                        (1, 'Controle de Estoque', 'N', 5)
                    """
                )
                print("Registro inicial criado.")
            else:
                print("Registro ID=1 já existe.")

            print("Migração concluída com sucesso.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
