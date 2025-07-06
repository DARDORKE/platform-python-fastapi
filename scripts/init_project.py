#!/usr/bin/env python3
"""
Script d'initialisation complète du projet.
Génère la structure de la base de données et déploie les fixtures.
"""
import os
import sys
import time
import subprocess
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
    print("🚀 INITIALISATION DU PROJET PORTFOLIO PLATFORM")
    print("=" * 80)
    print(f"📅 Date/Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Version Python : {sys.version.split()[0]}")
    print("=" * 80)

def get_database_url():
    """Get database URL from environment or use default."""
    # Use synchronous driver for initialization
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
    print("⏳ Attente de la connexion à la base de données...")
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données établie")
            return True
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"❌ Base de données non prête (tentative {attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"❌ Échec de connexion après {max_retries} tentatives")
                return False
    return False

def run_migrations(engine):
    """Run database migrations using Alembic."""
    print("🔄 Exécution des migrations Alembic...")
    
    try:
        # Check if alembic is available
        result = subprocess.run(['alembic', '--version'], 
                              capture_output=True, text=True, cwd='/app')
        if result.returncode != 0:
            print("⚠️  Alembic non trouvé, création directe des tables...")
            create_tables_directly(engine)
            return True
            
        # Run migrations
        print("📋 Mise à jour vers la dernière version...")
        result = subprocess.run(['alembic', 'upgrade', 'head'], 
                              capture_output=True, text=True, cwd='/app')
        
        if result.returncode == 0:
            print("✅ Migrations Alembic exécutées avec succès")
            return True
        else:
            print(f"⚠️  Erreur Alembic : {result.stderr}")
            print("🔄 Tentative de création directe des tables...")
            create_tables_directly(engine)
            return True
            
    except Exception as e:
        print(f"⚠️  Erreur lors des migrations : {e}")
        print("🔄 Tentative de création directe des tables...")
        create_tables_directly(engine)
        return True

