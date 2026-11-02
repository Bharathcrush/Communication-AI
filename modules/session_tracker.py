import time


class SessionTracker:

    def __init__(self):

        self.running = False

        self.start_time = 0

        self.frame_count = 0

        self.eye_contact_total = 0

        self.posture_total = 0

        self.smile_total = 0

        self.straight_head_frames = 0

        self.hand_gesture_frames = 0

        self.face_detected_frames = 0


    # ========================================================
    # START SESSION
    # ========================================================

    def start(self):

        self.running = True

        self.start_time = time.time()

        self.frame_count = 0

        self.eye_contact_total = 0

        self.posture_total = 0

        self.smile_total = 0

        self.straight_head_frames = 0

        self.hand_gesture_frames = 0

        self.face_detected_frames = 0

        print("Communication evaluation session started")


    # ========================================================
    # UPDATE SESSION
    # ========================================================

    def update(
        self,
        detected,
        eye_contact,
        head_pose,
        smile_score,
        posture_score,
        hand_count
    ):

        if not self.running:
            return

        self.frame_count += 1


        # ----------------------------------------------------
        # Face detection
        # ----------------------------------------------------

        if detected:

            self.face_detected_frames += 1


        # ----------------------------------------------------
        # Eye contact
        # ----------------------------------------------------

        self.eye_contact_total += eye_contact


        # ----------------------------------------------------
        # Posture
        # ----------------------------------------------------

        self.posture_total += posture_score


        # ----------------------------------------------------
        # Smile
        # ----------------------------------------------------

        self.smile_total += smile_score


        # ----------------------------------------------------
        # Head pose
        # ----------------------------------------------------

        if head_pose == "Straight":

            self.straight_head_frames += 1


        # ----------------------------------------------------
        # Hand gestures
        # ----------------------------------------------------

        if hand_count > 0:

            self.hand_gesture_frames += 1


    # ========================================================
    # GET SESSION TIME
    # ========================================================

    def get_duration(self):

        if not self.running:
            return 0

        return int(
            time.time() - self.start_time
        )


    # ========================================================
    # STOP SESSION
    # ========================================================

    def stop(self):

        if not self.running:

            return None

        self.running = False

        duration = int(
            time.time() - self.start_time
        )


        if self.frame_count == 0:

            return None


        # ====================================================
        # CALCULATE AVERAGES
        # ====================================================

        average_eye_contact = int(
            self.eye_contact_total /
            self.frame_count
        )


        average_posture = int(
            self.posture_total /
            self.frame_count
        )


        average_smile = int(
            self.smile_total /
            self.frame_count
        )


        head_stability = int(
            (
                self.straight_head_frames /
                self.frame_count
            ) * 100
        )


        gesture_usage = int(
            (
                self.hand_gesture_frames /
                self.frame_count
            ) * 100
        )


        face_presence = int(
            (
                self.face_detected_frames /
                self.frame_count
            ) * 100
        )


        # ====================================================
        # FINAL COMMUNICATION SCORE
        # ====================================================

        final_score = int(

            average_eye_contact * 0.35

            + head_stability * 0.20

            + average_posture * 0.25

            + face_presence * 0.10

            + average_smile * 0.05

            + gesture_usage * 0.05

        )


        # ====================================================
        # FINAL RATING
        # ====================================================

        if final_score >= 85:

            rating = "Excellent"

        elif final_score >= 70:

            rating = "Good"

        elif final_score >= 50:

            rating = "Average"

        else:

            rating = "Needs Improvement"


        # ====================================================
        # RETURN RESULTS
        # ====================================================

        results = {

            "duration": duration,

            "eye_contact": average_eye_contact,

            "head_stability": head_stability,

            "posture": average_posture,

            "smile": average_smile,

            "gesture_usage": gesture_usage,

            "face_presence": face_presence,

            "final_score": final_score,

            "rating": rating
        }


        print("\n===================================")
        print("COMMUNICATION SESSION RESULT")
        print("===================================")

        print(
            f"Duration          : {duration} sec"
        )

        print(
            f"Eye Contact       : {average_eye_contact}%"
        )

        print(
            f"Head Stability    : {head_stability}%"
        )

        print(
            f"Posture           : {average_posture}%"
        )

        print(
            f"Smile             : {average_smile}%"
        )

        print(
            f"Gesture Usage     : {gesture_usage}%"
        )

        print(
            f"Face Presence     : {face_presence}%"
        )

        print("-----------------------------------")

        print(
            f"Final Score       : {final_score}/100"
        )

        print(
            f"Rating            : {rating}"
        )

        print("===================================\n")


        return results