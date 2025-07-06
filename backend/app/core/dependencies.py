"""
Advanced dependencies for FastAPI.
"""
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Query, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.core.redis import redis_client
from app.core.security import verify_token
from app.core.validators_simple import PaginationParams, SearchParams
from app.models.user import User
from app.services.user_service import UserService


# Security
security = HTTPBearer()


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency pour obtenir l'utilisateur courant.
    
    Fonctionnalités avancées:
    - Vérification du token JWT
    - Cache Redis pour éviter les requêtes répétées
    - Gestion des tokens expirés
    """
    try:
        # Vérifier le token et récupérer l'user_id
        user_id = verify_token(credentials.credentials)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide"
            )
        
        # Vérifier en cache Redis d'abord
        cache_key = f"user:{user_id}"
        cached_user = await redis_client.get(cache_key)
        
        if cached_user:
            # Retourner l'utilisateur depuis le cache
            import json
            user_data = json.loads(cached_user)
            return User.model_validate(user_data)
        
        # Récupérer l'utilisateur depuis la base de données
        user_service = UserService(session)
        user = await user_service.get_by_id(int(user_id))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non trouvé"
            )
        
        # Mettre en cache pour 5 minutes
        await redis_client.setex(
            cache_key, 
            300, 
            user.model_dump_json()
        )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Dependency pour obtenir l'utilisateur actif."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency pour obtenir l'utilisateur admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilèges administrateur requis"
        )
    return current_user


async def get_current_manager_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency pour obtenir l'utilisateur manager ou admin."""
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilèges manager ou administrateur requis"
        )
    return current_user


# Pagination
async def get_pagination_params(
    page: int = Query(1, ge=1, le=1000, description="Numéro de page"),
    size: int = Query(10, ge=1, le=100, description="Taille de la page")
) -> PaginationParams:
    """Dependency pour les paramètres de pagination."""
    return PaginationParams(page=page, size=size)


# Search
async def get_search_params(
    q: Optional[str] = Query(None, min_length=1, max_length=100, description="Terme de recherche"),
    fields: Optional[list[str]] = Query(None, description="Champs à rechercher")
) -> SearchParams:
    """Dependency pour les paramètres de recherche."""
    return SearchParams(q=q, fields=fields)


# Rate limiting info
class RateLimitInfo(BaseModel):
    """Informations sur la limitation de taux."""
    limit: int
    remaining: int
    reset_time: int


async def get_rate_limit_info(
    request_id: str = Header(None, alias="X-Request-ID")
) -> Optional[RateLimitInfo]:
    """Dependency pour obtenir les informations de rate limiting."""
    if not request_id:
        return None
    
    try:
        # Récupérer les informations depuis Redis
        info = await redis_client.hgetall(f"rate_limit_info:{request_id}")
        if info:
            return RateLimitInfo(
                limit=int(info.get("limit", 0)),
                remaining=int(info.get("remaining", 0)),
                reset_time=int(info.get("reset_time", 0))
            )
    except Exception:
        pass
    
    return None


# Database transaction
class DatabaseTransaction:
    """Context manager pour les transactions de base de données."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def __aenter__(self):
        return self.session
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()


async def get_db_transaction(
    session: AsyncSession = Depends(get_session)
) -> DatabaseTransaction:
    """Dependency pour obtenir une transaction de base de données."""
    return DatabaseTransaction(session)


# Cache
class CacheService:
    """Service de cache avancé."""
    
    def __init__(self):
        self.default_ttl = 300  # 5 minutes
    
    async def get(self, key: str) -> Optional[str]:
        """Récupérer une valeur depuis le cache."""
        try:
            return await redis_client.get(f"cache:{key}")
        except Exception:
            return None
    
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Stocker une valeur dans le cache."""
        try:
            await redis_client.setex(
                f"cache:{key}", 
                ttl or self.default_ttl, 
                value
            )
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Supprimer une valeur du cache."""
        try:
            await redis_client.delete(f"cache:{key}")
            return True
        except Exception:
            return False
    
    async def exists(self, key: str) -> bool:
        """Vérifier si une clé existe dans le cache."""
        try:
            return await redis_client.exists(f"cache:{key}")
        except Exception:
            return False


async def get_cache_service() -> CacheService:
    """Dependency pour obtenir le service de cache."""
    return CacheService()


# API Key validation
async def validate_api_key(
    api_key: str = Header(None, alias="X-API-Key")
) -> bool:
    """Valider une clé API."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante"
        )
    
    # Vérifier la clé API en base ou cache
    try:
        valid_key = await redis_client.get(f"api_key:{api_key}")
        if not valid_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Clé API invalide"
            )
        return True
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erreur de validation de la clé API"
        )


# Content negotiation
async def get_content_type(
    accept: str = Header("application/json", alias="Accept")
) -> str:
    """Dependency pour la négociation de contenu."""
    supported_types = ["application/json", "application/xml", "text/csv"]
    
    # Parser le header Accept
    accepted_types = [t.strip() for t in accept.split(",")]
    
    for accepted_type in accepted_types:
        if accepted_type in supported_types:
            return accepted_type
    
    # Retourner JSON par défaut
    return "application/json"


# Request ID
async def get_request_id(
    request_id: str = Header(None, alias="X-Request-ID")
) -> str:
    """Dependency pour obtenir ou générer un ID de requête."""
    if not request_id:
        import uuid
        request_id = str(uuid.uuid4())
    
    return request_id


# Type aliases pour une utilisation plus claire
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]
CurrentManagerUser = Annotated[User, Depends(get_current_manager_user)]
PaginationDep = Annotated[PaginationParams, Depends(get_pagination_params)]
SearchDep = Annotated[SearchParams, Depends(get_search_params)]
CacheDep = Annotated[CacheService, Depends(get_cache_service)]
RequestIdDep = Annotated[str, Depends(get_request_id)]