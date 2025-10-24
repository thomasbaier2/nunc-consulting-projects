#!/usr/bin/env python3
"""
NUNC Expert Management System - Simple Web Interface
"""

from flask import Flask, request, jsonify, render_template, send_file
from pathlib import Path
import os
import sys
import time
import webbrowser
import threading
from datetime import datetime

# Importiere alle System-Komponenten
sys.path.append(str(Path(__file__).parent / 'NUNC_Expert_Management_System' / '01_Core_System'))
from profile_manager import ProfileManager

sys.path.append(str(Path(__file__).parent / 'NUNC_Expert_Management_System' / '02_Availability_System'))
from availability_manager import AvailabilityManager

sys.path.append(str(Path(__file__).parent / 'NUNC_Expert_Management_System' / '03_Candidate_Search'))
from candidate_search import CandidateSearch

sys.path.append(str(Path(__file__).parent / 'NUNC_Expert_Management_System' / '04_Project_Matching'))
from project_matcher import ProjectMatcher

# CV-Processing Komponenten
sys.path.append(str(Path(__file__).parent / 'NUNC_Expert_Management_System' / '06_CV_Processing'))
from cv_processor import CvProcessor
from word_generator import NuncWordGenerator
from supabase_integration import SupabaseIntegration

app = Flask(__name__)

# Globale System-Komponenten
profile_manager = ProfileManager()
availability_manager = AvailabilityManager()
candidate_search = CandidateSearch()
project_matcher = ProjectMatcher()

# CV-Processing Komponenten
cv_processor = CvProcessor()
word_generator = NuncWordGenerator()
supabase_integration = SupabaseIntegration()

# Ordner für Uploads und Outputs
UPLOAD_FOLDER = Path(__file__).parent / 'NUNC_Expert_Management_System' / '08_Output_Files' / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent / 'NUNC_Expert_Management_System' / '08_Output_Files' / 'generated_profiles'
WORD_OUTPUT_FOLDER = Path(__file__).parent / 'NUNC_Expert_Management_System' / '08_Output_Files' / 'word_documents'
HTML_OUTPUT_FOLDER = Path(__file__).parent / 'NUNC_Expert_Management_System' / '08_Output_Files' / 'html_templates'

