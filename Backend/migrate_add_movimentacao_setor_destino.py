"""
Migração: adiciona SETOR_DESTINO e SETOR_ORIGEM em ESTOQUES_TI_MOVIMENTACOES
(necessários para saídas e devoluções na tela de Controle de Estoque).

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_movimentacao_setor_destino.py
"""
from app.core.database import init_pool, close_pool, get_cursor


TABELA = "ESTOQUES_TI_MOVIMENTACOES"
COLUNAS = (
    ("SETOR_DESTINO", "VARCHAR2(80)"),
    ("SETOR_ORIGEM", "VARCHAR2(80)"),
)


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
            for nome, tipo in COLUNAS:
                if not coluna_existe(cursor, TABELA, nome):
                    print(f"Adicionando coluna {nome} {tipo}...")
                    cursor.execute(f"ALTER TABLE {TABELA} ADD ({nome} {tipo})")
                    print(f"  OK: {nome} criada.")
                else:
                    print(f"Coluna {nome} já existe. Nada a fazer.")
            print("Migração de setores concluída.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
