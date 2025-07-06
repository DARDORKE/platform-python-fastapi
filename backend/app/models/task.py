"""
Task model for task management.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import Base


class TaskStatus(PyEnum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(PyEnum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    """Task model."""
    
    __tablename__ = "tasks"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    due_date = Column(DateTime, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"