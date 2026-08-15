"""
Handlers globais de exceção da API.

Converte violações de integridade do banco (FK/unique) em HTTP 400 amigável,
evitando Erro 500 com detalhe técnico no frontend.
"""
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Mensagem padrão solicitada na fase de hardening
FK_DETAIL = (
    "Não é possível excluir este registro pois ele possui dependências "
    "vinculadas (Ex: Itens, Movimentações)"
)


def _is_integrity_violation(exc: BaseException) -> bool:
    """Detecta FK/unique do PostgreSQL via SQLAlchemy IntegrityError."""
    if isinstance(exc, IntegrityError):
        return True

    msg = str(exc).upper()
    return any(
        token in msg
        for token in (
            "FOREIGN KEY",
            "UNIQUE CONSTRAINT",
            "UNIQUE VIOLATION",
            "FOREIGN KEY VIOLATION",
            "NOT NULL VIOLATION",
            "INTEGRITY CONSTRAINT",
        )
    )


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


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    print(f"Erro de banco em {request.method} {request.url.path}: {exc}", flush=True)
    if _is_integrity_violation(exc):
        return JSONResponse(status_code=400, content={"detail": FK_DETAIL})
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno ao acessar o banco de dados."},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Rede de segurança: IntegrityError aninhado (ou re-raised) vira 400.
    Demais exceções seguem como 500 sem detalhe técnico.
    """
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
    app.add_exception_handler(IntegrityError, sqlalchemy_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
