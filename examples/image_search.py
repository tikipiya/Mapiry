"""
Advanced image search examples for Mapiry SDK
"""

from mapiry import MapillaryClient
import json
from datetime import datetime


# Initialize client
api_key = "YOUR_API_KEY_HERE"
client = MapillaryClient(api_key=api_key)


def search_panoramic_images():
    """Search for panoramic images in a specific area"""
    print("=== Searching for panoramic images ===")
    
    try:
        response = client.images().in_bbox(
            west=-74.0100, south=40.7400, 
            east=-73.9800, north=40.7600
        ).panoramic_only().captured_after("2022-01-01").limit(10).get()
        
        print(f"Found {len(response.data)} panoramic images")
        
        for image in response.data:
            print(f"Image: {image.id}")
            print(f"  Captured: {image.captured_at}")
            print(f"  Compass angle: {image.compass_angle}°")
            if image.thumb_1024_url:
                print(f"  Thumbnail: {image.thumb_1024_url}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def search_by_camera_type():
    """Search images by specific camera make/model"""
    print("=== Searching by camera type ===")
    
    try:
        # Search for iPhone images
        response = client.images().close_to(
            longitude=-73.9857, latitude=40.7484,  # Times Square
            radius=1000
        ).camera_make("Apple").limit(5).get()
        
        print(f"Found {len(response.data)} iPhone images")
        
        for image in response.data:
            print(f"Image: {image.id}")
            print(f"  Camera: {image.camera_make} {image.camera_model}")
            print(f"  Captured: {image.captured_at}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def search_by_compass_direction():
    """Search images facing specific direction"""
    print("=== Searching by compass direction ===")
    
    try:
        # Search for images facing north (315° to 45°)
        response = client.images().close_to(
            longitude=2.3522, latitude=48.8566,  # Paris
            radius=500
        ).compass_angle((315, 45)).limit(5).get()
        
        print(f"Found {len(response.data)} north-facing images")
        
        for image in response.data:
            print(f"Image: {image.id}")
            print(f"  Compass angle: {image.compass_angle}°")
            print(f"  Captured: {image.captured_at}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def search_sequence_images():
    """Search images from specific sequences"""
    print("=== Searching sequence images ===")
    
    try:
        # First find sequences in the area
        sequences = client.sequences().close_to(
            longitude=13.4050, latitude=52.5200,  # Berlin
            radius=1000
        ).min_images(20).limit(2).get()
        
        if sequences.data:
            sequence_id = sequences.data[0].id
            print(f"Found sequence: {sequence_id}")
            
            # Get images from this sequence
            images = client.sequences().get_images(
                sequence_id, 
                fields=["id", "captured_at", "compass_angle"],
                limit=10
            )
            
            print(f"Sequence has {len(images.data)} images (showing first 10):")
            for i, image in enumerate(images.data):
                print(f"  {i+1}. {image.id} - {image.captured_at}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def search_by_organization():
    """Search images from specific organization"""
    print("=== Searching by organization ===")
    
    try:
        # Note: You would need to know actual organization IDs
        # This is just an example of the API usage
        org_id = "123456"  # Example organization ID
        
        response = client.images().by_organization(org_id).close_to(
            longitude=0.1278, latitude=51.5074,  # London
            radius=2000
        ).limit(5).get()
        
        print(f"Found {len(response.data)} images from organization {org_id}")
        
        for image in response.data:
            print(f"Image: {image.id}")
            print(f"  Organization: {image.organization_id}")
            print(f"  Creator: {image.creator_username}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def download_images():
    """Example of downloading image thumbnails"""
    print("=== Downloading image thumbnails ===")
    
    try:
        # Get a few images
        response = client.images().close_to(
            longitude=139.6917, latitude=35.6895,  # Tokyo
            radius=100
        ).limit(3).get()
        
        print(f"Downloading {len(response.data)} image thumbnails...")
        
        for i, image in enumerate(response.data):
            try:
                # Download 1024px thumbnail
                image_data = client.images().download_image(
                    image.id, 
                    size="thumb_1024_url"
                )
                
                # Save to file
                filename = f"image_{image.id}_{i+1}.jpg"
                with open(filename, "wb") as f:
                    f.write(image_data)
                
                print(f"  Saved: {filename} ({len(image_data)} bytes)")
                
            except Exception as e:
                print(f"  Failed to download {image.id}: {e}")
        
    except Exception as e:
        print(f"Error: {e}")


def advanced_filtering():
    """Example of advanced filtering combinations"""
    print("=== Advanced filtering ===")
    
    try:
        response = (client.images()
                   .in_bbox(west=-122.4194, south=37.7749,  # San Francisco
                           east=-122.4094, north=37.7849)
                   .image_type("both")
                   .captured_between("2023-06-01", "2023-08-31")  # Summer 2023
                   .compass_angle((270, 360))  # Facing west to north
                   .fields("id", "captured_at", "compass_angle", "is_pano", 
                          "camera_make", "creator_username")
                   .limit(15)
                   .get())
        
        print(f"Found {len(response.data)} images matching all criteria")
        
        # Analyze results
        pano_count = sum(1 for img in response.data if img.is_pano)
        print(f"  Panoramic: {pano_count}")
        print(f"  Flat: {len(response.data) - pano_count}")
        
        # Group by camera make
        cameras = {}
        for image in response.data:
            make = image.camera_make or "Unknown"
            cameras[make] = cameras.get(make, 0) + 1
        
        print("  Camera distribution:")
        for make, count in cameras.items():
            print(f"    {make}: {count}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Mapiry SDK - Advanced Image Search Examples")
    print("=" * 50)
    
    # Replace with your actual API key
    if api_key == "YOUR_API_KEY_HERE":
        print("Please set your API key in the script!")
        exit(1)
    
    # Run examples
    search_panoramic_images()
    search_by_camera_type()
    search_by_compass_direction()
    search_sequence_images()
    search_by_organization()
    download_images()
    advanced_filtering()
    
    print("Advanced examples completed!")