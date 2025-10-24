#!/usr/bin/env python3
"""
NUNC Expert Management System - Boutique Profile Manager
Verwaltet maximal 100 Kandidaten mit persönlichen Beziehungen
"""

import os
import json
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BoutiqueStatus(Enum):
    """Status im Boutique-System"""
    CANDIDATE = "candidate"
    ACTIVE = "active"
    TRUSTED = "trusted"
    ARCHIVED = "archived"

class TrustLevel(Enum):
    """Vertrauens-Level"""
    NEW = 1
    DEVELOPING = 2
    GOOD = 3
    STRONG = 4
    TRUSTED = 5

class RelationshipQuality(Enum):
    """Qualität der Beziehung"""
    NEW = "new"
    GOOD = "good"
    EXCELLENT = "excellent"
    PARTNERSHIP = "partnership"

@dataclass
class Profile:
    """Kandidaten-Profil mit Boutique-Features"""
    id: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: Optional[str] = None
    location: Optional[str] = None
    
    # Boutique-spezifische Felder
    boutique_status: BoutiqueStatus = BoutiqueStatus.CANDIDATE
    trust_level: TrustLevel = TrustLevel.NEW
    personal_notes: Optional[str] = None
    relationship_quality: RelationshipQuality = RelationshipQuality.NEW
    
    # Verfügbarkeit
    availability_status: str = "unknown"
    next_available_date: Optional[date] = None
    preferred_hours_per_week: Optional[int] = None
    remote_preference: str = "flexible"
    
    # Skills und Erfahrung
    technical_skills: List[str] = None
    soft_skills: List[str] = None
    certifications: List[str] = None
    languages: List[str] = None
    
    # Projekt-Erfahrung (für Cross-connections)
    company_experience: Dict[str, str] = None
    project_experience: Dict[str, str] = None
    industry_experience: List[str] = None
    
    # AI-basierte Bewertung
    reliability_score: float = 0.0
    experience_score: float = 0.0
    quality_score: float = 0.0
    
    # Metadaten
    source: str = "manual"
    external_id: Optional[str] = None
    last_contact_date: Optional[date] = None
    total_contact_count: int = 0
    
    def __post_init__(self):
        if self.technical_skills is None:
            self.technical_skills = []
        if self.soft_skills is None:
            self.soft_skills = []
        if self.certifications is None:
            self.certifications = []
        if self.languages is None:
            self.languages = []
        if self.company_experience is None:
            self.company_experience = {}
        if self.project_experience is None:
            self.project_experience = {}
        if self.industry_experience is None:
            self.industry_experience = []

@dataclass
class Relationship:
    """Persönliche Beziehung zu einem Kandidaten"""
    id: Optional[str] = None
    profile_id: str = ""
    relationship_type: str = "professional"
    relationship_strength: int = 1
    personal_notes: Optional[str] = None
    personality_traits: List[str] = None
    communication_style: Optional[str] = None
    motivation_factors: List[str] = None
    career_goals: Optional[str] = None
    development_areas: List[str] = None
    mentoring_relationship: bool = False
    trust_indicators: Dict[str, int] = None
    reliability_notes: Optional[str] = None
    red_flags: List[str] = None
    preferred_contact_method: str = "email"
    contact_frequency: str = "monthly"
    best_contact_time: Optional[str] = None
    created_by: str = "system"
    last_interaction_date: Optional[date] = None
    interaction_count: int = 0
    
    def __post_init__(self):
        if self.personality_traits is None:
            self.personality_traits = []
        if self.motivation_factors is None:
            self.motivation_factors = []
        if self.development_areas is None:
            self.development_areas = []
        if self.trust_indicators is None:
            self.trust_indicators = {}
        if self.red_flags is None:
            self.red_flags = []

