# 09_Testing

Dieser Ordner enthält alle Test-Dateien und Test-Skripte für das NUNC Expert Management System.

## Struktur

- `file_upload_test.py` - Einfacher Datei-Upload Test mit Flask
- `unit_tests/` - Unit Tests für einzelne Module
- `integration_tests/` - Integration Tests für das gesamte System
- `test_data/` - Test-Daten und Beispieldateien

## Verwendung

### Datei-Upload Test
```bash
cd 09_Testing
python file_upload_test.py
```

Öffnen Sie dann http://127.0.0.1:5000 in Ihrem Browser.

### Unit Tests ausführen
```bash
cd 09_Testing/unit_tests
python -m pytest
```

### Integration Tests ausführen
```bash
cd 09_Testing/integration_tests
python -m pytest
```
