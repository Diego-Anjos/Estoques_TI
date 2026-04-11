"""
Router para endpoints de Ocorrências
"""
from fastapi import APIRouter, status, Query
from typing import List, Optional
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaUpdate, OcorrenciaResponse, FecharOcorrenciaRequest, AlterarStatusRequest
from app.services.ocorrencia_service import OcorrenciaService


router = APIRouter(prefix="/ocorrencias", tags=["Ocorrências"])


@router.post("/", response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
def criar_ocorrencia(dados: OcorrenciaCreate):
    """Cria uma nova ocorrência"""
    return OcorrenciaService.criar_ocorrencia(dados)


@router.get("/", response_model=List[OcorrenciaResponse])
def listar_ocorrencias(
    status_filtro: Optional[str] = Query(None, alias="status", description="Filtrar por status"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo")
):
    """Lista todas as ocorrências, opcionalmente filtradas por status e/ou tipo"""
    return OcorrenciaService.listar_ocorrencias(status_filtro, tipo)


@router.get("/abertas", response_model=List[OcorrenciaResponse])
def listar_ocorrencias_abertas():
    """Lista apenas ocorrências abertas (status diferente de FECHADO)"""
    return OcorrenciaService.listar_ocorrencias_abertas()


@router.get("/{ocorrencia_id}", response_model=OcorrenciaResponse)
def buscar_ocorrencia(ocorrencia_id: int):
    """Busca ocorrência por ID"""
    return OcorrenciaService.buscar_ocorrencia(ocorrencia_id)


@router.patch("/{ocorrencia_id}/status", response_model=OcorrenciaResponse)
def alterar_status_ocorrencia(ocorrencia_id: int, dados: AlterarStatusRequest):
    """Altera apenas o status de uma ocorrência"""
    return OcorrenciaService.alterar_status(ocorrencia_id, dados)


@router.put("/{ocorrencia_id}", response_model=OcorrenciaResponse)
def atualizar_ocorrencia(ocorrencia_id: int, dados: OcorrenciaUpdate):
    """Atualiza uma ocorrência"""
    return OcorrenciaService.atualizar_ocorrencia(ocorrencia_id, dados)


@router.post("/{ocorrencia_id}/fechar", response_model=OcorrenciaResponse)
def fechar_ocorrencia(ocorrencia_id: int, dados: FecharOcorrenciaRequest):
    """Fecha uma ocorrência"""
    return OcorrenciaService.fechar_ocorrencia(ocorrencia_id, dados)


@router.delete("/{ocorrencia_id}", status_code=status.HTTP_200_OK)
def deletar_ocorrencia(ocorrencia_id: int):
    """Deleta uma ocorrência"""
    return OcorrenciaService.deletar_ocorrencia(ocorrencia_id)