class BoutiqueProfileManager:
    """Verwaltet maximal 100 Kandidaten mit persönlichen Beziehungen"""
    
    MAX_PROFILES = 100
    
    def __init__(self):
        """Initialisiert den BoutiqueProfileManager"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
    def get_profile_count(self) -> int:
        """Gibt die aktuelle Anzahl der Profile zurück"""
        try:
            result = self.supabase.table('profiles').select('id', count='exact').execute()
            return result.count or 0
        except Exception as e:
            print(f"Error getting profile count: {e}")
            return 0
    
    def can_add_profile(self) -> bool:
        """Prüft ob ein neues Profil hinzugefügt werden kann (max. 100)"""
        return self.get_profile_count() < self.MAX_PROFILES
    
    def add_profile(self, profile: Profile) -> Tuple[bool, str]:
        """Fügt ein neues Profil hinzu"""
        try:
            # Prüfe ob noch Platz vorhanden ist
            if not self.can_add_profile():
                return False, f"Maximum of {self.MAX_PROFILES} profiles reached"
            
            # Prüfe ob E-Mail bereits existiert
            existing = self.supabase.table('profiles').select('id').eq('email', profile.email).execute()
            if existing.data:
                return False, "Profile with this email already exists"
            
            # Konvertiere Profile zu Dict für Supabase
            profile_data = self._profile_to_dict(profile)
            
            # Füge Profil hinzu
            result = self.supabase.table('profiles').insert(profile_data).execute()
            
            if result.data:
                profile_id = result.data[0]['id']
                
                # Erstelle automatisch eine Relationship
                relationship = Relationship(
                    profile_id=profile_id,
                    relationship_type="professional",
                    relationship_strength=1,
                    personal_notes="New candidate - initial contact needed",
                    created_by="system"
                )
                
                self._add_relationship(relationship)
                
                return True, f"Profile added successfully with ID: {profile_id}"
            else:
                return False, "Failed to add profile"
                
        except Exception as e:
            return False, f"Error adding profile: {e}"
    
    def get_profile(self, profile_id: str) -> Optional[Profile]:
        """Holt ein Profil anhand der ID"""
        try:
            result = self.supabase.table('profiles').select('*').eq('id', profile_id).execute()
            
            if result.data:
                return self._dict_to_profile(result.data[0])
            return None
            
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    def get_all_profiles(self, boutique_status: Optional[BoutiqueStatus] = None) -> List[Profile]:
        """Holt alle Profile, optional gefiltert nach Status"""
        try:
            query = self.supabase.table('profiles').select('*')
            
            if boutique_status:
                query = query.eq('boutique_status', boutique_status.value)
            
            result = query.execute()
            
            profiles = []
            for data in result.data:
                profiles.append(self._dict_to_profile(data))
            
            return profiles
            
        except Exception as e:
            print(f"Error getting profiles: {e}")
            return []
    
    def update_profile(self, profile: Profile) -> Tuple[bool, str]:
        """Aktualisiert ein bestehendes Profil"""
        try:
            if not profile.id:
                return False, "Profile ID is required for update"
            
            profile_data = self._profile_to_dict(profile)
            
            result = self.supabase.table('profiles').update(profile_data).eq('id', profile.id).execute()
            
            if result.data:
                return True, "Profile updated successfully"
            else:
                return False, "Profile not found or update failed"
                
        except Exception as e:
            return False, f"Error updating profile: {e}"
    
    def delete_profile(self, profile_id: str) -> Tuple[bool, str]:
        """Löscht ein Profil (und alle zugehörigen Relationships)"""
        try:
            # Lösche zuerst alle Relationships
            self.supabase.table('relationships').delete().eq('profile_id', profile_id).execute()
            self.supabase.table('contact_history').delete().eq('profile_id', profile_id).execute()
            
            # Lösche dann das Profil
            result = self.supabase.table('profiles').delete().eq('id', profile_id).execute()
            
            if result.data:
                return True, "Profile deleted successfully"
            else:
                return False, "Profile not found"
                
        except Exception as e:
            return False, f"Error deleting profile: {e}"
    
    def search_profiles(self, query: str, limit: int = 10) -> List[Profile]:
        """Semantische Suche in Profilen"""
        try:
            # Verwende Supabase's Volltext-Suche
            result = self.supabase.table('profiles').select('*').text_search('search_vector', query).limit(limit).execute()
            
            profiles = []
            for data in result.data:
                profiles.append(self._dict_to_profile(data))
            
            return profiles
            
        except Exception as e:
            print(f"Error searching profiles: {e}")
            return []
    
    def get_profiles_by_company(self, company: str) -> List[Profile]:
        """Findet Profile die bei einer bestimmten Firma gearbeitet haben"""
        try:
            result = self.supabase.table('profiles').select('*').contains('company_experience', {company: True}).execute()
            
            profiles = []
            for data in result.data:
                profiles.append(self._dict_to_profile(data))
            
            return profiles
            
        except Exception as e:
            print(f"Error getting profiles by company: {e}")
            return []
    
    def get_profiles_by_skill(self, skill: str) -> List[Profile]:
        """Findet Profile mit einer bestimmten Fähigkeit"""
        try:
            result = self.supabase.table('profiles').select('*').contains('technical_skills', [skill]).execute()
            
            profiles = []
            for data in result.data:
                profiles.append(self._dict_to_profile(data))
            
            return profiles
            
        except Exception as e:
            print(f"Error getting profiles by skill: {e}")
            return []
    
    def get_trusted_profiles(self) -> List[Profile]:
        """Holt alle vertrauenswürdigen Profile (Trust Level 4-5)"""
        try:
            result = self.supabase.table('profiles').select('*').gte('trust_level', 4).execute()
            
            profiles = []
            for data in result.data:
                profiles.append(self._dict_to_profile(data))
            
            return profiles
            
        except Exception as e:
            print(f"Error getting trusted profiles: {e}")
            return []
    
    def _add_relationship(self, relationship: Relationship) -> Tuple[bool, str]:
        """Fügt eine neue Beziehung hinzu"""
        try:
            relationship_data = self._relationship_to_dict(relationship)
            
            result = self.supabase.table('relationships').insert(relationship_data).execute()
            
            if result.data:
                return True, "Relationship added successfully"
            else:
                return False, "Failed to add relationship"
                
        except Exception as e:
            return False, f"Error adding relationship: {e}"
    
    def get_relationship(self, profile_id: str) -> Optional[Relationship]:
        """Holt die Beziehung zu einem Profil"""
        try:
            result = self.supabase.table('relationships').select('*').eq('profile_id', profile_id).execute()
            
            if result.data:
                return self._dict_to_relationship(result.data[0])
            return None
            
        except Exception as e:
            print(f"Error getting relationship: {e}")
            return None
    
    def update_relationship(self, relationship: Relationship) -> Tuple[bool, str]:
        """Aktualisiert eine Beziehung"""
        try:
            if not relationship.id:
                return False, "Relationship ID is required for update"
            
            relationship_data = self._relationship_to_dict(relationship)
            
            result = self.supabase.table('relationships').update(relationship_data).eq('id', relationship.id).execute()
            
            if result.data:
                return True, "Relationship updated successfully"
            else:
                return False, "Relationship not found or update failed"
                
        except Exception as e:
            return False, f"Error updating relationship: {e}"
    
    def _profile_to_dict(self, profile: Profile) -> Dict:
        """Konvertiert Profile zu Dict für Supabase"""
        data = asdict(profile)
        
        # Konvertiere Enums zu Strings
        if isinstance(data.get('boutique_status'), BoutiqueStatus):
            data['boutique_status'] = data['boutique_status'].value
        if isinstance(data.get('trust_level'), TrustLevel):
            data['trust_level'] = data['trust_level'].value
        if isinstance(data.get('relationship_quality'), RelationshipQuality):
            data['relationship_quality'] = data['relationship_quality'].value
        
        # Konvertiere date zu string
        if data.get('next_available_date'):
            data['next_available_date'] = data['next_available_date'].isoformat()
        if data.get('last_contact_date'):
            data['last_contact_date'] = data['last_contact_date'].isoformat()
        
        # Entferne None-Werte
        data = {k: v for k, v in data.items() if v is not None}
        
        return data
    
    def _dict_to_profile(self, data: Dict) -> Profile:
        """Konvertiert Dict von Supabase zu Profile"""
        # Entferne Supabase-spezifische Felder
        data = {k: v for k, v in data.items() if k not in ['id', 'created_at', 'updated_at', 'search_vector']}
        
        # Konvertiere Strings zu Enums
        if data.get('boutique_status'):
            data['boutique_status'] = BoutiqueStatus(data['boutique_status'])
        if data.get('trust_level'):
            data['trust_level'] = TrustLevel(data['trust_level'])
        if data.get('relationship_quality'):
            data['relationship_quality'] = RelationshipQuality(data['relationship_quality'])
        
        # Konvertiere date strings zu date objects
        if data.get('next_available_date'):
            data['next_available_date'] = datetime.fromisoformat(data['next_available_date']).date()
        if data.get('last_contact_date'):
            data['last_contact_date'] = datetime.fromisoformat(data['last_contact_date']).date()
        
        return Profile(**data)
    
    def _relationship_to_dict(self, relationship: Relationship) -> Dict:
        """Konvertiert Relationship zu Dict für Supabase"""
        data = asdict(relationship)
        
        # Konvertiere date zu string
        if data.get('last_interaction_date'):
            data['last_interaction_date'] = data['last_interaction_date'].isoformat()
        
        # Entferne None-Werte
        data = {k: v for k, v in data.items() if v is not None}
        
        return data
    
    def _dict_to_relationship(self, data: Dict) -> Relationship:
        """Konvertiert Dict von Supabase zu Relationship"""
        # Konvertiere date strings zu date objects
        if data.get('last_interaction_date'):
            data['last_interaction_date'] = datetime.fromisoformat(data['last_interaction_date']).date()
        
        return Relationship(**data)

# Beispiel-Verwendung
if __name__ == "__main__":
    # Test des BoutiqueProfileManager
    manager = BoutiqueProfileManager()
    
    print(f"Current profile count: {manager.get_profile_count()}")
    print(f"Can add profile: {manager.can_add_profile()}")
    
    # Beispiel-Profil erstellen
    profile = Profile(
        first_name="Max",
        last_name="Mustermann",
        email="max.mustermann@example.com",
        technical_skills=["Python", "React", "AWS"],
        soft_skills=["Teamwork", "Communication"],
        company_experience={"BMW": "2 years", "SAP": "1 year"},
        reliability_score=0.85,
        experience_score=0.90,
        quality_score=0.88
    )
    
    # Profil hinzufügen
    success, message = manager.add_profile(profile)
    print(f"Add profile: {success} - {message}")
    
    # Alle Profile anzeigen
    profiles = manager.get_all_profiles()
    print(f"Total profiles: {len(profiles)}")
    
    # Suche nach BMW-Erfahrung
    bmw_profiles = manager.get_profiles_by_company("BMW")
    print(f"BMW experience profiles: {len(bmw_profiles)}")
