# NUNC Expert Management System - Profile Repository

## 📁 Übersicht

Das Profile Repository verwaltet Word/PDF Profile und synchronisiert sie mit der Supabase-Datenbank.

## 🏗️ Verzeichnis-Struktur

```
📁 12_Profile_Repository/
├── 📁 Active_Profiles/          ← Importierte Profile (aktiv)
├── 📁 Archived_Profiles/        ← Archivierte Profile
├── 📁 Import_Queue/             ← Neue Profile zum Import
├── 📁 Templates/                 ← Word/PDF Templates
├── 📄 profile_parser.py         ← Word/PDF Parser
├── 📄 import_manager.py         ← Import Manager
├── 📄 setup_import.py           ← Setup & Import Script
└── 📄 README.md                 ← Diese Datei
```

## 🚀 Setup

### 1. Dependencies installieren

```bash
pip install python-docx PyPDF2 pdfplumber
```

### 2. Setup ausführen

```bash
python setup_import.py
```

### 3. Profile kopieren

Kopiere deine 40+ Word Profile in:
```
NUNC_Expert_Management_System/12_Profile_Repository/Import_Queue/
```

### 4. Import starten

```bash
python setup_import.py import
```

## 📋 Features

### ✅ Word/PDF Parser
- **Automatische Textextraktion** aus Word (.docx) und PDF Dateien
- **Intelligente Datenextraktion:**
  - Namen, E-Mail, Telefon
  - Technische Skills (Python, React, AWS, etc.)
  - Soft Skills (Teamwork, Leadership, etc.)
  - Zertifizierungen
  - Sprachen
  - Berufserfahrung
  - Firmen-Erfahrung (für Cross-connections)

### ✅ Import Manager
- **Batch-Import** von mehreren Profilen
- **Duplikat-Prüfung** (basierend auf E-Mail)
- **Automatische Datei-Verschiebung** nach Import
- **Detaillierte Import-Statistiken**
- **Fehlerbehandlung** und Logging

### ✅ Supabase Integration
- **Automatische Konvertierung** zu BoutiqueProfileManager-Format
- **Trust-Level System** (neue Profile = Level 1)
- **AI-Scores** basierend auf Parsing-Confidence
- **Cross-connections** für Firmen-Erfahrung

## 🔧 Verwendung

### Einzelne Profile importieren

```python
from import_manager import ImportManager

import_manager = ImportManager()
stats = import_manager.import_directory("path/to/profiles")
print(f"Imported {stats['successful_imports']} profiles")
```

### Profile parsen (ohne Import)

```python
from profile_parser import ProfileParser

parser = ProfileParser()
profile = parser.parse_file("path/to/profile.docx")
print(f"Name: {profile.first_name} {profile.last_name}")
print(f"Skills: {profile.technical_skills}")
```

## 📊 Import-Statistiken

Nach dem Import erhältst du:
- **Gesamtanzahl** verarbeiteter Dateien
- **Erfolgreiche Imports**
- **Fehlgeschlagene Imports**
- **Übersprungene Imports** (Duplikate)
- **Erfolgsrate** in Prozent
- **Detaillierte Fehlermeldungen**

## 🎯 Workflow

### 1. Neue Profile hinzufügen
1. Kopiere Word/PDF Profile in `Import_Queue/`
2. Führe Import aus: `python setup_import.py import`
3. Profile werden automatisch nach `Active_Profiles/` verschoben

### 2. Profile bearbeiten
1. Bearbeite Profile in `Active_Profiles/`
2. Änderungen werden beim nächsten Import erkannt
3. Supabase wird automatisch aktualisiert

### 3. Profile archivieren
1. Verschiebe Profile nach `Archived_Profiles/`
2. Profile werden in Supabase als "archived" markiert

## 🔍 Parsing-Confidence

Der Parser berechnet eine Confidence-Score (0.0-1.0) basierend auf:
- **Grunddaten** (40%): Name, E-Mail, Telefon
- **Skills** (30%): Technische und Soft Skills
- **Erfahrung** (30%): Berufserfahrung, Firmen-Erfahrung

## 🚨 Fehlerbehandlung

### Häufige Probleme

**1. "python-docx not installed"**
```bash
pip install python-docx
```

**2. "PDF libraries not installed"**
```bash
pip install PyPDF2 pdfplumber
```

**3. "Supabase connection failed"**
- Prüfe `.env` Datei
- Stelle sicher, dass Supabase Schema erstellt wurde

**4. "Profile limit reached"**
- Archiviere alte Profile
- Oder erhöhe Limit in BoutiqueProfileManager

## 📈 Performance

- **Word-Dateien:** ~2-5 Sekunden pro Datei
- **PDF-Dateien:** ~3-8 Sekunden pro Datei
- **Batch-Import:** 40 Profile in ~5-10 Minuten

## 🔄 Synchronisation

Das System synchronisiert automatisch:
- **Word/PDF Änderungen** → Supabase Updates
- **Supabase Änderungen** → Lokale Dateien
- **Version Control** für Profile-Änderungen

## 📞 Support

Bei Problemen:
1. Prüfe die Import-Statistiken
2. Schaue in die Fehler-Logs
3. Validiere die Supabase-Verbindung
4. Teste mit einzelnen Dateien

---

**Ready to import your 40+ Word profiles?** 🚀
