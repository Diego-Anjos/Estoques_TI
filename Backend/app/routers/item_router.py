"""
Router para endpoints de Itens
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.repositories.item_repo import ItemRepository
from app.repositories.local_repo import LocalRepository
from app.repositories.tipo_item_repo import TipoItemRepository
from app.core.deps import get_current_active_user
from app.core.status_filter import normalizar_status_filtro


router = APIRouter(
    prefix="/itens",
    tags=["Itens"],
    dependencies=[Depends(get_current_active_user)],
)


def _validar_tipo_item(id_tipo_item: int, exigir_ativo: bool = True) -> dict:
    tipo = TipoItemRepository.buscar_por_id(id_tipo_item)
    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo de item informado não existe")
    if exigir_ativo and (tipo.get("status") or "").lower() != "ativo":
        raise HTTPException(
            status_code=400,
            detail="Não é possível vincular o item a um tipo inativo",
        )
    return tipo


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemCreate):
    """Cria um novo item"""
    local = LocalRepository.buscar_por_id(dados.id_local)
    if not local:
        raise HTTPException(status_code=400, detail="Local informado não existe")
    if (local.get("status") or "").lower() != "ativo":
        raise HTTPException(
            status_code=400,
            detail="Não é possível vincular o item a um local inativo",
        )

    _validar_tipo_item(dados.id_tipo_item, exigir_ativo=True)

    try:
        novo_id = ItemRepository.criar(dados.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível criar o item: {exc}") from exc

    item = ItemRepository.buscar_por_id(novo_id)
    return ItemResponse(**item)


@router.get("/", response_model=List[ItemResponse])
def listar_itens(
    tipo: Optional[str] = Query(None, description="Filtrar pelo nome do tipo/categoria"),
    id_tipo_item: Optional[int] = Query(None, description="Filtrar pelo ID do tipo/categoria"),
    status_filtro: Optional[str] = Query(
        None,
        alias="status",
        description="Filtro de status: ativos (padrão), inativos ou todos",
    ),
):
    """Lista itens (com nome do local e do tipo). Por padrão retorna apenas Ativos."""
    itens = ItemRepository.listar_todos(
        tipo=tipo,
        id_tipo_item=id_tipo_item,
        status_filtro=normalizar_status_filtro(status_filtro),
    )
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
    """Atualiza um item (quantidade é read-only — use /movimentacoes/)."""
    existente = ItemRepository.buscar_por_id(item_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    dados_dict = dados.model_dump(exclude_unset=True)
    # Blindagem: nunca permitir alteração direta de saldo via PUT
    dados_dict.pop("quantidade", None)
    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    if 'id_local' in dados_dict:
        local = LocalRepository.buscar_por_id(dados_dict['id_local'])
        if not local:
            raise HTTPException(status_code=400, detail="Local informado não existe")
        # Só exige local ativo ao mudar o vínculo (reativação pode manter o local atual)
        id_local_atual = existente.get("id_local")
        mudou_local = int(dados_dict["id_local"]) != int(id_local_atual or 0)
        if mudou_local and (local.get("status") or "").lower() != "ativo":
            raise HTTPException(
                status_code=400,
                detail="Não é possível vincular o item a um local inativo",
            )

    if 'id_tipo_item' in dados_dict:
        id_tipo_atual = existente.get("id_tipo_item")
        mudou_tipo = int(dados_dict["id_tipo_item"]) != int(id_tipo_atual or 0)
        _validar_tipo_item(dados_dict["id_tipo_item"], exigir_ativo=mudou_tipo)

    try:
        sucesso = ItemRepository.atualizar(item_id, dados_dict)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível atualizar o item: {exc}") from exc

    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item = ItemRepository.buscar_por_id(item_id)
    return ItemResponse(**item)


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def inativar_item(item_id: int):
    """Inativa um item (soft-delete)."""
    existente = ItemRepository.buscar_por_id(item_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    if (existente.get("status") or "").lower() == "inativo":
        return {"mensagem": "Item já está inativo"}

    sucesso = ItemRepository.inativar(item_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return {"mensagem": "Item inativado com sucesso"}
