"""
Migração: torna CRIADO_POR nullable em ESTOQUES_TI_MOVIMENTACOES
(usuario_id opcional na API de movimentações).

Uso (com venv ativo, a partir da pasta Backend):
    python migrate_movimentacao_criado_por_nullable.py
"""
from app.core.database import init_pool, close_pool, get_cursor


def main() -> None:
    print("Conectando ao Oracle...")
    init_pool()
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT NULLABLE
                FROM USER_TAB_COLUMNS
                WHERE TABLE_NAME = 'ESTOQUES_TI_MOVIMENTACOES'
                  AND COLUMN_NAME = 'CRIADO_POR'
                """
            )
            row = cursor.fetchone()
            if not row:
                print("Coluna CRIADO_POR não encontrada.")
                return
            if row[0] == "Y":
                print("CRIADO_POR já é nullable. Nada a fazer.")
                return

            print("Tornando CRIADO_POR nullable...")
            cursor.execute(
                "ALTER TABLE ESTOQUES_TI_MOVIMENTACOES MODIFY (CRIADO_POR NULL)"
            )
            print("Migração concluída com sucesso.")
    finally:
        close_pool()


if __name__ == "__main__":
    main()
