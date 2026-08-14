"""
Router para endpoints de Movimentações de Estoque
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from app.schemas.movimentacao import (
    MovimentacaoCreate,
    MovimentacaoResponse,
    normalizar_tipo_movimentacao,
)
from app.repositories.movimentacao_repo import MovimentacaoRepository
from app.core.deps import get_current_active_user


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_movimentacao(dados: MovimentacaoCreate):
    """
    Registra entrada/saída/devolução em transação:
    - Insere movimentação
    - Atualiza quantidade do item (ENTRADA e DEVOLUCAO somam; SAIDA subtrai)
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
def listar_movimentacoes(
    tipo: Optional[str] = Query(
        None,
        description=(
            "Filtra por tipo. Aceita Entrada/Saída/Devolução, "
            "ENTRADA/SAIDA/DEVOLUCAO ou E/S/D"
        ),
    ),
    item: Optional[str] = Query(None, description="Filtro parcial pelo nome do item"),
):
    """Lista histórico de movimentações com nome do item"""
    tipo_normalizado = None
    if tipo and tipo.strip():
        try:
            tipo_normalizado = normalizar_tipo_movimentacao(tipo)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    movimentacoes = MovimentacaoRepository.listar_todas(
        tipo=tipo_normalizado,
        nome_item=item,
    )
    return [MovimentacaoResponse(**m) for m in movimentacoes]


@router.get("/{mov_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao(mov_id: int):
    """Busca movimentação por ID"""
    mov = MovimentacaoRepository.buscar_por_id(mov_id)
    if not mov:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return MovimentacaoResponse(**mov)
