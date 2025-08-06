"""
FastAPI application for cloud deployment (Railway + Supabase).
This version mirrors simple_main.py endpoints but uses real PostgreSQL database.
"""
import os
from datetime import datetime, timedelta
from typing import List, Optional

import asyncpg
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import jwt
from contextlib import asynccontextmanager

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "80f42ad38ba618fc60dfa0d283f87e8a")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL")
API_V1_STR = "/api/v1"


if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable is required")
    raise ValueError("DATABASE_URL environment variable is required")

# CORS origins - include both local and production URLs
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database connection pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection pool lifecycle"""
    global db_pool
    try:
        db_pool = await asyncpg.create_pool(
            DATABASE_URL, 
            min_size=1, 
            max_size=10,
            command_timeout=30,
            statement_cache_size=0,  # Désactive les prepared statements pour Supabase/pgbouncer
            server_settings={
                'jit': 'off'
            }
        )
        yield
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    finally:
        if db_pool:
            await db_pool.close()

app = FastAPI(
    title="Platform API - Cloud",
    description="Portfolio demonstration API with real database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://platform-python-fastapi.vercel.app",
        "http://localhost:3000",
        "https://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Models (same as simple_main.py)
class User(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool = True
    role: str = "USER"
    created_at: datetime

class Project(BaseModel):
    id: int
    name: str
    description: str
    status: str
    priority: str
    budget: Optional[float] = None
    created_at: datetime

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    is_completed: bool = False
    project_id: Optional[int] = None
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

# Request models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: str

class CreateProjectRequest(BaseModel):
    name: str
    description: str
    status: str = "planning"
    priority: str = "medium"
    budget: Optional[float] = None

class CreateTaskRequest(BaseModel):
    title: str
    description: str
    status: str = "todo"
    priority: str = "medium"
    project_id: Optional[int] = None

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token - no user ID")
        user_id = int(user_id)  # Convert string back to int
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    async with db_pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT id, email, username, full_name, is_active, role, created_at FROM users WHERE id = $1",
            user_id
        )
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return User(**dict(user_data))

# Routes
@app.get("/")
async def root():
    return {"message": "Platform API is running!", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Health check endpoint with database verification."""
    try:
        # Test database connection
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
        
        return {
            "status": "healthy", 
            "timestamp": datetime.utcnow(),
            "database": "connected" if db_pool else "not_configured"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "timestamp": datetime.utcnow(),
            "error": str(e)
        }

# Auth endpoints
@app.post(f"{API_V1_STR}/auth/register", response_model=Token)
async def register(user_data: RegisterRequest):
    # TODO: Implement real registration
    return Token(
        access_token="demo_access_token",
        token_type="bearer",
        refresh_token="demo_refresh_token"
    )

@app.post(f"{API_V1_STR}/auth/login", response_model=Token)
async def login(credentials: LoginRequest):
    return await authenticate_user(credentials.email, credentials.password)

@app.post(f"{API_V1_STR}/auth/login/json", response_model=Token)
async def login_json(credentials: LoginRequest):
    return await authenticate_user(credentials.email, credentials.password)

@app.post(f"{API_V1_STR}/auth/refresh", response_model=Token)
async def refresh_token(refresh_data: dict):
    # Pour l'instant, on génère un nouveau token sans vérifier le refresh token
    # TODO: Implémenter la vraie logique de refresh token
    try:
        # Normalement on devrait décoder le refresh token et vérifier sa validité
        # Pour l'instant on génère juste un nouveau token pour l'utilisateur 1
        access_token = create_access_token(data={"sub": "1"})  # TODO: obtenir le vrai user_id du refresh token
        return Token(
            access_token=access_token,
            token_type="bearer",
            refresh_token="demo_refresh_token"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

async def authenticate_user(email: str, password: str) -> Token:
    """Authenticate user with database"""
    async with db_pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT id, email, hashed_password FROM users WHERE email = $1 AND is_active = true",
            email
        )
        if not user_data or not verify_password(password, user_data["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": str(user_data["id"])})
        return Token(
            access_token=access_token,
            token_type="bearer",
            refresh_token="demo_refresh_token"
        )

# User endpoints
@app.get(f"{API_V1_STR}/users", response_model=List[User])
async def get_users():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, email, username, full_name, is_active, role, created_at FROM users ORDER BY id")
        return [User(**dict(row)) for row in rows]

