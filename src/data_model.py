"""Data models for the camera and user specification."""
from dataclasses import dataclass
from typing import Optional, Tuple
@dataclass
class Camera:
    """
    Data model for a simple pinhole camera.
    
    References: 
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """
    fx: float # Focal length along the x axis (in pixels)
    fy: float # Focal length along the y axis (in pixels)
    cx: float # Optical center of the image along the x axis (in pixels)
    cy: float # Optical center of the image along the y axis (in pixels)
    sensor_size_x_mm: float # Size of the sensor along the x axis (in mm)
    sensor_size_y_mm: float # Size of the sensor along the y axis (in mm)
    image_size_x: int # Number of pixels in the image along the x axis
    image_size_y: int # Number of pixels in the image along the y axis

    def __repr__(self):
        return (f"Camera(fx={self.fx}, fy={self.fy}, cx={self.cx}, cy={self.cy}, "
    f"sensor_size_x_mm={self.sensor_size_x_mm}, "
    f"sensor_size_y_mm={self.sensor_size_y_mm}, "
    f"image_size_x={self.image_size_x}, image_size_y={self.image_size_y})")

@dataclass
class DatasetSpec:
    """
    Data model for specifications of an image dataset.
    """
    overlap: float  # Ratio of scene shared between two consecutive images (0 to 1)
    sidelap: float  # Ratio of scene shared between two images in adjacent rows (0 to 1)
    height: float   # Height of the scan above the ground (in meters)
    scan_dimension_x: float  # Horizontal size of the rectangle to be scanned (in meters)
    scan_dimension_y: float  # Vertical size of the rectangle to be scanned (in meters)
    exposure_time_ms: int    # Exposure time for each image (in milliseconds)
    camera_angle: float  # Camera tilt angle (degrees)

    def __repr__(self):
        return (f"DatasetSpec(overlap={self.overlap}, sidelap={self.sidelap}, height={self.height}, scan_dimension_x={self.scan_dimension_x},scan_dimension_y={self.scan_dimension_y},exposure_time_ms={self.exposure_time_ms},camera_angle={self.camera_angle} ")


@dataclass
class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """
    x: float  # x position in meters
    y: float  # y position in meters
    z: float  # z position (altitude) in meters
    camera_angle: Optional[float] = 0.0  # camera angle relative to the nadir, in degrees (default: 0 for nadir)
    look_at: Optional[Tuple[float, float, float]] = None  # the point the camera is looking at (x, y, z)
    speed: float = 0.0  # speed at this waypoint (in meters per second)
    timestamp: Optional[float] = None  # time of the image capture (in seconds, optional)
