#!/usr/bin/env python3
"""
Démarrage direct de l'application sans uvicorn CLI
"""
import os
import sys

def main():
    """Démarrer l'application directement"""
    # Aller dans le dossier backend
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_dir)
    
    print(f"📁 Backend directory: {backend_dir}")
    print(f"🐍 Python path: {sys.path[:3]}")
    
    try:
        # Importer l'application
        print("📦 Importing main_cloud...")
        from main_cloud import app
        print("✅ Import successful!")
        
        # Démarrer avec uvicorn programmatically
        print("🚀 Starting uvicorn...")
        import uvicorn
        
        port = int(os.getenv("PORT", "8080"))
        print(f"🔌 Port: {port}")
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()