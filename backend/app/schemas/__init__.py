"""
Schemas package initialization.
"""
from app.schemas.user import User, UserCreate, UserUpdate, UserInDB, UserWithStats
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectInDB, ProjectWithStats, ProjectWithTasks
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskInDB, TaskWithProject
from app.schemas.auth import Token, TokenData, LoginRequest, RefreshTokenRequest, PasswordChangeRequest

__all__ = [
    # User schemas
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserWithStats",
    
    # Project schemas
    "Project",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectInDB",
    "ProjectWithStats",
    "ProjectWithTasks",
    
    # Task schemas
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskInDB",
    "TaskWithProject",
    
    # Auth schemas
    "Token",
    "TokenData",
    "LoginRequest",
    "RefreshTokenRequest",
    "PasswordChangeRequest",
]