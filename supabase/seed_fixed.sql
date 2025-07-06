-- Données de démonstration pour Supabase - Version corrigée
-- Vider les tables existantes
TRUNCATE TABLE tasks, projects, users RESTART IDENTITY CASCADE;

-- Utilisateurs avec mots de passe en clair temporaire (à modifier après test)
INSERT INTO users (email, username, full_name, hashed_password, is_active, role) VALUES
-- Utilise des hashes bcrypt générés avec le bon contexte
('admin@example.com', 'admin', 'System Administrator', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'ADMIN'),
('manager@example.com', 'manager', 'Project Manager', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'MANAGER'),
('john.doe@example.com', 'johndoe', 'John Doe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'USER'),
('jane.smith@example.com', 'janesmith', 'Jane Smith', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'USER'),
('developer@example.com', 'developer', 'Senior Developer', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'USER'),
('tester@example.com', 'tester', 'QA Tester', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, 'USER');

-- ====================================
-- PROJETS DE DÉMONSTRATION  
-- ====================================
INSERT INTO projects (name, description, status, created_by, start_date, end_date) VALUES
('Développement API', 'Création API REST avec FastAPI', 'ACTIVE', 1, '2024-01-15', '2024-06-15'),
('Refonte Frontend', 'Migration vers React et TypeScript', 'ACTIVE', 2, '2024-02-01', '2024-08-01'),
('Infrastructure Cloud', 'Migration vers AWS/Azure', 'PLANNING', 1, '2024-03-01', '2024-12-01'),
('Système de monitoring', 'Mise en place observabilité', 'ACTIVE', 2, '2024-01-20', '2024-05-20'),
('Documentation technique', 'Refonte complète docs', 'COMPLETED', 3, '2023-11-01', '2024-01-31'),
('Tests automatisés', 'Implémentation CI/CD complet', 'ACTIVE', 3, '2024-02-15', '2024-07-15'),
('Sécurité applicative', 'Audit et renforcement sécurité', 'PLANNING', 1, '2024-04-01', '2024-09-01'),
('Mobile App', 'Développement application mobile', 'PLANNING', 2, '2024-05-01', '2024-11-01'),
('Data Analytics', 'Plateforme analyse de données', 'ACTIVE', 1, '2024-01-10', '2024-08-10'),
('Formation équipe', 'Formation développeurs junior', 'COMPLETED', 3, '2023-10-01', '2023-12-31'),
('Optimisation BDD', 'Amélioration performances base', 'ACTIVE', 2, '2024-02-20', '2024-06-20'),
('Backup & Recovery', 'Stratégie sauvegarde/restoration', 'PLANNING', 1, '2024-03-15', '2024-08-15');

-- NOTE: Les mots de passe sont tous "secret" pour ce test
-- Credentials de test: admin@example.com / secret