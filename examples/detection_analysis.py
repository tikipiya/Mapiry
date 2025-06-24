"""
Detection and analysis examples for Mapiry SDK
"""

from mapiry import MapillaryClient
import json
from collections import defaultdict


# Initialize client
api_key = "YOUR_API_KEY_HERE"
client = MapillaryClient(api_key=api_key)


def analyze_traffic_signs():
    """Analyze traffic signs in an area"""
    print("=== Traffic Sign Analysis ===")
    
    try:
        # Get traffic signs around Central Park, NYC
        response = client.detections().traffic_signs().in_bbox(
            west=-73.9820, south=40.7640,
            east=-73.9490, north=40.8000
        ).min_confidence(0.7).limit(50).get()
        
        print(f"Found {len(response.data)} traffic signs")
        
        # Analyze by sign type
        sign_types = defaultdict(int)
        confidence_sum = defaultdict(float)
        
        for detection in response.data:
            sign_type = detection.object_value or "unknown"
            sign_types[sign_type] += 1
            confidence_sum[sign_type] += detection.confidence or 0
        
        print("\nTraffic sign distribution:")
        for sign_type, count in sorted(sign_types.items(), key=lambda x: x[1], reverse=True):
            avg_confidence = confidence_sum[sign_type] / count
            print(f"  {sign_type}: {count} signs (avg confidence: {avg_confidence:.2f})")
        
    except Exception as e:
        print(f"Error: {e}")


def detect_objects_along_route():
    """Detect objects along a sequence route"""
    print("=== Object Detection Along Route ===")
    
    try:
        # First find a sequence
        sequences = client.sequences().close_to(
            longitude=-73.9857, latitude=40.7484,  # Times Square
            radius=500
        ).min_images(15).limit(1).get()
        
        if not sequences.data:
            print("No sequences found")
            return
        
        sequence_id = sequences.data[0].id
        print(f"Analyzing sequence: {sequence_id}")
        
        # Get all detections for this sequence
        detections = client.detections().by_sequence(sequence_id).limit(100).get()
        
        print(f"Found {len(detections.data)} detections in sequence")
        
        # Group by object type
        objects = defaultdict(list)
        for detection in detections.data:
            obj_type = detection.object_type or "unknown"
            objects[obj_type].append(detection)
        
        print("\nObjects detected along route:")
        for obj_type, obj_list in objects.items():
            print(f"  {obj_type}: {len(obj_list)} detections")
            
            # Show high-confidence detections
            high_conf = [d for d in obj_list if (d.confidence or 0) > 0.8]
            if high_conf:
                print(f"    High confidence ({len(high_conf)}):")
                for detection in high_conf[:3]:  # Show first 3
                    print(f"      - {detection.object_value} ({detection.confidence:.2f})")
        
    except Exception as e:
        print(f"Error: {e}")


def map_street_furniture():
    """Map street furniture in an area"""
    print("=== Street Furniture Mapping ===")
    
    try:
        # Define area around downtown area
        bbox_coords = {
            "west": -73.9900, "south": 40.7500,
            "east": -73.9700, "north": 40.7600
        }
        
        # Get various types of street furniture
        furniture_types = ["pole", "fire_hydrant", "bench", "mailbox"]
        
        all_detections = []
        for furniture_type in furniture_types:
            try:
                response = client.detections().object_value(furniture_type).in_bbox(
                    **bbox_coords
                ).min_confidence(0.6).limit(20).get()
                
                all_detections.extend(response.data)
                print(f"Found {len(response.data)} {furniture_type}s")
                
            except Exception as e:
                print(f"Error getting {furniture_type}: {e}")
        
        print(f"\nTotal street furniture detected: {len(all_detections)}")
        
        # Create a simple map of locations
        locations = []
        for detection in all_detections:
            if detection.geometry and detection.geometry.coordinates:
                coords = detection.geometry.coordinates
                locations.append({
                    "type": detection.object_value,
                    "confidence": detection.confidence,
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "latitude": coords[1] if len(coords) > 1 else None
                })
        
        # Save to JSON file
        with open("street_furniture_map.json", "w") as f:
            json.dump(locations, f, indent=2, default=str)
        
        print("Saved street furniture map to 'street_furniture_map.json'")
        
    except Exception as e:
        print(f"Error: {e}")


