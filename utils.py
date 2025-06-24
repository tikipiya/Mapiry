"""
Utility functions for Mapiry SDK
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union, List
from urllib.parse import urlencode

from .exceptions import ValidationError


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
        
    Raises:
        ValidationError: If coordinates are invalid
    """
    if not isinstance(latitude, (int, float)):
        raise ValidationError("Latitude must be a number", "latitude")
    if not isinstance(longitude, (int, float)):
        raise ValidationError("Longitude must be a number", "longitude")
    
    if not -90 <= latitude <= 90:
        raise ValidationError("Latitude must be between -90 and 90", "latitude")
    if not -180 <= longitude <= 180:
        raise ValidationError("Longitude must be between -180 and 180", "longitude")


def validate_bbox(west: float, south: float, east: float, north: float) -> None:
    """
    Validate bounding box coordinates.
    
    Args:
        west: Western longitude
        south: Southern latitude
        east: Eastern longitude
        north: Northern latitude
        
    Raises:
        ValidationError: If bounding box is invalid
    """
    validate_coordinates(south, west)
    validate_coordinates(north, east)
    
    if west >= east:
        raise ValidationError("West longitude must be less than east longitude", "bbox")
    if south >= north:
        raise ValidationError("South latitude must be less than north latitude", "bbox")


def validate_date_string(date_str: str) -> None:
    """
    Validate date string format.
    
    Args:
        date_str: Date string in format YYYY, YYYY-MM, or YYYY-MM-DDTHH:MM:SS
        
    Raises:
        ValidationError: If date format is invalid
    """
    if not isinstance(date_str, str):
        raise ValidationError("Date must be a string", "date")
    
    # Try different date formats
    formats = [
        "%Y",
        "%Y-%m",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ"
    ]
    
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return
        except ValueError:
            continue
    
    raise ValidationError(
        "Date must be in format YYYY, YYYY-MM, YYYY-MM-DD, or YYYY-MM-DDTHH:MM:SS", 
        "date"
    )


def validate_image_type(image_type: str) -> None:
    """
    Validate image type.
    
    Args:
        image_type: Image type string
        
    Raises:
        ValidationError: If image type is invalid
    """
    valid_types = ["flat", "pano", "both", "all"]
    if image_type not in valid_types:
        raise ValidationError(
            f"Image type must be one of: {', '.join(valid_types)}", 
            "image_type"
        )


def validate_compass_angle(angle: Union[float, tuple]) -> None:
    """
    Validate compass angle or angle range.
    
    Args:
        angle: Single angle or tuple of (min_angle, max_angle)
        
    Raises:
        ValidationError: If angle is invalid
    """
    if isinstance(angle, (int, float)):
        if not 0 <= angle <= 360:
            raise ValidationError("Compass angle must be between 0 and 360", "compass_angle")
    elif isinstance(angle, (tuple, list)) and len(angle) == 2:
        min_angle, max_angle = angle
        if not 0 <= min_angle <= 360 or not 0 <= max_angle <= 360:
            raise ValidationError("Compass angles must be between 0 and 360", "compass_angle")
        # Handle wraparound case (e.g., 315° to 45° covers north)
        if min_angle > max_angle and not (min_angle > 180 and max_angle < 180):
            raise ValidationError("Invalid compass angle range", "compass_angle")
    else:
        raise ValidationError("Compass angle must be a number or tuple of two numbers", "compass_angle")


def build_query_params(params: Dict[str, Any]) -> str:
    """
    Build query parameters string from dictionary.
    
    Args:
        params: Dictionary of parameters
        
    Returns:
        URL-encoded query string
    """
    # Filter out None values
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    # Convert lists to comma-separated strings
    for key, value in filtered_params.items():
        if isinstance(value, list):
            filtered_params[key] = ",".join(str(v) for v in value)
    
    return urlencode(filtered_params)


def parse_response_data(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and normalize response data.
    
    Args:
        response_data: Raw response data from API
        
    Returns:
        Normalized response data
    """
    if not isinstance(response_data, dict):
        return response_data
    
    # Handle GeoJSON format
    if "type" in response_data and response_data["type"] == "FeatureCollection":
        return {
            "type": "FeatureCollection",
            "features": response_data.get("features", []),
            "total_count": len(response_data.get("features", [])),
            "metadata": response_data.get("metadata", {})
        }
    
    return response_data


def retry_with_backoff(func, max_retries: int = 3, backoff_factor: float = 1.0):
    """
    Retry function with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        backoff_factor: Backoff multiplier
        
    Returns:
        Function result
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise e
            
            wait_time = backoff_factor * (2 ** attempt)
            time.sleep(wait_time)


def format_timestamp(timestamp: Optional[str]) -> Optional[datetime]:
    """
    Format timestamp string to datetime object.
    
    Args:
        timestamp: Timestamp string
        
    Returns:
        datetime object or None
    """
    if not timestamp:
        return None
    
    # Try different timestamp formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    
    return None


def chunks(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divide list into chunks of specified size.
    
    Args:
        lst: List to divide
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]