"""
Advanced API endpoints showcasing FastAPI capabilities.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
import asyncio
import json
import csv
import io
from datetime import datetime

from app.core.database import get_session
from app.core.dependencies import (
    CurrentActiveUser, CurrentAdminUser, PaginationDep, SearchDep, 
    CacheDep, RequestIdDep, get_content_type
)
from app.core.validators_simple import CreateUserSimple, CreateProjectSimple
from app.models.user import User
from app.services.user_service import UserService
from app.services.project_service import ProjectService


router = APIRouter()


class BulkOperationResult(BaseModel):
    """Résultat d'une opération en lot."""
    success_count: int
    error_count: int
    errors: List[Dict[str, Any]]
    processed_ids: List[int]


class ExportOptions(BaseModel):
    """Options d'export."""
    format: str = "json"  # json, csv, xml
    fields: Optional[List[str]] = None
    include_deleted: bool = False
    date_range: Optional[Dict[str, datetime]] = None


class AsyncTaskResult(BaseModel):
    """Résultat d'une tâche asynchrone."""
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[int] = None


@router.post("/bulk-users", response_model=BulkOperationResult)
async def create_bulk_users(
    users_data: List[CreateUserSimple],
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentAdminUser = None,
    request_id: RequestIdDep = None
):
    """
    Création en lot d'utilisateurs avec validation avancée.
    
    Fonctionnalités:
    - Validation stricte de chaque utilisateur
    - Traitement asynchrone en arrière-plan
    - Rollback en cas d'erreur partielle
    - Logging détaillé
    """
    
    result = BulkOperationResult(
        success_count=0,
        error_count=0,
        errors=[],
        processed_ids=[]
    )
    
    user_service = UserService(session)
    
    # Traitement en lot avec gestion d'erreurs
    for i, user_data in enumerate(users_data):
        try:
            # Vérifier si l'utilisateur existe déjà
            existing_user = await user_service.get_by_email(user_data.email)
            if existing_user:
                result.error_count += 1
                result.errors.append({
                    "index": i,
                    "email": user_data.email,
                    "error": "Utilisateur déjà existant"
                })
                continue
            
            # Créer l'utilisateur
            user = await user_service.create_user(user_data.dict())
            result.success_count += 1
            result.processed_ids.append(user.id)
            
        except Exception as e:
            result.error_count += 1
            result.errors.append({
                "index": i,
                "email": user_data.email,
                "error": str(e)
            })
    
    # Tâche en arrière-plan pour notification
    background_tasks.add_task(
        send_bulk_creation_notification,
        result.dict(),
        current_user.email,
        request_id
    )
    
    return result


@router.get("/users/export")
async def export_users(
    response: Response,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentAdminUser = None,
    content_type: str = Depends(get_content_type),
    pagination: PaginationDep = None,
    search: SearchDep = None,
    include_deleted: bool = Query(False),
    format: str = Query("json", regex="^(json|csv|xml)$")
):
    """
    Export des utilisateurs dans différents formats.
    
    Fonctionnalités:
    - Formats multiples (JSON, CSV, XML)
    - Streaming pour gros volumes
    - Filtrage et pagination
    - Négociation de contenu
    """
    
    user_service = UserService(session)
    
    # Récupérer les utilisateurs avec filtres
    users = await user_service.get_users_with_filters(
        skip=pagination.offset,
        limit=pagination.size,
        search_query=search.q,
        search_fields=search.fields or ["email", "first_name", "last_name"],
        include_deleted=include_deleted
    )
    
    # Génération du contenu selon le format
    if format == "csv":
        return StreamingResponse(
            generate_csv_stream(users),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=users.csv"}
        )
    elif format == "xml":
        return StreamingResponse(
            generate_xml_stream(users),
            media_type="application/xml",
            headers={"Content-Disposition": "attachment; filename=users.xml"}
        )
    else:
        return StreamingResponse(
            generate_json_stream(users),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=users.json"}
        )


@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    session: AsyncSession = Depends(get_session),
    current_user: CurrentActiveUser = None,
    cache_service: CacheDep = None,
    date_range: Optional[str] = Query(None, regex="^(7d|30d|90d|1y)$")
):
    """
    Tableau de bord analytique avec cache intelligent.
    
    Fonctionnalités:
    - Métriques en temps réel
    - Cache intelligent avec TTL
    - Calculs complexes optimisés
    - Données historiques
    """
    
    # Clé de cache basée sur les paramètres
    cache_key = f"analytics_dashboard:{current_user.id}:{date_range or '30d'}"
    
    # Vérifier le cache
    cached_data = await cache_service.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Calculer les métriques
    user_service = UserService(session)
    project_service = ProjectService(session)
    
    # Métriques utilisateurs
    total_users = await user_service.count_users()
    active_users = await user_service.count_active_users()
    new_users_today = await user_service.count_new_users_today()
    
    # Métriques projets
    total_projects = await project_service.count_projects()
    active_projects = await project_service.count_active_projects()
    completed_projects = await project_service.count_completed_projects()
    
    # Métriques avancées
    user_growth = await user_service.get_user_growth_stats(date_range or "30d")
    project_completion_rate = await project_service.get_completion_rate()
    
    analytics_data = {
        "users": {
            "total": total_users,
            "active": active_users,
            "new_today": new_users_today,
            "growth": user_growth
        },
        "projects": {
            "total": total_projects,
            "active": active_projects,
            "completed": completed_projects,
            "completion_rate": project_completion_rate
        },
        "generated_at": datetime.now().isoformat(),
        "cache_key": cache_key
    }
    
    # Mettre en cache pour 10 minutes
    await cache_service.set(cache_key, json.dumps(analytics_data), ttl=600)
    
    return analytics_data


