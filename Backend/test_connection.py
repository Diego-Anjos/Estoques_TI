"""
Script de teste de conexão com PostgreSQL (Supabase).
Uso (na pasta Backend):
    python test_connection.py
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import text

from app.core.config import settings
from app.core.database import init_db, engine


def main() -> int:
    print("=" * 60)
    print("  Teste de conexão PostgreSQL")
    print("=" * 60)

    if not settings.database_configured:
        print("❌ DATABASE_URL não configurada no .env")
        return 1

    safe = settings.DATABASE_URL
    if "@" in safe:
        prefix, rest = safe.split("@", 1)
        if ":" in prefix:
            safe = f"{prefix.rsplit(':', 1)[0]}:***@{rest}"
    print(f"\n📋 DATABASE_URL: {safe}\n")

    err = init_db()
    if engine is None:
        print("❌ Falha ao conectar.")
        if err:
            print(f"   Detalhe: {err}")
        return 1

    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar()
        current_user = conn.execute(text("SELECT current_user")).scalar()
        db_name = conn.execute(text("SELECT current_database()")).scalar()
        tables = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name LIKE 'estoques_ti_%'
                """
            )
        ).scalar()

    print(f"✅ Conectado como: {current_user}")
    print(f"✅ Database: {db_name}")
    print(f"✅ Tabelas estoques_ti_*: {tables}")
    print(f"📊 {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
