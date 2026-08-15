"""
Repository para operações de banco de dados relacionadas a Ocorrências.
Alinhado ao DDL de ESTOQUES_TI_OCORRENCIAS (init_db.py).
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor

TABLE_NAME = "ESTOQUES_TI_OCORRENCIAS"
TABLE_USUARIOS = "ESTOQUES_TI_USUARIOS"

# Status considerados "abertos" (ainda em tratamento)
STATUS_ABERTOS = ("ABERTA", "EM_ANDAMENTO")


def _row_to_dict(row) -> Dict[str, Any]:
    return {
        "id_ocorrencia": row[0],
        "titulo": row[1],
        "descricao": row[2],
        "severidade": row[3],
        "status": row[4],
        "id_usuario_abriu": row[5],
        "id_usuario_solicitante": row[6],
        "id_usuario_relacionado": row[7],
        "id_patrimonio_relacionado": row[8],
        "data_abertura": row[9],
        "data_fechamento": row[10],
        "data_alteracao": row[11],
        "alterado_por": row[12],
        "solicitante_nome": row[13] if len(row) > 13 else None,
    }


_SELECT_COLS = f"""
    o.ID_OCORRENCIA, o.TITULO, o.DESCRICAO, o.SEVERIDADE, o.STATUS,
    o.ID_USUARIO_ABRIU, o.ID_USUARIO_SOLICITANTE, o.ID_USUARIO_RELACIONADO,
    o.ID_PATRIMONIO_RELACIONADO, o.DATA_ABERTURA, o.DATA_FECHAMENTO,
    o.DATA_ALTERACAO, o.ALTERADO_POR, u.NOME as SOLICITANTE_NOME
