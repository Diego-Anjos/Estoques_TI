"""
Migração: suporte a Devolução (DEVOLUCAO / 'D').

1) Adiciona coluna SETOR_ORIGEM em ESTOQUES_TI_MOVIMENTACOES
2) Atualiza CHECK CK_EST_EMV_TIPO para incluir 'DEVOLUCAO'

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_add_devolucao.py
"""
from app.core.database import init_pool, close_pool, get_cursor


TABELA = "ESTOQUES_TI_MOVIMENTACOES"
CONSTRAINT = "CK_EST_EMV_TIPO"
TIPOS_OK = "('ENTRADA', 'SAIDA', 'TRANSFERENCIA', 'AJUSTE', 'DEVOLUCAO')"


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
            if not coluna_existe(cursor, TABELA, "SETOR_ORIGEM"):
                print("Adicionando coluna SETOR_ORIGEM VARCHAR2(80)...")
                cursor.execute(
                    f"ALTER TABLE {TABELA} ADD (SETOR_ORIGEM VARCHAR2(80))"
                )
                print("  OK: SETOR_ORIGEM criada.")
            else:
                print("Coluna SETOR_ORIGEM já existe.")

            # Recria CHECK para incluir DEVOLUCAO (idempotente na prática)
            if constraint_existe(cursor, CONSTRAINT):
                print(f"Recriando constraint {CONSTRAINT} com DEVOLUCAO...")
                cursor.execute(f"ALTER TABLE {TABELA} DROP CONSTRAINT {CONSTRAINT}")
            else:
                print(f"Constraint {CONSTRAINT} não existia; criando...")

            cursor.execute(
                f"""
                ALTER TABLE {TABELA} ADD CONSTRAINT {CONSTRAINT} CHECK (
                    TIPO_MOVIMENTACAO IN {TIPOS_OK}
                )
                """
            )
            print(f"  OK: {CONSTRAINT} inclui DEVOLUCAO.")
            print("Migração de Devolução concluída.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
