# Configuration Supabase

Ce dossier contient les fichiers de configuration pour Supabase.

## Setup Initial

1. **Créer un projet sur Supabase**
   - Aller sur [supabase.com](https://supabase.com)
   - Créer un nouveau projet
   - Noter l'URL du projet et la clé anonyme

2. **Exécuter le schéma**
   - Aller dans l'éditeur SQL de Supabase
   - Copier et exécuter le contenu de `schema.sql`

3. **Charger les données de démonstration**
   - Exécuter le contenu de `seed.sql` dans l'éditeur SQL

## Variables d'environnement requises

```bash
# URL de connexion PostgreSQL
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

# URL et clé Supabase (optionnel pour les fonctionnalités avancées)
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_ANON_KEY=[anon-key]
SUPABASE_SERVICE_KEY=[service-key]
```

## Comptes de démonstration

**EXACTEMENT les mêmes que `scripts/init_project_simple.py` :**

- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123  
- **John Doe**: john.doe@example.com / user123
- **Jane Smith**: jane.smith@example.com / user123
- **Developer**: developer@example.com / dev123
- **Tester**: tester@example.com / test123

Tous les mots de passe sont hashés avec bcrypt.

## Données synchronisées

**✅ Les données dans `seed.sql` sont EXACTEMENT les mêmes que `scripts/init_project_simple.py`**

- **6 utilisateurs** avec les mêmes rôles et mots de passe
- **12 projets** complets avec budgets réalistes  
- **61 tâches** détaillées avec statuts variés
- **Dates cohérentes** pour un workflow réaliste
- **Statistiques riches** pour démonstration

## Notes techniques

- Les tables incluent des triggers pour `updated_at`
- Les index sont optimisés pour les requêtes fréquentes
- La suppression en cascade est configurée pour les relations
- Utilisation de `CURRENT_DATE` et `CURRENT_TIMESTAMP` pour des données dynamiques