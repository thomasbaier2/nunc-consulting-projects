# project_matcher.py
"""
NUNC Expert Management System - Projekt-Matching
AI-basiertes Matching von Projekten mit Experten
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

class ProjectMatcher:
    """AI-basiertes Matching von Projekten mit Experten"""
    
    def __init__(self):
        self.projects_file = Path("08_Output_Files/projects.json")
        self.matches_file = Path("08_Output_Files/project_matches.json")
        
        # Erstelle Ordner falls nicht vorhanden
        self.projects_file.parent.mkdir(parents=True, exist_ok=True)
        self.matches_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Lade bestehende Daten
        self.projects = self._load_projects()
        self.matches = self._load_matches()
    
    def _load_projects(self) -> List[Dict]:
        """Lädt Projekte aus lokaler Datei"""
        if self.projects_file.exists():
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _load_matches(self) -> List[Dict]:
        """Lädt Matches aus lokaler Datei"""
        if self.matches_file.exists():
            with open(self.matches_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_projects(self):
        """Speichert Projekte in lokaler Datei"""
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, indent=4, ensure_ascii=False)
    
    def _save_matches(self):
        """Speichert Matches in lokaler Datei"""
        with open(self.matches_file, 'w', encoding='utf-8') as f:
            json.dump(self.matches, f, indent=4, ensure_ascii=False)
    
    def create_project(self, project_data: Dict) -> str:
        """Erstellt ein neues Projekt"""
        project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Vollständige Projekt-Struktur
        full_project = {
            "id": project_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active",  # active, completed, cancelled
            
            # Projekt-Informationen
            "title": project_data.get("title", ""),
            "description": project_data.get("description", ""),
            "client": project_data.get("client", ""),
            "industry": project_data.get("industry", ""),
            
            # Zeitliche Anforderungen
            "start_date": project_data.get("start_date", ""),
            "duration": project_data.get("duration", ""),
            "hours_per_week": project_data.get("hours_per_week", ""),
            "deadline": project_data.get("deadline", ""),
            
            # Standort & Remote
            "location": project_data.get("location", ""),
            "remote_onsite": project_data.get("remote_onsite", "both"),
            "travel_required": project_data.get("travel_required", False),
            
            # Technische Anforderungen
            "required_skills": project_data.get("required_skills", []),
            "preferred_skills": project_data.get("preferred_skills", []),
            "technologies": project_data.get("technologies", []),
            "certifications": project_data.get("certifications", []),
            
            # Erfahrungs-Anforderungen
            "min_experience": project_data.get("min_experience", 0),
            "max_experience": project_data.get("max_experience", 99),
            "experience_level": project_data.get("experience_level", "mid"),  # junior, mid, senior, lead
            
            # Sprach-Anforderungen
            "languages": project_data.get("languages", ["Deutsch"]),
            "language_level": project_data.get("language_level", "fluent"),
            
            # Soft Skills
            "soft_skills": project_data.get("soft_skills", []),
            "leadership_required": project_data.get("leadership_required", False),
            "team_size": project_data.get("team_size", 1),
            
            # Budget & Vertrag
            "budget_range": project_data.get("budget_range", ""),
            "contract_type": project_data.get("contract_type", "freelance"),  # freelance, permanent, contract
            "urgency": project_data.get("urgency", "normal"),  # low, normal, high, urgent
            
            # Zusätzliche Informationen
            "notes": project_data.get("notes", ""),
            "tags": project_data.get("tags", []),
            "priority": project_data.get("priority", "medium")  # low, medium, high
        }
        
        # Projekt speichern
        self.projects.append(full_project)
        self._save_projects()
        
        print(f"✅ Projekt erstellt: {project_id}")
        return project_id
    
    def match_experts_to_project(self, project_id: str, expert_profiles: List[Dict]) -> List[Dict]:
        """Matcht Experten zu einem Projekt"""
        project = self._get_project(project_id)
        if not project:
            print(f"❌ Projekt nicht gefunden: {project_id}")
            return []
        
        print(f"🔍 Matche Experten zu Projekt: {project['title']}")
        
        matches = []
        
        for expert in expert_profiles:
            # Berechne Match-Score
            match_score = self._calculate_match_score(project, expert)
            
            # Nur relevante Matches
            if match_score >= 0.3:  # Mindest-Score
                match = {
                    "expert_id": expert.get("id", ""),
                    "expert_name": expert.get("expert_name", ""),
                    "match_score": match_score,
                    "matched_at": datetime.now().isoformat(),
                    "match_reasons": self._get_match_reasons(project, expert),
                    "gaps": self._get_gaps(project, expert)
                }
                matches.append(match)
        
        # Sortiere nach Match-Score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Speichere Matches
        match_record = {
            "id": f"match_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "matches": matches,
            "total_matches": len(matches)
        }
        
        self.matches.append(match_record)
        self._save_matches()
        
        print(f"✅ {len(matches)} Matches gefunden")
        return matches
    
    def _get_project(self, project_id: str) -> Optional[Dict]:
        """Gibt ein Projekt anhand der ID zurück"""
        for project in self.projects:
            if project["id"] == project_id:
                return project
        return None
    
    def _calculate_match_score(self, project: Dict, expert: Dict) -> float:
        """Berechnet den Match-Score zwischen Projekt und Experte"""
        score = 0.0
        
        # Skills-Matching (40% Gewichtung)
        required_skills = project.get("required_skills", [])
        expert_skills = expert.get("technologien", "").split(", ")
        expert_skills = [skill.strip() for skill in expert_skills if skill.strip()]
        
        if required_skills:
            skill_matches = len(set(required_skills) & set(expert_skills))
            skill_score = skill_matches / len(required_skills)
            score += skill_score * 0.4
        
        # Erfahrungs-Matching (20% Gewichtung)
        required_experience = project.get("min_experience", 0)
        expert_experience = self._extract_experience_from_text(expert.get("projekthistorie_text", ""))
        
        if expert_experience >= required_experience:
            score += 0.2
        
        # Branchen-Matching (15% Gewichtung)
        project_industry = project.get("industry", "").lower()
        expert_industries = expert.get("branchenkenntnisse", "").lower()
        
        if project_industry and project_industry in expert_industries:
            score += 0.15
        
        # Verfügbarkeit (15% Gewichtung)
        if expert.get("availability", {}).get("status") == "available":
            score += 0.15
        
        # Zertifizierungen (10% Gewichtung)
        required_certs = project.get("certifications", [])
        expert_certs = expert.get("zertifizierungen", "").split(", ")
        expert_certs = [cert.strip() for cert in expert_certs if cert.strip()]
        
        if required_certs:
            cert_matches = len(set(required_certs) & set(expert_certs))
            cert_score = cert_matches / len(required_certs)
            score += cert_score * 0.1
        
        return min(score, 1.0)  # Maximal 1.0
    
    def _extract_experience_from_text(self, text: str) -> int:
        """Extrahiert Jahre aus Text"""
        if not text:
            return 0
        
        # Suche nach Jahren in der Projekthistorie
        years = re.findall(r'(\d+)\s*(?:jahr|year|jahren|years)', text.lower())
        if years:
            return max([int(year) for year in years])
        
        return 0
    
    def _get_match_reasons(self, project: Dict, expert: Dict) -> List[str]:
        """Gibt Gründe für das Matching zurück"""
        reasons = []
        
        # Skills-Matches
        required_skills = project.get("required_skills", [])
        expert_skills = expert.get("technologien", "").split(", ")
        expert_skills = [skill.strip() for skill in expert_skills if skill.strip()]
        
        matching_skills = set(required_skills) & set(expert_skills)
        if matching_skills:
            reasons.append(f"Skills: {', '.join(matching_skills)}")
        
        # Branchen-Match
        project_industry = project.get("industry", "")
        expert_industries = expert.get("branchenkenntnisse", "")
        if project_industry and project_industry.lower() in expert_industries.lower():
            reasons.append(f"Branche: {project_industry}")
        
        # Zertifizierungen
        required_certs = project.get("certifications", [])
        expert_certs = expert.get("zertifizierungen", "").split(", ")
        expert_certs = [cert.strip() for cert in expert_certs if cert.strip()]
        
        matching_certs = set(required_certs) & set(expert_certs)
        if matching_certs:
            reasons.append(f"Zertifizierungen: {', '.join(matching_certs)}")
        
        return reasons
    
    def _get_gaps(self, project: Dict, expert: Dict) -> List[str]:
        """Gibt Lücken zwischen Projekt und Experte zurück"""
        gaps = []
        
        # Fehlende Skills
        required_skills = project.get("required_skills", [])
        expert_skills = expert.get("technologien", "").split(", ")
        expert_skills = [skill.strip() for skill in expert_skills if skill.strip()]
        
        missing_skills = set(required_skills) - set(expert_skills)
        if missing_skills:
            gaps.append(f"Fehlende Skills: {', '.join(missing_skills)}")
        
        # Fehlende Zertifizierungen
        required_certs = project.get("certifications", [])
        expert_certs = expert.get("zertifizierungen", "").split(", ")
        expert_certs = [cert.strip() for cert in expert_certs if cert.strip()]
        
        missing_certs = set(required_certs) - set(expert_certs)
        if missing_certs:
            gaps.append(f"Fehlende Zertifizierungen: {', '.join(missing_certs)}")
        
        return gaps
    
    def get_project_matches(self, project_id: str) -> List[Dict]:
        """Gibt Matches für ein Projekt zurück"""
        for match_record in self.matches:
            if match_record["project_id"] == project_id:
                return match_record["matches"]
        return []
    
    def get_all_projects(self) -> List[Dict]:
        """Gibt alle Projekte zurück"""
        return self.projects
    
    def get_active_projects(self) -> List[Dict]:
        """Gibt aktive Projekte zurück"""
        return [p for p in self.projects if p["status"] == "active"]

if __name__ == "__main__":
    # Test des Project Matchers
    matcher = ProjectMatcher()
    
    # Test-Projekt erstellen
    project_data = {
        "title": "Salesforce Implementation",
        "description": "Implementierung einer neuen Salesforce-Instanz für einen Kunden",
        "client": "TechCorp GmbH",
        "industry": "Technology",
        "start_date": "2025-01-15",
        "duration": "6 Monate",
        "hours_per_week": "40",
        "location": "München",
        "remote_onsite": "Hybrid",
        "required_skills": ["Salesforce", "CRM", "Python"],
        "technologies": ["Salesforce", "Apex", "Lightning"],
        "certifications": ["Salesforce Certified Administrator"],
        "min_experience": 3,
        "experience_level": "senior"
    }
    
    project_id = matcher.create_project(project_data)
    print(f"✅ Test-Projekt erstellt: {project_id}")
    
    # Test-Experten
    test_experts = [
        {
            "id": "expert_1",
            "expert_name": "Lukas Pfanner",
            "technologien": "Salesforce, CRM, Python",
            "branchenkenntnisse": "Technology, Retail",
            "zertifizierungen": "Salesforce Certified Administrator",
            "projekthistorie_text": "5 Jahre Erfahrung in Salesforce-Implementierungen",
            "availability": {"status": "available"}
        },
        {
            "id": "expert_2",
            "expert_name": "Sarah Weber",
            "technologien": "Java, Spring, Microservices",
            "branchenkenntnisse": "Finance, Banking",
            "zertifizierungen": "AWS Certified Developer",
            "projekthistorie_text": "3 Jahre Erfahrung in Java-Entwicklung",
            "availability": {"status": "available"}
        }
    ]
    
    # Matches berechnen
    matches = matcher.match_experts_to_project(project_id, test_experts)
    
    # Ergebnisse anzeigen
    print(f"\n🎯 Projekt-Matches:")
    for i, match in enumerate(matches, 1):
        print(f"{i}. {match['expert_name']} - Score: {match['match_score']:.2f}")
        print(f"   Gründe: {', '.join(match['match_reasons'])}")
        if match['gaps']:
            print(f"   Lücken: {', '.join(match['gaps'])}")
        print()

