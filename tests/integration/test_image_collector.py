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



def test_close_cameras():
    """
    Integration test for close_cameras.
    Assumes a camera is available at index 0.
    """
    camera_names = {"cam1": 0}
    collector = ImageCollector(camera_names)
    collector.start_cameras()
    collector.close_cameras()

