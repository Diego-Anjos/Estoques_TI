"""
Repository para operações de banco de dados relacionadas a Usuários
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor
from app.core.security import hash_password
from datetime import datetime

# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_USUARIOS"


class UsuarioRepository:
    """Repository para gerenciar usuários no banco de dados Oracle"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo usuário"""
        senha_hash = hash_password(dados['senha'])
        
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, EMAIL, SENHA_HASH, ATIVO, CRIADO_POR)
            VALUES (:nome, :email, :senha_hash, :ativo, :criado_por)
            RETURNING ID_USUARIO INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'nome': dados['nome'],
                'email': dados['email'],
                'senha_hash': senha_hash,
                'ativo': dados.get('ativo', 'S'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID"""
        sql = f"""
            SELECT ID_USUARIO, NOME, EMAIL, ATIVO, 
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE ID_USUARIO = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': usuario_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_usuario': row[0],
                    'nome': row[1],
                    'email': row[2],
                    'ativo': row[3],
                    'data_criacao': row[4],
                    'criado_por': row[5],
                    'data_alteracao': row[6],
                    'alterado_por': row[7]
                }
            return None
    
    @staticmethod
    def buscar_por_email(email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email (para login)"""
        sql = f"""
            SELECT ID_USUARIO, NOME, EMAIL, SENHA_HASH, ATIVO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE EMAIL = :email
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'email': email})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id_usuario': row[0],
                    'nome': row[1],
                    'email': row[2],
                    'senha_hash': row[3],
                    'ativo': row[4],
                    'data_criacao': row[5],
                    'criado_por': row[6],
                    'data_alteracao': row[7],
                    'alterado_por': row[8]
                }
            return None
    
    @staticmethod
    def listar_todos(apenas_ativos: bool = True) -> List[Dict[str, Any]]:
        """Lista todos os usuários"""
        if apenas_ativos:
            sql = f"""
                SELECT ID_USUARIO, NOME, EMAIL, ATIVO,
                       DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
                FROM {TABLE_NAME}
                WHERE ATIVO = 'S'
                ORDER BY NOME
            """
        else:
            sql = f"""
                SELECT ID_USUARIO, NOME, EMAIL, ATIVO,
                       DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
                FROM {TABLE_NAME}
                ORDER BY NOME
            """
        
        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [
                {
                    'id_usuario': row[0],
                    'nome': row[1],
                    'email': row[2],
                    'ativo': row[3],
                    'data_criacao': row[4],
                    'criado_por': row[5],
                    'data_alteracao': row[6],
                    'alterado_por': row[7]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(usuario_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um usuário"""
        campos = []
        params = {'id': usuario_id, 'alterado_por': alterado_por}
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'email' in dados:
            campos.append("EMAIL = :email")
            params['email'] = dados['email']
        
        if 'senha' in dados:
            campos.append("SENHA_HASH = :senha_hash")
            params['senha_hash'] = hash_password(dados['senha'])
        
        if 'ativo' in dados:
            campos.append("ATIVO = :ativo")
            params['ativo'] = dados['ativo']
        
        if not campos:
            return False
        
        campos.append("DATA_ALTERACAO = SYSTIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_USUARIO = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(usuario_id: int) -> bool:
        """Deleta um usuário (soft delete - marca como inativo)"""
        sql = f"UPDATE {TABLE_NAME} SET ATIVO = 'N' WHERE ID_USUARIO = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': usuario_id})
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar_permanente(usuario_id: int) -> bool:
        """Deleta permanentemente um usuário (usar com cuidado)"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID_USUARIO = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': usuario_id})
            return cursor.rowcount > 0
