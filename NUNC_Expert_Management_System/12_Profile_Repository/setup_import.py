#!/usr/bin/env python3
"""
NUNC Expert Management System - Profile Import Setup
Setup und Import von bestehenden Word/PDF Profilen
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def setup_profile_import():
    """Setup für Profile Import"""
    print("NUNC Expert Management System - Profile Import Setup")
    print("=" * 60)
    
    # Prüfe Dependencies
    print("Checking dependencies...")
    
    missing_deps = []
    
    try:
        from docx import Document
        print("python-docx available")
    except ImportError:
        missing_deps.append("python-docx")
        print("python-docx missing")
    
    try:
        import PyPDF2
        import pdfplumber
        print("PDF libraries available")
    except ImportError:
        missing_deps.append("PyPDF2 pdfplumber")
        print("PDF libraries missing")
    
    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install python-docx PyPDF2 pdfplumber")
        return False
    
    # Prüfe Supabase-Verbindung
    print("\nChecking Supabase connection...")
    try:
        from import_manager import ImportManager
        import_manager = ImportManager()
        
        ready, issues = import_manager.validate_import_readiness()
        
        if ready:
            print("Supabase connection ready")
        else:
            print("Supabase connection issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
            
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        return False
    
    # Erstelle Verzeichnis-Struktur
    print("\nSetting up directory structure...")
    
    base_dir = Path("NUNC_Expert_Management_System/12_Profile_Repository")
    
    directories = [
        "Active_Profiles",
        "Archived_Profiles", 
        "Import_Queue",
        "Templates"
    ]
    
    for dir_name in directories:
        dir_path = base_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETED!")
    print("=" * 60)
    print("\nNEXT STEPS:")
    print("1. Copy your 40+ Word profiles to:")
    print("   NUNC_Expert_Management_System/12_Profile_Repository/Import_Queue/")
    print("\n2. Run the import:")
    print("   python import_profiles.py")
    print("\n3. Check imported profiles in Supabase Dashboard")
    
    return True

def import_profiles():
    """Importiert Profile aus Import_Queue"""
    print("NUNC Expert Management System - Profile Import")
    print("=" * 60)
    
    try:
        from import_manager import ImportManager
        
        import_manager = ImportManager()
        
        # Prüfe Import-Bereitschaft
        ready, issues = import_manager.validate_import_readiness()
        
        if not ready:
            print("❌ Import system not ready:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        # Importiere aus Import_Queue
        import_queue = "NUNC_Expert_Management_System/12_Profile_Repository/Import_Queue"
        
        if not Path(import_queue).exists():
            print(f"❌ Import queue directory not found: {import_queue}")
            return False
        
        # Zähle Dateien
        word_files = list(Path(import_queue).glob("*.docx"))
        pdf_files = list(Path(import_queue).glob("*.pdf"))
        
        total_files = len(word_files) + len(pdf_files)
        
        if total_files == 0:
            print("❌ No Word/PDF files found in Import_Queue")
            print("Please copy your profile files to the Import_Queue directory")
            return False
        
        print(f"Found {len(word_files)} Word files and {len(pdf_files)} PDF files")
        print(f"Total: {total_files} files to import")
        
        # Automatischer Import (ohne Bestätigung)
        print(f"\nStarting automatic import of {total_files} profiles...")
        
        # Starte Import
        print("\nStarting import...")
        stats = import_manager.import_directory(import_queue, move_after_import=True)
        
        # Zeige Ergebnisse
        print("\n" + "=" * 60)
        print("IMPORT RESULTS")
        print("=" * 60)
        print(f"Total files: {stats['total_files']}")
        print(f"Successful imports: {stats['successful_imports']}")
        print(f"Failed imports: {stats['failed_imports']}")
        print(f"Skipped imports: {stats['skipped_imports']}")
        print(f"Success rate: {stats['successful_imports']/max(stats['total_files'], 1)*100:.1f}%")
        
        if stats['errors']:
            print(f"\nErrors ({len(stats['errors'])}):")
            for error in stats['errors'][:5]:  # Zeige nur erste 5 Fehler
                print(f"  - {error}")
            if len(stats['errors']) > 5:
                print(f"  ... and {len(stats['errors'])-5} more errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        # Import-Modus
        success = import_profiles()
        if success:
            print("\nImport completed successfully!")
        else:
            print("\nImport failed!")
    else:
        # Setup-Modus
        success = setup_profile_import()
        if success:
            print("\nSetup completed successfully!")
        else:
            print("\nSetup failed!")
