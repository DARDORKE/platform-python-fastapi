# Platform Python FastAPI - Portfolio Demonstration

Une plateforme de gestion moderne développée avec FastAPI et React, conçue pour démontrer des compétences en développement full-stack.

## 🎯 Objectif

Ce projet sert de **démonstration technique** pour showcaser les compétences en développement d'applications web modernes avec des technologies de pointe.

## 📋 Prérequis

Avant d'installer le projet, assurez-vous d'avoir les outils suivants installés :

- **Docker** (version 20.10+) - [Installation](https://docs.docker.com/get-docker/)
- **Docker Compose** (version 2.0+) - [Installation](https://docs.docker.com/compose/install/)
- **Make** - Généralement préinstallé sur Linux/macOS, [Installation Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
- **Git** - [Installation](https://git-scm.com/downloads)

### Vérification des prérequis
```bash
docker --version          # Docker version 20.10+
docker-compose --version  # Docker Compose version 2.0+
make --version            # GNU Make 4.0+
git --version             # Git 2.0+
```

## 🚀 Démarrage Rapide

### Installation Simple

```bash
# Cloner le repository
git clone https://github.com/DARDORKE/platform-python-fastapi
cd platform-python-fastapi

# Rendre les scripts exécutables (si nécessaire)
chmod +x scripts/*.sh

# Initialisation complète en une commande
make quick-init
```

Cette commande :
- ✅ Démarre tous les services Docker
- ✅ Initialise la base de données (avec fallback intelligent)
- ✅ Déploie les données de démonstration
- ✅ Valide l'installation

### Commandes Alternatives

```bash
# Initialisation avec confirmation
make init

# Initialisation simple sans Alembic
make init-simple

# Redéployer seulement les données
make fixtures
```

### Accès aux Services

- **🌐 Frontend React** : http://localhost:3000
- **🔗 API Backend** : http://localhost:8000
- **📚 Documentation API** : http://localhost:8000/docs

### Comptes de Démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Admin** | admin@example.com | admin123 |
| **Manager** | manager@example.com | manager123 |
| **User** | john.doe@example.com | user123 |

## ✅ Fonctionnalités Démontrées

### 🔐 Authentification & Autorisation
- ✅ **Login/Register** avec validation des données
- ✅ **JWT Authentication** avec access et refresh tokens
- ✅ **RBAC** (Role-Based Access Control) : Admin, Manager, User
- ✅ **Endpoints sécurisés** avec middleware d'authentification

### 👥 Gestion des Utilisateurs
- ✅ **Profils utilisateurs** complets avec rôles
- ✅ **API REST** pour CRUD utilisateurs
- ✅ **Interface utilisateur** moderne et responsive

### 📊 Gestion des Projets
- ✅ **CRUD complet** pour les projets
- ✅ **Statuts et priorités** configurables
- ✅ **Budget et dates** de suivi
- ✅ **Interface React** pour la gestion visuelle

### 📝 Gestion des Tâches
- ✅ **CRUD complet** pour les tâches
- ✅ **Assignation** aux projets
- ✅ **Statuts de progression** (TODO, IN_PROGRESS, DONE)
- ✅ **Priorités** et dates d'échéance

### 📈 Dashboard & Statistiques
- ✅ **Métriques en temps réel** depuis l'API
- ✅ **Statistiques des projets** et tâches
- ✅ **Interface dashboard** moderne

## 🛠️ Stack Technique

### Backend (FastAPI)
- **Python 3.11+** avec typage moderne
- **FastAPI** pour l'API REST haute performance
- **Pydantic** pour la validation et sérialisation
- **PostgreSQL 15** comme base de données
- **Redis** pour la mise en cache et sessions
- **JWT** pour l'authentification sécurisée
- **Docker** pour la containerisation

### Frontend (React + TypeScript)
- **React 18** avec les derniers hooks
- **TypeScript** pour le typage strict
- **Vite** pour le build et développement rapide
- **Zustand** pour la gestion d'état moderne
- **Tailwind CSS** pour le styling utilitaire
- **Heroicons** pour l'iconographie

### Infrastructure & DevOps
- **Docker Compose** pour l'orchestration locale
- **Multi-stage builds** pour l'optimisation
- **Health checks** pour la supervision
- **Scripts d'initialisation** automatisés

## 📊 APIs Disponibles

### Authentification
- `POST /api/v1/auth/login` - Connexion utilisateur
- `POST /api/v1/auth/login/json` - Connexion (format JSON)
- `POST /api/v1/auth/register` - Inscription utilisateur
- `POST /api/v1/auth/refresh` - Rafraîchissement des tokens

### Utilisateurs
- `GET /api/v1/users` - Liste des utilisateurs
- `GET /api/v1/users/me` - Profil utilisateur courant

### Projets
- `GET /api/v1/projects` - Liste des projets
- `GET /api/v1/projects/{id}` - Détails d'un projet
- `POST /api/v1/projects` - Créer un projet
- `PUT /api/v1/projects/{id}` - Modifier un projet
- `DELETE /api/v1/projects/{id}` - Supprimer un projet

### Tâches
- `GET /api/v1/tasks` - Liste des tâches
- `GET /api/v1/tasks/{id}` - Détails d'une tâche
- `POST /api/v1/tasks` - Créer une tâche
- `PUT /api/v1/tasks/{id}` - Modifier une tâche
- `DELETE /api/v1/tasks/{id}` - Supprimer une tâche
- `GET /api/v1/tasks/stats/me` - Statistiques des tâches

### Dashboard
- `GET /api/v1/dashboard/stats` - Statistiques générales

## 🧪 Tests & Validation

### Tests API (Backend)
```bash
# Test de connexion
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test des projets
curl http://localhost:8000/api/v1/projects

# Test des statistiques
curl http://localhost:8000/api/v1/dashboard/stats
```

### Tests Frontend
- Accédez à http://localhost:3000
- Connectez-vous avec un compte de démo
- Naviguez dans le dashboard, projets et tâches

## 🔧 Commandes de Développement

### Gestion des Services
```bash
# État des services
docker-compose ps

# Logs en temps réel
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Arrêter tous les services
docker-compose down

# Redémarrer tous les services
docker-compose up -d
```

### Données de Démonstration
```bash
# Redéployer les données
make fixtures

# Réinitialiser complètement
make quick-init
```

## 📊 Données de Démonstration

### 👥 Utilisateurs (6)
- **👑 Administrateur** : admin@example.com / admin123
- **👨‍💼 Chef de projet** : manager@example.com / manager123  
- **👤 John Doe** : john.doe@example.com / user123
- **👤 Jane Smith** : jane.smith@example.com / user123
- **👨‍💻 Développeur senior** : developer@example.com / dev123
- **🧪 Testeur QA** : tester@example.com / test123

## 🔍 Résolution des Problèmes

### Problème de Connexion à la Base de Données
```bash
# Vérifier l'état des services
docker-compose ps

# Vérifier les logs
docker-compose logs database

# Redémarrer la base de données
docker-compose restart database
```

### Erreurs de Migration
Le système utilise une approche intelligente :
1. **Tentative avec Alembic** : Essaie les migrations standard
2. **Fallback automatique** : Bascule sur la création directe si échec
3. **Redémarrage du backend** : Vide le cache SQLAlchemy

### Nettoyage Complet
```bash
# Arrêter et supprimer tout
docker-compose down -v --remove-orphans

# Nettoyer le système Docker
docker system prune -f

# Réinitialiser
make quick-init
```

## 🎯 Compétences Démontrées

### 🐍 Backend Development
- **FastAPI** architecture moderne et performances
- **Async/await** programmation asynchrone
- **SQLAlchemy** ORM avec relations complexes
- **Pydantic** validation et sérialisation de données
- **JWT** authentification et autorisation
- **Docker** containerisation et déploiement

### ⚛️ Frontend Development
- **React 18** avec hooks modernes
- **TypeScript** typage strict et productivité
- **State Management** avec Zustand
- **API Integration** avec gestion d'erreurs
- **Responsive Design** avec Tailwind CSS
- **Component Architecture** réutilisable

### 🗄️ Base de Données
- **PostgreSQL** design et optimisation
- **Relations** complexes et contraintes
- **Migrations** avec versioning
- **Performance** indexing et requêtes optimisées

### 🐳 DevOps & Infrastructure
- **Docker** multi-stage builds optimisés
- **Docker Compose** orchestration de services
- **Environment Configuration** sécurisée
- **Health Checks** et monitoring basique
- **Scripts d'automatisation** robustes

## 🔮 Évolutions Possibles

### 🔐 Sécurité Avancée
- **Rate limiting** avancé par utilisateur
- **Audit logs** pour toutes les actions sensibles

### 📊 Analytics & Reporting
- **Tableaux de bord** personnalisables
- **Graphiques interactifs** (Chart.js/D3.js)
- **Exports PDF/Excel** des rapports
- **Métriques de performance** en temps réel

### 🔄 Intégrations & API
- **API GraphQL** en complément du REST
- **Webhooks** pour les événements
- **Intégrations tierces** (Slack, Teams, Discord)

### 📱 Application Mobile
- **Synchronisation offline** avec cache intelligent
- **Notifications push** natives
- **Interface adaptive** tablette/mobile

### 🚀 Performance & Scalabilité
- **Cache Redis** intelligent multi-niveaux
- **Pagination** optimisée avec curseurs
- **Compression** des réponses API

### 🔧 DevOps & Monitoring
- **CI/CD pipelines** avec GitHub Actions
- **Tests automatisés** (unit, integration, e2e)

## 📞 Contact

**Kévy DARDOR** - Développeur Full-Stack
- 💼 **LinkedIn** : [linkedin.com/in/kevy-dardor](https://www.linkedin.com/in/kevy-dardor/)
- 🐱 **GitHub** : [github.com/kevy-dardor](https://github.com/DARDORKE/)
- 📧 **Email** : contact@kevydardor.dev

---

## 📄 Licence

Ce projet est développé à des fins de démonstration technique et de portfolio professionnel.

**© 2024 Kévy DARDOR - Développé avec ❤️ pour showcaser les compétences en développement moderne**
