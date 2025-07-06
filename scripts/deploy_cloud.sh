#!/bin/bash

# Script de déploiement cloud automatisé
# Usage: ./scripts/deploy_cloud.sh [supabase|railway|vercel|all]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    log_info "Vérification des dépendances..."
    
    # Check if required tools are installed
    command -v git >/dev/null 2>&1 || { log_error "Git n'est pas installé"; exit 1; }
    
    log_success "Dépendances vérifiées"
}

deploy_supabase() {
    log_info "📊 Configuration Supabase..."
    
    if [ ! -f ".env.cloud" ]; then
        log_warning "Fichier .env.cloud non trouvé. Créez-le depuis .env.cloud.example"
        log_info "Instructions:"
        echo "1. Créer un projet sur https://supabase.com"
        echo "2. Copier .env.cloud.example vers .env.cloud"
        echo "3. Remplir DATABASE_URL depuis Supabase Settings > Database"
        echo "4. Exécuter le schéma: supabase/schema.sql dans l'éditeur SQL"
        echo "5. Exécuter les données: supabase/seed.sql dans l'éditeur SQL"
        return 1
    fi
    
    source .env.cloud
    
    if [ -z "$DATABASE_URL" ]; then
        log_error "DATABASE_URL non définie dans .env.cloud"
        return 1
    fi
    
    log_info "⚡ Instructions pour Supabase:"
    echo "1. Aller sur votre projet Supabase"
    echo "2. Copier le contenu de supabase/schema.sql dans l'éditeur SQL et exécuter"
    echo "3. Copier le contenu de supabase/seed.sql dans l'éditeur SQL et exécuter"
    
    log_success "Configuration Supabase prête"
}

deploy_railway() {
    log_info "🚂 Déploiement Railway..."
    
    if [ ! -f ".env.cloud" ]; then
        log_error "Fichier .env.cloud requis pour Railway"
        return 1
    fi
    
    # Check if railway CLI is available
    if command -v railway >/dev/null 2>&1; then
        log_info "Utilisation de Railway CLI"
        
        # Link to project if not already linked
        if [ ! -f "railway.json" ]; then
            log_info "Premier déploiement - suivez les instructions Railway CLI"
            railway login
            railway link
        fi
        
        # Set environment variables
        source .env.cloud
        railway variables set DATABASE_URL="$DATABASE_URL"
        railway variables set SECRET_KEY="$SECRET_KEY"
        railway variables set CORS_ORIGINS="$CORS_ORIGINS"
        railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="$ACCESS_TOKEN_EXPIRE_MINUTES"
        
        # Deploy
        railway up
        
        log_success "Déploiement Railway terminé"
    else
        log_warning "Railway CLI non installé. Déploiement manuel requis:"
        echo "1. Aller sur https://railway.app"
        echo "2. Créer un nouveau projet depuis GitHub"
        echo "3. Configurer les variables d'environnement depuis .env.cloud"
        echo "4. Railway détectera automatiquement railway.toml"
    fi
}

deploy_vercel() {
    log_info "▲ Déploiement Vercel..."
    
    if [ ! -f ".env.cloud" ]; then
        log_error "Fichier .env.cloud requis pour Vercel"
        return 1
    fi
    
    # Check if vercel CLI is available
    if command -v vercel >/dev/null 2>&1; then
        log_info "Utilisation de Vercel CLI"
        
        # Login if not already
        vercel whoami >/dev/null 2>&1 || vercel login
        
        # Set environment variables
        source .env.cloud
        vercel env add VITE_API_BASE_URL production <<< "$VITE_API_BASE_URL"
        vercel env add VITE_APP_NAME production <<< "$VITE_APP_NAME"
        vercel env add NODE_ENV production <<< "production"
        
        # Deploy
        vercel --prod
        
        log_success "Déploiement Vercel terminé"
    else
        log_warning "Vercel CLI non installé. Déploiement manuel requis:"
        echo "1. Aller sur https://vercel.com"
        echo "2. Importer votre repository GitHub"
        echo "3. Configurer les variables d'environnement:"
        source .env.cloud
        echo "   VITE_API_BASE_URL=$VITE_API_BASE_URL"
        echo "   VITE_APP_NAME=$VITE_APP_NAME"
        echo "   NODE_ENV=production"
        echo "4. Vercel détectera automatiquement vercel.json"
    fi
}

test_cloud_deployment() {
    log_info "🧪 Test du déploiement cloud..."
    
    if [ ! -f ".env.cloud" ]; then
        log_warning "Impossible de tester sans .env.cloud"
        return 1
    fi
    
    source .env.cloud
    
    # Test backend health
    if [ ! -z "$VITE_API_BASE_URL" ]; then
        log_info "Test de l'API backend..."
        if curl -f "$VITE_API_BASE_URL/health" >/dev/null 2>&1; then
            log_success "API backend accessible"
        else
            log_error "API backend non accessible"
        fi
    fi
    
    # Test database connection (via API)
    if [ ! -z "$VITE_API_BASE_URL" ]; then
        log_info "Test de la base de données..."
        if curl -f "$VITE_API_BASE_URL/api/v1/dashboard/stats" >/dev/null 2>&1; then
            log_success "Base de données connectée"
        else
            log_warning "Base de données non accessible (vérifiez l'authentification)"
        fi
    fi
}

# Main script
main() {
    local command=${1:-all}
    
    log_info "🚀 Déploiement Cloud Platform Portfolio"
    log_info "Commande: $command"
    echo
    
    check_dependencies
    
    case $command in
        "supabase")
            deploy_supabase
            ;;
        "railway")
            deploy_railway
            ;;
        "vercel")
            deploy_vercel
            ;;
        "test")
            test_cloud_deployment
            ;;
        "all")
            deploy_supabase
            deploy_railway
            deploy_vercel
            test_cloud_deployment
            ;;
        *)
            log_error "Commande inconnue: $command"
            echo "Usage: $0 [supabase|railway|vercel|test|all]"
            exit 1
            ;;
    esac
    
    echo
    log_success "🎉 Déploiement cloud terminé!"
    log_info "URLs du projet:"
    
    if [ -f ".env.cloud" ]; then
        source .env.cloud
        echo "  Frontend: https://your-app.vercel.app (à remplacer par votre vraie URL)"
        echo "  Backend:  https://your-app.railway.app (à remplacer par votre vraie URL)"
        echo "  Database: Supabase Dashboard"
    fi
}

# Run script
main "$@"