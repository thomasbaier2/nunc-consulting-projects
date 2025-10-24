"""
NUNC Expert Management System - CV Processing Exceptions
Custom Exceptions für CV-Verarbeitung
"""


class CvProcessingError(Exception):
    """Basis-Exception für CV-Verarbeitungsfehler"""
    pass


class PdfExtractionError(CvProcessingError):
    """Exception bei PDF-Extraktionsfehlern"""
    
    def __init__(self, file_path: str, message: str = None):
        self.file_path = file_path
        super().__init__(f"PDF extraction failed for '{file_path}': {message or 'Unknown error'}")


class DataValidationError(CvProcessingError):
    """Exception bei Daten-Validierungsfehlern"""
    
    def __init__(self, field: str, message: str = None):
        self.field = field
        super().__init__(f"Data validation error for field '{field}': {message or 'Invalid data'}")


class WordGenerationError(CvProcessingError):
    """Exception bei Word-Dokument-Generierung"""
    
    def __init__(self, profile_id: str, message: str = None):
        self.profile_id = profile_id
        super().__init__(f"Word generation failed for profile '{profile_id}': {message or 'Unknown error'}")


class SupabaseIntegrationError(CvProcessingError):
    """Exception bei Supabase-Integration-Fehlern"""
    
    def __init__(self, operation: str, message: str = None):
        self.operation = operation
        super().__init__(f"Supabase integration error during '{operation}': {message or 'Unknown error'}")


class FileFormatError(CvProcessingError):
    """Exception bei ungültigen Dateiformaten"""
    
    def __init__(self, file_path: str, expected_format: str = None):
        self.file_path = file_path
        self.expected_format = expected_format
        message = f"Invalid file format for '{file_path}'"
        if expected_format:
            message += f". Expected: {expected_format}"
        super().__init__(message)


class ProcessingTimeoutError(CvProcessingError):
    """Exception bei Verarbeitungs-Timeout"""
    
    def __init__(self, timeout_seconds: int):
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Processing timeout after {timeout_seconds} seconds")
