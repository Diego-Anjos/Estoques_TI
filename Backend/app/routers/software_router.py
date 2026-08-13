"""
Router para endpoints de Software/Licenças
"""
from fastapi import APIRouter, status
from typing import List
from app.schemas.software import (
    SoftwareCreate, 
    SoftwareUpdate, 
    SoftwareResponse,
    SoftwareAtribuicaoCreate,
    SoftwareAtribuicaoResponse
)
from app.services.software_service import SoftwareService


router = APIRouter(prefix="/software", tags=["Software/Licenças"])


@router.post("/", response_model=SoftwareResponse, status_code=status.HTTP_201_CREATED)
def criar_software(dados: SoftwareCreate):
    """Cria um novo software"""
    return SoftwareService.criar_software(dados)


@router.get("/", response_model=List[SoftwareResponse])
def listar_softwares():
    """Lista todos os softwares"""
    return SoftwareService.listar_softwares()


@router.get("/{software_id}", response_model=SoftwareResponse)
def buscar_software(software_id: int):
    """Busca software por ID"""
    return SoftwareService.buscar_software(software_id)


@router.put("/{software_id}", response_model=SoftwareResponse)
def atualizar_software(software_id: int, dados: SoftwareUpdate):
    """Atualiza um software"""
    return SoftwareService.atualizar_software(software_id, dados)


@router.delete("/{software_id}", status_code=status.HTTP_200_OK)
def deletar_software(software_id: int):
    """Deleta um software"""
    return SoftwareService.deletar_software(software_id)
