# NUNC Expert Management System (NEMS)

## 🎯 Überblick

Das **NUNC Expert Management System (NEMS)** ist ein vollständiges Expert-Management-System für NUNC Consulting GmbH.

## 🏗️ System-Architektur

### **Phase 1: Core System** ✅
- **Profil-Management**: PDF → Text → Strukturierte Daten
- **Supabase Integration**: Vector Database für Semantic Search
- **Web-Interface**: Upload, Verarbeitung, Download

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
├── 01_Core_System/           # Phase 1: Core System
├── 02_Availability_System/  # Phase 2: Verfügbarkeits-Management
├── 03_Candidate_Search/     # Phase 3: Kandidaten-Suche
├── 04_Project_Matching/     # Phase 4: Projekt-Matching
├── 05_Shared_Components/    # Gemeinsame Komponenten
├── 06_Testing/             # Test-Suite
├── 07_Documentation/       # Dokumentation
└── 08_Output_Files/        # Output & Logs
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

## 📋 Nächste Schritte

1. **Phase 1**: Core System testen und erweitern
2. **Phase 2**: Verfügbarkeits-Management implementieren
3. **Phase 3**: Kandidaten-Suche entwickeln
4. **Phase 4**: Projekt-Matching aufbauen

## 🎯 Ziel

Ein vollständiges, automatisiertes Expert-Management-System für NUNC Consulting GmbH.

