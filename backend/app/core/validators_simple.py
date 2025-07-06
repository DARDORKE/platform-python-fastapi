"""
Simplified validators for testing FastAPI advanced features.
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PaginationParams(BaseModel):
    """Paramètres de pagination avec validation."""
    
    page: int = Field(1, ge=1, le=1000, description="Numéro de page")
    size: int = Field(10, ge=1, le=100, description="Taille de la page")
    
    @property
    def offset(self) -> int:
        """Calculer l'offset pour la base de données."""
        return (self.page - 1) * self.size


class SearchParams(BaseModel):
    """Paramètres de recherche avec validation."""
    
    q: Optional[str] = Field(None, min_length=1, max_length=100, description="Terme de recherche")
    fields: Optional[list[str]] = Field(None, description="Champs à rechercher")


class CreateUserSimple(BaseModel):
    """Schéma simplifié pour la création d'utilisateur."""
    
    email: str = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., min_length=8, description="Mot de passe")
    first_name: str = Field(..., min_length=2, max_length=50, description="Prénom")
    last_name: str = Field(..., min_length=2, max_length=50, description="Nom")
    phone: Optional[str] = Field(None, description="Numéro de téléphone")


class CreateProjectSimple(BaseModel):
    """Schéma simplifié pour la création de projet."""
    
    name: str = Field(..., min_length=3, max_length=100, description="Nom du projet")
    description: Optional[str] = Field(None, max_length=1000, description="Description")
    budget: Optional[float] = Field(None, gt=0, description="Budget du projet")
    priority: str = Field("medium", description="Priorité du projet")


class CreateTaskSimple(BaseModel):
    """Schéma simplifié pour la création de tâche."""
    
    title: str = Field(..., min_length=3, max_length=200, description="Titre de la tâche")
    description: Optional[str] = Field(None, max_length=2000, description="Description détaillée")
    priority: str = Field("medium", description="Priorité de la tâche")
    estimated_hours: Optional[float] = Field(None, gt=0, le=1000, description="Heures estimées")
    due_date: Optional[datetime] = Field(None, description="Date d'échéance")