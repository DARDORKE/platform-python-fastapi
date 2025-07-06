"""
Task endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=List[Task])
async def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    project_id: int = Query(None, description="Filter by project ID"),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's tasks."""
    if project_id:
        return await TaskService.get_tasks_by_project(db, project_id, skip=skip, limit=limit)
    else:
        return await TaskService.get_tasks_by_user(db, current_user.id, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get task by ID."""
    task = await TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check ownership
    if task.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create new task."""
    return await TaskService.create_task(db, task, current_user.id)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update task."""
    return await TaskService.update_task(db, task_id, task_update, current_user.id)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete task."""
    success = await TaskService.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {"message": "Task deleted successfully"}


@router.get("/stats/me")
async def get_my_task_stats(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's task statistics."""
    return await TaskService.get_user_task_stats(db, current_user.id)