# NUNC CV Converter - Vollständige Dokumentation

## 🚀 Übersicht

Der **NUNC CV Converter** ist ein umfassendes System zur automatischen Verarbeitung von Lebenslauf-PDFs in strukturierte NUNC-Profile mit Word-Dokument-Generierung, Supabase-Integration und semantischer Suche.

## 📁 Projektstruktur

```
NUNC_CV_Converter/
├── 01_Core_Components/          # Kern-Komponenten
│   └── cv_processor.py         # CV-Verarbeitung und Datenextraktion
├── 02_Web_Interface/           # Web-Oberfläche
│   └── web_interface.py       # Flask Web-Interface
├── 03_Word_Generation/        # Word-Dokument-Generierung
│   └── word_generator.py      # .docx Dokument-Erstellung
├── 04_Supabase_Integration/   # Supabase VDB Integration
│   └── supabase_integration.py # Semantische Suche und VDB
├── 05_Testing/                # Test-Suite
│   └── test_suite.py          # Umfassende Tests
├── 06_Documentation/          # Dokumentation
│   └── README.md              # Diese Datei
└── 07_Output_Files/           # Ausgabe-Dateien
    ├── generated_profiles/    # Generierte Profile
    ├── word_documents/        # Word-Dokumente
    ├── html_templates/        # HTML-Templates
    └── test_results/          # Test-Ergebnisse
```

## 🛠️ Installation

### Voraussetzungen
- Python 3.9+
- pip3

### Abhängigkeiten installieren
```bash
pip3 install PyPDF2 pdfplumber python-docx docxtpl supabase openai sentence-transformers flask
```

## 🚀 Schnellstart

### 1. Web-Interface starten
```bash
cd 02_Web_Interface
python web_interface.py
```
Öffnet automatisch http://localhost:5000

### 2. Test-Suite ausführen
```bash
cd 05_Testing
python test_suite.py
```

### 3. Word-Dokumente generieren
```bash
cd 03_Word_Generation
python word_generator.py
```

## 📋 Features

### ✅ Implementierte Features

1. **PDF-CV Verarbeitung**
   - Automatische Text-Extraktion
   - Strukturierte Datenextraktion
   - NUNC-Format Konvertierung

2. **Word-Dokument-Generierung**
   - Echte .docx Dateien
   - NUNC-Template mit Platzhaltern
   - Professionelle Formatierung

3. **Supabase VDB Integration**
   - Lokale Fallback-Datenbank
   - Embedding-Generierung
   - Semantische Suche

4. **Web-Interface**
   - Drag & Drop Upload
   - Real-time Verarbeitung
   - Download-Management

5. **Semantische Suche**
   - Cosinus-Ähnlichkeit
   - Lokale und Cloud-Embeddings
   - Intelligente Ergebnis-Ranking

## 🔧 Konfiguration

### Umgebungsvariablen (optional)
```bash
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
export OPENAI_API_KEY="your_openai_key"
```

### Lokale Konfiguration
Das System funktioniert vollständig lokal ohne externe APIs.

## 📊 Verwendung

### Web-Interface
1. **CV Upload**: PDF-Datei hochladen
2. **Automatische Verarbeitung**: System extrahiert Daten
3. **Word-Generierung**: .docx Dokument erstellen
4. **Supabase Integration**: Profil speichern
5. **Download**: Dateien herunterladen

### Programmierung
```python
from cv_processor import CvProcessor
from word_generator import NuncWordGenerator
from supabase_integration import SupabaseIntegration

# CV verarbeiten
processor = CvProcessor()
result = processor.process_pdf("cv.pdf")

# Word-Dokument generieren
word_gen = NuncWordGenerator()
word_file = word_gen.generate_word_document(result)

# In Supabase speichern
supabase = SupabaseIntegration()
profile_id = supabase.insert_profile(result)
```

## 🧪 Testing

### Test-Suite ausführen
```bash
cd 05_Testing
python test_suite.py
```

### Einzelne Tests
```bash
# CV Processor
python ../01_Core_Components/cv_processor.py

# Word Generator
python ../03_Word_Generation/word_generator.py

# Supabase Integration
python ../04_Supabase_Integration/supabase_integration.py
```

## 📈 Performance

- **PDF-Verarbeitung**: ~2-5 Sekunden pro CV
- **Word-Generierung**: ~1-2 Sekunden
- **Supabase-Integration**: ~1-3 Sekunden
- **Semantische Suche**: ~0.5-1 Sekunde

## 🔒 Sicherheit

- Lokale Verarbeitung (keine Cloud-Uploads)
- Sichere Datei-Handling
- Input-Validierung
- Error-Handling

## 🐛 Troubleshooting

### Häufige Probleme

1. **ModuleNotFoundError**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **PDF-Verarbeitung fehlgeschlagen**
   - Überprüfen Sie PDF-Format
   - Stellen Sie sicher, dass PDF nicht passwort-geschützt ist

3. **Word-Generierung fehlgeschlagen**
   - Überprüfen Sie Template-Pfad
   - Stellen Sie sicher, dass Ausgabe-Ordner existiert

4. **Supabase-Verbindung fehlgeschlagen**
   - System verwendet automatisch lokale Fallback-Datenbank
   - Überprüfen Sie Umgebungsvariablen

## 📞 Support

Bei Problemen oder Fragen:
1. Überprüfen Sie die Test-Suite
2. Schauen Sie in die Logs
3. Überprüfen Sie die Dokumentation

## 🚀 Nächste Schritte

### Geplante Features
- [ ] n8n Cloud Integration
- [ ] Erweiterte AI-Extraktion
- [ ] Batch-Verarbeitung
- [ ] API-Endpoints
- [ ] Docker-Container

### Erweiterungen
- [ ] Mehrsprachige Unterstützung
- [ ] Custom Templates
- [ ] Advanced Analytics
- [ ] Export-Formate

---

**NUNC Consulting GmbH** - Powered by AI 🤖

