"""
Migração: adiciona coluna SETOR_DESTINO em ESTOQUES_TI_MOVIMENTACOES
(setor/departamento para o qual o item foi enviado em saídas).

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_movimentacao_setor_destino.py
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
            tabela = "ESTOQUES_TI_MOVIMENTACOES"

            if not coluna_existe(cursor, tabela, "SETOR_DESTINO"):
                print("Adicionando coluna SETOR_DESTINO VARCHAR2(80)...")
                cursor.execute(
                    f"ALTER TABLE {tabela} ADD (SETOR_DESTINO VARCHAR2(80))"
                )
                print("Migração concluída com sucesso: SETOR_DESTINO.")
            else:
                print("Coluna SETOR_DESTINO já existe. Nada a fazer.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