def create_tables_directly(engine):
    """Create tables directly using SQLAlchemy."""
    print("🔧 Création directe des tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        raise

def check_database_schema(session):
    """Check if database schema is properly initialized."""
    print("🔍 Vérification du schéma de la base de données...")
    
    try:
        # Try to query each table
        session.query(User).first()
        session.query(Project).first()
        session.query(Task).first()
        print("✅ Schéma de la base de données validé")
        return True
    except Exception as e:
        print(f"❌ Problème avec le schéma : {e}")
        return False

def clear_existing_data(session):
    """Clear existing data from tables."""
    print("🗑️  Nettoyage des données existantes...")
    
    try:
        # Delete in reverse order of dependencies
        deleted_tasks = session.query(Task).count()
        deleted_projects = session.query(Project).count()
        deleted_users = session.query(User).count()
        
        session.query(Task).delete()
        session.query(Project).delete()
        session.query(User).delete()
        session.commit()
        
        print(f"✅ Données supprimées : {deleted_users} utilisateurs, {deleted_projects} projets, {deleted_tasks} tâches")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage : {e}")
        session.rollback()
        raise

def create_demo_users(session):
    """Create demo users with comprehensive data."""
    print("👥 Création des utilisateurs de démonstration...")
    
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "full_name": "Administrateur Système",
            "hashed_password": get_password_hash("admin123"),
            "is_active": True,
            "is_superuser": True,
            "role": UserRole.ADMIN,
        },
        {
            "email": "manager@example.com",
            "username": "manager",
            "full_name": "Chef de Projet",
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
            "full_name": "Développeur Senior",
            "hashed_password": get_password_hash("dev123"),
            "is_active": True,
            "role": UserRole.USER,
        },
        {
            "email": "tester@example.com",
            "username": "tester",
            "full_name": "Testeur QA",
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
            "description": "Développement d'une plateforme e-commerce moderne avec React, FastAPI et PostgreSQL. Système complet avec gestion des produits, commandes, paiements et analytics.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=45),
            "end_date": datetime.now() + timedelta(days=75),
            "budget": 85000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "Mobile App Development",
            "description": "Application mobile React Native pour iOS et Android. Interface utilisateur moderne avec fonctionnalités offline, notifications push et synchronisation cloud.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=10),
            "end_date": datetime.now() + timedelta(days=150),
            "budget": 65000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "API Documentation Portal",
            "description": "Portail de documentation API complet avec guides développeur, exemples interactifs et outils de test. Basé sur OpenAPI/Swagger avec personnalisation avancée.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() - timedelta(days=20),
            "end_date": datetime.now() + timedelta(days=40),
            "budget": 25000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "DevOps Pipeline",
            "description": "Pipeline CI/CD complet avec Docker, Kubernetes, monitoring et déploiement automatisé. Incluant tests automatisés, sécurité et observabilité.",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=90),
            "end_date": datetime.now() - timedelta(days=10),
            "budget": 45000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Analytics Dashboard",
            "description": "Tableau de bord analytics en temps réel avec visualisations interactives, rapports personnalisés et alertes automatiques. Intégration avec diverses sources de données.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=60),
            "budget": 40000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Security Audit",
            "description": "Audit de sécurité complet de l'infrastructure et des applications. Tests de pénétration, analyse des vulnérabilités et recommandations de sécurité.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() + timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=35),
            "budget": 30000,
            "owner_id": users[5].id,  # Tester
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
        # E-commerce Platform tasks
        {
            "title": "Setup infrastructure",
            "description": "Configuration de l'infrastructure AWS avec Terraform, mise en place des environnements de dev/staging/prod",
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
            "title": "User authentication system",
            "description": "Implémentation du système d'authentification JWT avec refresh tokens, 2FA et gestion des sessions",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=7),
            "estimated_hours": 32,
            "actual_hours": 24,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Product catalog API",
            "description": "Développement des endpoints REST pour la gestion des produits avec recherche, filtrage et pagination",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 40,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Shopping cart & checkout",
            "description": "Fonctionnalité de panier d'achat avec gestion des sessions Redis et processus de commande complet",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 28,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },
        {
            "title": "Payment integration",
            "description": "Intégration avec Stripe pour les paiements en ligne, gestion des webhooks et réconciliation",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 24,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[0].id,
        },
        
        # Mobile App tasks
        {
            "title": "App architecture design",
            "description": "Conception de l'architecture React Native avec Redux, navigation et gestion d'état",
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
            "description": "Création du système de design avec composants réutilisables, thèmes et guidelines",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 36,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[1].id,
        },
        {
            "title": "Push notifications",
            "description": "Implémentation des notifications push avec Firebase/FCM et gestion des permissions",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 16,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        
        # API Documentation tasks
        {
            "title": "OpenAPI specification",
            "description": "Documentation complète des endpoints API avec OpenAPI 3.0, exemples et schémas",
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
            "title": "Interactive API explorer",
            "description": "Portail développeur interactif avec tests d'API en temps réel et génération de code",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 24,
            "actual_hours": 8,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[2].id,
        },
        {
            "title": "Developer guides",
            "description": "Guides complets pour développeurs avec tutoriels, exemples pratiques et meilleures pratiques",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 18,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[2].id,
        },
        
        # DevOps Pipeline tasks (completed project)
        {
            "title": "Docker containerization",
            "description": "Containerisation complète des services avec Docker multi-stage builds et optimisations",
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
            "title": "Kubernetes deployment",
            "description": "Déploiement sur cluster Kubernetes avec auto-scaling, health checks et rolling updates",
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
            "title": "Monitoring & alerting",
            "description": "Mise en place de Prometheus, Grafana et AlertManager avec dashboards personnalisés",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() - timedelta(days=30),
            "estimated_hours": 20,
            "actual_hours": 18,
            "is_completed": True,
            "completion_date": datetime.now() - timedelta(days=30),
            "owner_id": users[4].id,  # Developer
            "project_id": projects[3].id,
        },
        
        # Analytics Dashboard tasks
        {
            "title": "Data pipeline setup",
            "description": "Pipeline de données avec Apache Airflow pour l'ingestion et transformation des données",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=10),
            "estimated_hours": 30,
            "actual_hours": 20,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[4].id,
        },
        {
            "title": "Real-time visualizations",
            "description": "Graphiques interactifs avec D3.js/Chart.js et mise à jour en temps réel via WebSocket",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 28,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[4].id,
        },
        
        # Security Audit tasks
        {
            "title": "Vulnerability assessment",
            "description": "Scan automatisé des vulnérabilités avec OWASP ZAP et analyse manuelle approfondie",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=12),
            "estimated_hours": 24,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Penetration testing",
            "description": "Tests de pénétration sur l'infrastructure et les applications avec rapport détaillé",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 32,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Security recommendations",
            "description": "Document complet avec recommandations de sécurité et plan d'amélioration",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 16,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
    ]
    
    tasks = []
    for task_data in tasks_data:
        task = Task(**task_data)
        session.add(task)
        tasks.append(task)
    
    session.commit()
    print(f"✅ {len(tasks)} tâches créées")
    return tasks

