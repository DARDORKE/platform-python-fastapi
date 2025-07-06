# 🚀 Guide d'initialisation complète du projet

Ce guide vous permettra d'initialiser votre projet Portfolio Platform de A à Z avec un seul script.

## ⚡ Initialisation rapide (Recommandée)

Pour initialiser complètement votre projet en une seule commande :

```bash
make quick-init
```

Cette commande va :
- ✅ Vérifier les dépendances (Docker, Docker Compose)
- ✅ Démarrer tous les services Docker
- ✅ Attendre que les services soient prêts
- ✅ Initialiser la structure de base de données
- ✅ Exécuter les migrations Alembic (ou créer les tables directement)
- ✅ Déployer 6 utilisateurs, 6 projets et 19 tâches de démonstration
- ✅ Valider l'installation complète

## 📋 Initialisation interactive

Si vous préférez confirmer avant l'exécution :

```bash
make init
```

Vous verrez un résumé des actions qui seront effectuées et devrez confirmer.

## 🛠️ Scripts disponibles

### Scripts d'initialisation

| Commande | Description | Usage |
|----------|-------------|-------|
| `make init` | Initialisation complète avec confirmation | Recommandé pour la première fois |
| `make quick-init` | Initialisation complète sans confirmation | Idéal pour les environnements automatisés |
| `make fixtures` | Déploie seulement les fixtures (services déjà en cours) | Pour recharger les données |
| `./scripts/init_project.sh --help` | Aide détaillée du script | Voir toutes les options |

### Scripts individuels

| Script | Description |
|--------|-------------|
| `scripts/init_project.py` | Script Python d'initialisation complète |
| `scripts/init_project.sh` | Script bash wrapper avec interface colorée |
| `scripts/deploy_fixtures.py` | Script Python pour déployer seulement les fixtures |
| `scripts/deploy_fixtures.sh` | Script bash pour déployer seulement les fixtures |

## 📊 Données créées

### 👥 Utilisateurs (6)
- **👑 Administrateur** : admin@example.com / admin123
- **👨‍💼 Chef de projet** : manager@example.com / manager123  
- **👤 John Doe** : john.doe@example.com / user123
- **👤 Jane Smith** : jane.smith@example.com / user123
- **👨‍💻 Développeur senior** : developer@example.com / dev123
- **🧪 Testeur QA** : tester@example.com / test123

### 📁 Projets (6)
1. **E-commerce Platform** - Plateforme e-commerce moderne (€85,000)
2. **Mobile App Development** - Application React Native (€65,000)
3. **API Documentation Portal** - Portail de documentation (€25,000)
4. **DevOps Pipeline** - Pipeline CI/CD complet (€45,000) ✅ Terminé
5. **Analytics Dashboard** - Tableau de bord analytics (€40,000)
6. **Security Audit** - Audit de sécurité complet (€30,000)

### 📝 Tâches (19)
Réparties entre les projets avec différents statuts :
- ✅ **Terminées** : 5 tâches
- 🔄 **En cours** : 5 tâches  
- 📋 **À faire** : 9 tâches

## 🌐 Accès après initialisation

Une fois l'initialisation terminée, vous pouvez accéder à :

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Interface utilisateur React |
| **API Backend** | http://localhost:8000 | API FastAPI |
| **Documentation** | http://localhost:8000/docs | Swagger UI interactif |
| **Redoc** | http://localhost:8000/redoc | Documentation alternative |

## 🧪 Tests de validation

### Test d'authentification
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

### Test des endpoints
```bash
# Liste des projets
curl http://localhost:8000/api/v1/projects

# Liste des tâches
curl http://localhost:8000/api/v1/tasks

# Statistiques du dashboard
curl http://localhost:8000/api/v1/dashboard/stats
```

## 🔧 Commandes utiles post-initialisation

### Gestion des services
```bash
# État des services
docker-compose ps

# Logs en temps réel
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Arrêter tous les services
make dev-stop

# Redémarrer tous les services
make dev-restart
```

### Re-déploiement des données
```bash
# Redéployer seulement les fixtures
make fixtures

# Réinitialiser complètement
make quick-init
```

## ⚙️ Configuration avancée

### Variables d'environnement modifiables

Les scripts utilisent ces variables avec des valeurs par défaut :

```bash
DATABASE_URL=postgresql://platform_user:platform_password@database:5432/platform
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-change-in-production
```

### Personnalisation des données

Pour personnaliser les données de démonstration, modifiez :
- `scripts/init_project.py` - Données complètes
- `scripts/deploy_fixtures.py` - Données simples

## 🔍 Dépannage

### Problème de connexion à la base de données
```bash
# Vérifier l'état de la base de données
docker-compose logs database

# Redémarrer la base de données
docker-compose restart database
```

### Erreur de migrations Alembic
Le script gère automatiquement les erreurs d'Alembic et bascule sur la création directe des tables.

### Services non prêts
Le script attend automatiquement jusqu'à 30 tentatives (1 minute) que les services soient prêts.

### Nettoyage complet
```bash
# Arrêter et supprimer tout
docker-compose down -v --remove-orphans

# Nettoyer le système Docker
docker system prune -f

# Réinitialiser
make quick-init
```

## 📈 Workflow de développement recommandé

1. **Initialisation** : `make quick-init`
2. **Développement** : Modifier le code
3. **Tests** : `make test-all`
4. **Validation** : Tester manuellement via l'interface
5. **Reset si nécessaire** : `make fixtures` ou `make quick-init`

## 🎯 Prochaines étapes

Après l'initialisation réussie :

1. **Connectez-vous** au frontend avec un compte de démonstration
2. **Explorez l'API** via la documentation Swagger
3. **Testez les fonctionnalités** CRUD (projets, tâches, utilisateurs)
4. **Commencez votre développement** avec une base solide

---

**🎉 Félicitations ! Votre projet Portfolio Platform est maintenant complètement initialisé et prêt pour le développement.**