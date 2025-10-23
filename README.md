# NUNC Consulting - Projekt-Sammlung

Diese Repository enthält die wichtigsten Entwicklungsprojekte von NUNC Consulting GmbH.

## 📁 Projektübersicht

### 1. NUNC CV Converter
**Automatisierte CV-Verarbeitung und Profil-Generierung**

- **Zweck**: Konvertierung von PDF-CVs in strukturierte Profile
- **Features**: 
  - PDF-zu-Text Extraktion
  - KI-basierte Datenanalyse
  - Word-Dokument Generierung
  - Supabase Integration
  - Web-Interface
- **Status**: ✅ Aktiv in Entwicklung

### 2. NUNC Expert Management System (NEMS)
**Expertensuche und Projekt-Matching**

- **Zweck**: Intelligente Zuordnung von Experten zu Projekten
- **Features**:
  - Profil-Management
  - Verfügbarkeits-Tracking
  - Kandidaten-Suche
  - Projekt-Matching Algorithmus
- **Status**: ✅ Aktiv in Entwicklung

### 3. NUNC Salesforce Org
**CRM und Kundenmanagement**

- **Zweck**: Salesforce Custom Objects und Workflows
- **Features**:
  - Custom Objects für NUNC-spezifische Daten
  - Automatisierte Workflows
- **Status**: 🔄 In Planung

## 🚀 Schnellstart

### CV Converter starten
```bash
cd NUNC_CV_Converter/07_Output_Files
python start_system.py
```

### Expert Management System starten
```bash
cd NUNC_Expert_Management_System/08_Output_Files
python start_nems.py
```

## 🛠️ Technologie-Stack

- **Backend**: Python 3.8+
- **Web Framework**: Flask
- **Database**: Supabase (PostgreSQL)
- **AI/ML**: OpenAI API, Custom Models
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript

## 📋 Entwicklung

### Git Workflow
```bash
# Neues Feature erstellen
git checkout -b feature/neue-funktion
git add .
git commit -m "Beschreibung der Änderung"
git push origin feature/neue-funktion
```

### Projektstruktur
```
├── NUNC_CV_Converter/          # CV-Verarbeitung
├── NUNC_Expert_Management_System/  # Expertensuche
├── NUNC_Salesforce_Org/        # Salesforce Integration
└── PROJEKT_ÜBERSICHT.md        # Detaillierte Projektbeschreibung
```

## 📞 Kontakt

**NUNC Consulting GmbH**
- Entwickler: Thomas
- Email: thomas@nunc-consulting.de

## 📄 Lizenz

Proprietäre Software - NUNC Consulting GmbH
Alle Rechte vorbehalten.

---
*Letzte Aktualisierung: $(date)*
