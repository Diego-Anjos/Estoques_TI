"""
Migração: adapta ESTOQUES_TI_ITENS aos campos da UI de Cadastro de Itens.

Adiciona: TIPO, QUANTIDADE, UNIDADE, ID_LOCAL, STATUS
Torna ID_TIPO_ITEM opcional (nullable) — tipos da UI podem ser texto livre.

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_item_campos_ui.py
"""
from app.core.database import init_pool, close_pool, get_cursor


def coluna_existe(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM USER_TAB_COLUMNS
        WHERE TABLE_NAME = :tabela
          AND COLUMN_NAME = :coluna
        """,
        {"tabela": table_name.upper(), "coluna": column_name.upper()},
    )
    return cursor.fetchone()[0] > 0


def constraint_existe(cursor, constraint_name: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM USER_CONSTRAINTS
        WHERE CONSTRAINT_NAME = :nome
        """,
        {"nome": constraint_name.upper()},
    )
    return cursor.fetchone()[0] > 0


def main() -> None:
    print("Conectando ao Oracle...")
    init_pool()
    try:
        with get_cursor() as cursor:
            tabela = "ESTOQUES_TI_ITENS"
            alteracoes = []

            # ID_TIPO_ITEM era NOT NULL; UI usa tipo textual — tornar opcional
            cursor.execute(
                """
                SELECT NULLABLE
                FROM USER_TAB_COLUMNS
                WHERE TABLE_NAME = :tabela
                  AND COLUMN_NAME = 'ID_TIPO_ITEM'
                """,
                {"tabela": tabela},
            )
            row = cursor.fetchone()
            if row and row[0] == "N":
                print("Tornando ID_TIPO_ITEM nullable...")
                cursor.execute(f"ALTER TABLE {tabela} MODIFY (ID_TIPO_ITEM NULL)")
                alteracoes.append("ID_TIPO_ITEM nullable")

            colunas = [
                ("TIPO", "VARCHAR2(120)"),
                ("QUANTIDADE", "NUMBER DEFAULT 0"),
                ("UNIDADE", "VARCHAR2(30) DEFAULT 'UN'"),
                ("ID_LOCAL", "NUMBER"),
                ("STATUS", "VARCHAR2(20) DEFAULT 'Ativo'"),
            ]

            for nome, definicao in colunas:
                if coluna_existe(cursor, tabela, nome):
                    print(f"Coluna {nome} já existe. Nada a fazer.")
                    continue
                print(f"Adicionando coluna {nome} {definicao}...")
                cursor.execute(f"ALTER TABLE {tabela} ADD ({nome} {definicao})")
                alteracoes.append(nome)

            if coluna_existe(cursor, tabela, "STATUS"):
                cursor.execute(
                    f"UPDATE {tabela} SET STATUS = 'Ativo' WHERE STATUS IS NULL"
                )
            if coluna_existe(cursor, tabela, "QUANTIDADE"):
                cursor.execute(
                    f"UPDATE {tabela} SET QUANTIDADE = 0 WHERE QUANTIDADE IS NULL"
                )
            if coluna_existe(cursor, tabela, "UNIDADE"):
                cursor.execute(
                    f"UPDATE {tabela} SET UNIDADE = 'UN' WHERE UNIDADE IS NULL"
                )

            fk_name = "FK_EST_IT_LOC"
            if coluna_existe(cursor, tabela, "ID_LOCAL") and not constraint_existe(cursor, fk_name):
                print("Adicionando FK ID_LOCAL -> ESTOQUES_TI_LOCAIS...")
                cursor.execute(
                    f"""
                    ALTER TABLE {tabela}
                    ADD CONSTRAINT {fk_name} FOREIGN KEY (ID_LOCAL)
                    REFERENCES ESTOQUES_TI_LOCAIS (ID_LOCAL)
                    """
                )
                alteracoes.append(fk_name)

            if alteracoes:
                print(f"Migração concluída: {', '.join(alteracoes)}.")
            else:
                print("Nenhuma alteração necessária.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
