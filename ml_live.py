import cv2
from ultralytics import YOLO

# Load your custom trained YOLOv8 model
model_path = "E:\\ssup\\Trained.pt"  # Path to your trained model
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Define the class ID for crack detection
crack_class_id = 0  # Update this based on your training data's class ID for cracks

def detect_cracks_from_webcam():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Resize frame for faster processing (optional)
        resized_frame = cv2.resize(frame, (640, 640))

        # Perform inference on the current frame
        results = model(resized_frame)

        # Extract bounding boxes and class IDs
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])  # Class ID

            if class_id == crack_class_id:
                # Draw a bounding box around the crack
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'Crack: {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the frame with the detections
        cv2.imshow('Crack Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the crack detection function
detect_cracks_from_webcam()