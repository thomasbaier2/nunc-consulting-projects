#!/usr/bin/env python3
"""
NUNC CV Converter - Web Interface
Vollständige Web-Oberfläche für CV-Verarbeitung
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
import base64
from datetime import datetime
import webbrowser
import threading
import time
import sys

# Import unserer Komponenten
sys.path.append('../01_Core_Components')
sys.path.append('../03_Word_Generation')
sys.path.append('../04_Supabase_Integration')

from cv_processor import CvProcessor
from word_generator import NuncWordGenerator
from supabase_integration import SupabaseIntegration

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Globale Variablen
cv_processor = CvProcessor()
word_generator = NuncWordGenerator()
supabase_integration = SupabaseIntegration()

UPLOAD_FOLDER = Path(__file__).parent.parent / '07_Output_Files' / 'test_results' / 'input'
OUTPUT_FOLDER = Path(__file__).parent.parent / '07_Output_Files' / 'generated_profiles'

@app.route('/')
def index():
    """Hauptseite mit Upload-Interface"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """CV-PDF Upload und Verarbeitung"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            # Datei speichern
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            filepath = UPLOAD_FOLDER / filename
            UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
            file.save(str(filepath))
            
            # CV verarbeiten
            result = cv_processor.process_pdf(str(filepath))
            
            if 'error' in result:
                return jsonify({'error': result['error']}), 500
            
            # Word-Dokument generieren
            word_file = word_generator.generate_word_document(result)
            word_filename = Path(word_file).name if word_file else None
            
            # HTML-Output generieren
            html_output = generate_html_output(result)
            
            # HTML speichern
            html_filename = f"NUNC_Profile_{result['expert_name'].replace(' ', '_')}.html"
            html_path = OUTPUT_FOLDER / html_filename
            OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
            
            # In Supabase speichern
            profile_id = supabase_integration.insert_profile(result)
            
            return jsonify({
                'success': True,
                'expert_name': result['expert_name'],
                'hauptfokus': result['hauptfokus'],
                'projekte': len(result['projekthistorie']),
                'html_file': html_filename,
                'word_file': word_filename,
                'profile_id': profile_id,
                'download_urls': {
                    'html': f'/download/{html_filename}',
                    'word': f'/download/{word_filename}' if word_filename else None
                }
            })
        
        return jsonify({'error': 'Nur PDF-Dateien sind erlaubt'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Fehler bei der Verarbeitung: {str(e)}'}), 500

def generate_html_output(profile_data: dict) -> str:
    """Generiert HTML-Output für das Profil"""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NUNC Profile - {profile_data.get('expert_name', 'Unbekannt')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; border-bottom: 3px solid #0f3460; padding-bottom: 20px; margin-bottom: 30px; }}
            .section {{ margin-bottom: 25px; }}
            .section h2 {{ color: #0f3460; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }}
            .contact {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>NUNC Co.-Expert: {profile_data.get('expert_name', 'Unbekannt')}</h1>
                <h2>Hauptfokus: {profile_data.get('hauptfokus', 'Consultant')}</h2>
            </div>
            
            <div class="section">
                <h2>Profilvorstellung NUNC Consulting GmbH</h2>
                <p>Sprachen: {profile_data.get('sprachen', 'Deutsch/Englisch')}</p>
            </div>
            
            <div class="section">
                <h2>Zur Person</h2>
                <p>{profile_data.get('zur_person', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Besondere Kenntnisse</h2>
                <p>{profile_data.get('besondere_kenntnisse', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Branchenkenntnisse</h2>
                <p>{profile_data.get('branchenkenntnisse', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Methoden</h2>
                <p>{profile_data.get('methoden', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Technologien</h2>
                <p>{profile_data.get('technologien', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Zertifizierungen</h2>
                <p>{profile_data.get('zertifizierungen', 'Keine Informationen verfügbar')}</p>
            </div>
            
            <div class="section">
                <h2>Projekthistorie</h2>
                <ul>
    """
    
    # Projekthistorie hinzufügen
    for project in profile_data.get('projekthistorie', []):
        html_template += f"""
                    <li>
                        <strong>{project.get('projekt_name', 'Unbekanntes Projekt')}</strong> 
                        ({project.get('zeitraum', 'Unbekannter Zeitraum')})<br>
                        <em>Rolle:</em> {project.get('projektrolle', 'Unbekannt')}<br>
                        <em>Aufgaben:</em> {project.get('aufgaben', 'Keine Details verfügbar')}
                    </li>
        """
    
    html_template += """
                </ul>
            </div>
            
            <div class="contact">
                <h3>Kontakt</h3>
                <p><strong>NUNC Consulting GmbH</strong></p>
                <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

@app.route('/download/<filename>')
def download_file(filename):
    """Download der generierten Dateien"""
    try:
        # Prüfe verschiedene Ordner
        possible_paths = [
            OUTPUT_FOLDER / filename,
            Path(__file__).parent.parent / '07_Output_Files' / 'word_documents' / filename,
            Path(__file__).parent.parent / '07_Output_Files' / 'generated_profiles' / filename
        ]
        
        for file_path in possible_paths:
            if file_path.exists():
                print(f"✅ Datei gefunden: {file_path}")
                return send_file(str(file_path), as_attachment=True)
        
        print(f"❌ Datei nicht gefunden: {filename}")
        print(f"Sucht in: {[str(p) for p in possible_paths]}")
        return jsonify({'error': f'Datei nicht gefunden: {filename}'}), 404
    except Exception as e:
        print(f"❌ Download-Fehler: {e}")
        return jsonify({'error': f'Download-Fehler: {str(e)}'}), 500

@app.route('/search')
def search_page():
    """Semantische Suche Seite"""
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
def perform_search():
    """Semantische Suche ausführen"""
    try:
        data = request.json
        query = data.get('query', '')
        limit = data.get('limit', 5)
        
        if not query:
            return jsonify({'error': 'Suchanfrage ist leer'}), 400
        
        # Semantische Suche durchführen
        results = supabase_integration.semantic_search(query, limit)
        
        # Ergebnisse formatieren
        formatted_results = []
        for result in results:
            formatted_results.append({
                'expert_name': result.get('expert_name', 'Unbekannt'),
                'hauptfokus': result.get('hauptfokus', ''),
                'technologien': result.get('technologien', ''),
                'zertifizierungen': result.get('zertifizierungen', ''),
                'similarity_score': result.get('similarity_score', 0),
                'profile_id': result.get('id', ''),
                'created_at': result.get('created_at', '')
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results,
            'total': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({'error': f'Suche Fehler: {str(e)}'}), 500

def create_templates():
    """Erstellt HTML-Templates"""
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Index Template
    index_html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUNC CV Converter</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #ffffff;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        .header { 
            text-align: center; 
            color: #1a1a2e; 
            margin-bottom: 40px; 
            border-bottom: 3px solid #0f3460;
            padding-bottom: 20px;
        }
        .header h1 { 
            font-size: 3em; 
            margin: 0; 
            background: linear-gradient(45deg, #0f3460, #1a1a2e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .nunc-logo {
            font-size: 1.2em;
            color: #0f3460;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .upload-area { 
            border: 3px dashed #0f3460; 
            padding: 60px; 
            text-align: center; 
            border-radius: 20px; 
            margin: 30px 0; 
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        .upload-area:hover { 
            background: linear-gradient(135deg, #e9ecef, #dee2e6); 
            border-color: #1a1a2e; 
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(15, 52, 96, 0.2);
        }
        .btn { 
            background: linear-gradient(45deg, #0f3460, #1a1a2e); 
            color: white; 
            padding: 15px 35px; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            margin: 10px; 
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 6px 20px rgba(15, 52, 96, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(15, 52, 96, 0.5);
        }
        .result { 
            margin-top: 30px; 
            padding: 25px; 
            background: linear-gradient(135deg, #2ecc71, #27ae60); 
            border-radius: 10px; 
            color: white;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="nunc-logo">NUNC CONSULTING GmbH</div>
            <h1>🚀 CV Converter</h1>
            <p style="font-size: 1.2em; color: #0f3460; margin: 10px 0; font-weight: 500;">
                Vollständige CV-Verarbeitung mit Word-Generierung, Supabase Integration und semantischer Suche
            </p>
        </div>
        
        <div class="upload-area" id="uploadArea">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">📤 CV-PDF hochladen</h3>
            <p style="font-size: 1.1em; color: #7f8c8d; margin-bottom: 20px;">
                Ziehen Sie eine PDF-Datei hierher oder klicken Sie zum Auswählen
            </p>
            <input type="file" id="fileInput" accept=".pdf" style="display: none;">
            <button class="btn" onclick="document.getElementById('fileInput').click()">
                📁 Datei auswählen
            </button>
            <p style="font-size: 0.9em; color: #95a5a6; margin-top: 15px;">
                Unterstützte Formate: PDF (max. 16MB)
            </p>
        </div>
        
        <div id="result" class="result">
            <h3 style="margin-top: 0;">✅ Verarbeitung erfolgreich!</h3>
            <div id="resultContent"></div>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const result = document.getElementById('result');
        const resultContent = document.getElementById('resultContent');

        // Drag & Drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });

        function handleFile(file) {
            if (!file.type.includes('pdf')) {
                alert('Bitte wählen Sie eine PDF-Datei aus.');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultContent.innerHTML = `
                        <p><strong>Expert:</strong> ${data.expert_name}</p>
                        <p><strong>Hauptfokus:</strong> ${data.hauptfokus}</p>
                        <p><strong>Projekte:</strong> ${data.projekte}</p>
                        <p><strong>Profile ID:</strong> ${data.profile_id}</p>
                        <p><a href="${data.download_urls.html}" class="btn">📥 HTML Template</a></p>
                        ${data.download_urls.word ? `<p><a href="${data.download_urls.word}" class="btn">📄 Word Dokument</a></p>` : ''}
                    `;
                    result.style.display = 'block';
                } else {
                    alert('Fehler: ' + data.error);
                }
            })
            .catch(error => {
                alert('Fehler bei der Verarbeitung: ' + error);
            });
        }
    </script>
</body>
</html>
    """
    
    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

def start_web_interface():
    """Startet das vollständige Web-Interface"""
    print("🚀 Starte NUNC CV Converter - Vollständige Web-Interface...")
    
    # Templates erstellen
    create_templates()
    
    # Ordner erstellen
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Browser öffnen
    def open_browser():
        time.sleep(1)
        port = os.environ.get('FLASK_PORT', '9000')
        webbrowser.open(f'http://localhost:{port}')
    
    threading.Thread(target=open_browser).start()
    
    # Flask App starten
    port = int(os.environ.get('FLASK_PORT', 9000))
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)

if __name__ == "__main__":
    start_web_interface()
