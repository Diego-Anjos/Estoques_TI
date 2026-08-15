"""
Inicializa o schema PostgreSQL (Supabase) do Sistema Estoques TI.

Usa SQLAlchemy Base.metadata.create_all(bind=engine).
Idempotente: cria apenas tabelas que ainda não existem.

Uso (na pasta Backend, com venv ativo):
    python init_db.py
"""
from __future__ import annotations

import sys

# Evita UnicodeEncodeError no console Windows (cp1252) com emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv

load_dotenv()

from app.core import database as db
from app.core.config import settings
from app.models.base import Base

# Importa todos os models para registrá-los no metadata do SQLAlchemy
from app.models.usuarios import Usuario  # noqa: F401
from app.models.locais import Local  # noqa: F401
from app.models.tipos_item import TipoItem  # noqa: F401
from app.models.itens import Item  # noqa: F401
from app.models.estoque_saldo import EstoqueSaldo  # noqa: F401
from app.models.estoque_movimentacoes import EstoqueMovimentacao  # noqa: F401
from app.models.patrimonios import Patrimonio  # noqa: F401
from app.models.patrimonio_atributos import PatrimonioAtributo  # noqa: F401
from app.models.softwares import Software  # noqa: F401
from app.models.software_licencas_pool import SoftwareLicencaPool  # noqa: F401
from app.models.software_atribuicoes import SoftwareAtribuicao  # noqa: F401
from app.models.ocorrencias import Ocorrencia  # noqa: F401
from app.models.configuracao import ConfiguracaoSistema  # noqa: F401


def main() -> None:
    print("=" * 60)
    print("  Inicialização do schema PostgreSQL (Estoques TI)")
    print("=" * 60)

    if not settings.database_configured:
        print("\n❌ DATABASE_URL não configurada.")
        print("   Defina no Backend/.env, por exemplo:")
        print(
            "   DATABASE_URL=postgresql://postgres:sua_senha@db.xxxx.supabase.co:5432/postgres"
        )
        sys.exit(1)

    # Oculta senha na URL ao exibir
    safe_url = settings.DATABASE_URL
    if "@" in safe_url:
        prefix, rest = safe_url.split("@", 1)
        if ":" in prefix:
            scheme_user = prefix.rsplit(":", 1)[0]
            safe_url = f"{scheme_user}:***@{rest}"

    print(f"\n📋 DATABASE_URL: {safe_url}\n")

    conn_error = db.init_db()
    if db.engine is None:
        print("❌ Não foi possível conectar ao PostgreSQL. Verifique DATABASE_URL.")
        if conn_error:
            print(f"   Detalhe: {conn_error}")
        print(
            "\nDicas:\n"
            "  - Confirme a senha do banco no Supabase (Settings → Database).\n"
            "  - Use ?sslmode=require no final da URL.\n"
            "  - Se a rede bloquear a porta 5432, use o Connection Pooler (porta 6543).\n"
        )
        sys.exit(1)

    print("📦 Criando tabelas via Base.metadata.create_all ...")
    Base.metadata.create_all(bind=db.engine)

    tabelas = sorted(Base.metadata.tables.keys())
    print(f"\n✅ Schema pronto. {len(tabelas)} tabela(s) registradas:")
    for nome in tabelas:
        print(f"   - {nome}")

    print("\nPronto. Você já pode iniciar a API:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")


if __name__ == "__main__":
    main()
