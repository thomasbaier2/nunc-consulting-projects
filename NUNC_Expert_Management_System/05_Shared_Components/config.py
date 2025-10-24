"""
NUNC Expert Management System - Shared Components Configuration
Zentrale Konfiguration für alle System-Komponenten
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Zentrale Konfiguration für NEMS"""
    
    # Basis-Pfade
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "08_Output_Files" / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "08_Output_Files" / "generated_profiles"
    PROFILES_FILE: Path = BASE_DIR / "profiles.json"
    
    # API Keys (aus Umgebungsvariablen)
    OPENAI_API_KEY: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    # Komponenten-Einstellungen
    CV_PROCESSING: Dict[str, Any] = None
    PROFILE_MANAGEMENT: Dict[str, Any] = None
    WEB_INTERFACE: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialisierung nach Dataclass-Erstellung"""
        # Lade Umgebungsvariablen
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        
        # Setze Standard-Komponenten-Einstellungen
        if self.CV_PROCESSING is None:
            self.CV_PROCESSING = {
                "max_file_size": 10 * 1024 * 1024,  # 10MB
                "supported_formats": [".pdf"],
                "extraction_timeout": 30,
                "processing_timeout": 120
            }
        
        if self.PROFILE_MANAGEMENT is None:
            self.PROFILE_MANAGEMENT = {
                "max_profiles": 1000,
                "backup_enabled": True,
                "auto_save": True
            }
        
        if self.WEB_INTERFACE is None:
            self.WEB_INTERFACE = {
                "host": "127.0.0.1",
                "port": 5000,
                "debug": True,
                "auto_reload": True
            }
    
    def get_upload_path(self, filename: str) -> Path:
        """Gibt den vollständigen Upload-Pfad zurück"""
        return self.UPLOAD_DIR / filename
    
    def get_output_path(self, filename: str) -> Path:
        """Gibt den vollständigen Output-Pfad zurück"""
        return self.OUTPUT_DIR / filename
    
    def ensure_directories(self):
        """Stellt sicher, dass alle benötigten Verzeichnisse existieren"""
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    def is_testing(self) -> bool:
        """Prüft ob im Test-Modus"""
        return os.getenv("TESTING", "false").lower() == "true"
    
    def get_database_config(self) -> Dict[str, str]:
        """Gibt Datenbank-Konfiguration zurück"""
        return {
            "url": self.SUPABASE_URL or "",
            "key": self.SUPABASE_KEY or ""
        }
    
    def get_openai_config(self) -> Dict[str, str]:
        """Gibt OpenAI-Konfiguration zurück"""
        return {
            "api_key": self.OPENAI_API_KEY or ""
        }
    
    def validate_config(self) -> bool:
        """Validiert die Konfiguration"""
        # Prüfe ob Verzeichnisse erstellt werden können
        try:
            self.ensure_directories()
        except Exception:
            return False
        
        # Prüfe API Keys (nur wenn nicht im Test-Modus)
        if not self.is_testing():
            if not self.OPENAI_API_KEY:
                print("Warning: OPENAI_API_KEY not set")
            if not self.SUPABASE_URL:
                print("Warning: SUPABASE_URL not set")
            if not self.SUPABASE_KEY:
                print("Warning: SUPABASE_KEY not set")
        
        return True


# Globale Konfigurationsinstanz
config = Config()
