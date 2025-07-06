#!/usr/bin/env python3
"""
Script to deploy fixtures and demo data to the database.
Can be run standalone or via Docker.
"""
import os
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from datetime import datetime, timedelta

# Add the backend directory to the path
sys.path.insert(0, '/app')
sys.path.insert(0, '/app/app')

from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, ProjectPriority
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash
from app.models.base import Base

def get_database_url():
    """Get database URL from environment or use default."""
    # Use synchronous driver for fixtures deployment
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://platform_user:platform_password@database:5432/platform"
    )
    # Convert asyncpg URL to psycopg2 URL for synchronous operation
    if "postgresql+asyncpg://" in database_url:
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    return database_url

def wait_for_database(engine, max_retries=30):
    """Wait for database to be ready."""
    print("⏳ Waiting for database connection...")
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection established")
            return True
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"❌ Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)
            else:
                print(f"❌ Failed to connect to database after {max_retries} attempts")
                return False
    return False

def create_tables(engine):
    """Create all tables."""
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def clear_existing_data(session):
    """Clear existing data from tables."""
    print("🗑️ Clearing existing data...")
    
    # Delete in reverse order of dependencies
    session.query(Task).delete()
    session.query(Project).delete()
    session.query(User).delete()
    session.commit()
    
    print("✅ Existing data cleared")

def create_demo_users(session):
    """Create demo users."""
    print("👥 Creating demo users...")
    
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "full_name": "Admin User",
            "hashed_password": get_password_hash("admin123"),
            "is_active": True,
            "is_superuser": True,
            "role": UserRole.ADMIN,
        },
        {
            "email": "manager@example.com",
            "username": "manager",
            "full_name": "Project Manager",
            "hashed_password": get_password_hash("manager123"),
            "is_active": True,
            "role": UserRole.MANAGER,
        },
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "full_name": "John Doe",
            "hashed_password": get_password_hash("user123"),
            "is_active": True,
            "role": UserRole.USER,
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "full_name": "Jane Smith",
            "hashed_password": get_password_hash("user123"),
            "is_active": True,
            "role": UserRole.USER,
        },
        {
            "email": "developer@example.com",
            "username": "developer",
            "full_name": "Senior Developer",
            "hashed_password": get_password_hash("dev123"),
            "is_active": True,
            "role": UserRole.USER,
        },
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        session.add(user)
        users.append(user)
    
    session.commit()
    print(f"✅ Created {len(users)} users")
    return users

def create_demo_projects(session, users):
    """Create demo projects."""
    print("📁 Creating demo projects...")
    
    projects_data = [
        {
            "name": "E-commerce Platform",
            "description": "Development of a modern e-commerce platform with React and FastAPI",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=60),
            "budget": 50000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "Mobile App Development",
            "description": "React Native mobile application for iOS and Android",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=15),
            "end_date": datetime.now() + timedelta(days=120),
            "budget": 35000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "API Documentation",
            "description": "Comprehensive API documentation and developer portal",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() - timedelta(days=10),
            "end_date": datetime.now() + timedelta(days=30),
            "budget": 15000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "DevOps Pipeline",
            "description": "CI/CD pipeline setup with Docker and Kubernetes",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": datetime.now() - timedelta(days=5),
            "budget": 25000,
            "owner_id": users[4].id,  # Developer
        },
    ]
    
    projects = []
    for project_data in projects_data:
        project = Project(**project_data)
        session.add(project)
        projects.append(project)
    
    session.commit()
    print(f"✅ Created {len(projects)} projects")
    return projects

def create_demo_tasks(session, users, projects):
    """Create demo tasks."""
    print("📝 Creating demo tasks...")
    
    tasks_data = [
        # E-commerce Platform tasks
        {
            "title": "Setup project repository",
            "description": "Initialize Git repository and setup CI/CD pipeline",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=25),
            "estimated_hours": 8,
            "actual_hours": 6,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=25),
            "owner_id": users[2].id,
            "project_id": projects[0].id,
        },
        {
            "title": "Implement user authentication",
            "description": "JWT-based authentication system with refresh tokens",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=5),
            "estimated_hours": 24,
            "actual_hours": 16,
            "owner_id": users[2].id,
            "project_id": projects[0].id,
        },
        {
            "title": "Product catalog API",
            "description": "REST API endpoints for product management",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=15),
            "estimated_hours": 32,
            "owner_id": users[2].id,
            "project_id": projects[0].id,
        },
        {
            "title": "Shopping cart functionality",
            "description": "Implement shopping cart with Redis session storage",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 16,
            "owner_id": users[3].id,
            "project_id": projects[0].id,
        },
        # Mobile App tasks
        {
            "title": "App architecture design",
            "description": "Design React Native application architecture",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 12,
            "actual_hours": 8,
            "owner_id": users[4].id,
            "project_id": projects[1].id,
        },
        {
            "title": "UI/UX mockups",
            "description": "Create detailed mockups for all app screens",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 20,
            "owner_id": users[3].id,
            "project_id": projects[1].id,
        },
        # API Documentation tasks
        {
            "title": "API endpoint documentation",
            "description": "Document all REST API endpoints with OpenAPI",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() - timedelta(days=5),
            "estimated_hours": 16,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=5),
            "owner_id": users[2].id,
            "project_id": projects[2].id,
        },
        {
            "title": "Developer portal setup",
            "description": "Setup developer portal with interactive API docs",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 12,
            "actual_hours": 4,
            "owner_id": users[2].id,
            "project_id": projects[2].id,
        },
        # DevOps Pipeline tasks
        {
            "title": "Docker containerization",
            "description": "Containerize all application services",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=20),
            "estimated_hours": 16,
            "actual_hours": 14,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=20),
            "owner_id": users[4].id,
            "project_id": projects[3].id,
        },
        {
            "title": "Kubernetes deployment",
            "description": "Deploy application to Kubernetes cluster",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=10),
            "estimated_hours": 20,
            "actual_hours": 22,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=10),
            "owner_id": users[4].id,
            "project_id": projects[3].id,
        },
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    
    session.commit()
    print(f"✅ Created {len(tasks)} tasks")
    return tasks

def main():
    """Main function to deploy fixtures."""
    print("🚀 Starting fixture deployment...")
    print(f"📅 Timestamp: {datetime.now()}")
    
    # Create database engine
    database_url = get_database_url()
    print(f"🔗 Database URL: {database_url}")
    
    engine = create_engine(database_url)
    
    # Wait for database to be ready
    if not wait_for_database(engine):
        print("❌ Failed to connect to database")
        sys.exit(1)
    
    # Create tables
    create_tables(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Clear existing data
        clear_existing_data(session)
        
        # Create demo data
        users = create_demo_users(session)
        projects = create_demo_projects(session, users)
        tasks = create_demo_tasks(session, users, projects)
        
        print("\n🎉 Fixtures deployed successfully!")
        print("\n📋 Demo accounts:")
        print("├── Admin: admin@example.com / admin123")
        print("├── Manager: manager@example.com / manager123")
        print("├── User 1: john.doe@example.com / user123")
        print("├── User 2: jane.smith@example.com / user123")
        print("└── Developer: developer@example.com / dev123")
        
        print(f"\n📊 Summary:")
        print(f"├── Users: {len(users)}")
        print(f"├── Projects: {len(projects)}")
        print(f"└── Tasks: {len(tasks)}")
        
    except Exception as e:
        print(f"❌ Error deploying fixtures: {e}")
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    main()