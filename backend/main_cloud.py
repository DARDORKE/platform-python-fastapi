"""
FastAPI application for cloud deployment (Railway + Supabase).
This version uses real PostgreSQL database instead of in-memory data.
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
import jwt
from contextlib import asynccontextmanager

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable is required")
    print("Available env vars:", list(os.environ.keys()))
    raise ValueError("DATABASE_URL environment variable is required")

# CORS origins - include both local and production URLs
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

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
            print("🔄 Closing database connection pool")
            await db_pool.close()

app = FastAPI(
    title="Platform Python FastAPI",
    version="1.0.0",
    description="Demo platform for portfolio showcase - Cloud Version",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool = True
    role: str = "USER"
    created_at: datetime

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str
    role: str = "USER"

class UserLogin(BaseModel):
    email: str
    password: str

class Project(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str = "ACTIVE"
    priority: str = "MEDIUM"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner_id: int
    created_at: datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "ACTIVE"
    priority: str = "MEDIUM"
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

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

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
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    async with db_pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT id, email, username, full_name, is_active, role, created_at FROM users WHERE id = $1",
            user_id
        )
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        return User(**dict(user_data))

# Simple health check pour Railway (sans DB)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(),
        "environment": "cloud",
        "service": "platform-api"
    }

# Health check complet avec base de données
@app.get("/health/full")
async def full_health_check():
    try:
        # Test database connection
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            
            return {
                "status": "healthy", 
                "timestamp": datetime.utcnow(),
                "database": "connected",
                "environment": "cloud"
            }
        else:
            return {
                "status": "starting",
                "timestamp": datetime.utcnow(), 
                "database": "initializing",
                "environment": "cloud"
            }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "timestamp": datetime.utcnow(),
            "database": "disconnected",
            "error": str(e),
            "environment": "cloud"
        }

# Simple root endpoint
@app.get("/")
async def root():
    return {
        "message": "Platform Portfolio API", 
        "status": "running",
        "docs": "/docs"
    }

# Authentication endpoints
@app.post("/api/v1/auth/register", response_model=User)
async def register(user_data: UserCreate):
    async with db_pool.acquire() as conn:
        # Check if user exists
        existing = await conn.fetchrow("SELECT id FROM users WHERE email = $1 OR username = $2", 
                                     user_data.email, user_data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Email or username already registered")
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user_id = await conn.fetchval(
            """INSERT INTO users (email, username, full_name, hashed_password, role) 
               VALUES ($1, $2, $3, $4, $5) RETURNING id""",
            user_data.email, user_data.username, user_data.full_name, hashed_password, user_data.role
        )
        
        # Fetch created user
        user_record = await conn.fetchrow(
            "SELECT id, email, username, full_name, is_active, role, created_at FROM users WHERE id = $1",
            user_id
        )
        return User(**dict(user_record))

@app.post("/api/v1/auth/login", response_model=Token)
async def login_form(email: str, password: str):
    return await _authenticate_user(email, password)

@app.post("/api/v1/auth/login/json", response_model=Token)
async def login_json(user_data: UserLogin):
    return await _authenticate_user(user_data.email, user_data.password)

async def _authenticate_user(email: str, password: str) -> Token:
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
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

# User endpoints
@app.get("/api/v1/users/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/v1/users", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        users_data = await conn.fetch(
            "SELECT id, email, username, full_name, is_active, role, created_at FROM users ORDER BY created_at DESC"
        )
        return [User(**dict(user)) for user in users_data]

# Project endpoints
@app.get("/api/v1/projects", response_model=List[Project])
async def get_projects(current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        projects_data = await conn.fetch(
            "SELECT * FROM projects ORDER BY created_at DESC"
        )
        return [Project(**dict(project)) for project in projects_data]

@app.get("/api/v1/projects/{project_id}", response_model=Project)
async def get_project(project_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        project_data = await conn.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
        if not project_data:
            raise HTTPException(status_code=404, detail="Project not found")
        return Project(**dict(project_data))

@app.post("/api/v1/projects", response_model=Project)
async def create_project(project_data: ProjectCreate, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        project_id = await conn.fetchval(
            """INSERT INTO projects (title, description, status, priority, start_date, end_date, owner_id)
               VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id""",
            project_data.title, project_data.description, project_data.status,
            project_data.priority, project_data.start_date, project_data.end_date, current_user.id
        )
        
        project_record = await conn.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
        return Project(**dict(project_record))

@app.put("/api/v1/projects/{project_id}", response_model=Project)
async def update_project(project_id: int, project_data: ProjectCreate, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        # Check if project exists
        existing = await conn.fetchrow("SELECT owner_id FROM projects WHERE id = $1", project_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Update project
        await conn.execute(
            """UPDATE projects SET title = $1, description = $2, status = $3, priority = $4, 
               start_date = $5, end_date = $6 WHERE id = $7""",
            project_data.title, project_data.description, project_data.status,
            project_data.priority, project_data.start_date, project_data.end_date, project_id
        )
        
        project_record = await conn.fetchrow("SELECT * FROM projects WHERE id = $1", project_id)
        return Project(**dict(project_record))

@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM projects WHERE id = $1", project_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}

# Task endpoints
@app.get("/api/v1/tasks", response_model=List[Task])
async def get_tasks(project_id: Optional[int] = None, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        if project_id:
            tasks_data = await conn.fetch(
                "SELECT * FROM tasks WHERE project_id = $1 ORDER BY created_at DESC", project_id
            )
        else:
            tasks_data = await conn.fetch("SELECT * FROM tasks ORDER BY created_at DESC")
        return [Task(**dict(task)) for task in tasks_data]

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        task_data = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**dict(task_data))

@app.post("/api/v1/tasks", response_model=Task)
async def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        task_id = await conn.fetchval(
            """INSERT INTO tasks (title, description, status, priority, due_date, project_id, assigned_to, created_by)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id""",
            task_data.title, task_data.description, task_data.status, task_data.priority,
            task_data.due_date, task_data.project_id, task_data.assigned_to, current_user.id
        )
        
        task_record = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        return Task(**dict(task_record))

@app.put("/api/v1/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_data: TaskCreate, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        # Check if task exists
        existing = await conn.fetchrow("SELECT id FROM tasks WHERE id = $1", task_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update task
        await conn.execute(
            """UPDATE tasks SET title = $1, description = $2, status = $3, priority = $4,
               due_date = $5, project_id = $6, assigned_to = $7 WHERE id = $8""",
            task_data.title, task_data.description, task_data.status, task_data.priority,
            task_data.due_date, task_data.project_id, task_data.assigned_to, task_id
        )
        
        task_record = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        return Task(**dict(task_record))

@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}

# Dashboard endpoint
@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        total_projects = await conn.fetchval("SELECT COUNT(*) FROM projects")
        total_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks")
        completed_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE status = 'COMPLETED'")
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
        
        return {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_users": total_users,
            "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        }

@app.get("/api/v1/tasks/stats/me")
async def get_my_task_stats(current_user: User = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        my_tasks = await conn.fetchval("SELECT COUNT(*) FROM tasks WHERE assigned_to = $1", current_user.id)
        my_completed = await conn.fetchval(
            "SELECT COUNT(*) FROM tasks WHERE assigned_to = $1 AND status = 'COMPLETED'", current_user.id
        )
        
        return {
            "total_assigned": my_tasks,
            "completed": my_completed,
            "pending": my_tasks - my_completed,
            "completion_rate": round((my_completed / my_tasks * 100) if my_tasks > 0 else 0, 1)
        }

if __name__ == "__main__":
    import uvicorn
    # Railway utilise le port 8080 par défaut, ou $PORT si défini
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)