"""
Repository para operações de banco de dados relacionadas a Estoque
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


# Nome da tabela no PostgreSQL
TABLE_NAME = "ESTOQUES_TI_ESTOQUE_SALDO"
TABLE_ITENS = "ESTOQUES_TI_ITENS"


class EstoqueRepository:
    """Repository para gerenciar estoque no banco de dados"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo registro de estoque"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (ITEM_ID, QUANTIDADE, QUANTIDADE_MINIMA, LOCALIZACAO, CRIADO_POR)
            VALUES (:item_id, :quantidade, :quantidade_minima, :localizacao, :criado_por)
            RETURNING ID
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'item_id': dados['item_id'],
                'quantidade': dados.get('quantidade', 0),
                'quantidade_minima': dados.get('quantidade_minima', 0),
                'localizacao': dados.get('localizacao'),
                'criado_por': usuario_id,
            })
            return cursor.fetchone()[0]
    
    @staticmethod
    def buscar_por_id(estoque_id: int) -> Optional[Dict[str, Any]]:
        """Busca estoque por ID"""
        sql = f"""
            SELECT e.ID, e.ITEM_ID, i.NOME as ITEM_NOME, e.QUANTIDADE, 
                   e.QUANTIDADE_MINIMA, e.LOCALIZACAO,
                   e.CRIADO_EM, e.CRIADO_POR, e.ALTERADO_EM, e.ALTERADO_POR
            FROM {TABLE_NAME} e
            JOIN {TABLE_ITENS} i ON e.ITEM_ID = i.ID
            WHERE e.ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': estoque_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'quantidade': row[3],
                    'quantidade_minima': row[4],
                    'localizacao': row[5],
                    'criado_em': row[6],
                    'criado_por': row[7],
                    'alterado_em': row[8],
                    'alterado_por': row[9]
                }
            return None
    
    @staticmethod
    def buscar_por_item(item_id: int) -> Optional[Dict[str, Any]]:
        """Busca estoque por item_id"""
        sql = f"""
            SELECT e.ID, e.ITEM_ID, i.NOME as ITEM_NOME, e.QUANTIDADE, 
                   e.QUANTIDADE_MINIMA, e.LOCALIZACAO,
                   e.CRIADO_EM, e.CRIADO_POR, e.ALTERADO_EM, e.ALTERADO_POR
            FROM {TABLE_NAME} e
            JOIN {TABLE_ITENS} i ON e.ITEM_ID = i.ID
            WHERE e.ITEM_ID = :item_id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'item_id': item_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'quantidade': row[3],
                    'quantidade_minima': row[4],
                    'localizacao': row[5],
                    'criado_em': row[6],
                    'criado_por': row[7],
                    'alterado_em': row[8],
                    'alterado_por': row[9]
                }
            return None
    
    @staticmethod
    def listar_todos() -> List[Dict[str, Any]]:
        """Lista todo o estoque"""
        sql = f"""
            SELECT e.ID, e.ITEM_ID, i.NOME as ITEM_NOME, e.QUANTIDADE, 
                   e.QUANTIDADE_MINIMA, e.LOCALIZACAO,
                   e.CRIADO_EM, e.CRIADO_POR, e.ALTERADO_EM, e.ALTERADO_POR
            FROM {TABLE_NAME} e
            JOIN {TABLE_ITENS} i ON e.ITEM_ID = i.ID
            ORDER BY i.NOME
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'quantidade': row[3],
                    'quantidade_minima': row[4],
                    'localizacao': row[5],
                    'criado_em': row[6],
                    'criado_por': row[7],
                    'alterado_em': row[8],
                    'alterado_por': row[9]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar_quantidade(item_id: int, quantidade: int, alterado_por: Optional[int] = None) -> bool:
        """Atualiza a quantidade de um item no estoque"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET QUANTIDADE = :quantidade,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ITEM_ID = :item_id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'item_id': item_id,
                'quantidade': quantidade,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def entrada(item_id: int, quantidade: int, alterado_por: Optional[int] = None) -> bool:
        """Adiciona quantidade ao estoque"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET QUANTIDADE = QUANTIDADE + :quantidade,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ITEM_ID = :item_id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'item_id': item_id,
                'quantidade': quantidade,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def saida(item_id: int, quantidade: int, alterado_por: Optional[int] = None) -> bool:
        """Remove quantidade do estoque (com validação de quantidade negativa)"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET QUANTIDADE = QUANTIDADE - :quantidade,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ITEM_ID = :item_id
            AND QUANTIDADE >= :quantidade
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'item_id': item_id,
                'quantidade': quantidade,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(estoque_id: int) -> bool:
        """Deleta um registro de estoque"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': estoque_id})
            return cursor.rowcount > 0
