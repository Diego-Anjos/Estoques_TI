"""
Router para endpoints de Movimentações de Estoque
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from app.repositories.movimentacao_repo import MovimentacaoRepository


router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.post("/", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_movimentacao(dados: MovimentacaoCreate):
    """
    Registra entrada/saída em transação:
    - Insere movimentação
    - Atualiza quantidade do item
    - Retorna 400 se saída com saldo insuficiente
    """
    try:
        novo_id = MovimentacaoRepository.registrar(dados.model_dump())
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível registrar a movimentação: {exc}",
        ) from exc

    mov = MovimentacaoRepository.buscar_por_id(novo_id)
    if not mov:
        raise HTTPException(status_code=500, detail="Movimentação criada, mas não encontrada")
    return MovimentacaoResponse(**mov)


@router.get("/", response_model=List[MovimentacaoResponse])
def listar_movimentacoes():
    """Lista histórico de movimentações com nome do item"""
    return [MovimentacaoResponse(**m) for m in MovimentacaoRepository.listar_todas()]


@router.get("/{mov_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao(mov_id: int):
    """Busca movimentação por ID"""
    mov = MovimentacaoRepository.buscar_por_id(mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return MovimentacaoResponse(**mov)
