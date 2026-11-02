import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    h, w, _ = frame.shape

    if result.multi_face_landmarks:

        face = result.multi_face_landmarks[0]

        nose = face.landmark[1]

        left = face.landmark[234]
        right = face.landmark[454]

        x = nose.x * w

        left_x = left.x * w
        right_x = right.x * w

        center = (left_x + right_x) / 2

        difference = x - center

        if difference < -20:
            direction = "LOOKING LEFT"

        elif difference > 20:
            direction = "LOOKING RIGHT"

        else:
            direction = "LOOKING STRAIGHT"

        cv2.putText(frame,
                    direction,
                    (20,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)

    cv2.imshow("Head Pose", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()