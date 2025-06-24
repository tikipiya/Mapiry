"""
Custom exceptions for Mapiry SDK
"""

class MapiryError(Exception):
    """Base exception class for Mapiry SDK"""
    pass


class AuthenticationError(MapiryError):
    """Raised when authentication fails"""
    def __init__(self, message="Authentication failed. Please check your API key."):
        self.message = message
        super().__init__(self.message)


class RateLimitError(MapiryError):
    """Raised when API rate limit is exceeded"""
    def __init__(self, message="API rate limit exceeded. Please wait before making more requests."):
        self.message = message
        super().__init__(self.message)


class APIError(MapiryError):
    """Raised when API returns an error response"""
    def __init__(self, message, status_code=None, response_data=None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class ValidationError(MapiryError):
    """Raised when input validation fails"""
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class NetworkError(MapiryError):
    """Raised when network-related errors occur"""
    def __init__(self, message="Network error occurred. Please check your connection."):
        self.message = message
        super().__init__(self.message)


class NotFoundError(MapiryError):
    """Raised when requested resource is not found"""
    def __init__(self, message="Requested resource not found."):
        self.message = message
        super().__init__(self.message)


class TimeoutError(MapiryError):
    """Raised when request times out"""
    def __init__(self, message="Request timed out. Please try again."):
        self.message = message
        super().__init__(self.message)