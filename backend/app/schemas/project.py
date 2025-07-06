"""
Project schemas for API serialization.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.project import ProjectStatus, ProjectPriority


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[int] = None  # Budget in cents


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[int] = None


class ProjectInDB(ProjectBase):
    """Project schema with database fields."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Project(ProjectInDB):
    """Public project schema."""
    pass


class ProjectWithStats(Project):
    """Project with statistics."""
    total_tasks: int = 0
    completed_tasks: int = 0
    in_progress_tasks: int = 0
    completion_percentage: float = 0.0


class ProjectWithTasks(Project):
    """Project with tasks."""
    tasks: List["Task"] = []


# Forward reference for circular imports
from app.schemas.task import Task
ProjectWithTasks.update_forward_refs()