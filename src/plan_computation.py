import typing as T
import math

import numpy as np

from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import compute_image_footprint_on_surface, compute_ground_sampling_distance,compute_image_footprint_on_surface_with_angle


def compute_distance_between_images(camera: Camera, dataset_spec: DatasetSpec) -> np.ndarray:
    """Compute the distance between images in the horizontal and vertical directions for specified overlap and sidelap.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        float: The distance between images in the horizontal direction.
        float: The distance between images in the vertical direction.
    """
    # Extract parameters from dataset_spec
    overlap = dataset_spec.overlap
    sidelap = dataset_spec.sidelap
    height = dataset_spec.height
    scan_dimension_x = dataset_spec.scan_dimension_x
    scan_dimension_y = dataset_spec.scan_dimension_y
    
    # Calculate the footprint of a single image at the given height
    footprint_width, footprint_height = compute_image_footprint_on_surface(camera, height)
    
    # Compute horizontal distance between consecutive images based on overlap
    distance_x = (1 - overlap) * footprint_width  # Distance between consecutive images along the x-axis
    
    # Compute vertical distance between consecutive rows based on sidelap
    distance_y = (1 - sidelap) * footprint_height  # Distance between adjacent rows of images
    
    return distance_x, distance_y

def compute_distance_between_images_with_angle(camera: Camera, dataset_spec: DatasetSpec) -> np.ndarray:
    # Extract parameters from dataset_spec
    overlap = dataset_spec.overlap
    sidelap = dataset_spec.sidelap 
    height = dataset_spec.height
    camera_angle = dataset_spec.camera_angle  # Camera tilt angle (degrees)
    
    # Compute the footprint size at the given height and tilt angle
    footprint_width, footprint_height = compute_image_footprint_on_surface_with_angle(camera, height, camera_angle)
    
    # Compute horizontal distance between consecutive images based on overlap
    distance_x = (1 - overlap) * footprint_width  # Distance between consecutive images along the x-axis
    
    # Compute vertical distance between consecutive rows based on sidelap
    distance_y = (1 - sidelap) * footprint_height  # Distance between adjacent rows of images
    
    return distance_x, distance_y

def compute_speed_during_photo_capture(camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1) -> float:
    """Compute the speed of drone during an active photo capture to prevent more than 1px of motion blur.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.
        allowed_movement_px (float, optional): The maximum allowed movement in pixels. Defaults to 1 px.

    Returns:
        float: The speed at which the drone should move during photo capture.
    """
    # Compute Ground Sampling Distance (GSD)
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    
    # Convert exposure time from milliseconds to seconds
    exposure_time_seconds = dataset_spec.exposure_time_ms / 1000.0
    
    # Compute the maximum allowable speed to avoid motion blur
    max_speed = gsd / exposure_time_seconds
    
    return max_speed


def generate_photo_plan_on_grid(camera: Camera, dataset_spec: DatasetSpec) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera (Camera): Camera model used for image capture.
        dataset_spec (DatasetSpec): user specification for the dataset.

    Returns:
        List[Waypoint]: scan plan as a list of waypoints.

    """
    waypoints = []

    # Step 1: Compute horizontal and vertical distances between images
    distance_horizontal, distance_vertical = compute_distance_between_images(camera, dataset_spec)

    # Step 2: Compute the number of images required to cover the scan area horizontally and vertically
    num_images_x = math.ceil(dataset_spec.scan_dimension_x / distance_horizontal)
    num_images_y = math.ceil(dataset_spec.scan_dimension_y / distance_vertical)

    # Step 3: Create waypoints for the photo grid
    # The grid will be arranged in a "snake-like" pattern to alternate between rows.
    for i in range(num_images_y):
        for j in range(num_images_x):
            # Determine the x, y, z position of the waypoint
            if(i%2==1):
                x_position = (num_images_x-j-1) * distance_horizontal #For backward transversal
            else:
                x_position = j*distance_horizontal #For forward transversal
            y_position = i * distance_vertical
            z_position = dataset_spec.height  # Assume the height is constant for all waypoints

            # For general case (non-nadir), adjust the camera angle and look_at point
            if dataset_spec.camera_angle != 0:
                # Here, you would compute the look_at point based on the camera angle
                # (This is a simplified version; full implementation would need trigonometry).
                look_at_point = (x_position, y_position, z_position - 100)  # Simplified for now
            else:
                look_at_point = (x_position, y_position, 0)

            # Compute the speed for the current waypoint
            speed = compute_speed_during_photo_capture(camera, dataset_spec)

            # Create the waypoint object
            waypoint = Waypoint(
                x=x_position,
                y=y_position,
                z=z_position,
                camera_angle=dataset_spec.camera_angle,
                look_at=look_at_point,
                speed=speed
            )

            # Add the waypoint to the list
            waypoints.append(waypoint)

    return waypoints
