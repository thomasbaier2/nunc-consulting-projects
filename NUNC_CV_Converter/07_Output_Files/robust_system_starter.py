#!/usr/bin/env python3
"""
NUNC CV Converter - Robust System Starter
Automatische Fehlerbehandlung und System-Optimierung
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import json
import logging
from pathlib import Path
from datetime import datetime

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RobustSystemStarter:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.required_packages = [
            'PyPDF2', 'pdfplumber', 'python-docx', 'docxtpl',
            'supabase', 'openai', 'sentence-transformers', 'flask',
            'numpy', 'scipy', 'scikit-learn', 'transformers'
        ]
        self.system_status = {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': str(Path.cwd()),
            'timestamp': datetime.now().isoformat()
        }
        
    def print_banner(self):
        """Zeigt NUNC Banner"""
        print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NUNC CONSULTING GmbH                     ║
    ║                                                              ║
    ║              🚀 ROBUST CV CONVERTER SYSTEM 🚀                ║
    ║                                                              ║
    ║        PDF → NUNC Template → Word → Supabase → Search        ║
    ║                                                              ║
    ║              🔧 Auto-Fix & Error-Handling 🔧                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    def check_system_requirements(self):
        """Überprüft System-Anforderungen"""
        logger.info("🔍 Überprüfe System-Anforderungen...")
        
        issues = []
        
        # Python Version Check
        if sys.version_info < (3, 8):
            issues.append("Python 3.8+ erforderlich")
        else:
            logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        
        # Platform Check
        if sys.platform not in ['darwin', 'linux', 'win32']:
            issues.append(f"Unbekannte Plattform: {sys.platform}")
        else:
            logger.info(f"✅ Plattform: {sys.platform}")
        
        # Working Directory Check
        if not os.path.exists(self.base_dir):
            issues.append(f"Base Directory nicht gefunden: {self.base_dir}")
        else:
            logger.info(f"✅ Base Directory: {self.base_dir}")
        
        return issues
    
    def install_required_packages(self):
        """Installiert fehlende Pakete automatisch"""
        logger.info("📦 Überprüfe und installiere Pakete...")
        
        missing_packages = []
        
        for package in self.required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"❌ {package} fehlt")
        
        if missing_packages:
            logger.info(f"📦 Installiere {len(missing_packages)} fehlende Pakete...")
            
            for package in missing_packages:
                try:
                    logger.info(f"Installing {package}...")
                    subprocess.run([
                        sys.executable, '-m', 'pip', 'install', package, '--quiet'
                    ], check=True, capture_output=True)
                    logger.info(f"✅ {package} installiert")
                except subprocess.CalledProcessError as e:
                    logger.error(f"❌ Fehler bei {package}: {e}")
                    # Fallback: Try without --quiet
                    try:
                        subprocess.run([
                            sys.executable, '-m', 'pip', 'install', package
                        ], check=True)
                        logger.info(f"✅ {package} installiert (Fallback)")
                    except subprocess.CalledProcessError:
                        logger.error(f"❌ {package} konnte nicht installiert werden")
        
        return len(missing_packages) == 0
    
    def create_necessary_directories(self):
        """Erstellt notwendige Verzeichnisse"""
        logger.info("📁 Erstelle Verzeichnisse...")
        
        directories = [
            'generated_profiles',
            'word_documents', 
            'html_templates',
            'test_results/input',
            'test_results/output',
            'uploads',
            'downloads'
        ]
        
        for directory in directories:
            dir_path = self.base_dir / '07_Output_Files' / directory
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ {directory}")
            except Exception as e:
                logger.error(f"❌ {directory}: {e}")
    
    def fix_import_paths(self):
        """Korrigiert Import-Pfade"""
        logger.info("🔧 Korrigiere Import-Pfade...")
        
        # Add base directory to Python path
        sys.path.insert(0, str(self.base_dir))
        sys.path.insert(0, str(self.base_dir / '01_Core_Components'))
        sys.path.insert(0, str(self.base_dir / '03_Word_Generation'))
        sys.path.insert(0, str(self.base_dir / '04_Supabase_Integration'))
        
        logger.info("✅ Import-Pfade korrigiert")
    
    def test_system_components(self):
        """Testet alle System-Komponenten"""
        logger.info("🧪 Teste System-Komponenten...")
        
        tests = {
            'CV Processor': self.test_cv_processor,
            'Word Generator': self.test_word_generator,
            'Supabase Integration': self.test_supabase_integration,
            'Web Interface': self.test_web_interface
        }
        
        results = {}
        
        for name, test_func in tests.items():
            try:
                result = test_func()
                results[name] = {'status': 'PASS', 'result': result}
                logger.info(f"✅ {name}")
            except Exception as e:
                results[name] = {'status': 'FAIL', 'error': str(e)}
                logger.error(f"❌ {name}: {e}")
        
        return results
    
    def test_cv_processor(self):
        """Testet CV Processor"""
        try:
            from cv_processor import CvProcessor
            processor = CvProcessor()
            return "CV Processor geladen"
        except Exception as e:
            raise Exception(f"CV Processor Fehler: {e}")
    
    def test_word_generator(self):
        """Testet Word Generator"""
        try:
            from word_generator import NuncWordGenerator
            generator = NuncWordGenerator()
            return "Word Generator geladen"
        except Exception as e:
            raise Exception(f"Word Generator Fehler: {e}")
    
    def test_supabase_integration(self):
        """Testet Supabase Integration"""
        try:
            from supabase_integration import SupabaseIntegration
            integration = SupabaseIntegration()
            return "Supabase Integration geladen"
        except Exception as e:
            raise Exception(f"Supabase Integration Fehler: {e}")
    
    def test_web_interface(self):
        """Testet Web Interface"""
        try:
            from web_interface import app
            return "Web Interface geladen"
        except Exception as e:
            raise Exception(f"Web Interface Fehler: {e}")
    
    def start_web_interface(self):
        """Startet Web-Interface mit Fehlerbehandlung"""
        logger.info("🌐 Starte Web-Interface...")
        
        try:
            # Web-Interface starten
            web_script = self.base_dir / '02_Web_Interface' / 'web_interface.py'
            if web_script.exists():
                logger.info("✅ Web-Interface wird gestartet...")
                logger.info("🌐 Öffne http://localhost:5000")
                
                # Browser öffnen
                def open_browser():
                    time.sleep(2)
                    try:
                        webbrowser.open('http://localhost:5000')
                    except Exception as e:
                        logger.warning(f"Browser konnte nicht geöffnet werden: {e}")
                
                threading.Thread(target=open_browser).start()
                
                # Web-Interface starten
                subprocess.run([sys.executable, str(web_script)])
            else:
                logger.error("❌ Web-Interface nicht gefunden")
                return False
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Web-Interface gestoppt")
        except Exception as e:
            logger.error(f"❌ Web-Interface Fehler: {e}")
            return False
        
        return True
    
    def save_system_report(self, test_results):
        """Speichert System-Report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': self.system_status,
            'test_results': test_results,
            'total_tests': len(test_results),
            'passed_tests': sum(1 for r in test_results.values() if r['status'] == 'PASS'),
            'failed_tests': sum(1 for r in test_results.values() if r['status'] == 'FAIL')
        }
        
        report_file = self.base_dir / '07_Output_Files' / 'test_results' / 'system_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📄 System-Report gespeichert: {report_file}")
    
    def run_robust_startup(self):
        """Führt robusten System-Start durch"""
        self.print_banner()
        
        # 1. System-Anforderungen prüfen
        issues = self.check_system_requirements()
        if issues:
            logger.error(f"❌ System-Probleme: {issues}")
            return False
        
        # 2. Pakete installieren
        if not self.install_required_packages():
            logger.error("❌ Paket-Installation fehlgeschlagen")
            return False
        
        # 3. Verzeichnisse erstellen
        self.create_necessary_directories()
        
        # 4. Import-Pfade korrigieren
        self.fix_import_paths()
        
        # 5. System-Komponenten testen
        test_results = self.test_system_components()
        
        # 6. System-Report speichern
        self.save_system_report(test_results)
        
        # 7. Web-Interface starten
        if all(r['status'] == 'PASS' for r in test_results.values()):
            logger.info("🎉 Alle Tests erfolgreich! Starte Web-Interface...")
            return self.start_web_interface()
        else:
            logger.error("❌ Einige Tests fehlgeschlagen. System nicht startbereit.")
            return False

def main():
    """Hauptfunktion für robusten System-Start"""
    starter = RobustSystemStarter()
    
    try:
        success = starter.run_robust_startup()
        if success:
            logger.info("🚀 System erfolgreich gestartet!")
        else:
            logger.error("❌ System-Start fehlgeschlagen!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unerwarteter Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

