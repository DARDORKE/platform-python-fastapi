"""
Task service for business logic.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException, status

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Task service class."""
    
    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_tasks_by_user(
        db: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        """Get tasks by user with pagination."""
        result = await db.execute(
            select(Task)
            .where(Task.owner_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_tasks_by_project(
        db: AsyncSession, 
        project_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        """Get tasks by project with pagination."""
        result = await db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_all_tasks(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Task]:
        """Get all tasks with pagination."""
        result = await db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()
    
    @staticmethod
    async def create_task(
        db: AsyncSession, 
        task: TaskCreate, 
        user_id: int
    ) -> Task:
        """Create new task."""
        db_task = Task(
            **task.dict(),
            owner_id=user_id,
        )
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def update_task(
        db: AsyncSession, 
        task_id: int, 
        task_update: TaskUpdate,
        user_id: int
    ) -> Task:
        """Update task."""
        db_task = await TaskService.get_task_by_id(db, task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check ownership
        if db_task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Update fields
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)
        
        # Auto-update completion status and date
        if task_update.status == TaskStatus.DONE and not db_task.is_completed:
            db_task.is_completed = True
            db_task.completion_date = datetime.utcnow()
        elif task_update.status != TaskStatus.DONE and db_task.is_completed:
            db_task.is_completed = False
            db_task.completion_date = None
        
        await db.commit()
        await db.refresh(db_task)
        return db_task
    
    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
        """Delete task."""
        db_task = await TaskService.get_task_by_id(db, task_id)
        if not db_task:
            return False
        
        # Check ownership
        if db_task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        await db.delete(db_task)
        await db.commit()
        return True
    
    @staticmethod
    async def get_user_task_stats(db: AsyncSession, user_id: int) -> dict:
        """Get user task statistics."""
        result = await db.execute(
            select(
                func.count(Task.id).label("total_tasks"),
                func.count(Task.id).filter(Task.is_completed == True).label("completed_tasks"),
                func.count(Task.id).filter(Task.status == TaskStatus.IN_PROGRESS).label("in_progress_tasks"),
                func.count(Task.id).filter(Task.status == TaskStatus.TODO).label("todo_tasks"),
            )
            .where(Task.owner_id == user_id)
        )
        
        stats = result.first()
        return {
            "total_tasks": stats.total_tasks or 0,
            "completed_tasks": stats.completed_tasks or 0,
            "in_progress_tasks": stats.in_progress_tasks or 0,
            "todo_tasks": stats.todo_tasks or 0,
        }