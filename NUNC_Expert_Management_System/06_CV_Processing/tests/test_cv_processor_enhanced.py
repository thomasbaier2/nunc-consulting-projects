"""
NUNC Expert Management System - CV Processing Enhanced Tests
Erweiterte Unit-Tests für den verbesserten CvProcessor
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import os

# Importiere die zu testenden Module
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from NUNC_Expert_Management_System.cv_processing.cv_processor import CvProcessor
from NUNC_Expert_Management_System.cv_processing.models import CvData, ExtractedData, ProcessingResult, ProcessingStatus
from NUNC_Expert_Management_System.cv_processing.exceptions import PdfExtractionError, DataValidationError, ProcessingTimeoutError
from NUNC_Expert_Management_System.shared_components.config import Config


class TestCvProcessorEnhanced:
    """Erweiterte Test-Klasse für CvProcessor"""
    
    def test_init_with_config(self):
        """Test CvProcessor Initialisierung mit Konfiguration"""
        config = Config()
        config.CV_PROCESSING = {
            'max_file_size': 5 * 1024 * 1024,
            'extraction_timeout': 15,
            'processing_timeout': 60
        }
        
        processor = CvProcessor(config)
        
        assert processor.max_file_size == 5 * 1024 * 1024
        assert processor.extraction_timeout == 15
        assert processor.processing_timeout == 60
        assert processor.supported_formats == ['.pdf']
    
    def test_validate_file_success(self, temp_dir):
        """Test erfolgreiche Datei-Validierung"""
        processor = CvProcessor()
        
        # Erstelle Test-PDF
        pdf_path = temp_dir / "test.pdf"
        pdf_path.write_bytes(b"PDF content")
        
        # Sollte keine Exception werfen
        processor._validate_file(str(pdf_path))
    
    def test_validate_file_not_found(self, temp_dir):
        """Test Datei-Validierung mit nicht existierender Datei"""
        processor = CvProcessor()
        
        pdf_path = temp_dir / "nonexistent.pdf"
        
        with pytest.raises(FileNotFoundError):
            processor._validate_file(str(pdf_path))
    
    def test_validate_file_too_large(self, temp_dir):
        """Test Datei-Validierung mit zu großer Datei"""
        config = Config()
        config.CV_PROCESSING = {'max_file_size': 100}  # 100 bytes
        
        processor = CvProcessor(config)
        
        # Erstelle große Datei
        pdf_path = temp_dir / "large.pdf"
        pdf_path.write_bytes(b"x" * 200)  # 200 bytes
        
        with pytest.raises(ValueError, match="Datei zu groß"):
            processor._validate_file(str(pdf_path))
    
    def test_validate_file_wrong_format(self, temp_dir):
        """Test Datei-Validierung mit falschem Format"""
        processor = CvProcessor()
        
        # Erstelle Text-Datei
        txt_path = temp_dir / "test.txt"
        txt_path.write_text("Not a PDF")
        
        with pytest.raises(ValueError, match="Nur PDF-Dateien"):
            processor._validate_file(str(txt_path))
    
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.pdfplumber')
    def test_extract_text_pdfplumber_success(self, mock_pdfplumber, temp_dir):
        """Test erfolgreiche PDF-Text-Extraktion mit pdfplumber"""
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
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.PyPDF2')
    def test_extract_text_fallback_pypdf2(self, mock_pypdf2, mock_pdfplumber, temp_dir):
        """Test Fallback zu PyPDF2 wenn pdfplumber fehlschlägt"""
        processor = CvProcessor()
        
        # Mock pdfplumber Fehler
        mock_pdfplumber.open.side_effect = Exception("pdfplumber failed")
        
        # Mock PyPDF2
        mock_reader = Mock()
        mock_page = Mock()
        mock_page.extract_text.return_value = "Fallback text"
        mock_reader.pages = [mock_page]
        mock_pypdf2.PdfReader.return_value = mock_reader
        
        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()
        
        result = processor._extract_text_from_pdf(str(pdf_path))
        
        assert result == "Fallback text\n"
        mock_pypdf2.PdfReader.assert_called_once()
    
    def test_categorize_skills(self):
        """Test Skill-Kategorisierung"""
        processor = CvProcessor()
        
        skills = [
            "Python", "JavaScript", "React", "Leadership", "Teamwork",
            "SQL", "Docker", "Communication", "AWS", "Agile"
        ]
        
        technical, soft = processor._categorize_skills(skills)
        
        # Prüfe technische Skills
        assert "Python" in technical
        assert "JavaScript" in technical
        assert "React" in technical
        assert "SQL" in technical
        assert "Docker" in technical
        assert "AWS" in technical
        
        # Prüfe Soft Skills
        assert "Leadership" in soft
        assert "Teamwork" in soft
        assert "Communication" in soft
        assert "Agile" in soft
    
    def test_extract_certifications(self):
        """Test Zertifizierungs-Extraktion"""
        processor = CvProcessor()
        
        text = """
        AWS Certified Solutions Architect
        Microsoft Azure Certification
        Salesforce Certified Developer
        """
        
        certifications = processor._extract_certifications(text)
        
        assert len(certifications) > 0
        assert any("AWS" in cert['name'] for cert in certifications)
        assert any("Microsoft" in cert['name'] for cert in certifications)
    
    def test_extract_availability(self):
        """Test Verfügbarkeits-Extraktion"""
        processor = CvProcessor()
        
        text = """
        Available for remote work
        40 hours per week
        Can work onsite if needed
        """
        
        availability = processor._extract_availability(text)
        
        assert availability['remote'] is True
        assert availability['onsite'] is True
        assert availability['hours_per_week'] == 40
    
    def test_validate_cv_data_valid(self):
        """Test CV-Daten-Validierung - gültige Daten"""
        processor = CvProcessor()
        
        valid_data = {
            'name': 'Max Mustermann',
            'email': 'max.mustermann@example.com',
            'experience': [{'company': 'Tech Corp', 'position': 'Developer'}],
            'skills': ['Python', 'JavaScript']
        }
        
        result = processor.validate_cv_data(valid_data)
        assert result is True
    
    def test_validate_cv_data_invalid_name(self):
        """Test CV-Daten-Validierung - ungültiger Name"""
        processor = CvProcessor()
        
        invalid_data = {
            'name': '',  # Leerer Name
            'email': 'max.mustermann@example.com',
            'experience': [{'company': 'Tech Corp'}]
        }
        
        result = processor.validate_cv_data(invalid_data)
        assert result is False
    
    def test_validate_cv_data_invalid_email(self):
        """Test CV-Daten-Validierung - ungültige E-Mail"""
        processor = CvProcessor()
        
        invalid_data = {
            'name': 'Max Mustermann',
            'email': 'invalid-email',  # Ungültige E-Mail
            'experience': [{'company': 'Tech Corp'}]
        }
        
        result = processor.validate_cv_data(invalid_data)
        assert result is False
    
    def test_validate_cv_data_no_experience_or_skills(self):
        """Test CV-Daten-Validierung - keine Erfahrung oder Skills"""
        processor = CvProcessor()
        
        invalid_data = {
            'name': 'Max Mustermann',
            'email': 'max.mustermann@example.com',
            'experience': [],
            'skills': []
        }
        
        result = processor.validate_cv_data(invalid_data)
        assert result is False
    
    @patch('NUNC_Expert_Management_System.cv_processing.cv_processor.pdfplumber')
    def test_process_pdf_success(self, mock_pdfplumber, temp_dir):
        """Test erfolgreiche PDF-Verarbeitung"""
        processor = CvProcessor()
        
        # Mock pdfplumber
        mock_pdf = Mock()
        mock_pdf.pages = [Mock()]
        mock_pdf.pages[0].extract_text.return_value = "Max Mustermann\nSenior Developer\nmax.mustermann@example.com"
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
        
        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()
        
        result = processor.process_pdf(str(pdf_path))
        
        assert isinstance(result, ProcessingResult)
        assert result.status == ProcessingStatus.COMPLETED
        assert result.cv_data is not None
        assert result.extracted_data is not None
        assert result.processing_time > 0
    
    def test_process_pdf_file_not_found(self, temp_dir):
        """Test PDF-Verarbeitung mit nicht existierender Datei"""
        processor = CvProcessor()
        
        pdf_path = temp_dir / "nonexistent.pdf"
        
        result = processor.process_pdf(str(pdf_path))
        
        assert isinstance(result, ProcessingResult)
        assert result.status == ProcessingStatus.FAILED
        assert result.error_message is not None
        assert "PDF-Datei nicht gefunden" in result.error_message
    
    def test_process_pdf_validation_error(self, temp_dir):
        """Test PDF-Verarbeitung mit Validierungsfehler"""
        config = Config()
        config.CV_PROCESSING = {'max_file_size': 100}  # Sehr kleine Datei
        
        processor = CvProcessor(config)
        
        # Erstelle große Datei
        pdf_path = temp_dir / "large.pdf"
        pdf_path.write_bytes(b"x" * 200)
        
        result = processor.process_pdf(str(pdf_path))
        
        assert isinstance(result, ProcessingResult)
        assert result.status == ProcessingStatus.FAILED
        assert "Datei zu groß" in result.error_message
    
    def test_processing_result_creation(self):
        """Test ProcessingResult Erstellung"""
        cv_data = CvData(
            file_path="test.pdf",
            file_name="test.pdf",
            file_size=1024,
            extracted_text="Test content",
            extraction_method="pdfplumber"
        )
        
        extracted_data = ExtractedData(
            name="Max Mustermann",
            email="max@example.com"
        )
        
        result = ProcessingResult(
            status=ProcessingStatus.COMPLETED,
            cv_data=cv_data,
            extracted_data=extracted_data,
            profile_id="profile_001",
            processing_time=2.5
        )
        
        assert result.is_successful() is True
        assert result.has_error() is False
        assert result.processing_time == 2.5
        assert result.profile_id == "profile_001"
    
    def test_processing_result_error(self):
        """Test ProcessingResult mit Fehler"""
        result = ProcessingResult(
            status=ProcessingStatus.FAILED,
            cv_data=None,
            error_message="Test error",
            processing_time=1.0
        )
        
        assert result.is_successful() is False
        assert result.has_error() is True
        assert result.error_message == "Test error"
