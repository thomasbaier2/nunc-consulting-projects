#!/usr/bin/env python3
"""
NUNC CV Converter - System Starter
Startet das komplette System mit allen Komponenten
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """Zeigt NUNC Banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NUNC CONSULTING GmbH                     ║
    ║                                                              ║
    ║              🚀 CV CONVERTER SYSTEM 🚀                       ║
    ║                                                              ║
    ║        PDF → NUNC Template → Word → Supabase → Search        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Überprüft Abhängigkeiten"""
    print("🔍 Überprüfe Abhängigkeiten...")
    
    required_packages = [
        'PyPDF2', 'pdfplumber', 'python-docx', 'docxtpl',
        'supabase', 'openai', 'sentence-transformers', 'flask'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Fehlende Pakete: {', '.join(missing_packages)}")
        print("📦 Installiere fehlende Pakete...")
        
        for package in missing_packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True, capture_output=True)
                print(f"✅ {package} installiert")
            except subprocess.CalledProcessError:
                print(f"❌ Fehler bei Installation von {package}")
    
    print("✅ Abhängigkeiten überprüft\n")

def create_directories():
    """Erstellt notwendige Verzeichnisse"""
    print("📁 Erstelle Verzeichnisse...")
    
    directories = [
        'generated_profiles',
        'word_documents', 
        'html_templates',
        'test_results/input',
        'test_results/output'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")
    
    print("✅ Verzeichnisse erstellt\n")

def run_tests():
    """Führt Tests aus"""
    print("🧪 Führe Tests aus...")
    
    try:
        # Test-Suite ausführen
        test_script = Path('../05_Testing/test_suite.py')
        if test_script.exists():
            result = subprocess.run([sys.executable, str(test_script)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Alle Tests erfolgreich")
            else:
                print(f"⚠️ Tests mit Warnungen: {result.stderr}")
        else:
            print("⚠️ Test-Suite nicht gefunden")
            
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
    
    print("✅ Tests abgeschlossen\n")

def start_web_interface():
    """Startet Web-Interface"""
    print("🌐 Starte Web-Interface...")
    
    try:
        # Web-Interface starten
        web_script = Path('../02_Web_Interface/web_interface.py')
        if web_script.exists():
            print("✅ Web-Interface wird gestartet...")
            print("🌐 Öffne http://localhost:5000")
            
            # Browser öffnen
            def open_browser():
                time.sleep(2)
                webbrowser.open('http://localhost:5000')
            
            threading.Thread(target=open_browser).start()
            
            # Web-Interface starten
            subprocess.run([sys.executable, str(web_script)])
        else:
            print("❌ Web-Interface nicht gefunden")
            
    except KeyboardInterrupt:
        print("\n🛑 Web-Interface gestoppt")
    except Exception as e:
        print(f"❌ Web-Interface Fehler: {e}")

def show_menu():
    """Zeigt Hauptmenü"""
    while True:
        print("\n" + "="*60)
        print("🎯 NUNC CV CONVERTER - HAUPTMENÜ")
        print("="*60)
        print("1. 🌐 Web-Interface starten")
        print("2. 🧪 Tests ausführen")
        print("3. 📄 Word-Generator testen")
        print("4. 🗄️ Supabase Integration testen")
        print("5. 📊 System-Status anzeigen")
        print("6. 📁 Verzeichnisstruktur anzeigen")
        print("7. 🚪 Beenden")
        print("="*60)
        
        choice = input("Wählen Sie eine Option (1-7): ").strip()
        
        if choice == '1':
            start_web_interface()
        elif choice == '2':
            run_tests()
        elif choice == '3':
            test_word_generator()
        elif choice == '4':
            test_supabase_integration()
        elif choice == '5':
            show_system_status()
        elif choice == '6':
            show_directory_structure()
        elif choice == '7':
            print("👋 Auf Wiedersehen!")
            break
        else:
            print("❌ Ungültige Auswahl")

def test_word_generator():
    """Testet Word-Generator"""
    print("📄 Teste Word-Generator...")
    
    try:
        word_script = Path('../03_Word_Generation/word_generator.py')
        if word_script.exists():
            subprocess.run([sys.executable, str(word_script)])
        else:
            print("❌ Word-Generator nicht gefunden")
    except Exception as e:
        print(f"❌ Word-Generator Fehler: {e}")

def test_supabase_integration():
    """Testet Supabase Integration"""
    print("🗄️ Teste Supabase Integration...")
    
    try:
        supabase_script = Path('../04_Supabase_Integration/supabase_integration.py')
        if supabase_script.exists():
            subprocess.run([sys.executable, str(supabase_script)])
        else:
            print("❌ Supabase Integration nicht gefunden")
    except Exception as e:
        print(f"❌ Supabase Integration Fehler: {e}")

def show_system_status():
    """Zeigt System-Status"""
    print("\n📊 SYSTEM-STATUS")
    print("="*40)
    
    # Python Version
    print(f"Python Version: {sys.version}")
    
    # Verzeichnisse
    directories = [
        '../01_Core_Components',
        '../02_Web_Interface', 
        '../03_Word_Generation',
        '../04_Supabase_Integration',
        '../05_Testing',
        '../06_Documentation'
    ]
    
    for directory in directories:
        if Path(directory).exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory}")
    
    # Output-Verzeichnisse
    output_dirs = [
        'generated_profiles',
        'word_documents',
        'html_templates',
        'test_results'
    ]
    
    print("\n📁 Output-Verzeichnisse:")
    for directory in output_dirs:
        if Path(directory).exists():
            files = list(Path(directory).glob('*'))
            print(f"✅ {directory} ({len(files)} Dateien)")
        else:
            print(f"❌ {directory}")

def show_directory_structure():
    """Zeigt Verzeichnisstruktur"""
    print("\n📁 VERZEICHNISSTRUKTUR")
    print("="*40)
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(Path(directory).iterdir())
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and current_depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            print(f"{prefix}└── [Zugriff verweigert]")
    
    print_tree('..')

def main():
    """Hauptfunktion"""
    print_banner()
    
    # Abhängigkeiten überprüfen
    check_dependencies()
    
    # Verzeichnisse erstellen
    create_directories()
    
    # Tests ausführen
    run_tests()
    
    # Menü anzeigen
    show_menu()

if __name__ == "__main__":
    main()

