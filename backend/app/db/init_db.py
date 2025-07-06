"""
Initial database setup with demo data.
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus, ProjectPriority
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash


async def create_demo_users(db: AsyncSession) -> list[User]:
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
        db.add(user)
        users.append(user)
    
    await db.commit()
    
    # Refresh to get IDs
    for user in users:
        await db.refresh(user)
    
    return users


async def create_demo_projects(db: AsyncSession, users: list[User]) -> list[Project]:
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
        {
            "name": "Data Analytics Dashboard",
            "description": "Real-time analytics dashboard with charts and metrics",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=90),
            "end_date": datetime.now() - timedelta(days=15),
            "budget": 25000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Security Audit",
            "description": "Comprehensive security audit and penetration testing",
            "status": ProjectStatus.ON_HOLD,
            "priority": ProjectPriority.URGENT,
            "start_date": datetime.now() - timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=45),
            "budget": 20000,
            "owner_id": users[1].id,  # Manager
        },
    ]
    
    projects = []
    for project_data in projects_data:
        project = Project(**project_data)
        db.add(project)
        projects.append(project)
    
    await db.commit()
    
    # Refresh to get IDs
    for project in projects:
        await db.refresh(project)
    
    return projects


async def create_demo_tasks(db: AsyncSession, users: list[User], projects: list[Project]) -> list[Task]:
    """Create demo tasks."""
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
            "title": "Design database schema",
            "description": "Create ERD and define database tables for the e-commerce platform",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=20),
            "estimated_hours": 16,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=18),
            "owner_id": users[3].id,
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
            "description": "Implement shopping cart with session management",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 20,
            "owner_id": users[3].id,
            "project_id": projects[0].id,
        },
        
        # Mobile App Development tasks
        {
            "title": "Market research",
            "description": "Research competitor apps and user requirements",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() - timedelta(days=5),
            "estimated_hours": 16,
            "actual_hours": 14,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=3),
            "owner_id": users[1].id,
            "project_id": projects[1].id,
        },
        {
            "title": "UI/UX Design",
            "description": "Create wireframes and mockups for mobile app",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 40,
            "actual_hours": 24,
            "owner_id": users[3].id,
            "project_id": projects[1].id,
        },
        
        # API Documentation tasks
        {
            "title": "API endpoint documentation",
            "description": "Document all REST API endpoints with examples",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 30,
            "actual_hours": 12,
            "owner_id": users[2].id,
            "project_id": projects[2].id,
        },
        {
            "title": "Setup developer portal",
            "description": "Create interactive documentation portal",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 16,
            "owner_id": users[2].id,
            "project_id": projects[2].id,
        },
        
        # Data Analytics Dashboard tasks (completed project)
        {
            "title": "Data visualization components",
            "description": "Create reusable chart components with D3.js",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=50),
            "estimated_hours": 40,
            "actual_hours": 38,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=45),
            "owner_id": users[3].id,
            "project_id": projects[3].id,
        },
        {
            "title": "Real-time data integration",
            "description": "Implement WebSocket connection for live data updates",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=30),
            "estimated_hours": 24,
            "actual_hours": 28,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=25),
            "owner_id": users[3].id,
            "project_id": projects[3].id,
        },
        
        # Security Audit tasks
        {
            "title": "Vulnerability assessment",
            "description": "Automated security scanning and vulnerability assessment",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.URGENT,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 20,
            "owner_id": users[1].id,
            "project_id": projects[4].id,
        },
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        db.add(task)
        tasks.append(task)
    
    await db.commit()
    
    # Refresh to get IDs
    for task in tasks:
        await db.refresh(task)
    
    return tasks


async def init_db():
    """Initialize database with demo data."""
    print("🌱 Initializing database with demo data...")
    
    async with async_session() as db:
        try:
            # Create users
            print("👥 Creating demo users...")
            users = await create_demo_users(db)
            print(f"✅ Created {len(users)} users")
            
            # Create projects
            print("📁 Creating demo projects...")
            projects = await create_demo_projects(db, users)
            print(f"✅ Created {len(projects)} projects")
            
            # Create tasks
            print("📝 Creating demo tasks...")
            tasks = await create_demo_tasks(db, users, projects)
            print(f"✅ Created {len(tasks)} tasks")
            
            print("🎉 Database initialization completed successfully!")
            print("\n📋 Demo accounts:")
            print("Admin: admin@example.com / admin123")
            print("Manager: manager@example.com / manager123")
            print("User 1: john.doe@example.com / user123")
            print("User 2: jane.smith@example.com / user123")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(init_db())