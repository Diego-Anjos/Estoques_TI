"""
Router para endpoints de Tipos de Item
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.tipo_item import TipoItemCreate, TipoItemUpdate, TipoItemResponse
from app.repositories.tipo_item_repo import TipoItemRepository


router = APIRouter(prefix="/tipos-item", tags=["Tipos de Item"])


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
def listar_tipos_item():
    """Lista todos os tipos de item"""
    tipos = TipoItemRepository.listar_todos()
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
def deletar_tipo_item(tipo_id: int):
    """Deleta um tipo de item"""
    try:
        sucesso = TipoItemRepository.deletar(tipo_id)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível excluir o tipo (pode estar em uso): {exc}",
        ) from exc

    if not sucesso:
        raise HTTPException(status_code=404, detail="Tipo de item não encontrado")
    return {"mensagem": "Tipo de item deletado com sucesso"}
