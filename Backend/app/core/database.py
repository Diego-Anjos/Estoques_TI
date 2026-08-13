"""
Gerenciamento de conexão com Oracle Database usando pool de conexões
"""
import logging
from contextlib import contextmanager
from typing import Generator

import oracledb

from app.core.config import settings

logger = logging.getLogger(__name__)

# Pool de conexões global
_pool = None


def init_pool():
    """Inicializa o pool de conexões Oracle"""
    global _pool

    if not settings.oracle_configured:
        logger.warning(
            "Pool Oracle não inicializado: defina ORACLE_USER, ORACLE_PASSWORD "
            "e ORACLE_DSN nas variáveis de ambiente. A API continuará no ar."
        )
        return

    try:
        # Tenta inicializar em modo thick (com Oracle Client)
        # Se falhar, usa modo thin (sem Oracle Client)
        try:
            oracledb.init_oracle_client()
            logger.info("Usando modo thick (Oracle Client)")
        except Exception as e:
            logger.warning("Modo thick não disponível: %s", e)
            logger.info("Usando modo thin (sem Oracle Client)")

        _pool = oracledb.create_pool(
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            dsn=settings.ORACLE_DSN,
            min=settings.ORACLE_POOL_MIN,
            max=settings.ORACLE_POOL_MAX,
            increment=settings.ORACLE_POOL_INC,
        )
        logger.info(
            "Pool de conexões Oracle criado (DSN=%s, min=%s, max=%s)",
            settings.ORACLE_DSN,
            settings.ORACLE_POOL_MIN,
            settings.ORACLE_POOL_MAX,
        )
    except Exception as e:
        _pool = None
        logger.warning(
            "Erro ao criar pool de conexões Oracle: %s. "
            "A API iniciará, mas as operações de banco falharão até corrigir "
            "as variáveis de ambiente.",
            e,
        )


def close_pool():
    """Fecha o pool de conexões Oracle"""
    global _pool
    if _pool:
        try:
            _pool.close()
            logger.info("Pool de conexões Oracle fechado")
        except Exception as e:
            logger.warning("Erro ao fechar pool Oracle: %s", e)
        finally:
            _pool = None


@contextmanager
def get_connection() -> Generator[oracledb.Connection, None, None]:
    """
    Context manager para obter uma conexão do pool

    Uso:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USUARIOS")
    """
    if not _pool:
        raise Exception(
            "Pool de conexões não foi inicializado. "
            "Configure ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN e reinicie a API."
        )

    conn = _pool.acquire()
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_cursor() -> Generator[oracledb.Cursor, None, None]:
    """
    Context manager para obter um cursor diretamente

    Uso:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM USUARIOS")
            rows = cursor.fetchall()
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


def execute_select(query: str, params: dict = None):
    """
    Helper para executar SELECT e retornar resultados

    Args:
        query: Query SQL SELECT
        params: Parâmetros da query

    Returns:
        Lista de tuplas com os resultados

    Uso:
        rows = execute_select("SELECT * FROM USUARIOS WHERE ID = :id", {"id": 1})
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or {})
        return cursor.fetchall()


def execute_dml(query: str, params: dict = None) -> int:
    """
    Helper para executar INSERT/UPDATE/DELETE com commit automático

    Args:
        query: Query SQL DML (INSERT, UPDATE, DELETE)
        params: Parâmetros da query

    Returns:
        Número de linhas afetadas

    Uso:
        rowcount = execute_dml("UPDATE USUARIOS SET NOME = :nome WHERE ID = :id",
                               {"nome": "João", "id": 1})
    """
    with get_cursor() as cursor:
        cursor.execute(query, params or {})
        return cursor.rowcount
