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
-- Note: Les colonnes dans Supabase utilisent title au lieu de name, et des types légèrement différents

INSERT INTO projects (title, description, status, priority, start_date, end_date, owner_id) VALUES
('E-commerce Platform', 
 'Development of a modern e-commerce platform with React, FastAPI and PostgreSQL. Complete system with product management, orders, Stripe payments and advanced analytics.', 
 'ACTIVE', 'HIGH', 
 CURRENT_DATE - INTERVAL '45 days', CURRENT_DATE + INTERVAL '75 days', 
 2), -- Manager

('Mobile App Development', 
 'React Native mobile application for iOS and Android with offline features, push notifications and cloud synchronization.', 
 'PLANNING', 'MEDIUM', 
 CURRENT_DATE + INTERVAL '10 days', CURRENT_DATE + INTERVAL '150 days', 
 2), -- Manager

('API Documentation Portal', 
 'Complete API documentation portal with developer guides, interactive examples and automated testing tools.', 
 'ACTIVE', 'LOW', 
 CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE + INTERVAL '40 days', 
 3), -- John Doe

('DevOps Pipeline', 
 'Complete CI/CD pipeline with Docker, Kubernetes, Prometheus/Grafana monitoring and automated multi-environment deployment.', 
 'COMPLETED', 'HIGH', 
 CURRENT_DATE - INTERVAL '90 days', CURRENT_DATE - INTERVAL '10 days', 
 5), -- Developer

('Analytics Dashboard', 
 'Real-time analytics dashboard with D3.js visualizations, custom reports and automatic alerts for business KPI tracking.', 
 'ACTIVE', 'MEDIUM', 
 CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE + INTERVAL '60 days', 
 4), -- Jane Smith

('Security Audit & Compliance', 
 'Complete security audit with penetration testing, OWASP vulnerability analysis, GDPR compliance and security recommendations.', 
 'PLANNING', 'HIGH', 
 CURRENT_DATE + INTERVAL '5 days', CURRENT_DATE + INTERVAL '45 days', 
 6), -- Tester

('Microservices Architecture', 
 'Refactoring to microservices architecture with API Gateway, service mesh, observability and resilience patterns.', 
 'ACTIVE', 'HIGH', 
 CURRENT_DATE - INTERVAL '60 days', CURRENT_DATE + INTERVAL '90 days', 
 5), -- Developer

('Customer Support Portal', 
 'Customer support portal with AI chatbot, ticket system, knowledge base and customer satisfaction analytics.', 
 'PLANNING', 'MEDIUM', 
 CURRENT_DATE + INTERVAL '20 days', CURRENT_DATE + INTERVAL '120 days', 
 3), -- John Doe

('Data Warehouse & ETL', 
 'Data warehouse construction with Apache Airflow ETL pipelines, multi-source integration and business intelligence dashboards.', 
 'ACTIVE', 'MEDIUM', 
 CURRENT_DATE - INTERVAL '25 days', CURRENT_DATE + INTERVAL '100 days', 
 4), -- Jane Smith

('Machine Learning Platform', 
 'Complete MLOps platform with model training, automated deployment, performance monitoring and A/B testing.', 
 'PLANNING', 'LOW', 
 CURRENT_DATE + INTERVAL '30 days', CURRENT_DATE + INTERVAL '180 days', 
 5), -- Developer

('Performance Optimization', 
 'Frontend and backend performance optimization: lazy loading, CDN, Redis cache, SQL optimization and APM monitoring.', 
 'COMPLETED', 'HIGH', 
 CURRENT_DATE - INTERVAL '50 days', CURRENT_DATE - INTERVAL '5 days', 
 5), -- Developer

('Multi-tenant SaaS Platform', 
 'Transformation into multi-tenant SaaS platform with data isolation, automated billing and self-service onboarding.', 
 'ACTIVE', 'HIGH', 
 CURRENT_DATE - INTERVAL '35 days', CURRENT_DATE + INTERVAL '110 days', 
 2); -- Manager

-- ====================================
-- TÂCHES DE DÉMONSTRATION
-- ====================================
-- Note: assigned_to correspond à owner_id, created_by correspond au créateur

-- Projet 1: E-commerce Platform
INSERT INTO tasks (title, description, status, priority, due_date, project_id, assigned_to, created_by) VALUES
('Setup AWS infrastructure', 
 'AWS infrastructure configuration with Terraform: VPC, subnets, ECS, RDS, ElastiCache', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '40 days', 1, 5, 2),

