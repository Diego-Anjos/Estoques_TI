"""
Repository para operações de banco de dados relacionadas a Tipos de Item
"""
import re
import time
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


TABLE_NAME = "ESTOQUES_TI_TIPOS_ITEM"
TABLE_USUARIOS = "ESTOQUES_TI_USUARIOS"

_SELECT = f"""
    t.ID_TIPO_ITEM, t.NOME, t.CATEGORIA, t.DESCRICAO, t.STATUS,
    t.DATA_CRIACAO, t.CRIADO_POR, t.DATA_ALTERACAO, t.ALTERADO_POR,
    u.NOME AS NOME_CRIADO_POR
"""


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        'id_tipo_item': row[0],
        'nome': row[1],
        'categoria': row[2],
        'descricao': row[3],
        'status': row[4] or 'Ativo',
        'data_criacao': row[5],
        'criado_por': row[6],
        'data_alteracao': row[7],
        'alterado_por': row[8],
        'nome_criado_por': row[9],
    }


def _gerar_codigo(nome: str) -> str:
    """Gera código único a partir do nome (máx. 40 chars)."""
    base = re.sub(r'[^A-Za-z0-9]+', '_', (nome or '').strip().upper()).strip('_')
    if not base:
        base = 'TIPO'
    base = base[:32]
    sufixo = str(int(time.time()))[-6:]
    return f"{base}_{sufixo}"[:40]


class TipoItemRepository:
    """Repository para gerenciar tipos de item no banco de dados Oracle"""

    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo tipo de item"""
        codigo = dados.get('codigo') or _gerar_codigo(dados['nome'])
        sql = f"""
            INSERT INTO {TABLE_NAME}
                (CODIGO, NOME, CATEGORIA, DESCRICAO, STATUS, SERIALIZADO, UNIDADE, CRIADO_POR)
            VALUES
                (:codigo, :nome, :categoria, :descricao, :status, :serializado, :unidade, :criado_por)
            RETURNING ID_TIPO_ITEM INTO :id
        """

        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'codigo': codigo,
                'nome': dados['nome'],
                'categoria': dados.get('categoria'),
                'descricao': dados.get('descricao'),
                'status': dados.get('status') or 'Ativo',
                'serializado': dados.get('serializado', 'N'),
                'unidade': dados.get('unidade', 'UN'),
                'criado_por': usuario_id,
                'id': id_var,
            })
            return id_var.getvalue()[0]

    @staticmethod
    def buscar_por_id(tipo_item_id: int) -> Optional[Dict[str, Any]]:
        """Busca tipo de item por ID"""
        sql = f"""
            SELECT {_SELECT}
            FROM {TABLE_NAME} t
            LEFT JOIN {TABLE_USUARIOS} u ON u.ID_USUARIO = t.CRIADO_POR
            WHERE t.ID_TIPO_ITEM = :id
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {'id': tipo_item_id})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def buscar_por_nome(nome: str) -> Optional[Dict[str, Any]]:
        """Busca tipo de item por nome"""
        sql = f"""
            SELECT {_SELECT}
            FROM {TABLE_NAME} t
            LEFT JOIN {TABLE_USUARIOS} u ON u.ID_USUARIO = t.CRIADO_POR
            WHERE UPPER(t.NOME) = UPPER(:nome)
        """

        with get_cursor() as cursor:
            cursor.execute(sql, {'nome': nome})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def listar_todos(status_filtro: str = "ativos") -> List[Dict[str, Any]]:
        """Lista tipos de item. Padrão: apenas STATUS = 'Ativo'."""
        if status_filtro == "ativos":
            where_sql = "WHERE t.STATUS = 'Ativo'"
        elif status_filtro == "inativos":
            where_sql = "WHERE t.STATUS = 'Inativo'"
        else:
            where_sql = ""

        sql = f"""
            SELECT {_SELECT}
            FROM {TABLE_NAME} t
            LEFT JOIN {TABLE_USUARIOS} u ON u.ID_USUARIO = t.CRIADO_POR
            {where_sql}
            ORDER BY t.NOME
        """

        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [_row_to_dict(row) for row in rows]

    @staticmethod
    def atualizar(tipo_item_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um tipo de item"""
        campos = []
        params = {'id': tipo_item_id, 'alterado_por': alterado_por}

        mapeamento = {
            'nome': 'NOME',
            'categoria': 'CATEGORIA',
            'descricao': 'DESCRICAO',
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

        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_TIPO_ITEM = :id"

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0

    @staticmethod
    def inativar(tipo_item_id: int, alterado_por: Optional[int] = None) -> bool:
        """Soft-delete: marca o tipo como Inativo."""
        return TipoItemRepository.atualizar(
            tipo_item_id,
            {'status': 'Inativo'},
            alterado_por=alterado_por,
        )

    @staticmethod
    def deletar(tipo_item_id: int) -> bool:
        """Deleta fisicamente um tipo de item (uso interno)."""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_TIPO_ITEM = :id"

        with get_cursor() as cursor:
            cursor.execute(sql, {'id': tipo_item_id})
            return cursor.rowcount > 0
