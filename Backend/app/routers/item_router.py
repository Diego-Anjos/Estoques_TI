"""
Router para endpoints de Itens
"""
from fastapi import APIRouter, status, Query
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.repositories.item_repo import ItemRepository


router = APIRouter(prefix="/itens", tags=["Itens"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemCreate):
    """Cria um novo item"""
    dados_dict = dados.model_dump()
    novo_id = ItemRepository.criar(dados_dict)
    item = ItemRepository.buscar_por_id(novo_id)
    return ItemResponse(**item)


@router.get("/", response_model=List[ItemResponse])
def listar_itens(tipo: Optional[str] = Query(None, description="Filtrar por tipo: ESTOQUE ou PATRIMONIO")):
    """Lista todos os itens, opcionalmente filtrados por tipo"""
    itens = ItemRepository.listar_todos(tipo)
    return [ItemResponse(**i) for i in itens]


@router.get("/{item_id}", response_model=ItemResponse)
def buscar_item(item_id: int):
    """Busca item por ID"""
    from fastapi import HTTPException
    item = ItemRepository.buscar_por_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return ItemResponse(**item)


@router.put("/{item_id}", response_model=ItemResponse)
def atualizar_item(item_id: int, dados: ItemUpdate):
    """Atualiza um item"""
    from fastapi import HTTPException
    dados_dict = dados.model_dump(exclude_unset=True)
    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
    
    sucesso = ItemRepository.atualizar(item_id, dados_dict)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    item = ItemRepository.buscar_por_id(item_id)
    return ItemResponse(**item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def deletar_item(item_id: int):
    """Deleta um item"""
    from fastapi import HTTPException
    sucesso = ItemRepository.deletar(item_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"mensagem": "Item deletado com sucesso"}
