"""
NUNC Expert Management System - Shared Components Exceptions
Basis-Exceptions für alle System-Komponenten
"""


class NemsError(Exception):
    """Basis-Exception für alle NEMS-Fehler"""
    pass


class ValidationError(NemsError):
    """Exception bei Validierungsfehlern"""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(f"Validation error: {message}")


class DatabaseError(NemsError):
    """Exception bei Datenbank-Fehlern"""
    
    def __init__(self, operation: str, message: str = None):
        self.operation = operation
        super().__init__(f"Database error during '{operation}': {message or 'Unknown error'}")


class ConfigurationError(NemsError):
    """Exception bei Konfigurationsfehlern"""
    
    def __init__(self, config_key: str, message: str = None):
        self.config_key = config_key
        super().__init__(f"Configuration error for '{config_key}': {message or 'Invalid configuration'}")


class AuthenticationError(NemsError):
    """Exception bei Authentifizierungsfehlern"""
    
    def __init__(self, service: str, message: str = None):
        self.service = service
        super().__init__(f"Authentication error for '{service}': {message or 'Authentication failed'}")


class NetworkError(NemsError):
    """Exception bei Netzwerk-Fehlern"""
    
    def __init__(self, url: str, message: str = None):
        self.url = url
        super().__init__(f"Network error for '{url}': {message or 'Network request failed'}")


class FileSystemError(NemsError):
    """Exception bei Dateisystem-Fehlern"""
    
    def __init__(self, path: str, operation: str, message: str = None):
        self.path = path
        self.operation = operation
        super().__init__(f"File system error during '{operation}' on '{path}': {message or 'Unknown error'}")


class ServiceUnavailableError(NemsError):
    """Exception bei nicht verfügbaren Services"""
    
    def __init__(self, service: str, message: str = None):
        self.service = service
        super().__init__(f"Service '{service}' unavailable: {message or 'Service not responding'}")
