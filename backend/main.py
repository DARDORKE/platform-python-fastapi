"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

# Configuration
API_V1_STR = "/api/v1"
PROJECT_NAME = "Platform Python FastAPI"
VERSION = "1.0.0"

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:19006",
    "http://127.0.0.1:3000",
]

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Demo platform for portfolio showcase",
    openapi_url=f"{API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
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

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

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
    created_at: datetime

# Demo data
demo_users = [
    User(
        id=1,
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        role="ADMIN",
        created_at=datetime.now()
    ),
    User(
        id=2,
        email="manager@example.com",
        username="manager",
        full_name="Project Manager",
        role="MANAGER",
        created_at=datetime.now()
    ),
    User(
        id=3,
        email="john.doe@example.com",
        username="johndoe",
        full_name="John Doe",
        role="USER",
        created_at=datetime.now()
    )
]

demo_projects = [
    Project(
        id=1,
        name="E-commerce Platform",
        description="Development of a modern e-commerce platform with React and FastAPI",
        status="ACTIVE",
        priority="HIGH",
        budget=50000,
        created_at=datetime.now()
    ),
    Project(
        id=2,
        name="Mobile App Development",
        description="React Native mobile application for iOS and Android",
        status="PLANNING",
        priority="MEDIUM",
        budget=35000,
        created_at=datetime.now()
    )
]

demo_tasks = [
    Task(
        id=1,
        title="Setup project repository",
        description="Initialize Git repository and setup CI/CD pipeline",
        status="DONE",
        priority="HIGH",
        is_completed=True,
        created_at=datetime.now()
    ),
    Task(
        id=2,
        title="Implement user authentication",
        description="JWT-based authentication system with refresh tokens",
        status="IN_PROGRESS",
        priority="HIGH",
        is_completed=False,
        created_at=datetime.now()
    )
]

# Routes
@app.get("/")
async def root():
    return {"message": "Platform API is running!", "version": VERSION}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

# Auth endpoints
@app.post(f"{API_V1_STR}/auth/register", response_model=Token)
async def register(user_data: RegisterRequest):
    # Simulate registration
    return Token(
        access_token="demo_access_token",
        token_type="bearer",
        refresh_token="demo_refresh_token"
    )

@app.post(f"{API_V1_STR}/auth/login", response_model=Token)
async def login(credentials: LoginRequest):
    # Simulate login
    demo_credentials = {
        "admin@example.com": "admin123",
        "manager@example.com": "manager123",
        "john.doe@example.com": "user123"
    }
    
    if credentials.email in demo_credentials and demo_credentials[credentials.email] == credentials.password:
        return Token(
            access_token="demo_access_token",
            token_type="bearer",
            refresh_token="demo_refresh_token"
        )
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# User endpoints
@app.get(f"{API_V1_STR}/users", response_model=List[User])
async def get_users():
    return demo_users

@app.get(f"{API_V1_STR}/users/me", response_model=User)
async def get_current_user():
    return demo_users[0]  # Return admin user for demo

# Project endpoints
@app.get(f"{API_V1_STR}/projects", response_model=List[Project])
async def get_projects():
    return demo_projects

@app.get(f"{API_V1_STR}/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    project = next((p for p in demo_projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Task endpoints
@app.get(f"{API_V1_STR}/tasks", response_model=List[Task])
async def get_tasks():
    return demo_tasks

@app.get(f"{API_V1_STR}/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = next((t for t in demo_tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Dashboard endpoint
@app.get(f"{API_V1_STR}/dashboard/stats")
async def get_dashboard_stats():
    return {
        "users_count": len(demo_users),
        "projects_count": len(demo_projects),
        "tasks_count": len(demo_tasks),
        "completed_tasks": len([t for t in demo_tasks if t.is_completed]),
        "active_projects": len([p for p in demo_projects if p.status == "ACTIVE"])
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)