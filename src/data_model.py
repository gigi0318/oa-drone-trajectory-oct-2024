"""Data models for the camera and user specification."""
from dataclasses import dataclass

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
    pass


@dataclass
class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """
    pass
