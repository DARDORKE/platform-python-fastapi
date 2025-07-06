# Makefile pour Plateforme Python FastAPI

.DEFAULT_GOAL := help
.PHONY: help dev-start dev-stop install-all test-all

# Variables
DOCKER_COMPOSE = docker-compose
BACKEND_CONTAINER = backend
FRONTEND_CONTAINER = platform_frontend
DATABASE_CONTAINER = platform_database
WORKER_CONTAINER = platform_worker

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m

help: ## Affiche l'aide
	@echo "$(GREEN)Plateforme Python FastAPI - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'

# Développement
dev-start: ## Démarre l'environnement de développement
	@echo "$(GREEN)🚀 Démarrage de l'environnement de développement...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Environnement démarré!$(NC)"
	@echo "$(BLUE)API: http://localhost:8000$(NC)"
	@echo "$(BLUE)Frontend: http://localhost:3000$(NC)"
	@echo "$(BLUE)Docs: http://localhost:8000/docs$(NC)"
	@echo "$(BLUE)Flower: http://localhost:5555$(NC)"
	@echo "$(BLUE)Grafana: http://localhost:3001$(NC)"

dev-stop: ## Arrête l'environnement de développement
	@echo "$(YELLOW)🔄 Arrêt de l'environnement...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Environnement arrêté!$(NC)"

dev-restart: ## Redémarre l'environnement
	@echo "$(YELLOW)🔄 Redémarrage de l'environnement...$(NC)"
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✅ Environnement redémarré!$(NC)"

dev-logs: ## Affiche les logs de tous les services
	$(DOCKER_COMPOSE) logs -f

dev-logs-backend: ## Affiche les logs du backend
	$(DOCKER_COMPOSE) logs -f $(BACKEND_CONTAINER)

dev-logs-frontend: ## Affiche les logs du frontend
	$(DOCKER_COMPOSE) logs -f $(FRONTEND_CONTAINER)

dev-logs-worker: ## Affiche les logs du worker
	$(DOCKER_COMPOSE) logs -f $(WORKER_CONTAINER)

# Installation
install-all: ## Installe toutes les dépendances
	@echo "$(GREEN)📦 Installation des dépendances...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pip install -r requirements.txt
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm install
	@echo "$(GREEN)✅ Dépendances installées!$(NC)"

install-backend: ## Installe les dépendances backend
	@echo "$(GREEN)📦 Installation des dépendances backend...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pip install -r requirements.txt
	@echo "$(GREEN)✅ Dépendances backend installées!$(NC)"

install-frontend: ## Installe les dépendances frontend
	@echo "$(GREEN)📦 Installation des dépendances frontend...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm install
	@echo "$(GREEN)✅ Dépendances frontend installées!$(NC)"

# Base de données
db-migrate: ## Exécute les migrations
	@echo "$(GREEN)🗄️ Exécution des migrations...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) alembic upgrade head
	@echo "$(GREEN)✅ Migrations exécutées!$(NC)"

db-rollback: ## Rollback de la dernière migration
	@echo "$(YELLOW)🔄 Rollback de la dernière migration...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) alembic downgrade -1
	@echo "$(GREEN)✅ Rollback effectué!$(NC)"

db-seed: ## Charge les données de test
	@echo "$(GREEN)🌱 Chargement des données de test...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) python -m app.db.init_db
	@echo "$(GREEN)✅ Données de test chargées!$(NC)"

fixtures: ## Déploie les fixtures (données de démonstration)
	@echo "$(GREEN)🚀 Déploiement des fixtures...$(NC)"
	@chmod +x scripts/deploy_fixtures.sh
	@./scripts/deploy_fixtures.sh
	@echo "$(GREEN)✅ Fixtures déployées!$(NC)"

init: ## Initialise complètement le projet (BDD + fixtures)
	@echo "$(GREEN)🚀 Initialisation complète du projet...$(NC)"
	@chmod +x scripts/init_project.sh
	@./scripts/init_project.sh
	@echo "$(GREEN)✅ Projet initialisé!$(NC)"

quick-init: ## Initialise le projet sans confirmation
	@echo "$(GREEN)🚀 Initialisation rapide du projet...$(NC)"
	@chmod +x scripts/init_project.sh
	@./scripts/init_project.sh --yes
	@echo "$(GREEN)✅ Projet initialisé!$(NC)"

init-simple: ## Initialise le projet sans Alembic (création directe)
	@echo "$(GREEN)🚀 Initialisation simple du projet (sans Alembic)...$(NC)"
	@$(DOCKER_COMPOSE) exec -T $(BACKEND_CONTAINER) python /app/scripts/init_project_simple.py
	@echo "$(GREEN)✅ Projet initialisé!$(NC)"

db-reset: ## Remet à zéro la base de données
	@echo "$(YELLOW)⚠️ Remise à zéro de la base de données...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) alembic downgrade base
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) alembic upgrade head
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) python -m app.db.init_db
	@echo "$(GREEN)✅ Base de données remise à zéro!$(NC)"

db-shell: ## Ouvre un shell PostgreSQL
	$(DOCKER_COMPOSE) exec $(DATABASE_CONTAINER) psql -U platform_user -d platform

# Tests
test-all: ## Lance tous les tests
	@echo "$(GREEN)🧪 Lancement de tous les tests...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run test:ci
	@echo "$(GREEN)✅ Tests terminés!$(NC)"

test-backend: ## Lance les tests backend
	@echo "$(GREEN)🧪 Lancement des tests backend...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest -v
	@echo "$(GREEN)✅ Tests backend terminés!$(NC)"

