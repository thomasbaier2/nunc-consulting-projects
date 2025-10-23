#!/usr/bin/env python3
"""
NUNC CV Converter - Start für Morgen
Einfachste Möglichkeit, das System zu starten
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Einfachster Start für morgen"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NUNC CONSULTING GmbH                     ║
    ║                                                              ║
    ║              🚀 MORGEN START - CV CONVERTER 🚀              ║
    ║                                                              ║
    ║        PDF → NUNC Template → Word → Supabase → Search        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("🚀 Starte NUNC CV Converter...")
    
    # Automatische Installation
    print("📦 Installiere Pakete...")
    packages = ['PyPDF2', 'pdfplumber', 'python-docx', 'docxtpl', 'supabase', 'openai', 'sentence-transformers', 'flask']
    
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package, '--quiet'], check=True, capture_output=True)
            print(f"✅ {package}")
        except:
            print(f"⚠️ {package} - manuell: pip install {package}")
    
    # Verzeichnisse erstellen
    print("📁 Erstelle Verzeichnisse...")
    base_dir = Path(__file__).parent
    for dir_name in ['generated_profiles', 'word_documents', 'html_templates', 'test_results', 'uploads', 'downloads']:
        (base_dir / dir_name).mkdir(exist_ok=True)
        print(f"✅ {dir_name}")
    
    # Web-Interface starten
    print("🌐 Starte Web-Interface...")
    web_script = Path(__file__).parent.parent / '02_Web_Interface' / 'web_interface.py'
    
    if web_script.exists():
        print("✅ Web-Interface gefunden")
        print("🌐 Starte auf Port 8080 (localhost:8080)")
        
        # Browser öffnen
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:8080')
        
        import threading
        threading.Thread(target=open_browser).start()
        
        # Web-Interface starten auf Port 8080
        try:
            print("🔄 Starte Flask auf Port 8080...")
            os.environ['FLASK_PORT'] = '8080'
            subprocess.run([sys.executable, str(web_script)])
        except KeyboardInterrupt:
            print("\n🛑 Gestoppt")
    else:
        print("❌ Web-Interface nicht gefunden")
        print("Versuche alternativen Start...")
        
        # Alternative: Robust System Starter
        robust_script = Path(__file__).parent / 'robust_system_starter.py'
        if robust_script.exists():
            print("🔄 Starte Robust System Starter...")
            subprocess.run([sys.executable, str(robust_script)])
        else:
            print("❌ Kein Web-Interface gefunden")

if __name__ == "__main__":
    main()
