# 🔒 Guide de Sécurité

Ce document décrit les bonnes pratiques de sécurité pour ce projet, particulièrement concernant la gestion des secrets et variables d'environnement.

## 🚨 Variables d'Environnement et Secrets

### ❌ JAMAIS Commiter

Les fichiers suivants ne doivent **JAMAIS** être commitées dans Git :

```bash
# Variables d'environnement avec vraies valeurs
.env
.env.local
.env.cloud
.env.production
.env.development

# Clés et secrets
*.key
*.pem
*.crt
jwt_secret.txt
supabase-service-key.txt

# Configuration avec credentials
railway.json
config_prod.py
supabase.toml
```

### ✅ Fichiers Sécurisés

Ces fichiers sont protégés par `.gitignore` :

- **Root** : `.gitignore` principal
- **Backend** : `backend/.gitignore`
- **Frontend** : `frontend/.gitignore`
- **Supabase** : `supabase/.gitignore`
- **Scripts** : `scripts/.gitignore`

## 🔑 Gestion des Secrets

### Variables d'environnement Cloud

```bash
# ❌ NE PAS commiter .env.cloud avec vraies valeurs
DATABASE_URL=postgresql://postgres:REAL_PASSWORD@host:5432/db
SECRET_KEY=real-super-secret-key
SUPABASE_SERVICE_KEY=eyJ0eXAiOiJKV1Q...real-key

# ✅ Utiliser .env.cloud.example pour documentation
DATABASE_URL=postgresql://postgres:PASSWORD@host:5432/db
SECRET_KEY=your-super-secret-key
SUPABASE_SERVICE_KEY=your-service-key
```

### Développement Local

```bash
# ✅ Copier l'exemple
cp .env.cloud.example .env.cloud

# ✅ Éditer avec vos vraies valeurs
nano .env.cloud

# ❌ Ne pas commiter le fichier modifié
git add .env.cloud  # ⚠️ DANGER !
```

## 🛡️ Bonnes Pratiques

### 1. Vérification avant Commit

```bash
# Vérifier les fichiers à commiter
git status

# Simulation d'ajout (voir ce qui serait ajouté)
git add -n .

# Vérifier le diff avant commit
git diff --cached
```

### 2. Configuration Git Hooks

```bash
# Créer un pre-commit hook (optionnel)
echo '#!/bin/bash
if git diff --cached --name-only | grep -E "\.(env|key|pem)$"; then
  echo "❌ ERREUR: Fichier sensible détecté!"
  echo "Fichiers bloqués:"
  git diff --cached --name-only | grep -E "\.(env|key|pem)$"
  exit 1
fi' > .git/hooks/pre-commit

chmod +x .git/hooks/pre-commit
```

### 3. Suppression d'un Secret Committé par Erreur

Si un secret a été committé par erreur :

```bash
# ⚠️ DANGER : Réécriture de l'historique Git
# NE PAS faire si d'autres personnes ont déjà pull

# Supprimer le fichier de l'historique
git filter-branch --index-filter 'git rm --cached --ignore-unmatch .env' HEAD

# OU utiliser BFG Repo-Cleaner (recommandé)
# java -jar bfg.jar --delete-files .env

# Forcer le push (DANGER)
git push --force
```

**⚠️ Important** : Si un secret a été exposé publiquement :
1. **Révoquer immédiatement** la clé/secret
2. **Générer de nouvelles** clés
3. **Mettre à jour** tous les services

## 🔍 Variables par Service

### Supabase
```bash
# Sensibles
DATABASE_URL=postgresql://...
SUPABASE_SERVICE_KEY=eyJ...

# Publiques (OK dans le frontend)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ... (anonyme, OK)
```

### Railway
```bash
# Sensibles
SECRET_KEY=jwt-secret-key
DATABASE_URL=postgresql://...
```

### Vercel
```bash
# Publiques (exposées au frontend)
VITE_API_BASE_URL=https://api.example.com
VITE_APP_NAME=Platform Portfolio
```

## 🧪 Test de Sécurité

### Vérifier les Gitignores

```bash
# Créer un fichier test
echo "SECRET_KEY=test" > .env.test

# Vérifier qu'il est ignoré
git status | grep -q ".env.test" && echo "❌ PROBLÈME" || echo "✅ OK"

# Nettoyer
rm .env.test
```

### Audit des Commits

```bash
# Chercher des secrets dans l'historique
git log --all --full-history -- .env
git log --all --full-history -- "*.key"

# Chercher des patterns suspects
git log --all --grep="password\|secret\|key" --oneline
```

## 📚 Ressources Sécurité

### Outils de Scan

- **TruffleHog** : Détection de secrets dans Git
- **GitLeaks** : Scanner de secrets
- **GitHub Secret Scanning** : Automatique sur GitHub

### Générateurs de Secrets

```bash
# Générer une clé JWT sécurisée
openssl rand -hex 32

# Générer un UUID
python -c "import uuid; print(uuid.uuid4())"

# Générer un mot de passe fort
openssl rand -base64 32
```

## ⚡ Actions d'Urgence

Si un secret est compromis :

1. **🚨 Révoquer immédiatement**
   - Supabase : Réinitialiser les clés dans le dashboard
   - Railway : Regénérer les variables d'environnement
   - JWT : Changer `SECRET_KEY`

2. **🔄 Mettre à jour partout**
   - Services cloud
   - Équipe de développement
   - Environnements de staging/prod

3. **📊 Monitorer**
   - Logs d'accès inhabituels
   - Activité suspecte dans les services

---

**🎯 Rappel** : La sécurité est une responsabilité partagée. Toujours vérifier avant de commiter !