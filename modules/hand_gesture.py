import mediapipe as mp


# ============================================================
# INITIALIZE MEDIAPIPE HANDS
# ============================================================

mp_hands = mp.solutions.hands

hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# ============================================================
# HAND GESTURE DETECTION
# ============================================================

def detect_hand_gesture(frame, rgb):

    results = hands_detector.process(rgb)

    hand_count = 0
    gesture_status = "No Hands"
    gesture_color = (0, 0, 255)
    gesture_score = 0

    # --------------------------------------------------------
    # Check whether hands are detected
    # --------------------------------------------------------

    if results.multi_hand_landmarks:

        hand_count = len(
            results.multi_hand_landmarks
        )

        # ----------------------------------------------------
        # One Hand
        # ----------------------------------------------------

        if hand_count == 1:

            gesture_status = "One Hand"
            gesture_color = (0, 255, 255)
            gesture_score = 70

        # ----------------------------------------------------
        # Two Hands
        # ----------------------------------------------------

        elif hand_count >= 2:

            gesture_status = "Two Hands"
            gesture_color = (0, 255, 0)
            gesture_score = 100

    return (
        gesture_status,
        gesture_color,
        gesture_score,
        hand_count
    )