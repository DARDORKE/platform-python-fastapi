# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **portfolio demonstration project** showcasing modern full-stack development skills. Built with FastAPI and React, it demonstrates:
- FastAPI backend with PostgreSQL database and Redis cache
- React frontend with TypeScript and modern state management
- Complete CRUD operations for projects and tasks management
- JWT authentication with role-based access control
- Docker containerization and service orchestration

**Important**: This project serves as a **technical demonstration** for portfolio purposes, not as a production enterprise application.

## Current Architecture & Services

### Active Services
The project currently runs with these core services:
- **Backend (FastAPI)**: Main API server with demo data
- **Frontend (React)**: Modern web interface with TypeScript
- **Database (PostgreSQL)**: Data persistence layer
- **Redis**: Caching and session storage

### Simplified Commands

Since this is a demo project, the main commands are simplified:

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View service status
docker-compose ps

# View logs
docker-compose logs [service_name]

# Rebuild after changes
docker-compose build [service_name]
docker-compose down && docker-compose up -d
```

## Development Workflow

### Starting Development
1. Run `docker-compose up -d` to start all services
2. Verify services are running with `docker-compose ps`
3. Access the API at http://localhost:8000
4. Access the frontend at http://localhost:3000
5. View API documentation at http://localhost:8000/docs

### Demo Accounts (Pre-loaded)
- **Admin**: admin@example.com / admin123
- **Manager**: manager@example.com / manager123
- **User**: john.doe@example.com / user123

### Making Changes
1. **Backend changes**: Modify files in `backend/` then rebuild with `docker-compose build backend`
2. **Frontend changes**: Modify files in `frontend/src/` then rebuild with `docker-compose build frontend`
3. **Always restart services**: `docker-compose down && docker-compose up -d` after builds

## Architecture Details

### Backend (FastAPI)
- **Main file**: `backend/simple_main.py` (contains full API with demo data)
- **Dependencies**: Listed in `backend/requirements.txt`
- **Key features**: 
  - FastAPI with Pydantic validation
  - JWT authentication with multiple endpoints
  - Complete CRUD APIs for users, projects, tasks
  - Demo data embedded in the application
  - CORS configured for frontend integration

### Frontend (React + TypeScript)
- **Location**: `frontend/src/`
- **Build tool**: Vite for fast development
- **State management**: Zustand stores in `src/store/`
- **Key features**:
  - Modern React 18 with TypeScript
  - Tailwind CSS for styling
  - Responsive dashboard and CRUD interfaces
  - API integration with error handling

### Database & Cache
- **PostgreSQL**: Primary data storage (though demo uses in-memory data)
- **Redis**: Available for caching and sessions
- **Data**: Demo data is embedded in the backend application

## API Endpoints Available

### Authentication
- `POST /api/v1/auth/login` - Standard login
- `POST /api/v1/auth/login/json` - JSON login (frontend compatible)
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Token refresh

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/me` - Current user profile

### Projects
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project details
- `POST /api/v1/projects` - Create project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Tasks
- `GET /api/v1/tasks` - List tasks (with optional project filter)
- `GET /api/v1/tasks/{id}` - Get task details
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `GET /api/v1/tasks/stats/me` - Task statistics

### Dashboard
- `GET /api/v1/dashboard/stats` - General statistics

## Current Features Implemented

### ✅ Fully Functional
- **Authentication**: JWT with multiple login endpoints
- **User Management**: Complete user system with roles
- **Project Management**: Full CRUD operations
- **Task Management**: Full CRUD with project relationships
- **Dashboard**: Real-time statistics from API
- **Frontend Interface**: Modern React UI with all features
- **API Documentation**: Auto-generated Swagger docs

### ⚠️ Demo/Simplified
- **Data Persistence**: Uses in-memory demo data (resets on restart)
- **Security**: Basic JWT implementation (demo tokens)
- **File Structure**: Simplified for demonstration purposes

## Service URLs (Development)
- **API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432
- **Redis**: Port 6379

## Important Development Notes

### When Working with This Project:
1. **This is a DEMO project** - focus on showcasing technical skills
2. **Always rebuild containers** after code changes
3. **Use `docker-compose down && docker-compose up -d`** for reliable restarts
4. **Demo data resets** on each restart (this is intentional)
5. **Frontend/backend routes are aligned** - both use the same API contract

### File Structure (Current)
```
├── backend/
│   ├── simple_main.py          # Main API with all endpoints and demo data
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── app/                   # Modular structure (ready for expansion)
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── store/            # Zustand state management
│   │   ├── lib/              # API configuration
│   │   └── types/            # TypeScript definitions
│   ├── Dockerfile            # Frontend container
│   └── package.json          # Node.js dependencies
├── docker-compose.yml         # Service orchestration
└── CLAUDE.md                  # This file
```

## Testing the Application

### Quick Verification Commands:
```bash
# Test backend API
curl http://localhost:8000/api/v1/dashboard/stats

# Test authentication
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test projects API
curl http://localhost:8000/api/v1/projects
```

### Frontend Testing:
1. Open http://localhost:3000
2. Login with demo credentials
3. Navigate through dashboard, projects, and tasks
4. Verify all CRUD operations work

## Future Expansion Possibilities

The current structure is designed to be easily expandable with:
- Real database persistence with SQLAlchemy models
- Advanced authentication (OAuth, 2FA)
- File upload capabilities
- Real-time features with WebSockets
- Mobile React Native app
- Advanced monitoring and logging
- CI/CD pipelines
- Kubernetes deployment

---

**This project successfully demonstrates modern full-stack development skills with FastAPI, React, TypeScript, Docker, and PostgreSQL.**