# NUNC Expert Management System (NEMS)

## 🎯 Überblick

Das **NUNC Expert Management System (NEMS)** ist ein vollständiges Expert-Management-System für NUNC Consulting GmbH mit sauberer Komponenten-Architektur und umfassender Test-Abdeckung.

## 🏗️ System-Architektur

### **Phase 1: Core System** ✅ (Strukturiert & Getestet)
- **Profil-Management**: PDF → Text → Strukturierte Daten
- **CV-Processing**: PDF-Extraktion, KI-Verarbeitung, Word-Export
- **Supabase Integration**: Vector Database für Semantic Search
- **Web-Interface**: Upload, Verarbeitung, Download
- **Test-Infrastruktur**: Unit-Tests, Integration-Tests, E2E-Tests

### **Phase 2: Verfügbarkeits-Management** 🚀
- **Mail-Tool**: Automatische Verfügbarkeits-Abfrage
- **Link-Tool**: Quick-Response System
- **Verfügbarkeits-Tracking**: Automatische Updates

### **Phase 3: Kandidaten-Suche** 🔍
- **LinkedIn-Scraping**: Automatisierte Kandidaten-Suche
- **Freelancermap-Scraping**: Freelancer-Integration
- **AI-Matching**: Semantic Search & Ranking

### **Phase 4: Projekt-Matching** 🎯
- **Projekt-Anforderungen**: Automatische Analyse
- **Kandidaten-Matching**: AI-basiertes Matching
- **End-to-End Workflow**: Vollständiger Prozess

## 📁 Ordnerstruktur

```
NUNC_Expert_Management_System/
├── 01_Core_System/           # Phase 1: Core System (Strukturiert & Getestet)
│   ├── __init__.py
│   ├── profile_manager.py
│   ├── models.py
│   ├── exceptions.py
│   ├── tests/
│   └── requirements.txt
├── 02_Availability_System/  # Phase 2: Verfügbarkeits-Management
├── 03_Candidate_Search/     # Phase 3: Kandidaten-Suche
├── 04_Project_Matching/     # Phase 4: Projekt-Matching
├── 05_Shared_Components/    # Gemeinsame Komponenten (Strukturiert)
│   ├── __init__.py
│   ├── config.py
│   ├── base_models.py
│   ├── utils.py
│   ├── exceptions.py
│   └── web_interface.py
├── 06_CV_Processing/        # CV-Verarbeitung (Strukturiert & Getestet)
│   ├── __init__.py
│   ├── cv_processor.py
│   ├── word_generator.py
│   ├── supabase_integration.py
│   ├── models.py
│   ├── exceptions.py
│   ├── tests/
│   └── requirements.txt
├── 07_Utilities/            # Utility-Skripte
├── 08_Output_Files/        # Output & Logs
├── 09_Testing/             # Test-Infrastruktur
├── 10_Project_Preferences/ # VS Code Einstellungen
├── profiles.json           # Wichtige Datenbank-Datei
├── requirements.txt        # Gesamte Abhängigkeiten
└── README.md
```

## 🚀 Features

### **Profil-Management**
- PDF → Text Extraktion
- Strukturierte Daten (Sprache, Zertifizierungen, etc.)
- Persönliche Daten (Name, E-Mail, Handy)
- Verfügbarkeit (Datum, Stunden, Remote/Onsite)
- Charakter (Soft Skills, Arbeitsweise)

### **Verfügbarkeits-Management**
- Automatische E-Mail-Abfrage
- Link-basierte Quick-Response
- Verfügbarkeits-Tracking
- Automatische Updates

### **Kandidaten-Suche**
- LinkedIn-Scraping
- Freelancermap-Scraping
- AI-basiertes Matching
- Kandidaten-Ranking

### **Projekt-Matching**
- Projekt-Anforderungen → Kandidaten
- Verfügbarkeits-Check → Matching
- End-to-End Workflow
- Reporting & Analytics

## 🔧 Technologie-Stack

- **Backend**: Python (Flask)
- **Database**: Supabase (PostgreSQL + pg_vector)
- **AI**: OpenAI (Embeddings, Semantic Search)
- **Frontend**: HTML/CSS/JavaScript
- **Scraping**: Selenium, BeautifulSoup
- **Deployment**: Docker, Cloud (Railway/Render)

## 🧪 Testing

### Test-Ausführung
```bash
# Alle Tests
python -m pytest 09_Testing/ -v

# Mit Coverage
python -m pytest 09_Testing/ --cov=. --cov-report=html

# Spezifische Komponenten
python -m pytest 01_Core_System/tests/ -v
python -m pytest 06_CV_Processing/tests/ -v
```

### Coverage-Ziele
- **Core System**: > 90%
- **CV Processing**: > 85%
- **Shared Components**: > 95%
- **Gesamt**: > 80%

## 📋 Nächste Schritte

1. **Phase 1**: ✅ Core System strukturiert und getestet
2. **Phase 2**: Verfügbarkeits-Management implementieren
3. **Phase 3**: Kandidaten-Suche entwickeln
4. **Phase 4**: Projekt-Matching aufbauen

## 🎯 Ziel

Ein vollständiges, automatisiertes Expert-Management-System für NUNC Consulting GmbH.

