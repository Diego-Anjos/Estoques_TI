"""
Router para endpoints de Locais
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.local import LocalCreate, LocalUpdate, LocalResponse
from app.repositories.local_repo import LocalRepository
from app.core.deps import get_current_active_user
from app.core.status_filter import normalizar_status_filtro


router = APIRouter(
    prefix="/locais",
    tags=["Locais"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=LocalResponse, status_code=status.HTTP_201_CREATED)
def criar_local(dados: LocalCreate):
    """Cria um novo local"""
    existente = LocalRepository.buscar_por_nome(dados.nome)
    if existente:
        raise HTTPException(status_code=400, detail="Já existe um local com este nome")

    dados_dict = dados.model_dump()
    novo_id = LocalRepository.criar(dados_dict)
    local = LocalRepository.buscar_por_id(novo_id)
    return LocalResponse(**local)


@router.get("/", response_model=List[LocalResponse])
def listar_locais(
    status_filtro: Optional[str] = Query(
        None,
        alias="status",
        description="Filtro de status: ativos (padrão), inativos ou todos",
    ),
):
    """
    Lista locais.
    Padrão: apenas Ativos — usado pela tabela principal e pelos dropdowns
    (Cadastro de Itens / Movimentações).
    """
    locais = LocalRepository.listar_todos(status_filtro=normalizar_status_filtro(status_filtro))
    return [LocalResponse(**l) for l in locais]


@router.get("/{local_id}", response_model=LocalResponse)
def buscar_local(local_id: int):
    """Busca local por ID"""
    local = LocalRepository.buscar_por_id(local_id)
    if not local:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return LocalResponse(**local)


@router.put("/{local_id}", response_model=LocalResponse)
def atualizar_local(local_id: int, dados: LocalUpdate):
    """Atualiza um local"""
    existente = LocalRepository.buscar_por_id(local_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    dados_dict = dados.model_dump(exclude_unset=True)
    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    if 'nome' in dados_dict:
        outro = LocalRepository.buscar_por_nome(dados_dict['nome'])
        if outro and outro['id_local'] != local_id:
            raise HTTPException(status_code=400, detail="Já existe um local com este nome")

    sucesso = LocalRepository.atualizar(local_id, dados_dict)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    local = LocalRepository.buscar_por_id(local_id)
    return LocalResponse(**local)


@router.delete("/{local_id}", status_code=status.HTTP_200_OK)
def inativar_local(local_id: int):
    """
    Inativa um local (soft-delete).
    Locais com dependências (itens, movimentações) não podem ser apagados;
    a regra de negócio é apenas marcar STATUS = 'Inativo'.
    """
    existente = LocalRepository.buscar_por_id(local_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    if (existente.get("status") or "").lower() == "inativo":
        return {"mensagem": "Local já está inativo"}

    sucesso = LocalRepository.inativar(local_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    return {"mensagem": "Local inativado com sucesso"}
