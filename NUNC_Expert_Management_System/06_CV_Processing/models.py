"""
NUNC Expert Management System - CV Processing Models
Datenmodelle für CV-Verarbeitung und Extraktion
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class ProcessingStatus(Enum):
    """Status der CV-Verarbeitung"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class CvData:
    """CV-Datenmodell für rohe Extraktion"""
    file_path: str
    file_name: str
    file_size: int
    extracted_text: str
    extraction_method: str
    extraction_timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary"""
        return {
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'extracted_text': self.extracted_text,
            'extraction_method': self.extraction_method,
            'extraction_timestamp': self.extraction_timestamp.isoformat()
        }


@dataclass
class ExtractedData:
    """Extrahierten Daten aus CV"""
    # Persönliche Daten
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    
    # Berufserfahrung
    experience: List[Dict[str, Any]] = field(default_factory=list)
    
    # Bildung
    education: List[Dict[str, Any]] = field(default_factory=list)
    
    # Skills
    skills: List[str] = field(default_factory=list)
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    
    # Zertifizierungen
    certifications: List[Dict[str, Any]] = field(default_factory=list)
    
    # Sprachen
    languages: List[Dict[str, Any]] = field(default_factory=list)
    
    # Verfügbarkeit
    availability: Dict[str, Any] = field(default_factory=dict)
    
    # Zusätzliche Daten
    additional_info: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'linkedin': self.linkedin,
            'experience': self.experience,
            'education': self.education,
            'skills': self.skills,
            'technical_skills': self.technical_skills,
            'soft_skills': self.soft_skills,
            'certifications': self.certifications,
            'languages': self.languages,
            'availability': self.availability,
            'additional_info': self.additional_info
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExtractedData':
        """Erstellt aus Dictionary"""
        return cls(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            linkedin=data.get('linkedin'),
            experience=data.get('experience', []),
            education=data.get('education', []),
            skills=data.get('skills', []),
            technical_skills=data.get('technical_skills', []),
            soft_skills=data.get('soft_skills', []),
            certifications=data.get('certifications', []),
            languages=data.get('languages', []),
            availability=data.get('availability', {}),
            additional_info=data.get('additional_info', {})
        )


@dataclass
class ProcessingResult:
    """Ergebnis der CV-Verarbeitung"""
    status: ProcessingStatus
    cv_data: CvData
    extracted_data: Optional[ExtractedData] = None
    profile_id: Optional[str] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary"""
        return {
            'status': self.status.value,
            'cv_data': self.cv_data.to_dict(),
            'extracted_data': self.extracted_data.to_dict() if self.extracted_data else None,
            'profile_id': self.profile_id,
            'error_message': self.error_message,
            'processing_time': self.processing_time,
            'created_at': self.created_at.isoformat()
        }
    
    def is_successful(self) -> bool:
        """Prüft ob Verarbeitung erfolgreich war"""
        return self.status == ProcessingStatus.COMPLETED
    
    def has_error(self) -> bool:
        """Prüft ob Fehler aufgetreten ist"""
        return self.status == ProcessingStatus.FAILED
