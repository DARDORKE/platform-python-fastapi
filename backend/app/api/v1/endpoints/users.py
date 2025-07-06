"""
User endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies import get_current_active_user, get_current_superuser
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate, UserWithStats
from app.services.user_service import UserService
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    """Get all users (admin only)."""
    return await UserService.get_users(db, skip=skip, limit=limit)


@router.get("/me", response_model=UserWithStats)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session)
):
    """Get current user with statistics."""
    stats = await TaskService.get_user_task_stats(db, current_user.id)
    
    user_data = UserWithStats.from_orm(current_user)
    user_data.total_tasks = stats["total_tasks"]
    user_data.completed_tasks = stats["completed_tasks"]
    
    return user_data


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID."""
    # Users can only see their own profile, unless they are superuser
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    """Create new user (admin only)."""
    return await UserService.create_user(db, user)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update user."""
    # Users can only update their own profile, unless they are superuser
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return await UserService.update_user(db, user_id, user_update)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_superuser)
):
    """Delete user (admin only)."""
    success = await UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}