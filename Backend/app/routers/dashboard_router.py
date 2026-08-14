"""
Router de estatísticas do Dashboard
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.database import get_cursor
from app.core.deps import get_current_active_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_active_user)],
)


class DashboardStatsResponse(BaseModel):
    total_usuarios: int
    usuarios_ativos: int
    itens_cadastrados: int
    atividades_hoje: int


@router.get("/stats", response_model=DashboardStatsResponse)
def obter_estatisticas():
    """
    Retorna contadores rápidos para os cards do dashboard.
    """
    try:
        with get_cursor() as cursor:
            # Total alinhado à listagem (só ativos — soft delete não conta)
            cursor.execute(
                "SELECT COUNT(*) FROM ESTOQUES_TI_USUARIOS WHERE ATIVO = 'S'"
            )
            total_ativos = int(cursor.fetchone()[0])
            total_usuarios = total_ativos
            usuarios_ativos = total_ativos

            cursor.execute("SELECT COUNT(*) FROM ESTOQUES_TI_ITENS")
            itens_cadastrados = int(cursor.fetchone()[0])

            # Atividades do dia: movimentações + ocorrências abertas hoje
            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM ESTOQUES_TI_MOVIMENTACOES
                     WHERE TRUNC(DATA_CRIACAO) = TRUNC(SYSDATE))
                  + (SELECT COUNT(*) FROM ESTOQUES_TI_OCORRENCIAS
                     WHERE TRUNC(DATA_ABERTURA) = TRUNC(SYSDATE))
                FROM DUAL
                """
            )
            atividades_hoje = int(cursor.fetchone()[0])

        return DashboardStatsResponse(
            total_usuarios=total_usuarios,
            usuarios_ativos=usuarios_ativos,
            itens_cadastrados=itens_cadastrados,
            atividades_hoje=atividades_hoje,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estatísticas do dashboard: {exc}",
        ) from exc
