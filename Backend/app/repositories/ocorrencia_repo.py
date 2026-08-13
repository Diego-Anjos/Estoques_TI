"""
Repository para operações de banco de dados relacionadas a Ocorrências
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor
from datetime import datetime


# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_OCORRENCIAS"
TABLE_USUARIOS = "ESTOQUES_TI_USUARIOS"


class OcorrenciaRepository:
    """Repository para gerenciar ocorrências no banco de dados"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria uma nova ocorrência"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (TITULO, DESCRICAO, USUARIO_SOLICITANTE_ID, TIPO,
                                    PRIORIDADE, STATUS, ITEM_ID, PATRIMONIO_ID, CRIADO_POR)
            VALUES (:titulo, :descricao, :usuario_solicitante_id, :tipo,
                    :prioridade, :status, :item_id, :patrimonio_id, :criado_por)
            RETURNING ID INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'titulo': dados['titulo'],
                'descricao': dados['descricao'],
                'usuario_solicitante_id': dados['usuario_solicitante_id'],
                'tipo': dados['tipo'],
                'prioridade': dados.get('prioridade', 'MEDIA'),
                'status': dados.get('status', 'ABERTO'),
                'item_id': dados.get('item_id'),
                'patrimonio_id': dados.get('patrimonio_id'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(ocorrencia_id: int) -> Optional[Dict[str, Any]]:
        """Busca ocorrência por ID"""
        sql = f"""
            SELECT o.ID, o.TITULO, o.DESCRICAO, o.USUARIO_SOLICITANTE_ID, 
                   u.NOME as SOLICITANTE_NOME, o.TIPO, o.PRIORIDADE, o.STATUS,
                   o.ITEM_ID, o.PATRIMONIO_ID, o.RESOLUCAO, o.DATA_RESOLUCAO,
                   o.CRIADO_EM, o.CRIADO_POR, o.ALTERADO_EM, o.ALTERADO_POR
            FROM {TABLE_NAME} o
            JOIN {TABLE_USUARIOS} u ON o.USUARIO_SOLICITANTE_ID = u.ID_USUARIO
            WHERE o.ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': ocorrencia_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'titulo': row[1],
                    'descricao': row[2],
                    'usuario_solicitante_id': row[3],
                    'solicitante_nome': row[4],
                    'tipo': row[5],
                    'prioridade': row[6],
                    'status': row[7],
                    'item_id': row[8],
                    'patrimonio_id': row[9],
                    'resolucao': row[10],
                    'data_resolucao': row[11],
                    'criado_em': row[12],
                    'criado_por': row[13],
                    'alterado_em': row[14],
                    'alterado_por': row[15]
                }
            return None
    
    @staticmethod
    def listar_todos(status: Optional[str] = None, tipo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todas as ocorrências, opcionalmente filtradas por status e/ou tipo"""
        where_clauses = []
        params = {}
        
        if status:
            where_clauses.append("o.STATUS = :status")
            params['status'] = status
        
        if tipo:
            where_clauses.append("o.TIPO = :tipo")
            params['tipo'] = tipo
        
        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        
        sql = f"""
            SELECT o.ID, o.TITULO, o.DESCRICAO, o.USUARIO_SOLICITANTE_ID,
                   u.NOME as SOLICITANTE_NOME, o.TIPO, o.PRIORIDADE, o.STATUS,
                   o.ITEM_ID, o.PATRIMONIO_ID, o.RESOLUCAO, o.DATA_RESOLUCAO,
                   o.CRIADO_EM, o.CRIADO_POR, o.ALTERADO_EM, o.ALTERADO_POR
            FROM {TABLE_NAME} o
            JOIN {TABLE_USUARIOS} u ON o.USUARIO_SOLICITANTE_ID = u.ID_USUARIO
            {where_sql}
            ORDER BY o.CRIADO_EM DESC
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'titulo': row[1],
                    'descricao': row[2],
                    'usuario_solicitante_id': row[3],
                    'solicitante_nome': row[4],
                    'tipo': row[5],
                    'prioridade': row[6],
                    'status': row[7],
                    'item_id': row[8],
                    'patrimonio_id': row[9],
                    'resolucao': row[10],
                    'data_resolucao': row[11],
                    'criado_em': row[12],
                    'criado_por': row[13],
                    'alterado_em': row[14],
                    'alterado_por': row[15]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(ocorrencia_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza uma ocorrência"""
        campos = []
        params = {'id': ocorrencia_id, 'alterado_por': alterado_por}
        
        if 'titulo' in dados:
            campos.append("TITULO = :titulo")
            params['titulo'] = dados['titulo']
        
        if 'descricao' in dados:
            campos.append("DESCRICAO = :descricao")
            params['descricao'] = dados['descricao']
        
        if 'tipo' in dados:
            campos.append("TIPO = :tipo")
            params['tipo'] = dados['tipo']
        
        if 'prioridade' in dados:
            campos.append("PRIORIDADE = :prioridade")
            params['prioridade'] = dados['prioridade']
        
        if 'status' in dados:
            campos.append("STATUS = :status")
            params['status'] = dados['status']
        
        if 'item_id' in dados:
            campos.append("ITEM_ID = :item_id")
            params['item_id'] = dados['item_id']
        
        if 'patrimonio_id' in dados:
            campos.append("PATRIMONIO_ID = :patrimonio_id")
            params['patrimonio_id'] = dados['patrimonio_id']
        
        if 'resolucao' in dados:
            campos.append("RESOLUCAO = :resolucao")
            params['resolucao'] = dados['resolucao']
        
        if 'data_resolucao' in dados:
            campos.append("DATA_RESOLUCAO = :data_resolucao")
            params['data_resolucao'] = dados['data_resolucao']
        
        if not campos:
            return False
        
        campos.append("ALTERADO_EM = CURRENT_TIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def fechar(ocorrencia_id: int, resolucao: str, alterado_por: Optional[int] = None) -> bool:
        """Fecha uma ocorrência"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET STATUS = 'FECHADO',
                RESOLUCAO = :resolucao,
                DATA_RESOLUCAO = CURRENT_TIMESTAMP,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'id': ocorrencia_id,
                'resolucao': resolucao,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(ocorrencia_id: int) -> bool:
        """Deleta uma ocorrência"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': ocorrencia_id})
            return cursor.rowcount > 0
