# Scripts de déploiement des fixtures

Ce répertoire contient les scripts pour déployer les données de démonstration (fixtures) dans votre projet.

## 🚀 Déploiement rapide

Pour déployer les fixtures, utilisez simplement :

```bash
make fixtures
```

## 📁 Scripts disponibles

### `deploy_fixtures.py`
Script Python principal qui :
- Se connecte à la base de données PostgreSQL
- Crée les tables nécessaires
- Efface les données existantes
- Charge des données de démonstration réalistes

### `deploy_fixtures.sh`
Script bash wrapper qui :
- Vérifie que Docker Compose est en cours d'exécution
- Exécute le script Python dans le conteneur backend
- Affiche les informations de connexion

## 📊 Données créées

### Utilisateurs (5)
- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123
- **User 1**: john.doe@example.com / user123
- **User 2**: jane.smith@example.com / user123
- **Developer**: developer@example.com / dev123

### Projets (4)
- **E-commerce Platform** - Développement d'une plateforme e-commerce moderne
- **Mobile App Development** - Application mobile React Native
- **API Documentation** - Documentation complète de l'API
- **DevOps Pipeline** - Pipeline CI/CD avec Docker et Kubernetes

### Tâches (10)
Diverses tâches réparties entre les projets avec différents statuts :
- ✅ Terminées
- 🔄 En cours
- 📋 À faire

## 🔧 Configuration

### Variables d'environnement
Le script utilise ces variables (avec des valeurs par défaut) :

```bash
DATABASE_URL=postgresql://platform_user:platform_password@database:5432/platform
```

### Fonctionnalités
- ✅ Attend automatiquement que la base de données soit prête
- ✅ Crée les tables automatiquement
- ✅ Efface les données existantes avant le déploiement
- ✅ Gère les erreurs et les rollbacks
- ✅ Affiche des messages de progression colorés

## 🎯 Utilisation

### Déploiement initial
```bash
# Démarrer les services
docker-compose up -d

# Déployer les fixtures
make fixtures
```

### Redéploiement
```bash
# Redéployer les fixtures (efface les données existantes)
make fixtures
```

### Déploiement manuel
```bash
# Exécuter le script directement
docker-compose exec -T backend python /app/scripts/deploy_fixtures.py
```

## 🧪 Validation

Après le déploiement, vous pouvez tester :

```bash
# Test de connexion
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test de l'API
curl http://localhost:8000/api/v1/projects
```

## 📋 Intégration Makefile

Le script est intégré dans le Makefile principal :

```makefile
fixtures: ## Déploie les fixtures (données de démonstration)
	@echo "$(GREEN)🚀 Déploiement des fixtures...$(NC)"
	@chmod +x scripts/deploy_fixtures.sh
	@./scripts/deploy_fixtures.sh
	@echo "$(GREEN)✅ Fixtures déployées!$(NC)"
```

## 🔍 Dépannage

### Problème de connexion à la base de données
```bash
# Vérifier le statut des services
docker-compose ps

# Vérifier les logs de la base de données
docker-compose logs database
```

### Problème de permissions
```bash
# Rendre le script exécutable
chmod +x scripts/deploy_fixtures.sh
```

### Problème de modules Python
```bash
# Reconstruire le conteneur backend
docker-compose build backend
docker-compose up -d backend
```

## 📝 Notes importantes

1. **Données de démonstration** : Ce script est conçu pour un environnement de développement/démonstration
2. **Efface les données** : Le script efface toutes les données existantes avant le déploiement
3. **Pas pour la production** : Ne pas utiliser en production sans adaptation
4. **Gestion des erreurs** : Le script gère les erreurs et effectue des rollbacks en cas de problème

## 🔄 Évolution

Pour ajouter de nouvelles données de démonstration :

1. Modifier `deploy_fixtures.py`
2. Ajouter les nouvelles données dans les fonctions `create_demo_*`
3. Tester le déploiement
4. Mettre à jour cette documentation

---

**Note** : Ce script fait partie du système de démonstration du portfolio et est optimisé pour showcaser les fonctionnalités de l'application.