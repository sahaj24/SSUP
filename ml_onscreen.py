import cv2
from ultralytics import YOLO
import pyautogui
import numpy as np

# Load your custom trained YOLOv8 model
model_path = "E:\\ssup\\Trained.pt"  # Path to your trained model
model = YOLO(model_path)

# Define the class ID for crack detection
crack_class_id = 0  # Update this based on your training data's class ID for cracks

# Define the region of interest for screen capture (x, y, width, height)
region = (100, 100, 800, 600)  # Adjust coordinates as needed

def detect_cracks_on_screen():
    while True:
        # Capture a specific region of the screen
        screenshot = pyautogui.screenshot(region=region)

        # Convert screenshot to a numpy array (compatible with OpenCV)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Perform inference on the captured screen
        results = model(frame)

        # Extract bounding boxes and class IDs
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])  # Class ID

            if class_id == crack_class_id:
                # Draw a bounding box around the crack
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red box
                cv2.putText(frame, f'Crack: {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the captured region with detections
        cv2.imshow('Crack Detection on Region', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV window
    cv2.destroyAllWindows()

# Run crack detection on the defined screen region
detect_cracks_on_screen()
