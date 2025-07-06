#!/usr/bin/env python3
"""
Script de démarrage pour Railway
"""
import os
import sys
import subprocess

def main():
    """Démarrer l'application"""
    # Aller dans le dossier backend
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Ajouter au Python path
    sys.path.insert(0, backend_dir)
    
    # Démarrer uvicorn
    port = os.getenv("PORT", "8080")
    cmd = [
        "uvicorn", 
        "main_cloud:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ]
    
    print(f"🚀 Starting: {' '.join(cmd)}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Exécuter la commande
    subprocess.run(cmd)

if __name__ == "__main__":
    main()