# profile_manager.py
"""
NUNC Expert Management System - Core System
Profil-Management für Experten
"""

from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

class ProfileManager:
    """Verwaltet Experten-Profile mit CRUD-Operationen"""
    
    def __init__(self, supabase_client=None):
        self.supabase_client = supabase_client
        self.profiles_file = Path("08_Output_Files/profiles.json")
        self.profiles_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Lade bestehende Profile
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> List[Dict]:
        """Lädt Profile aus lokaler Datei oder Supabase"""
        if self.profiles_file.exists():
            with open(self.profiles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_profiles(self):
        """Speichert Profile in lokaler Datei"""
        with open(self.profiles_file, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, indent=4, ensure_ascii=False)
    
    def create_profile(self, profile_data: Dict) -> str:
        """Erstellt ein neues Experten-Profil"""
        profile_id = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Vollständige Profil-Struktur
        full_profile = {
            "id": profile_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            
            # Persönliche Daten
            "expert_name": profile_data.get("expert_name", ""),
            "email": profile_data.get("email", ""),
            "phone": profile_data.get("phone", ""),
            "location": profile_data.get("location", ""),
            
            # Verfügbarkeit
            "availability": {
                "status": "available",  # available, busy, unavailable
                "start_date": profile_data.get("start_date", ""),
                "hours_per_week": profile_data.get("hours_per_week", ""),
                "remote_onsite": profile_data.get("remote_onsite", "both"),
                "last_updated": datetime.now().isoformat()
            },
            
            # Fachliche Daten
            "hauptfokus": profile_data.get("hauptfokus", ""),
            "sprachen": profile_data.get("sprachen", ""),
            "zur_person": profile_data.get("zur_person", ""),
            
            # Kenntnisse
            "besondere_kenntnisse": profile_data.get("besondere_kenntnisse", ""),
            "branchenkenntnisse": profile_data.get("branchenkenntnisse", ""),
            "methoden": profile_data.get("methoden", ""),
            "technologien": profile_data.get("technologien", ""),
            "zertifizierungen": profile_data.get("zertifizierungen", ""),
            
            # Charakter & Soft Skills
            "charakter": profile_data.get("charakter", ""),
            "soft_skills": profile_data.get("soft_skills", ""),
            "arbeitsweise": profile_data.get("arbeitsweise", ""),
            
            # Projekthistorie
            "projekthistorie": profile_data.get("projekthistorie", []),
            "projekthistorie_text": profile_data.get("projekthistorie_text", ""),
            
            # System-Daten
            "source": profile_data.get("source", "pdf"),  # pdf, mail, manual
            "version": "1.0",
            "tags": profile_data.get("tags", []),
            "notes": profile_data.get("notes", "")
        }
        
        # Profil speichern
        self.profiles.append(full_profile)
        self._save_profiles()
        
        # In Supabase speichern (falls verfügbar)
        if self.supabase_client:
            try:
                self.supabase_client.insert_profile(full_profile)
                print(f"✅ Profil in Supabase gespeichert: {profile_id}")
            except Exception as e:
                print(f"⚠️ Supabase-Fehler: {e}")
        
        print(f"✅ Profil erstellt: {profile_id}")
        return profile_id
    
    def read_profile(self, profile_id: str) -> Optional[Dict]:
        """Liest ein Profil anhand der ID"""
        for profile in self.profiles:
            if profile["id"] == profile_id:
                return profile
        return None
    
    def update_profile(self, profile_id: str, update_data: Dict) -> bool:
        """Aktualisiert ein Profil"""
        for i, profile in enumerate(self.profiles):
            if profile["id"] == profile_id:
                # Update-Daten hinzufügen
                self.profiles[i].update(update_data)
                self.profiles[i]["updated_at"] = datetime.now().isoformat()
                
                # Speichern
                self._save_profiles()
                
                # Supabase aktualisieren (falls verfügbar)
                if self.supabase_client:
                    try:
                        self.supabase_client.update_profile(profile_id, update_data)
                        print(f"✅ Profil in Supabase aktualisiert: {profile_id}")
                    except Exception as e:
                        print(f"⚠️ Supabase-Fehler: {e}")
                
                print(f"✅ Profil aktualisiert: {profile_id}")
                return True
        
        print(f"❌ Profil nicht gefunden: {profile_id}")
        return False
    
    def delete_profile(self, profile_id: str) -> bool:
        """Löscht ein Profil"""
        for i, profile in enumerate(self.profiles):
            if profile["id"] == profile_id:
                # Profil entfernen
                deleted_profile = self.profiles.pop(i)
                self._save_profiles()
                
                # Supabase löschen (falls verfügbar)
                if self.supabase_client:
                    try:
                        self.supabase_client.delete_profile(profile_id)
                        print(f"✅ Profil aus Supabase gelöscht: {profile_id}")
                    except Exception as e:
                        print(f"⚠️ Supabase-Fehler: {e}")
                
                print(f"✅ Profil gelöscht: {profile_id}")
                return True
        
        print(f"❌ Profil nicht gefunden: {profile_id}")
        return False
    
    def get_all_profiles(self) -> List[Dict]:
        """Gibt alle Profile zurück"""
        return self.profiles
    
    def search_profiles(self, query: str) -> List[Dict]:
        """Sucht Profile basierend auf Query"""
        results = []
        query_lower = query.lower()
        
        for profile in self.profiles:
            # Suche in verschiedenen Feldern
            searchable_text = f"""
                {profile.get('expert_name', '')}
                {profile.get('hauptfokus', '')}
                {profile.get('technologien', '')}
                {profile.get('branchenkenntnisse', '')}
                {profile.get('zertifizierungen', '')}
                {profile.get('projekthistorie_text', '')}
            """.lower()
            
            if query_lower in searchable_text:
                results.append(profile)
        
        return results
    
    def get_available_profiles(self) -> List[Dict]:
        """Gibt verfügbare Profile zurück"""
        return [p for p in self.profiles if p.get("availability", {}).get("status") == "available"]
    
    def update_availability(self, profile_id: str, availability_data: Dict) -> bool:
        """Aktualisiert die Verfügbarkeit eines Profils"""
        update_data = {
            "availability": {
                **availability_data,
                "last_updated": datetime.now().isoformat()
            }
        }
        return self.update_profile(profile_id, update_data)

if __name__ == "__main__":
    # Test des Profile Managers
    manager = ProfileManager()
    
    # Test-Profil erstellen
    test_profile = {
        "expert_name": "Lukas Pfanner",
        "email": "lukas@example.com",
        "phone": "+49 123 456789",
        "location": "München",
        "hauptfokus": "Salesforce Consultant",
        "sprachen": "Deutsch/Englisch",
        "technologien": "Salesforce, CRM, Python",
        "zertifizierungen": "Salesforce Certified Administrator",
        "availability": {
            "status": "available",
            "start_date": "2025-01-01",
            "hours_per_week": "40",
            "remote_onsite": "both"
        }
    }
    
    # Profil erstellen
    profile_id = manager.create_profile(test_profile)
    print(f"✅ Test-Profil erstellt: {profile_id}")
    
    # Profil lesen
    profile = manager.read_profile(profile_id)
    print(f"✅ Profil gelesen: {profile['expert_name']}")
    
    # Verfügbarkeit aktualisieren
    manager.update_availability(profile_id, {
        "status": "busy",
        "start_date": "2025-02-01"
    })
    print(f"✅ Verfügbarkeit aktualisiert")
    
    # Alle Profile anzeigen
    all_profiles = manager.get_all_profiles()
    print(f"✅ Gesamt Profile: {len(all_profiles)}")

