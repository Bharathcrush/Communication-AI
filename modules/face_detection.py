import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)


def detect_face(frame, rgb):

    results = face_detector.process(rgb)

    detected = False

    if results.detections:

        detected = True

        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

    return frame, detected