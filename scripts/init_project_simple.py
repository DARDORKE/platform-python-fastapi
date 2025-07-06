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
    print("🚀 INITIALISATION SIMPLE DU PROJET PORTFOLIO PLATFORM")
    print("=" * 80)
    print(f"📅 Date/Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Version Python : {sys.version.split()[0]}")
    print("⚡ Mode : Création directe des tables (sans Alembic)")
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

def create_database_schema(engine):
    """Create database schema without Alembic."""
    print("🔧 Création du schéma de base de données...")
    
    try:
        # Drop and recreate all tables for clean state
        print("🗑️  Suppression des tables existantes...")
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
            "description": "Développement d'une plateforme e-commerce moderne avec React, FastAPI et PostgreSQL. Système complet avec gestion des produits, commandes, paiements Stripe et analytics avancées.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=45),
            "end_date": datetime.now() + timedelta(days=75),
            "budget": 120000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "Mobile App Development",
            "description": "Application mobile React Native pour iOS et Android avec fonctionnalités offline, notifications push et synchronisation cloud.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=10),
            "end_date": datetime.now() + timedelta(days=150),
            "budget": 85000,
            "owner_id": users[1].id,  # Manager
        },
        {
            "name": "API Documentation Portal",
            "description": "Portail de documentation API complet avec guides développeur, exemples interactifs et outils de test automatisés.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() - timedelta(days=20),
            "end_date": datetime.now() + timedelta(days=40),
            "budget": 35000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "DevOps Pipeline",
            "description": "Pipeline CI/CD complet avec Docker, Kubernetes, monitoring Prometheus/Grafana et déploiement automatisé multi-environnements.",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=90),
            "end_date": datetime.now() - timedelta(days=10),
            "budget": 65000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Analytics Dashboard",
            "description": "Tableau de bord analytics en temps réel avec visualisations D3.js, rapports personnalisés et alertes automatiques pour le suivi des KPIs business.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=60),
            "budget": 55000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Security Audit & Compliance",
            "description": "Audit de sécurité complet avec tests de pénétration, analyse des vulnérabilités OWASP, mise en conformité RGPD et recommandations de sécurité.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() + timedelta(days=5),
            "end_date": datetime.now() + timedelta(days=45),
            "budget": 40000,
            "owner_id": users[5].id,  # Tester
        },
        {
            "name": "Microservices Architecture",
            "description": "Refactoring vers une architecture microservices avec API Gateway, service mesh, observabilité et patterns de résilience.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=60),
            "end_date": datetime.now() + timedelta(days=90),
            "budget": 95000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Customer Support Portal",
            "description": "Portail de support client avec chatbot IA, système de tickets, base de connaissances et analytics de satisfaction client.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() + timedelta(days=20),
            "end_date": datetime.now() + timedelta(days=120),
            "budget": 70000,
            "owner_id": users[2].id,  # John Doe
        },
        {
            "name": "Data Warehouse & ETL",
            "description": "Construction d'un data warehouse avec pipelines ETL Apache Airflow, intégration multi-sources et dashboards business intelligence.",
            "status": ProjectStatus.ACTIVE,
            "priority": ProjectPriority.MEDIUM,
            "start_date": datetime.now() - timedelta(days=25),
            "end_date": datetime.now() + timedelta(days=100),
            "budget": 80000,
            "owner_id": users[3].id,  # Jane Smith
        },
        {
            "name": "Machine Learning Platform",
            "description": "Plateforme MLOps complète avec entraînement de modèles, déploiement automatisé, monitoring des performances et A/B testing.",
            "status": ProjectStatus.PLANNING,
            "priority": ProjectPriority.LOW,
            "start_date": datetime.now() + timedelta(days=30),
            "end_date": datetime.now() + timedelta(days=180),
            "budget": 110000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Performance Optimization",
            "description": "Optimisation des performances frontend et backend : lazy loading, CDN, cache Redis, optimisation SQL et monitoring APM.",
            "status": ProjectStatus.COMPLETED,
            "priority": ProjectPriority.HIGH,
            "start_date": datetime.now() - timedelta(days=50),
            "end_date": datetime.now() - timedelta(days=5),
            "budget": 25000,
            "owner_id": users[4].id,  # Developer
        },
        {
            "name": "Multi-tenant SaaS Platform",
            "description": "Transformation en plateforme SaaS multi-tenant avec isolation des données, facturation automatisée et self-service onboarding.",
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
            "description": "Configuration de l'infrastructure AWS avec Terraform : VPC, subnets, ECS, RDS, ElastiCache",
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
            "description": "Implémentation complète du système d'authentification JWT avec refresh tokens, 2FA et gestion des rôles",
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
            "description": "Développement des endpoints REST pour la gestion des produits avec recherche avancée, filtres et pagination",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 40,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Shopping Cart & Checkout",
            "description": "Fonctionnalité de panier d'achat avec persistance Redis, calcul de taxes et processus de commande",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 28,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },
        {
            "title": "Stripe Payment Integration",
            "description": "Intégration complète avec Stripe : paiements, webhooks, remboursements et gestion des échecs",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=42),
            "estimated_hours": 24,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[0].id,
        },
        {
            "title": "Order Management System",
            "description": "Système de gestion des commandes avec tracking, notifications et gestion des retours",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 36,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[0].id,
        },
        {
            "title": "Inventory Management",
            "description": "Gestion des stocks en temps réel avec alertes automatiques et synchronisation multi-canal",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=55),
            "estimated_hours": 32,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[0].id,
        },
        {
            "title": "Analytics & Reporting Dashboard",
            "description": "Tableau de bord avec métriques business, analyses de vente et rapports automatisés",
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
            "description": "Conception de l'architecture React Native avec Redux Toolkit, navigation et gestion d'état",
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
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 36,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[1].id,
        },
        {
            "title": "Push Notifications Setup",
            "description": "Implémentation des notifications push avec Firebase/FCM et gestion des permissions",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 16,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        {
            "title": "Offline Data Synchronization",
            "description": "Système de synchronisation offline avec résolution de conflits et mise en queue",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 48,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[1].id,
        },
        {
            "title": "User Authentication Mobile",
            "description": "Authentification mobile avec biométrie, SSO et gestion sécurisée des tokens",
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
            "description": "Documentation complète des endpoints API avec OpenAPI 3.0, exemples et schémas de validation",
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
            "description": "Portail développeur interactif avec tests d'API en temps réel et génération de code",
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
            "description": "Génération automatique des SDKs Python, JavaScript, Go avec distribution via npm/PyPI",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.LOW,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 32,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[2].id,
        },
        {
            "title": "Developer Onboarding Guide",
            "description": "Guides complets pour développeurs avec tutoriels, exemples pratiques et meilleures pratiques",
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
            "description": "Containerisation avec Docker multi-stage builds, optimisation de taille et sécurité",
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
            "description": "Déploiement sur cluster Kubernetes avec Helm charts, auto-scaling et health checks",
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
            "description": "Pipeline complet avec tests automatisés, sécurité, déploiement et rollback automatique",
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
            "description": "Setup Prometheus, Grafana, AlertManager avec dashboards personnalisés et alertes intelligentes",
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
            "description": "Architecture pipeline de données avec Apache Airflow pour l'ingestion et transformation",
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
            "description": "Graphiques interactifs avec D3.js et mise à jour temps réel via WebSocket",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 35,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[4].id,
        },
        {
            "title": "Custom Report Builder",
            "description": "Constructeur de rapports drag-and-drop avec filtres avancés et export multi-format",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 42,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[4].id,
        },
        {
            "title": "Automated Alert System",
            "description": "Système d'alertes automatiques basé sur des seuils personnalisables et ML",
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
            "description": "Analyse complète des vulnérabilités OWASP Top 10 avec tests automatisés et manuels",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=12),
            "estimated_hours": 24,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Penetration Testing",
            "description": "Tests de pénétration sur l'infrastructure et applications avec rapport détaillé",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 40,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "GDPR Compliance Review",
            "description": "Audit de conformité RGPD avec recommandations et mise en place des mesures",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 32,
            "owner_id": users[5].id,  # Tester
            "project_id": projects[5].id,
        },
        {
            "title": "Security Documentation",
            "description": "Documentation complète des pratiques de sécurité et formation des équipes",
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
            "description": "Analyse et définition de la stratégie de décomposition en microservices",
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
            "description": "Mise en place de l'API Gateway avec routing, rate limiting et authentication",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=20),
            "estimated_hours": 32,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },
        {
            "title": "Service Mesh Setup",
            "description": "Configuration d'Istio pour la communication inter-services et observabilité",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 28,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[6].id,
        },
        {
            "title": "Database per Service",
            "description": "Migration vers une architecture database-per-service avec gestion des transactions",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=50),
            "estimated_hours": 45,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[6].id,
        },
        {
            "title": "Event-Driven Communication",
            "description": "Implémentation de la communication asynchrone avec Apache Kafka",
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
            "description": "Développement d'un chatbot IA avec NLP pour le support client automatisé",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 50,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[7].id,
        },
        {
            "title": "Ticket Management System",
            "description": "Système de gestion des tickets avec workflow personnalisable et SLA tracking",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=35),
            "estimated_hours": 38,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[7].id,
        },
        {
            "title": "Knowledge Base CMS",
            "description": "Système de gestion de contenu pour la base de connaissances avec recherche avancée",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 32,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[7].id,
        },
        {
            "title": "Customer Satisfaction Analytics",
            "description": "Système d'analytics pour mesurer la satisfaction client et générer des insights",
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
            "description": "Conception du schéma dimensionnel pour le data warehouse avec tables de faits et dimensions",
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
            "description": "Développement des pipelines ETL avec Apache Airflow pour l'ingestion multi-sources",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=25),
            "estimated_hours": 40,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[8].id,
        },
        {
            "title": "Data Quality Framework",
            "description": "Framework de qualité des données avec validation, nettoyage et monitoring",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=40),
            "estimated_hours": 30,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[8].id,
        },
        {
            "title": "BI Dashboard Suite",
            "description": "Suite de dashboards business intelligence avec drill-down et export avancé",
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
            "description": "Setup de l'infrastructure MLOps avec MLflow, Kubeflow et model registry",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 40,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "Automated Model Training",
            "description": "Pipeline d'entraînement automatisé avec hyperparameter tuning et validation croisée",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=60),
            "estimated_hours": 45,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "Model Deployment & Serving",
            "description": "Système de déploiement automatisé des modèles avec versioning et rollback",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=80),
            "estimated_hours": 38,
            "owner_id": users[4].id,  # Developer
            "project_id": projects[9].id,
        },
        {
            "title": "A/B Testing Framework",
            "description": "Framework pour A/B testing des modèles ML avec métriques statistiques",
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
            "description": "Audit complet des performances frontend avec Lighthouse et Web Vitals",
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
            "description": "Implémentation du lazy loading pour images, components et routes",
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
            "description": "Mise en place du CDN CloudFront et stratégie de cache Redis optimisée",
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
            "description": "Optimisation des requêtes SQL avec indexation et analyse des performances",
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
            "description": "Conception de l'architecture multi-tenant avec isolation des données et sécurité",
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
            "description": "Système d'onboarding automatisé pour nouveaux tenants avec provisioning",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=30),
            "estimated_hours": 35,
            "owner_id": users[2].id,  # John Doe
            "project_id": projects[11].id,
        },
        {
            "title": "Billing & Subscription Management",
            "description": "Système de facturation automatisée avec gestion des abonnements et métriques d'usage",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.HIGH,
            "due_date": datetime.now() + timedelta(days=45),
            "estimated_hours": 42,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[11].id,
        },
        {
            "title": "Tenant-specific Customization",
            "description": "Système de personnalisation par tenant : thèmes, configurations et branding",
            "status": TaskStatus.TODO,
            "priority": TaskPriority.MEDIUM,
            "due_date": datetime.now() + timedelta(days=60),
            "estimated_hours": 38,
            "owner_id": users[3].id,  # Jane Smith
            "project_id": projects[11].id,
        },
        {
            "title": "Usage Analytics & Reporting",
            "description": "Analytics d'usage par tenant avec rapports détaillés et alertes de seuil",
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
    print(f"✅ {len(tasks)} tâches créées")
    return tasks

def print_summary(users, projects, tasks):
    """Print initialization summary."""
    print("\n" + "=" * 80)
    print("🎉 INITIALISATION SIMPLE TERMINÉE AVEC SUCCÈS")
    print("=" * 80)
    
    print("\n📊 RÉSUMÉ DES DONNÉES CRÉÉES:")
    print(f"├── Utilisateurs : {len(users)}")
    print(f"├── Projets : {len(projects)}")
    print(f"└── Tâches : {len(tasks)}")
    
    # Calculate statistics
    budget_total = sum(p.budget or 0 for p in projects)
    completed_tasks = sum(1 for t in tasks if t.is_completed)
    in_progress_tasks = sum(1 for t in tasks if t.status.value == 'IN_PROGRESS')
    
    print(f"\n💰 STATISTIQUES BUSINESS:")
    print(f"├── Budget total : {budget_total:,}€")
    print(f"├── Tâches terminées : {completed_tasks}")
    print(f"├── Tâches en cours : {in_progress_tasks}")
    print(f"└── Taux de completion : {(completed_tasks/len(tasks)*100):.1f}%")
    
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
    
    # Create database schema
    if not create_database_schema(engine):
        print("❌ Échec de la création du schéma")
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
        print("\n💡 RECOMMANDATION :")
        print("└── Redémarrez le backend pour vider le cache : docker-compose restart backend")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    main()