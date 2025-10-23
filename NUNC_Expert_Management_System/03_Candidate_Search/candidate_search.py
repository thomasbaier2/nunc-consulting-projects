# candidate_search.py
"""
NUNC Expert Management System - Kandidaten-Suche
Automatisierte Suche auf LinkedIn und Freelancermap
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

class CandidateSearch:
    """Automatisierte Kandidaten-Suche auf verschiedenen Plattformen"""
    
    def __init__(self):
        self.search_results_file = Path("08_Output_Files/candidate_search_results.json")
        self.search_results_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Lade bestehende Suchergebnisse
        self.search_results = self._load_search_results()
    
    def _load_search_results(self) -> List[Dict]:
        """Lädt Suchergebnisse aus lokaler Datei"""
        if self.search_results_file.exists():
            with open(self.search_results_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_search_results(self):
        """Speichert Suchergebnisse in lokaler Datei"""
        with open(self.search_results_file, 'w', encoding='utf-8') as f:
            json.dump(self.search_results, f, indent=4, ensure_ascii=False)
    
    def search_linkedin(self, search_params: Dict) -> List[Dict]:
        """Sucht Kandidaten auf LinkedIn (Simulation)"""
        print("🔍 Suche auf LinkedIn...")
        
        # Simulierte LinkedIn-Suche (in Produktion würde hier die LinkedIn API verwendet)
        linkedin_results = [
            {
                "platform": "linkedin",
                "name": "Dr. Sarah Weber",
                "title": "Senior Salesforce Consultant",
                "location": "München, Deutschland",
                "experience": "8 Jahre",
                "skills": ["Salesforce", "CRM", "Python", "Agile"],
                "certifications": ["Salesforce Certified Administrator", "PMP"],
                "profile_url": "https://linkedin.com/in/sarah-weber",
                "availability": "available",
                "match_score": 0.95
            },
            {
                "platform": "linkedin",
                "name": "Michael Schmidt",
                "title": "Salesforce Developer",
                "location": "Berlin, Deutschland",
                "experience": "5 Jahre",
                "skills": ["Salesforce", "Apex", "Lightning", "JavaScript"],
                "certifications": ["Salesforce Certified Developer"],
                "profile_url": "https://linkedin.com/in/michael-schmidt",
                "availability": "available",
                "match_score": 0.88
            }
        ]
        
        # Filtere basierend auf Suchparametern
        filtered_results = self._filter_candidates(linkedin_results, search_params)
        
        print(f"✅ LinkedIn: {len(filtered_results)} Kandidaten gefunden")
        return filtered_results
    
    def search_freelancermap(self, search_params: Dict) -> List[Dict]:
        """Sucht Kandidaten auf Freelancermap (Simulation)"""
        print("🔍 Suche auf Freelancermap...")
        
        # Simulierte Freelancermap-Suche
        freelancermap_results = [
            {
                "platform": "freelancermap",
                "name": "Thomas Müller",
                "title": "Freelance Salesforce Consultant",
                "location": "Hamburg, Deutschland",
                "experience": "6 Jahre",
                "skills": ["Salesforce", "CRM", "Integration", "Consulting"],
                "certifications": ["Salesforce Certified Administrator"],
                "profile_url": "https://freelancermap.de/profile/thomas-mueller",
                "availability": "available",
                "match_score": 0.92
            },
            {
                "platform": "freelancermap",
                "name": "Anna Fischer",
                "title": "Salesforce Technical Architect",
                "location": "Stuttgart, Deutschland",
                "experience": "10 Jahre",
                "skills": ["Salesforce", "Architecture", "Integration", "Leadership"],
                "certifications": ["Salesforce Certified Technical Architect"],
                "profile_url": "https://freelancermap.de/profile/anna-fischer",
                "availability": "busy",
                "match_score": 0.85
            }
        ]
        
        # Filtere basierend auf Suchparametern
        filtered_results = self._filter_candidates(freelancermap_results, search_params)
        
        print(f"✅ Freelancermap: {len(filtered_results)} Kandidaten gefunden")
        return filtered_results
    
    def _filter_candidates(self, candidates: List[Dict], search_params: Dict) -> List[Dict]:
        """Filtert Kandidaten basierend auf Suchparametern"""
        filtered = []
        
        for candidate in candidates:
            match_score = 0.0
            
            # Skills-Matching
            required_skills = search_params.get("required_skills", [])
            candidate_skills = candidate.get("skills", [])
            
            if required_skills:
                skill_matches = len(set(required_skills) & set(candidate_skills))
                skill_score = skill_matches / len(required_skills)
                match_score += skill_score * 0.4
            
            # Location-Matching
            preferred_location = search_params.get("location", "").lower()
            candidate_location = candidate.get("location", "").lower()
            
            if preferred_location and preferred_location in candidate_location:
                match_score += 0.2
            
            # Experience-Matching
            required_experience = search_params.get("min_experience", 0)
            candidate_experience = self._extract_experience_years(candidate.get("experience", "0"))
            
            if candidate_experience >= required_experience:
                match_score += 0.2
            
            # Availability-Matching
            if candidate.get("availability") == "available":
                match_score += 0.2
            
            # Nur Kandidaten mit Mindest-Score
            if match_score >= search_params.get("min_match_score", 0.5):
                candidate["calculated_match_score"] = match_score
                filtered.append(candidate)
        
        # Sortiere nach Match-Score
        filtered.sort(key=lambda x: x["calculated_match_score"], reverse=True)
        
        return filtered
    
    def _extract_experience_years(self, experience_str: str) -> int:
        """Extrahiert Jahre aus Erfahrungs-String"""
        if not experience_str:
            return 0
        
        # Suche nach Zahlen in der Erfahrungs-Beschreibung
        numbers = re.findall(r'\d+', experience_str)
        if numbers:
            return int(numbers[0])
        
        return 0
    
    def search_all_platforms(self, search_params: Dict) -> List[Dict]:
        """Sucht auf allen Plattformen"""
        print("🚀 Starte Kandidaten-Suche auf allen Plattformen...")
        
        all_results = []
        
        # LinkedIn-Suche
        try:
            linkedin_results = self.search_linkedin(search_params)
            all_results.extend(linkedin_results)
        except Exception as e:
            print(f"❌ LinkedIn-Suche fehlgeschlagen: {e}")
        
        # Freelancermap-Suche
        try:
            freelancermap_results = self.search_freelancermap(search_params)
            all_results.extend(freelancermap_results)
        except Exception as e:
            print(f"❌ Freelancermap-Suche fehlgeschlagen: {e}")
        
        # Ergebnisse speichern
        search_result = {
            "id": f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "search_params": search_params,
            "results": all_results,
            "total_candidates": len(all_results)
        }
        
        self.search_results.append(search_result)
        self._save_search_results()
        
        print(f"✅ Gesamt: {len(all_results)} Kandidaten gefunden")
        return all_results
    
    def get_search_history(self) -> List[Dict]:
        """Gibt Suchhistorie zurück"""
        return self.search_results
    
    def get_candidate_details(self, candidate_id: str) -> Optional[Dict]:
        """Gibt Details zu einem Kandidaten zurück"""
        for search_result in self.search_results:
            for candidate in search_result["results"]:
                if candidate.get("id") == candidate_id:
                    return candidate
        return None
    
    def create_candidate_profile(self, candidate_data: Dict) -> str:
        """Erstellt ein Profil aus Kandidaten-Daten"""
        # Kandidaten-Daten in Profil-Format konvertieren
        profile_data = {
            "expert_name": candidate_data.get("name", ""),
            "hauptfokus": candidate_data.get("title", ""),
            "location": candidate_data.get("location", ""),
            "technologien": ", ".join(candidate_data.get("skills", [])),
            "zertifizierungen": ", ".join(candidate_data.get("certifications", [])),
            "source": "candidate_search",
            "platform": candidate_data.get("platform", ""),
            "profile_url": candidate_data.get("profile_url", ""),
            "match_score": candidate_data.get("match_score", 0.0)
        }
        
        # Profil-ID generieren
        profile_id = f"candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"✅ Kandidaten-Profil erstellt: {profile_id}")
        return profile_id

if __name__ == "__main__":
    # Test der Kandidaten-Suche
    searcher = CandidateSearch()
    
    # Test-Suchparameter
    search_params = {
        "required_skills": ["Salesforce", "CRM"],
        "location": "München",
        "min_experience": 3,
        "min_match_score": 0.7
    }
    
    # Suche starten
    results = searcher.search_all_platforms(search_params)
    
    # Ergebnisse anzeigen
    print(f"\n🎯 Suchergebnisse:")
    for i, candidate in enumerate(results[:3], 1):
        print(f"{i}. {candidate['name']} - {candidate['title']}")
        print(f"   Score: {candidate['calculated_match_score']:.2f}")
        print(f"   Skills: {', '.join(candidate['skills'])}")
        print(f"   Platform: {candidate['platform']}")
        print()

