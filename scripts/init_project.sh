#!/bin/bash
# Script d'initialisation complète du projet Portfolio Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[ÉTAPE]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCÈS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_banner() {
    echo -e "${PURPLE}"
    echo "================================================================================"
    echo "🚀 INITIALISATION COMPLÈTE DU PROJET PORTFOLIO PLATFORM"
    echo "================================================================================"
    echo -e "${NC}"
    echo "Ce script va :"
    echo "├── 🐳 Vérifier et démarrer Docker Compose"
    echo "├── 🗄️  Initialiser la base de données"
    echo "├── 📋 Exécuter les migrations"
    echo "├── 🌱 Déployer les fixtures"
    echo "└── ✅ Valider l'installation"
    echo ""
    echo -e "${YELLOW}⚠️  ATTENTION : Ce script va effacer toutes les données existantes !${NC}"
    echo ""
}

check_dependencies() {
    print_step "Vérification des dépendances..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker n'est pas installé"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    print_success "Dépendances vérifiées"
}

start_services() {
    print_step "Démarrage des services Docker..."
    
    # Stop existing services
    print_info "Arrêt des services existants..."
    docker-compose down > /dev/null 2>&1 || true
    
    # Start services
    print_info "Démarrage des services..."
    if docker-compose up -d; then
        print_success "Services démarrés"
    else
        print_error "Échec du démarrage des services"
        exit 1
    fi
    
    # Wait for services to be ready
    print_info "Attente de la disponibilité des services..."
    sleep 10
    
    # Check service health
    print_info "Vérification de l'état des services..."
    if docker-compose ps | grep -q "Up (healthy)"; then
        print_success "Services opérationnels"
    else
        print_warning "Certains services ne sont pas encore prêts, continuation..."
    fi
}

wait_for_services() {
    print_step "Attente de la disponibilité complète des services..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_info "Vérification des services (tentative $attempt/$max_attempts)..."
        
        # Check database
        if docker-compose exec -T database pg_isready -U platform_user -d platform > /dev/null 2>&1; then
            print_success "Base de données prête"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            print_error "Timeout : les services ne sont pas prêts"
            print_info "Logs des services :"
            docker-compose logs --tail=10
            exit 1
        fi
        
        sleep 2
        ((attempt++))
    done
}

run_initialization() {
    print_step "Exécution de l'initialisation complète..."
    
    # Try the full init script first
    print_info "Tentative d'initialisation avec Alembic..."
    if docker-compose exec -T backend python /app/scripts/init_project.py 2>/dev/null; then
        print_success "Initialisation avec Alembic terminée avec succès"
        return 0
    fi
    
    # If that fails, try the simple version
    print_warning "Échec avec Alembic, tentative d'initialisation simple..."
    print_info "Lancement du script d'initialisation simple (sans Alembic)..."
    if docker-compose exec -T backend python /app/scripts/init_project_simple.py; then
        print_info "Redémarrage du backend pour vider le cache..."
        docker-compose restart backend > /dev/null 2>&1
        print_success "Initialisation simple terminée avec succès"
        return 0
    else
        print_error "Échec des deux méthodes d'initialisation"
        print_info "Logs du backend :"
        docker-compose logs --tail=20 backend
        return 1
    fi
}

validate_installation() {
    print_step "Validation de l'installation..."
    
    # Test database connection
    print_info "Test de connexion à la base de données..."
    if docker-compose exec -T database psql -U platform_user -d platform -c "SELECT COUNT(*) FROM users;" > /dev/null 2>&1; then
        print_success "Base de données accessible"
    else
        print_error "Problème de connexion à la base de données"
        exit 1
    fi
    
    # Test API endpoints
    print_info "Test des endpoints API..."
    sleep 5  # Wait for API to be ready
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "API opérationnelle"
    else
        print_warning "API non accessible, mais l'initialisation semble réussie"
    fi
    
    # Test authentication
    print_info "Test de l'authentification..."
    if curl -X POST http://localhost:8000/api/v1/auth/login/json \
        -H "Content-Type: application/json" \
        -d '{"email":"admin@example.com","password":"admin123"}' \
        -f > /dev/null 2>&1; then
        print_success "Authentification fonctionnelle"
    else
        print_warning "Test d'authentification échoué, mais les données sont créées"
    fi
}

