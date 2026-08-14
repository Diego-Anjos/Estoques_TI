"""
Router para endpoints de Usuários
"""
from fastapi import APIRouter, status, Query
from typing import List, Optional
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioLogin, UsuarioLoginResponse
from app.services.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate):
    """Cria um novo usuário"""
    return UsuarioService.criar_usuario(dados)


@router.post("/login", response_model=UsuarioLoginResponse)
def login(dados: UsuarioLogin):
    """Realiza login do usuário"""
    return UsuarioService.login(dados)


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    nome: Optional[str] = Query(None, description="Filtro parcial por nome"),
    email: Optional[str] = Query(None, description="Filtro parcial por email"),
    skip: int = Query(0, ge=0, description="Registros a pular (paginação)"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="Máximo de registros"),
    apenas_ativos: Optional[bool] = Query(
        None,
        description="True = só ativos, False = só inativos, omitir = todos",
    ),
):
    """Lista usuários (Oracle) com filtros e paginação opcionais."""
    return UsuarioService.listar_usuarios(
        nome=nome,
        email=email,
        skip=skip,
        limit=limit,
        apenas_ativos=apenas_ativos,
    )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int):
    """Busca usuário por ID"""
    return UsuarioService.buscar_usuario(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate):
    """Atualiza parcialmente um usuário (nome, email, cargo e/ou senha)."""
    return UsuarioService.atualizar_usuario(usuario_id, dados)


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def deletar_usuario(usuario_id: int):
    """Inativa um usuário (soft delete)."""
    return UsuarioService.deletar_usuario(usuario_id)
