"""
Mapiry - A comprehensive Python SDK for Mapillary API v4

This package provides a simple and intuitive interface to interact with
all Mapillary API v4 endpoints, including images, sequences, detections,
vector tiles, and organizations.

Example:
    >>> from mapiry import MapillaryClient
    >>> client = MapillaryClient(api_key="your_api_key")
    >>> images = client.images().close_to(longitude=31, latitude=30).get()
"""

__version__ = "1.0.0"
__author__ = "tikisn"
__email__ = "s2501082@sendai-nct.jp"
__url__ = "https://github.com/tikipiya/Mapiry"

from .client import MapillaryClient
from .models import (
    Image, Sequence, Detection, MapFeature, Organization, 
    Geometry, APIResponse
)
from .exceptions import (
    MapiryError, AuthenticationError, RateLimitError, APIError,
    ValidationError, NetworkError, NotFoundError, TimeoutError
)

__all__ = [
    "MapillaryClient",
    "Image", "Sequence", "Detection", "MapFeature", "Organization",
    "Geometry", "APIResponse",
    "MapiryError", "AuthenticationError", "RateLimitError", "APIError",
    "ValidationError", "NetworkError", "NotFoundError", "TimeoutError"
]