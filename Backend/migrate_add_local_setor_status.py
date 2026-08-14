"""
Migração: adiciona colunas SETOR e STATUS em ESTOQUES_TI_LOCAIS (se ainda não existirem).

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_local_setor_status.py
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
            tabela = "ESTOQUES_TI_LOCAIS"
            alteracoes = []

            if not coluna_existe(cursor, tabela, "SETOR"):
                print("Adicionando coluna SETOR VARCHAR2(80)...")
                cursor.execute(f"ALTER TABLE {tabela} ADD (SETOR VARCHAR2(80))")
                alteracoes.append("SETOR")
            else:
                print("Coluna SETOR já existe. Nada a fazer.")

            if not coluna_existe(cursor, tabela, "STATUS"):
                print("Adicionando coluna STATUS VARCHAR2(20) DEFAULT 'Ativo'...")
                cursor.execute(
                    f"ALTER TABLE {tabela} ADD (STATUS VARCHAR2(20) DEFAULT 'Ativo')"
                )
                cursor.execute(
                    f"UPDATE {tabela} SET STATUS = 'Ativo' WHERE STATUS IS NULL"
                )
                alteracoes.append("STATUS")
            else:
                print("Coluna STATUS já existe. Nada a fazer.")

            if alteracoes:
                print(f"Migração concluída com sucesso: {', '.join(alteracoes)}.")
            else:
                print("Nenhuma alteração necessária.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
