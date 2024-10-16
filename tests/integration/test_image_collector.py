import pytest
from eggs_machina.data.image_collection import ImageCollector, CameraNotOpenedError 
import cv2
from numpy import dtype, ndarray


def test_start_cameras():
    """Test that cameras are started correctly."""
    camera_names = {"cam1": 0}  # Assuming camera index 0 is valid
    collector = ImageCollector(camera_names)
    collector.start_cameras()
    assert len(collector.cameras) == 1
    assert isinstance(collector.cameras["cam1"], cv2.VideoCapture)

def test_get_images():
    """
    Integration test for get_images. 
    Assumes a camera is available at index 0.
    """
    camera_names = {"cam1": 0}
    collector = ImageCollector(camera_names)
    collector.start_cameras()

    images = collector.get_images()
    assert len(images) == 1
    assert "cam1" in images
    assert isinstance(images["cam1"], ndarray)  # Check if it's a NumPy array
    assert images["cam1"].dtype == dtype('uint8')  # Check the data type


def test_close_cameras():
    """
    Integration test for close_cameras.
    Assumes a camera is available at index 0.
    """
    camera_names = {"cam1": 0}
    collector = ImageCollector(camera_names)
    collector.start_cameras()
    collector.close_cameras()

