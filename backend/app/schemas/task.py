"""
Task schemas for API serialization.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0, le=1000)
    actual_hours: Optional[int] = Field(None, ge=0, le=1000)
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0, le=1000)
    actual_hours: Optional[int] = Field(None, ge=0, le=1000)
    project_id: Optional[int] = None


class TaskInDB(TaskBase):
    """Task schema with database fields."""
    id: int
    owner_id: int
    is_completed: bool = False
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class Task(TaskInDB):
    """Public task schema."""
    pass


class TaskWithProject(Task):
    """Task with project information."""
    project_name: Optional[str] = None
    project_status: Optional[str] = None