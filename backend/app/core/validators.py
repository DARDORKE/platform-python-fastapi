"""
Custom validators for advanced data validation.
"""
import re
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.networks import EmailStr
from fastapi import HTTPException, status
from datetime import datetime, timedelta


class PasswordValidator:
    """Validateur avancé pour les mots de passe."""
    
    @staticmethod
    def validate_password_strength(password: str) -> str:
        """
        Valider la force du mot de passe.
        
        Critères:
        - Au moins 8 caractères
        - Au moins une majuscule
        - Au moins une minuscule
        - Au moins un chiffre
        - Au moins un caractère spécial
        """
        if len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        
        if not re.search(r'[A-Z]', password):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        
        if not re.search(r'[a-z]', password):
            raise ValueError("Le mot de passe doit contenir au moins une minuscule")
        
        if not re.search(r'\d', password):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        
        return password


class EmailValidator:
    """Validateur avancé pour les emails."""
    
    @staticmethod
    def validate_email_domain(email: str) -> str:
        """Valider le domaine de l'email."""
        # Domaines interdits
        blocked_domains = [
            "tempmail.com", "10minutemail.com", "guerrillamail.com",
            "mailinator.com", "throwaway.email"
        ]
        
        domain = email.split('@')[1].lower()
        if domain in blocked_domains:
            raise ValueError(f"Le domaine {domain} n'est pas autorisé")
        
        return email


class PhoneValidator:
    """Validateur pour les numéros de téléphone."""
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        """Valider le format du numéro de téléphone."""
        # Format français simplifié
        phone_pattern = r'^(\+33|0)[1-9](?:[0-9]{8})$'
        
        if not re.match(phone_pattern, phone):
            raise ValueError("Format de téléphone invalide (format français attendu)")
        
        return phone


class DateValidator:
    """Validateur pour les dates."""
    
    @staticmethod
    def validate_future_date(date_value: datetime) -> datetime:
        """Valider que la date est dans le futur."""
        if date_value <= datetime.now():
            raise ValueError("La date doit être dans le futur")
        
        return date_value
    
    @staticmethod
    def validate_business_hours(date_value: datetime) -> datetime:
        """Valider que la date est dans les heures ouvrables."""
        # Lundi = 0, Dimanche = 6
        if date_value.weekday() > 4:  # Samedi ou dimanche
            raise ValueError("La date doit être un jour ouvrable")
        
        if date_value.hour < 8 or date_value.hour > 18:
            raise ValueError("L'heure doit être entre 8h et 18h")
        
        return date_value


class BudgetValidator:
    """Validateur pour les budgets."""
    
    @staticmethod
    def validate_budget_range(budget: float) -> float:
        """Valider que le budget est dans une plage acceptable."""
        if budget < 0:
            raise ValueError("Le budget ne peut pas être négatif")
        
        if budget > 1000000:  # 1M€
            raise ValueError("Le budget ne peut pas dépasser 1 000 000€")
        
        return budget


# Schémas avec validation avancée
class CreateUserAdvanced(BaseModel):
    """Schéma avancé pour la création d'utilisateur."""
    
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., min_length=8, description="Mot de passe")
    first_name: str = Field(..., min_length=2, max_length=50, description="Prénom")
    last_name: str = Field(..., min_length=2, max_length=50, description="Nom")
    phone: Optional[str] = Field(None, description="Numéro de téléphone")
    birth_date: Optional[datetime] = Field(None, description="Date de naissance")
    company: Optional[str] = Field(None, max_length=100, description="Entreprise")
    
    @validator('email')
    def validate_email(cls, v):
        """Valider l'email."""
        return EmailValidator.validate_email_domain(v)
    
    @validator('password')
    def validate_password(cls, v):
        """Valider le mot de passe."""
        return PasswordValidator.validate_password_strength(v)
    
    @validator('phone')
    def validate_phone(cls, v):
        """Valider le téléphone."""
        if v:
            return PhoneValidator.validate_phone(v)
        return v
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Valider la date de naissance."""
        if v:
            if v > datetime.now():
                raise ValueError("La date de naissance ne peut pas être dans le futur")
            
            # Vérifier l'âge minimum (13 ans)
            min_age = datetime.now() - timedelta(days=13*365)
            if v > min_age:
                raise ValueError("L'utilisateur doit avoir au moins 13 ans")
        
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Valider les noms."""
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\']+$', v):
            raise ValueError("Le nom ne peut contenir que des lettres, espaces, tirets et apostrophes")
        return v.title()  # Capitaliser


