from typing import Any, Dict
import cv2
from cv2.typing import NumPyArrayNumeric
from numpy import dtype, floating, integer
from numpy.typing import NDArray
import time

class CameraNotOpenedError(Exception):
    """Raised when the camera could not be opened."""
    pass


class FrameNotReadError(Exception):
    """Raised when the frame could not be read from a camera."""
    pass


class ImageCollector:
    
    def __init__(self, camera_names: Dict[str, int]):
        self.camera_names = camera_names
        self.cameras: Dict[str, cv2.VideoCapture] = {}
    

    def start_cameras(self):
        """
        Start cameras specified in the camera_names dictionary.
        """
        for camera_name, camera_index in self.camera_names.items():
            camera = cv2.VideoCapture(camera_index)
            if not camera.isOpened():
                raise CameraNotOpenedError("Error: Could not open camera.")
            self.cameras[camera_name] = camera


    def get_images(self) -> Dict[Any, Any]:
        """
        Return images from all cameras.

        :returns images: Keys are camera names, values are image data.
        """
        images = {}
        for camera_name, camera in self.cameras.items():
            images[camera_name] = self._get_image(camera)
        return images
        

    def _get_image(self, camera: cv2.VideoCapture) -> NDArray[Any]:
        # Read a single frame from the camera
        ret, frame = camera.read()

        # Check if frame is read correctly
        if not ret:
            raise FrameNotReadError("Error: Could not read frame.")

        return frame
    
    
    def close_cameras(self):
        """Close all cameras."""
        for camera in self.cameras.values():
            camera.release()
        self.cameras.clear()
        cv2.destroyAllWindows()


def get_image_from_camera():
    cam = cv2.VideoCapture(4)  # 0 usually refers to the default camera
    # Read a frame from the camera
    result, image = cam.read()
    if result:
        return image
    else:
        print("Error: Could not capture image from camera.")


def display_image(image):
    cv2.imshow("Camera Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    # image = get_image_from_camera()
    # display_image(image)
    image_collector = ImageCollector({"main_cam": 4})
    image_collector.start_cameras()
    images = image_collector.get_images()
    for camera_name, image in images.items():
        display_image(image) 
    time.sleep(5)
    image_collector.close_cameras()