from modules.report_manager import load_history


# ============================================================
# COMMUNICATION AI - PROGRESS ANALYTICS
# ============================================================


def calculate_analytics():

    history = load_history()

    # --------------------------------------------------------
    # No sessions available
    # --------------------------------------------------------

    if not history:

        return {
            "total_sessions": 0,
            "average_score": 0,
            "best_score": 0,
            "latest_score": 0,
            "improvement": 0,

            "average_eye_contact": 0,
            "average_head_stability": 0,
            "average_posture": 0,
            "average_smile": 0,
            "average_gesture_usage": 0,
            "average_face_presence": 0,

            "dates": [],
            "scores": [],
            "eye_contact": [],
            "posture": [],
            "head_stability": []
        }


    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    total_sessions = len(history)


    scores = [
        session.get("final_score", 0)
        for session in history
    ]


    eye_scores = [
        session.get("eye_contact", 0)
        for session in history
    ]


    head_scores = [
        session.get("head_stability", 0)
        for session in history
    ]


    posture_scores = [
        session.get("posture", 0)
        for session in history
    ]


    smile_scores = [
        session.get("smile", 0)
        for session in history
    ]


    gesture_scores = [
        session.get("gesture_usage", 0)
        for session in history
    ]


    face_scores = [
        session.get("face_presence", 0)
        for session in history
    ]


    dates = [
        session.get("date", "")
        for session in history
    ]


    # ========================================================
    # SCORE STATISTICS
    # ========================================================

    average_score = round(
        sum(scores) / total_sessions,
        1
    )


    best_score = max(
        scores
    )


    latest_score = scores[-1]


    # ========================================================
    # IMPROVEMENT
    # ========================================================

    if total_sessions >= 2:

        improvement = (
            scores[-1]
            - scores[0]
        )

    else:

        improvement = 0


    # ========================================================
    # AVERAGE METRICS
    # ========================================================

    average_eye_contact = round(
        sum(eye_scores) / total_sessions,
        1
    )


    average_head_stability = round(
        sum(head_scores) / total_sessions,
        1
    )


    average_posture = round(
        sum(posture_scores) / total_sessions,
        1
    )


    average_smile = round(
        sum(smile_scores) / total_sessions,
        1
    )


    average_gesture_usage = round(
        sum(gesture_scores) / total_sessions,
        1
    )


    average_face_presence = round(
        sum(face_scores) / total_sessions,
        1
    )


    # ========================================================
    # RETURN ANALYTICS
    # ========================================================

    return {

        "total_sessions":
            total_sessions,

        "average_score":
            average_score,

        "best_score":
            best_score,

        "latest_score":
            latest_score,

        "improvement":
            improvement,


        "average_eye_contact":
            average_eye_contact,

        "average_head_stability":
            average_head_stability,

        "average_posture":
            average_posture,

        "average_smile":
            average_smile,

        "average_gesture_usage":
            average_gesture_usage,

        "average_face_presence":
            average_face_presence,


        "dates":
            dates,

        "scores":
            scores,

        "eye_contact":
            eye_scores,

        "posture":
            posture_scores,

        "head_stability":
            head_scores
    }


# ============================================================
# GET RECENT SESSIONS
# ============================================================

def get_recent_sessions(limit=10):

    history = load_history()

    if not history:

        return []

    return history[-limit:]


# ============================================================
# GET PERFORMANCE TREND
# ============================================================

def get_performance_trend():

    analytics = calculate_analytics()

    total_sessions = analytics[
        "total_sessions"
    ]


    if total_sessions < 2:

        return (
            "Not enough data",
            "Complete at least two sessions "
            "to calculate your progress."
        )


    improvement = analytics[
        "improvement"
    ]


    if improvement >= 10:

        return (
            "Strong Improvement",
            "Your communication score has "
            "improved significantly."
        )


    elif improvement > 0:

        return (
            "Improving",
            "Your overall communication "
            "performance is moving upward."
        )


    elif improvement == 0:

        return (
            "Stable",
            "Your overall performance "
            "has remained consistent."
        )


    else:

        return (
            "Needs Attention",
            "Your latest score is below "
            "your first recorded session."
        )