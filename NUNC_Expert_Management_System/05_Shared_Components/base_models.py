"""
NUNC Expert Management System - Base Models
Gemeinsame Basis-Datenmodelle für alle Komponenten
"""

from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class BaseModel(ABC):
    """Basis-Modell für alle Datenmodelle"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary - muss in Subklassen implementiert werden"""
        raise NotImplementedError("Subclasses must implement to_dict")
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Erstellt aus Dictionary - muss in Subklassen implementiert werden"""
        raise NotImplementedError("Subclasses must implement from_dict")
    
    def validate(self) -> bool:
        """Validiert das Modell - Standard-Implementation"""
        return True


@dataclass
class TimestampMixin:
    """Mixin für Timestamp-Funktionalität"""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update_timestamp(self):
        """Aktualisiert den updated_at Timestamp"""
        self.updated_at = datetime.now()
    
    def get_age_days(self) -> int:
        """Gibt das Alter in Tagen zurück"""
        return (datetime.now() - self.created_at).days


@dataclass
class IdentifiableMixin:
    """Mixin für ID-Funktionalität"""
    id: str
    
    def get_id(self) -> str:
        """Gibt die ID zurück"""
        return self.id
    
    def is_valid_id(self) -> bool:
        """Prüft ob ID gültig ist"""
        return bool(self.id and len(self.id.strip()) > 0)


@dataclass
class StatusMixin:
    """Mixin für Status-Funktionalität"""
    status: str = "active"
    
    def is_active(self) -> bool:
        """Prüft ob Status aktiv ist"""
        return self.status.lower() == "active"
    
    def set_status(self, status: str):
        """Setzt den Status"""
        self.status = status.lower()
    
    def get_status(self) -> str:
        """Gibt den Status zurück"""
        return self.status
