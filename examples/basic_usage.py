"""
Basic usage examples for Mapiry SDK
"""

from mapiry import MapillaryClient

# Initialize client with your API key
api_key = "YOUR_API_KEY_HERE"
client = MapillaryClient(api_key=api_key)


def example_get_images_near_location():
    """Example: Get images near a specific location"""
    print("=== Getting images near Tokyo ===")
    
    # Get images within 100 meters of Tokyo Station
    try:
        response = client.images().close_to(
            longitude=139.7673068,
            latitude=35.6809591,
            radius=100
        ).limit(5).get()
        
        print(f"Found {len(response.data)} images")
        for image in response.data:
            print(f"- Image ID: {image.id}")
            print(f"  Captured at: {image.captured_at}")
            print(f"  Compass angle: {image.compass_angle}")
            print(f"  Is panoramic: {image.is_pano}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


def example_get_images_in_area():
    """Example: Get images in a bounding box"""
    print("=== Getting images in Manhattan ===")
    
    # Define bounding box for part of Manhattan
    west = -74.0059
    south = 40.7589
    east = -74.0000
    north = 40.7614
    
    try:
        response = client.images().in_bbox(
            west=west, south=south, east=east, north=north
        ).image_type("flat").limit(10).get()
        
        print(f"Found {len(response.data)} flat images in the area")
        for image in response.data:
            print(f"- Image ID: {image.id}")
            print(f"  Creator: {image.creator_username}")
            if image.camera_make:
                print(f"  Camera: {image.camera_make} {image.camera_model}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


def example_get_traffic_signs():
    """Example: Get traffic sign detections"""
    print("=== Getting traffic sign detections ===")
    
    try:
        response = client.detections().traffic_signs().close_to(
            longitude=139.7673068,
            latitude=35.6809591,
            radius=500
        ).min_confidence(0.8).limit(5).get()
        
        print(f"Found {len(response.data)} traffic signs")
        for detection in response.data:
            print(f"- Detection ID: {detection.id}")
            print(f"  Object type: {detection.object_type}")
            print(f"  Object value: {detection.object_value}")
            print(f"  Confidence: {detection.confidence}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


def example_get_sequences():
    """Example: Get image sequences"""
    print("=== Getting image sequences ===")
    
    try:
        response = client.sequences().close_to(
            longitude=139.7673068,
            latitude=35.6809591,
            radius=1000
        ).min_images(10).limit(3).get()
        
        print(f"Found {len(response.data)} sequences")
        for sequence in response.data:
            print(f"- Sequence ID: {sequence.id}")
            print(f"  Image count: {sequence.image_count}")
            print(f"  Creator: {sequence.creator_username}")
            print(f"  Created at: {sequence.created_at}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


def example_get_image_by_id():
    """Example: Get specific image by ID"""
    print("=== Getting specific image ===")
    
    # First get an image ID from search
    try:
        search_response = client.images().close_to(
            longitude=139.7673068,
            latitude=35.6809591
        ).limit(1).get()
        
        if search_response.data:
            image_id = search_response.data[0].id
            
            # Get full image details
            image = client.images().get_by_id(
                image_id,
                fields=["all"]
            )
            
            print(f"Image ID: {image.id}")
            print(f"Captured at: {image.captured_at}")
            print(f"Camera: {image.camera_make} {image.camera_model}")
            print(f"Dimensions: {image.width}x{image.height}")
            print(f"Sequence ID: {image.sequence_id}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


def example_filter_by_date():
    """Example: Filter images by date range"""
    print("=== Getting recent images ===")
    
    try:
        response = client.images().close_to(
            longitude=139.7673068,
            latitude=35.6809591,
            radius=2000
        ).captured_between(
            start_date="2023-01-01",
            end_date="2024-01-01"
        ).limit(5).get()
        
        print(f"Found {len(response.data)} images from 2023")
        for image in response.data:
            print(f"- Image ID: {image.id}")
            print(f"  Captured: {image.captured_at}")
            print()
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Mapiry SDK - Basic Usage Examples")
    print("=" * 40)
    
    # Replace with your actual API key
    if api_key == "YOUR_API_KEY_HERE":
        print("Please set your API key in the script!")
        exit(1)
    
    # Run examples
    example_get_images_near_location()
    example_get_images_in_area()
    example_get_traffic_signs()
    example_get_sequences()
    example_get_image_by_id()
    example_filter_by_date()
    
    print("Examples completed!")