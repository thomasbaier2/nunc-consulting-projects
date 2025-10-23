#!/usr/bin/env python3
"""
NUNC CV Converter - Core CV Processing Component
Hauptkomponente für PDF-Verarbeitung und Datenextraktion
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Installing required packages...")
    os.system("pip3 install PyPDF2 pdfplumber")
    import PyPDF2
    import pdfplumber

class CvProcessor:
    """Hauptklasse für CV-Verarbeitung und Datenextraktion"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.output_dir = "07_Output_Files/generated_profiles"
        
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Verarbeitet PDF-CV und extrahiert strukturierte Daten"""
        try:
            # PDF Text extrahieren
            text_content = self._extract_text_from_pdf(pdf_path)
            
            # Strukturierte Daten extrahieren
            structured_data = self._extract_structured_data(text_content)
            
            # NUNC-Format konvertieren
            nunc_profile = self._convert_to_nunc_format(structured_data)
            
            return nunc_profile
            
        except Exception as e:
            return {'error': f'Fehler bei der PDF-Verarbeitung: {str(e)}'}
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrahiert Text aus PDF-Datei"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text
        except Exception as e:
            raise Exception(f"PDF Text-Extraktion fehlgeschlagen: {str(e)}")
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extrahiert strukturierte Daten aus CV-Text"""
        # Name extrahieren (erste Zeile oder nach bestimmten Mustern)
        name = self._extract_name(text)
        
        # Kontaktdaten
        contact = self._extract_contact_info(text)
        
        # Berufserfahrung
        experience = self._extract_experience(text)
        
        # Bildung
        education = self._extract_education(text)
        
        # Fähigkeiten
        skills = self._extract_skills(text)
        
        # Sprachen
        languages = self._extract_languages(text)
        
        return {
            'name': name,
            'contact': contact,
            'experience': experience,
            'education': education,
            'skills': skills,
            'languages': languages,
            'raw_text': text
        }
    
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
        """Extrahiert Fähigkeiten und Technologien"""
        skills = []
        
        # Technologie-Keywords
        tech_keywords = [
            'salesforce', 'python', 'java', 'javascript', 'react', 'angular',
            'sql', 'oracle', 'sap', 'microsoft', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'agile', 'scrum', 'kanban'
        ]
        
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                skills.append(keyword.title())
        
        return skills
    
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
            'hauptfokus': hauptfokus,
            'sprachen': ', '.join(structured_data.get('languages', [])),
            'zur_person': zur_person,
            'besondere_kenntnisse': ', '.join(structured_data.get('skills', [])),
            'branchenkenntnisse': 'Diverse Branchen',
            'methoden': 'Agile Methoden, Scrum',
            'technologien': ', '.join(structured_data.get('skills', [])),
            'zertifizierungen': 'Zu ermitteln',
            'projekthistorie': projekthistorie,
            'contact': structured_data.get('contact', {}),
            'education': structured_data.get('education', [])
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

def main():
    """Test der CV-Verarbeitung"""
    print("🚀 NUNC CV Processor Test")
    
    processor = CvProcessor()
    
    # Test mit vorhandener PDF
    test_pdf = "07_Output_Files/test_results/test_cv.pdf"
    
    if os.path.exists(test_pdf):
        result = processor.process_pdf(test_pdf)
        print(f"✅ CV verarbeitet: {result.get('expert_name', 'Unbekannt')}")
        print(f"Hauptfokus: {result.get('hauptfokus', 'Unbekannt')}")
    else:
        print("⚠️ Test-PDF nicht gefunden")

if __name__ == "__main__":
    main()