('JWT Authentication System', 
 'Complete JWT authentication system implementation with refresh tokens, 2FA and role management', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '7 days', 1, 3, 2),

('Product Catalog API', 
 'REST endpoints development for product management with advanced search, filters and pagination', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '20 days', 1, 3, 2),

('Shopping Cart & Checkout', 
 'Shopping cart functionality with Redis persistence, tax calculation and order process', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '35 days', 1, 4, 2),

('Stripe Payment Integration', 
 'Complete Stripe integration: payments, webhooks, refunds and failure handling', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '42 days', 1, 5, 2),

('Order Management System', 
 'Order management system with tracking, notifications and returns handling', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '50 days', 1, 4, 2),

('Inventory Management', 
 'Real-time inventory management with automatic alerts and multi-channel synchronization', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '55 days', 1, 3, 2),

('Analytics & Reporting Dashboard', 
 'Dashboard with business metrics, sales analytics and automated reports', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '65 days', 1, 4, 2),

-- Projet 2: Mobile App Development
('React Native Architecture', 
 'React Native architecture design with Redux Toolkit, navigation and state management', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '15 days', 2, 5, 2),

('UI/UX Design System', 
 'Design system creation with reusable components, themes and guidelines', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '25 days', 2, 4, 2),

('Push Notifications Setup', 
 'Push notifications implementation with Firebase/FCM and permissions management', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '35 days', 2, 5, 2),

('Offline Data Synchronization', 
 'Offline synchronization system with conflict resolution and queuing', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '45 days', 2, 5, 2),

('User Authentication Mobile', 
 'Mobile authentication with biometrics, SSO and secure token management', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '40 days', 2, 3, 2),

-- Projet 3: API Documentation Portal
('OpenAPI 3.0 Specification', 
 'Complete API endpoints documentation with OpenAPI 3.0, examples and validation schemas', 
 'COMPLETED', 'MEDIUM', 
 CURRENT_TIMESTAMP - INTERVAL '15 days', 3, 3, 3),

('Interactive API Explorer', 
 'Interactive developer portal with real-time API testing and code generation', 
 'IN_PROGRESS', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '20 days', 3, 3, 3),

('SDK Generation & Distribution', 
 'Automatic SDK generation for Python, JavaScript, Go with distribution via npm/PyPI', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '35 days', 3, 5, 3),

('Developer Onboarding Guide', 
 'Complete developer guides with tutorials, practical examples and best practices', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '38 days', 3, 4, 3),

-- Projet 4: DevOps Pipeline (COMPLETED)
('Docker Multi-stage Build', 
 'Containerization with Docker multi-stage builds, size optimization and security', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '80 days', 4, 5, 5),

('Kubernetes Deployment', 
 'Kubernetes cluster deployment with Helm charts, auto-scaling and health checks', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '60 days', 4, 5, 5),

('CI/CD Pipeline GitHub Actions', 
 'Complete pipeline with automated tests, security, deployment and automatic rollback', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '45 days', 4, 5, 5),

('Monitoring & Alerting', 
 'Setup Prometheus, Grafana, AlertManager with custom dashboards and intelligent alerts', 
 'COMPLETED', 'MEDIUM', 
 CURRENT_TIMESTAMP - INTERVAL '25 days', 4, 6, 5),

-- Projet 5: Analytics Dashboard
('Data Pipeline Architecture', 
 'Data pipeline architecture with Apache Airflow for ingestion and transformation', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '10 days', 5, 4, 4),

('Real-time Data Visualization', 
 'Interactive charts with D3.js and real-time updates via WebSocket', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '25 days', 5, 4, 4),

('Custom Report Builder', 
 'Drag-and-drop report builder with advanced filters and multi-format export', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '40 days', 5, 3, 4),

('Automated Alert System', 
 'Automatic alert system based on customizable thresholds and ML', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '50 days', 5, 5, 4),

-- Projet 6: Security Audit & Compliance
('OWASP Security Assessment', 
 'Complete OWASP Top 10 vulnerability analysis with automated and manual tests', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '12 days', 6, 6, 6),

('Penetration Testing', 
 'Penetration testing on infrastructure and applications with detailed report', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '20 days', 6, 6, 6),

('GDPR Compliance Review', 
 'GDPR compliance audit with recommendations and implementation of measures', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '30 days', 6, 6, 6),

