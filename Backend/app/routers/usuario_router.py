"""
Router para endpoints de Usuários
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Any, List, Optional
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin, UsuarioLoginResponse
from app.services.usuario_service import UsuarioService
from app.core.deps import get_current_active_user
from app.core.status_filter import normalizar_status_filtro


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(dados: UsuarioCreate):
    """
    Cadastro público (tela de registro).
    Não exige JWT — necessário para o primeiro usuário e auto-cadastro.
    Body JSON: { nome, email, senha, ativo? }
    """
    return UsuarioService.criar_usuario(dados, usuario_id=None)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    dados: UsuarioCreate,
    current_user: dict[str, Any] = Depends(get_current_active_user),
):
    """Cria um novo usuário (admin autenticado — dashboard)."""
    return UsuarioService.criar_usuario(dados, usuario_id=current_user["id_usuario"])


@router.post("/login", response_model=UsuarioLoginResponse)
def login(dados: UsuarioLogin):
    """
    Login público com JSON (não OAuth2 form).
    Body: { "email": "...", "senha": "..." } → JWT em access_token.
    """
    return UsuarioService.login(dados)


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    nome: Optional[str] = Query(None, description="Filtro parcial por nome"),
    email: Optional[str] = Query(None, description="Filtro parcial por email"),
    skip: int = Query(0, ge=0, description="Registros a pular (paginação)"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Máximo de registros"),
    status_filtro: Optional[str] = Query(
        None,
        alias="status",
        description="Filtro de status: ativos (padrão), inativos ou todos",
    ),
    _current_user: dict[str, Any] = Depends(get_current_active_user),
):
    """Lista usuários. Por padrão retorna apenas ATIVO='S'."""
    return UsuarioService.listar_usuarios(
        nome=nome,
        email=email,
        skip=skip,
        limit=limit,
        status_filtro=normalizar_status_filtro(status_filtro),
    )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(
    usuario_id: int,
    _current_user: dict[str, Any] = Depends(get_current_active_user),
):
    """Busca usuário por ID"""
    return UsuarioService.buscar_usuario(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    current_user: dict[str, Any] = Depends(get_current_active_user),
):
    """Atualiza parcialmente um usuário (nome, email, cargo e/ou senha)."""
    return UsuarioService.atualizar_usuario(
        usuario_id, dados, alterado_por=current_user["id_usuario"]
    )


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def deletar_usuario(
    usuario_id: int,
    _current_user: dict[str, Any] = Depends(get_current_active_user),
):
    """Inativa um usuário (soft delete)."""
    return UsuarioService.deletar_usuario(usuario_id)
