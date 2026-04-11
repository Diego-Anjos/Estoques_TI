"""
Repository para operações de banco de dados relacionadas a Patrimônio
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_PATRIMONIOS"
TABLE_ITENS = "ESTOQUES_TI_ITENS"


class PatrimonioRepository:
    """Repository para gerenciar patrimônio no banco de dados"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo patrimônio"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (ITEM_ID, NUMERO_SERIE, NUMERO_PATRIMONIO, STATUS, 
                                   LOCALIZACAO, USUARIO_RESPONSAVEL_ID, OBSERVACOES, CRIADO_POR)
            VALUES (:item_id, :numero_serie, :numero_patrimonio, :status, 
                    :localizacao, :usuario_responsavel_id, :observacoes, :criado_por)
            RETURNING ID INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'item_id': dados['item_id'],
                'numero_serie': dados['numero_serie'],
                'numero_patrimonio': dados.get('numero_patrimonio'),
                'status': dados.get('status', 'DISPONIVEL'),
                'localizacao': dados.get('localizacao'),
                'usuario_responsavel_id': dados.get('usuario_responsavel_id'),
                'observacoes': dados.get('observacoes'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(patrimonio_id: int) -> Optional[Dict[str, Any]]:
        """Busca patrimônio por ID"""
        sql = f"""
            SELECT p.ID, p.ITEM_ID, i.NOME as ITEM_NOME, p.NUMERO_SERIE, p.NUMERO_PATRIMONIO,
                   p.STATUS, p.LOCALIZACAO, p.USUARIO_RESPONSAVEL_ID, p.OBSERVACOES,
                   p.CRIADO_EM, p.CRIADO_POR, p.ALTERADO_EM, p.ALTERADO_POR
            FROM {TABLE_NAME} p
            JOIN {TABLE_ITENS} i ON p.ITEM_ID = i.ID
            WHERE p.ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': patrimonio_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'numero_serie': row[3],
                    'numero_patrimonio': row[4],
                    'status': row[5],
                    'localizacao': row[6],
                    'usuario_responsavel_id': row[7],
                    'observacoes': row[8],
                    'criado_em': row[9],
                    'criado_por': row[10],
                    'alterado_em': row[11],
                    'alterado_por': row[12]
                }
            return None
    
    @staticmethod
    def buscar_por_numero_serie(numero_serie: str) -> Optional[Dict[str, Any]]:
        """Busca patrimônio por número de série"""
        sql = f"""
            SELECT p.ID, p.ITEM_ID, i.NOME as ITEM_NOME, p.NUMERO_SERIE, p.NUMERO_PATRIMONIO,
                   p.STATUS, p.LOCALIZACAO, p.USUARIO_RESPONSAVEL_ID, p.OBSERVACOES,
                   p.CRIADO_EM, p.CRIADO_POR, p.ALTERADO_EM, p.ALTERADO_POR
            FROM {TABLE_NAME} p
            JOIN {TABLE_ITENS} i ON p.ITEM_ID = i.ID
            WHERE p.NUMERO_SERIE = :numero_serie
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'numero_serie': numero_serie})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'numero_serie': row[3],
                    'numero_patrimonio': row[4],
                    'status': row[5],
                    'localizacao': row[6],
                    'usuario_responsavel_id': row[7],
                    'observacoes': row[8],
                    'criado_em': row[9],
                    'criado_por': row[10],
                    'alterado_em': row[11],
                    'alterado_por': row[12]
                }
            return None
    
    @staticmethod
    def listar_todos(status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todos os patrimônios, opcionalmente filtrados por status"""
        if status:
            sql = f"""
                SELECT p.ID, p.ITEM_ID, i.NOME as ITEM_NOME, p.NUMERO_SERIE, p.NUMERO_PATRIMONIO,
                       p.STATUS, p.LOCALIZACAO, p.USUARIO_RESPONSAVEL_ID, p.OBSERVACOES,
                       p.CRIADO_EM, p.CRIADO_POR, p.ALTERADO_EM, p.ALTERADO_POR
                FROM {TABLE_NAME} p
                JOIN {TABLE_ITENS} i ON p.ITEM_ID = i.ID
                WHERE p.STATUS = :status
                ORDER BY i.NOME, p.NUMERO_SERIE
            """
            params = {'status': status}
        else:
            sql = f"""
                SELECT p.ID, p.ITEM_ID, i.NOME as ITEM_NOME, p.NUMERO_SERIE, p.NUMERO_PATRIMONIO,
                       p.STATUS, p.LOCALIZACAO, p.USUARIO_RESPONSAVEL_ID, p.OBSERVACOES,
                       p.CRIADO_EM, p.CRIADO_POR, p.ALTERADO_EM, p.ALTERADO_POR
                FROM {TABLE_NAME} p
                JOIN {TABLE_ITENS} i ON p.ITEM_ID = i.ID
                ORDER BY i.NOME, p.NUMERO_SERIE
            """
            params = {}
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'item_id': row[1],
                    'item_nome': row[2],
                    'numero_serie': row[3],
                    'numero_patrimonio': row[4],
                    'status': row[5],
                    'localizacao': row[6],
                    'usuario_responsavel_id': row[7],
                    'observacoes': row[8],
                    'criado_em': row[9],
                    'criado_por': row[10],
                    'alterado_em': row[11],
                    'alterado_por': row[12]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(patrimonio_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um patrimônio"""
        campos = []
        params = {'id': patrimonio_id, 'alterado_por': alterado_por}
        
        if 'numero_serie' in dados:
            campos.append("NUMERO_SERIE = :numero_serie")
            params['numero_serie'] = dados['numero_serie']
        
        if 'numero_patrimonio' in dados:
            campos.append("NUMERO_PATRIMONIO = :numero_patrimonio")
            params['numero_patrimonio'] = dados['numero_patrimonio']
        
        if 'status' in dados:
            campos.append("STATUS = :status")
            params['status'] = dados['status']
        
        if 'localizacao' in dados:
            campos.append("LOCALIZACAO = :localizacao")
            params['localizacao'] = dados['localizacao']
        
        if 'usuario_responsavel_id' in dados:
            campos.append("USUARIO_RESPONSAVEL_ID = :usuario_responsavel_id")
            params['usuario_responsavel_id'] = dados['usuario_responsavel_id']
        
        if 'observacoes' in dados:
            campos.append("OBSERVACOES = :observacoes")
            params['observacoes'] = dados['observacoes']
        
        if not campos:
            return False
        
        campos.append("ALTERADO_EM = CURRENT_TIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(patrimonio_id: int) -> bool:
        """Deleta um patrimônio"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': patrimonio_id})
            return cursor.rowcount > 0
