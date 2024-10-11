import threading
import cv2 
from deepface import DeepFace
import os

# Check if the reference image exists
reference_path = "reference.jpg"
if not os.path.exists(reference_path):
    print(f"Error: Reference image '{reference_path}' not found.")
    exit(1)

# Load the reference image
reference_img = cv2.imread(reference_path)
if reference_img is None:
    print(f"Error: Unable to load reference image '{reference_path}'.")
    exit(1)

# Initialize video capture with the default webcam
cap = cv2.VideoCapture(2)  # Use 0 for the default webcam

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit(1)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False

def check_face(frame):
    global face_match
    try:
        result = DeepFace.verify(frame, reference_img.copy())
        face_match = result['verified']
    except ValueError as e:
        print(f"Face verification error: {e}")
        face_match = False
    except Exception as e:
        print(f"Unexpected error in face verification: {e}")
        face_match = False

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    if counter % 30 == 0:  # Check every 30 frames
        try:
            threading.Thread(target=check_face, args=(frame.copy(),), daemon=True).start()
        except Exception as e:
            print(f"Error starting face check thread: {e}")

    counter += 1

    # Display result
    color = (0, 255, 0) if face_match else (0, 0, 255)
    text = "MATCH!" if face_match else "NO MATCH!"
    cv2.putText(frame, text, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

    cv2.imshow("video", frame)

    # Check for 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
