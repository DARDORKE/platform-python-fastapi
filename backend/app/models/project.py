"""
Project model for project management.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import Base


class ProjectStatus(PyEnum):
    """Project status enumeration."""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectPriority(PyEnum):
    """Project priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Project(Base):
    """Project model."""
    
    __tablename__ = "projects"
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    priority = Column(Enum(ProjectPriority), default=ProjectPriority.MEDIUM)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget = Column(Integer, nullable=True)  # Budget in cents
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"