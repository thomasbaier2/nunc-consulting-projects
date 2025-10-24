"""
NUNC Expert Management System - Core System Tests
Unit-Tests für ProfileManager
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Importiere die zu testenden Module
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from NUNC_Expert_Management_System.core_system.profile_manager import ProfileManager
from NUNC_Expert_Management_System.core_system.models import Profile, Expert, ProfileStatus
from NUNC_Expert_Management_System.core_system.exceptions import ProfileNotFoundError, ProfileValidationError


class TestProfileManager:
    """Test-Klasse für ProfileManager"""
    
    def test_init(self, temp_dir):
        """Test ProfileManager Initialisierung"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        assert manager.profiles_file == profiles_file
        assert manager.profiles == []
    
    def test_create_profile(self, temp_dir, sample_profile):
        """Test Profil-Erstellung"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        profile_data = sample_profile.to_dict()
        profile_id = manager.create_profile(profile_data)
        
        assert profile_id is not None
        assert profile_id in [p['id'] for p in manager.profiles]
        
        # Prüfe ob Datei erstellt wurde
        assert profiles_file.exists()
    
    def test_get_profile(self, temp_dir, sample_profile):
        """Test Profil-Abruf"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle Profil
        profile_data = sample_profile.to_dict()
        profile_id = manager.create_profile(profile_data)
        
        # Hole Profil
        retrieved_profile = manager.get_profile(profile_id)
        assert retrieved_profile is not None
        assert retrieved_profile['id'] == profile_id
    
    def test_get_profile_not_found(self, temp_dir):
        """Test Profil nicht gefunden"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        with pytest.raises(ProfileNotFoundError):
            manager.get_profile("nonexistent_id")
    
    def test_update_profile(self, temp_dir, sample_profile):
        """Test Profil-Update"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle Profil
        profile_data = sample_profile.to_dict()
        profile_id = manager.create_profile(profile_data)
        
        # Update Profil
        updates = {"expert_name": "Updated Name"}
        result = manager.update_profile(profile_id, updates)
        
        assert result is True
        
        # Prüfe Update
        updated_profile = manager.get_profile(profile_id)
        assert updated_profile['expert_name'] == "Updated Name"
    
    def test_delete_profile(self, temp_dir, sample_profile):
        """Test Profil-Löschung"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle Profil
        profile_data = sample_profile.to_dict()
        profile_id = manager.create_profile(profile_data)
        
        # Lösche Profil
        result = manager.delete_profile(profile_id)
        assert result is True
        
        # Prüfe dass Profil gelöscht wurde
        with pytest.raises(ProfileNotFoundError):
            manager.get_profile(profile_id)
    
    def test_search_profiles(self, temp_dir, sample_profile):
        """Test Profil-Suche"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle mehrere Profile
        profile_data = sample_profile.to_dict()
        manager.create_profile(profile_data)
        
        # Suche nach E-Mail
        results = manager.search_profiles({"email": sample_profile.expert.email})
        assert len(results) > 0
        assert results[0]['expert']['email'] == sample_profile.expert.email
    
    def test_duplicate_email_validation(self, temp_dir, sample_profile):
        """Test Duplikat-E-Mail Validierung"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle erstes Profil
        profile_data = sample_profile.to_dict()
        manager.create_profile(profile_data)
        
        # Versuche zweites Profil mit gleicher E-Mail
        profile_data2 = sample_profile.to_dict()
        profile_data2['id'] = 'different_id'
        
        # Sollte Duplikat-Fehler werfen
        with pytest.raises(Exception):  # ProfileDuplicateError
            manager.create_profile(profile_data2)
    
    def test_profile_validation(self, temp_dir):
        """Test Profil-Validierung"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Ungültige Profil-Daten
        invalid_data = {
            "expert_name": "",  # Leerer Name
            "email": "invalid-email"  # Ungültige E-Mail
        }
        
        with pytest.raises(ProfileValidationError):
            manager.create_profile(invalid_data)
    
    def test_save_and_load_profiles(self, temp_dir, sample_profile):
        """Test Speichern und Laden von Profilen"""
        profiles_file = temp_dir / "profiles.json"
        manager = ProfileManager(profiles_file=str(profiles_file))
        
        # Erstelle Profil
        profile_data = sample_profile.to_dict()
        profile_id = manager.create_profile(profile_data)
        
        # Erstelle neuen Manager (simuliert Neustart)
        manager2 = ProfileManager(profiles_file=str(profiles_file))
        
        # Prüfe dass Profil geladen wurde
        assert len(manager2.profiles) == 1
        assert manager2.get_profile(profile_id) is not None
