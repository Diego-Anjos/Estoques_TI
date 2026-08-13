"""
Migração: adiciona coluna CARGO em ESTOQUES_TI_USUARIOS (se ainda não existir).

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_cargo.py
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
            if coluna_existe(cursor, "ESTOQUES_TI_USUARIOS", "CARGO"):
                print("Coluna CARGO já existe em ESTOQUES_TI_USUARIOS. Nada a fazer.")
                return

            print("Adicionando coluna CARGO VARCHAR2(100)...")
            cursor.execute(
                "ALTER TABLE ESTOQUES_TI_USUARIOS ADD (CARGO VARCHAR2(100))"
            )
            print("Migração concluída com sucesso.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
