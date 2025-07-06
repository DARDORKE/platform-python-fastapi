"""
User model for authentication and user management.
"""
from sqlalchemy import Boolean, Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import Base


class UserRole(PyEnum):
    """User role enumeration."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    tasks = relationship("Task", back_populates="owner")
    projects = relationship("Project", back_populates="owner")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"