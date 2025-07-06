"""
Project endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectWithStats
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("/", response_model=List[Project])
async def read_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's projects."""
    return await ProjectService.get_projects_by_user(db, current_user.id, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectWithStats)
async def read_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get project by ID with statistics."""
    project = await ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check ownership
    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get project statistics
    stats = await ProjectService.get_project_stats(db, project_id)
    
    project_data = ProjectWithStats.model_validate(project)
    project_data.total_tasks = stats["total_tasks"]
    project_data.completed_tasks = stats["completed_tasks"]
    project_data.in_progress_tasks = stats["in_progress_tasks"]
    project_data.completion_percentage = stats["completion_percentage"]
    
    return project_data


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create new project."""
    return await ProjectService.create_project(db, project, current_user.id)


@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update project."""
    return await ProjectService.update_project(db, project_id, project_update, current_user.id)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete project."""
    success = await ProjectService.delete_project(db, project_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"message": "Project deleted successfully"}