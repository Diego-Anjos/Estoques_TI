"""
Router para endpoints de Locais
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.local import LocalCreate, LocalUpdate, LocalResponse
from app.repositories.local_repo import LocalRepository


router = APIRouter(prefix="/locais", tags=["Locais"])


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
def listar_locais():
    """Lista todos os locais"""
    locais = LocalRepository.listar_todos()
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
def deletar_local(local_id: int):
    """Deleta um local"""
    sucesso = LocalRepository.deletar(local_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return {"mensagem": "Local deletado com sucesso"}
