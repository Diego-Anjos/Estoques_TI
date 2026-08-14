"""
Handlers globais de exceção da API.

Converte violações de integridade do banco (FK/unique) em HTTP 400 amigável,
evitando Erro 500 com stack/Oracle cru no frontend.
"""
from __future__ import annotations

import re
from typing import Optional

import oracledb
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Mensagem padrão solicitada na fase de hardening
FK_DETAIL = (
    "Não é possível excluir este registro pois ele possui dependências "
    "vinculadas (Ex: Itens, Movimentações)"
)

# ORA-02292: child record found | ORA-02291: parent key not found | ORA-00001: unique
_INTEGRITY_ORA_CODES = {1, 2291, 2292}
_ORA_CODE_RE = re.compile(r"ORA-0*(\d+)", re.IGNORECASE)


def _oracle_error_code(exc: BaseException) -> Optional[int]:
    """Extrai o código Oracle (ex.: 2292) de DatabaseError / args."""
    error_obj = getattr(exc, "args", [None])[0] if getattr(exc, "args", None) else None
    code = getattr(error_obj, "code", None)
    if isinstance(code, int):
        return code

    match = _ORA_CODE_RE.search(str(exc))
    if match:
        return int(match.group(1))
    return None


def _is_integrity_violation(exc: BaseException) -> bool:
    """Detecta FK/unique do Oracle e IntegrityError do SQLAlchemy (se presente)."""
    try:
        from sqlalchemy.exc import IntegrityError as SAIntegrityError  # type: ignore

        if isinstance(exc, SAIntegrityError):
            return True
    except ImportError:
        pass

    if isinstance(exc, oracledb.IntegrityError):
        return True

    if isinstance(exc, oracledb.DatabaseError):
        code = _oracle_error_code(exc)
        if code in _INTEGRITY_ORA_CODES:
            return True
        msg = str(exc).upper()
        if any(
            token in msg
            for token in (
                "INTEGRITY CONSTRAINT",
                "CHILD RECORD FOUND",
                "PARENT KEY NOT FOUND",
                "UNIQUE CONSTRAINT",
            )
        ):
            return True

    return False


def _walk_exception_chain(exc: BaseException):
    seen: set[int] = set()
    current: Optional[BaseException] = exc
    while current is not None and id(current) not in seen:
        yield current
        seen.add(id(current))
        current = current.__cause__ or current.__context__


def _find_integrity_exc(exc: BaseException) -> Optional[BaseException]:
    for candidate in _walk_exception_chain(exc):
        if _is_integrity_violation(candidate):
            return candidate
    return None


async def oracle_database_error_handler(request: Request, exc: oracledb.DatabaseError):
    # Sempre loga o erro real no terminal (o cliente recebe mensagem genérica)
    print(f"Erro Oracle em {request.method} {request.url.path}: {exc}", flush=True)
    if _is_integrity_violation(exc):
        return JSONResponse(status_code=400, content={"detail": FK_DETAIL})
    # Outros erros de banco: 500 genérico (sem vazar SQL/ORA ao cliente)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno ao acessar o banco de dados."},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Rede de segurança: IntegrityError aninhado (ou re-raised) vira 400.
    Demais exceções seguem como 500 sem detalhe técnico.
    """
    # Não interferir em HTTPException (handler específico do FastAPI/Starlette)
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )

    if _find_integrity_exc(exc):
        return JSONResponse(status_code=400, content={"detail": FK_DETAIL})

    print(f"Erro não tratado em {request.method} {request.url.path}: {exc}", flush=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor."},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registra os handlers na instância FastAPI."""
    app.add_exception_handler(oracledb.IntegrityError, oracle_database_error_handler)
    app.add_exception_handler(oracledb.DatabaseError, oracle_database_error_handler)
    # Opcional: SQLAlchemy IntegrityError (projeto usa oracledb puro, mas cobre dual-use)
    try:
        from sqlalchemy.exc import IntegrityError as SAIntegrityError  # type: ignore

        async def sa_integrity_handler(request: Request, exc: SAIntegrityError):
            return JSONResponse(status_code=400, content={"detail": FK_DETAIL})

        app.add_exception_handler(SAIntegrityError, sa_integrity_handler)
    except ImportError:
        pass

    app.add_exception_handler(Exception, unhandled_exception_handler)
