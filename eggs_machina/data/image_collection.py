import cv2

# Initialize the camera
camera = cv2.VideoCapture(0)

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