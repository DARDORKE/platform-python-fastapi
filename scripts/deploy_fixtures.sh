#!/bin/bash
# Script to deploy fixtures to the database

set -e

echo "🚀 Deploying fixtures to database..."

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
    echo "⚠️  Docker Compose services are not running. Starting them..."
    docker-compose up -d
    echo "⏳ Waiting for services to be ready..."
    sleep 10
fi

# Check if backend container is running
if ! docker-compose ps backend | grep -q "Up"; then
    echo "❌ Backend container is not running"
    exit 1
fi

# Run the fixtures script inside the backend container (mount the script as volume)
echo "🔧 Running fixtures deployment..."
docker-compose exec -T backend python /app/scripts/deploy_fixtures.py

echo "✅ Fixtures deployment completed!"
echo ""
echo "🌐 You can now access:"
echo "├── Frontend: http://localhost:3000"
echo "├── Backend API: http://localhost:8000"
echo "└── API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Demo accounts:"
echo "├── Admin: admin@example.com / admin123"
echo "├── Manager: manager@example.com / manager123"
echo "├── User 1: john.doe@example.com / user123"
echo "├── User 2: jane.smith@example.com / user123"
echo "└── Developer: developer@example.com / dev123"