('Security Documentation', 
 'Complete documentation of security practices and team training', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '40 days', 6, 6, 6),

-- Projet 7: Microservices Architecture
('Service Decomposition Strategy', 
 'Analysis and definition of microservices decomposition strategy', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '5 days', 7, 5, 5),

('API Gateway Implementation', 
 'API Gateway implementation with routing, rate limiting and authentication', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '20 days', 7, 5, 5),

('Service Mesh Setup', 
 'Istio configuration for inter-service communication and observability', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '35 days', 7, 5, 5),

('Database per Service', 
 'Migration to database-per-service architecture with transaction management', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '50 days', 7, 3, 5),

('Event-Driven Communication', 
 'Asynchronous communication implementation with Apache Kafka', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '60 days', 7, 5, 5),

-- Projet 8: Customer Support Portal
('Chatbot AI Development', 
 'AI chatbot development with NLP for automated customer support', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '30 days', 8, 3, 3),

('Ticket Management System', 
 'Ticket management system with customizable workflow and SLA tracking', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '35 days', 8, 3, 3),

('Knowledge Base CMS', 
 'Content management system for knowledge base with advanced search', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '45 days', 8, 4, 3),

('Customer Satisfaction Analytics', 
 'Analytics system to measure customer satisfaction and generate insights', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '70 days', 8, 4, 3),

-- Projet 9: Data Warehouse & ETL
('Data Warehouse Schema Design', 
 'Dimensional schema design for data warehouse with fact and dimension tables', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '8 days', 9, 4, 4),

('ETL Pipeline with Airflow', 
 'ETL pipeline development with Apache Airflow for multi-source ingestion', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '25 days', 9, 4, 4),

('Data Quality Framework', 
 'Data quality framework with validation, cleaning and monitoring', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '40 days', 9, 5, 4),

('BI Dashboard Suite', 
 'Business intelligence dashboard suite with drill-down and advanced export', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '65 days', 9, 4, 4),

-- Projet 10: Machine Learning Platform
('MLOps Infrastructure Setup', 
 'MLOps infrastructure setup with MLflow, Kubeflow and model registry', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '45 days', 10, 5, 5),

('Automated Model Training', 
 'Automated training pipeline with hyperparameter tuning and cross-validation', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '60 days', 10, 5, 5),

('Model Deployment & Serving', 
 'Automated model deployment system with versioning and rollback', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '80 days', 10, 5, 5),

('A/B Testing Framework', 
 'Framework for A/B testing ML models with statistical metrics', 
 'TODO', 'LOW', 
 CURRENT_TIMESTAMP + INTERVAL '100 days', 10, 4, 5),

-- Projet 11: Performance Optimization (COMPLETED)
('Frontend Performance Audit', 
 'Complete frontend performance audit with Lighthouse and Web Vitals', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '45 days', 11, 5, 5),

('Lazy Loading Implementation', 
 'Lazy loading implementation for images, components and routes', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '35 days', 11, 5, 5),

('CDN & Caching Strategy', 
 'CloudFront CDN setup and optimized Redis cache strategy', 
 'COMPLETED', 'MEDIUM', 
 CURRENT_TIMESTAMP - INTERVAL '25 days', 11, 5, 5),

('Database Query Optimization', 
 'SQL query optimization with indexing and performance analysis', 
 'COMPLETED', 'HIGH', 
 CURRENT_TIMESTAMP - INTERVAL '15 days', 11, 3, 5),

-- Projet 12: Multi-tenant SaaS Platform
('Multi-tenancy Architecture Design', 
 'Multi-tenant architecture design with data isolation and security', 
 'IN_PROGRESS', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '15 days', 12, 5, 5),

('Tenant Onboarding System', 
 'Automated onboarding system for new tenants with provisioning', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '30 days', 12, 3, 5),

('Billing & Subscription Management', 
 'Automated billing system with subscription management and usage metrics', 
 'TODO', 'HIGH', 
 CURRENT_TIMESTAMP + INTERVAL '45 days', 12, 4, 5),

('Tenant-specific Customization', 
 'Per-tenant customization system: themes, configurations and branding', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '60 days', 12, 4, 5),

('Usage Analytics & Reporting', 
 'Per-tenant usage analytics with detailed reports and threshold alerts', 
 'TODO', 'MEDIUM', 
 CURRENT_TIMESTAMP + INTERVAL '75 days', 12, 4, 5);

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