test-frontend: ## Lance les tests frontend
	@echo "$(GREEN)🧪 Lancement des tests frontend...$(NC)"
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run test:ci
	@echo "$(GREEN)✅ Tests frontend terminés!$(NC)"

test-coverage: ## Génère les rapports de couverture
	@echo "$(GREEN)📊 Génération des rapports de couverture...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest --cov=app --cov-report=html
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run test:coverage
	@echo "$(GREEN)✅ Rapports de couverture générés!$(NC)"

test-integration: ## Lance les tests d'intégration
	@echo "$(GREEN)🧪 Lancement des tests d'intégration...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/integration/
	@echo "$(GREEN)✅ Tests d'intégration terminés!$(NC)"

test-performance: ## Lance les tests de performance
	@echo "$(GREEN)⚡ Lancement des tests de performance...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) pytest tests/performance/
	@echo "$(GREEN)✅ Tests de performance terminés!$(NC)"

# Qualité de code
lint: ## Vérifie la qualité du code
	@echo "$(GREEN)🔍 Vérification de la qualité du code...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) flake8 app/
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) mypy app/
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run lint
	@echo "$(GREEN)✅ Vérification terminée!$(NC)"

format: ## Formate le code
	@echo "$(GREEN)✨ Formatage du code...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) black app/
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) isort app/
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm run format
	@echo "$(GREEN)✅ Code formaté!$(NC)"

security-scan: ## Scan de sécurité
	@echo "$(GREEN)🔒 Scan de sécurité...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) bandit -r app/
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) npm audit
	@echo "$(GREEN)✅ Scan de sécurité terminé!$(NC)"

# Utilitaires
shell-backend: ## Ouvre un shell dans le backend
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) bash

shell-frontend: ## Ouvre un shell dans le frontend
	$(DOCKER_COMPOSE) exec $(FRONTEND_CONTAINER) bash

shell-database: ## Ouvre un shell dans la base de données
	$(DOCKER_COMPOSE) exec $(DATABASE_CONTAINER) bash

status: ## Affiche le statut des services
	@echo "$(GREEN)📊 Statut des services:$(NC)"
	$(DOCKER_COMPOSE) ps

clean: ## Nettoie les volumes et containers
	@echo "$(YELLOW)🧹 Nettoyage...$(NC)"
	$(DOCKER_COMPOSE) down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)✅ Nettoyage terminé!$(NC)"

# Backup et restauration
backup-db: ## Sauvegarde la base de données
	@echo "$(GREEN)💾 Sauvegarde de la base de données...$(NC)"
	$(DOCKER_COMPOSE) exec $(DATABASE_CONTAINER) pg_dump -U platform_user platform > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Sauvegarde terminée!$(NC)"

restore-db: ## Restaure la base de données (usage: make restore-db FILE=backup.sql)
	@echo "$(GREEN)🔄 Restauration de la base de données...$(NC)"
	$(DOCKER_COMPOSE) exec -T $(DATABASE_CONTAINER) psql -U platform_user platform < $(FILE)
	@echo "$(GREEN)✅ Restauration terminée!$(NC)"

# Monitoring
monitoring-start: ## Démarre le monitoring
	@echo "$(GREEN)📈 Démarrage du monitoring...$(NC)"
	$(DOCKER_COMPOSE) up -d prometheus grafana
	@echo "$(GREEN)✅ Monitoring démarré!$(NC)"
	@echo "$(BLUE)Prometheus: http://localhost:9090$(NC)"
	@echo "$(BLUE)Grafana: http://localhost:3001 (admin/admin)$(NC)"

monitoring-stop: ## Arrête le monitoring
	@echo "$(YELLOW)🔄 Arrêt du monitoring...$(NC)"
	$(DOCKER_COMPOSE) stop prometheus grafana
	@echo "$(GREEN)✅ Monitoring arrêté!$(NC)"

# Production
build: ## Build les images pour la production
	@echo "$(GREEN)🏗️ Build des images...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✅ Images construites!$(NC)"

deploy-staging: ## Déploie en staging
	@echo "$(GREEN)🚀 Déploiement en staging...$(NC)"
	$(DOCKER_COMPOSE) -f docker-compose.staging.yml up -d
	@echo "$(GREEN)✅ Déploiement staging terminé!$(NC)"

deploy-production: ## Déploie en production
	@echo "$(GREEN)🚀 Déploiement en production...$(NC)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✅ Déploiement production terminé!$(NC)"

# Documentation
docs-serve: ## Démarre la documentation
	@echo "$(GREEN)📚 Démarrage de la documentation...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) mkdocs serve -a 0.0.0.0:8080
	@echo "$(BLUE)Documentation: http://localhost:8080$(NC)"

docs-build: ## Build la documentation
	@echo "$(GREEN)📚 Build de la documentation...$(NC)"
	$(DOCKER_COMPOSE) exec $(BACKEND_CONTAINER) mkdocs build
	@echo "$(GREEN)✅ Documentation construite!$(NC)"

# Développement mobile
mobile-expo: ## Démarre Expo pour le mobile
	@echo "$(GREEN)📱 Démarrage d'Expo...$(NC)"
	cd mobile && npm start
	@echo "$(BLUE)Expo DevTools: http://localhost:19002$(NC)"

mobile-build-ios: ## Build iOS
	@echo "$(GREEN)📱 Build iOS...$(NC)"
	cd mobile && expo build:ios
	@echo "$(GREEN)✅ Build iOS terminé!$(NC)"

mobile-build-android: ## Build Android
	@echo "$(GREEN)📱 Build Android...$(NC)"
	cd mobile && expo build:android
	@echo "$(GREEN)✅ Build Android terminé!$(NC)"