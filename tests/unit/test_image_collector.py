import pytest
from eggs_machina.data.image_collection import ImageCollector, CameraNotOpenedError 


def test_instantiation():
    """Test that the ImageCollector can be instantiated."""
    camera_names = {"cam1": 0, "cam2": 1}
    collector = ImageCollector(camera_names)
    assert collector.camera_names == camera_names
    assert collector.cameras == {}


def test_start_cameras_invalid_index():
    """Test that an exception is raised for an invalid camera index."""
    camera_names = {"cam1": 100}  # Assuming 100 is an invalid camera index
    collector = ImageCollector(camera_names)
    with pytest.raises(CameraNotOpenedError):
        collector.start_cameras()

