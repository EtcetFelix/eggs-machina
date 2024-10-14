from typing import Any, Dict
import cv2
from cv2.typing import NumPyArrayNumeric
from numpy import dtype, floating, integer
from numpy.typing import NDArray

def get_images() -> Dict[Any, Any]:
    """
    Return images from all cameras.

    :returns images: Keys are camera names, values are image data.
    """
    cameras = {"test_cam_name": 0}
    images = {}
    for camera_name, camera_index in cameras.items():
        images[camera_name] = get_image(camera_index)
    return images
    
def get_image(camera_index: int) -> NDArray[Any]:
    # Initialize the camera
    camera = cv2.VideoCapture(camera_index)

    # Check if the camera opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        exit()   

    # Read a single frame from the camera
    ret, frame = camera.read()

    # Check if frame is read correctly
    if not ret:
        print("Error: Could not read frame.")
        exit()

    # Display the captured frame
    cv2.imshow('Camera Image', frame)
    cv2.waitKey(0)  # Wait indefinitely for a key press

    # Release the camera and destroy all windows
    camera.release()
    cv2.destroyAllWindows()
    return frame