# start_nems.py
"""
NUNC Expert Management System - Starter Script
Startet das vollständige NEMS System
"""

import subprocess
import sys
import os
from pathlib import Path
import time
import webbrowser

def install_packages():
    """Installiert erforderliche Python-Pakete"""
    print("📦 Installiere Pakete...")
    required_packages = [
        "PyPDF2", "pdfplumber", "python-docx", "docxtpl",
        "supabase", "openai", "sentence-transformers", "flask",
        "requests", "beautifulsoup4", "smtplib"
    ]
    
    for package in required_packages:
        try:
            if package == "smtplib":
                # smtplib ist Teil der Standard-Bibliothek
                print(f"✅ {package} (Standard-Bibliothek)")
            else:
                __import__(package.replace('-', '_'))
                print(f"✅ {package}")
        except ImportError:
            print(f"🔄 Installiere {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installiert")

def create_directories():
    """Erstellt notwendige Verzeichnisse"""
    print("📁 Erstelle Verzeichnisse...")
    base_dir = Path(__file__).parent
    
    # Erstelle alle notwendigen Ordner
    directories = [
        "uploads", "generated_profiles", "word_documents", "html_templates",
        "test_results", "downloads", "templates", "profiles", "projects",
        "availability_requests", "candidate_search_results", "project_matches"
    ]
    
    for dir_name in directories:
        (base_dir / dir_name).mkdir(exist_ok=True)
        print(f"✅ {dir_name}")

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    NUNC CONSULTING GmbH                     ║
║                                                              ║
║              🚀 EXPERT MANAGEMENT SYSTEM 🚀                 ║
║                                                              ║
║        Profile → Availability → Candidates → Projects        ║
║                                                              ║
║              🔧 Vollständiges System 🔧                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    install_packages()
    create_directories()

    # Web-Interface starten
    print("🌐 Starte Web-Interface...")
    web_script = Path(__file__).parent.parent / '05_Shared_Components' / 'web_interface.py'
    
    if web_script.exists():
        print("✅ Web-Interface gefunden")
        
        # Setze den Port und Host für Flask
        port = "9000"
        host = "127.0.0.1"
        os.environ['FLASK_PORT'] = port
        os.environ['FLASK_HOST'] = host

        print(f"🌐 Starte auf Port {port} ({host}:{port})")
        print("🔧 Vollständiges Expert Management System")
        
        # Browser öffnen
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open(f'http://{host}:{port}')
                print("✅ Browser geöffnet")
            except Exception as e:
                print(f"❌ Fehler beim Öffnen des Browsers: {e}")
                print(f"Bitte manuell öffnen: http://{host}:{port}")
        
        import threading
        threading.Thread(target=open_browser).start()
        
        # Web-Interface starten
        try:
            print(f"🔄 Starte Flask auf Port {port}...")
            subprocess.run([sys.executable, str(web_script)])
        except KeyboardInterrupt:
            print("\n🛑 Gestoppt")
    else:
        print("❌ Web-Interface nicht gefunden")
        print("Bitte stellen Sie sicher, dass 'web_interface.py' im Ordner '05_Shared_Components' existiert.")

if __name__ == "__main__":
    main()

