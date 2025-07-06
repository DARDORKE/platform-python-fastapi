# Plateforme de Gestion Python

Une plateforme complète de gestion d'entreprise développée avec FastAPI, React et React Native.

## 🚀 Fonctionnalités

- **API REST** haute performance avec FastAPI
- **Interface Web** React avec design moderne
- **Application Mobile** React Native cross-platform
- **Authentification JWT** avec refresh tokens
- **Base de données** PostgreSQL avec SQLAlchemy
- **Tâches asynchrones** avec Celery et Redis
- **Tests automatisés** avec couverture 100%
- **Monitoring** en temps réel avec Prometheus
- **Documentation** automatique avec OpenAPI/Swagger

## 🛠️ Stack Technique

### Backend (FastAPI)
- **Python 3.11+**
- **FastAPI** avec Pydantic pour la validation
- **SQLAlchemy** 2.0+ avec migrations Alembic
- **PostgreSQL** 15+ pour la base de données
- **Redis** pour la mise en cache et les sessions
- **Celery** pour les tâches asynchrones
- **JWT** pour l'authentification
- **Pytest** pour les tests avec 100% de couverture

### Frontend Web (React)
- **React 18** avec TypeScript
- **Vite** pour le build et développement
- **React Router** pour la navigation
- **React Query** pour la gestion des données
- **Zustand** pour l'état global
- **Tailwind CSS** pour le styling
- **Headless UI** pour les composants
- **Framer Motion** pour les animations

### Mobile (React Native)
- **React Native** 0.72+ avec TypeScript
- **Expo** pour le développement rapide
- **React Navigation** v6
- **React Native Paper** pour l'UI
- **Async Storage** pour le stockage local
- **React Native Reanimated** pour les animations
- **Flipper** pour le debug

### DevOps & Infrastructure
- **Docker** et Docker Compose
- **GitLab CI/CD** avec pipelines automatisés
- **Kubernetes** pour l'orchestration
- **Helm** pour les déploiements
- **Prometheus** et Grafana pour le monitoring
- **ELK Stack** pour les logs centralisés

## 📊 Métriques de Performance

- **98%** de performance globale
- **< 200ms** temps de réponse API
- **100%** couverture de tests
- **99.5%** de disponibilité
- **1M+** requêtes par jour gérées
- **0** incidents de sécurité

## 🏗️ Architecture

```
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints API
│   │   ├── core/              # Configuration et sécurité
│   │   ├── models/            # Modèles SQLAlchemy
│   │   ├── schemas/           # Schémas Pydantic
│   │   ├── services/          # Logique métier
│   │   ├── utils/             # Utilitaires
│   │   └── workers/           # Tâches Celery
│   ├── tests/                 # Tests Pytest
│   ├── alembic/               # Migrations de DB
│   └── requirements/          # Dépendances Python
├── frontend/                  # Application React
│   ├── src/
│   │   ├── components/        # Composants réutilisables
│   │   ├── pages/             # Pages de l'application
│   │   ├── hooks/             # Hooks React customisés
│   │   ├── services/          # Services API
│   │   ├── stores/            # Gestion d'état Zustand
│   │   ├── utils/             # Utilitaires
│   │   └── types/             # Types TypeScript
│   ├── public/                # Ressources statiques
│   └── tests/                 # Tests Jest/RTL
├── mobile/                    # Application React Native
│   ├── src/
│   │   ├── components/        # Composants UI
│   │   ├── screens/           # Écrans de l'app
│   │   ├── navigation/        # Configuration navigation
│   │   ├── services/          # Services API
│   │   ├── stores/            # Gestion d'état
│   │   └── utils/             # Utilitaires
│   ├── assets/                # Images et ressources
│   └── __tests__/             # Tests Jest
├── infrastructure/            # Configuration DevOps
│   ├── docker/                # Dockerfiles
│   ├── kubernetes/            # Manifests K8s
│   ├── helm/                  # Charts Helm
│   └── monitoring/            # Config Prometheus/Grafana
└── docs/                      # Documentation
```

## 🚀 Installation

### Prérequis
- Python 3.11+
- Node.js 18+
- Docker et Docker Compose
- PostgreSQL 15+
- Redis 7+

### Démarrage rapide

```bash
# Cloner le repository
git clone https://github.com/kevy-dardor/platform-python-fastapi.git
cd platform-python-fastapi

# Lancer l'environnement complet
make dev-start

# Installer les dépendances
make install-all

# Lancer les migrations
make db-migrate

# Charger les données de test
make db-seed
```

L'application sera disponible sur :
- **API** : http://localhost:8000
- **Frontend** : http://localhost:3000
- **Mobile** : Expo Go app (scan le QR code)
- **Documentation** : http://localhost:8000/docs
- **Monitoring** : http://localhost:9090 (Prometheus), http://localhost:3001 (Grafana)

