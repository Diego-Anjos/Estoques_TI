"""
Repository para operações de banco de dados relacionadas a Usuários
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor
from app.core.security import hash_password

# Nome da tabela no PostgreSQL
TABLE_NAME = "ESTOQUES_TI_USUARIOS"


class UsuarioRepository:
    """Repository para gerenciar usuários no PostgreSQL"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo usuário"""
        senha_hash = hash_password(dados['senha'])
        
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, EMAIL, SENHA_HASH, CARGO, ATIVO, CRIADO_POR)
            VALUES (:nome, :email, :senha_hash, :cargo, :ativo, :criado_por)
            RETURNING ID_USUARIO
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'nome': dados['nome'],
                'email': dados['email'],
                'senha_hash': senha_hash,
                'cargo': dados.get('cargo') or None,
                'ativo': dados.get('ativo', 'S'),
                'criado_por': usuario_id,
            })
            return cursor.fetchone()[0]
    
    @staticmethod
    def buscar_por_id(usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID"""
        sql = f"""
            SELECT ID_USUARIO, NOME, EMAIL, CARGO, ATIVO, 
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
                    'cargo': row[3],
                    'ativo': row[4],
                    'data_criacao': row[5],
                    'criado_por': row[6],
                    'data_alteracao': row[7],
                    'alterado_por': row[8]
                }
            return None
    
    @staticmethod
    def buscar_por_email(email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email (para login). Comparação case-insensitive."""
        sql = f"""
            SELECT ID_USUARIO, NOME, EMAIL, SENHA_HASH, CARGO, ATIVO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE LOWER(EMAIL) = LOWER(:email)
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
                    'cargo': row[4],
                    'ativo': row[5],
                    'data_criacao': row[6],
                    'criado_por': row[7],
                    'data_alteracao': row[8],
                    'alterado_por': row[9]
                }
            return None
    
    @staticmethod
    def listar(
        nome: Optional[str] = None,
        email: Optional[str] = None,
        skip: int = 0,
        limit: Optional[int] = None,
        status_filtro: str = "ativos",
        apenas_ativos: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Lista usuários com filtros opcionais e paginação (skip/limit)."""
        where = []
        params: Dict[str, Any] = {}

        # Compatibilidade: apenas_ativos sobrescreve se status_filtro não for explícito via service
        if apenas_ativos is True:
            where.append("ATIVO = 'S'")
        elif apenas_ativos is False:
            where.append("ATIVO = 'N'")
        elif status_filtro == "ativos":
            where.append("ATIVO = 'S'")
        elif status_filtro == "inativos":
            where.append("ATIVO = 'N'")
        # status_filtro == "todos" → sem filtro de ATIVO

        if nome:
            where.append("UPPER(NOME) LIKE UPPER(:nome)")
            params["nome"] = f"%{nome.strip()}%"

        if email:
            where.append("UPPER(EMAIL) LIKE UPPER(:email)")
            params["email"] = f"%{email.strip()}%"

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""

        # Paginação PostgreSQL
        pagination_sql = ""
        if limit is not None:
            pagination_sql = " LIMIT :limit OFFSET :skip"
            params["skip"] = max(0, int(skip))
            params["limit"] = max(1, int(limit))

        sql = f"""
            SELECT ID_USUARIO, NOME, EMAIL, CARGO, ATIVO,
                   DATA_CRIACAO, CRIADO_POR, DATA_ALTERACAO, ALTERADO_POR
            FROM {TABLE_NAME}
            {where_sql}
            ORDER BY NOME
            {pagination_sql}
        """

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

            return [
                {
                    "id_usuario": row[0],
                    "nome": row[1],
                    "email": row[2],
                    "cargo": row[3],
                    "ativo": row[4],
                    "data_criacao": row[5],
                    "criado_por": row[6],
                    "data_alteracao": row[7],
                    "alterado_por": row[8],
                }
                for row in rows
            ]

    @staticmethod
    def contar(
        nome: Optional[str] = None,
        email: Optional[str] = None,
        status_filtro: str = "ativos",
        apenas_ativos: Optional[bool] = None,
    ) -> int:
        """Conta usuários com os mesmos filtros de listar."""
        where = []
        params: Dict[str, Any] = {}

        if apenas_ativos is True:
            where.append("ATIVO = 'S'")
        elif apenas_ativos is False:
            where.append("ATIVO = 'N'")
        elif status_filtro == "ativos":
            where.append("ATIVO = 'S'")
        elif status_filtro == "inativos":
            where.append("ATIVO = 'N'")

        if nome:
            where.append("UPPER(NOME) LIKE UPPER(:nome)")
            params["nome"] = f"%{nome.strip()}%"

        if email:
            where.append("UPPER(EMAIL) LIKE UPPER(:email)")
            params["email"] = f"%{email.strip()}%"

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        sql = f"SELECT COUNT(*) FROM {TABLE_NAME} {where_sql}"

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return int(cursor.fetchone()[0])

    @staticmethod
    def listar_todos(apenas_ativos: bool = True) -> List[Dict[str, Any]]:
        """Lista todos os usuários (compatibilidade)."""
        return UsuarioRepository.listar(
            status_filtro="ativos" if apenas_ativos else "todos"
        )
    
    @staticmethod
    def atualizar(usuario_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um usuário (parcial). Senha é hasheada com bcrypt antes de salvar."""
        campos = []
        params = {'id': usuario_id, 'alterado_por': alterado_por}
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'email' in dados:
            campos.append("EMAIL = :email")
            params['email'] = dados['email']

        if 'cargo' in dados:
            campos.append("CARGO = :cargo")
            params['cargo'] = dados['cargo'] if dados['cargo'] else None
        
        if 'senha' in dados and dados['senha']:
            campos.append("SENHA_HASH = :senha_hash")
            params['senha_hash'] = hash_password(dados['senha'])
        
        if 'ativo' in dados:
            campos.append("ATIVO = :ativo")
            params['ativo'] = dados['ativo']
        
        if not campos:
            return False
        
        campos.append("DATA_ALTERACAO = NOW()")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID_USUARIO = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0

    @staticmethod
    def reativar(
        usuario_id: int,
        dados: Dict[str, Any],
        alterado_por: Optional[int] = None,
    ) -> bool:
        """
        Reativa um usuário soft-deleted (ATIVO='N'):
        atualiza nome, cargo, senha e volta ATIVO='S', preservando o ID.
        """
        sql = f"""
            UPDATE {TABLE_NAME}
            SET NOME = :nome,
                CARGO = :cargo,
                SENHA_HASH = :senha_hash,
                ATIVO = 'S',
                DATA_ALTERACAO = NOW(),
                ALTERADO_POR = :alterado_por
            WHERE ID_USUARIO = :id
              AND ATIVO = 'N'
        """
        with get_cursor() as cursor:
            cursor.execute(
                sql,
                {
                    "id": usuario_id,
                    "nome": dados["nome"],
                    "cargo": dados.get("cargo") or None,
                    "senha_hash": hash_password(dados["senha"]),
                    "alterado_por": alterado_por,
                },
            )
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
