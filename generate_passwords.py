#!/usr/bin/env python3
"""
Script pour générer les mots de passe hashés avec bcrypt
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

passwords = {
    "admin123": "admin@example.com",
    "manager123": "manager@example.com", 
    "user123": "john.doe@example.com",
    "user123": "jane.smith@example.com",
    "dev123": "developer@example.com",
    "test123": "tester@example.com"
}

print("-- Mots de passe hashés avec bcrypt")
for password, email in passwords.items():
    hashed = pwd_context.hash(password)
    print(f"-- {email} -> {password}")
    print(f"'{hashed}',")
    print()