# Déploiement Railway

Ce dossier contient les instructions pour déployer sur Railway.

## Setup Initial

1. **Créer un compte Railway**
   - Aller sur [railway.app](https://railway.app)
   - Se connecter avec GitHub

2. **Déployer depuis GitHub**
   - Créer un nouveau projet
   - Connecter votre repository GitHub
   - Railway détectera automatiquement `railway.toml`

3. **Variables d'environnement Railway**
   ```bash
   DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres
   SECRET_KEY=your-super-secret-jwt-key-change-in-production
   CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Configuration

### Fichiers importants
- `railway.toml` - Configuration Railway
- `Procfile` - Commande de démarrage
- `backend/Dockerfile.railway` - Dockerfile optimisé pour Railway
- `backend/main_cloud.py` - Version cloud de l'application

### Commandes Railway CLI

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Login
railway login

# Déployer
railway up

# Voir les logs
railway logs

# Ouvrir dans le navigateur
railway open
```

## Health Check

L'application expose un endpoint `/health` pour les vérifications de santé :

```bash
curl https://your-app.railway.app/health
```

## Domaine personnalisé

1. Aller dans les settings du projet Railway
2. Ajouter votre domaine personnalisé
3. Configurer les DNS selon les instructions Railway

## Monitoring

Railway fournit automatiquement :
- Monitoring des ressources
- Logs en temps réel
- Métriques de performance
- Alertes automatiques