def analyze_detection_quality():
    """Analyze detection quality and confidence"""
    print("=== Detection Quality Analysis ===")
    
    try:
        # Get various detections
        response = client.detections().close_to(
            longitude=2.3522, latitude=48.8566,  # Paris
            radius=1000
        ).limit(100).get()
        
        print(f"Analyzing {len(response.data)} detections")
        
        # Confidence distribution
        confidence_ranges = {
            "Very High (0.9-1.0)": 0,
            "High (0.8-0.9)": 0,
            "Medium (0.6-0.8)": 0,
            "Low (0.4-0.6)": 0,
            "Very Low (0.0-0.4)": 0
        }
        
        for detection in response.data:
            conf = detection.confidence or 0
            if conf >= 0.9:
                confidence_ranges["Very High (0.9-1.0)"] += 1
            elif conf >= 0.8:
                confidence_ranges["High (0.8-0.9)"] += 1
            elif conf >= 0.6:
                confidence_ranges["Medium (0.6-0.8)"] += 1
            elif conf >= 0.4:
                confidence_ranges["Low (0.4-0.6)"] += 1
            else:
                confidence_ranges["Very Low (0.0-0.4)"] += 1
        
        print("\nConfidence distribution:")
        for range_name, count in confidence_ranges.items():
            percentage = (count / len(response.data)) * 100
            print(f"  {range_name}: {count} ({percentage:.1f}%)")
        
        # Most confident detections
        sorted_detections = sorted(
            response.data, 
            key=lambda d: d.confidence or 0, 
            reverse=True
        )
        
        print("\nTop 5 most confident detections:")
        for i, detection in enumerate(sorted_detections[:5]):
            print(f"  {i+1}. {detection.object_type}: {detection.object_value} "
                  f"({detection.confidence:.3f})")
        
    except Exception as e:
        print(f"Error: {e}")


def get_vector_tiles():
    """Example of getting vector tiles"""
    print("=== Vector Tiles Example ===")
    
    try:
        # Get a tile for Manhattan
        # Zoom level 14, tile coordinates for Manhattan area
        tile_data = client.vector_tiles().get_image_tiles(
            z=14, x=4823, y=6160
        )
        
        print(f"Retrieved vector tile: {len(tile_data)} bytes")
        
        # Save tile to file
        with open("manhattan_images_tile.mvt", "wb") as f:
            f.write(tile_data)
        
        print("Saved tile to 'manhattan_images_tile.mvt'")
        
        # Get tile bounds
        bounds = client.vector_tiles().get_tile_bounds(14, 4823, 6160)
        print(f"Tile bounds: {bounds}")
        
        # Get traffic sign tiles
        traffic_tile = client.vector_tiles().get_traffic_sign_tiles(
            z=14, x=4823, y=6160
        )
        
        print(f"Traffic sign tile: {len(traffic_tile)} bytes")
        
    except Exception as e:
        print(f"Error: {e}")


def comprehensive_area_analysis():
    """Comprehensive analysis of an area"""
    print("=== Comprehensive Area Analysis ===")
    
    # Define area (small section of Manhattan)
    area = {
        "name": "Times Square Area",
        "west": -73.9900, "south": 40.7550,
        "east": -73.9800, "north": 40.7600
    }
    
    print(f"Analyzing: {area['name']}")
    
    try:
        # Get images
        images = client.images().in_bbox(**{k: v for k, v in area.items() if k != "name"}).limit(50).get()
        print(f"Images: {len(images.data)}")
        
        # Analyze image types
        pano_count = sum(1 for img in images.data if img.is_pano)
        print(f"  Panoramic: {pano_count}")
        print(f"  Flat: {len(images.data) - pano_count}")
        
        # Get sequences
        sequences = client.sequences().in_bbox(**{k: v for k, v in area.items() if k != "name"}).limit(20).get()
        print(f"Sequences: {len(sequences.data)}")
        
        # Get detections
        detections = client.detections().in_bbox(**{k: v for k, v in area.items() if k != "name"}).limit(100).get()
        print(f"Detections: {len(detections.data)}")
        
        # Analyze detection types
        detection_types = defaultdict(int)
        for detection in detections.data:
            det_type = detection.object_type or "unknown"
            detection_types[det_type] += 1
        
        print("Detection breakdown:")
        for det_type, count in sorted(detection_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {det_type}: {count}")
        
        # Summary report
        report = {
            "area": area,
            "summary": {
                "total_images": len(images.data),
                "panoramic_images": pano_count,
                "flat_images": len(images.data) - pano_count,
                "total_sequences": len(sequences.data),
                "total_detections": len(detections.data),
                "detection_types": dict(detection_types)
            }
        }
        
        # Save report
        with open("area_analysis_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        print("\nSaved comprehensive report to 'area_analysis_report.json'")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Mapiry SDK - Detection and Analysis Examples")
    print("=" * 50)
    
    # Replace with your actual API key
    if api_key == "YOUR_API_KEY_HERE":
        print("Please set your API key in the script!")
        exit(1)
    
    # Run examples
    analyze_traffic_signs()
    detect_objects_along_route()
    map_street_furniture()
    analyze_detection_quality()
    get_vector_tiles()
    comprehensive_area_analysis()
    
    print("Detection analysis examples completed!")