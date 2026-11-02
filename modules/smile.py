from collections import deque


# Keep the last 10 smile scores
smile_history = deque(maxlen=10)


def detect_smile(face_landmarks):

    # --------------------------------------------------------
    # Important facial landmarks
    # --------------------------------------------------------

    # Mouth corners
    left_corner = face_landmarks.landmark[61]
    right_corner = face_landmarks.landmark[291]

    # Upper and lower lips
    upper_lip = face_landmarks.landmark[0]
    lower_lip = face_landmarks.landmark[17]

    # Left and right sides of face
    left_face = face_landmarks.landmark[234]
    right_face = face_landmarks.landmark[454]


    # --------------------------------------------------------
    # Calculate mouth width
    # --------------------------------------------------------

    mouth_width = abs(
        right_corner.x - left_corner.x
    )


    # --------------------------------------------------------
    # Calculate face width
    # --------------------------------------------------------

    face_width = abs(
        right_face.x - left_face.x
    )


    # Avoid division by zero
    if face_width < 0.001:

        return (
            "Unknown",
            (255, 255, 255),
            0
        )


    # --------------------------------------------------------
    # Normalize mouth width
    # --------------------------------------------------------

    width_ratio = (
        mouth_width / face_width
    )


    # --------------------------------------------------------
    # Calculate mouth corner position
    # --------------------------------------------------------

    corner_y = (
        left_corner.y +
        right_corner.y
    ) / 2


    # Mouth center
    mouth_center_y = (
        upper_lip.y +
        lower_lip.y
    ) / 2


    # --------------------------------------------------------
    # Calculate corner lift
    # --------------------------------------------------------

    corner_lift = (
        mouth_center_y -
        corner_y
    )


    normalized_lift = (
        corner_lift / face_width
    )


    # --------------------------------------------------------
    # Width component
    # --------------------------------------------------------

    width_component = (
        width_ratio - 0.32
    ) / 0.18


    # --------------------------------------------------------
    # Corner lift component
    # --------------------------------------------------------

    lift_component = (
        normalized_lift + 0.01
    ) / 0.06


    # Keep values between 0 and 1
    width_component = max(
        0.0,
        min(1.0, width_component)
    )

    lift_component = max(
        0.0,
        min(1.0, lift_component)
    )


    # --------------------------------------------------------
    # Calculate raw smile score
    # --------------------------------------------------------

    raw_score = (
        width_component * 0.55 +
        lift_component * 0.45
    )


    smile_score = int(
        raw_score * 100
    )


    # --------------------------------------------------------
    # Temporal smoothing
    # --------------------------------------------------------

    smile_history.append(
        smile_score
    )


    smooth_score = int(
        sum(smile_history) /
        len(smile_history)
    )


    # --------------------------------------------------------
    # Smile classification
    # --------------------------------------------------------

    if smooth_score >= 60:

        smile_status = "Yes"
        smile_color = (0, 255, 0)

    elif smooth_score >= 40:

        smile_status = "Slight"
        smile_color = (0, 255, 255)

    else:

        smile_status = "No"
        smile_color = (0, 0, 255)


    return (
        smile_status,
        smile_color,
        smooth_score
    )