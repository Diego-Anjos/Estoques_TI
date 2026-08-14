"""
Router para endpoints de Tipos de Item
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.tipo_item import TipoItemCreate, TipoItemUpdate, TipoItemResponse
from app.repositories.tipo_item_repo import TipoItemRepository
from app.core.deps import get_current_active_user
from app.core.status_filter import normalizar_status_filtro


router = APIRouter(
    prefix="/tipos-item",
    tags=["Tipos de Item"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=TipoItemResponse, status_code=status.HTTP_201_CREATED)
def criar_tipo_item(dados: TipoItemCreate):
    """Cria um novo tipo de item"""
    existente = TipoItemRepository.buscar_por_nome(dados.nome)
    if existente:
        raise HTTPException(status_code=400, detail="Já existe um tipo com este nome")

    try:
        novo_id = TipoItemRepository.criar(dados.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Não foi possível criar o tipo: {exc}") from exc

    tipo = TipoItemRepository.buscar_por_id(novo_id)
    return TipoItemResponse(**tipo)


@router.get("/", response_model=List[TipoItemResponse])
def listar_tipos_item(
    status_filtro: Optional[str] = Query(
        None,
        alias="status",
        description="Filtro de status: ativos (padrão), inativos ou todos",
    ),
):
    """Lista tipos de item. Por padrão retorna apenas Ativos."""
    tipos = TipoItemRepository.listar_todos(status_filtro=normalizar_status_filtro(status_filtro))
    return [TipoItemResponse(**t) for t in tipos]


@router.get("/{tipo_id}", response_model=TipoItemResponse)
def buscar_tipo_item(tipo_id: int):
    """Busca tipo de item por ID"""
    tipo = TipoItemRepository.buscar_por_id(tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")
    return TipoItemResponse(**tipo)


@router.put("/{tipo_id}", response_model=TipoItemResponse)
def atualizar_tipo_item(tipo_id: int, dados: TipoItemUpdate):
    """Atualiza um tipo de item"""
    existente = TipoItemRepository.buscar_por_id(tipo_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")

    dados_dict = dados.model_dump(exclude_unset=True)
    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    if 'nome' in dados_dict:
        outro = TipoItemRepository.buscar_por_nome(dados_dict['nome'])
        if outro and outro['id_tipo_item'] != tipo_id:
            raise HTTPException(status_code=400, detail="Já existe um tipo com este nome")

    sucesso = TipoItemRepository.atualizar(tipo_id, dados_dict)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")

    tipo = TipoItemRepository.buscar_por_id(tipo_id)
    return TipoItemResponse(**tipo)


@router.delete("/{tipo_id}", status_code=status.HTTP_200_OK)
def inativar_tipo_item(tipo_id: int):
    """Inativa um tipo de item (soft-delete)."""
    existente = TipoItemRepository.buscar_por_id(tipo_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")

    if (existente.get("status") or "").lower() == "inativo":
        return {"mensagem": "Tipo de item já está inativo"}

    sucesso = TipoItemRepository.inativar(tipo_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")

    return {"mensagem": "Tipo de item inativado com sucesso"}
