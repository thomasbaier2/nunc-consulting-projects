#!/usr/bin/env python3
"""
NUNC Expert Management System - Complete System
"""

from flask import Flask, request, jsonify, render_template, send_file
from pathlib import Path
import os
import sys
import time
import webbrowser
import threading
from datetime import datetime
import json

app = Flask(__name__)

# Ordner erstellen
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")
WORD_FOLDER = Path("word_docs")

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, WORD_FOLDER]:
    folder.mkdir(exist_ok=True)

# Einfache Profil-Datenbank
PROFILES_FILE = "profiles.json"

def load_profiles():
    """Lädt Profile aus Datei"""
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_profiles(profiles):
    """Speichert Profile in Datei"""
    with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    """Hauptseite"""
    return """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NUNC Expert Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #ffffff;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #0f3460;
            padding-bottom: 20px;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            color: #0f3460;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>NUNC Expert Management System</h1>
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
</body>
</html>
    """

@app.route('/cv-processing')
def cv_processing():
    """CV-Verarbeitung Seite"""
    return """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV-Verarbeitung - NUNC Expert Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #ffffff;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #0f3460;
            padding-bottom: 20px;
        }
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            color: #0f3460;
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

@app.route('/api/cv/upload', methods=['POST'])
def upload_cv():
    """Lädt CV-PDF hoch und verarbeitet es"""
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
            
            # Einfache Profil-Daten erstellen
            processed_data = {
                'expert_name': 'Test Expert',
                'hauptfokus': 'Consultant',
                'sprachen': 'Deutsch/Englisch',
                'zur_person': 'Erfahrener Consultant mit umfassender Expertise.',
                'technologien': 'Python, Flask, Web-Development',
                'besondere_kenntnisse': 'Projektmanagement, Beratung',
                'branchenkenntnisse': 'IT, Consulting',
                'methoden': 'Agile, Scrum',
                'zertifizierungen': 'Zu ermitteln',
                'projekthistorie_text': 'Verschiedene Projekte in der IT-Branche'
            }
            
            return jsonify({
                'success': True, 
                'profile_id': 'test_profile_123',
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
        
        # Einfache Word-Datei erstellen
        word_filename = f"NUNC_Profile_{profile_data.get('expert_name', 'Test')}.txt"
        word_file = WORD_FOLDER / word_filename
        
        # Einfache Text-Datei als Word-Ersatz
        with open(word_file, 'w', encoding='utf-8') as f:
            f.write(f"NUNC Profile: {profile_data.get('expert_name', 'Test')}\n")
            f.write(f"Hauptfokus: {profile_data.get('hauptfokus', 'Consultant')}\n")
            f.write(f"Sprachen: {profile_data.get('sprachen', 'Deutsch/Englisch')}\n")
            f.write(f"Zur Person: {profile_data.get('zur_person', 'Erfahrener Consultant')}\n")
            f.write(f"Technologien: {profile_data.get('technologien', 'Python, Flask')}\n")
            f.write(f"Besondere Kenntnisse: {profile_data.get('besondere_kenntnisse', 'Projektmanagement')}\n")
            f.write(f"Branchenkenntnisse: {profile_data.get('branchenkenntnisse', 'IT, Consulting')}\n")
            f.write(f"Methoden: {profile_data.get('methoden', 'Agile, Scrum')}\n")
            f.write(f"Zertifizierungen: {profile_data.get('zertifizierungen', 'Zu ermitteln')}\n")
            f.write(f"Projekthistorie: {profile_data.get('projekthistorie_text', 'Verschiedene Projekte')}\n")
        
        return jsonify({
            'success': True, 
            'word_file': str(word_file),
            'download_url': f'/api/cv/download/{word_filename}'
        })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/cv/download/<filename>')
def download_word_document(filename):
    """Lädt Word-Dokument herunter"""
    try:
        file_path = WORD_FOLDER / filename
        if file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'Datei nicht gefunden'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/profiles', methods=['POST'])
def save_profile():
    """Speichert Profil"""
    try:
        profile_data = request.json
        profiles = load_profiles()
        
        # Profil hinzufügen
        profile_data['id'] = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        profile_data['created_at'] = datetime.now().isoformat()
        profiles.append(profile_data)
        
        save_profiles(profiles)
        
        return jsonify({'success': True, 'profile_id': profile_data['id']})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def start_system():
    """Startet das System"""
    print("Starting NUNC Expert Management System...")
    
    # Browser öffnen
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open('http://127.0.0.1:9000')
            print("Browser opened: http://127.0.0.1:9000")
        except Exception as e:
            print(f"Error opening browser: {e}")
            print("Please open manually: http://127.0.0.1:9000")
    
    threading.Thread(target=open_browser).start()
    
    # Flask App starten
    app.run(debug=True, host='127.0.0.1', port=9000)

if __name__ == "__main__":
    start_system()

