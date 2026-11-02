import cv2

def calculate_eye_contact(frame, face_landmarks):

    h, w, _ = frame.shape

    # Iris landmarks
    left_iris = face_landmarks.landmark[468]
    right_iris = face_landmarks.landmark[473]

    lx = int(left_iris.x * w)
    ly = int(left_iris.y * h)

    rx = int(right_iris.x * w)
    ry = int(right_iris.y * h)

    # Draw iris points
    cv2.circle(frame, (lx, ly), 3, (0,255,0), -1)
    cv2.circle(frame, (rx, ry), 3, (0,255,0), -1)

    # Simple eye-contact estimation
    center = (lx + rx) / 2
    screen_center = w / 2

    distance = abs(center - screen_center)

    eye_contact = max(0, 100 - int(distance / 3))

    eye_contact = min(100, eye_contact)

    return eye_contact, frame