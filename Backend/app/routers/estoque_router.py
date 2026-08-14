"""
Router para endpoints de Estoque

Entrada/saída de saldo NÃO são feitas aqui — use POST /api/movimentacoes/.
As rotas legadas /entrada e /saida foram removidas na fase de hardening.
"""
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from app.services.estoque_service import EstoqueService
from app.core.deps import get_current_active_user


router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"],
    dependencies=[Depends(get_current_active_user)],
)


class EstoqueCreate(BaseModel):
    item_id: int
    quantidade: int = 0
    quantidade_minima: int = 0
    localizacao: str = None


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


@router.delete("/{estoque_id}", status_code=status.HTTP_200_OK)
def deletar_estoque(estoque_id: int):
    """Deleta um registro de estoque"""
    return EstoqueService.deletar_estoque(estoque_id)
