#!/usr/bin/env python3
"""
NUNC CV Converter - Desktop Version
Umgeht macOS-Berechtigungsprobleme mit Desktop-App
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class NuncDesktopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NUNC CV Converter")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche"""
        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a2e', height=100)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(
            header_frame, 
            text="NUNC CV Converter", 
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#1a1a2e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame, 
            text="PDF → NUNC Template → Word → Supabase → Search", 
            font=('Arial', 12),
            fg='#0f3460',
            bg='#1a1a2e'
        )
        subtitle_label.pack()
        
        # Main Content
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Upload Section
        upload_frame = tk.LabelFrame(
            main_frame, 
            text="📤 CV-PDF hochladen", 
            font=('Arial', 14, 'bold'),
            bg='#f8f9fa'
        )
        upload_frame.pack(fill='x', pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(
            upload_frame, 
            textvariable=self.file_path_var, 
            font=('Arial', 12),
            width=50
        )
        file_entry.pack(side='left', padx=10, pady=10)
        
        browse_btn = tk.Button(
            upload_frame,
            text="📁 Durchsuchen",
            command=self.browse_file,
            font=('Arial', 12, 'bold'),
            bg='#0f3460',
            fg='white',
            padx=20
        )
        browse_btn.pack(side='right', padx=10, pady=10)
        
        # Process Button
        process_btn = tk.Button(
            main_frame,
            text="🚀 CV verarbeiten",
            command=self.process_cv,
            font=('Arial', 16, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15
        )
        process_btn.pack(pady=20)
        
        # Status
        self.status_var = tk.StringVar(value="Bereit für CV-Upload")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 12),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        status_label.pack(pady=10)
        
        # Results
        self.results_text = tk.Text(
            main_frame,
            height=15,
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50'
        )
        self.results_text.pack(fill='both', expand=True, pady=10)
        
    def browse_file(self):
        """Datei auswählen"""
        file_path = filedialog.askopenfilename(
            title="CV-PDF auswählen",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.status_var.set(f"Datei ausgewählt: {os.path.basename(file_path)}")
    
    def process_cv(self):
        """CV verarbeiten"""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine PDF-Datei aus!")
            return
        
        if not file_path.lower().endswith('.pdf'):
            messagebox.showerror("Fehler", "Bitte wählen Sie eine PDF-Datei aus!")
            return
        
        # Status aktualisieren
        self.status_var.set("Verarbeite CV...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🚀 Starte CV-Verarbeitung...\n")
        
        # In separatem Thread verarbeiten
        threading.Thread(target=self._process_cv_thread, args=(file_path,)).start()
    
    def _process_cv_thread(self, file_path):
        """CV-Verarbeitung in separatem Thread"""
        try:
            # CV Processor importieren
            sys.path.append(str(Path(__file__).parent.parent / '01_Core_Components'))
            from cv_processor import CvProcessor
            
            # CV verarbeiten
            processor = CvProcessor()
            result = processor.process_pdf(file_path)
            
            if 'error' in result:
                self.root.after(0, lambda: self._show_error(result['error']))
                return
            
            # Word-Dokument generieren
            sys.path.append(str(Path(__file__).parent.parent / '03_Word_Generation'))
            from word_generator import NuncWordGenerator
            
            word_generator = NuncWordGenerator()
            word_file = word_generator.generate_word_document(result)
            
            # Supabase Integration
            sys.path.append(str(Path(__file__).parent.parent / '04_Supabase_Integration'))
            from supabase_integration import SupabaseIntegration
            
            supabase_integration = SupabaseIntegration()
            profile_id = supabase_integration.insert_profile(result)
            
            # Ergebnisse anzeigen
            self.root.after(0, lambda: self._show_results(result, word_file, profile_id))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Fehler bei der Verarbeitung: {str(e)}"))
    
    def _show_results(self, result, word_file, profile_id):
        """Zeigt Verarbeitungsergebnisse"""
        self.status_var.set("✅ CV erfolgreich verarbeitet!")
        
        results = f"""
✅ CV erfolgreich verarbeitet!

📋 Expert: {result.get('expert_name', 'Unbekannt')}
🎯 Hauptfokus: {result.get('hauptfokus', 'Unbekannt')}
📊 Projekte: {len(result.get('projekthistorie', []))}
🆔 Profile ID: {profile_id}

📄 Word-Dokument: {word_file if word_file else 'Nicht erstellt'}
🗄️ Supabase: {'Gespeichert' if profile_id else 'Nicht gespeichert'}

🔍 Verfügbare Daten:
- Sprachen: {result.get('sprachen', 'N/A')}
- Technologien: {result.get('technologien', 'N/A')}
- Zertifizierungen: {result.get('zertifizierungen', 'N/A')}

🎉 Verarbeitung abgeschlossen!
        """
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
    
    def _show_error(self, error_msg):
        """Zeigt Fehlermeldung"""
        self.status_var.set("❌ Fehler bei der Verarbeitung")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"❌ Fehler: {error_msg}")
        messagebox.showerror("Verarbeitungsfehler", error_msg)
    
    def run(self):
        """Startet die Desktop-App"""
        self.root.mainloop()

def main():
    """Hauptfunktion für Desktop-App"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    NUNC CONSULTING GmbH                     ║
    ║                                                              ║
    ║              🚀 DESKTOP CV CONVERTER 🚀                      ║
    ║                                                              ║
    ║        PDF → NUNC Template → Word → Supabase → Search        ║
    ║                                                              ║
    ║              🔧 macOS Fixed - Desktop App 🔧                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("🚀 Starte NUNC CV Converter Desktop App...")
    
    # Automatische Installation
    print("📦 Installiere Pakete...")
    packages = ['PyPDF2', 'pdfplumber', 'python-docx', 'docxtpl', 'supabase', 'openai', 'sentence-transformers']
    
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package, '--quiet'], check=True, capture_output=True)
            print(f"✅ {package}")
        except:
            print(f"⚠️ {package} - manuell: pip install {package}")
    
    # Verzeichnisse erstellen
    print("📁 Erstelle Verzeichnisse...")
    base_dir = Path(__file__).parent
    for dir_name in ['generated_profiles', 'word_documents', 'html_templates', 'test_results', 'uploads', 'downloads']:
        (base_dir / dir_name).mkdir(exist_ok=True)
        print(f"✅ {dir_name}")
    
    # Desktop-App starten
    print("🖥️ Starte Desktop-App...")
    app = NuncDesktopApp()
    app.run()

if __name__ == "__main__":
    main()

