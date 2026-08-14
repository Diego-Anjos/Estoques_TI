"""
Router para exportação de dados em CSV
"""
import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.core.database import get_cursor
from app.core.deps import get_current_active_user


router = APIRouter(
    prefix="/exportar",
    tags=["Exportação"],
    dependencies=[Depends(get_current_active_user)],
)


def _csv_response(filename: str, headers: list[str], rows: list[list]) -> StreamingResponse:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';', lineterminator='\n')
    writer.writerow(headers)
    writer.writerows(rows)
    # BOM para Excel abrir UTF-8 corretamente
    content = '\ufeff' + buffer.getvalue()

    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@router.get("/itens")
def exportar_itens():
    """Exporta inventário (itens) em CSV"""
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT i.ID_ITEM, i.NOME, i.TIPO, i.DESCRICAO, i.QUANTIDADE,
                       i.UNIDADE, i.STATUS, l.NOME AS NOME_LOCAL
                FROM ESTOQUES_TI_ITENS i
                LEFT JOIN ESTOQUES_TI_LOCAIS l ON l.ID_LOCAL = i.ID_LOCAL
                ORDER BY i.NOME
                """
            )
            rows = [
                [
                    r[0],
                    r[1] or '',
                    r[2] or '',
                    r[3] or '',
                    int(r[4] or 0),
                    r[5] or 'UN',
                    r[6] or '',
                    r[7] or '',
                ]
                for r in cursor.fetchall()
            ]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar itens: {exc}") from exc

    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return _csv_response(
        f"inventario_{stamp}.csv",
        ["ID", "Nome", "Tipo", "Descricao", "Quantidade", "Unidade", "Status", "Local"],
        rows,
    )


@router.get("/movimentacoes")
def exportar_movimentacoes():
    """Exporta histórico de movimentações em CSV"""
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT m.ID_MOVIMENTACAO, m.DATA_CRIACAO, i.NOME, m.TIPO_MOVIMENTACAO,
                       m.QUANTIDADE, m.SETOR_DESTINO, m.MOTIVO
                FROM ESTOQUES_TI_MOVIMENTACOES m
                JOIN ESTOQUES_TI_ITENS i ON i.ID_ITEM = m.ID_ITEM
                ORDER BY m.DATA_CRIACAO DESC, m.ID_MOVIMENTACAO DESC
                """
            )
            rows = []
            for r in cursor.fetchall():
                data = r[1]
                data_str = data.isoformat(sep=' ', timespec='seconds') if data else ''
                rows.append([
                    r[0],
                    data_str,
                    r[2] or '',
                    r[3] or '',
                    int(r[4] or 0),
                    r[5] or '',
                    r[6] or '',
                ])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar movimentações: {exc}") from exc

    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return _csv_response(
        f"movimentacoes_{stamp}.csv",
        ["ID", "Data", "Item", "Tipo", "Quantidade", "Setor Destino", "Observacao"],
        rows,
    )
