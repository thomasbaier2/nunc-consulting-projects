#!/usr/bin/env python3
"""
Einfacher Datei-Upload Test
"""

from flask import Flask, request, jsonify
from pathlib import Path
import os

app = Flask(__name__)

# Upload-Ordner
UPLOAD_FOLDER = Path("test_uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Einfache Test-Seite"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Datei-Upload Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .upload-area { border: 2px dashed #ccc; padding: 20px; text-align: center; margin: 20px 0; }
        .upload-area:hover { background: #f9f9f9; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Datei-Upload Test</h1>
    
    <div class="upload-area" id="uploadArea">
        <p>Ziehen Sie eine Datei hierher oder klicken Sie zum Auswählen</p>
        <input type="file" id="fileInput" style="display: none;" accept=".pdf,.txt,.docx">
        <button onclick="document.getElementById('fileInput').click()">Datei auswählen</button>
    </div>
    
    <div id="result" class="result" style="display: none;"></div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const result = document.getElementById('result');
        
        // Drag & Drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.background = '#e9ecef';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.background = '';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.background = '';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });
        
        // File Input
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
        
        function handleFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            result.style.display = 'block';
            result.innerHTML = 'Datei wird hochgeladen...';
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    result.innerHTML = `✅ Erfolgreich hochgeladen!<br>
                                      Datei: ${data.filename}<br>
                                      Größe: ${data.size} bytes<br>
                                      Typ: ${data.type}`;
                } else {
                    result.innerHTML = `❌ Fehler: ${data.error}`;
                }
            })
            .catch(error => {
                result.innerHTML = `❌ Fehler: ${error}`;
            });
        }
    </script>
</body>
</html>
    """

@app.route('/upload', methods=['POST'])
def upload_file():
    """Datei-Upload Handler"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Keine Datei gefunden'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Keine Datei ausgewählt'})
        
        # Datei speichern
        filename = file.filename
        file_path = UPLOAD_FOLDER / filename
        file.save(file_path)
        
        # Datei-Info
        file_size = file_path.stat().st_size
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': file_size,
            'type': file.content_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Starting File Upload Test...")
    print("Open: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
