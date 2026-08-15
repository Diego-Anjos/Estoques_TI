"""
Aplicação principal FastAPI - Sistema de Gestão de TI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings, validate_jwt_secret_key
from app.core.database import init_pool, close_pool
from app.core.exception_handlers import register_exception_handlers
from app.routers import (
    usuario_router,
    item_router,
    estoque_router,
    patrimonio_router,
    software_router,
    ocorrencia_router,
    dashboard_router,
    local_router,
    tipo_item_router,
    movimentacao_router,
    configuracao_router,
    exportacao_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup — revalida JWT (falha clara no terminal se .env estiver errado)
    try:
        validate_jwt_secret_key(settings.JWT_SECRET_KEY)
    except ValueError as exc:
        print(str(exc), flush=True)
        raise RuntimeError(str(exc)) from exc

    print("🚀 Iniciando aplicação...")
    init_pool()
    yield
    # Shutdown
    print("🛑 Encerrando aplicação...")
    close_pool()


# Cria aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="""
    ## Sistema de Gestão de TI
    
    API REST para gerenciamento de:
    - 📦 **Estoque** - Controle de itens por quantidade
    - 🖥️ **Patrimônio** - Itens serializados (PC, Monitor, etc)
    - 💿 **Software/Licenças** - Controle de licenças
    - 📋 **Ocorrências** - Sistema de chamados
    - 👥 **Usuários** - Autenticação e controle de acesso
    
    ### Recursos
    - ✅ Auditoria completa (criado/alterado por)
    - ✅ Validações de negócio
    - ✅ Conexão com PostgreSQL (Supabase)
    """,
    lifespan=lifespan
)

# FK / IntegrityError → HTTP 400 amigável (em vez de 500)
register_exception_handlers(app)


# Configuração CORS — liberado para desenvolvimento local e Vercel (produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite local
        "http://localhost:5174",  # Vite (porta alternativa)
        "http://localhost:3000",  # React / serve alternativo
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        "*",  # Libera qualquer subdomínio da Vercel e origens externas em produção
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registra routers
app.include_router(usuario_router.router, prefix=settings.API_PREFIX)
app.include_router(item_router.router, prefix=settings.API_PREFIX)
app.include_router(estoque_router.router, prefix=settings.API_PREFIX)
app.include_router(patrimonio_router.router, prefix=settings.API_PREFIX)
app.include_router(software_router.router, prefix=settings.API_PREFIX)
app.include_router(ocorrencia_router.router, prefix=settings.API_PREFIX)
app.include_router(dashboard_router.router, prefix=settings.API_PREFIX)
app.include_router(local_router.router, prefix=settings.API_PREFIX)
app.include_router(tipo_item_router.router, prefix=settings.API_PREFIX)
app.include_router(movimentacao_router.router, prefix=settings.API_PREFIX)
app.include_router(configuracao_router.router, prefix=settings.API_PREFIX)
app.include_router(exportacao_router.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "mensagem": "🚀 API de Gestão de TI",
        "versao": settings.API_VERSION,
        "documentacao": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Verifica saúde da aplicação"""
    return {
        "status": "healthy",
        "api": settings.API_TITLE,
        "versao": settings.API_VERSION
    }


if __name__ == "__main__":
    import os
    import uvicorn

    # Render (e outros PaaS) injetam PORT dinamicamente
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.environ.get("ENV", "development") == "development",
    )