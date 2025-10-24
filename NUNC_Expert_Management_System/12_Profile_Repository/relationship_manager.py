#!/usr/bin/env python3
"""
NUNC Expert Management System - Relationship Manager
Verwaltet persönliche Beziehungen und Kontakt-Historie
"""

import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ContactType(Enum):
    """Art des Kontakts"""
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    LINKEDIN = "linkedin"
    PROJECT_DISCUSSION = "project_discussion"
    CHECK_IN = "check_in"

class ContactMethod(Enum):
    """Kontakt-Methode"""
    PHONE = "phone"
    EMAIL = "email"
    VIDEO_CALL = "video_call"
    IN_PERSON = "in_person"
    LINKEDIN = "linkedin"
    WHATSAPP = "whatsapp"

class ContactOutcome(Enum):
    """Ergebnis des Kontakts"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    CONCERNS = "concerns"
    FOLLOW_UP_NEEDED = "follow_up_needed"

@dataclass
class ContactRecord:
    """Einzelner Kontakt-Eintrag"""
    id: Optional[str] = None
    profile_id: str = ""
    relationship_id: Optional[str] = None
    
    # Kontakt-Details
    contact_type: ContactType = ContactType.CHECK_IN
    contact_method: ContactMethod = ContactMethod.EMAIL
    subject: Optional[str] = None
    notes: str = ""
    outcome: Optional[ContactOutcome] = None
    
    # Follow-up
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None
    follow_up_notes: Optional[str] = None
    
    # Metadaten
    duration_minutes: Optional[int] = None
    initiated_by: str = "recruiter"
    mood_rating: Optional[int] = None  # 1-5
    satisfaction_rating: Optional[int] = None  # 1-5
    
    def __post_init__(self):
        if self.mood_rating and not (1 <= self.mood_rating <= 5):
            raise ValueError("Mood rating must be between 1 and 5")
        if self.satisfaction_rating and not (1 <= self.satisfaction_rating <= 5):
            raise ValueError("Satisfaction rating must be between 1 and 5")

class RelationshipManager:
    """Verwaltet persönliche Beziehungen und Kontakt-Historie"""
    
    def __init__(self):
        """Initialisiert den RelationshipManager"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def add_contact(self, contact: ContactRecord) -> Tuple[bool, str]:
        """Fügt einen neuen Kontakt hinzu"""
        try:
            contact_data = self._contact_to_dict(contact)
            
            result = self.supabase.table('contact_history').insert(contact_data).execute()
            
            if result.data:
                contact_id = result.data[0]['id']
                
                # Aktualisiere Relationship-Statistiken
                self._update_relationship_stats(contact.profile_id)
                
                return True, f"Contact added successfully with ID: {contact_id}"
            else:
                return False, "Failed to add contact"
                
        except Exception as e:
            return False, f"Error adding contact: {e}"
    
    def get_contact_history(self, profile_id: str, limit: int = 50) -> List[ContactRecord]:
        """Holt die Kontakt-Historie für ein Profil"""
        try:
            result = self.supabase.table('contact_history').select('*').eq('profile_id', profile_id).order('created_at', desc=True).limit(limit).execute()
            
            contacts = []
            for data in result.data:
                contacts.append(self._dict_to_contact(data))
            
            return contacts
            
        except Exception as e:
            print(f"Error getting contact history: {e}")
            return []
    
    def get_recent_contacts(self, days: int = 30) -> List[ContactRecord]:
        """Holt alle Kontakte der letzten X Tage"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            result = self.supabase.table('contact_history').select('*').gte('created_at', cutoff_date).order('created_at', desc=True).execute()
            
            contacts = []
            for data in result.data:
                contacts.append(self._dict_to_contact(data))
            
            return contacts
            
        except Exception as e:
            print(f"Error getting recent contacts: {e}")
            return []
    
    def get_contacts_by_type(self, contact_type: ContactType, limit: int = 50) -> List[ContactRecord]:
        """Holt Kontakte nach Typ"""
        try:
            result = self.supabase.table('contact_history').select('*').eq('contact_type', contact_type.value).order('created_at', desc=True).limit(limit).execute()
            
            contacts = []
            for data in result.data:
                contacts.append(self._dict_to_contact(data))
            
            return contacts
            
        except Exception as e:
            print(f"Error getting contacts by type: {e}")
            return []
    
    def get_follow_up_required(self) -> List[ContactRecord]:
        """Holt alle Kontakte die ein Follow-up benötigen"""
        try:
            result = self.supabase.table('contact_history').select('*').eq('follow_up_required', True).order('follow_up_date', desc=False).execute()
            
            contacts = []
            for data in result.data:
                contacts.append(self._dict_to_contact(data))
            
            return contacts
            
        except Exception as e:
            print(f"Error getting follow-up required: {e}")
            return []
    
    def update_contact(self, contact: ContactRecord) -> Tuple[bool, str]:
        """Aktualisiert einen bestehenden Kontakt"""
        try:
            if not contact.id:
                return False, "Contact ID is required for update"
            
            contact_data = self._contact_to_dict(contact)
            
            result = self.supabase.table('contact_history').update(contact_data).eq('id', contact.id).execute()
            
            if result.data:
                return True, "Contact updated successfully"
            else:
                return False, "Contact not found or update failed"
                
        except Exception as e:
            return False, f"Error updating contact: {e}"
    
    def mark_follow_up_completed(self, contact_id: str, follow_up_notes: str = "") -> Tuple[bool, str]:
        """Markiert ein Follow-up als abgeschlossen"""
        try:
            result = self.supabase.table('contact_history').update({
                'follow_up_required': False,
                'follow_up_notes': follow_up_notes
            }).eq('id', contact_id).execute()
            
            if result.data:
                return True, "Follow-up marked as completed"
            else:
                return False, "Contact not found"
                
        except Exception as e:
            return False, f"Error marking follow-up completed: {e}"
    
    def get_relationship_insights(self, profile_id: str) -> Dict:
        """Analysiert die Beziehung zu einem Profil"""
        try:
            # Hole alle Kontakte für das Profil
            contacts = self.get_contact_history(profile_id)
            
            if not contacts:
                return {"message": "No contact history available"}
            
            # Analysiere Kontakt-Muster
            total_contacts = len(contacts)
            recent_contacts = len([c for c in contacts if c.created_at and (datetime.now().date() - c.created_at.date()).days <= 30])
            
            # Kontakt-Typen
            contact_types = {}
            for contact in contacts:
                contact_type = contact.contact_type.value
                contact_types[contact_type] = contact_types.get(contact_type, 0) + 1
            
            # Mood und Satisfaction Trends
            mood_ratings = [c.mood_rating for c in contacts if c.mood_rating]
            satisfaction_ratings = [c.satisfaction_rating for c in contacts if c.satisfaction_rating]
            
            avg_mood = sum(mood_ratings) / len(mood_ratings) if mood_ratings else None
            avg_satisfaction = sum(satisfaction_ratings) / len(satisfaction_ratings) if satisfaction_ratings else None
            
            # Follow-up Status
            pending_follow_ups = len([c for c in contacts if c.follow_up_required])
            
            # Letzter Kontakt
            last_contact = max(contacts, key=lambda x: x.created_at) if contacts else None
            
            return {
                "total_contacts": total_contacts,
                "recent_contacts": recent_contacts,
                "contact_types": contact_types,
                "avg_mood_rating": round(avg_mood, 2) if avg_mood else None,
                "avg_satisfaction_rating": round(avg_satisfaction, 2) if avg_satisfaction else None,
                "pending_follow_ups": pending_follow_ups,
                "last_contact_date": last_contact.created_at.isoformat() if last_contact and last_contact.created_at else None,
                "last_contact_type": last_contact.contact_type.value if last_contact else None,
                "relationship_strength": self._calculate_relationship_strength(contacts)
            }
            
        except Exception as e:
            return {"error": f"Error analyzing relationship: {e}"}
    
    def get_contact_statistics(self) -> Dict:
        """Gibt allgemeine Kontakt-Statistiken zurück"""
        try:
            # Gesamt-Kontakte
            total_result = self.supabase.table('contact_history').select('id', count='exact').execute()
            total_contacts = total_result.count or 0
            
            # Kontakte heute
            today = datetime.now().date().isoformat()
            today_result = self.supabase.table('contact_history').select('id', count='exact').gte('created_at', today).execute()
            today_contacts = today_result.count or 0
            
            # Kontakte diese Woche
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            week_result = self.supabase.table('contact_history').select('id', count='exact').gte('created_at', week_ago).execute()
            week_contacts = week_result.count or 0
            
            # Pending Follow-ups
            follow_up_result = self.supabase.table('contact_history').select('id', count='exact').eq('follow_up_required', True).execute()
            pending_follow_ups = follow_up_result.count or 0
            
            return {
                "total_contacts": total_contacts,
                "today_contacts": today_contacts,
                "week_contacts": week_contacts,
                "pending_follow_ups": pending_follow_ups
            }
            
        except Exception as e:
            return {"error": f"Error getting statistics: {e}"}
    
    def _update_relationship_stats(self, profile_id: str):
        """Aktualisiert Relationship-Statistiken nach einem Kontakt"""
        try:
            # Hole aktuelle Relationship
            relationship_result = self.supabase.table('relationships').select('*').eq('profile_id', profile_id).execute()
            
            if relationship_result.data:
                relationship = relationship_result.data[0]
                
                # Aktualisiere Statistiken
                new_interaction_count = relationship.get('interaction_count', 0) + 1
                last_interaction_date = datetime.now().date().isoformat()
                
                self.supabase.table('relationships').update({
                    'interaction_count': new_interaction_count,
                    'last_interaction_date': last_interaction_date
                }).eq('profile_id', profile_id).execute()
                
        except Exception as e:
            print(f"Error updating relationship stats: {e}")
    
    def _calculate_relationship_strength(self, contacts: List[ContactRecord]) -> int:
        """Berechnet die Beziehungsstärke basierend auf Kontakten"""
        if not contacts:
            return 1
        
        # Faktoren für Beziehungsstärke
        total_contacts = len(contacts)
        recent_contacts = len([c for c in contacts if c.created_at and (datetime.now().date() - c.created_at.date()).days <= 30])
        
        # Positive Ratings
        positive_contacts = len([c for c in contacts if c.outcome == ContactOutcome.POSITIVE])
        
        # Berechne Score (1-5)
        score = 1
        
        if total_contacts >= 5:
            score += 1
        if recent_contacts >= 3:
            score += 1
        if positive_contacts >= total_contacts * 0.7:
            score += 1
        if total_contacts >= 10:
            score += 1
        
        return min(score, 5)
    
    def _contact_to_dict(self, contact: ContactRecord) -> Dict:
        """Konvertiert ContactRecord zu Dict für Supabase"""
        data = asdict(contact)
        
        # Konvertiere Enums zu Strings
        if isinstance(data.get('contact_type'), ContactType):
            data['contact_type'] = data['contact_type'].value
        if isinstance(data.get('contact_method'), ContactMethod):
            data['contact_method'] = data['contact_method'].value
        if isinstance(data.get('outcome'), ContactOutcome):
            data['outcome'] = data['outcome'].value
        
        # Konvertiere date zu string
        if data.get('follow_up_date'):
            data['follow_up_date'] = data['follow_up_date'].isoformat()
        
        # Entferne None-Werte
        data = {k: v for k, v in data.items() if v is not None}
        
        return data
    
    def _dict_to_contact(self, data: Dict) -> ContactRecord:
        """Konvertiert Dict von Supabase zu ContactRecord"""
        # Konvertiere Strings zu Enums
        if data.get('contact_type'):
            data['contact_type'] = ContactType(data['contact_type'])
        if data.get('contact_method'):
            data['contact_method'] = ContactMethod(data['contact_method'])
        if data.get('outcome'):
            data['outcome'] = ContactOutcome(data['outcome'])
        
        # Konvertiere date strings zu date objects
        if data.get('follow_up_date'):
            data['follow_up_date'] = datetime.fromisoformat(data['follow_up_date']).date()
        
        # Konvertiere created_at zu datetime
        if data.get('created_at'):
            data['created_at'] = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        
        return ContactRecord(**data)

# Beispiel-Verwendung
if __name__ == "__main__":
    # Test des RelationshipManager
    manager = RelationshipManager()
    
    # Kontakt-Statistiken
    stats = manager.get_contact_statistics()
    print(f"Contact Statistics: {stats}")
    
    # Beispiel-Kontakt erstellen
    contact = ContactRecord(
        profile_id="example-profile-id",
        contact_type=ContactType.CHECK_IN,
        contact_method=ContactMethod.EMAIL,
        subject="Quarterly Check-in",
        notes="Sehr positive Gespräch, interessiert an neuen Projekten",
        outcome=ContactOutcome.POSITIVE,
        mood_rating=5,
        satisfaction_rating=4,
        duration_minutes=30
    )
    
    # Kontakt hinzufügen
    success, message = manager.add_contact(contact)
    print(f"Add contact: {success} - {message}")
    
    # Follow-ups anzeigen
    follow_ups = manager.get_follow_up_required()
    print(f"Pending follow-ups: {len(follow_ups)}")