def print_summary(users, projects, tasks):
    """Print initialization summary."""
    print("\n" + "=" * 80)
    print("🎉 INITIALISATION TERMINÉE AVEC SUCCÈS")
    print("=" * 80)
    
    print("\n📊 RÉSUMÉ DES DONNÉES CRÉÉES:")
    print(f"├── Utilisateurs : {len(users)}")
    print(f"├── Projets : {len(projects)}")
    print(f"└── Tâches : {len(tasks)}")
    
    print("\n🔑 COMPTES DE DÉMONSTRATION:")
    print("├── Admin : admin@example.com / admin123")
    print("├── Manager : manager@example.com / manager123")
    print("├── John Doe : john.doe@example.com / user123")
    print("├── Jane Smith : jane.smith@example.com / user123")
    print("├── Developer : developer@example.com / dev123")
    print("└── Tester : tester@example.com / test123")
    
    print("\n🌐 ACCÈS À L'APPLICATION:")
    print("├── Frontend : http://localhost:3000")
    print("├── API Backend : http://localhost:8000")
    print("├── Documentation API : http://localhost:8000/docs")
    print("└── Alternative docs : http://localhost:8000/redoc")
    
    print("\n🧪 TESTS RAPIDES:")
    print("├── Connexion : curl -X POST http://localhost:8000/api/v1/auth/login/json \\")
    print("│                -H 'Content-Type: application/json' \\")
    print("│                -d '{\"email\":\"admin@example.com\",\"password\":\"admin123\"}'")
    print("├── Projets : curl http://localhost:8000/api/v1/projects")
    print("└── Tâches : curl http://localhost:8000/api/v1/tasks")
    
    print("\n" + "=" * 80)
    print("🚀 PROJET PRÊT POUR LE DÉVELOPPEMENT !")
    print("=" * 80)

def main():
    """Main initialization function."""
    print_banner()
    
    # Get database configuration
    database_url = get_database_url()
    print(f"🔗 URL de la base de données : {database_url}")
    
    # Create database engine
    engine = create_engine(database_url)
    
    # Wait for database to be ready
    if not wait_for_database(engine):
        print("❌ Impossible de se connecter à la base de données")
        sys.exit(1)
    
    # Run migrations or create tables
    if not run_migrations(engine):
        print("❌ Échec de l'initialisation du schéma")
        sys.exit(1)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verify database schema
        if not check_database_schema(session):
            print("❌ Schéma de la base de données invalide")
            sys.exit(1)
        
        # Clear existing data
        clear_existing_data(session)
        
        # Create demo data
        users = create_demo_users(session)
        projects = create_demo_projects(session, users)
        tasks = create_demo_tasks(session, users, projects)
        
        # Print summary
        print_summary(users, projects, tasks)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    main()