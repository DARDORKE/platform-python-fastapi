"""
Rate limiting middleware using Redis for distributed rate limiting.
"""
import time
from typing import Optional
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis import redis_client


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware de limitation de taux avec Redis.
    
    Fonctionnalités avancées:
    - Sliding window rate limiting
    - Configuration par endpoint
    - Exemptions pour certains utilisateurs
    - Métriques de limitation
    """
    
    def __init__(self, app, default_requests: int = 100, default_window: int = 60):
        super().__init__(app)
        self.default_requests = default_requests
        self.default_window = default_window
        
        # Configuration spécifique par endpoint
        self.endpoint_limits = {
            "/api/v1/auth/login": {"requests": 5, "window": 60},  # 5 req/min pour login
            "/api/v1/auth/register": {"requests": 3, "window": 60},  # 3 req/min pour register
            "/api/v1/projects": {"requests": 50, "window": 60},  # 50 req/min pour projects
            "/api/v1/tasks": {"requests": 100, "window": 60},  # 100 req/min pour tasks
        }
        
        # Utilisateurs exemptés (par email ou ID)
        self.exempt_users = set()
    
    async def dispatch(self, request: Request, call_next):
        """Traiter la requête avec limitation de taux."""
        
        # Ignorer certains endpoints
        if request.url.path in ["/health", "/metrics", "/docs", "/redoc"]:
            return await call_next(request)
        
        # Obtenir l'identifiant client (IP + User-Agent pour plus de précision)
        client_id = self._get_client_id(request)
        
        # Vérifier si l'utilisateur est exempté
        if await self._is_exempt_user(request):
            return await call_next(request)
        
        # Obtenir les limites pour cet endpoint
        limits = self._get_endpoint_limits(request.url.path)
        
        # Vérifier la limite
        is_allowed, current_count, reset_time = await self._check_rate_limit(
            client_id, request.url.path, limits["requests"], limits["window"]
        )
        
        if not is_allowed:
            # Ajouter des headers informatifs
            response = Response(
                content='{"detail": "Rate limit exceeded"}',
                status_code=429,
                media_type="application/json"
            )
            response.headers["X-RateLimit-Limit"] = str(limits["requests"])
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            response.headers["Retry-After"] = str(reset_time - int(time.time()))
            return response
        
        # Traiter la requête
        response = await call_next(request)
        
        # Ajouter des headers informatifs
        response.headers["X-RateLimit-Limit"] = str(limits["requests"])
        response.headers["X-RateLimit-Remaining"] = str(limits["requests"] - current_count)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Obtenir un identifiant unique pour le client."""
        # Utiliser l'IP + User-Agent pour plus de robustesse
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        return f"{client_ip}:{hash(user_agent)}"
    
    async def _is_exempt_user(self, request: Request) -> bool:
        """Vérifier si l'utilisateur est exempté."""
        # Ici, on pourrait vérifier l'utilisateur connecté
        # Pour l'instant, on utilise une liste d'IPs exemptées
        client_ip = request.client.host if request.client else "unknown"
        return client_ip in ["127.0.0.1", "localhost"]
    
    def _get_endpoint_limits(self, path: str) -> dict:
        """Obtenir les limites pour un endpoint spécifique."""
        return self.endpoint_limits.get(path, {
            "requests": self.default_requests,
            "window": self.default_window
        })
    
    async def _check_rate_limit(self, client_id: str, endpoint: str, 
                               max_requests: int, window: int) -> tuple[bool, int, int]:
        """
        Vérifier la limite de taux avec sliding window.
        
        Returns:
            (is_allowed, current_count, reset_time)
        """
        current_time = int(time.time())
        window_start = current_time - window
        
        # Clé Redis pour ce client et endpoint
        key = f"rate_limit:{client_id}:{endpoint}"
        
        try:
            # Pipeline Redis pour atomicité
            pipe = redis_client.pipeline()
            
            # Supprimer les entrées expirées
            pipe.zremrangebyscore(key, 0, window_start)
            
            # Compter les requêtes dans la fenêtre
            pipe.zcard(key)
            
            # Ajouter cette requête
            pipe.zadd(key, {str(current_time): current_time})
            
            # Définir l'expiration
            pipe.expire(key, window)
            
            # Exécuter le pipeline
            results = await pipe.execute()
            
            current_count = results[1] + 1  # +1 pour inclure la requête actuelle
            reset_time = current_time + window
            
            is_allowed = current_count <= max_requests
            
            return is_allowed, current_count, reset_time
            
        except Exception as e:
            # En cas d'erreur Redis, on autorise la requête
            print(f"Rate limiter error: {e}")
            return True, 0, current_time + window


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """Middleware pour liste blanche d'IPs."""
    
    def __init__(self, app, whitelist: Optional[list] = None):
        super().__init__(app)
        self.whitelist = whitelist or []
    
    async def dispatch(self, request: Request, call_next):
        """Vérifier si l'IP est dans la liste blanche."""
        
        # Si pas de liste blanche, autoriser tout
        if not self.whitelist:
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        # Vérifier les endpoints d'admin
        if request.url.path.startswith("/admin/"):
            if client_ip not in self.whitelist:
                return Response(
                    content='{"detail": "Access denied"}',
                    status_code=403,
                    media_type="application/json"
                )
        
        return await call_next(request)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Middleware de logging avancé des requêtes."""
    
    async def dispatch(self, request: Request, call_next):
        """Logger les requêtes avec informations détaillées."""
        
        start_time = time.time()
        
        # Informations de la requête
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Traiter la requête
        response = await call_next(request)
        
        # Calculer la durée
        duration = time.time() - start_time
        
        # Logger avec structuration
        log_data = {
            "timestamp": time.time(),
            "method": request.method,
            "url": str(request.url),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "headers": dict(request.headers),
        }
        
        # Stocker dans Redis pour analyse
        try:
            await redis_client.lpush("request_logs", str(log_data))
            await redis_client.ltrim("request_logs", 0, 9999)  # Garder les 10k dernières
        except Exception:
            pass  # Ignorer les erreurs Redis pour le logging
        
        return response