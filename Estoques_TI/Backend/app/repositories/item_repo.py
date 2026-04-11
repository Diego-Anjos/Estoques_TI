"""
Repository para operações de banco de dados relacionadas a Itens
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_ITENS"


class ItemRepository:
    """Repository para gerenciar itens no banco de dados"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo item"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, DESCRICAO, TIPO, CATEGORIA, CRIADO_POR)
            VALUES (:nome, :descricao, :tipo, :categoria, :criado_por)
            RETURNING ID INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'nome': dados['nome'],
                'descricao': dados.get('descricao'),
                'tipo': dados['tipo'],
                'categoria': dados.get('categoria'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(item_id: int) -> Optional[Dict[str, Any]]:
        """Busca item por ID"""
        sql = f"""
            SELECT ID, NOME, DESCRICAO, TIPO, CATEGORIA, 
                   CRIADO_EM, CRIADO_POR, ALTERADO_EM, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': item_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'tipo': row[3],
                    'categoria': row[4],
                    'criado_em': row[5],
                    'criado_por': row[6],
                    'alterado_em': row[7],
                    'alterado_por': row[8]
                }
            return None
    
    @staticmethod
    def listar_todos(tipo: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todos os itens, opcionalmente filtrados por tipo"""
        if tipo:
            sql = f"""
                SELECT ID, NOME, DESCRICAO, TIPO, CATEGORIA,
                       CRIADO_EM, CRIADO_POR, ALTERADO_EM, ALTERADO_POR
                FROM {TABLE_NAME}
                WHERE TIPO = :tipo
                ORDER BY NOME
            """
            params = {'tipo': tipo}
        else:
            sql = f"""
                SELECT ID, NOME, DESCRICAO, TIPO, CATEGORIA,
                       CRIADO_EM, CRIADO_POR, ALTERADO_EM, ALTERADO_POR
                FROM {TABLE_NAME}
                ORDER BY NOME
            """
            params = {}
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'tipo': row[3],
                    'categoria': row[4],
                    'criado_em': row[5],
                    'criado_por': row[6],
                    'alterado_em': row[7],
                    'alterado_por': row[8]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(item_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um item"""
        campos = []
        params = {'id': item_id, 'alterado_por': alterado_por}
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'descricao' in dados:
            campos.append("DESCRICAO = :descricao")
            params['descricao'] = dados['descricao']
        
        if 'tipo' in dados:
            campos.append("TIPO = :tipo")
            params['tipo'] = dados['tipo']
        
        if 'categoria' in dados:
            campos.append("CATEGORIA = :categoria")
            params['categoria'] = dados['categoria']
        
        if not campos:
            return False
        
        campos.append("ALTERADO_EM = CURRENT_TIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(item_id: int) -> bool:
        """Deleta um item"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': item_id})
            return cursor.rowcount > 0
