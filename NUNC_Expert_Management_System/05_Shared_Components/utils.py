"""
NUNC Expert Management System - Shared Components Utilities
Gemeinsame Utility-Funktionen für alle System-Komponenten
"""

import re
import unicodedata
from typing import Optional, List, Dict, Any
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validiert E-Mail-Adresse"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_phone(phone: str) -> Optional[str]:
    """Formatiert Telefonnummer"""
    if not phone:
        return None
    
    # Entferne alle Nicht-Ziffern außer +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Deutsche Telefonnummer formatieren
    if cleaned.startswith('+49'):
        return f"+49 {cleaned[3:]}"
    elif cleaned.startswith('49'):
        return f"+49 {cleaned[2:]}"
    elif cleaned.startswith('0'):
        return f"+49 {cleaned[1:]}"
    
    return cleaned


def clean_text(text: str) -> str:
    """Bereinigt Text von unerwünschten Zeichen"""
    if not text:
        return ""
    
    # Entferne Unicode-Normalisierung
    text = unicodedata.normalize('NFKD', text)
    
    # Entferne überflüssige Leerzeichen
    text = re.sub(r'\s+', ' ', text)
    
    # Entferne führende/nachfolgende Leerzeichen
    text = text.strip()
    
    return text


def extract_skills_from_text(text: str) -> List[str]:
    """Extrahiert Skills aus Text"""
    if not text:
        return []
    
    # Häufige Tech-Skills
    tech_skills = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby',
        'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django',
        'Flask', 'Spring', 'Laravel', 'Rails', 'ASP.NET',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'Git', 'GitHub', 'GitLab', 'Jenkins', 'CI/CD'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in tech_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills


def parse_date(date_str: str) -> Optional[datetime]:
    """Parst Datum aus verschiedenen Formaten"""
    if not date_str:
        return None
    
    # Häufige Datumsformate
    formats = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%Y-%m',
        '%m/%Y',
        '%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def format_date(date: datetime) -> str:
    """Formatiert Datum für Anzeige"""
    if not date:
        return ""
    
    return date.strftime('%d.%m.%Y')


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extrahiert Kontaktinformationen aus Text"""
    contact = {
        'email': '',
        'phone': '',
        'linkedin': ''
    }
    
    if not text:
        return contact
    
    # E-Mail extrahieren
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact['email'] = email_match.group()
    
    # Telefon extrahieren
    phone_pattern = r'(\+?49\s?)?(\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4})'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact['phone'] = phone_match.group()
    
    # LinkedIn extrahieren
    linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-]+'
    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        contact['linkedin'] = linkedin_match.group()
    
    return contact


def sanitize_filename(filename: str) -> str:
    """Bereinigt Dateiname von unerwünschten Zeichen"""
    if not filename:
        return "unnamed"
    
    # Entferne gefährliche Zeichen
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Entferne führende/nachfolgende Punkte und Leerzeichen
    filename = filename.strip('. ')
    
    # Stelle sicher, dass Dateiname nicht leer ist
    if not filename:
        filename = "unnamed"
    
    return filename


def get_file_extension(filename: str) -> str:
    """Gibt Dateiendung zurück"""
    if not filename:
        return ""
    
    return filename.split('.')[-1].lower() if '.' in filename else ""


def is_supported_file_type(filename: str, supported_types: List[str]) -> bool:
    """Prüft ob Dateityp unterstützt wird"""
    extension = get_file_extension(filename)
    return extension in supported_types


def truncate_text(text: str, max_length: int = 100) -> str:
    """Kürzt Text auf maximale Länge"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Führt mehrere Dictionaries zusammen"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Sichere Dictionary-Zugriff mit verschachtelten Keys"""
    keys = key.split('.')
    current = data
    
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current
