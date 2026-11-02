import cv2

def estimate_head_pose(frame, face_landmarks):

    h, w, _ = frame.shape

    # Nose
    nose = face_landmarks.landmark[1]

    # Left and Right Face
    left = face_landmarks.landmark[234]
    right = face_landmarks.landmark[454]

    nose_x = nose.x * w

    left_x = left.x * w
    right_x = right.x * w

    center = (left_x + right_x) / 2

    difference = nose_x - center

    if difference < -20:
        direction = "Left"
        color = (0, 0, 255)

    elif difference > 20:
        direction = "Right"
        color = (0, 0, 255)

    else:
        direction = "Straight"
        color = (0, 255, 0)

    return direction, color