"""
Router para endpoints de Usuários
"""
from fastapi import APIRouter, status
from typing import List
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
def listar_usuarios():
    """Lista todos os usuários"""
    return UsuarioService.listar_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int):
    """Busca usuário por ID"""
    return UsuarioService.buscar_usuario(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate):
    """Atualiza um usuário"""
    return UsuarioService.atualizar_usuario(usuario_id, dados)


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
def deletar_usuario(usuario_id: int):
    """Deleta um usuário"""
    return UsuarioService.deletar_usuario(usuario_id)
