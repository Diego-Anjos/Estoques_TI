"""
Repository transacional para Movimentações de Estoque

Tipos:
- ENTRADA / DEVOLUCAO → somam ao saldo (com FOR UPDATE)
- SAIDA → subtrai do saldo (com validação de saldo insuficiente)
"""
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.core.database import get_cursor


TABLE_MOV = "ESTOQUES_TI_MOVIMENTACOES"
TABLE_ITENS = "ESTOQUES_TI_ITENS"
TABLE_SALDO = "ESTOQUES_TI_ESTOQUE_SALDO"

# Tipos que aumentam o estoque (mesma matemática)
TIPOS_ENTRADA = frozenset({'ENTRADA', 'DEVOLUCAO'})


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_movimentacao': row[0],
        'id_item': row[1],
        'tipo_movimentacao': row[2],
        'quantidade': int(row[3]),
        'observacao': row[4],
        'setor_destino': row[5],
        'setor_origem': row[6],
        'data_movimentacao': row[7],
        'usuario_id': row[8],
        'nome_item': row[9],
        'quantidade_atual': int(row[10] or 0),
    }


class MovimentacaoRepository:
    """Operações de movimentação com atualização atômica do saldo do item"""

    @staticmethod
    def listar_todas(
        tipo: Optional[str] = None,
        nome_item: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Lista o histórico, opcionalmente filtrado por tipo
        ('ENTRADA'/'SAIDA'/'DEVOLUCAO') e por parte do nome do item.
        """
        filtros: List[str] = []
        params: Dict[str, Any] = {}

        if tipo:
            filtros.append("m.TIPO_MOVIMENTACAO = :tipo")
            params['tipo'] = tipo

        if nome_item and nome_item.strip():
            filtros.append("UPPER(i.NOME) LIKE UPPER(:nome_item)")
            params['nome_item'] = f"%{nome_item.strip()}%"

        where = f"WHERE {' AND '.join(filtros)}" if filtros else ""

        sql = f"""
            SELECT m.ID_MOVIMENTACAO, m.ID_ITEM, m.TIPO_MOVIMENTACAO, m.QUANTIDADE,
                   m.MOTIVO, m.SETOR_DESTINO, m.SETOR_ORIGEM, m.DATA_CRIACAO, m.CRIADO_POR,
                   i.NOME, i.QUANTIDADE
            FROM {TABLE_MOV} m
            JOIN {TABLE_ITENS} i ON i.ID_ITEM = m.ID_ITEM
            {where}
            ORDER BY m.DATA_CRIACAO DESC, m.ID_MOVIMENTACAO DESC
        """
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return [_row_to_dict(row) for row in cursor.fetchall()]

    @staticmethod
    def buscar_por_id(mov_id: int) -> Optional[Dict[str, Any]]:
        sql = f"""
            SELECT m.ID_MOVIMENTACAO, m.ID_ITEM, m.TIPO_MOVIMENTACAO, m.QUANTIDADE,
                   m.MOTIVO, m.SETOR_DESTINO, m.SETOR_ORIGEM, m.DATA_CRIACAO, m.CRIADO_POR,
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
        - ENTRADA / DEVOLUCAO: soma quantidade
        - SAIDA: subtrai (400 se insuficiente)
        Mantém SELECT … FOR UPDATE na linha do item.
        """
        id_item = dados['id_item']
        tipo = dados['tipo_movimentacao']  # ENTRADA | SAIDA | DEVOLUCAO
        quantidade = int(dados['quantidade'])
        observacao = dados.get('observacao')
        usuario_id = dados.get('usuario_id')

        # Setores só no tipo correspondente
        setor_destino = dados.get('setor_destino') if tipo == 'SAIDA' else None
        setor_origem = dados.get('setor_origem') if tipo == 'DEVOLUCAO' else None

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

            if tipo in TIPOS_ENTRADA:
                # ENTRADA e DEVOLUCAO: mesma matemática (somam ao estoque)
                nova_qtd = qtd_atual + quantidade
                id_local_origem = None
                id_local_destino = id_local
            elif tipo == 'SAIDA':
                nova_qtd = qtd_atual - quantidade
                id_local_origem = id_local
                id_local_destino = None
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de movimentação não suportado: {tipo}",
                )

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
                     TIPO_MOVIMENTACAO, MOTIVO, SETOR_DESTINO, SETOR_ORIGEM, CRIADO_POR)
                VALUES
                    (:id_item, :id_local_origem, :id_local_destino, :quantidade,
                     :tipo, :motivo, :setor_destino, :setor_origem, :criado_por)
                RETURNING ID_MOVIMENTACAO INTO :id
                """,
                {
                    'id_item': id_item,
                    'id_local_origem': id_local_origem,
                    'id_local_destino': id_local_destino,
                    'quantidade': quantidade,
                    'tipo': tipo,
                    'motivo': observacao,
                    'setor_destino': setor_destino,
                    'setor_origem': setor_origem,
                    'criado_por': usuario_id,
                    'id': id_var,
                },
            )
            return id_var.getvalue()[0]
