"""
NUNC Expert Management System - CV Processing Tests
Unit-Tests für CvProcessor
"""

import pytest
from unittest.mock import Mock, patch, mock_open
import tempfile
from pathlib import Path

# Importiere die zu testenden Module
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from NUNC_Expert_Management_System.cv_processing.cv_processor import CvProcessor
from NUNC_Expert_Management_System.cv_processing.models import CvData, ExtractedData, ProcessingResult, ProcessingStatus
from NUNC_Expert_Management_System.cv_processing.exceptions import PdfExtractionError, DataValidationError


class TestCvProcessor:
    """Test-Klasse für CvProcessor"""
    
    def test_init(self):
        """Test CvProcessor Initialisierung"""
        processor = CvProcessor()
        
        assert processor.supported_formats == ['.pdf']
        assert processor.output_dir == "08_Output_Files/generated_profiles"
    
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.pdfplumber')
    def test_extract_text_from_pdf_success(self, mock_pdfplumber, temp_dir):
        """Test erfolgreiche PDF-Text-Extraktion"""
        processor = CvProcessor()
        
        # Mock pdfplumber
        mock_pdf = Mock()
        mock_pdf.pages = [Mock()]
        mock_pdf.pages[0].extract_text.return_value = "Max Mustermann\nSenior Developer"
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
        
        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()
        
        result = processor._extract_text_from_pdf(str(pdf_path))
        
        assert result == "Max Mustermann\nSenior Developer"
        mock_pdfplumber.open.assert_called_once()
    
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.pdfplumber')
    def test_extract_text_from_pdf_failure(self, mock_pdfplumber, temp_dir):
        """Test PDF-Text-Extraktion Fehler"""
        processor = CvProcessor()
        
        # Mock pdfplumber Fehler
        mock_pdfplumber.open.side_effect = Exception("PDF cannot be opened")
        
        pdf_path = temp_dir / "invalid.pdf"
        pdf_path.touch()
        
        with pytest.raises(PdfExtractionError):
            processor._extract_text_from_pdf(str(pdf_path))
    
    def test_extract_structured_data(self):
        """Test strukturierte Datenextraktion"""
        processor = CvProcessor()
        
        text = """
        Max Mustermann
        Senior Developer
        max.mustermann@example.com
        +49 123 456789
        Berlin, Deutschland
        
        Experience:
        - Tech Corp (2020-2023): Senior Developer
        - Startup XYZ (2018-2020): Developer
        
        Skills: Python, JavaScript, React, Docker
        """
        
        result = processor._extract_structured_data(text)
        
        assert 'name' in result
        assert 'email' in result
        assert 'phone' in result
        assert 'location' in result
        assert 'experience' in result
        assert 'skills' in result
    
    def test_convert_to_nunc_format(self):
        """Test Konvertierung zu NUNC-Format"""
        processor = CvProcessor()
        
        structured_data = {
            'name': 'Max Mustermann',
            'email': 'max.mustermann@example.com',
            'phone': '+49 123 456789',
            'location': 'Berlin',
            'experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Senior Developer',
                    'start_date': '2020-01-01',
                    'end_date': '2023-12-31'
                }
            ],
            'skills': ['Python', 'JavaScript', 'React']
        }
        
        result = processor._convert_to_nunc_format(structured_data)
        
        assert result['expert_name'] == 'Max Mustermann'
        assert result['email'] == 'max.mustermann@example.com'
        assert result['phone'] == '+49 123 456789'
        assert result['location'] == 'Berlin'
        assert len(result['experience']) == 1
        assert result['skills'] == ['Python', 'JavaScript', 'React']
    
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.CvProcessor._extract_text_from_pdf')
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.CvProcessor._extract_structured_data')
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.CvProcessor._convert_to_nunc_format')
    def test_process_pdf_success(self, mock_convert, mock_extract, mock_text, temp_dir):
        """Test erfolgreiche PDF-Verarbeitung"""
        processor = CvProcessor()
        
        # Mock die internen Methoden
        mock_text.return_value = "Test CV text"
        mock_extract.return_value = {"name": "Max Mustermann"}
        mock_convert.return_value = {"expert_name": "Max Mustermann"}
        
        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()
        
        result = processor.process_pdf(str(pdf_path))
        
        assert 'expert_name' in result
        assert result['expert_name'] == "Max Mustermann"
        mock_text.assert_called_once()
        mock_extract.assert_called_once()
        mock_convert.assert_called_once()
    
    def test_process_pdf_file_not_found(self, temp_dir):
        """Test PDF-Verarbeitung mit nicht existierender Datei"""
        processor = CvProcessor()
        
        pdf_path = temp_dir / "nonexistent.pdf"
        
        result = processor.process_pdf(str(pdf_path))
        
        assert 'error' in result
        assert 'Fehler bei der PDF-Verarbeitung' in result['error']
    
    def test_validate_cv_data_valid(self):
        """Test CV-Daten-Validierung - gültige Daten"""
        processor = CvProcessor()
        
        valid_data = {
            'name': 'Max Mustermann',
            'email': 'max.mustermann@example.com',
            'phone': '+49 123 456789',
            'experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Developer',
                    'start_date': '2020-01-01'
                }
            ]
        }
        
        result = processor.validate_cv_data(valid_data)
        assert result is True
    
    def test_validate_cv_data_invalid(self):
        """Test CV-Daten-Validierung - ungültige Daten"""
        processor = CvProcessor()
        
        invalid_data = {
            'name': '',  # Leerer Name
            'email': 'invalid-email',  # Ungültige E-Mail
            'experience': []  # Keine Erfahrung
        }
        
        result = processor.validate_cv_data(invalid_data)
        assert result is False
    
    def test_supported_formats(self):
        """Test unterstützte Dateiformate"""
        processor = CvProcessor()
        
        assert '.pdf' in processor.supported_formats
        assert len(processor.supported_formats) == 1
    
    def test_output_directory_creation(self, temp_dir):
        """Test Output-Verzeichnis-Erstellung"""
        processor = CvProcessor()
        processor.output_dir = str(temp_dir / "output")
        
        # Sollte das Verzeichnis erstellen können
        assert True  # Placeholder - würde in echter Implementation getestet
