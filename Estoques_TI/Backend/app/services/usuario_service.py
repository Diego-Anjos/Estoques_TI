"""
Service para lógica de negócio relacionada a Usuários
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin, UsuarioLoginResponse
from app.core.security import verify_password


class UsuarioService:
    """Service para gerenciar usuários"""
    
    @staticmethod
    def criar_usuario(dados: UsuarioCreate, usuario_id: Optional[int] = None) -> UsuarioResponse:
        """Cria um novo usuário"""
        # Verifica se email já existe
        usuario_existente = UsuarioRepository.buscar_por_email(dados.email)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Cria usuário
        dados_dict = dados.model_dump()
        novo_id = UsuarioRepository.criar(dados_dict, usuario_id)
        
        # Busca e retorna usuário criado
        usuario = UsuarioRepository.buscar_por_id(novo_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar usuário"
            )
        
        return UsuarioResponse(**usuario)
    
    @staticmethod
    def buscar_usuario(usuario_id: int) -> UsuarioResponse:
        """Busca usuário por ID"""
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return UsuarioResponse(**usuario)
    
    @staticmethod
    def listar_usuarios() -> List[UsuarioResponse]:
        """Lista todos os usuários"""
        usuarios = UsuarioRepository.listar_todos()
        return [UsuarioResponse(**u) for u in usuarios]
    
    @staticmethod
    def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, alterado_por: Optional[int] = None) -> UsuarioResponse:
        """Atualiza um usuário"""
        # Verifica se usuário existe
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Verifica se email já está em uso por outro usuário
        if dados.email:
            usuario_email = UsuarioRepository.buscar_por_email(dados.email)
            if usuario_email and usuario_email['id'] != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro usuário"
                )
        
        # Atualiza usuário
        dados_dict = dados.model_dump(exclude_unset=True)
        if not dados_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado para atualizar"
            )
        
        sucesso = UsuarioRepository.atualizar(usuario_id, dados_dict, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar usuário"
            )
        
        # Busca e retorna usuário atualizado
        usuario_atualizado = UsuarioRepository.buscar_por_id(usuario_id)
        return UsuarioResponse(**usuario_atualizado)
    
    @staticmethod
    def deletar_usuario(usuario_id: int) -> dict:
        """Deleta um usuário"""
        # Verifica se usuário existe
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Deleta usuário
        sucesso = UsuarioRepository.deletar(usuario_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar usuário"
            )
        
        return {"mensagem": "Usuário deletado com sucesso"}
    
    @staticmethod
    def login(dados: UsuarioLogin) -> UsuarioLoginResponse:
        """Realiza login do usuário"""
        # Busca usuário por email
        usuario = UsuarioRepository.buscar_por_email(dados.email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Verifica senha
        if not verify_password(dados.senha, usuario['senha_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return UsuarioLoginResponse(
            id=usuario['id'],
            nome=usuario['nome'],
            email=usuario['email']
        )
