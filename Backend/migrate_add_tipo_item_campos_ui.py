"""
Migração: adapta ESTOQUES_TI_TIPOS_ITEM aos campos da UI.

Adiciona: CATEGORIA, DESCRICAO, STATUS

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_tipo_item_campos_ui.py
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


def main() -> None:
    print("Conectando ao Oracle...")
    init_pool()
    try:
        with get_cursor() as cursor:
            tabela = "ESTOQUES_TI_TIPOS_ITEM"
            alteracoes = []

            colunas = [
                ("CATEGORIA", "VARCHAR2(80)"),
                ("DESCRICAO", "VARCHAR2(400)"),
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

            if alteracoes:
                print(f"Migração concluída: {', '.join(alteracoes)}.")
            else:
                print("Nenhuma alteração necessária.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
