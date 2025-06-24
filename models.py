"""
Data models for Mapiry SDK responses
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field

from .utils import format_timestamp


@dataclass
class Geometry:
    """Represents a geometry object"""
    type: str
    coordinates: List[Union[float, List[float]]]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Geometry':
        return cls(
            type=data.get("type", ""),
            coordinates=data.get("coordinates", [])
        )


@dataclass
class Image:
    """Represents a Mapillary image"""
    id: str
    geometry: Optional[Geometry] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    camera_type: Optional[str] = None
    camera_parameters: Optional[List[float]] = None
    captured_at: Optional[datetime] = None
    compass_angle: Optional[float] = None
    sequence_id: Optional[str] = None
    organization_id: Optional[str] = None
    creator_id: Optional[str] = None
    creator_username: Optional[str] = None
    is_pano: Optional[bool] = None
    altitude: Optional[float] = None
    thumb_256_url: Optional[str] = None
    thumb_1024_url: Optional[str] = None
    thumb_2048_url: Optional[str] = None
    thumb_original_url: Optional[str] = None
    computed_geometry: Optional[Geometry] = None
    computed_compass_angle: Optional[float] = None
    computed_altitude: Optional[float] = None
    computed_rotation: Optional[List[float]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    exif_orientation: Optional[int] = None
    atomic_scale: Optional[float] = None
    mesh_id: Optional[str] = None
    sfm_cluster_id: Optional[str] = None
    detections: List['Detection'] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Image':
        properties = data.get("properties", {})
        
        # Handle detections if present
        detections_data = properties.get("detections", [])
        detections = []
        if detections_data:
            for detection_data in detections_data:
                detections.append(Detection.from_dict(detection_data))
        
        return cls(
            id=properties.get("id", ""),
            geometry=Geometry.from_dict(data.get("geometry", {})) if data.get("geometry") else None,
            camera_make=properties.get("camera_make"),
            camera_model=properties.get("camera_model"),
            camera_type=properties.get("camera_type"),
            camera_parameters=properties.get("camera_parameters"),
            captured_at=format_timestamp(properties.get("captured_at")),
            compass_angle=properties.get("compass_angle"),
            sequence_id=properties.get("sequence_id"),
            organization_id=properties.get("organization_id"),
            creator_id=properties.get("creator_id"),
            creator_username=properties.get("creator_username"),
            is_pano=properties.get("is_pano"),
            altitude=properties.get("altitude"),
            thumb_256_url=properties.get("thumb_256_url"),
            thumb_1024_url=properties.get("thumb_1024_url"),
            thumb_2048_url=properties.get("thumb_2048_url"),
            thumb_original_url=properties.get("thumb_original_url"),
            computed_geometry=Geometry.from_dict(properties.get("computed_geometry", {})) if properties.get("computed_geometry") else None,
            computed_compass_angle=properties.get("computed_compass_angle"),
            computed_altitude=properties.get("computed_altitude"),
            computed_rotation=properties.get("computed_rotation"),
            width=properties.get("width"),
            height=properties.get("height"),
            exif_orientation=properties.get("exif_orientation"),
            atomic_scale=properties.get("atomic_scale"),
            mesh_id=properties.get("mesh_id"),
            sfm_cluster_id=properties.get("sfm_cluster_id"),
            detections=detections
        )


@dataclass
class Sequence:
    """Represents a Mapillary sequence"""
    id: str
    geometry: Optional[Geometry] = None
    created_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    organization_id: Optional[str] = None
    creator_id: Optional[str] = None
    creator_username: Optional[str] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    image_count: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sequence':
        properties = data.get("properties", {})
        
        return cls(
            id=properties.get("id", ""),
            geometry=Geometry.from_dict(data.get("geometry", {})) if data.get("geometry") else None,
            created_at=format_timestamp(properties.get("created_at")),
            captured_at=format_timestamp(properties.get("captured_at")),
            organization_id=properties.get("organization_id"),
            creator_id=properties.get("creator_id"),
            creator_username=properties.get("creator_username"),
            camera_make=properties.get("camera_make"),
            camera_model=properties.get("camera_model"),
            image_count=properties.get("image_count")
        )


@dataclass
class Detection:
    """Represents a detected object"""
    id: str
    geometry: Optional[Geometry] = None
    image_id: Optional[str] = None
    sequence_id: Optional[str] = None
    organization_id: Optional[str] = None
    creator_id: Optional[str] = None
    created_at: Optional[datetime] = None
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    object_type: Optional[str] = None
    object_value: Optional[str] = None
    confidence: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Detection':
        properties = data.get("properties", {})
        
        return cls(
            id=properties.get("id", ""),
            geometry=Geometry.from_dict(data.get("geometry", {})) if data.get("geometry") else None,
            image_id=properties.get("image_id"),
            sequence_id=properties.get("sequence_id"),
            organization_id=properties.get("organization_id"),
            creator_id=properties.get("creator_id"),
            created_at=format_timestamp(properties.get("created_at")),
            first_seen_at=format_timestamp(properties.get("first_seen_at")),
            last_seen_at=format_timestamp(properties.get("last_seen_at")),
            object_type=properties.get("object_type"),
            object_value=properties.get("object_value"),
            confidence=properties.get("confidence")
        )


@dataclass
class MapFeature:
    """Represents a map feature"""
    id: str
    geometry: Optional[Geometry] = None
    feature_type: Optional[str] = None
    feature_value: Optional[str] = None
    confidence: Optional[float] = None
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    images: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MapFeature':
        properties = data.get("properties", {})
        
        return cls(
            id=properties.get("id", ""),
            geometry=Geometry.from_dict(data.get("geometry", {})) if data.get("geometry") else None,
            feature_type=properties.get("feature_type"),
            feature_value=properties.get("feature_value"),
            confidence=properties.get("confidence"),
            first_seen_at=format_timestamp(properties.get("first_seen_at")),
            last_seen_at=format_timestamp(properties.get("last_seen_at")),
            images=properties.get("images", [])
        )


@dataclass
class Organization:
    """Represents an organization"""
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Organization':
        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            description=data.get("description"),
            created_at=format_timestamp(data.get("created_at"))
        )


@dataclass
class APIResponse:
    """Represents an API response"""
    data: List[Union[Image, Sequence, Detection, MapFeature, Organization]]
    total_count: int
    has_more: bool = False
    next_cursor: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], model_class) -> 'APIResponse':
        features = data.get("features", [])
        parsed_data = [model_class.from_dict(feature) for feature in features]
        
        return cls(
            data=parsed_data,
            total_count=data.get("total_count", len(parsed_data)),
            has_more=data.get("has_more", False),
            next_cursor=data.get("next_cursor"),
            metadata=data.get("metadata", {})
        )