#!/usr/bin/env python3
"""
NUNC CV Converter - Test Suite
Umfassende Tests für alle Komponenten
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Import unserer Komponenten
sys.path.append('../01_Core_Components')
sys.path.append('../03_Word_Generation')
sys.path.append('../04_Supabase_Integration')

from cv_processor import CvProcessor
from word_generator import NuncWordGenerator
from supabase_integration import SupabaseIntegration

class NuncTestSuite:
    def __init__(self):
        self.test_results = []
        self.cv_processor = CvProcessor()
        self.word_generator = NuncWordGenerator()
        self.supabase_integration = SupabaseIntegration()
        
    def run_all_tests(self):
        """Führt alle Tests aus"""
        print("🚀 NUNC CV Converter - Test Suite")
        print("=" * 50)
        
        # Test 1: CV Processor
        self.test_cv_processor()
        
        # Test 2: Word Generator
        self.test_word_generator()
        
        # Test 3: Supabase Integration
        self.test_supabase_integration()
        
        # Test 4: End-to-End
        self.test_end_to_end()
        
        # Ergebnisse ausgeben
        self.print_test_results()
        
    def test_cv_processor(self):
        """Test der CV-Verarbeitung"""
        print("\n📄 Test 1: CV Processor")
        try:
            # Test mit Mock-Daten
            test_data = {
                'name': 'Test Expert',
                'contact': {'email': 'test@example.com'},
                'experience': [{'title': 'Consultant', 'description': 'Test experience'}],
                'skills': ['Python', 'Salesforce'],
                'languages': ['German', 'English']
            }
            
            # Mock-Verarbeitung
            result = self.cv_processor._convert_to_nunc_format(test_data)
            
            assert result['expert_name'] == 'Test Expert'
            assert 'Consultant' in result['hauptfokus']
            assert 'Python' in result['technologien']
            
            self.test_results.append({
                'test': 'CV Processor',
                'status': 'PASS',
                'message': 'CV-Verarbeitung funktioniert korrekt'
            })
            print("✅ CV Processor Test erfolgreich")
            
        except Exception as e:
            self.test_results.append({
                'test': 'CV Processor',
                'status': 'FAIL',
                'message': f'Fehler: {str(e)}'
            })
            print(f"❌ CV Processor Test fehlgeschlagen: {e}")
    
    def test_word_generator(self):
        """Test der Word-Generierung"""
        print("\n📄 Test 2: Word Generator")
        try:
            # Test-Daten
            test_data = {
                'expert_name': 'Test Expert',
                'hauptfokus': 'Test Consultant',
                'sprachen': 'Deutsch/Englisch',
                'zur_person': 'Test Beschreibung',
                'besondere_kenntnisse': 'Test Kenntnisse',
                'branchenkenntnisse': 'Test Branchen',
                'methoden': 'Test Methoden',
                'technologien': 'Test Technologien',
                'zertifizierungen': 'Test Zertifizierungen',
                'projekthistorie_text': 'Test Projekte'
            }
            
            # Word-Dokument generieren
            output_file = self.word_generator.generate_word_document(test_data)
            
            if output_file and os.path.exists(output_file):
                self.test_results.append({
                    'test': 'Word Generator',
                    'status': 'PASS',
                    'message': f'Word-Dokument erstellt: {output_file}'
                })
                print("✅ Word Generator Test erfolgreich")
            else:
                raise Exception("Word-Dokument wurde nicht erstellt")
                
        except Exception as e:
            self.test_results.append({
                'test': 'Word Generator',
                'status': 'FAIL',
                'message': f'Fehler: {str(e)}'
            })
            print(f"❌ Word Generator Test fehlgeschlagen: {e}")
    
    def test_supabase_integration(self):
        """Test der Supabase Integration"""
        print("\n🗄️ Test 3: Supabase Integration")
        try:
            # Test-Profil
            test_profile = {
                'expert_name': 'Test Expert',
                'hauptfokus': 'Test Consultant',
                'technologien': 'Test Technologien',
                'projekthistorie': [{'projekt_name': 'Test Projekt'}]
            }
            
            # Profil einfügen
            profile_id = self.supabase_integration.insert_profile(test_profile)
            
            if profile_id:
                # Semantische Suche testen
                search_results = self.supabase_integration.semantic_search("Test Consultant", limit=1)
                
                self.test_results.append({
                    'test': 'Supabase Integration',
                    'status': 'PASS',
                    'message': f'Profil gespeichert: {profile_id}, Suche: {len(search_results)} Ergebnisse'
                })
                print("✅ Supabase Integration Test erfolgreich")
            else:
                raise Exception("Profil konnte nicht gespeichert werden")
                
        except Exception as e:
            self.test_results.append({
                'test': 'Supabase Integration',
                'status': 'FAIL',
                'message': f'Fehler: {str(e)}'
            })
            print(f"❌ Supabase Integration Test fehlgeschlagen: {e}")
    
    def test_end_to_end(self):
        """End-to-End Test"""
        print("\n🔄 Test 4: End-to-End")
        try:
            # Mock CV-Daten
            mock_cv_data = {
                'name': 'End-to-End Test Expert',
                'contact': {'email': 'e2e@example.com'},
                'experience': [{'title': 'Senior Consultant', 'description': 'E2E Test experience'}],
                'skills': ['Python', 'Salesforce', 'Agile'],
                'languages': ['German', 'English']
            }
            
            # 1. CV verarbeiten
            nunc_profile = self.cv_processor._convert_to_nunc_format(mock_cv_data)
            
            # 2. Word-Dokument generieren
            word_file = self.word_generator.generate_word_document(nunc_profile)
            
            # 3. In Supabase speichern
            profile_id = self.supabase_integration.insert_profile(nunc_profile)
            
            # 4. Semantische Suche
            search_results = self.supabase_integration.semantic_search("Senior Consultant", limit=1)
            
            if word_file and profile_id and search_results:
                self.test_results.append({
                    'test': 'End-to-End',
                    'status': 'PASS',
                    'message': 'Kompletter Workflow erfolgreich'
                })
                print("✅ End-to-End Test erfolgreich")
            else:
                raise Exception("End-to-End Test fehlgeschlagen")
                
        except Exception as e:
            self.test_results.append({
                'test': 'End-to-End',
                'status': 'FAIL',
                'message': f'Fehler: {str(e)}'
            })
            print(f"❌ End-to-End Test fehlgeschlagen: {e}")
    
    def print_test_results(self):
        """Gibt Test-Ergebnisse aus"""
        print("\n" + "=" * 50)
        print("📊 TEST ERGEBNISSE")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['status'] == 'PASS')
        total = len(self.test_results)
        
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"{status_icon} {result['test']}: {result['message']}")
        
        print(f"\n📈 Gesamt: {passed}/{total} Tests erfolgreich")
        
        if passed == total:
            print("🎉 Alle Tests erfolgreich! System ist einsatzbereit.")
        else:
            print("⚠️ Einige Tests fehlgeschlagen. Bitte überprüfen Sie die Fehler.")
        
        # Ergebnisse in Datei speichern
        self.save_test_results()
    
    def save_test_results(self):
        """Speichert Test-Ergebnisse"""
        results_file = "../07_Output_Files/test_results/test_results.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        test_report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'passed_tests': sum(1 for r in self.test_results if r['status'] == 'PASS'),
            'failed_tests': sum(1 for r in self.test_results if r['status'] == 'FAIL'),
            'results': self.test_results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(test_report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Test-Ergebnisse gespeichert: {results_file}")

def main():
    """Hauptfunktion für Test-Suite"""
    test_suite = NuncTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()

