# Déploiement Vercel

Ce dossier contient les instructions pour déployer le frontend sur Vercel.

## Setup Initial

1. **Créer un compte Vercel**
   - Aller sur [vercel.com](https://vercel.com)
   - Se connecter avec GitHub

2. **Déployer depuis GitHub**
   - Importer votre repository
   - Vercel détectera automatiquement le framework React
   - Configurer le build command et output directory

3. **Configuration Build**
   ```
   Build Command: cd frontend && npm run build
   Output Directory: frontend/dist
   Install Command: cd frontend && npm install
   ```

## Variables d'Environnement Vercel

Dans les settings de votre projet Vercel, ajouter :

```bash
VITE_API_BASE_URL=https://your-app.railway.app
VITE_APP_NAME=Platform Portfolio
NODE_ENV=production
```

## Configuration

### Fichiers importants
- `vercel.json` - Configuration Vercel (routing SPA, headers)
- `frontend/.env.production` - Variables d'environnement production
- `frontend/package.json` - Scripts de build

### Scripts NPM pour Vercel

```json
{
  "scripts": {
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

## Déploiement

### Via Interface Vercel
1. Connecter le repository GitHub
2. Configurer les variables d'environnement
3. Déployer automatiquement

### Via CLI Vercel
```bash
# Installer Vercel CLI
npm install -g vercel

# Login
vercel login

# Déployer
vercel

# Déployer en production
vercel --prod
```

## Domaine personnalisé

1. Aller dans les settings du projet Vercel
2. Ajouter votre domaine
3. Configurer les DNS selon les instructions

## Optimisations

Le `vercel.json` inclut :
- Routing SPA (toutes les routes vers index.html)
- Cache headers pour les assets statiques
- Configuration des variables d'environnement

## Preview Deployments

Vercel crée automatiquement des preview deployments pour :
- Chaque push sur une branche
- Chaque pull request

Utile pour tester avant de merger en production.