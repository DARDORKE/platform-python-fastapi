"""
Task schemas for API serialization.
"""
from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[Union[datetime, str]] = None
    estimated_hours: Optional[float] = Field(None, ge=0, le=1000)
    actual_hours: Optional[float] = Field(None, ge=0, le=1000)
    project_id: Optional[int] = None
    
    @field_validator('due_date', mode='before')
    @classmethod
    def parse_due_date(cls, v):
        """Parse date from string format YYYY-MM-DD to datetime."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v + 'T00:00:00' if 'T' not in v else v)
            except ValueError:
                raise ValueError("Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
        return v


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(BaseModel):
    """Task update schema."""
    title: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[Union[datetime, str]] = None
    estimated_hours: Optional[float] = Field(None, ge=0, le=1000)
    actual_hours: Optional[float] = Field(None, ge=0, le=1000)
    project_id: Optional[int] = None
    
    @field_validator('due_date', mode='before')
    @classmethod
    def parse_due_date(cls, v):
        """Parse date from string format YYYY-MM-DD to datetime."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v + 'T00:00:00' if 'T' not in v else v)
            except ValueError:
                raise ValueError("Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
        return v


class TaskInDB(TaskBase):
    """Task schema with database fields."""
    id: int
    owner_id: int
    is_completed: bool = False
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Task(TaskInDB):
    """Public task schema."""
    pass


class TaskWithProject(Task):
    """Task with project information."""
    project_name: Optional[str] = None
    project_status: Optional[str] = None