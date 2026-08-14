"""
Router para Configurações do Sistema
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.configuracao import ConfiguracaoResponse, ConfiguracaoUpdate
from app.repositories.configuracao_repo import ConfiguracaoRepository
from app.core.deps import get_current_active_user


router = APIRouter(
    prefix="/configuracoes",
    tags=["Configurações"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/", response_model=ConfiguracaoResponse)
def obter_configuracoes():
    """Retorna as configurações globais (singleton ID=1)"""
    try:
        cfg = ConfiguracaoRepository.obter()
        return ConfiguracaoResponse(**cfg)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar configurações: {exc}") from exc


@router.put("/", response_model=ConfiguracaoResponse)
def atualizar_configuracoes(dados: ConfiguracaoUpdate):
    """Atualiza as configurações globais"""
    payload = dados.model_dump(exclude_unset=True)
    if not payload:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    try:
        cfg = ConfiguracaoRepository.atualizar(payload)
        return ConfiguracaoResponse(**cfg)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Erro ao salvar configurações: {exc}") from exc
