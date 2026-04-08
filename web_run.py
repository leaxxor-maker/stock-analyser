#!/usr/bin/env python
"""
Lance l'interface web de Stock Analyzer
"""
import subprocess
import sys
import os

def main():
    # Vérifier les dépendances
    try:
        import flask
        import yfinance
        import rich
        import tabulate
    except ImportError:
        print("Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "yfinance", "rich", "tabulate"])
    
    # Lancer le serveur web
    print("=" * 60)
    print("  📊 STOCK ANALYZER - Interface Web")
    print("=" * 60)
    print()
    print("  Lancement du serveur...")
    print("  Ouvrez votre navigateur à: http://localhost:5000")
    print()
    print("  Ctrl+C pour arrêter")
    print("=" * 60)
    print()
    
    from web import app
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
