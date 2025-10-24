#!/usr/bin/env python3
"""
NUNC Expert Management System - CV Processing Component
Hauptkomponente für PDF-Verarbeitung und Datenextraktion
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

# Importiere Shared Components
import sys
sys.path.append(str(Path(__file__).parent.parent / '05_Shared_Components'))

from config import Config
from utils import validate_email, format_phone, clean_text, extract_skills_from_text
from exceptions import NemsError, ValidationError

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Installing required packages...")
    os.system("pip3 install PyPDF2 pdfplumber")
    import PyPDF2
    import pdfplumber

# Importiere lokale Modelle und Exceptions
from .models import CvData, ExtractedData, ProcessingResult, ProcessingStatus
from .exceptions import CvProcessingError, PdfExtractionError, DataValidationError, ProcessingTimeoutError

class CvProcessor:
    """Hauptklasse für CV-Verarbeitung und Datenextraktion"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.supported_formats = ['.pdf']
        self.output_dir = self.config.OUTPUT_DIR
        self.max_file_size = self.config.CV_PROCESSING.get('max_file_size', 10 * 1024 * 1024)
        self.extraction_timeout = self.config.CV_PROCESSING.get('extraction_timeout', 30)
        self.processing_timeout = self.config.CV_PROCESSING.get('processing_timeout', 120)
        
    def process_pdf(self, pdf_path: str) -> ProcessingResult:
        """Verarbeitet PDF-CV und extrahiert strukturierte Daten"""
        start_time = time.time()
        
        try:
            # Validierung
            self._validate_file(pdf_path)
            
            # PDF Text extrahieren
            text_content = self._extract_text_from_pdf(pdf_path)
            
            # CV-Daten erstellen
            cv_data = CvData(
                file_path=pdf_path,
                file_name=Path(pdf_path).name,
                file_size=Path(pdf_path).stat().st_size,
                extracted_text=text_content,
                extraction_method="pdfplumber"
            )
            
            # Strukturierte Daten extrahieren
            extracted_data = self._extract_structured_data(text_content)
            
            # NUNC-Format konvertieren
            nunc_profile = self._convert_to_nunc_format(extracted_data)
            
            # Validierung der extrahierten Daten
            if not self.validate_cv_data(nunc_profile):
                raise DataValidationError("extracted_data", "Invalid extracted data")
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                cv_data=cv_data,
                extracted_data=extracted_data,
                profile_id=nunc_profile.get('id'),
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                cv_data=cv_data if 'cv_data' in locals() else None,
                error_message=str(e),
                processing_time=processing_time
            )
    
    def _validate_file(self, pdf_path: str) -> None:
        """Validiert PDF-Datei vor Verarbeitung"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF-Datei nicht gefunden: {pdf_path}")
        
        file_size = Path(pdf_path).stat().st_size
        if file_size > self.max_file_size:
            raise ValueError(f"Datei zu groß: {file_size} bytes (max: {self.max_file_size})")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("Nur PDF-Dateien werden unterstützt")
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrahiert Text aus PDF-Datei mit verbesserter Methode"""
        try:
            # Versuche zuerst pdfplumber (bessere Qualität)
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    return text
            
            # Fallback zu PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text
                
        except Exception as e:
            raise PdfExtractionError(pdf_path, f"PDF Text-Extraktion fehlgeschlagen: {str(e)}")
    
    def _extract_structured_data(self, text: str) -> ExtractedData:
        """Extrahiert strukturierte Daten aus CV-Text"""
        # Name extrahieren
        name = self._extract_name(text)
        
        # Kontaktdaten
        contact = self._extract_contact_info(text)
        
        # Berufserfahrung
        experience = self._extract_experience(text)
        
        # Bildung
        education = self._extract_education(text)
        
        # Fähigkeiten
        skills = self._extract_skills(text)
        
        # Technische und Soft Skills trennen
        technical_skills, soft_skills = self._categorize_skills(skills)
        
        # Zertifizierungen
        certifications = self._extract_certifications(text)
        
        # Sprachen
        languages = self._extract_languages(text)
        
        # Verfügbarkeit
        availability = self._extract_availability(text)
        
        return ExtractedData(
            name=name,
            email=contact.get('email'),
            phone=contact.get('phone'),
            location=contact.get('location'),
            linkedin=contact.get('linkedin'),
            experience=experience,
            education=education,
            skills=skills,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            certifications=certifications,
            languages=languages,
            availability=availability
        )
    
    def _extract_name(self, text: str) -> str:
        """Extrahiert den Namen aus dem CV"""
        lines = text.split('\n')
        for line in lines[:5]:  # Erste 5 Zeilen prüfen
            line = line.strip()
            if len(line) > 2 and not any(char.isdigit() for char in line):
                return line
        return "Unbekannt"
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extrahiert Kontaktdaten"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?[\d\s\-\(\)]{10,})'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        return {
            'email': emails[0] if emails else '',
            'phone': phones[0] if phones else ''
        }
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extrahiert Berufserfahrung"""
        experience = []
        
        # Einfache Heuristik für Erfahrung
        lines = text.split('\n')
        current_job = {}
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['consultant', 'manager', 'developer', 'analyst', 'engineer']):
                if current_job:
                    experience.append(current_job)
                current_job = {'title': line, 'description': ''}
            elif current_job and line:
                current_job['description'] += line + ' '
        
        if current_job:
            experience.append(current_job)
        
        return experience
    
    def _extract_education(self, text: str) -> List[str]:
        """Extrahiert Bildungsweg"""
        education = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['university', 'college', 'degree', 'bachelor', 'master', 'phd']):
                education.append(line)
        
        return education
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extrahiert Fähigkeiten und Technologien mit verbesserter Logik"""
        # Verwende die Utility-Funktion aus Shared Components
        skills = extract_skills_from_text(text)
        
        # Zusätzliche spezifische Skills
        additional_skills = [
            'Salesforce', 'Python', 'Java', 'JavaScript', 'React', 'Angular',
            'SQL', 'Oracle', 'SAP', 'Microsoft', 'AWS', 'Azure', 'Docker',
            'Kubernetes', 'Git', 'Agile', 'Scrum', 'Kanban', 'DevOps',
            'Machine Learning', 'AI', 'Data Science', 'Analytics'
        ]
        
        text_lower = text.lower()
        for skill in additional_skills:
            if skill.lower() in text_lower and skill not in skills:
                skills.append(skill)
        
        return skills
    
    def _categorize_skills(self, skills: List[str]) -> tuple[List[str], List[str]]:
        """Kategorisiert Skills in technische und Soft Skills"""
        technical_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'sql', 'oracle', 'sap', 'salesforce', 'microsoft', 'aws',
            'azure', 'docker', 'kubernetes', 'git', 'devops', 'machine learning',
            'ai', 'data science', 'analytics', 'html', 'css', 'node.js'
        ]
        
        soft_skills_keywords = [
            'leadership', 'teamwork', 'communication', 'problem solving',
            'project management', 'agile', 'scrum', 'kanban', 'mentoring',
            'collaboration', 'creativity', 'adaptability'
        ]
        
        technical = []
        soft = []
        
        for skill in skills:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in technical_keywords):
                technical.append(skill)
            elif any(keyword in skill_lower for keyword in soft_skills_keywords):
                soft.append(skill)
            else:
                # Standardmäßig als technisch einordnen
                technical.append(skill)
        
        return technical, soft
    
    def _extract_certifications(self, text: str) -> List[Dict[str, str]]:
        """Extrahiert Zertifizierungen"""
        certifications = []
        
        # Zertifizierungs-Patterns
        cert_patterns = [
            r'([A-Z][a-z]+)\s+Certified\s+([A-Z][a-z]+)',
            r'([A-Z]{2,})\s+Certification',
            r'([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+Certificate'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    cert_name = ' '.join(match)
                else:
                    cert_name = match
                
                certifications.append({
                    'name': cert_name,
                    'issuer': 'Unknown',
                    'date': ''
                })
        
        return certifications
    
    def _extract_availability(self, text: str) -> Dict[str, Any]:
        """Extrahiert Verfügbarkeitsinformationen"""
        availability = {
            'start_date': '',
            'hours_per_week': 40,
            'remote': False,
            'onsite': True
        }
        
        # Verfügbarkeits-Patterns
        if 'remote' in text.lower() or 'home office' in text.lower():
            availability['remote'] = True
        
        if 'onsite' in text.lower() or 'vor ort' in text.lower():
            availability['onsite'] = True
        
        # Stunden pro Woche
        hours_pattern = r'(\d+)\s*(?:hours?|h|stunden?)'
        hours_match = re.search(hours_pattern, text, re.IGNORECASE)
        if hours_match:
            availability['hours_per_week'] = int(hours_match.group(1))
        
        return availability
    
    def validate_cv_data(self, data: Dict[str, Any]) -> bool:
        """Validiert extrahierte CV-Daten"""
        # Mindestanforderungen
        if not data.get('name') or len(data.get('name', '').strip()) < 2:
            return False
        
        # E-Mail-Validierung
        email = data.get('email', '')
        if email and not validate_email(email):
            return False
        
        # Mindestens eine Erfahrung oder Skill
        if not data.get('experience') and not data.get('skills'):
            return False
        
        return True
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extrahiert Sprachen"""
        languages = []
        
        # Sprache-Keywords
        language_keywords = ['german', 'english', 'french', 'spanish', 'italian', 'deutsch', 'englisch']
        
        text_lower = text.lower()
        for keyword in language_keywords:
            if keyword in text_lower:
                languages.append(keyword.title())
        
        return languages
    
    def _convert_to_nunc_format(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Konvertiert extrahierte Daten in NUNC-Format"""
        # Hauptfokus bestimmen
        hauptfokus = self._determine_hauptfokus(structured_data)
        
        # Zur Person Beschreibung generieren
        zur_person = self._generate_zur_person(structured_data)
        
        # Projekthistorie erstellen
        projekthistorie = self._create_projekthistorie(structured_data)
        
        return {
            'expert_name': structured_data.get('name', 'Unbekannt'),
            'email': structured_data.get('contact', {}).get('email', ''),
            'phone': structured_data.get('contact', {}).get('phone', ''),
            'hauptfokus': hauptfokus,
            'sprachen': ', '.join(structured_data.get('languages', [])),
            'zur_person': zur_person,
            'besondere_kenntnisse': ', '.join(structured_data.get('skills', [])),
            'branchenkenntnisse': 'Diverse Branchen',
            'methoden': 'Agile Methoden, Scrum',
            'technologien': ', '.join(structured_data.get('skills', [])),
            'zertifizierungen': 'Zu ermitteln',
            'projekthistorie': projekthistorie,
            'projekthistorie_text': self._create_projekthistorie_text(projekthistorie),
            'education': structured_data.get('education', []),
            'source': 'pdf',
            'tags': structured_data.get('skills', [])
        }
    
    def _determine_hauptfokus(self, data: Dict[str, Any]) -> str:
        """Bestimmt den Hauptfokus basierend auf Erfahrung"""
        experience = data.get('experience', [])
        if experience:
            return experience[0].get('title', 'Consultant')
        return 'Consultant'
    
    def _generate_zur_person(self, data: Dict[str, Any]) -> str:
        """Generiert Zur Person Beschreibung"""
        name = data.get('name', '')
        experience = data.get('experience', [])
        skills = data.get('skills', [])
        
        description = f"Erfahrener {data.get('hauptfokus', 'Consultant')} mit umfassender Expertise"
        
        if skills:
            description += f" in {', '.join(skills[:3])}"
        
        if experience:
            description += f". {len(experience)} Jahre Berufserfahrung"
        
        return description
    
    def _create_projekthistorie(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Erstellt Projekthistorie aus Erfahrung"""
        projekthistorie = []
        experience = data.get('experience', [])
        
        for i, exp in enumerate(experience):
            projekthistorie.append({
                'projekt_name': exp.get('title', f'Projekt {i+1}'),
                'zeitraum': f'2020-{2023+i}',
                'projektrolle': exp.get('title', 'Consultant'),
                'aufgaben': exp.get('description', 'Beratung und Implementierung')
            })
        
        return projekthistorie
    
    def _create_projekthistorie_text(self, projekthistorie: List[Dict[str, str]]) -> str:
        """Erstellt Text-Version der Projekthistorie"""
        text_parts = []
        for project in projekthistorie:
            text_parts.append(f"{project['projekt_name']} ({project['zeitraum']}) - {project['projektrolle']}: {project['aufgaben']}")
        return '; '.join(text_parts)

def main():
    """Test der CV-Verarbeitung"""
    print("🚀 NUNC CV Processor Test")
    
    processor = CvProcessor()
    
    # Test mit vorhandener PDF
    test_pdf = "08_Output_Files/test_results/test_cv.pdf"
    
    if os.path.exists(test_pdf):
        result = processor.process_pdf(test_pdf)
        print(f"✅ CV verarbeitet: {result.get('expert_name', 'Unbekannt')}")
        print(f"Hauptfokus: {result.get('hauptfokus', 'Unbekannt')}")
    else:
        print("⚠️ Test-PDF nicht gefunden")

if __name__ == "__main__":
    main()

