# availability_manager.py
"""
NUNC Expert Management System - Verfügbarkeits-Management
Verwaltet Verfügbarkeits-Abfragen und Updates
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

class AvailabilityManager:
    """Verwaltet Verfügbarkeits-Abfragen und Updates"""
    
    def __init__(self, smtp_config: Dict = None):
        self.smtp_config = smtp_config or {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "your-email@gmail.com",
            "password": "your-app-password"
        }
        self.requests_file = Path("08_Output_Files/availability_requests.json")
        self.requests_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Lade bestehende Anfragen
        self.requests = self._load_requests()
    
    def _load_requests(self) -> List[Dict]:
        """Lädt Verfügbarkeits-Anfragen aus lokaler Datei"""
        if self.requests_file.exists():
            with open(self.requests_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_requests(self):
        """Speichert Verfügbarkeits-Anfragen in lokaler Datei"""
        with open(self.requests_file, 'w', encoding='utf-8') as f:
            json.dump(self.requests, f, indent=4, ensure_ascii=False)
    
    def create_availability_request(self, expert_emails: List[str], project_info: Dict) -> str:
        """Erstellt eine Verfügbarkeits-Anfrage"""
        request_id = f"avail_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Anfrage-Struktur
        request = {
            "id": request_id,
            "created_at": datetime.now().isoformat(),
            "status": "sent",  # sent, responded, completed
            "project_info": project_info,
            "expert_emails": expert_emails,
            "responses": [],
            "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
            "reminder_sent": False
        }
        
        # Anfrage speichern
        self.requests.append(request)
        self._save_requests()
        
        # E-Mails senden
        self._send_availability_emails(request)
        
        print(f"✅ Verfügbarkeits-Anfrage erstellt: {request_id}")
        return request_id
    
    def _send_availability_emails(self, request: Dict):
        """Sendet Verfügbarkeits-E-Mails an Experten"""
        for email in request["expert_emails"]:
            try:
                # E-Mail-Inhalt
                subject = f"Verfügbarkeits-Anfrage - {request['project_info']['title']}"
                
                # HTML-E-Mail
                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #0f3460, #1a1a2e); color: white; padding: 20px; text-align: center;">
                        <h1>NUNC Consulting GmbH</h1>
                        <h2>Verfügbarkeits-Anfrage</h2>
                    </div>
                    
                    <div style="padding: 20px; background: #f9f9f9;">
                        <h3>Projekt-Informationen:</h3>
                        <p><strong>Titel:</strong> {request['project_info']['title']}</p>
                        <p><strong>Beschreibung:</strong> {request['project_info']['description']}</p>
                        <p><strong>Startdatum:</strong> {request['project_info']['start_date']}</p>
                        <p><strong>Dauer:</strong> {request['project_info']['duration']}</p>
                        <p><strong>Standort:</strong> {request['project_info']['location']}</p>
                        <p><strong>Remote/Onsite:</strong> {request['project_info']['remote_onsite']}</p>
                    </div>
                    
                    <div style="padding: 20px; text-align: center;">
                        <h3>Verfügbarkeit bestätigen:</h3>
                        <p>Bitte klicken Sie auf einen der folgenden Links:</p>
                        
                        <div style="margin: 20px 0;">
                            <a href="http://localhost:9000/availability/respond/{request['id']}?status=available" 
                               style="background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 10px;">
                                ✅ Verfügbar
                            </a>
                            
                            <a href="http://localhost:9000/availability/respond/{request['id']}?status=busy" 
                               style="background: #ffc107; color: black; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 10px;">
                                ⚠️ Beschäftigt
                            </a>
                            
                            <a href="http://localhost:9000/availability/respond/{request['id']}?status=unavailable" 
                               style="background: #dc3545; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 10px;">
                                ❌ Nicht verfügbar
                            </a>
                        </div>
                        
                        <p><strong>Oder antworten Sie direkt auf diese E-Mail mit:</strong></p>
                        <ul style="text-align: left; display: inline-block;">
                            <li><strong>Verfügbar:</strong> Ja, ich bin verfügbar</li>
                            <li><strong>Beschäftigt:</strong> Nein, ich bin beschäftigt</li>
                            <li><strong>Nicht verfügbar:</strong> Nein, ich bin nicht verfügbar</li>
                        </ul>
                    </div>
                    
                    <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px;">
                        <p>NUNC Consulting GmbH | Verfügbarkeits-Management</p>
                        <p>Anfrage-ID: {request['id']}</p>
                    </div>
                </body>
                </html>
                """
                
                # E-Mail senden
                self._send_email(email, subject, html_content)
                print(f"✅ Verfügbarkeits-E-Mail gesendet an: {email}")
                
            except Exception as e:
                print(f"❌ Fehler beim Senden der E-Mail an {email}: {e}")
    
    def _send_email(self, to_email: str, subject: str, html_content: str):
        """Sendet eine E-Mail"""
        try:
            # E-Mail erstellen
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # HTML-Inhalt hinzufügen
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # E-Mail senden
            server = smtplib.SMTP(self.smtp_config['smtp_server'], self.smtp_config['smtp_port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"❌ E-Mail-Fehler: {e}")
    
    def process_availability_response(self, request_id: str, expert_email: str, status: str, notes: str = "") -> bool:
        """Verarbeitet eine Verfügbarkeits-Antwort"""
        for request in self.requests:
            if request["id"] == request_id:
                # Antwort hinzufügen
                response = {
                    "expert_email": expert_email,
                    "status": status,
                    "notes": notes,
                    "responded_at": datetime.now().isoformat()
                }
                
                request["responses"].append(response)
                request["updated_at"] = datetime.now().isoformat()
                
                # Status aktualisieren
                if len(request["responses"]) == len(request["expert_emails"]):
                    request["status"] = "completed"
                
                # Speichern
                self._save_requests()
                
                print(f"✅ Verfügbarkeits-Antwort verarbeitet: {request_id}")
                return True
        
        print(f"❌ Verfügbarkeits-Anfrage nicht gefunden: {request_id}")
        return False
    
    def get_availability_responses(self, request_id: str) -> List[Dict]:
        """Gibt Verfügbarkeits-Antworten für eine Anfrage zurück"""
        for request in self.requests:
            if request["id"] == request_id:
                return request["responses"]
        return []
    
    def get_pending_requests(self) -> List[Dict]:
        """Gibt ausstehende Verfügbarkeits-Anfragen zurück"""
        return [r for r in self.requests if r["status"] == "sent"]
    
    def send_reminder(self, request_id: str) -> bool:
        """Sendet eine Erinnerung für eine ausstehende Anfrage"""
        for request in self.requests:
            if request["id"] == request_id and not request["reminder_sent"]:
                # Erinnerungs-E-Mail senden
                for email in request["expert_emails"]:
                    subject = f"Erinnerung: Verfügbarkeits-Anfrage - {request['project_info']['title']}"
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background: #ffc107; color: black; padding: 20px; text-align: center;">
                            <h1>⏰ Erinnerung</h1>
                            <h2>Verfügbarkeits-Anfrage</h2>
                        </div>
                        
                        <div style="padding: 20px;">
                            <p>Hallo,</p>
                            <p>wir möchten Sie daran erinnern, dass noch keine Antwort auf unsere Verfügbarkeits-Anfrage vorliegt.</p>
                            
                            <p><strong>Projekt:</strong> {request['project_info']['title']}</p>
                            <p><strong>Deadline:</strong> {request['deadline']}</p>
                            
                            <p>Bitte antworten Sie so schnell wie möglich.</p>
                        </div>
                    </body>
                    </html>
                    """
                    
                    self._send_email(email, subject, html_content)
                
                request["reminder_sent"] = True
                self._save_requests()
                
                print(f"✅ Erinnerung gesendet für: {request_id}")
                return True
        
        return False
    
    def get_availability_summary(self, request_id: str) -> Dict:
        """Gibt eine Zusammenfassung der Verfügbarkeits-Antworten zurück"""
        for request in self.requests:
            if request["id"] == request_id:
                responses = request["responses"]
                total_experts = len(request["expert_emails"])
                responded = len(responses)
                
                # Status-Zusammenfassung
                status_counts = {}
                for response in responses:
                    status = response["status"]
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                return {
                    "request_id": request_id,
                    "total_experts": total_experts,
                    "responded": responded,
                    "pending": total_experts - responded,
                    "status_counts": status_counts,
                    "responses": responses
                }
        
        return {}

if __name__ == "__main__":
    # Test des Availability Managers
    manager = AvailabilityManager()
    
    # Test-Projekt
    project_info = {
        "title": "Salesforce Implementation",
        "description": "Implementierung einer neuen Salesforce-Instanz",
        "start_date": "2025-01-15",
        "duration": "6 Monate",
        "location": "München",
        "remote_onsite": "Hybrid"
    }
    
    # Test-Experten
    expert_emails = ["lukas@example.com", "max@example.com"]
    
    # Verfügbarkeits-Anfrage erstellen
    request_id = manager.create_availability_request(expert_emails, project_info)
    print(f"✅ Test-Anfrage erstellt: {request_id}")
    
    # Verfügbarkeits-Antworten simulieren
    manager.process_availability_response(request_id, "lukas@example.com", "available", "Gerne verfügbar")
    manager.process_availability_response(request_id, "max@example.com", "busy", "Bis März beschäftigt")
    
    # Zusammenfassung anzeigen
    summary = manager.get_availability_summary(request_id)
    print(f"✅ Zusammenfassung: {summary}")

