# Guide de Déploiement Cloud

Ce guide vous accompagne pour déployer votre application portfolio sur le cloud en utilisant :
- **Supabase** pour la base de données PostgreSQL
- **Railway** pour le backend FastAPI
- **Vercel** pour le frontend React

## 🏗️ Architecture de Déploiement

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│     Vercel      │───▶│     Railway     │───▶│    Supabase     │
│   (Frontend)    │    │    (Backend)    │    │   (Database)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Déploiement Rapide

### Prérequis
- Compte GitHub avec le repository pushé
- Comptes sur Supabase, Railway et Vercel

### 1. Configuration initiale
```bash
# Créer le fichier de configuration cloud
make cloud-setup
```

### 2. Configurer Supabase (Base de données)
1. Créer un projet sur [supabase.com](https://supabase.com)
2. Aller dans **Settings > Database**
3. Copier la **Connection string** 
4. Dans l'**éditeur SQL**, exécuter :
   - Le contenu de `supabase/schema.sql`
   - Le contenu de `supabase/seed.sql`

### 3. Configurer Railway (Backend)
1. Créer un projet sur [railway.app](https://railway.app)
2. Connecter votre repository GitHub
3. Configurer les variables d'environnement :
   ```
   DATABASE_URL=<votre_url_supabase>
   SECRET_KEY=<votre_clé_secrète>
   CORS_ORIGINS=https://votre-app.vercel.app
   ```

### 4. Configurer Vercel (Frontend)
1. Créer un projet sur [vercel.com](https://vercel.com)
2. Importer votre repository GitHub
3. Configurer les variables d'environnement :
   ```
   VITE_API_BASE_URL=https://votre-app.railway.app
   VITE_APP_NAME=Platform Portfolio
   ```

### 5. Finaliser le déploiement
```bash
# Mettre à jour .env.cloud avec vos vraies URLs
# Puis déployer tout
make deploy-cloud
```

## 📝 Guide Détaillé Étape par Étape

### Phase 1: Supabase (Base de données)

#### 1.1 Créer le projet Supabase
1. Aller sur [supabase.com](https://supabase.com)
2. Cliquer "New project"
3. Choisir votre organisation
4. Nommer votre projet (ex: "portfolio-platform")
5. Créer un mot de passe pour la base
6. Choisir une région proche de vous

#### 1.2 Configurer la base de données
1. Aller dans **Settings > Database**
2. Copier la **Connection string** qui ressemble à :
   ```
   postgresql://postgres.xxx:password@xxx.pooler.supabase.com:5432/postgres
   ```
3. Aller dans **SQL Editor**
4. Créer une nouvelle query et coller le contenu de `supabase/schema.sql`
5. Exécuter la query
6. Créer une nouvelle query et coller le contenu de `supabase/seed.sql`
7. Exécuter la query

#### 1.3 Récupérer les clés API (optionnel)
1. Aller dans **Settings > API**
2. Noter l'**URL** et les clés si besoin pour les fonctionnalités avancées

### Phase 2: Railway (Backend)

#### 2.1 Créer le projet Railway
1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. Cliquer "New Project"
4. Choisir "Deploy from GitHub repo"
5. Sélectionner votre repository

#### 2.2 Configurer les variables d'environnement
Dans les **Settings** de votre projet Railway, ajouter :

```bash
DATABASE_URL=postgresql://postgres.xxx:password@xxx.pooler.supabase.com:5432/postgres
SECRET_KEY=votre-clé-super-secrète-au-moins-32-caractères
CORS_ORIGINS=https://votre-app.vercel.app,http://localhost:3000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**💡 Générer une clé secrète :**
```bash
openssl rand -hex 32
```

#### 2.3 Vérifier le déploiement
1. Railway détectera automatiquement `railway.toml`
2. Le build démarrera automatiquement
3. Noter l'URL de déploiement (ex: `https://votre-app.railway.app`)
4. Tester : `https://votre-app.railway.app/health`

### Phase 3: Vercel (Frontend)

#### 3.1 Créer le projet Vercel
1. Aller sur [vercel.com](https://vercel.com)
2. Se connecter avec GitHub
3. Cliquer "New Project"
4. Importer votre repository
5. Vercel détectera automatiquement React

#### 3.2 Configurer le build
Vercel détectera automatiquement `vercel.json`, mais vérifiez :
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `cd frontend && npm install`

#### 3.3 Configurer les variables d'environnement
Dans les **Settings > Environment Variables** :

```bash
VITE_API_BASE_URL=https://votre-app.railway.app
VITE_APP_NAME=Platform Portfolio
NODE_ENV=production
```

#### 3.4 Mettre à jour Railway
Retourner dans Railway et mettre à jour `CORS_ORIGINS` :
```bash
CORS_ORIGINS=https://votre-app.vercel.app,http://localhost:3000
```

## 🧪 Tests et Validation

### Test local de la configuration cloud
```bash
# Tester la config cloud localement (optionnel)
make cloud-test-local

# Accéder aux services
# API: http://localhost:8001
# Frontend: http://localhost:3001

# Arrêter le test
make cloud-test-stop
```

### Test de santé
```bash
# Tester le statut du déploiement
make cloud-status
```

### Tests manuels
1. **Backend** : `curl https://votre-app.railway.app/health`
2. **Frontend** : Ouvrir `https://votre-app.vercel.app`
3. **Login** : Tester avec `admin@example.com` / `admin123`

## 🔧 Maintenance et Mises à Jour

### Développement local (inchangé)
```bash
# Développement local avec Docker
make quick-init
```

### Déploiement des changements
```bash
# Les déploiements sont automatiques lors des push sur main
git push origin main

# Ou déployer manuellement
make deploy-cloud
```

### Gestion des environnements
- **Local** : `docker-compose.yml` + `make quick-init`
- **Cloud** : Variables dans Supabase/Railway/Vercel
- **Test Cloud** : `docker-compose.cloud.yml` + `make cloud-test-local`

## 🆘 Dépannage

### Erreurs communes

#### Backend ne démarre pas
- Vérifier `DATABASE_URL` dans Railway
- Vérifier que Supabase est accessible
- Consulter les logs Railway

#### Frontend ne peut pas accéder à l'API
- Vérifier `VITE_API_BASE_URL` dans Vercel
- Vérifier `CORS_ORIGINS` dans Railway
- Vérifier que l'API répond : `/health`

#### Base de données vide
- Vérifier que `supabase/schema.sql` a été exécuté
- Vérifier que `supabase/seed.sql` a été exécuté
- Consulter les logs SQL dans Supabase

### Logs et monitoring
```bash
# Logs Railway
railway logs

# Logs Vercel
vercel logs

# Monitoring Supabase
# Dashboard Supabase > Logs
```

## 📊 URLs et Accès

Après déploiement, votre application sera accessible via :

- **Frontend** : `https://votre-app.vercel.app`
- **API** : `https://votre-app.railway.app`
- **Documentation API** : `https://votre-app.railway.app/docs`
- **Base de données** : Dashboard Supabase

### Comptes de démonstration
- **Admin** : `admin@example.com` / `admin123`
- **Manager** : `manager@example.com` / `manager123`  
- **User** : `john.doe@example.com` / `user123`

## 🔄 Workflow Complet

```bash
# 1. Setup initial (une seule fois)
make cloud-setup

# 2. Configurer Supabase, Railway, Vercel via interfaces web

# 3. Mettre à jour .env.cloud avec les vraies valeurs

# 4. Déployer (ou push sur main pour auto-deploy)
make deploy-cloud

# 5. Tester
make cloud-status

# 6. Développement local normal
make quick-init
```

Ce déploiement vous donne une application portfolio complètement fonctionnelle sur le cloud, tout en conservant la possibilité de développer localement avec Docker !