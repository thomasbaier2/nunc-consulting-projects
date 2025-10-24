#!/usr/bin/env python3
"""
NUNC Expert Management System - Import Manager
Importiert geparste Profile in Supabase
"""

import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from profile_parser import ProfileParser, ParsedProfile
from boutique_profile_manager import BoutiqueProfileManager, Profile, BoutiqueStatus, TrustLevel, RelationshipQuality

class ImportManager:
    """Verwaltet den Import von Profilen in Supabase"""
    
    def __init__(self):
        """Initialisiert den ImportManager"""
        self.parser = ProfileParser()
        self.profile_manager = BoutiqueProfileManager()
        self.import_stats = {
            'total_files': 0,
            'successful_imports': 0,
            'failed_imports': 0,
            'skipped_imports': 0,
            'errors': []
        }
    
    def import_directory(self, directory_path: str, move_after_import: bool = True) -> Dict:
        """Importiert alle Profile aus einem Verzeichnis"""
        print(f"Starting import from: {directory_path}")
        
        try:
            # Parse alle Profile
            parsed_profiles = self.parser.parse_directory(directory_path)
            self.import_stats['total_files'] = len(parsed_profiles)
            
            print(f"Found {len(parsed_profiles)} profiles to import")
            
            # Importiere jedes Profil
            for parsed_profile in parsed_profiles:
                try:
                    success = self._import_single_profile(parsed_profile)
                    if success:
                        self.import_stats['successful_imports'] += 1
                        print(f"Imported: {parsed_profile.first_name} {parsed_profile.last_name}")
                        
                        # Verschiebe Datei nach erfolgreichem Import
                        if move_after_import:
                            self._move_file_after_import(parsed_profile.file_path)
                    else:
                        self.import_stats['skipped_imports'] += 1
                        print(f"Skipped: {parsed_profile.first_name} {parsed_profile.last_name}")
                        
                except Exception as e:
                    self.import_stats['failed_imports'] += 1
                    self.import_stats['errors'].append(f"Error importing {parsed_profile.file_path}: {e}")
                    print(f"Failed: {parsed_profile.first_name} {parsed_profile.last_name} - {e}")
            
            return self.import_stats
            
        except Exception as e:
            print(f"Import failed: {e}")
            return self.import_stats
    
    def _import_single_profile(self, parsed_profile: ParsedProfile) -> bool:
        """Importiert ein einzelnes Profil"""
        try:
            # Konvertiere ParsedProfile zu Profile
            profile = self._convert_parsed_to_profile(parsed_profile)
            
            # Prüfe ob Profil bereits existiert (basierend auf Namen + E-Mail)
            if profile.email:
                existing = self.profile_manager.supabase.table('profiles').select('id').eq('email', profile.email).execute()
                if existing.data:
                    print(f"Profile with email {profile.email} already exists - skipping")
                    return False
            
            # Zusätzliche Prüfung: Name + E-Mail Kombination
            if profile.first_name and profile.last_name:
                existing = self.profile_manager.supabase.table('profiles').select('id').eq('first_name', profile.first_name).eq('last_name', profile.last_name).execute()
                if existing.data:
                    print(f"Profile {profile.first_name} {profile.last_name} already exists - skipping")
                    return False
            
            # Füge Profil hinzu
            success, message = self.profile_manager.add_profile(profile)
            
            if success:
                print(f"Profile added: {message}")
                return True
            else:
                print(f"Failed to add profile: {message}")
                return False
                
        except Exception as e:
            print(f"Error converting profile: {e}")
            return False
    
    def _convert_parsed_to_profile(self, parsed_profile: ParsedProfile) -> Profile:
        """Konvertiert ParsedProfile zu Profile"""
        # Erstelle Profile-Objekt
        profile = Profile(
            first_name=parsed_profile.first_name,
            last_name=parsed_profile.last_name,
            email=parsed_profile.email,
            phone=parsed_profile.phone,
            location=parsed_profile.location,
            
            # Boutique-spezifische Felder
            boutique_status=BoutiqueStatus.CANDIDATE,
            trust_level=TrustLevel.NEW,
            relationship_quality=RelationshipQuality.NEW,
            
            # Skills
            technical_skills=parsed_profile.technical_skills,
            soft_skills=parsed_profile.soft_skills,
            certifications=parsed_profile.certifications,
            languages=parsed_profile.languages,
            
            # Erfahrung
            company_experience=parsed_profile.company_experience,
            project_experience=parsed_profile.project_experience,
            industry_experience=parsed_profile.industry_experience,
            
            # Verfügbarkeit
            availability_status=parsed_profile.availability_status,
            next_available_date=parsed_profile.next_available_date,
            preferred_hours_per_week=parsed_profile.preferred_hours_per_week,
            remote_preference=parsed_profile.remote_preference,
            
            # AI-Scores basierend auf Parsing-Confidence
            reliability_score=parsed_profile.parsing_confidence * 0.8,  # Konservativer Score
            experience_score=parsed_profile.parsing_confidence * 0.9,
            quality_score=parsed_profile.parsing_confidence,
            
            # Metadaten
            source='manual',
            external_id=parsed_profile.file_path
        )
        
        return profile
    
    def _move_file_after_import(self, file_path: str):
        """Verschiebt eine Datei nach erfolgreichem Import"""
        try:
            source_path = Path(file_path)
            target_dir = Path("NUNC_Expert_Management_System/12_Profile_Repository/Active_Profiles")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_path = target_dir / source_path.name
            
            # Verschiebe Datei
            source_path.rename(target_path)
            print(f"Moved file to: {target_path}")
            
        except Exception as e:
            print(f"Error moving file {file_path}: {e}")
    
    def get_import_statistics(self) -> Dict:
        """Gibt Import-Statistiken zurück"""
        return {
            'total_files': self.import_stats['total_files'],
            'successful_imports': self.import_stats['successful_imports'],
            'failed_imports': self.import_stats['failed_imports'],
            'skipped_imports': self.import_stats['skipped_imports'],
            'success_rate': (self.import_stats['successful_imports'] / max(self.import_stats['total_files'], 1)) * 100,
            'errors': self.import_stats['errors']
        }
    
    def validate_import_readiness(self) -> Tuple[bool, List[str]]:
        """Validiert ob der Import bereit ist"""
        issues = []
        
        # Prüfe ob BoutiqueProfileManager funktioniert
        try:
            count = self.profile_manager.get_profile_count()
            if count >= 100:
                issues.append(f"Profile limit reached ({count}/100)")
        except Exception as e:
            issues.append(f"BoutiqueProfileManager error: {e}")
        
        # Prüfe ob Parser-Dependencies installiert sind
        try:
            from docx import Document
        except ImportError:
            issues.append("python-docx not installed - Word files cannot be parsed")
        
        try:
            import PyPDF2
            import pdfplumber
        except ImportError:
            issues.append("PDF libraries not installed - PDF files cannot be parsed")
        
        return len(issues) == 0, issues

# Beispiel-Verwendung
if __name__ == "__main__":
    import_manager = ImportManager()
    
    # Validiere Import-Bereitschaft
    ready, issues = import_manager.validate_import_readiness()
    
    if ready:
        print("✅ Import system ready!")
        
        # Beispiel-Import
        # stats = import_manager.import_directory("path/to/your/word/profiles")
        # print(f"Import completed: {stats}")
    else:
        print("❌ Import system not ready:")
        for issue in issues:
            print(f"  - {issue}")
        
        print("\nTo fix issues:")
        print("pip install python-docx PyPDF2 pdfplumber")