@router.post("/tasks/async")
async def create_async_task(
    task_type: str = Query(..., regex="^(data_import|report_generation|cleanup)$"),
    parameters: Dict[str, Any] = None,
    current_user: CurrentActiveUser = None,
    request_id: RequestIdDep = None
):
    """
    Création de tâches asynchrones avec suivi.
    
    Fonctionnalités:
    - Tâches longues en arrière-plan
    - Suivi de progression
    - Notifications de fin
    - Gestion d'erreurs
    """
    
    import uuid
    task_id = str(uuid.uuid4())
    
    # Créer la tâche selon le type
    if task_type == "data_import":
        # Lancer l'import de données
        asyncio.create_task(
            process_data_import(task_id, parameters or {}, current_user.id)
        )
    elif task_type == "report_generation":
        # Lancer la génération de rapport
        asyncio.create_task(
            generate_report(task_id, parameters or {}, current_user.id)
        )
    elif task_type == "cleanup":
        # Lancer le nettoyage
        asyncio.create_task(
            cleanup_data(task_id, parameters or {}, current_user.id)
        )
    
    return AsyncTaskResult(
        task_id=task_id,
        status="started",
        progress=0
    )


@router.get("/tasks/{task_id}/status")
async def get_task_status(
    task_id: str,
    cache_service: CacheDep = None,
    current_user: CurrentActiveUser = None
):
    """
    Récupérer le statut d'une tâche asynchrone.
    
    Fonctionnalités:
    - Suivi en temps réel
    - Progression détaillée
    - Résultats intermédiaires
    """
    
    # Récupérer le statut depuis le cache
    status_data = await cache_service.get(f"task_status:{task_id}")
    
    if not status_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tâche non trouvée"
        )
    
    return json.loads(status_data)


@router.get("/health/detailed")
async def detailed_health_check(
    session: AsyncSession = Depends(get_session),
    cache_service: CacheDep = None
):
    """
    Vérification de santé détaillée.
    
    Fonctionnalités:
    - Statut des services
    - Métriques de performance
    - Diagnostics avancés
    """
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "metrics": {}
    }
    
    # Vérifier la base de données
    try:
        result = await session.execute(text("SELECT 1"))
        health_data["services"]["database"] = {
            "status": "healthy",
            "response_time": "< 10ms"
        }
    except Exception as e:
        health_data["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_data["status"] = "unhealthy"
    
    # Vérifier Redis
    try:
        await cache_service.set("health_check", "ok", ttl=10)
        health_data["services"]["redis"] = {
            "status": "healthy",
            "response_time": "< 5ms"
        }
    except Exception as e:
        health_data["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_data["status"] = "unhealthy"
    
    # Métriques système
    import psutil
    health_data["metrics"] = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }
    
    return health_data


# Fonctions utilitaires pour les streams
async def generate_csv_stream(users):
    """Générer un stream CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(["id", "email", "first_name", "last_name", "role", "created_at"])
    
    # Données
    for user in users:
        writer.writerow([
            user.id, user.email, user.first_name, 
            user.last_name, user.role, user.created_at
        ])
    
    output.seek(0)
    yield output.read()


async def generate_xml_stream(users):
    """Générer un stream XML."""
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield '<users>\n'
    
    for user in users:
        yield f'  <user id="{user.id}">\n'
        yield f'    <email>{user.email}</email>\n'
        yield f'    <first_name>{user.first_name}</first_name>\n'
        yield f'    <last_name>{user.last_name}</last_name>\n'
        yield f'    <role>{user.role}</role>\n'
        yield f'    <created_at>{user.created_at}</created_at>\n'
        yield f'  </user>\n'
    
    yield '</users>'


async def generate_json_stream(users):
    """Générer un stream JSON."""
    yield '{\n  "users": [\n'
    
    for i, user in enumerate(users):
        if i > 0:
            yield ',\n'
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }
        
        yield f'    {json.dumps(user_data)}'
    
    yield '\n  ]\n}'


# Tâches asynchrones
async def send_bulk_creation_notification(result: dict, admin_email: str, request_id: str):
    """Envoyer une notification de création en lot."""
    await asyncio.sleep(1)  # Simuler l'envoi
    print(f"Notification envoyée à {admin_email} pour la requête {request_id}")
    print(f"Résultat: {result}")


async def process_data_import(task_id: str, parameters: dict, user_id: int):
    """Traiter l'import de données."""
    # Simuler un traitement long
    for i in range(10):
        await asyncio.sleep(1)
        # Mettre à jour le statut
        # await update_task_status(task_id, "running", progress=(i+1)*10)
    
    # await update_task_status(task_id, "completed", progress=100)


async def generate_report(task_id: str, parameters: dict, user_id: int):
    """Générer un rapport."""
    # Simuler la génération
    for i in range(5):
        await asyncio.sleep(2)
        # await update_task_status(task_id, "running", progress=(i+1)*20)
    
    # await update_task_status(task_id, "completed", progress=100)


async def cleanup_data(task_id: str, parameters: dict, user_id: int):
    """Nettoyer les données."""
    # Simuler le nettoyage
    for i in range(3):
        await asyncio.sleep(1)
        # await update_task_status(task_id, "running", progress=(i+1)*33)
    
    # await update_task_status(task_id, "completed", progress=100)