"""
Aplicação principal FastAPI - Sistema de Gestão de TI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_pool, close_pool
from app.routers import (
    usuario_router,
    item_router,
    estoque_router,
    patrimonio_router,
    software_router,
    ocorrencia_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
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
    - ✅ Conexão com Oracle Database
    """,
    lifespan=lifespan
)


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
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
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
