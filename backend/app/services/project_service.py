"""
Project service for business logic.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.project import Project
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Project service class."""
    
    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_projects_by_user(
        db: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Project]:
        """Get projects by user with pagination."""
        result = await db.execute(
            select(Project)
            .where(Project.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_all_projects(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Project]:
        """Get all projects with pagination."""
        result = await db.execute(select(Project).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def create_project(
        db: AsyncSession, 
        project: ProjectCreate, 
        user_id: int
    ) -> Project:
        """Create new project."""
        db_project = Project(
            **project.model_dump(),
            owner_id=user_id,
        )
        
        db.add(db_project)
        await db.commit()
        await db.refresh(db_project)
        return db_project
    
    @staticmethod
    async def update_project(
        db: AsyncSession, 
        project_id: int, 
        project_update: ProjectUpdate,
        user_id: int
    ) -> Project:
        """Update project."""
        db_project = await ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Check ownership
        if db_project.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Update fields
        for field, value in project_update.model_dump(exclude_unset=True).items():
            setattr(db_project, field, value)
        
        await db.commit()
        await db.refresh(db_project)
        return db_project
    
    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int, user_id: int) -> bool:
        """Delete project."""
        db_project = await ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            return False
        
        # Check ownership
        if db_project.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        await db.delete(db_project)
        await db.commit()
        return True
    
    @staticmethod
    async def get_project_stats(db: AsyncSession, project_id: int) -> dict:
        """Get project statistics."""
        # Get task counts
        result = await db.execute(
            select(
                func.count(Task.id).label("total_tasks"),
                func.count(Task.id).filter(Task.is_completed == True).label("completed_tasks"),
                func.count(Task.id).filter(Task.status == "in_progress").label("in_progress_tasks"),
            )
            .where(Task.project_id == project_id)
        )
        
        stats = result.first()
        total_tasks = stats.total_tasks or 0
        completed_tasks = stats.completed_tasks or 0
        in_progress_tasks = stats.in_progress_tasks or 0
        
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completion_percentage": round(completion_percentage, 2),
        }