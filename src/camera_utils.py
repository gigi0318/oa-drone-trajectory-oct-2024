"""Utility functions for the camera model.
"""
import numpy as np

from src.data_model import Camera

def compute_focal_length_in_mm(camera: Camera) -> np.ndarray:
    """Computes the focal length in mm for the given camera

    Args:
        camera (Camera): the camera model.

    Returns:
        np.ndarray: [fx, fy] in mm.
    """
    raise NotImplementedError() 
    # Note(Ayush): Solution provided by project leader.
    # pixel_to_mm_x = camera.sensor_size_x_mm / camera.image_size_x_px
    # pixel_to_mm_y = camera.sensor_size_y_mm / camera.image_size_y_px

    # return np.array([camera.fx * pixel_to_mm_x, camera.fy * pixel_to_mm_y])

def project_world_point_to_image(camera: Camera, point: np.ndarray) -> np.ndarray:
    """Project a 3D world point into the image coordinates.

    Args:
        camera (Camera): the camera model
        point (np.ndarray): the 3D world point

    Returns:
        np.ndarray: [u, v] pixel coordinates corresponding to the point.
    """
    X,Y,Z=point
    x = camera.fx * (X / Z)
    y = camera.fy * (Y / Z)
    u = x + camera.cx
    v = y + camera.cy

    return np.array([u, v], dtype=np.float32)



def compute_image_footprint_on_surface(camera: Camera, distance_from_surface: float) -> np.ndarray:
    """Compute the footprint of the image captured by the camera at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).

    Returns:
        np.ndarray: [footprint_x, footprint_y] in meters.
    """
    # Image corners in pixel coordinates
    corners = np.array([
        [0, 0],
        [camera.image_size_x, 0],
        [camera.image_size_x, camera.image_size_y],
        [0, camera.image_size_y]
    ])

    # Reproject corners to world coordinates
    world_coords = []
    for u, v in corners:
        X = (u - camera.cx) * distance_from_surface / camera.fx
        Y = (v - camera.cy) * distance_from_surface / camera.fy
        world_coords.append((X, Y))
    # Convert to numpy array for easier manipulation
    world_coords = np.array(world_coords)

    # Calculate width and height of the footprint
    width = np.abs(world_coords[1][0] - world_coords[0][0])  # right - left
    height = np.abs(world_coords[3][1] - world_coords[0][1])  # top - bottom

    return np.array([width, height], dtype=np.float32)



def compute_ground_sampling_distance(camera: Camera, distance_from_surface: float) -> float:
    """Compute the ground sampling distance (GSD) at a given distance from the surface.

    Args:
        camera (Camera): the camera model.
        distance_from_surface (float): distance from the surface (in m).
    
    Returns:
        float: the GSD in meters (smaller among x and y directions).
    """
    
    # Compute the footprint dimensions at distance Z
    footprint = compute_image_footprint_on_surface(camera, distance_from_surface)
    
    # Calculate GSD
    gsd_x = footprint[0] / camera.image_size_x  # width GSD
    gsd_y = footprint[1] / camera.image_size_y  # height GSD
    
    # You can choose to return either or average
    return (gsd_x + gsd_y) / 2
~1


def reproject_image_point_to_world(camera: Camera, pixel: np.ndarray, Z: float) -> np.ndarray:
    """
    Reproject a 2D image point back to a 3D world point at a specified depth Z.

    Parameters:
    - camera: An instance of the Camera class containing camera parameters.
    - pixel: A 2D pixel location as a numpy array (u, v).
    - Z: The depth at which to reproject (in the same units as camera parameters).

    Returns:
    - 3D world coordinates as a numpy array (X, Y, Z).
    """
    if pixel.shape != (2,):
        raise ValueError("Pixel must be a 2D coordinate array (u, v).")

    u, v = pixel

    # Apply the reprojection equations
    X = (u - camera.cx) * Z / camera.fx
    Y = (v - camera.cy) * Z / camera.fy
    return np.array([X, Y, Z], dtype=np.float32)

