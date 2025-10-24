# NUNC Expert Management System - Core System

## Überblick

Das Core System ist das Herzstück des NUNC Expert Management Systems und verwaltet alle Experten-Profile mit vollständigen CRUD-Operationen.

## Komponenten

### ProfileManager
Hauptklasse für die Verwaltung von Experten-Profilen.

**API:**
```python
from NUNC_Expert_Management_System.core_system import ProfileManager

manager = ProfileManager()

# Profil erstellen
profile_id = manager.create_profile(profile_data)

# Profil abrufen
profile = manager.get_profile(profile_id)

# Profil aktualisieren
manager.update_profile(profile_id, updates)

# Profil löschen
manager.delete_profile(profile_id)

# Profile suchen
results = manager.search_profiles(query)
```

### Datenmodelle

#### Expert
```python
from NUNC_Expert_Management_System.core_system import Expert

expert = Expert(
    name="Max Mustermann",
    email="max.mustermann@example.com",
    phone="+49 123 456789",
    location="Berlin, Deutschland"
)
```

#### Profile
```python
from NUNC_Expert_Management_System.core_system import Profile, ProfileStatus

profile = Profile(
    id="profile_001",
    expert=expert,
    status=ProfileStatus.ACTIVE,
    skills=["Python", "JavaScript", "React"],
    experience=[...],
    availability={...}
)
```

## Features

- **CRUD-Operationen**: Vollständige Profil-Verwaltung
- **Validierung**: Automatische Datenvalidierung
- **Suche**: Flexible Profil-Suche
- **Persistierung**: Lokale JSON-Speicherung
- **Supabase-Integration**: Cloud-Datenbank-Support

## Tests

### Unit-Tests ausführen
```bash
cd 01_Core_System
python -m pytest tests/ -v
```

### Test-Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## Abhängigkeiten

Siehe `requirements.txt` für detaillierte Abhängigkeiten.

## Verwendung

```python
# Beispiel: Profil erstellen
from NUNC_Expert_Management_System.core_system import ProfileManager, Expert, ProfileStatus

manager = ProfileManager()

# Experte erstellen
expert = Expert(
    name="Anna Schmidt",
    email="anna.schmidt@example.com",
    phone="+49 987 654321",
    location="München, Deutschland"
)

# Profil-Daten
profile_data = {
    "expert": expert.to_dict(),
    "status": "active",
    "skills": ["Java", "Spring", "Microservices"],
    "experience": [
        {
            "company": "Tech Corp",
            "position": "Senior Developer",
            "start_date": "2020-01-01",
            "end_date": "2023-12-31"
        }
    ],
    "availability": {
        "start_date": "2024-01-01",
        "hours_per_week": 40,
        "remote": True
    }
}

# Profil erstellen
profile_id = manager.create_profile(profile_data)
print(f"Profil erstellt: {profile_id}")

# Profil abrufen
profile = manager.get_profile(profile_id)
print(f"Profil: {profile['expert']['name']}")
```

## Fehlerbehandlung

Das Core System verwendet spezialisierte Exceptions:

- `ProfileNotFoundError`: Profil nicht gefunden
- `ProfileValidationError`: Validierungsfehler
- `ProfileDuplicateError`: Doppelte Profile
- `ProfileStorageError`: Speicher-Fehler

## Konfiguration

Das Core System verwendet die zentrale Konfiguration aus `05_Shared_Components/config.py`.
