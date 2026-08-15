"""
Gerenciamento de conexão PostgreSQL via SQLAlchemy (Supabase / local).
"""
from __future__ import annotations

import logging
import re
from contextlib import contextmanager
from typing import Any, Generator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import normalize_database_url, settings
from app.models.base import Base

logger = logging.getLogger(__name__)

engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker[Session]] = None


def _build_engine(database_url: str) -> Engine:
    url = normalize_database_url(database_url)
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def init_db() -> None:
    """Inicializa o engine e a SessionLocal a partir de DATABASE_URL."""
    global engine, SessionLocal

    if not settings.database_configured:
        logger.warning(
            "DATABASE_URL não configurada. A API subirá, mas o banco ficará indisponível."
        )
        return

    try:
        engine = _build_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Smoke test
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexão PostgreSQL inicializada com sucesso.")
    except Exception as e:
        engine = None
        SessionLocal = None
        logger.warning(
            "Erro ao conectar no PostgreSQL: %s. "
            "A API iniciará, mas as operações de banco falharão até corrigir DATABASE_URL.",
            e,
        )
        return e  # devolve o erro para scripts (init_db.py)
    return None



# Alias legado (main.py / migrations)
def init_pool() -> None:
    init_db()


def close_pool() -> None:
    """Encerra o engine SQLAlchemy."""
    global engine, SessionLocal
    if engine is not None:
        try:
            engine.dispose()
            logger.info("Engine PostgreSQL encerrado.")
        except Exception as e:
            logger.warning("Erro ao encerrar engine: %s", e)
        finally:
            engine = None
            SessionLocal = None


def get_db() -> Generator[Session, None, None]:
    """
    Dependency FastAPI: yield de sessão SQLAlchemy.

    Uso:
        def rota(db: Session = Depends(get_db)):
            ...
            db.commit()
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Sessão de banco não inicializada. Configure DATABASE_URL e reinicie a API."
        )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_connection():
    """
    Context manager de conexão SQLAlchemy (commit/rollback).
    Mantido para scripts e repositórios que ainda usam SQL textual.
    """
    if engine is None:
        raise RuntimeError(
            "Engine não inicializado. Configure DATABASE_URL e reinicie a API."
        )

    conn = engine.connect()
    trans = conn.begin()
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()


class _OutVar:
    """Holder para valores de RETURNING (compatibilidade residual)."""

    def __init__(self) -> None:
        self._value: Any = None

    def setvalue(self, value: Any) -> None:
        self._value = value

    def getvalue(self) -> Any:
        return self._value


class PgCursorAdapter:
    """
    Adaptador de cursor para SQL textual com binds estilo :param.
    Também traduz resquícios Oracle → PostgreSQL (rede de segurança):
    - :param → %(param)s (psycopg2)
    - SYSTIMESTAMP / SYSDATE → NOW() / CURRENT_DATE
    - NVL( → COALESCE(
    - TRUNC(col) → (col)::date
    - Remove FROM DUAL
    - ROWNUM = 1 → LIMIT 1
    - RETURNING col INTO :id → RETURNING col
    """

    _bind_re = re.compile(r"(?<!:):([A-Za-z_][A-Za-z0-9_]*)")
    _returning_into_re = re.compile(
        r"RETURNING\s+([A-Za-z_][A-Za-z0-9_]*)\s+INTO\s+:([A-Za-z_][A-Za-z0-9_]*)",
        re.IGNORECASE,
    )
    _trunc_re = re.compile(r"TRUNC\s*\(\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\)", re.IGNORECASE)
    _rownum_re = re.compile(r"\bWHERE\s+ROWNUM\s*=\s*(\d+)\b", re.IGNORECASE)
    _rownum_and_re = re.compile(r"\bAND\s+ROWNUM\s*=\s*(\d+)\b", re.IGNORECASE)

    def __init__(self, raw_cursor) -> None:
        self._cursor = raw_cursor
        self.rowcount = 0

    def var(self, _typ=None) -> _OutVar:
        return _OutVar()

    def _translate_sql(self, sql: str) -> tuple[str, Optional[str]]:
        out_var_name: Optional[str] = None
        match = self._returning_into_re.search(sql)
        if match:
            out_var_name = match.group(2)
            sql = self._returning_into_re.sub(r"RETURNING \1", sql, count=1)

        sql = re.sub(r"\bSYSTIMESTAMP\b", "NOW()", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bSYSDATE\b", "CURRENT_DATE", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bNVL\s*\(", "COALESCE(", sql, flags=re.IGNORECASE)
        sql = self._trunc_re.sub(r"(\1)::date", sql)
        sql = re.sub(r"\s+FROM\s+DUAL\b", "", sql, flags=re.IGNORECASE)

        # ROWNUM = N → LIMIT N (casos simples)
        m_row = self._rownum_re.search(sql)
        if m_row:
            lim = m_row.group(1)
            sql = self._rownum_re.sub("", sql, count=1)
            sql = sql.rstrip().rstrip(";") + f" LIMIT {lim}"
        else:
            m_and = self._rownum_and_re.search(sql)
            if m_and:
                lim = m_and.group(1)
                sql = self._rownum_and_re.sub("", sql, count=1)
                sql = sql.rstrip().rstrip(";") + f" LIMIT {lim}"

        sql = self._bind_re.sub(r"%(\1)s", sql)
        return sql, out_var_name

    def execute(self, sql: str, params: Optional[dict] = None):
        params = dict(params or {})
        out_vars = {k: v for k, v in params.items() if isinstance(v, _OutVar)}
        bind_params = {k: v for k, v in params.items() if not isinstance(v, _OutVar)}

        sql_pg, out_var_name = self._translate_sql(sql)
        self._cursor.execute(sql_pg, bind_params)
        self.rowcount = self._cursor.rowcount

        if out_var_name and out_var_name in out_vars:
            row = self._cursor.fetchone()
            out_vars[out_var_name].setvalue([row[0]] if row else [None])

        return self

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self) -> None:
        self._cursor.close()


@contextmanager
def get_cursor() -> Generator[PgCursorAdapter, None, None]:
    """
    Context manager de cursor (compatível com repositórios existentes).
    Usa conexão bruta do pool SQLAlchemy (psycopg2).
    """
    if engine is None:
        raise RuntimeError(
            "Engine não inicializado. Configure DATABASE_URL e reinicie a API."
        )

    raw = engine.raw_connection()
    cursor = raw.cursor()
    adapter = PgCursorAdapter(cursor)
    try:
        yield adapter
        raw.commit()
    except Exception:
        raw.rollback()
        raise
    finally:
        adapter.close()
        raw.close()


def execute_select(query: str, params: dict = None):
    """Helper SELECT — retorna lista de tuplas."""
    with get_cursor() as cursor:
        cursor.execute(query, params or {})
        return cursor.fetchall()


def execute_dml(query: str, params: dict = None) -> int:
    """Helper INSERT/UPDATE/DELETE com commit automático."""
    with get_cursor() as cursor:
        cursor.execute(query, params or {})
        return cursor.rowcount


# Re-export da Base para imports centralizados
__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "init_db",
    "init_pool",
    "close_pool",
    "get_db",
    "get_connection",
    "get_cursor",
    "execute_select",
    "execute_dml",
]
