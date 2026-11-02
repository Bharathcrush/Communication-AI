import mediapipe as mp


mp_pose = mp.solutions.pose

pose_detector = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def detect_posture(frame, rgb):

    results = pose_detector.process(rgb)

    # Default values
    posture_status = "Unknown"
    posture_color = (255, 255, 255)
    posture_score = 0

    if not results.pose_landmarks:
        return posture_status, posture_color, posture_score

    landmarks = results.pose_landmarks.landmark

    # --------------------------------
    # Shoulder landmarks
    # --------------------------------

    left_shoulder = landmarks[
        mp_pose.PoseLandmark.LEFT_SHOULDER.value
    ]

    right_shoulder = landmarks[
        mp_pose.PoseLandmark.RIGHT_SHOULDER.value
    ]

    # --------------------------------
    # Shoulder alignment
    # --------------------------------

    shoulder_difference = abs(
        left_shoulder.y - right_shoulder.y
    )

    # --------------------------------
    # Calculate posture score
    # --------------------------------

    if shoulder_difference < 0.025:

        posture_status = "Good"
        posture_color = (0, 255, 0)
        posture_score = 100

    elif shoulder_difference < 0.060:

        posture_status = "Average"
        posture_color = (0, 255, 255)
        posture_score = 70

    else:

        posture_status = "Poor"
        posture_color = (0, 0, 255)
        posture_score = 40

    return (
        posture_status,
        posture_color,
        posture_score
    )