"""


class OcorrenciaRepository:
    """Repository para gerenciar ocorrências no banco de dados"""

    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria uma nova ocorrência"""
        id_abriu = usuario_id or dados.get("id_usuario_abriu") or dados["id_usuario_solicitante"]
        sql = f"""
            INSERT INTO {TABLE_NAME} (
                TITULO, DESCRICAO, SEVERIDADE, STATUS,
                ID_USUARIO_ABRIU, ID_USUARIO_SOLICITANTE,
                ID_USUARIO_RELACIONADO, ID_PATRIMONIO_RELACIONADO, ALTERADO_POR
            )
            VALUES (
                :titulo, :descricao, :severidade, :status,
                :id_usuario_abriu, :id_usuario_solicitante,
                :id_usuario_relacionado, :id_patrimonio_relacionado, :alterado_por
            )
            RETURNING ID_OCORRENCIA
        """
        with get_cursor() as cursor:
            cursor.execute(
                sql,
                {
                    "titulo": dados["titulo"],
                    "descricao": dados.get("descricao"),
                    "severidade": dados.get("severidade", "MEDIA"),
                    "status": dados.get("status", "ABERTA"),
                    "id_usuario_abriu": id_abriu,
                    "id_usuario_solicitante": dados["id_usuario_solicitante"],
                    "id_usuario_relacionado": dados.get("id_usuario_relacionado"),
                    "id_patrimonio_relacionado": dados.get("id_patrimonio_relacionado"),
                    "alterado_por": usuario_id,
                },
            )
            return cursor.fetchone()[0]

    @staticmethod
    def buscar_por_id(ocorrencia_id: int) -> Optional[Dict[str, Any]]:
        """Busca ocorrência por ID"""
        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME} o
            JOIN {TABLE_USUARIOS} u ON o.ID_USUARIO_SOLICITANTE = u.ID_USUARIO
            WHERE o.ID_OCORRENCIA = :id
        """
        with get_cursor() as cursor:
            cursor.execute(sql, {"id": ocorrencia_id})
            row = cursor.fetchone()
            return _row_to_dict(row) if row else None

    @staticmethod
    def listar_todos(
        status: Optional[str] = None, tipo: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lista ocorrências, opcionalmente filtradas por status.
        O parâmetro `tipo` é ignorado (não existe no DDL atual) — mantido por compatibilidade.
        """
        where_clauses = []
        params: Dict[str, Any] = {}

        if status:
            where_clauses.append("o.STATUS = :status")
            params["status"] = status

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME} o
            JOIN {TABLE_USUARIOS} u ON o.ID_USUARIO_SOLICITANTE = u.ID_USUARIO
            {where_sql}
            ORDER BY o.DATA_ABERTURA DESC
        """
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return [_row_to_dict(row) for row in cursor.fetchall()]

    @staticmethod
    def listar_abertas() -> List[Dict[str, Any]]:
        """Lista ocorrências com status ABERTA ou EM_ANDAMENTO."""
        placeholders = ", ".join(f":s{i}" for i in range(len(STATUS_ABERTOS)))
        params = {f"s{i}": s for i, s in enumerate(STATUS_ABERTOS)}
        sql = f"""
            SELECT {_SELECT_COLS}
            FROM {TABLE_NAME} o
            JOIN {TABLE_USUARIOS} u ON o.ID_USUARIO_SOLICITANTE = u.ID_USUARIO
            WHERE o.STATUS IN ({placeholders})
            ORDER BY o.DATA_ABERTURA DESC
        """
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return [_row_to_dict(row) for row in cursor.fetchall()]

    @staticmethod
    def atualizar(
        ocorrencia_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None
    ) -> bool:
        """Atualiza campos de uma ocorrência"""
        mapeamento = {
            "titulo": "TITULO",
            "descricao": "DESCRICAO",
            "severidade": "SEVERIDADE",
            "status": "STATUS",
            "id_usuario_relacionado": "ID_USUARIO_RELACIONADO",
            "id_patrimonio_relacionado": "ID_PATRIMONIO_RELACIONADO",
        }
        campos = []
        params: Dict[str, Any] = {"id": ocorrencia_id, "alterado_por": alterado_por}

        for chave, coluna in mapeamento.items():
            if chave in dados:
                campos.append(f"{coluna} = :{chave}")
                valor = dados[chave]
                params[chave] = valor.value if hasattr(valor, "value") else valor

        if not campos:
            return False

        # Ao marcar como FECHADA/RESOLVIDA, registra data de fechamento se ainda vazia
        status_valor = params.get("status")
        if status_valor in ("FECHADA", "RESOLVIDA"):
            campos.append("DATA_FECHAMENTO = COALESCE(DATA_FECHAMENTO, NOW())")

        campos.append("DATA_ALTERACAO = NOW()")
        campos.append("ALTERADO_POR = :alterado_por")

        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_OCORRENCIA = :id"
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0

    @staticmethod
    def alterar_status(
        ocorrencia_id: int, status: str, alterado_por: Optional[int] = None
    ) -> bool:
        """Altera apenas o status da ocorrência."""
        campos = [
            "STATUS = :status",
            "DATA_ALTERACAO = NOW()",
            "ALTERADO_POR = :alterado_por",
        ]
        if status in ("FECHADA", "RESOLVIDA"):
            campos.append("DATA_FECHAMENTO = COALESCE(DATA_FECHAMENTO, NOW())")
        elif status in STATUS_ABERTOS:
            campos.append("DATA_FECHAMENTO = NULL")

        sql = f"""
            UPDATE {TABLE_NAME}
            SET {', '.join(campos)}
            WHERE ID_OCORRENCIA = :id
        """
        with get_cursor() as cursor:
            cursor.execute(
                sql,
                {
                    "id": ocorrencia_id,
                    "status": status,
                    "alterado_por": alterado_por,
                },
            )
            return cursor.rowcount > 0

    @staticmethod
    def fechar(
        ocorrencia_id: int, resolucao: Optional[str] = None, alterado_por: Optional[int] = None
    ) -> bool:
        """Fecha uma ocorrência (status FECHADA)."""
        # resolucao/observações: DDL não tem coluna dedicada; anexa à descrição se informado
        if resolucao:
            sql = f"""
                UPDATE {TABLE_NAME}
                SET STATUS = 'FECHADA',
                    DESCRICAO = CASE
                        WHEN :resolucao IS NULL THEN DESCRICAO
                        WHEN DESCRICAO IS NULL THEN :resolucao
                        ELSE DESCRICAO || CHR(10) || '[Fechamento] ' || :resolucao
                    END,
                    DATA_FECHAMENTO = NOW(),
                    DATA_ALTERACAO = NOW(),
                    ALTERADO_POR = :alterado_por
                WHERE ID_OCORRENCIA = :id
            """
            params = {
                "id": ocorrencia_id,
                "resolucao": resolucao,
                "alterado_por": alterado_por,
            }
        else:
            sql = f"""
                UPDATE {TABLE_NAME}
                SET STATUS = 'FECHADA',
                    DATA_FECHAMENTO = NOW(),
                    DATA_ALTERACAO = NOW(),
                    ALTERADO_POR = :alterado_por
                WHERE ID_OCORRENCIA = :id
            """
            params = {"id": ocorrencia_id, "alterado_por": alterado_por}

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0

    @staticmethod
    def deletar(ocorrencia_id: int) -> bool:
        """Deleta uma ocorrência"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_OCORRENCIA = :id"
        with get_cursor() as cursor:
            cursor.execute(sql, {"id": ocorrencia_id})
            return cursor.rowcount > 0
