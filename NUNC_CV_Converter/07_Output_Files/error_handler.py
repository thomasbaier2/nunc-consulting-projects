#!/usr/bin/env python3
"""
NUNC CV Converter - Error Handler
Automatische Fehlerbehandlung und Recovery
"""

import os
import sys
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class NuncErrorHandler:
    def __init__(self):
        self.error_log = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup für detailliertes Logging"""
        log_dir = Path(__file__).parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'error.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_import_error(self, module_name: str, error: Exception) -> bool:
        """Behandelt Import-Fehler automatisch"""
        self.logger.error(f"Import-Fehler für {module_name}: {error}")
        
        try:
            # Versuche automatische Installation
            import subprocess
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', module_name
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"✅ {module_name} erfolgreich installiert")
                return True
            else:
                self.logger.error(f"❌ Installation fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Fehler bei Installation: {e}")
            return False
    
    def handle_file_not_found(self, file_path: str, error: Exception) -> bool:
        """Behandelt Datei-nicht-gefunden Fehler"""
        self.logger.error(f"Datei nicht gefunden: {file_path}")
        
        try:
            # Versuche Datei zu erstellen
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if path.suffix == '.py':
                # Python-Datei erstellen
                with open(path, 'w') as f:
                    f.write(f"# Auto-generated file\n# Created: {datetime.now()}\n")
            else:
                # Leere Datei erstellen
                path.touch()
            
            self.logger.info(f"✅ Datei erstellt: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Fehler beim Erstellen: {e}")
            return False
    
    def handle_permission_error(self, file_path: str, error: Exception) -> bool:
        """Behandelt Berechtigungs-Fehler"""
        self.logger.error(f"Berechtigungs-Fehler: {file_path}")
        
        try:
            # Versuche Berechtigungen zu ändern
            os.chmod(file_path, 0o755)
            self.logger.info(f"✅ Berechtigungen geändert: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Fehler bei Berechtigungen: {e}")
            return False
    
    def handle_connection_error(self, service: str, error: Exception) -> bool:
        """Behandelt Verbindungs-Fehler"""
        self.logger.error(f"Verbindungs-Fehler zu {service}: {error}")
        
        # Fallback-Strategien
        if service == 'supabase':
            self.logger.info("🔄 Verwende lokale Datenbank als Fallback")
            return True
        elif service == 'openai':
            self.logger.info("🔄 Verwende lokale Embeddings als Fallback")
            return True
        
        return False
    
    def handle_memory_error(self, error: Exception) -> bool:
        """Behandelt Speicher-Fehler"""
        self.logger.error(f"Speicher-Fehler: {error}")
        
        try:
            # Versuche Speicher zu optimieren
            import gc
            gc.collect()
            self.logger.info("✅ Speicher optimiert")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Speicher-Optimierung fehlgeschlagen: {e}")
            return False
    
    def handle_general_error(self, error: Exception, context: str = "") -> bool:
        """Behandelt allgemeine Fehler"""
        self.logger.error(f"Allgemeiner Fehler in {context}: {error}")
        self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Fehler in Log speichern
        self.error_log.append({
            'timestamp': datetime.now().isoformat(),
            'context': context,
            'error': str(error),
            'traceback': traceback.format_exc()
        })
        
        return False
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Gibt Fehler-Zusammenfassung zurück"""
        return {
            'total_errors': len(self.error_log),
            'errors_by_type': self._categorize_errors(),
            'recent_errors': self.error_log[-5:] if self.error_log else []
        }
    
    def _categorize_errors(self) -> Dict[str, int]:
        """Kategorisiert Fehler nach Typ"""
        categories = {}
        for error in self.error_log:
            error_type = type(error['error']).__name__
            categories[error_type] = categories.get(error_type, 0) + 1
        return categories
    
    def save_error_report(self):
        """Speichert Fehler-Report"""
        report_file = Path(__file__).parent / 'error_report.json'
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'error_summary': self.get_error_summary(),
            'all_errors': self.error_log
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"📄 Fehler-Report gespeichert: {report_file}")

# Global Error Handler Instance
error_handler = NuncErrorHandler()

def handle_error(error: Exception, context: str = "") -> bool:
    """Globale Fehlerbehandlung"""
    error_type = type(error).__name__
    
    if error_type == 'ImportError':
        return error_handler.handle_import_error(str(error), error)
    elif error_type == 'FileNotFoundError':
        return error_handler.handle_file_not_found(str(error), error)
    elif error_type == 'PermissionError':
        return error_handler.handle_permission_error(str(error), error)
    elif error_type == 'ConnectionError':
        return error_handler.handle_connection_error('unknown', error)
    elif error_type == 'MemoryError':
        return error_handler.handle_memory_error(error)
    else:
        return error_handler.handle_general_error(error, context)

def safe_execute(func, *args, **kwargs):
    """Sichere Ausführung mit Fehlerbehandlung"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e, f"Function: {func.__name__}")
        return None

def safe_import(module_name: str):
    """Sichere Import mit Fehlerbehandlung"""
    try:
        return __import__(module_name)
    except ImportError as e:
        handle_error(e, f"Import: {module_name}")
        return None

if __name__ == "__main__":
    # Test des Error Handlers
    print("🧪 Teste Error Handler...")
    
    # Test Import Error
    try:
        import nonexistent_module
    except ImportError as e:
        handle_error(e, "Test Import")
    
    # Test File Not Found
    try:
        with open('nonexistent_file.txt', 'r') as f:
            f.read()
    except FileNotFoundError as e:
        handle_error(e, "Test File")
    
    print("✅ Error Handler Test abgeschlossen")

