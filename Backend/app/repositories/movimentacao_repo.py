"""
Repository transacional para Movimentações de Estoque
"""
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.core.database import get_cursor


TABLE_MOV = "ESTOQUES_TI_MOVIMENTACOES"
TABLE_ITENS = "ESTOQUES_TI_ITENS"
TABLE_SALDO = "ESTOQUES_TI_ESTOQUE_SALDO"


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_movimentacao': row[0],
        'id_item': row[1],
        'tipo_movimentacao': row[2],
        'quantidade': int(row[3]),
        'observacao': row[4],
        'data_movimentacao': row[5],
        'usuario_id': row[6],
        'nome_item': row[7],
        'quantidade_atual': int(row[8] or 0),
    }


class MovimentacaoRepository:
    """Operações de movimentação com atualização atômica do saldo do item"""

    @staticmethod
    def listar_todas() -> List[Dict[str, Any]]:
        sql = f"""
            SELECT m.ID_MOVIMENTACAO, m.ID_ITEM, m.TIPO_MOVIMENTACAO, m.QUANTIDADE,
                   m.MOTIVO, m.DATA_CRIACAO, m.CRIADO_POR,
                   i.NOME, i.QUANTIDADE
            FROM {TABLE_MOV} m
            JOIN {TABLE_ITENS} i ON i.ID_ITEM = m.ID_ITEM
            ORDER BY m.DATA_CRIACAO DESC, m.ID_MOVIMENTACAO DESC
        """
        with get_cursor() as cursor:
            cursor.execute(sql)
            return [_row_to_dict(row) for row in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(mov_id: int) -> Optional[Dict[str, Any]]:
        sql = f"""
            SELECT m.ID_MOVIMENTACAO, m.ID_ITEM, m.TIPO_MOVIMENTACAO, m.QUANTIDADE,
                   m.MOTIVO, m.DATA_CRIACAO, m.CRIADO_POR,
                   i.NOME, i.QUANTIDADE
            FROM {TABLE_MOV} m
            JOIN {TABLE_ITENS} i ON i.ID_ITEM = m.ID_ITEM
            WHERE m.ID_MOVIMENTACAO = :id
        """
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': mov_id})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def registrar(dados: Dict[str, Any]) -> int:
        """
        Transação: valida saldo, atualiza item (+ saldo) e insere movimentação.
        Lança HTTPException 400 se saída insuficiente ou item inexistente.
        """
        id_item = dados['id_item']
        tipo = dados['tipo_movimentacao']  # ENTRADA | SAIDA
        quantidade = int(dados['quantidade'])
        observacao = dados.get('observacao')
        usuario_id = dados.get('usuario_id')

        with get_cursor() as cursor:
            cursor.execute(
                f"""
                SELECT ID_ITEM, NOME, QUANTIDADE, ID_LOCAL
                FROM {TABLE_ITENS}
                WHERE ID_ITEM = :id
                FOR UPDATE
                """,
                {'id': id_item},
            )
            item = cursor.fetchone()
            if not item:
                raise HTTPException(status_code=404, detail="Item não encontrado")

            nome_item = item[1]
            qtd_atual = int(item[2] or 0)
            id_local = item[3]

            if tipo == 'SAIDA' and quantidade > qtd_atual:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Saldo insuficiente para '{nome_item}'. "
                        f"Disponível: {qtd_atual}, solicitado: {quantidade}."
                    ),
                )

            if tipo == 'ENTRADA':
                nova_qtd = qtd_atual + quantidade
                id_local_origem = None
                id_local_destino = id_local
            else:
                nova_qtd = qtd_atual - quantidade
                id_local_origem = id_local
                id_local_destino = None

            cursor.execute(
                f"""
                UPDATE {TABLE_ITENS}
                SET QUANTIDADE = :quantidade,
                    DATA_ALTERACAO = SYSTIMESTAMP,
                    ALTERADO_POR = :alterado_por
                WHERE ID_ITEM = :id
                """,
                {
                    'quantidade': nova_qtd,
                    'alterado_por': usuario_id,
                    'id': id_item,
                },
            )

            # Mantém ESTOQUE_SALDO alinhado (se o item tiver local)
            if id_local is not None:
                cursor.execute(
                    f"""
                    SELECT COUNT(*) FROM {TABLE_SALDO}
                    WHERE ID_ITEM = :id_item AND ID_LOCAL = :id_local
                    """,
                    {'id_item': id_item, 'id_local': id_local},
                )
                if cursor.fetchone()[0] > 0:
                    cursor.execute(
                        f"""
                        UPDATE {TABLE_SALDO}
                        SET QUANTIDADE = :quantidade,
                            DATA_ALTERACAO = SYSTIMESTAMP,
                            ALTERADO_POR = :alterado_por
                        WHERE ID_ITEM = :id_item AND ID_LOCAL = :id_local
                        """,
                        {
                            'quantidade': nova_qtd,
                            'alterado_por': usuario_id,
                            'id_item': id_item,
                            'id_local': id_local,
                        },
                    )
                else:
                    cursor.execute(
                        f"""
                        INSERT INTO {TABLE_SALDO}
                            (ID_ITEM, ID_LOCAL, QUANTIDADE, ALTERADO_POR)
                        VALUES
                            (:id_item, :id_local, :quantidade, :alterado_por)
                        """,
                        {
                            'id_item': id_item,
                            'id_local': id_local,
                            'quantidade': nova_qtd,
                            'alterado_por': usuario_id,
                        },
                    )

            id_var = cursor.var(int)
            cursor.execute(
                f"""
                INSERT INTO {TABLE_MOV}
                    (ID_ITEM, ID_LOCAL_ORIGEM, ID_LOCAL_DESTINO, QUANTIDADE,
                     TIPO_MOVIMENTACAO, MOTIVO, CRIADO_POR)
                VALUES
                    (:id_item, :id_local_origem, :id_local_destino, :quantidade,
                     :tipo, :motivo, :criado_por)
                RETURNING ID_MOVIMENTACAO INTO :id
                """,
                {
                    'id_item': id_item,
                    'id_local_origem': id_local_origem,
                    'id_local_destino': id_local_destino,
                    'quantidade': quantidade,
                    'tipo': tipo,
                    'motivo': observacao,
                    'criado_por': usuario_id,
                    'id': id_var,
                },
            )
            return id_var.getvalue()[0]
