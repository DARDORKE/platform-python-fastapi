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
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL")
API_V1_STR = "/api/v1"

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable is required")
    raise ValueError("DATABASE_URL environment variable is required")

# CORS origins - include both local and production URLs
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
print(f"🌐 CORS Origins configured: {CORS_ORIGINS}")

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
        print(f"🔗 Connecting to database...")
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
        print("✅ Database connection pool created")
        yield
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    finally:
        if db_pool:
            await db_pool.close()
            print("🔗 Database connection pool closed")

app = FastAPI(
    title="Platform API - Cloud",
    description="Portfolio demonstration API with real database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporaire : autoriser tous les domaines
    allow_credentials=False,  # Obligatoire avec allow_origins=["*"]
    allow_methods=["*"],
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
    description: Optional[str] = None
    status: str = "PLANNING"
    priority: str = "MEDIUM"
    budget: Optional[float] = None
    created_at: datetime
    created_by: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    created_by: int
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

# Request models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    username: str
    full_name: str
    password: str

class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "PLANNING"
    priority: str = "MEDIUM"
    budget: Optional[float] = None

class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None
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
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
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
    return {"status": "healthy", "timestamp": datetime.utcnow()}

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
async def refresh_token():
    # Simple token refresh
    return Token(
        access_token="demo_new_access_token",
        token_type="bearer",
        refresh_token="demo_new_refresh_token"
    )

async def authenticate_user(email: str, password: str) -> Token:
    """Authenticate user with database"""
    async with db_pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT id, email, hashed_password FROM users WHERE email = $1 AND is_active = true",
            email
        )
        if not user_data or not verify_password(password, user_data["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user_data["id"]})
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

# Project endpoints
@app.get(f"{API_V1_STR}/projects", response_model=List[Project])
async def get_projects():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM projects ORDER BY id")
        return [Project(**dict(row)) for row in rows]

@app.get(f"{API_V1_STR}/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
        if not row:
            raise HTTPException(status_code=404, detail="Project not found")
        return Project(**dict(row))

@app.post(f"{API_V1_STR}/projects", response_model=Project)
async def create_project(project_data: CreateProjectRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO projects (name, description, status, priority, budget, created_by) 
               VALUES ($1, $2, $3, $4, $5, $6) 
               RETURNING *""",
            project_data.name, project_data.description, project_data.status,
            project_data.priority, project_data.budget, current_user.id
        )
        return Project(**dict(row))

@app.put(f"{API_V1_STR}/projects/{project_id}", response_model=Project)
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

@app.delete(f"{API_V1_STR}/projects/{project_id}")
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

@app.get(f"{API_V1_STR}/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**dict(row))

@app.post(f"{API_V1_STR}/tasks", response_model=Task)
async def create_task(task_data: CreateTaskRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO tasks (title, description, status, priority, due_date, project_id, created_by) 
               VALUES ($1, $2, $3, $4, $5, $6, $7) 
               RETURNING *""",
            task_data.title, task_data.description, task_data.status,
            task_data.priority, task_data.due_date, task_data.project_id, current_user.id
        )
        return Task(**dict(row))

@app.put(f"{API_V1_STR}/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_data: CreateTaskRequest, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE tasks SET title = $1, description = $2, status = $3, priority = $4, due_date = $5, project_id = $6
               WHERE id = $7 RETURNING *""",
            task_data.title, task_data.description, task_data.status,
            task_data.priority, task_data.due_date, task_data.project_id, task_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**dict(row))

@app.delete(f"{API_V1_STR}/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}

@app.get(f"{API_V1_STR}/tasks/stats/me")
async def get_my_task_stats(current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        stats = await conn.fetchrow(
            """SELECT 
                COUNT(*) as total_tasks,
                COUNT(*) FILTER (WHERE status = 'TODO') as todo_tasks,
                COUNT(*) FILTER (WHERE status = 'IN_PROGRESS') as in_progress_tasks,
                COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed_tasks
               FROM tasks WHERE created_by = $1""",
            current_user.id
        )
        return dict(stats) if stats else {"total_tasks": 0, "todo_tasks": 0, "in_progress_tasks": 0, "completed_tasks": 0}

@app.get(f"{API_V1_STR}/dashboard/stats")
async def get_dashboard_stats():
    async with db_pool.acquire() as conn:
        users_count = await conn.fetchval("SELECT COUNT(*) FROM users")
        projects_count = await conn.fetchval("SELECT COUNT(*) FROM projects")
        tasks_count = await conn.fetchval("SELECT COUNT(*) FROM tasks")
        completed_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE status = 'COMPLETED'")
        active_projects = await conn.fetchval("SELECT COUNT(*) FROM projects WHERE status = 'ACTIVE'")
        
        return {
            "users_count": users_count,
            "projects_count": projects_count,
            "tasks_count": tasks_count,
            "completed_tasks": completed_tasks,
            "active_projects": active_projects
        }