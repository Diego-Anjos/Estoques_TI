"""
Gerenciamento de conexão com Oracle Database usando pool de conexões
"""
import oracledb
from contextlib import contextmanager
from typing import Generator
from app.core.config import settings


# Pool de conexões global
_pool = None


def init_pool():
    """Inicializa o pool de conexões Oracle"""
    global _pool
    try:
        # Tenta inicializar em modo thick (com Oracle Client)
        # Se falhar, usa modo thin (sem Oracle Client)
        try:
            oracledb.init_oracle_client()
            print("ℹ️  Usando modo thick (Oracle Client)")
        except Exception as e:
            print(f"⚠️  Modo thick não disponível: {e}")
            print("ℹ️  Usando modo thin (sem Oracle Client)")
        
        _pool = oracledb.create_pool(
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            dsn=settings.ORACLE_DSN,
            min=settings.ORACLE_POOL_MIN,
            max=settings.ORACLE_POOL_MAX,
            increment=settings.ORACLE_POOL_INC
        )
        print(f"✅ Pool de conexões Oracle criado com sucesso!")
        print(f"   DSN: {settings.ORACLE_DSN}")
        print(f"   Pool: min={settings.ORACLE_POOL_MIN}, max={settings.ORACLE_POOL_MAX}")
    except Exception as e:
        print(f"❌ Erro ao criar pool de conexões Oracle: {e}")
        print(f"⚠️  A API iniciará, mas as operações de banco de dados falharão")
        print(f"   Verifique as configurações no arquivo .env")


def close_pool():
    """Fecha o pool de conexões Oracle"""
    global _pool
    if _pool:
        _pool.close()
        print("✅ Pool de conexões Oracle fechado")


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
        raise Exception("Pool de conexões não foi inicializado. Chame init_pool() primeiro.")
    
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
