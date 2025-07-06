# Platform Python FastAPI - Démonstration Portfolio

Une plateforme de gestion moderne développée avec FastAPI et React, conçue pour démontrer des compétences en développement full-stack.

## 🎯 Objectif

Ce projet sert de **démonstration technique** pour showcaser les compétences en développement d'applications web modernes avec des technologies de pointe.

## ✅ Fonctionnalités Actuelles

### 🔐 Authentification & Autorisation
- ✅ **Login/Register** avec validation des données
- ✅ **JWT Authentication** avec access et refresh tokens
- ✅ **RBAC** (Role-Based Access Control) : Admin, Manager, User
- ✅ **Endpoints sécurisés** avec middleware d'authentification

### 👥 Gestion des Utilisateurs
- ✅ **Profils utilisateurs** complets avec rôles
- ✅ **API REST** pour CRUD utilisateurs
- ✅ **Données de démonstration** pré-chargées
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
- ✅ **API dédiée** pour les statistiques

### 🔧 API REST Complète
- ✅ **Documentation automatique** avec Swagger/OpenAPI
- ✅ **Validation des données** avec Pydantic
- ✅ **Gestion d'erreurs** standardisée
- ✅ **CORS** configuré pour le frontend

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
- **Axios** pour les appels API

### Infrastructure & DevOps
- **Docker Compose** pour l'orchestration locale
- **Multi-stage builds** pour l'optimisation
- **Health checks** pour la supervision
- **Volume persistence** pour les données

## 🏗️ Architecture

```
├── backend/                    # API FastAPI
│   ├── app/                    # Code applicatif (structure modulaire prête)
│   ├── simple_main.py          # API principale avec données de démo
│   ├── requirements.txt        # Dépendances Python
│   └── Dockerfile              # Container backend
├── frontend/                   # Application React
│   ├── src/
│   │   ├── components/         # Composants réutilisables
│   │   ├── store/              # Gestion d'état Zustand
│   │   ├── lib/                # Utilitaires et configuration API
│   │   └── types/              # Types TypeScript
│   ├── package.json            # Dépendances Node.js
│   └── Dockerfile              # Container frontend
├── docker-compose.yml          # Orchestration des services
└── CLAUDE.md                   # Instructions pour l'IA
```

## 🚀 Démarrage Rapide

### Prérequis
- **Docker** et **Docker Compose**
- **Git** pour cloner le repository

### Installation

```bash
# Cloner le repository
git clone <repository-url>
cd platform-python-fastapi

# Démarrer tous les services
docker-compose up -d

# Vérifier que les services sont opérationnels
docker-compose ps
```

### Accès aux Services

- **🌐 Frontend React** : http://localhost:3000
- **🔗 API Backend** : http://localhost:8000
- **📚 Documentation API** : http://localhost:8000/docs
- **🗄️ Base de données** : PostgreSQL sur port 5432
- **🔄 Redis** : Port 6379

### Comptes de Démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Admin** | admin@example.com | admin123 |
| **Manager** | manager@example.com | manager123 |
| **User** | john.doe@example.com | user123 |

## 🧪 Tests des Fonctionnalités

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

## 📊 APIs Disponibles

### Authentification
- `POST /api/v1/auth/login` - Connexion utilisateur
- `POST /api/v1/auth/login/json` - Connexion (format alternatif)
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

## 🔮 Fonctionnalités à Développer

### 🔐 Sécurité Avancée
- [ ] **2FA/MFA** avec TOTP ou SMS
- [ ] **OAuth2** avec Google/GitHub/LinkedIn
- [ ] **Rate limiting** avancé par utilisateur
- [ ] **Audit logs** pour toutes les actions sensibles
- [ ] **Chiffrement** des données sensibles
- [ ] **Session management** avancée

### 📊 Analytics & Reporting
- [ ] **Tableaux de bord** personnalisables avec widgets
- [ ] **Graphiques interactifs** (Chart.js/D3.js)
- [ ] **Exports PDF/Excel** des rapports
- [ ] **Métriques de performance** en temps réel
- [ ] **Alertes configurables** sur seuils
- [ ] **Rapports automatisés** par email

### 🔄 Intégrations & API
- [ ] **API GraphQL** en complément du REST
- [ ] **Webhooks** pour les événements
- [ ] **Intégrations tierces** (Slack, Teams, Discord)
- [ ] **API de paiement** (Stripe, PayPal)
- [ ] **Service d'email** (SendGrid, Mailgun)
- [ ] **Stockage cloud** (AWS S3, Google Cloud)

### 📱 Application Mobile
- [ ] **React Native** pour iOS/Android
- [ ] **Synchronisation offline** avec cache intelligent
- [ ] **Notifications push** natives
- [ ] **Interface adaptive** tablette/mobile
- [ ] **Biometric authentication** (Touch/Face ID)
- [ ] **Mode sombre** complet

### 🚀 Performance & Scalabilité
- [ ] **Cache Redis** intelligent multi-niveaux
- [ ] **Pagination** optimisée avec curseurs
- [ ] **Compression** des réponses API
- [ ] **CDN** pour les assets statiques
- [ ] **Database indexing** optimisé
- [ ] **Connection pooling** avancé

### 🔧 DevOps & Monitoring
- [ ] **CI/CD pipelines** avec GitLab/GitHub Actions
- [ ] **Tests automatisés** (unit, integration, e2e)
- [ ] **Monitoring** avec Prometheus + Grafana
- [ ] **Logging centralisé** avec ELK Stack
- [ ] **Infrastructure as Code** (Terraform)
- [ ] **Kubernetes** deployment avec Helm

### 🛡️ Qualité & Fiabilité
- [ ] **Tests de charge** avec locust/k6
- [ ] **Coverage** 100% avec tests unitaires
- [ ] **Linting** automatisé (Black, ESLint, Prettier)
- [ ] **Security scanning** avec Bandit/npm audit
- [ ] **Dependency updates** automatisées
- [ ] **Documentation** interactive avec Storybook

### 🎨 UX/UI Avancée
- [ ] **Thèmes personnalisables** (couleurs, polices)
- [ ] **Animations** micro-interactions avec Framer Motion
- [ ] **Drag & drop** pour organisation des tâches
- [ ] **Recherche globale** avec autocomplétion
- [ ] **Raccourcis clavier** pour power users
- [ ] **Accessibilité** WCAG 2.1 AAA complète

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

## 📞 Contact

**Kévy DARDOR** - Développeur Full-Stack
- 💼 **LinkedIn** : [linkedin.com/in/kevy-dardor](https://linkedin.com/in/kevy-dardor)
- 🐱 **GitHub** : [github.com/kevy-dardor](https://github.com/kevy-dardor)
- 📧 **Email** : kevy.dardor@example.com

---

## 📄 Licence

Ce projet est développé à des fins de démonstration technique et de portfolio professionnel.

**© 2024 Kévy DARDOR - Développé avec ❤️ pour showcaser les compétences en développement moderne**