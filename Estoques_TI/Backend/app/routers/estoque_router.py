"""
Router para endpoints de Estoque
"""
from fastapi import APIRouter, status
from typing import List
from pydantic import BaseModel, Field
from app.services.estoque_service import EstoqueService


router = APIRouter(prefix="/estoque", tags=["Estoque"])


class EstoqueCreate(BaseModel):
    item_id: int
    quantidade: int = 0
    quantidade_minima: int = 0
    localizacao: str = None


class EstoqueMovimentacao(BaseModel):
    item_id: int = Field(..., description="ID do item")
    quantidade: int = Field(..., gt=0, description="Quantidade a movimentar")


@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_estoque(dados: EstoqueCreate):
    """Cria um novo registro de estoque"""
    return EstoqueService.criar_estoque(
        item_id=dados.item_id,
        quantidade=dados.quantidade,
        quantidade_minima=dados.quantidade_minima,
        localizacao=dados.localizacao
    )


@router.get("/")
def listar_estoque():
    """Lista todo o estoque"""
    return EstoqueService.listar_estoque()


@router.get("/{estoque_id}")
def buscar_estoque(estoque_id: int):
    """Busca estoque por ID"""
    return EstoqueService.buscar_estoque(estoque_id)


@router.post("/entrada", status_code=status.HTTP_200_OK)
def entrada_estoque(dados: EstoqueMovimentacao):
    """Registra entrada de itens no estoque"""
    return EstoqueService.entrada_estoque(dados.item_id, dados.quantidade)


@router.post("/saida", status_code=status.HTTP_200_OK)
def saida_estoque(dados: EstoqueMovimentacao):
    """Registra saída de itens do estoque"""
    return EstoqueService.saida_estoque(dados.item_id, dados.quantidade)


@router.delete("/{estoque_id}", status_code=status.HTTP_200_OK)
def deletar_estoque(estoque_id: int):
    """Deleta um registro de estoque"""
    return EstoqueService.deletar_estoque(estoque_id)
