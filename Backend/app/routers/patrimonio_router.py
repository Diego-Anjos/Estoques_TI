"""
Router para endpoints de Patrimônio
"""
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from app.schemas.patrimonio import PatrimonioCreate, PatrimonioUpdate, PatrimonioResponse
from app.services.patrimonio_service import PatrimonioService
from app.core.deps import get_current_active_user


router = APIRouter(
    prefix="/patrimonio",
    tags=["Patrimônio"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=PatrimonioResponse, status_code=status.HTTP_201_CREATED)
def criar_patrimonio(dados: PatrimonioCreate):
    """Cria um novo patrimônio"""
    return PatrimonioService.criar_patrimonio(dados)


@router.get("/", response_model=List[PatrimonioResponse])
def listar_patrimonios(status_filtro: Optional[str] = Query(None, alias="status", description="Filtrar por status")):
    """Lista todos os patrimônios, opcionalmente filtrados por status"""
    return PatrimonioService.listar_patrimonios(status_filtro)


@router.get("/{patrimonio_id}", response_model=PatrimonioResponse)
def buscar_patrimonio(patrimonio_id: int):
    """Busca patrimônio por ID"""
    return PatrimonioService.buscar_patrimonio(patrimonio_id)


@router.put("/{patrimonio_id}", response_model=PatrimonioResponse)
def atualizar_patrimonio(patrimonio_id: int, dados: PatrimonioUpdate):
    """Atualiza um patrimônio"""
    return PatrimonioService.atualizar_patrimonio(patrimonio_id, dados)


@router.delete("/{patrimonio_id}", status_code=status.HTTP_200_OK)
def deletar_patrimonio(patrimonio_id: int):
    """Deleta um patrimônio"""
    return PatrimonioService.deletar_patrimonio(patrimonio_id)
