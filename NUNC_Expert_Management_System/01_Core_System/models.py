"""
NUNC Expert Management System - Core System Models
Datenmodelle für Profile und Experten
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field
import uuid


class ProfileStatus(Enum):
    """Status eines Experten-Profils"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ARCHIVED = "archived"


@dataclass
class Expert:
    """Experten-Datenmodell"""
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'linkedin': self.linkedin,
            'website': self.website
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expert':
        """Erstellt aus Dictionary"""
        return cls(
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone'),
            location=data.get('location'),
            linkedin=data.get('linkedin'),
            website=data.get('website')
        )


@dataclass
class Profile:
    """Experten-Profil Datenmodell"""
    id: str
    expert: Expert
    status: ProfileStatus = ProfileStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Persönliche Daten
    personal_data: Dict[str, Any] = field(default_factory=dict)
    
    # Berufserfahrung
    experience: List[Dict[str, Any]] = field(default_factory=list)
    
    # Skills und Zertifizierungen
    skills: List[str] = field(default_factory=list)
    certifications: List[Dict[str, Any]] = field(default_factory=list)
    languages: List[Dict[str, Any]] = field(default_factory=list)
    
    # Verfügbarkeit
    availability: Dict[str, Any] = field(default_factory=dict)
    
    # Charakter und Soft Skills
    character: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertiert zu Dictionary für JSON-Serialisierung"""
        return {
            'id': self.id,
            'expert': self.expert.to_dict(),
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'personal_data': self.personal_data,
            'experience': self.experience,
            'skills': self.skills,
            'certifications': self.certifications,
            'languages': self.languages,
            'availability': self.availability,
            'character': self.character
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        """Erstellt aus Dictionary"""
        expert = Expert.from_dict(data.get('expert', {}))
        
        profile = cls(
            id=data.get('id', str(uuid.uuid4())),
            expert=expert,
            status=ProfileStatus(data.get('status', 'active')),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            personal_data=data.get('personal_data', {}),
            experience=data.get('experience', []),
            skills=data.get('skills', []),
            certifications=data.get('certifications', []),
            languages=data.get('languages', []),
            availability=data.get('availability', {}),
            character=data.get('character', {})
        )
        return profile
    
    def update_timestamp(self):
        """Aktualisiert den updated_at Timestamp"""
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """Prüft ob Profil aktiv ist"""
        return self.status == ProfileStatus.ACTIVE
    
    def get_full_name(self) -> str:
        """Gibt den vollständigen Namen zurück"""
        return self.expert.name
    
    def get_contact_info(self) -> Dict[str, str]:
        """Gibt Kontaktinformationen zurück"""
        return {
            'email': self.expert.email,
            'phone': self.expert.phone or '',
            'location': self.expert.location or ''
        }
