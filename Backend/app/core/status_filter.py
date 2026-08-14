"""
Utilitário para filtro de status nas listagens (soft delete).

Valores aceitos no query param `status`:
  - ativos   (padrão): apenas registros ativos
  - inativos: apenas registros inativos
  - todos:   sem filtro de status
"""
from typing import Literal, Optional

StatusFiltro = Literal["ativos", "inativos", "todos"]
STATUS_FILTRO_VALUES = ("ativos", "inativos", "todos")


def normalizar_status_filtro(valor: Optional[str] = None) -> StatusFiltro:
    """Normaliza o query param; valores inválidos caem no padrão 'ativos'."""
    if not valor:
        return "ativos"
    normalizado = valor.strip().lower()
    if normalizado in STATUS_FILTRO_VALUES:
        return normalizado  # type: ignore[return-value]
    return "ativos"
