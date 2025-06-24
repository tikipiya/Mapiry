"""
Main API client for Mapiry SDK
"""

import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin
import time

from .exceptions import (
    AuthenticationError, RateLimitError, APIError, NetworkError, 
    NotFoundError, TimeoutError
)
from .endpoints.images import ImageEndpoint
from .endpoints.sequences import SequenceEndpoint
from .endpoints.detections import DetectionEndpoint
from .endpoints.vector_tiles import VectorTileEndpoint
from .endpoints.organizations import OrganizationEndpoint
from .endpoints.map_features import MapFeatureEndpoint
from .utils import retry_with_backoff


class MapillaryClient:
    """
    Main client for interacting with Mapillary API v4.
    
    This client provides access to all Mapillary API endpoints through
    a simple and intuitive interface.
    
    Example:
        >>> client = MapillaryClient(api_key="your_api_key")
        >>> images = client.images().close_to(longitude=31, latitude=30).get()
        >>> detections = client.detections().in_bbox(west=-122.151, south=37.484, east=-122.149, north=37.486).get()
    """
    
    BASE_URL = "https://graph.mapillary.com"
    VECTOR_TILES_URL = "https://tiles.mapillary.com/maps/vtp"
    COVERAGE_TILES_URL = "https://tiles.mapillary.com/maps/vtp/mly1_public/2"
    COMPUTED_COVERAGE_TILES_URL = "https://tiles.mapillary.com/maps/vtp/mly1_computed_public/2"
    MAP_FEATURES_POINTS_URL = "https://tiles.mapillary.com/maps/vtp/mly_map_feature_point/2"
    MAP_FEATURES_TRAFFIC_SIGNS_URL = "https://tiles.mapillary.com/maps/vtp/mly_map_feature_traffic_sign/2"
    
    def __init__(
        self, 
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
        session: Optional[requests.Session] = None
    ):
        """
        Initialize the Mapillary client.
        
        Args:
            api_key: Your Mapillary API access token
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for failed requests (default: 3)
            retry_backoff: Backoff factor for retries (default: 1.0)
            session: Optional requests session to use
            
        Raises:
            AuthenticationError: If API key is invalid
        """
        if not api_key or not isinstance(api_key, str):
            raise AuthenticationError("API key must be a non-empty string")
        
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        
        # Use provided session or create new one
        self.session = session or requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"OAuth {self.api_key}",
            "User-Agent": "Mapiry/1.0.0 Python SDK",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        # Initialize endpoints
        self._images = None
        self._sequences = None
        self._detections = None
        self._vector_tiles = None
        self._organizations = None
        self._map_features = None
    
    def images(self) -> ImageEndpoint:
        """
        Access image-related endpoints.
        
        Returns:
            ImageEndpoint instance
        """
        if self._images is None:
            self._images = ImageEndpoint(self)
        return self._images
    
    def sequences(self) -> SequenceEndpoint:
        """
        Access sequence-related endpoints.
        
        Returns:
            SequenceEndpoint instance
        """
        if self._sequences is None:
            self._sequences = SequenceEndpoint(self)
        return self._sequences
    
    def detections(self) -> DetectionEndpoint:
        """
        Access detection-related endpoints.
        
        Returns:
            DetectionEndpoint instance
        """
        if self._detections is None:
            self._detections = DetectionEndpoint(self)
        return self._detections
    
    def vector_tiles(self) -> VectorTileEndpoint:
        """
        Access vector tile endpoints.
        
        Returns:
            VectorTileEndpoint instance
        """
        if self._vector_tiles is None:
            self._vector_tiles = VectorTileEndpoint(self)
        return self._vector_tiles
    
    def map_features(self) -> MapFeatureEndpoint:
        """
        Access map feature endpoints.
        
        Returns:
            MapFeatureEndpoint instance
        """
        if self._map_features is None:
            self._map_features = MapFeatureEndpoint(self)
        return self._map_features
    
    def organizations(self) -> OrganizationEndpoint:
        """
        Access organization-related endpoints.
        
        Returns:
            OrganizationEndpoint instance
        """
        if self._organizations is None:
            self._organizations = OrganizationEndpoint(self)
        return self._organizations
    
    def request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        base_url: Optional[str] = None,
        use_oauth_header: bool = True
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Mapillary API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            base_url: Override base URL
            use_oauth_header: Whether to use OAuth header
            
        Returns:
            Response data as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: If API returns error
            NetworkError: If network error occurs
            NotFoundError: If resource not found
            TimeoutError: If request times out
        """
        url = urljoin(base_url or self.BASE_URL, endpoint)
        
        # Prepare headers
        headers = {}
        if use_oauth_header:
            headers["Authorization"] = f"OAuth {self.api_key}"
        elif params is None:
            params = {}
        
        # Add access token as query parameter if not using OAuth header
        if not use_oauth_header:
            if params is None:
                params = {}
            params["access_token"] = self.api_key
        
        def make_request():
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
                return self._handle_response(response)
            except requests.exceptions.Timeout:
                raise TimeoutError(f"Request to {url} timed out after {self.timeout} seconds")
            except requests.exceptions.ConnectionError:
                raise NetworkError(f"Failed to connect to {url}")
            except requests.exceptions.RequestException as e:
                raise NetworkError(f"Network error: {str(e)}")
        
        return retry_with_backoff(
            make_request, 
            max_retries=self.max_retries, 
            backoff_factor=self.retry_backoff
        )
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: HTTP response object
            
        Returns:
            Response data as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: If API returns error
            NotFoundError: If resource not found
        """
        # Handle successful responses
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                # Handle non-JSON responses (e.g., vector tiles)
                return {"content": response.content, "headers": dict(response.headers)}
        
        # Handle error responses
        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
        except ValueError:
            error_message = f"HTTP {response.status_code}: {response.reason}"
            error_data = None
        
        if response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif response.status_code == 403:
            raise AuthenticationError(f"Access forbidden: {error_message}")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {error_message}")
        elif response.status_code == 429:
            # Check for Retry-After header
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds.")
            else:
                raise RateLimitError(f"Rate limit exceeded: {error_message}")
        else:
            raise APIError(
                message=error_message,
                status_code=response.status_code,
                response_data=error_data
            )
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data
        """
        return self.request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make POST request to API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response data
        """
        return self.request("POST", endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make PUT request to API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response data
        """
        return self.request("PUT", endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make DELETE request to API.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Response data
        """
        return self.request("DELETE", endpoint)
    
    def close(self):
        """Close the HTTP session."""
        if self.session:
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()