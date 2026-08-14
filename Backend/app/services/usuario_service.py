"""
Service para lógica de negócio relacionada a Usuários
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin, UsuarioLoginResponse
from app.core.security import create_access_token, verify_password


class UsuarioService:
    """Service para gerenciar usuários"""
    
    @staticmethod
    def criar_usuario(dados: UsuarioCreate, usuario_id: Optional[int] = None) -> UsuarioResponse:
        """
        Cria um novo usuário.
        Se o e-mail pertencer a um usuário inativo (ATIVO='N'), reativa o registro
        (UPDATE nome/cargo/senha + ATIVO='S') em vez de inserir outro.
        """
        usuario_existente = UsuarioRepository.buscar_por_email(dados.email)
        if usuario_existente:
            if usuario_existente.get("ativo") == "S":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado",
                )

            # Soft-deleted: reativa preservando o ID e o histórico
            sucesso = UsuarioRepository.reativar(
                usuario_existente["id_usuario"],
                dados.model_dump(),
                alterado_por=usuario_id,
            )
            if not sucesso:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao reativar usuário",
                )

            usuario = UsuarioRepository.buscar_por_id(usuario_existente["id_usuario"])
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao carregar usuário reativado",
                )
            return UsuarioResponse(**usuario)

        novo_id = UsuarioRepository.criar(dados.model_dump(), usuario_id)
        usuario = UsuarioRepository.buscar_por_id(novo_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar usuário",
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
    def listar_usuarios(
        nome: Optional[str] = None,
        email: Optional[str] = None,
        skip: int = 0,
        limit: Optional[int] = None,
        status_filtro: str = "ativos",
    ) -> List[UsuarioResponse]:
        """Lista usuários. Por padrão retorna apenas ativos (ATIVO='S')."""
        usuarios = UsuarioRepository.listar(
            nome=nome,
            email=email,
            skip=skip,
            limit=limit,
            status_filtro=status_filtro,
        )
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
            if usuario_email and usuario_email['id_usuario'] != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado para outro usuário"
                )
        
        # Atualiza usuário (parcial — só campos enviados)
        dados_dict = dados.model_dump(exclude_unset=True)

        # Senha vazia não deve ser atualizada
        if 'senha' in dados_dict and not dados_dict['senha']:
            del dados_dict['senha']

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
        """Realiza login do usuário e emite JWT."""
        usuario = UsuarioRepository.buscar_por_email(dados.email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
            )

        if not verify_password(dados.senha, usuario["senha_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
            )

        if usuario.get("ativo") != "S":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )

        token = create_access_token(
            subject=usuario["id_usuario"],
            extra_claims={"email": usuario["email"]},
        )
        return UsuarioLoginResponse(
            id_usuario=usuario["id_usuario"],
            nome=usuario["nome"],
            email=usuario["email"],
            cargo=usuario.get("cargo"),
            access_token=token,
        )
