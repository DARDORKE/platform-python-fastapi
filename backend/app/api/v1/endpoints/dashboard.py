"""
Dashboard endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, func
from pydantic import BaseModel

from app.core.database import get_session
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.project import Project
from app.models.task import Task, TaskStatus

router = APIRouter()


class DashboardStats(BaseModel):
    """Dashboard statistics."""
    users_count: int
    projects_count: int
    tasks_count: int
    completed_tasks: int
    active_projects: int


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics."""
    
    # Count total users
    users_result = await db.execute(
        text("SELECT COUNT(*) FROM users WHERE is_active = true")
    )
    users_count = users_result.scalar()
    
    # Count total projects
    projects_result = await db.execute(
        text("SELECT COUNT(*) FROM projects")
    )
    projects_count = projects_result.scalar()
    
    # Count active projects
    active_projects_result = await db.execute(
        text("SELECT COUNT(*) FROM projects WHERE status = 'ACTIVE'")
    )
    active_projects = active_projects_result.scalar()
    
    # Count total tasks
    tasks_result = await db.execute(
        text("SELECT COUNT(*) FROM tasks")
    )
    tasks_count = tasks_result.scalar()
    
    # Count completed tasks
    completed_tasks_result = await db.execute(
        text("SELECT COUNT(*) FROM tasks WHERE status = 'DONE'")
    )
    completed_tasks = completed_tasks_result.scalar()
    
    return DashboardStats(
        users_count=users_count or 0,
        projects_count=projects_count or 0,
        tasks_count=tasks_count or 0,
        completed_tasks=completed_tasks or 0,
        active_projects=active_projects or 0
    )