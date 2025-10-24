"""
NUNC Expert Management System - Core System Tests
Unit-Tests für Datenmodelle
"""

import pytest
from datetime import datetime
from NUNC_Expert_Management_System.core_system.models import Profile, Expert, ProfileStatus


class TestExpert:
    """Test-Klasse für Expert-Modell"""
    
    def test_expert_creation(self):
        """Test Expert-Erstellung"""
        expert = Expert(
            name="Max Mustermann",
            email="max@example.com",
            phone="+49 123 456789",
            location="Berlin"
        )
        
        assert expert.name == "Max Mustermann"
        assert expert.email == "max@example.com"
        assert expert.phone == "+49 123 456789"
        assert expert.location == "Berlin"
    
    def test_expert_to_dict(self):
        """Test Expert zu Dictionary"""
        expert = Expert(
            name="Max Mustermann",
            email="max@example.com",
            phone="+49 123 456789"
        )
        
        data = expert.to_dict()
        assert data['name'] == "Max Mustermann"
        assert data['email'] == "max@example.com"
        assert data['phone'] == "+49 123 456789"
    
    def test_expert_from_dict(self):
        """Test Expert aus Dictionary"""
        data = {
            'name': 'Anna Schmidt',
            'email': 'anna@example.com',
            'phone': '+49 987 654321',
            'location': 'München'
        }
        
        expert = Expert.from_dict(data)
        assert expert.name == "Anna Schmidt"
        assert expert.email == "anna@example.com"
        assert expert.phone == "+49 987 654321"
        assert expert.location == "München"


class TestProfile:
    """Test-Klasse für Profile-Modell"""
    
    def test_profile_creation(self, sample_expert):
        """Test Profile-Erstellung"""
        profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE
        )
        
        assert profile.id == "test_001"
        assert profile.expert == sample_expert
        assert profile.status == ProfileStatus.ACTIVE
        assert profile.is_active() is True
    
    def test_profile_to_dict(self, sample_expert):
        """Test Profile zu Dictionary"""
        profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE,
            skills=["Python", "JavaScript"],
            experience=[{"company": "Tech Corp", "position": "Developer"}]
        )
        
        data = profile.to_dict()
        assert data['id'] == "test_001"
        assert data['status'] == "active"
        assert data['skills'] == ["Python", "JavaScript"]
        assert len(data['experience']) == 1
    
    def test_profile_from_dict(self, sample_expert):
        """Test Profile aus Dictionary"""
        data = {
            'id': 'test_002',
            'expert': sample_expert.to_dict(),
            'status': 'active',
            'created_at': '2024-01-01T10:00:00',
            'updated_at': '2024-01-01T10:00:00',
            'skills': ['Java', 'Spring'],
            'experience': []
        }
        
        profile = Profile.from_dict(data)
        assert profile.id == "test_002"
        assert profile.status == ProfileStatus.ACTIVE
        assert profile.skills == ['Java', 'Spring']
    
    def test_profile_update_timestamp(self, sample_expert):
        """Test Timestamp-Update"""
        profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE
        )
        
        old_timestamp = profile.updated_at
        profile.update_timestamp()
        
        assert profile.updated_at > old_timestamp
    
    def test_profile_get_full_name(self, sample_expert):
        """Test Vollständiger Name"""
        profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE
        )
        
        assert profile.get_full_name() == sample_expert.name
    
    def test_profile_get_contact_info(self, sample_expert):
        """Test Kontaktinformationen"""
        profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE
        )
        
        contact = profile.get_contact_info()
        assert contact['email'] == sample_expert.email
        assert contact['phone'] == sample_expert.phone
        assert contact['location'] == sample_expert.location
    
    def test_profile_status_enum(self):
        """Test ProfileStatus Enum"""
        assert ProfileStatus.ACTIVE.value == "active"
        assert ProfileStatus.INACTIVE.value == "inactive"
        assert ProfileStatus.PENDING.value == "pending"
        assert ProfileStatus.ARCHIVED.value == "archived"
    
    def test_profile_is_active(self, sample_expert):
        """Test Aktiv-Status"""
        active_profile = Profile(
            id="test_001",
            expert=sample_expert,
            status=ProfileStatus.ACTIVE
        )
        
        inactive_profile = Profile(
            id="test_002",
            expert=sample_expert,
            status=ProfileStatus.INACTIVE
        )
        
        assert active_profile.is_active() is True
        assert inactive_profile.is_active() is False
