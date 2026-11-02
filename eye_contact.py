import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

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

        # Left Eye Iris
        left_iris = face.landmark[468]

        # Right Eye Iris
        right_iris = face.landmark[473]

        lx = int(left_iris.x * w)
        ly = int(left_iris.y * h)

        rx = int(right_iris.x * w)
        ry = int(right_iris.y * h)

        cv2.circle(frame, (lx, ly), 4, (0, 255, 0), -1)
        cv2.circle(frame, (rx, ry), 4, (0, 255, 0), -1)

        cv2.putText(
            frame,
            "Eyes Detected",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow("Eye Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()