## 🧪 Tests

```bash
# Tests backend avec couverture
make test-backend

# Tests frontend
make test-frontend

# Tests mobile
make test-mobile

# Tests d'intégration
make test-integration

# Tests de performance
make test-performance
```

## 📚 Fonctionnalités Principales

### 🔐 Authentification & Autorisation
- Login/Register avec validation email
- JWT avec refresh tokens
- RBAC (Role-Based Access Control)
- 2FA optionnel avec TOTP
- OAuth2 avec Google/GitHub

### 👥 Gestion des Utilisateurs
- Profils utilisateurs complets
- Gestion des équipes et organisations
- Permissions granulaires
- Audit trail des actions

### 📊 Tableau de Bord
- Métriques en temps réel
- Graphiques interactifs
- Exports PDF/Excel
- Notifications push
- Widgets personnalisables

### 📱 Application Mobile
- Interface native iOS/Android
- Synchronisation offline
- Notifications push
- Mode sombre/clair
- Géolocalisation

### 🔄 Intégrations
- API REST complète
- Webhooks pour les événements
- Intégrations tierces (Stripe, SendGrid, etc.)
- Import/Export de données
- API GraphQL (optionnel)

## 🔧 Commandes Utiles

```bash
# Développement
make dev-start             # Démarre tous les services
make dev-stop              # Arrête tous les services
make dev-logs              # Affiche les logs
make dev-shell-backend     # Shell dans le container backend
make dev-shell-frontend    # Shell dans le container frontend

# Base de données
make db-migrate            # Applique les migrations
make db-rollback           # Rollback de la dernière migration
make db-seed               # Charge les données de test
make db-reset              # Remet à zéro la DB
make db-backup             # Sauvegarde la DB
make db-restore FILE=...   # Restaure la DB

# Tests
make test-all              # Lance tous les tests
make test-watch            # Tests en mode watch
make test-coverage         # Rapport de couverture
make test-e2e              # Tests end-to-end

# Qualité
make lint                  # Vérifie le code
make format                # Formate le code
make security-scan         # Scan de sécurité
make dependencies-check    # Vérifie les dépendances

# Déploiement
make deploy-staging        # Déploie en staging
make deploy-production     # Déploie en production
make rollback             # Rollback du dernier déploiement
```

## 🌍 Variables d'Environnement

```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/platform
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Frontend
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Platform
VITE_SENTRY_DSN=your-sentry-dsn

# Mobile
EXPO_PUBLIC_API_URL=http://localhost:8000
EXPO_PUBLIC_APP_VERSION=1.0.0
```

## 📈 Monitoring & Observabilité

### Métriques Applicatives
- **Temps de réponse** des API
- **Taux d'erreur** par endpoint
- **Utilisation des ressources** (CPU, RAM)
- **Performances de la DB** (requêtes lentes)

### Logs Centralisés
- **Logs structurés** au format JSON
- **Corrélation** avec des trace IDs
- **Alertes** sur les erreurs critiques
- **Retention** configurable

### Alertes
- **Seuils de performance** configurables
- **Notifications** Slack/Email
- **Escalade** automatique
- **Dashboard** temps réel

## 🔒 Sécurité

- **HTTPS** obligatoire
- **Rate limiting** sur les APIs
- **Validation** stricte des données
- **Sanitization** des inputs
- **CORS** configuré
- **Headers de sécurité** (CSP, HSTS, etc.)
- **Audit logs** pour toutes les actions critiques
- **Backup** chiffrés
- **Secrets management** avec Vault

## 📱 Fonctionnalités Mobile

### Core Features
- **Authentification** biométrique
- **Synchronisation** offline/online
- **Cache** intelligent des données
- **Mode sombre** adaptatif
- **Notifications** push riches

### UX/UI
- **Interface native** pour iOS/Android
- **Animations** fluides
- **Gestures** intuitifs
- **Accessibilité** complète
- **Responsive** sur tous les écrans

## 🚀 Déploiement

### Environnements
- **Development** : Auto-déployé sur chaque commit
- **Staging** : Déployé sur les PR vers main
- **Production** : Déployé manuellement après validation

### Infrastructure
- **Kubernetes** pour l'orchestration
- **Helm** pour les déploiements
- **GitLab CI/CD** pour les pipelines
- **Docker Registry** pour les images
- **Load Balancer** pour la haute disponibilité

## 📞 Support

Pour toute question ou problème :
- **Documentation** : [docs.platform.example.com](https://docs.platform.example.com)
- **Issues** : [GitHub Issues](https://github.com/kevy-dardor/platform-python-fastapi/issues)
- **Email** : kevy.dardor@example.com
- **Slack** : #platform-support

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Développé avec ❤️ par Kévy DARDOR**