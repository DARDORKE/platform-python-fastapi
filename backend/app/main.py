"""
Main FastAPI application module.
"""
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import engine
from app.core.redis import redis_client
from app.models.base import Base

# Métriques Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
REQUEST_IN_PROGRESS = Counter('http_requests_in_progress', 'HTTP requests currently in progress')


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware pour collecter les métriques Prometheus."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        REQUEST_IN_PROGRESS.inc()
        
        try:
            response = await call_next(request)
            
            # Collecter les métriques
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            REQUEST_DURATION.observe(time.time() - start_time)
            
            return response
        except Exception as e:
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            raise
        finally:
            REQUEST_IN_PROGRESS.dec()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Gestionnaire de cycle de vie de l'application."""
    # Startup
    print("🚀 Démarrage de l'application Platform...")
    
    # Créer les tables si elles n'existent pas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Vérifier la connexion Redis
    try:
        await redis_client.ping()
        print("✅ Connexion Redis établie")
    except Exception as e:
        print(f"❌ Erreur de connexion Redis: {e}")
    
    print("✅ Application démarrée avec succès!")
    
    yield
    
    # Shutdown
    print("🔄 Arrêt de l'application...")
    await redis_client.close()
    await engine.dispose()
    print("✅ Application arrêtée proprement")


def create_application() -> FastAPI:
    """Créer et configurer l'application FastAPI."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="""
        ## Plateforme de Gestion Python

        Une API moderne et performante pour la gestion d'entreprise.

        ### Fonctionnalités principales:
        - 🔐 Authentification JWT sécurisée
        - 👥 Gestion des utilisateurs et équipes
        - 📊 Tableaux de bord et analytics
        - 🔄 Tâches asynchrones avec Celery
        - 📈 Monitoring avec Prometheus
        - 🚀 Performance optimisée avec Redis

        ### Technologies:
        - **FastAPI** - Framework web moderne
        - **SQLAlchemy** - ORM Python
        - **PostgreSQL** - Base de données
        - **Redis** - Cache et sessions
        - **Celery** - Tâches asynchrones
        """,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(PrometheusMiddleware)
    
    # Routes
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app


# Créer l'instance de l'application
app = create_application()


@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé."""
    try:
        # Vérifier la base de données
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        
        # Vérifier Redis
        await redis_client.ping()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.VERSION,
            "database": "connected",
            "redis": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": time.time(),
                "error": str(e)
            }
        )


@app.get("/metrics")
async def metrics():
    """Endpoint pour les métriques Prometheus."""
    return Response(generate_latest(), media_type="text/plain")


@app.get("/")
async def root():
    """Endpoint racine."""
    return {
        "message": "Bienvenue sur la Plateforme de Gestion Python",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )