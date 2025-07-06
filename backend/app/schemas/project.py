"""
Project schemas for API serialization.
"""
from typing import Optional, List, Union, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, computed_field
from app.models.project import ProjectStatus, ProjectPriority


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: Optional[Union[datetime, str]] = None
    end_date: Optional[Union[datetime, str]] = None
    budget: Optional[int] = None  # Budget as integer
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        """Parse date from string format YYYY-MM-DD to datetime."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v + 'T00:00:00' if 'T' not in v else v)
            except ValueError:
                raise ValueError("Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
        return v


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    start_date: Optional[Union[datetime, str]] = None
    end_date: Optional[Union[datetime, str]] = None
    budget: Optional[int] = None
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        """Parse date from string format YYYY-MM-DD to datetime."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v + 'T00:00:00' if 'T' not in v else v)
            except ValueError:
                raise ValueError("Date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
        return v


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