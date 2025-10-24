"""
NUNC Expert Management System - Core System Exceptions
Custom Exceptions für Profile-Management
"""


class ProfileError(Exception):
    """Basis-Exception für Profile-Fehler"""
    pass


class ProfileNotFoundError(ProfileError):
    """Exception wenn Profil nicht gefunden wird"""
    
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        super().__init__(f"Profile with ID '{profile_id}' not found")


class ProfileValidationError(ProfileError):
    """Exception bei Profil-Validierungsfehlern"""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(f"Profile validation error: {message}")


class ProfileDuplicateError(ProfileError):
    """Exception bei doppelten Profilen"""
    
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Profile with email '{email}' already exists")


class ProfileStorageError(ProfileError):
    """Exception bei Speicher-Fehlern"""
    
    def __init__(self, message: str):
        super().__init__(f"Profile storage error: {message}")


class ProfileSearchError(ProfileError):
    """Exception bei Such-Fehlern"""
    
    def __init__(self, query: str, message: str = None):
        self.query = query
        super().__init__(f"Profile search error for query '{query}': {message or 'Unknown error'}")
