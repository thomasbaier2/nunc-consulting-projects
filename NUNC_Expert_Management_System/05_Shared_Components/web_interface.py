# web_interface.py
"""
NUNC Expert Management System - Web Interface
Vollständiges Web-Interface für alle System-Komponenten
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
sys.path.append(str(Path(__file__).parent.parent / '01_Core_System'))
from profile_manager import ProfileManager

sys.path.append(str(Path(__file__).parent.parent / '02_Availability_System'))
from availability_manager import AvailabilityManager

sys.path.append(str(Path(__file__).parent.parent / '03_Candidate_Search'))
from candidate_search import CandidateSearch

sys.path.append(str(Path(__file__).parent.parent / '04_Project_Matching'))
from project_matcher import ProjectMatcher

app = Flask(__name__)

# Globale System-Komponenten
profile_manager = ProfileManager()
availability_manager = AvailabilityManager()
candidate_search = CandidateSearch()
project_matcher = ProjectMatcher()

# Ordner für Uploads und Outputs
UPLOAD_FOLDER = Path(__file__).parent.parent / '08_Output_Files' / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent.parent / '08_Output_Files' / 'generated_profiles'
WORD_OUTPUT_FOLDER = Path(__file__).parent.parent / '08_Output_Files' / 'word_documents'
HTML_OUTPUT_FOLDER = Path(__file__).parent.parent / '08_Output_Files' / 'html_templates'

# Erstelle Ordner falls nicht vorhanden
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, WORD_OUTPUT_FOLDER, HTML_OUTPUT_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Hauptseite mit System-Übersicht"""
    return render_template('index.html')

@app.route('/profiles')
def profiles_page():
    """Seite für Profil-Management"""
    return render_template('profiles.html')

@app.route('/availability')
def availability_page():
    """Seite für Verfügbarkeits-Management"""
    return render_template('availability.html')

@app.route('/candidates')
def candidates_page():
    """Seite für Kandidaten-Suche"""
    return render_template('candidates.html')

@app.route('/projects')
def projects_page():
    """Seite für Projekt-Matching"""
    return render_template('projects.html')

# API-Endpunkte für Profile
@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Gibt alle Profile zurück"""
    try:
        profiles = profile_manager.get_all_profiles()
        return jsonify({'success': True, 'profiles': profiles})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Erstellt ein neues Profil"""
    try:
        profile_data = request.json
        profile_id = profile_manager.create_profile(profile_data)
        return jsonify({'success': True, 'profile_id': profile_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/profiles/<profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Aktualisiert ein Profil"""
    try:
        update_data = request.json
        success = profile_manager.update_profile(profile_id, update_data)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Löscht ein Profil"""
    try:
        success = profile_manager.delete_profile(profile_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API-Endpunkte für Verfügbarkeit
@app.route('/api/availability/request', methods=['POST'])
def create_availability_request():
    """Erstellt eine Verfügbarkeits-Anfrage"""
    try:
        data = request.json
        expert_emails = data.get('expert_emails', [])
        project_info = data.get('project_info', {})
        
        request_id = availability_manager.create_availability_request(expert_emails, project_info)
        return jsonify({'success': True, 'request_id': request_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/availability/respond/<request_id>')
def respond_availability(request_id):
    """Verarbeitet Verfügbarkeits-Antworten"""
    try:
        status = request.args.get('status', '')
        expert_email = request.args.get('email', '')
        notes = request.args.get('notes', '')
        
        success = availability_manager.process_availability_response(
            request_id, expert_email, status, notes
        )
        
        if success:
            return render_template('availability_response.html', 
                                status=status, 
                                message="Antwort erfolgreich übermittelt!")
        else:
            return render_template('availability_response.html', 
                                status='error', 
                                message="Fehler bei der Übermittlung!")
    except Exception as e:
        return render_template('availability_response.html', 
                            status='error', 
                            message=f"Fehler: {str(e)}")

# API-Endpunkte für Kandidaten-Suche
@app.route('/api/candidates/search', methods=['POST'])
def search_candidates():
    """Sucht Kandidaten auf verschiedenen Plattformen"""
    try:
        search_params = request.json
        results = candidate_search.search_all_platforms(search_params)
        return jsonify({'success': True, 'candidates': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API-Endpunkte für Projekt-Matching
@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Gibt alle Projekte zurück"""
    try:
        projects = project_matcher.get_all_projects()
        return jsonify({'success': True, 'projects': projects})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Erstellt ein neues Projekt"""
    try:
        project_data = request.json
        project_id = project_matcher.create_project(project_data)
        return jsonify({'success': True, 'project_id': project_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<project_id>/match', methods=['POST'])
def match_project(project_id):
    """Matcht Experten zu einem Projekt"""
    try:
        expert_profiles = request.json.get('expert_profiles', [])
        matches = project_matcher.match_experts_to_project(project_id, expert_profiles)
        return jsonify({'success': True, 'matches': matches})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def create_templates():
    """Erstellt HTML-Templates für das Web-Interface"""
    templates_dir = Path(__file__).parent / 'templates'
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
            <p>Vollständiges Expert-Management für NUNC Consulting</p>
        </div>
        
        <div class="nav">
            <div class="nav-card">
                <h2>👥 Profil-Management</h2>
                <p>Verwalten Sie Experten-Profile, erstellen Sie neue Profile und aktualisieren Sie bestehende.</p>
                <a href="/profiles">Profile verwalten</a>
            </div>
            
            <div class="nav-card">
                <h2>📅 Verfügbarkeits-Management</h2>
                <p>Verfügbarkeits-Anfragen senden, Antworten verwalten und Verfügbarkeit tracken.</p>
                <a href="/availability">Verfügbarkeit verwalten</a>
            </div>
            
            <div class="nav-card">
                <h2>🔍 Kandidaten-Suche</h2>
                <p>Automatisierte Suche auf LinkedIn und Freelancermap mit AI-basiertem Matching.</p>
                <a href="/candidates">Kandidaten suchen</a>
            </div>
            
            <div class="nav-card">
                <h2>🎯 Projekt-Matching</h2>
                <p>Projekte mit passenden Experten matchen und optimale Besetzungen finden.</p>
                <a href="/projects">Projekte verwalten</a>
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
    
    # Weitere Templates werden bei Bedarf erstellt
    print("✅ Templates erstellt")

def start_web_interface():
    """Startet das vollständige Web-Interface"""
    print("🚀 Starte NUNC Expert Management System...")
    
    # Templates erstellen
    create_templates()
    
    # Browser öffnen
    def open_browser():
        time.sleep(2)
        port = os.environ.get('FLASK_PORT', '9000')
        host = os.environ.get('FLASK_HOST', '127.0.0.1')
        try:
            webbrowser.open(f'http://{host}:{port}')
            print("✅ Browser geöffnet")
        except Exception as e:
            print(f"❌ Fehler beim Öffnen des Browsers: {e}")
            print(f"Bitte manuell öffnen: http://{host}:{port}")
    
    threading.Thread(target=open_browser).start()
    
    # Flask App starten
    port = int(os.environ.get('FLASK_PORT', 9000))
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)

if __name__ == "__main__":
    start_web_interface()

