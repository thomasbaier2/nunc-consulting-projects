# NUNC Expert Management System - CV Processing

## Überblick

Das CV Processing System verarbeitet PDF-Lebensläufe und extrahiert strukturierte Daten für das NUNC Expert Management System.

## Komponenten

### CvProcessor
Hauptklasse für PDF-Verarbeitung und Datenextraktion.

**API:**
```python
from NUNC_Expert_Management_System.cv_processing import CvProcessor

processor = CvProcessor()

# PDF verarbeiten
result = processor.process_pdf("path/to/cv.pdf")

# Text extrahieren
text = processor.extract_text("path/to/cv.pdf")

# Strukturierte Daten extrahieren
data = processor.extract_structured_data(text)

# Daten validieren
is_valid = processor.validate_cv_data(data)
```

### NuncWordGenerator
Generiert NUNC-formatierte Word-Dokumente aus Profil-Daten.

**API:**
```python
from NUNC_Expert_Management_System.cv_processing import NuncWordGenerator

generator = NuncWordGenerator()

# Word-Dokument generieren
output_path = generator.generate_word_document(profile_data, "output.docx")
```

### SupabaseIntegration
Datenbank-Integration für Profile-Speicherung.

**API:**
```python
from NUNC_Expert_Management_System.cv_processing import SupabaseIntegration

db = SupabaseIntegration()

# Profil speichern
profile_id = db.save_profile(profile_data)

# Profile abrufen
profiles = db.get_profiles()
```

## Datenmodelle

### CvData
```python
from NUNC_Expert_Management_System.cv_processing import CvData

cv_data = CvData(
    file_path="cv.pdf",
    file_name="cv.pdf",
    file_size=1024,
    extracted_text="Max Mustermann\nSenior Developer...",
    extraction_method="pdfplumber"
)
```

### ExtractedData
```python
from NUNC_Expert_Management_System.cv_processing import ExtractedData

extracted = ExtractedData(
    name="Max Mustermann",
    email="max.mustermann@example.com",
    phone="+49 123 456789",
    experience=[...],
    skills=["Python", "JavaScript"],
    technical_skills=["Python", "React"],
    soft_skills=["Teamwork", "Leadership"]
)
```

### ProcessingResult
```python
from NUNC_Expert_Management_System.cv_processing import ProcessingResult, ProcessingStatus

result = ProcessingResult(
    status=ProcessingStatus.COMPLETED,
    cv_data=cv_data,
    extracted_data=extracted,
    profile_id="profile_001",
    processing_time=2.5
)
```

## Features

- **PDF-Extraktion**: PyPDF2 und pdfplumber Support
- **KI-Integration**: OpenAI GPT für Datenextraktion
- **Word-Export**: Automatische NUNC-Template-Generierung
- **Datenbank-Integration**: Supabase Cloud-Speicherung
- **Validierung**: Umfassende Datenvalidierung
- **Error-Handling**: Robuste Fehlerbehandlung

## Tests

### Unit-Tests ausführen
```bash
cd 06_CV_Processing
python -m pytest tests/ -v
```

### Test-Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## Abhängigkeiten

Siehe `requirements.txt` für detaillierte Abhängigkeiten.

## Verwendung

### PDF-Verarbeitung
```python
from NUNC_Expert_Management_System.cv_processing import CvProcessor

processor = CvProcessor()

# PDF verarbeiten
result = processor.process_pdf("lebenslauf.pdf")

if result.get('error'):
    print(f"Fehler: {result['error']}")
else:
    print(f"Verarbeitet: {result['expert_name']}")
    print(f"E-Mail: {result['email']}")
    print(f"Skills: {result['skills']}")
```

### Word-Dokument generieren
```python
from NUNC_Expert_Management_System.cv_processing import NuncWordGenerator

generator = NuncWordGenerator()

# Word-Dokument erstellen
output_path = generator.generate_word_document(
    profile_data=result,
    output_path="NUNC_Profile_Max_Mustermann.docx"
)

print(f"Word-Dokument erstellt: {output_path}")
```

### Supabase-Integration
```python
from NUNC_Expert_Management_System.cv_processing import SupabaseIntegration

db = SupabaseIntegration()

# Profil in Datenbank speichern
profile_id = db.save_profile(result)
print(f"Profil gespeichert: {profile_id}")

# Profile aus Datenbank abrufen
profiles = db.get_profiles()
print(f"Gefunden: {len(profiles)} Profile")
```

## Fehlerbehandlung

Das CV Processing System verwendet spezialisierte Exceptions:

- `PdfExtractionError`: PDF-Extraktionsfehler
- `DataValidationError`: Datenvalidierungsfehler
- `WordGenerationError`: Word-Dokument-Fehler
- `SupabaseIntegrationError`: Datenbank-Fehler
- `FileFormatError`: Ungültige Dateiformate
- `ProcessingTimeoutError`: Verarbeitungs-Timeout

## Konfiguration

Das CV Processing System verwendet die zentrale Konfiguration aus `05_Shared_Components/config.py`.

### Umgebungsvariablen
```bash
OPENAI_API_KEY=your_openai_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Unterstützte Formate

- **PDF**: Vollständige Unterstützung
- **Word**: Export-Format
- **JSON**: Daten-Austausch

## Performance

- **PDF-Extraktion**: ~1-3 Sekunden pro Seite
- **KI-Verarbeitung**: ~2-5 Sekunden pro CV
- **Word-Generierung**: ~1-2 Sekunden pro Dokument
- **Datenbank-Speicherung**: ~0.5-1 Sekunde pro Profil
