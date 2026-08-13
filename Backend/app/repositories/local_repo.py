"""
Repository para operações de banco de dados relacionadas a Locais
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor

# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_LOCAIS"


class LocalRepository:
    """Repository para gerenciar locais no banco de dados Oracle"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo local"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, DESCRICAO, CRIADO_POR)
            VALUES (:nome, :descricao, :criado_por)
            RETURNING ID_LOCAL INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'nome': dados['nome'],
                'descricao': dados.get('descricao'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(local_id: int) -> Optional[Dict[str, Any]]:
        """Busca local por ID"""
        sql = f"""
            SELECT ID_LOCAL, NOME, DESCRICAO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE ID_LOCAL = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': local_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_local': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'data_criacao': row[3],
                    'criado_por': row[4],
                    'data_alteracao': row[5],
                    'alterado_por': row[6]
                }
            return None
    
    @staticmethod
    def buscar_por_nome(nome: str) -> Optional[Dict[str, Any]]:
        """Busca local por nome"""
        sql = f"""
            SELECT ID_LOCAL, NOME, DESCRICAO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE UPPER(NOME) = UPPER(:nome)
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'nome': nome})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_local': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'data_criacao': row[3],
                    'criado_por': row[4],
                    'data_alteracao': row[5],
                    'alterado_por': row[6]
                }
            return None
    
    @staticmethod
    def listar_todos() -> List[Dict[str, Any]]:
        """Lista todos os locais"""
        sql = f"""
            SELECT ID_LOCAL, NOME, DESCRICAO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            ORDER BY NOME
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [
                {
                    'id_local': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'data_criacao': row[3],
                    'criado_por': row[4],
                    'data_alteracao': row[5],
                    'alterado_por': row[6]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(local_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um local"""
        campos = []
        params = {'id': local_id, 'alterado_por': alterado_por}
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'descricao' in dados:
            campos.append("DESCRICAO = :descricao")
            params['descricao'] = dados['descricao']
        
        if not campos:
            return False
        
        campos.append("DATA_ALTERACAO = SYSTIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_LOCAL = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(local_id: int) -> bool:
        """Deleta um local"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_LOCAL = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': local_id})
            return cursor.rowcount > 0