class CreateProjectAdvanced(BaseModel):
    """Schéma avancé pour la création de projet."""
    
    name: str = Field(..., min_length=3, max_length=100, description="Nom du projet")
    description: Optional[str] = Field(None, max_length=1000, description="Description")
    budget: Optional[float] = Field(None, gt=0, description="Budget du projet")
    start_date: Optional[datetime] = Field(None, description="Date de début")
    end_date: Optional[datetime] = Field(None, description="Date de fin")
    client_email: Optional[EmailStr] = Field(None, description="Email du client")
    priority: str = Field("medium", pattern="^(low|medium|high|urgent)$")
    
    @validator('budget')
    def validate_budget(cls, v):
        """Valider le budget."""
        if v:
            return BudgetValidator.validate_budget_range(v)
        return v
    
    @validator('start_date')
    def validate_start_date(cls, v):
        """Valider la date de début."""
        if v:
            return DateValidator.validate_future_date(v)
        return v
    
    @root_validator
    def validate_dates(cls, values):
        """Valider la cohérence des dates."""
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise ValueError("La date de fin doit être après la date de début")
            
            # Vérifier que la durée n'est pas trop longue (max 5 ans)
            if (end_date - start_date).days > 5 * 365:
                raise ValueError("La durée du projet ne peut pas dépasser 5 ans")
        
        return values


class CreateTaskAdvanced(BaseModel):
    """Schéma avancé pour la création de tâche."""
    
    title: str = Field(..., min_length=3, max_length=200, description="Titre de la tâche")
    description: Optional[str] = Field(None, max_length=2000, description="Description détaillée")
    priority: str = Field("medium", pattern="^(low|medium|high|urgent)$")
    estimated_hours: Optional[float] = Field(None, gt=0, le=1000, description="Heures estimées")
    due_date: Optional[datetime] = Field(None, description="Date d'échéance")
    tags: Optional[list[str]] = Field(None, description="Tags pour la tâche")
    
    @validator('due_date')
    def validate_due_date(cls, v):
        """Valider la date d'échéance."""
        if v:
            return DateValidator.validate_future_date(v)
        return v
    
    @validator('tags')
    def validate_tags(cls, v):
        """Valider les tags."""
        if v:
            # Limiter le nombre de tags
            if len(v) > 10:
                raise ValueError("Maximum 10 tags autorisés")
            
            # Valider chaque tag
            for tag in v:
                if not re.match(r'^[a-zA-Z0-9_-]+$', tag):
                    raise ValueError("Les tags ne peuvent contenir que des lettres, chiffres, tirets et underscores")
                
                if len(tag) > 20:
                    raise ValueError("Les tags ne peuvent pas dépasser 20 caractères")
        
        return v


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
    
    @validator('q')
    def validate_search_query(cls, v):
        """Valider la requête de recherche."""
        if v:
            # Interdire les caractères dangereux
            if re.search(r'[<>"\']', v):
                raise ValueError("Caractères non autorisés dans la recherche")
        
        return v
    
    @validator('fields')
    def validate_search_fields(cls, v):
        """Valider les champs de recherche."""
        if v:
            allowed_fields = ['title', 'description', 'name', 'email']
            for field in v:
                if field not in allowed_fields:
                    raise ValueError(f"Champ de recherche non autorisé: {field}")
        
        return v