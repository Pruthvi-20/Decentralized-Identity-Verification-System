import cv2
import numpy as np

def capture_face():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("Look at the camera...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error")
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            print("Face detected!")
            cap.release()
            cv2.destroyAllWindows()
            return True

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

def authenticate_user():
    # Simulate biometric login
    return capture_face()  # Replace with password input if no webcam