# Erstelle Ordner falls nicht vorhanden
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, WORD_OUTPUT_FOLDER, HTML_OUTPUT_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Hauptseite mit System-Ubersicht"""
    return render_template('index.html')

@app.route('/cv-processing')
def cv_processing_page():
    """Seite fur CV-Verarbeitung"""
    return render_template('cv_processing.html')

# CV-Processing API-Endpunkte
@app.route('/api/cv/upload', methods=['POST'])
def upload_cv():
    """Ladt CV-PDF hoch und verarbeitet es"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Keine Datei ausgewahlt'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Keine Datei ausgewahlt'})
        
        if file and file.filename.lower().endswith('.pdf'):
            # Datei speichern
            filename = f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)
            
            # CV verarbeiten
            processed_data = cv_processor.process_pdf(str(file_path))
            
            if 'error' in processed_data:
                return jsonify({'success': False, 'error': processed_data['error']})
            
            # Profil im System erstellen
            profile_id = profile_manager.create_profile(processed_data)
            
            # In Supabase speichern
            supabase_id = supabase_integration.insert_profile(processed_data)
            
            return jsonify({
                'success': True, 
                'profile_id': profile_id,
                'supabase_id': supabase_id,
                'processed_data': processed_data
            })
        else:
            return jsonify({'success': False, 'error': 'Nur PDF-Dateien sind erlaubt'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/cv/generate-word', methods=['POST'])
def generate_word_document():
    """Generiert Word-Dokument aus Profil"""
    try:
        profile_data = request.json
        
        # Word-Dokument generieren
        word_file = word_generator.generate_word_document(profile_data)
        
        if word_file:
            return jsonify({
                'success': True, 
                'word_file': word_file,
                'download_url': f'/api/cv/download/{Path(word_file).name}'
            })
        else:
            return jsonify({'success': False, 'error': 'Fehler beim Generieren des Word-Dokuments'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/cv/download/<filename>')
def download_word_document(filename):
    """Ladt Word-Dokument herunter"""
    try:
        file_path = WORD_OUTPUT_FOLDER / filename
        if file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'Datei nicht gefunden'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def create_templates():
    """Erstellt HTML-Templates fur das Web-Interface"""
    templates_dir = Path(__file__).parent / 'NUNC_Expert_Management_System' / '05_Shared_Components' / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    # Index Template
    index_html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUNC Expert Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #ffffff;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: #ffffff;
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
        .nav {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .nav-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s ease;
            color: #1a1a2e;
        }
        .nav-card:hover {
            transform: translateY(-5px);
        }
        .nav-card h2 {
            color: #0f3460;
            margin-bottom: 15px;
        }
        .nav-card p {
            margin-bottom: 20px;
            color: #666;
        }
        .nav-card a {
            display: inline-block;
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            color: white;
            padding: 12px 25px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .nav-card a:hover {
            background: linear-gradient(135deg, #1a1a2e, #0f3460);
            transform: translateY(-2px);
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #cccccc;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="nunc-logo">NUNC Consulting GmbH</div>
            <h1>Expert Management System</h1>
            <p>Vollstandiges Expert-Management fur NUNC Consulting</p>
        </div>
        
        <div class="nav">
            <div class="nav-card">
                <h2>Profil-Management</h2>
                <p>Verwalten Sie Experten-Profile, erstellen Sie neue Profile und aktualisieren Sie bestehende.</p>
                <a href="/profiles">Profile verwalten</a>
            </div>
            
            <div class="nav-card">
                <h2>Verfugbarkeits-Management</h2>
                <p>Verfugbarkeits-Anfragen senden, Antworten verwalten und Verfugbarkeit tracken.</p>
                <a href="/availability">Verfugbarkeit verwalten</a>
            </div>
            
            <div class="nav-card">
                <h2>Kandidaten-Suche</h2>
                <p>Automatisierte Suche auf LinkedIn und Freelancermap mit AI-basiertem Matching.</p>
                <a href="/candidates">Kandidaten suchen</a>
            </div>
            
            <div class="nav-card">
                <h2>Projekt-Matching</h2>
                <p>Projekte mit passenden Experten matchen und optimale Besetzungen finden.</p>
                <a href="/projects">Projekte verwalten</a>
            </div>
            
            <div class="nav-card">
                <h2>CV-Verarbeitung</h2>
                <p>PDF-CVs hochladen, automatisch verarbeiten und in NUNC-Profile konvertieren.</p>
                <a href="/cv-processing">CV verarbeiten</a>
            </div>
        </div>
    </div>
    
    <div class="footer">
        &copy; 2025 NUNC Consulting GmbH. All rights reserved.
    </div>
</body>
</html>
    """
    
    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # CV-Processing Template
    cv_processing_html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV-Verarbeitung - NUNC Expert Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #ffffff;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: #ffffff;
            margin-bottom: 40px;
            border-bottom: 3px solid #0f3460;
            padding-bottom: 20px;
        }
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #0f3460, #1a1a2e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .upload-section {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            color: #1a1a2e;
        }
        .upload-area {
            border: 3px dashed #0f3460;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            background: rgba(15, 52, 96, 0.1);
        }
        .upload-area.dragover {
            background: rgba(15, 52, 96, 0.2);
            border-color: #1a1a2e;
        }
        .file-input {
            display: none;
        }
        .upload-btn {
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .upload-btn:hover {
            background: linear-gradient(135deg, #1a1a2e, #0f3460);
            transform: translateY(-2px);
        }
        .results-section {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            color: #1a1a2e;
            display: none;
        }
        .profile-data {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .profile-field {
            margin: 10px 0;
        }
        .profile-field strong {
            color: #0f3460;
        }
        .download-btn {
            background: linear-gradient(135deg, #17a2b8, #138496);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        .download-btn:hover {
            background: linear-gradient(135deg, #138496, #17a2b8);
            transform: translateY(-2px);
        }
        .back-btn {
            background: linear-gradient(135deg, #6c757d, #495057);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            margin: 20px 0;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            background: linear-gradient(135deg, #495057, #6c757d);
            transform: translateY(-2px);
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0f3460;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CV-Verarbeitung</h1>
            <p>Laden Sie PDF-CVs hoch und konvertieren Sie sie automatisch in NUNC-Profile</p>
        </div>
        
        <div class="upload-section">
            <h2>PDF-CV hochladen</h2>
            <div class="upload-area" id="uploadArea">
                <p>Ziehen Sie eine PDF-Datei hierher oder klicken Sie zum Auswahlen</p>
                <input type="file" id="fileInput" class="file-input" accept=".pdf">
                <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                    Datei auswahlen
                </button>
            </div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>CV wird verarbeitet...</p>
            </div>
        </div>
        
        <div class="results-section" id="resultsSection">
            <h2>Verarbeitetes Profil</h2>
            <div id="profileData"></div>
            <div>
                <button class="download-btn" id="downloadWordBtn" onclick="downloadWord()">
                    Word-Dokument herunterladen
                </button>
                <button class="download-btn" id="saveProfileBtn" onclick="saveProfile()">
                    Profil speichern
                </button>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="back-btn" onclick="window.location.href='/'">
                Zuruck zur Hauptseite
            </button>
        </div>
    </div>
    
    <script>
        let currentProfileData = null;
        
        // Drag & Drop Funktionalitat
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        
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
            if (file.type !== 'application/pdf') {
                alert('Bitte wahlen Sie eine PDF-Datei aus.');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            // Loading anzeigen
            document.getElementById('loading').style.display = 'block';
            document.getElementById('resultsSection').style.display = 'none';
            
            fetch('/api/cv/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                
                if (data.success) {
                    currentProfileData = data.processed_data;
                    displayProfile(data.processed_data);
                } else {
                    alert('Fehler: ' + data.error);
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                alert('Fehler beim Hochladen: ' + error);
            });
        }
        
        function displayProfile(profileData) {
            const profileHtml = `
                <div class="profile-data">
                    <div class="profile-field"><strong>Name:</strong> ${profileData.expert_name || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Hauptfokus:</strong> ${profileData.hauptfokus || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Sprachen:</strong> ${profileData.sprachen || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Zur Person:</strong> ${profileData.zur_person || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Technologien:</strong> ${profileData.technologien || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Besondere Kenntnisse:</strong> ${profileData.besondere_kenntnisse || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Branchenkenntnisse:</strong> ${profileData.branchenkenntnisse || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Methoden:</strong> ${profileData.methoden || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Zertifizierungen:</strong> ${profileData.zertifizierungen || 'Nicht verfugbar'}</div>
                    <div class="profile-field"><strong>Projekthistorie:</strong> ${profileData.projekthistorie_text || 'Nicht verfugbar'}</div>
                </div>
            `;
            
            document.getElementById('profileData').innerHTML = profileHtml;
            document.getElementById('resultsSection').style.display = 'block';
        }
        
        function downloadWord() {
            if (!currentProfileData) {
                alert('Kein Profil verfugbar');
                return;
            }
            
            fetch('/api/cv/generate-word', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(currentProfileData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.open(data.download_url, '_blank');
                } else {
                    alert('Fehler beim Generieren des Word-Dokuments: ' + data.error);
                }
            })
            .catch(error => {
                alert('Fehler: ' + error);
            });
        }
        
        function saveProfile() {
            if (!currentProfileData) {
                alert('Kein Profil verfugbar');
                return;
            }
            
            fetch('/api/profiles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(currentProfileData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Profil erfolgreich gespeichert!');
                } else {
                    alert('Fehler beim Speichern: ' + data.error);
                }
            })
            .catch(error => {
                alert('Fehler: ' + error);
            });
        }
    </script>
</body>
</html>
    """
    
    with open(templates_dir / 'cv_processing.html', 'w', encoding='utf-8') as f:
        f.write(cv_processing_html)
    
    print("Templates created")

def start_web_interface():
    """Startet das vollstandige Web-Interface"""
    print("Starting NUNC Expert Management System...")
    
    # Templates erstellen
    create_templates()
    
    # Browser öffnen
    def open_browser():
        time.sleep(2)
        port = os.environ.get('FLASK_PORT', '9000')
        host = os.environ.get('FLASK_HOST', '127.0.0.1')
        try:
            webbrowser.open(f'http://{host}:{port}')
            print("Browser opened")
        except Exception as e:
            print(f"Error opening browser: {e}")
            print(f"Please open manually: http://{host}:{port}")
    
    threading.Thread(target=open_browser).start()
    
    # Flask App starten
    port = int(os.environ.get('FLASK_PORT', 9000))
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)

if __name__ == "__main__":
    start_web_interface()

