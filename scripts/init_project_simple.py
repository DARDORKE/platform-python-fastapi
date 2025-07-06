#!/usr/bin/env python3
"""
Script d'initialisation simple sans Alembic.
Création directe des tables et déploiement des fixtures.
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

def print_banner():
    """Print initialization banner."""
    print("=" * 80)
    print("🚀 SIMPLE INITIALIZATION OF PORTFOLIO PLATFORM PROJECT")
    print("=" * 80)
    print(f"📅 Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print("⚡ Mode: Direct table creation (without Alembic)")
    print("=" * 80)

def get_database_url():
    """Get database URL from environment or use default."""
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
                print(f"❌ Database not ready (attempt {attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"❌ Connection failed after {max_retries} attempts")
                return False
    return False

def create_database_schema(engine):
    """Create database schema without Alembic."""
    print("🔧 Creating database schema...")
    
    try:
        # Drop and recreate all tables for clean state
        print("🗑️  Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("🏗️  Création des nouvelles tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Schéma de base de données créé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du schéma : {e}")
        return False

def create_demo_users(session):
    """Create demo users with comprehensive data."""
    print("👥 Création des utilisateurs de démonstration...")
    
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "full_name": "System Administrator",
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
        {
            "email": "tester@example.com",
            "username": "tester",
            "full_name": "QA Tester",
            "hashed_password": get_password_hash("test123"),
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
    print(f"✅ {len(users)} utilisateurs créés")
    return users

def create_demo_projects(session, users):
    """Create demo projects with realistic data."""
    print("📁 Création des projets de démonstration...")
    
    projects_data = [
        {
            "name": "E-commerce Platform",
            "description": "Development of a modern e-commerce platform with React, FastAPI and PostgreSQL. Complete system with product management, orders, Stripe payments and advanced analytics.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=45),
            "end_date": datetime.now() + timedelta(days=75),
            "budget": 120000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "Mobile App Development",
            "description": "React Native mobile application for iOS and Android with offline features, push notifications and cloud synchronization.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=10),
            "end_date": datetime.now() + timedelta(days=150),
            "budget": 85000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "API Documentation Portal",
            "description": "Complete API documentation portal with developer guides, interactive examples and automated testing tools.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() - timedelta(days=20),
            "end_date": datetime.now() + timedelta(days=40),
            "budget": 35000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "DevOps Pipeline",
            "description": "Complete CI/CD pipeline with Docker, Kubernetes, Prometheus/Grafana monitoring and automated multi-environment deployment.",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=90),
            "end_date": datetime.now() - timedelta(days=10),
            "budget": 65000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Analytics Dashboard",
            "description": "Real-time analytics dashboard with D3.js visualizations, custom reports and automatic alerts for business KPI tracking.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=60),
            "budget": 55000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Security Audit & Compliance",
            "description": "Complete security audit with penetration testing, OWASP vulnerability analysis, GDPR compliance and security recommendations.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() + timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=45),
            "budget": 40000,
            "owner_id": users[5].id,  # Tester
        },
        {
            "name": "Microservices Architecture",
            "description": "Refactoring to microservices architecture with API Gateway, service mesh, observability and resilience patterns.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": datetime.now() + timedelta(days=90),
            "budget": 95000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Customer Support Portal",
            "description": "Customer support portal with AI chatbot, ticket system, knowledge base and customer satisfaction analytics.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=20),
            "end_date": datetime.now() + timedelta(days=120),
            "budget": 70000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "Data Warehouse & ETL",
            "description": "Data warehouse construction with Apache Airflow ETL pipelines, multi-source integration and business intelligence dashboards.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=25),
            "end_date": datetime.now() + timedelta(days=100),
            "budget": 80000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Machine Learning Platform",
            "description": "Complete MLOps platform with model training, automated deployment, performance monitoring and A/B testing.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() + timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=180),
            "budget": 110000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Performance Optimization",
            "description": "Frontend and backend performance optimization: lazy loading, CDN, Redis cache, SQL optimization and APM monitoring.",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=50),
            "end_date": datetime.now() - timedelta(days=5),
            "budget": 25000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Multi-tenant SaaS Platform",
            "description": "Transformation into multi-tenant SaaS platform with data isolation, automated billing and self-service onboarding.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=35),
            "end_date": datetime.now() + timedelta(days=110),
            "budget": 140000,
            "owner_id": users[1].id,  # Manager
        },
    ]
    
    projects = []
    for project_data in projects_data:
        project = Project(**project_data)
        session.add(project)
        projects.append(project)
    
    session.commit()
    print(f"✅ {len(projects)} projets créés")
    return projects

def create_demo_tasks(session, users, projects):
    """Create demo tasks with realistic workflow."""
    print("📝 Création des tâches de démonstration...")
    
    tasks_data = [
        # E-commerce Platform tasks (project[0])
        {
            "title": "Setup AWS infrastructure",
            "description": "AWS infrastructure configuration with Terraform: VPC, subnets, ECS, RDS, ElastiCache",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=40),
            "estimated_hours": 16,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=40),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[0].id,
        },
        {
            "title": "JWT Authentication System",
            "description": "Complete JWT authentication system implementation with refresh tokens, 2FA and role management",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=7),
            "estimated_hours": 32,
            "actual_hours": 24,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Product Catalog API",
            "description": "REST endpoints development for product management with advanced search, filters and pagination",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 40,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Shopping Cart & Checkout",
            "description": "Shopping cart functionality with Redis persistence, tax calculation and order process",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 28,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },
        {
            "title": "Stripe Payment Integration",
            "description": "Complete Stripe integration: payments, webhooks, refunds and failure handling",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=42),
            "estimated_hours": 24,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[0].id,
        },
        {
            "title": "Order Management System",
            "description": "Order management system with tracking, notifications and returns handling",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 36,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },
        {
            "title": "Inventory Management",
            "description": "Real-time inventory management with automatic alerts and multi-channel synchronization",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=55),
            "estimated_hours": 32,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Analytics & Reporting Dashboard",
            "description": "Dashboard with business metrics, sales analytics and automated reports",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=65),
            "estimated_hours": 40,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },

        # Mobile App Development tasks (project[1])
        {
            "title": "React Native Architecture",
            "description": "React Native architecture design with Redux Toolkit, navigation and state management",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=15),
            "estimated_hours": 20,
            "actual_hours": 12,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        {
            "title": "UI/UX Design System",
            "description": "Design system creation with reusable components, themes and guidelines",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 36,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[1].id,
        },
        {
            "title": "Push Notifications Setup",
            "description": "Push notifications implementation with Firebase/FCM and permissions management",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 16,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        {
            "title": "Offline Data Synchronization",
            "description": "Offline synchronization system with conflict resolution and queuing",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 48,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        {
            "title": "User Authentication Mobile",
            "description": "Mobile authentication with biometrics, SSO and secure token management",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 28,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[1].id,
        },

        # API Documentation Portal tasks (project[2])
        {
            "title": "OpenAPI 3.0 Specification",
            "description": "Complete API endpoints documentation with OpenAPI 3.0, examples and validation schemas",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() - timedelta(days=15),
            "estimated_hours": 20,
            "actual_hours": 22,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=15),
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[2].id,
        },
        {
            "title": "Interactive API Explorer",
            "description": "Interactive developer portal with real-time API testing and code generation",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 24,
            "actual_hours": 8,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[2].id,
        },
        {
            "title": "SDK Generation & Distribution",
            "description": "Automatic SDK generation for Python, JavaScript, Go with distribution via npm/PyPI",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 32,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[2].id,
        },
        {
            "title": "Developer Onboarding Guide",
            "description": "Complete developer guides with tutorials, practical examples and best practices",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=38),
            "estimated_hours": 18,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[2].id,
        },

        # DevOps Pipeline tasks (project[3]) - COMPLETED
        {
            "title": "Docker Multi-stage Build",
            "description": "Containerization with Docker multi-stage builds, size optimization and security",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=80),
            "estimated_hours": 24,
            "actual_hours": 26,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=80),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[3].id,
        },
        {
            "title": "Kubernetes Deployment",
            "description": "Kubernetes cluster deployment with Helm charts, auto-scaling and health checks",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=60),
            "estimated_hours": 32,
            "actual_hours": 35,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=60),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[3].id,
        },
        {
            "title": "CI/CD Pipeline GitHub Actions",
            "description": "Complete pipeline with automated tests, security, deployment and automatic rollback",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=45),
            "estimated_hours": 28,
            "actual_hours": 30,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=45),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[3].id,
        },
        {
            "title": "Monitoring & Alerting",
            "description": "Setup Prometheus, Grafana, AlertManager with custom dashboards and intelligent alerts",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() - timedelta(days=25),
            "estimated_hours": 20,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=25),
            "owner_id": users[5].id,  # Tester
            "project_id": projects[3].id,
        },

        # Analytics Dashboard tasks (project[4])
        {
            "title": "Data Pipeline Architecture",
            "description": "Data pipeline architecture with Apache Airflow for ingestion and transformation",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 30,
            "actual_hours": 20,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[4].id,
        },
        {
            "title": "Real-time Data Visualization",
            "description": "Interactive charts with D3.js and real-time updates via WebSocket",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 35,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[4].id,
        },
        {
            "title": "Custom Report Builder",
            "description": "Drag-and-drop report builder with advanced filters and multi-format export",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 42,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[4].id,
        },
        {
            "title": "Automated Alert System",
            "description": "Automatic alert system based on customizable thresholds and ML",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 24,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[4].id,
        },

        # Security Audit & Compliance tasks (project[5])
        {
            "title": "OWASP Security Assessment",
            "description": "Complete OWASP Top 10 vulnerability analysis with automated and manual tests",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=12),
            "estimated_hours": 24,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Penetration Testing",
            "description": "Penetration testing on infrastructure and applications with detailed report",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 40,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "GDPR Compliance Review",
            "description": "GDPR compliance audit with recommendations and implementation of measures",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 32,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Security Documentation",
            "description": "Complete documentation of security practices and team training",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 16,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },

        # Microservices Architecture tasks (project[6])
        {
            "title": "Service Decomposition Strategy",
            "description": "Analysis and definition of microservices decomposition strategy",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=5),
            "estimated_hours": 20,
            "actual_hours": 15,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },
        {
            "title": "API Gateway Implementation",
            "description": "API Gateway implementation with routing, rate limiting and authentication",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 32,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },
        {
            "title": "Service Mesh Setup",
            "description": "Istio configuration for inter-service communication and observability",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 28,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },
        {
            "title": "Database per Service",
            "description": "Migration to database-per-service architecture with transaction management",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 45,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[6].id,
        },
        {
            "title": "Event-Driven Communication",
            "description": "Asynchronous communication implementation with Apache Kafka",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=60),
            "estimated_hours": 36,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },

        # Customer Support Portal tasks (project[7])
        {
            "title": "Chatbot AI Development",
            "description": "AI chatbot development with NLP for automated customer support",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 50,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[7].id,
        },
        {
            "title": "Ticket Management System",
            "description": "Ticket management system with customizable workflow and SLA tracking",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 38,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[7].id,
        },
        {
            "title": "Knowledge Base CMS",
            "description": "Content management system for knowledge base with advanced search",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 32,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[7].id,
        },
        {
            "title": "Customer Satisfaction Analytics",
            "description": "Analytics system to measure customer satisfaction and generate insights",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=70),
            "estimated_hours": 25,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[7].id,
        },

        # Data Warehouse & ETL tasks (project[8])
        {
            "title": "Data Warehouse Schema Design",
            "description": "Dimensional schema design for data warehouse with fact and dimension tables",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=8),
            "estimated_hours": 25,
            "actual_hours": 18,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[8].id,
        },
        {
            "title": "ETL Pipeline with Airflow",
            "description": "ETL pipeline development with Apache Airflow for multi-source ingestion",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 40,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[8].id,
        },
        {
            "title": "Data Quality Framework",
            "description": "Data quality framework with validation, cleaning and monitoring",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 30,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[8].id,
        },
        {
            "title": "BI Dashboard Suite",
            "description": "Business intelligence dashboard suite with drill-down and advanced export",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=65),
            "estimated_hours": 35,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[8].id,
        },

        # Machine Learning Platform tasks (project[9])
        {
            "title": "MLOps Infrastructure Setup",
            "description": "MLOps infrastructure setup with MLflow, Kubeflow and model registry",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 40,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "Automated Model Training",
            "description": "Automated training pipeline with hyperparameter tuning and cross-validation",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=60),
            "estimated_hours": 45,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "Model Deployment & Serving",
            "description": "Automated model deployment system with versioning and rollback",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=80),
            "estimated_hours": 38,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "A/B Testing Framework",
            "description": "Framework for A/B testing ML models with statistical metrics",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=100),
            "estimated_hours": 32,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[9].id,
        },

        # Performance Optimization tasks (project[10]) - COMPLETED
        {
            "title": "Frontend Performance Audit",
            "description": "Complete frontend performance audit with Lighthouse and Web Vitals",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=45),
            "estimated_hours": 12,
            "actual_hours": 14,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=45),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[10].id,
        },
        {
            "title": "Lazy Loading Implementation",
            "description": "Lazy loading implementation for images, components and routes",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=35),
            "estimated_hours": 16,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=35),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[10].id,
        },
        {
            "title": "CDN & Caching Strategy",
            "description": "CloudFront CDN setup and optimized Redis cache strategy",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() - timedelta(days=25),
            "estimated_hours": 14,
            "actual_hours": 12,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=25),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[10].id,
        },
        {
            "title": "Database Query Optimization",
            "description": "SQL query optimization with indexing and performance analysis",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() - timedelta(days=15),
            "estimated_hours": 20,
            "actual_hours": 22,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=15),
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[10].id,
        },

        # Multi-tenant SaaS Platform tasks (project[11])
        {
            "title": "Multi-tenancy Architecture Design",
            "description": "Multi-tenant architecture design with data isolation and security",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=15),
            "estimated_hours": 30,
            "actual_hours": 22,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[11].id,
        },
        {
            "title": "Tenant Onboarding System",
            "description": "Automated onboarding system for new tenants with provisioning",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 35,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[11].id,
        },
        {
            "title": "Billing & Subscription Management",
            "description": "Automated billing system with subscription management and usage metrics",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 42,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[11].id,
        },
        {
            "title": "Tenant-specific Customization",
            "description": "Per-tenant customization system: themes, configurations and branding",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=60),
            "estimated_hours": 38,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[11].id,
        },
        {
            "title": "Usage Analytics & Reporting",
            "description": "Per-tenant usage analytics with detailed reports and threshold alerts",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=75),
            "estimated_hours": 28,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[11].id,
        },
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    
    session.commit()
    print(f"✅ {len(tasks)} tasks created")
    return tasks

def print_summary(users, projects, tasks):
    """Print initialization summary."""
    print("\n" + "=" * 80)
    print("🎉 SIMPLE INITIALIZATION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    print("\n📊 SUMMARY OF CREATED DATA:")
    print(f"├── Users: {len(users)}")
    print(f"├── Projects: {len(projects)}")
    print(f"└── Tasks: {len(tasks)}")
    
    # Calculate statistics
    budget_total = sum(p.budget or 0 for p in projects)
    completed_tasks = sum(1 for t in tasks if t.is_completed)
    in_progress_tasks = sum(1 for t in tasks if t.status.value == 'IN_PROGRESS')
    
    print(f"\n💰 BUSINESS STATISTICS:")
    print(f"├── Total budget: €{budget_total:,}")
    print(f"├── Completed tasks: {completed_tasks}")
    print(f"├── In progress tasks: {in_progress_tasks}")
    print(f"└── Completion rate: {(completed_tasks/len(tasks)*100):.1f}%")
    
    print("\n🔑 DEMO ACCOUNTS:")
    print("├── Admin : admin@example.com / admin123")
    print("├── Manager : manager@example.com / manager123")
    print("├── John Doe : john.doe@example.com / user123")
    print("├── Jane Smith : jane.smith@example.com / user123")
    print("├── Developer : developer@example.com / dev123")
    print("└── Tester : tester@example.com / test123")
    
    print("\n🌐 APPLICATION ACCESS:")
    print("├── Frontend : http://localhost:3000")
    print("├── API Backend : http://localhost:8000")
    print("├── Documentation API : http://localhost:8000/docs")
    print("└── Alternative docs : http://localhost:8000/redoc")
    
    print("\n" + "=" * 80)
    print("🚀 PROJECT READY FOR DEVELOPMENT!")
    print("=" * 80)

def main():
    """Main initialization function."""
    print_banner()
    
    # Get database configuration
    database_url = get_database_url()
    print(f"🔗 Database URL: {database_url}")
    
    # Create database engine
    engine = create_engine(database_url)
    
    # Wait for database to be ready
    if not wait_for_database(engine):
        print("❌ Unable to connect to database")
        sys.exit(1)
    
    # Create database schema
    if not create_database_schema(engine):
        print("❌ Schema creation failed")
        sys.exit(1)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create demo data
        users = create_demo_users(session)
        projects = create_demo_projects(session, users)
        tasks = create_demo_tasks(session, users, projects)
        
        # Print summary
        print_summary(users, projects, tasks)
        
        # Recommend backend restart for cache clearing
        print("\n💡 RECOMMENDATION:")
        print("└── Restart backend to clear cache: docker-compose restart backend")
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    main()