@app.get(f"{API_V1_STR}/users/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Debug endpoint to test token validation
@app.get(f"{API_V1_STR}/debug/validate-token")
async def debug_validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload, "token_preview": token[:20] + "..."}
    except Exception as e:
        return {"valid": False, "error": str(e), "token_preview": token[:20] + "..."}

# Project endpoints
@app.get(f"{API_V1_STR}/projects", response_model=List[Project])
async def get_projects():
    try:
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM projects ORDER BY id")
            return [Project(**dict(row)) for row in rows]
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{API_V1_STR}/projects/{{project_id}}", response_model=Project)
async def get_project(project_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
        if not row:
            raise HTTPException(status_code=404, detail="Project not found")
        return Project(**dict(row))

@app.post(f"{API_V1_STR}/projects", response_model=Project)
@app.post(f"{API_V1_STR}/projects/", response_model=Project)
async def create_project(project_data: CreateProjectRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO projects (name, description, status, priority, budget) 
               VALUES ($1, $2, $3, $4, $5) 
               RETURNING *""",
            project_data.name, project_data.description, project_data.status,
            project_data.priority, project_data.budget
        )
        return Project(**dict(row))

@app.put(f"{API_V1_STR}/projects/{{project_id}}", response_model=Project)
async def update_project(project_id: int, project_data: CreateProjectRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE projects SET name = $1, description = $2, status = $3, priority = $4, budget = $5
               WHERE id = $6 RETURNING *""",
            project_data.name, project_data.description, project_data.status,
            project_data.priority, project_data.budget, project_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Project not found")
        return Project(**dict(row))

@app.delete(f"{API_V1_STR}/projects/{{project_id}}")
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM projects WHERE id = $1", project_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}

# Task endpoints
@app.get(f"{API_V1_STR}/tasks", response_model=List[Task])
async def get_tasks(project_id: Optional[int] = None):
    async with db_pool.acquire() as conn:
        if project_id:
            rows = await conn.fetch("SELECT * FROM tasks WHERE project_id = $1 ORDER BY id", project_id)
        else:
            rows = await conn.fetch("SELECT * FROM tasks ORDER BY id")
        return [Task(**dict(row)) for row in rows]

@app.get(f"{API_V1_STR}/tasks/{{task_id}}", response_model=Task)
async def get_task(task_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**dict(row))

@app.post(f"{API_V1_STR}/tasks", response_model=Task)
@app.post(f"{API_V1_STR}/tasks/", response_model=Task)
async def create_task(task_data: CreateTaskRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO tasks (title, description, status, priority, is_completed, project_id) 
               VALUES ($1, $2, $3, $4, $5, $6) 
               RETURNING *""",
            task_data.title, task_data.description, task_data.status,
            task_data.priority, task_data.status == "done", task_data.project_id
        )
        return Task(**dict(row))

@app.put(f"{API_V1_STR}/tasks/{{task_id}}", response_model=Task)
async def update_task(task_id: int, task_data: CreateTaskRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE tasks SET title = $1, description = $2, status = $3, priority = $4, is_completed = $5, project_id = $6
               WHERE id = $7 RETURNING *""",
            task_data.title, task_data.description, task_data.status,
            task_data.priority, task_data.status == "done", task_data.project_id, task_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**dict(row))

@app.delete(f"{API_V1_STR}/tasks/{{task_id}}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}

@app.get(f"{API_V1_STR}/tasks/stats/me")
async def get_task_stats():
    async with db_pool.acquire() as conn:
        total_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks")
        completed_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE is_completed = true")
        pending_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE is_completed = false")
        high_priority_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE priority = 'high'")
        
        return {
            "total_tasks": total_tasks or 0,
            "completed_tasks": completed_tasks or 0,
            "pending_tasks": pending_tasks or 0,
            "high_priority_tasks": high_priority_tasks or 0,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks else 0
        }

@app.get(f"{API_V1_STR}/dashboard/stats")
async def get_dashboard_stats():
    async with db_pool.acquire() as conn:
        users_count = await conn.fetchval("SELECT COUNT(*) FROM users")
        projects_count = await conn.fetchval("SELECT COUNT(*) FROM projects")
        tasks_count = await conn.fetchval("SELECT COUNT(*) FROM tasks")
        completed_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE is_completed = true")
        active_projects = await conn.fetchval("SELECT COUNT(*) FROM projects WHERE status = 'active'")
        
        return {
            "users_count": users_count,
            "projects_count": projects_count,
            "tasks_count": tasks_count,
            "completed_tasks": completed_tasks,
            "active_projects": active_projects
        }