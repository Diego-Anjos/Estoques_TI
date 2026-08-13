"""
Repository para operações de banco de dados relacionadas a Tipos de Item
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_TIPOS_ITEM"


class TipoItemRepository:
    """Repository para gerenciar tipos de item no banco de dados Oracle"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo tipo de item"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (CODIGO, NOME, SERIALIZADO, UNIDADE, CRIADO_POR)
            VALUES (:codigo, :nome, :serializado, :unidade, :criado_por)
            RETURNING ID_TIPO_ITEM INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'codigo': dados['codigo'],
                'nome': dados['nome'],
                'serializado': dados.get('serializado', 'N'),
                'unidade': dados.get('unidade', 'UN'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(tipo_item_id: int) -> Optional[Dict[str, Any]]:
        """Busca tipo de item por ID"""
        sql = f"""
            SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO, UNIDADE,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE ID_TIPO_ITEM = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': tipo_item_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_tipo_item': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'serializado': row[3],
                    'unidade': row[4],
                    'data_criacao': row[5],
                    'criado_por': row[6],
                    'data_alteracao': row[7],
                    'alterado_por': row[8]
                }
            return None
    
    @staticmethod
    def buscar_por_codigo(codigo: str) -> Optional[Dict[str, Any]]:
        """Busca tipo de item por código"""
        sql = f"""
            SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO, UNIDADE,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE UPPER(CODIGO) = UPPER(:codigo)
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'codigo': codigo})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_tipo_item': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'serializado': row[3],
                    'unidade': row[4],
                    'data_criacao': row[5],
                    'criado_por': row[6],
                    'data_alteracao': row[7],
                    'alterado_por': row[8]
                }
            return None
    
    @staticmethod
    def listar_todos(apenas_serializados: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Lista todos os tipos de item"""
        if apenas_serializados is True:
            sql = f"""
                SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO, UNIDADE,
                       DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
                FROM {TABLE_NAME}
                WHERE SERIALIZADO = 'S'
                ORDER BY NOME
            """
        elif apenas_serializados is False:
            sql = f"""
                SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO, UNIDADE,
                       DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
                FROM {TABLE_NAME}
                WHERE SERIALIZADO = 'N'
                ORDER BY NOME
            """
        else:
            sql = f"""
                SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO, UNIDADE,
                       DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
                FROM {TABLE_NAME}
                ORDER BY NOME
            """
        
        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [
                {
                    'id_tipo_item': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'serializado': row[3],
                    'unidade': row[4],
                    'data_criacao': row[5],
                    'criado_por': row[6],
                    'data_alteracao': row[7],
                    'alterado_por': row[8]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(tipo_item_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um tipo de item"""
        campos = []
        params = {'id': tipo_item_id, 'alterado_por': alterado_por}
        
        if 'codigo' in dados:
            campos.append("CODIGO = :codigo")
            params['codigo'] = dados['codigo']
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'serializado' in dados:
            campos.append("SERIALIZADO = :serializado")
            params['serializado'] = dados['serializado']
        
        if 'unidade' in dados:
            campos.append("UNIDADE = :unidade")
            params['unidade'] = dados['unidade']
        
        if not campos:
            return False
        
        campos.append("DATA_ALTERACAO = SYSTIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_TIPO_ITEM = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(tipo_item_id: int) -> bool:
        """Deleta um tipo de item"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_TIPO_ITEM = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': tipo_item_id})
            return cursor.rowcount > 0
