#!/usr/bin/env python3
"""
NUNC CV Converter - Quick Start
Einfacher Start für morgen mit automatischer Fehlerbehandlung
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Zeigt NUNC Banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NUNC CONSULTING GmbH                     ║
    ║                                                              ║
    ║              🚀 QUICK START - CV CONVERTER 🚀                ║
    ║                                                              ║
    ║        PDF → NUNC Template → Word → Supabase → Search        ║
    ║                                                              ║
    ║              🔧 Auto-Fix & Ready to Go! 🔧                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def quick_install():
    """Schnelle Installation aller Pakete"""
    print("📦 Installiere alle benötigten Pakete...")
    
    packages = [
        'PyPDF2', 'pdfplumber', 'python-docx', 'docxtpl',
        'supabase', 'openai', 'sentence-transformers', 'flask',
        'numpy', 'scipy', 'scikit-learn', 'transformers'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ], check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️ {package} - versuche ohne --quiet...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], check=True)
                print(f"✅ {package}")
            except subprocess.CalledProcessError:
                print(f"❌ {package} - manuell installieren: pip install {package}")

def create_directories():
    """Erstellt alle notwendigen Verzeichnisse"""
    print("📁 Erstelle Verzeichnisse...")
    
    base_dir = Path(__file__).parent
    directories = [
        'generated_profiles',
        'word_documents', 
        'html_templates',
        'test_results/input',
        'test_results/output',
        'uploads',
        'downloads',
        'logs'
    ]
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")

def start_web_interface():
    """Startet Web-Interface"""
    print("🌐 Starte Web-Interface...")
    
    base_dir = Path(__file__).parent.parent
    web_script = base_dir / '02_Web_Interface' / 'web_interface.py'
    
    if web_script.exists():
        print("✅ Web-Interface gefunden")
        print("🌐 Öffne http://localhost:5000 in 2 Sekunden...")
        
        # Browser öffnen
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        threading.Thread(target=open_browser).start()
        
        # Web-Interface starten
        try:
            subprocess.run([sys.executable, str(web_script)])
        except KeyboardInterrupt:
            print("\n🛑 Web-Interface gestoppt")
    else:
        print("❌ Web-Interface nicht gefunden")
        print(f"Erwartet: {web_script}")

def main():
    """Hauptfunktion für Quick Start"""
    print_banner()
    
    print("🚀 NUNC CV Converter - Quick Start")
    print("=" * 50)
    
    # 1. Pakete installieren
    quick_install()
    
    # 2. Verzeichnisse erstellen
    create_directories()
    
    # 3. Web-Interface starten
    start_web_interface()

if __name__ == "__main__":
    main()

