"""
Load demo data using synchronous database connection.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, ProjectPriority
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash

# Create synchronous engine
engine = create_engine("postgresql://platform_user:platform_password@database:5432/platform")
Session = sessionmaker(bind=engine)

def create_demo_users(session) -> list[User]:
    """Create demo users."""
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
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        session.add(user)
        users.append(user)
    
    session.commit()
    return users

def create_demo_projects(session, users: list[User]) -> list[Project]:
    """Create demo projects."""
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
    ]
    
    projects = []
    for project_data in projects_data:
        project = Project(**project_data)
        session.add(project)
        projects.append(project)
    
    session.commit()
    return projects

def create_demo_tasks(session, users: list[User], projects: list[Project]) -> list[Task]:
    """Create demo tasks."""
    tasks_data = [
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
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    
    session.commit()
    return tasks

def main():
    """Load demo data."""
    print("🌱 Loading demo data...")
    
    session = Session()
    try:
        # Create users
        print("👥 Creating demo users...")
        users = create_demo_users(session)
        print(f"✅ Created {len(users)} users")
        
        # Create projects
        print("📁 Creating demo projects...")
        projects = create_demo_projects(session, users)
        print(f"✅ Created {len(projects)} projects")
        
        # Create tasks
        print("📝 Creating demo tasks...")
        tasks = create_demo_tasks(session, users, projects)
        print(f"✅ Created {len(tasks)} tasks")
        
        print("🎉 Demo data loaded successfully!")
        print("\n📋 Demo accounts:")
        print("Admin: admin@example.com / admin123")
        print("Manager: manager@example.com / manager123")
        print("User 1: john.doe@example.com / user123")
        print("User 2: jane.smith@example.com / user123")
        
    except Exception as e:
        print(f"❌ Error loading demo data: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    main()