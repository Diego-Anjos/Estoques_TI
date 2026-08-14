"""
Repository para operações de banco de dados relacionadas a Itens
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


TABLE_NAME = "ESTOQUES_TI_ITENS"
TABLE_LOCAIS = "ESTOQUES_TI_LOCAIS"
TABLE_SALDO = "ESTOQUES_TI_ESTOQUE_SALDO"

_SELECT = f"""
    i.ID_ITEM, i.NOME, i.TIPO, i.DESCRICAO, i.QUANTIDADE, i.UNIDADE,
    i.ID_LOCAL, i.STATUS, i.DATA_CRIACAO, i.CRIADO_POR,
    i.DATA_ALTERACAO, i.ALTERADO_POR, l.NOME AS NOME_LOCAL
"""


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_item': row[0],
        'nome': row[1],
        'tipo': row[2],
        'descricao': row[3],
        'quantidade': int(row[4] or 0),
        'unidade': row[5] or 'UN',
        'id_local': row[6],
        'status': row[7] or 'Ativo',
        'data_criacao': row[8],
        'criado_por': row[9],
        'data_alteracao': row[10],
        'alterado_por': row[11],
        'nome_local': row[12],
    }


class ItemRepository:
    """Repository para gerenciar itens no banco de dados"""

    @staticmethod
    def _upsert_saldo(cursor, id_item: int, id_local: int, quantidade: int, usuario_id: Optional[int] = None):
        """Mantém ESTOQUE_SALDO alinhado ao local/quantidade do item."""
        cursor.execute(
            f"SELECT COUNT(*) FROM {TABLE_SALDO} WHERE ID_ITEM = :id_item",
            {'id_item': id_item},
        )
        existe = cursor.fetchone()[0] > 0

        if existe:
            # Remove saldos antigos (item simplificado: 1 local principal)
            cursor.execute(
                f"DELETE FROM {TABLE_SALDO} WHERE ID_ITEM = :id_item",
                {'id_item': id_item},
            )

        cursor.execute(
            f"""
            INSERT INTO {TABLE_SALDO} (ID_ITEM, ID_LOCAL, QUANTIDADE, ALTERADO_POR)
            VALUES (:id_item, :id_local, :quantidade, :alterado_por)
            """,
            {
                'id_item': id_item,
                'id_local': id_local,
                'quantidade': quantidade,
                'alterado_por': usuario_id,
            },
        )

    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo item e saldo no local informado"""
        sql = f"""
            INSERT INTO {TABLE_NAME}
                (NOME, TIPO, DESCRICAO, QUANTIDADE, UNIDADE, ID_LOCAL, STATUS, CRIADO_POR)
            VALUES
                (:nome, :tipo, :descricao, :quantidade, :unidade, :id_local, :status, :criado_por)
            RETURNING ID_ITEM INTO :id
        """

        with get_cursor() as cursor:
            id_var = cursor.var(int)
            quantidade = int(dados.get('quantidade') or 0)
            id_local = dados['id_local']
            cursor.execute(sql, {
                'nome': dados['nome'],
                'tipo': dados.get('tipo'),
                'descricao': dados.get('descricao'),
                'quantidade': quantidade,
                'unidade': dados.get('unidade') or 'UN',
                'id_local': id_local,
                'status': dados.get('status') or 'Ativo',
                'criado_por': usuario_id,
                'id': id_var,
            })
            novo_id = id_var.getvalue()[0]
            ItemRepository._upsert_saldo(cursor, novo_id, id_local, quantidade, usuario_id)
            return novo_id

    @staticmethod
    def buscar_por_id(item_id: int) -> Optional[Dict[str, Any]]:
        """Busca item por ID com nome do local"""
        sql = f"""
            SELECT {_SELECT}
            FROM {TABLE_NAME} i
            LEFT JOIN {TABLE_LOCAIS} l ON l.ID_LOCAL = i.ID_LOCAL
            WHERE i.ID_ITEM = :id
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {'id': item_id})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def listar_todos(tipo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todos os itens com nome do local"""
        if tipo:
            sql = f"""
                SELECT {_SELECT}
                FROM {TABLE_NAME} i
                LEFT JOIN {TABLE_LOCAIS} l ON l.ID_LOCAL = i.ID_LOCAL
                WHERE UPPER(i.TIPO) = UPPER(:tipo)
                ORDER BY i.NOME
            """
            params = {'tipo': tipo}
        else:
            sql = f"""
                SELECT {_SELECT}
                FROM {TABLE_NAME} i
                LEFT JOIN {TABLE_LOCAIS} l ON l.ID_LOCAL = i.ID_LOCAL
                ORDER BY i.NOME
            """
            params = {}

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [_row_to_dict(row) for row in rows]

    @staticmethod
    def atualizar(item_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um item e sincroniza saldo se local/quantidade mudarem"""
        campos = []
        params = {'id': item_id, 'alterado_por': alterado_por}

        mapeamento = {
            'nome': 'NOME',
            'tipo': 'TIPO',
            'descricao': 'DESCRICAO',
            'quantidade': 'QUANTIDADE',
            'unidade': 'UNIDADE',
            'id_local': 'ID_LOCAL',
            'status': 'STATUS',
        }

        for chave, coluna in mapeamento.items():
            if chave in dados:
                campos.append(f"{coluna} = :{chave}")
                params[chave] = dados[chave]

        if not campos:
            return False

        campos.append("DATA_ALTERACAO = SYSTIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")

        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_ITEM = :id"

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            if cursor.rowcount <= 0:
                return False

            if 'id_local' in dados or 'quantidade' in dados:
                cursor.execute(
                    f"SELECT ID_LOCAL, QUANTIDADE FROM {TABLE_NAME} WHERE ID_ITEM = :id",
                    {'id': item_id},
                )
                atual = cursor.fetchone()
                if atual and atual[0] is not None:
                    ItemRepository._upsert_saldo(
                        cursor,
                        item_id,
                        int(atual[0]),
                        int(atual[1] or 0),
                        alterado_por,
                    )

            return True

    @staticmethod
    def deletar(item_id: int) -> bool:
        """Deleta saldo e item"""
        with get_cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {TABLE_SALDO} WHERE ID_ITEM = :id",
                {'id': item_id},
            )
            cursor.execute(
                f"DELETE FROM {TABLE_NAME} WHERE ID_ITEM = :id",
                {'id': item_id},
            )
            return cursor.rowcount > 0
