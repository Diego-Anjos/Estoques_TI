"""
Router para endpoints de Itens
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.repositories.item_repo import ItemRepository
from app.repositories.local_repo import LocalRepository


router = APIRouter(prefix="/itens", tags=["Itens"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemCreate):
    """Cria um novo item"""
    local = LocalRepository.buscar_por_id(dados.id_local)
    if not local:
        raise HTTPException(status_code=400, detail="Local informado não existe")

    try:
        novo_id = ItemRepository.criar(dados.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível criar o item: {exc}") from exc

    item = ItemRepository.buscar_por_id(novo_id)
    return ItemResponse(**item)


@router.get("/", response_model=List[ItemResponse])
def listar_itens(tipo: Optional[str] = Query(None, description="Filtrar por tipo/categoria")):
    """Lista todos os itens (com nome do local)"""
    itens = ItemRepository.listar_todos(tipo)
    return [ItemResponse(**i) for i in itens]


@router.get("/{item_id}", response_model=ItemResponse)
def buscar_item(item_id: int):
    """Busca item por ID"""
    item = ItemRepository.buscar_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return ItemResponse(**item)


@router.put("/{item_id}", response_model=ItemResponse)
def atualizar_item(item_id: int, dados: ItemUpdate):
    """Atualiza um item"""
    existente = ItemRepository.buscar_por_id(item_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    dados_dict = dados.model_dump(exclude_unset=True)
    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    if 'id_local' in dados_dict:
        local = LocalRepository.buscar_por_id(dados_dict['id_local'])
        if not local:
            raise HTTPException(status_code=400, detail="Local informado não existe")

    try:
        sucesso = ItemRepository.atualizar(item_id, dados_dict)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível atualizar o item: {exc}") from exc

    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item = ItemRepository.buscar_por_id(item_id)
    return ItemResponse(**item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def deletar_item(item_id: int):
    """Deleta um item"""
    try:
        sucesso = ItemRepository.deletar(item_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível excluir o item (pode estar em uso): {exc}",
        ) from exc

    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"mensagem": "Item deletado com sucesso"}