show_final_info() {
    echo ""
    echo -e "${GREEN}================================================================================"
    echo "🎉 INITIALISATION TERMINÉE AVEC SUCCÈS !"
    echo "================================================================================${NC}"
    echo ""
    echo -e "${CYAN}📋 INFORMATIONS D'ACCÈS :${NC}"
    echo "├── 🌐 Frontend : http://localhost:3000"
    echo "├── 🔧 API Backend : http://localhost:8000"
    echo "├── 📚 Documentation API : http://localhost:8000/docs"
    echo "└── 📖 Redoc : http://localhost:8000/redoc"
    echo ""
    echo -e "${CYAN}🔑 COMPTES DE DÉMONSTRATION :${NC}"
    echo "├── 👑 Admin : admin@example.com / admin123"
    echo "├── 👨‍💼 Manager : manager@example.com / manager123"
    echo "├── 👤 John Doe : john.doe@example.com / user123"
    echo "├── 👤 Jane Smith : jane.smith@example.com / user123"
    echo "├── 👨‍💻 Developer : developer@example.com / dev123"
    echo "└── 🧪 Tester : tester@example.com / test123"
    echo ""
    echo -e "${CYAN}🧪 TESTS RAPIDES :${NC}"
    echo "├── État des services : docker-compose ps"
    echo "├── Logs en temps réel : docker-compose logs -f"
    echo "├── Test API : curl http://localhost:8000/api/v1/projects"
    echo "└── Test auth : curl -X POST http://localhost:8000/api/v1/auth/login/json \\"
    echo "                 -H 'Content-Type: application/json' \\"
    echo "                 -d '{\"email\":\"admin@example.com\",\"password\":\"admin123\"}'"
    echo ""
    echo -e "${CYAN}⚡ COMMANDES UTILES :${NC}"
    echo "├── Redémarrer : make dev-restart"
    echo "├── Arrêter : make dev-stop"
    echo "├── Logs : make dev-logs"
    echo "├── Refaire les fixtures : make fixtures"
    echo "└── Aide : make help"
    echo ""
    echo -e "${GREEN}🚀 PROJET PRÊT POUR LE DÉVELOPPEMENT !${NC}"
    echo ""
}

# Confirmation prompt
confirm_initialization() {
    echo -e "${YELLOW}Voulez-vous continuer ? (y/N)${NC}"
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY]|[oO][uU][iI]|[oO]) 
            echo "Initialisation confirmée..."
            ;;
        *)
            echo "Initialisation annulée."
            exit 0
            ;;
    esac
}

main() {
    print_banner
    
    # Skip confirmation if --yes flag is provided
    if [[ "$1" != "--yes" && "$1" != "-y" ]]; then
        confirm_initialization
    fi
    
    echo ""
    echo -e "${PURPLE}🚀 DÉBUT DE L'INITIALISATION...${NC}"
    echo ""
    
    # Main initialization steps
    check_dependencies
    start_services
    wait_for_services
    run_initialization
    validate_installation
    
    echo ""
    show_final_info
}

# Handle script arguments
case "$1" in
    --help|-h)
        echo "Script d'initialisation du projet Portfolio Platform"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  -y, --yes     Pas de confirmation interactive"
        echo "  -h, --help    Affiche cette aide"
        echo ""
        echo "Ce script initialise complètement le projet avec :"
        echo "- Démarrage des services Docker"
        echo "- Création de la structure de base de données"
        echo "- Déploiement des fixtures"
        echo "- Validation de l'installation"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac