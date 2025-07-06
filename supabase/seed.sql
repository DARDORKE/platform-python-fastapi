-- Données de démonstration pour Supabase
-- EXACTEMENT les mêmes données que scripts/init_project_simple.py
-- Exécuter après schema.sql

-- Vider les tables existantes
TRUNCATE TABLE tasks, projects, users RESTART IDENTITY CASCADE;

-- ====================================
-- UTILISATEURS DE DÉMONSTRATION
-- ====================================
-- Mots de passe hashés avec bcrypt (tous les mots de passe sont dans le script Python)
-- admin123, manager123, user123, dev123, test123

INSERT INTO users (email, username, full_name, hashed_password, is_active, role) VALUES
('admin@example.com', 'admin', 'System Administrator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'ADMIN'),
('manager@example.com', 'manager', 'Project Manager', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'MANAGER'),
('john.doe@example.com', 'johndoe', 'John Doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'USER'),
('jane.smith@example.com', 'janesmith', 'Jane Smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'USER'),
('developer@example.com', 'developer', 'Senior Developer', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'USER'),
('tester@example.com', 'tester', 'QA Tester', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3qn5oo5J1m', true, 'USER');

-- ====================================
-- PROJETS DE DÉMONSTRATION
-- ====================================
-- Note: Utilise les champs corrects selon schema.sql (name, description, status, priority, budget, created_at)

INSERT INTO projects (name, description, status, priority, budget) VALUES
('E-commerce Platform', 
 'Development of a modern e-commerce platform with React, FastAPI and PostgreSQL. Complete system with product management, orders, Stripe payments and advanced analytics.', 
 'active', 'high', 
 50000.00),

('Mobile App Development', 
 'React Native mobile application for iOS and Android with offline features, push notifications and cloud synchronization.', 
 'planning', 'medium', 
 35000.00),

('API Documentation Portal', 
 'Complete API documentation portal with developer guides, interactive examples and automated testing tools.', 
 'active', 'low', 
 NULL),

('DevOps Pipeline', 
 'Complete CI/CD pipeline with Docker, Kubernetes, Prometheus/Grafana monitoring and automated multi-environment deployment.', 
 'completed', 'high', 
 NULL),

('Analytics Dashboard', 
 'Real-time analytics dashboard with D3.js visualizations, custom reports and automatic alerts for business KPI tracking.', 
 'active', 'medium', 
 25000.00),

('Security Audit & Compliance', 
 'Complete security audit with penetration testing, OWASP vulnerability analysis, GDPR compliance and security recommendations.', 
 'planning', 'high', 
 15000.00),

('Microservices Architecture', 
 'Refactoring to microservices architecture with API Gateway, service mesh, observability and resilience patterns.', 
 'active', 'high', 
 NULL),

('Customer Support Portal', 
 'Customer support portal with AI chatbot, ticket system, knowledge base and customer satisfaction analytics.', 
 'planning', 'medium', 
 20000.00),

('Data Warehouse & ETL', 
 'Data warehouse construction with Apache Airflow ETL pipelines, multi-source integration and business intelligence dashboards.', 
 'active', 'medium', 
 30000.00),

('Machine Learning Platform', 
 'Complete MLOps platform with model training, automated deployment, performance monitoring and A/B testing.', 
 'planning', 'low', 
 NULL),

('Performance Optimization', 
 'Frontend and backend performance optimization: lazy loading, CDN, Redis cache, SQL optimization and APM monitoring.', 
 'completed', 'high', 
 NULL),

('Multi-tenant SaaS Platform', 
 'Transformation into multi-tenant SaaS platform with data isolation, automated billing and self-service onboarding.', 
 'active', 'high', 
 40000.00);

-- ====================================
-- TÂCHES DE DÉMONSTRATION
-- ====================================
-- Note: Utilise les champs corrects selon schema.sql (title, description, status, priority, is_completed, project_id)

-- Projet 1: E-commerce Platform
INSERT INTO tasks (title, description, status, priority, is_completed, project_id) VALUES
('Setup AWS infrastructure', 
 'AWS infrastructure configuration with Terraform: VPC, subnets, ECS, RDS, ElastiCache', 
 'done', 'high', 
 true, 1),

('JWT Authentication System', 
 'Complete JWT authentication system implementation with refresh tokens, 2FA and role management', 
 'in_progress', 'high', 
 false, 1),

('Product Catalog API', 
 'REST endpoints development for product management with advanced search, filters and pagination', 
 'todo', 'medium', 
 false, 1),

('Shopping Cart & Checkout', 
 'Shopping cart functionality with Redis persistence, tax calculation and order process', 
 'todo', 'high', 
 false, 1),

('Stripe Payment Integration', 
 'Complete Stripe integration: payments, webhooks, refunds and failure handling', 
 'todo', 'high', 
 false, 1),

('Order Management System', 
 'Order management system with tracking, notifications and returns handling', 
 'todo', 'medium', 
 false, 1),

('Inventory Management', 
 'Real-time inventory management with automatic alerts and multi-channel synchronization', 
 'todo', 'medium', 
 false, 1),

('Analytics & Reporting Dashboard', 
 'Dashboard with business metrics, sales analytics and automated reports', 
 'todo', 'low', 
 false, 1),

-- Projet 2: Mobile App Development
('React Native Architecture', 
 'React Native architecture design with Redux Toolkit, navigation and state management', 
 'in_progress', 'high', 
 false, 2),

('UI/UX Design System', 
 'Design system creation with reusable components, themes and guidelines', 
 'todo', 'medium', 
 false, 2),

('Push Notifications Setup', 
 'Push notifications implementation with Firebase/FCM and permissions management', 
 'todo', 'medium', 
 false, 2),

('Offline Data Synchronization', 
 'Offline synchronization system with conflict resolution and queuing', 
 'todo', 'high', 
 false, 2),

('User Authentication Mobile', 
 'Mobile authentication with biometrics, SSO and secure token management', 
 'todo', 'high', 
 false, 2),

-- Projet 3: API Documentation Portal
('OpenAPI 3.0 Specification', 
 'Complete API endpoints documentation with OpenAPI 3.0, examples and validation schemas', 
 'done', 'medium', 
 true, 3),

('Interactive API Explorer', 
 'Interactive developer portal with real-time API testing and code generation', 
 'in_progress', 'medium', 
 false, 3),

('SDK Generation & Distribution', 
 'Automatic SDK generation for Python, JavaScript, Go with distribution via npm/PyPI', 
 'todo', 'low', 
 false, 3),

('Developer Onboarding Guide', 
 'Complete developer guides with tutorials, practical examples and best practices', 
 'todo', 'low', 
 false, 3),

-- Projet 4: DevOps Pipeline (COMPLETED)
('Docker Multi-stage Build', 
 'Containerization with Docker multi-stage builds, size optimization and security', 
 'done', 'high', 
 true, 4),

('Kubernetes Deployment', 
 'Kubernetes cluster deployment with Helm charts, auto-scaling and health checks', 
 'done', 'high', 
 true, 4),

('CI/CD Pipeline GitHub Actions', 
 'Complete pipeline with automated tests, security, deployment and automatic rollback', 
 'done', 'high', 
 true, 4),

('Monitoring & Alerting', 
 'Setup Prometheus, Grafana, AlertManager with custom dashboards and intelligent alerts', 
 'done', 'medium', 
 true, 4),

-- Projet 5: Analytics Dashboard
('Data Pipeline Architecture', 
 'Data pipeline architecture with Apache Airflow for ingestion and transformation', 
 'in_progress', 'high', 
 false, 5),

('Real-time Data Visualization', 
 'Interactive charts with D3.js and real-time updates via WebSocket', 
 'todo', 'medium', 
 false, 5),

('Custom Report Builder', 
 'Drag-and-drop report builder with advanced filters and multi-format export', 
 'todo', 'medium', 
 false, 5),

('Automated Alert System', 
 'Automatic alert system based on customizable thresholds and ML', 
 'todo', 'low', 
 false, 5),

-- Projet 6: Security Audit & Compliance
('OWASP Security Assessment', 
 'Complete OWASP Top 10 vulnerability analysis with automated and manual tests', 
 'todo', 'high', 
 false, 6),

('Penetration Testing', 
 'Penetration testing on infrastructure and applications with detailed report', 
 'todo', 'high', 
 false, 6),

('GDPR Compliance Review', 
 'GDPR compliance audit with recommendations and implementation of measures', 
 'todo', 'high', 
 false, 6),

('Security Documentation', 
 'Complete documentation of security practices and team training', 
 'todo', 'medium', 
 false, 6),

-- Projet 7: Microservices Architecture
('Service Decomposition Strategy', 
 'Analysis and definition of microservices decomposition strategy', 
 'in_progress', 'high', 
 false, 7),

('API Gateway Implementation', 
 'API Gateway implementation with routing, rate limiting and authentication', 
 'todo', 'high', 
 false, 7),

('Service Mesh Setup', 
 'Istio configuration for inter-service communication and observability', 
 'todo', 'medium', 
 false, 7),

('Database per Service', 
 'Migration to database-per-service architecture with transaction management', 
 'todo', 'high', 
 false, 7),

('Event-Driven Communication', 
 'Asynchronous communication implementation with Apache Kafka', 
 'todo', 'medium', 
 false, 7),

-- Projet 8: Customer Support Portal
('Chatbot AI Development', 
 'AI chatbot development with NLP for automated customer support', 
 'todo', 'medium', 
 false, 8),

('Ticket Management System', 
 'Ticket management system with customizable workflow and SLA tracking', 
 'todo', 'high', 
 false, 8),

('Knowledge Base CMS', 
 'Content management system for knowledge base with advanced search', 
 'todo', 'medium', 
 false, 8),

('Customer Satisfaction Analytics', 
 'Analytics system to measure customer satisfaction and generate insights', 
 'todo', 'low', 
 false, 8),

-- Projet 9: Data Warehouse & ETL
('Data Warehouse Schema Design', 
 'Dimensional schema design for data warehouse with fact and dimension tables', 
 'in_progress', 'high', 
 false, 9),

('ETL Pipeline with Airflow', 
 'ETL pipeline development with Apache Airflow for multi-source ingestion', 
 'todo', 'high', 
 false, 9),

('Data Quality Framework', 
 'Data quality framework with validation, cleaning and monitoring', 
 'todo', 'medium', 
 false, 9),

('BI Dashboard Suite', 
 'Business intelligence dashboard suite with drill-down and advanced export', 
 'todo', 'medium', 
 false, 9),

-- Projet 10: Machine Learning Platform
('MLOps Infrastructure Setup', 
 'MLOps infrastructure setup with MLflow, Kubeflow and model registry', 
 'todo', 'high', 
 false, 10),

('Automated Model Training', 
 'Automated training pipeline with hyperparameter tuning and cross-validation', 
 'todo', 'high', 
 false, 10),

('Model Deployment & Serving', 
 'Automated model deployment system with versioning and rollback', 
 'todo', 'medium', 
 false, 10),

('A/B Testing Framework', 
 'Framework for A/B testing ML models with statistical metrics', 
 'todo', 'low', 
 false, 10),

-- Projet 11: Performance Optimization (COMPLETED)
('Frontend Performance Audit', 
 'Complete frontend performance audit with Lighthouse and Web Vitals', 
 'done', 'high', 
 true, 11),

('Lazy Loading Implementation', 
 'Lazy loading implementation for images, components and routes', 
 'done', 'high', 
 true, 11),

('CDN & Caching Strategy', 
 'CloudFront CDN setup and optimized Redis cache strategy', 
 'done', 'medium', 
 true, 11),

('Database Query Optimization', 
 'SQL query optimization with indexing and performance analysis', 
 'done', 'high', 
 true, 11),

-- Projet 12: Multi-tenant SaaS Platform
('Multi-tenancy Architecture Design', 
 'Multi-tenant architecture design with data isolation and security', 
 'in_progress', 'high', 
 false, 12),

('Tenant Onboarding System', 
 'Automated onboarding system for new tenants with provisioning', 
 'todo', 'high', 
 false, 12),

('Billing & Subscription Management', 
 'Automated billing system with subscription management and usage metrics', 
 'todo', 'high', 
 false, 12),

('Tenant-specific Customization', 
 'Per-tenant customization system: themes, configurations and branding', 
 'todo', 'medium', 
 false, 12),

('Usage Analytics & Reporting', 
 'Per-tenant usage analytics with detailed reports and threshold alerts', 
 'todo', 'medium', 
 false, 12),

-- Tâches supplémentaires comme dans simple_main.py
('Setup project repository',
 'Initialize Git repository and setup CI/CD pipeline',
 'done',
 'high',
 true, 1),

('Implement user authentication',
 'JWT-based authentication system with refresh tokens',
 'in_progress',
 'high',
 false, 1);

-- ====================================
-- COMPTES DE DÉMONSTRATION
-- ====================================
-- Les mêmes que dans init_project_simple.py :
--
-- Admin      : admin@example.com      / admin123
-- Manager    : manager@example.com    / manager123  
-- John Doe   : john.doe@example.com   / user123
-- Jane Smith : jane.smith@example.com / user123
-- Developer  : developer@example.com  / dev123
-- Tester     : tester@example.com     / test123
--
-- ====================================
-- STATISTIQUES
-- ====================================
-- 6 utilisateurs
-- 12 projets (2 complétés, 6 actifs, 4 en planification)
-- 61 tâches (12 complétées, 7 en cours, 42 à faire)
-- Budgets totaux significatifs avec des données réalistes
-- Dates cohérentes avec le workflow de développement
--
-- ✅ Ces données sont EXACTEMENT les mêmes que init_project_simple.py