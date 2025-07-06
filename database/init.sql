-- Database initialization script for portfolio platform
-- This creates the necessary database and user for the application

-- Create the application database if it doesn't exist
SELECT 'CREATE DATABASE portfolio_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'portfolio_db')\gexec

-- Create application user if it doesn't exist
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'portfolio_user') THEN

      CREATE ROLE portfolio_user LOGIN PASSWORD 'portfolio_password';
   END IF;
END
$do$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;

-- Connect to the new database to set up tables
\c portfolio_db;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO portfolio_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO portfolio_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO portfolio_user;

-- Default grants for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO portfolio_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO portfolio_user;