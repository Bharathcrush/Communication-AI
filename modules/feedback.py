# ============================================================
# COMMUNICATION AI - AUTOMATIC FEEDBACK GENERATOR
# ============================================================


def generate_feedback(results):

    strengths = []
    improvements = []
    suggestions = []

    # --------------------------------------------------------
    # Get session values safely
    # --------------------------------------------------------

    eye_contact = results.get("eye_contact", 0)
    head_stability = results.get("head_stability", 0)
    posture = results.get("posture", 0)
    smile = results.get("smile", 0)
    gesture_usage = results.get("gesture_usage", 0)
    face_presence = results.get("face_presence", 0)

    final_score = results.get("final_score", 0)
    rating = results.get("rating", "Unknown")


    # ========================================================
    # 1. EYE CONTACT FEEDBACK
    # ========================================================

    if eye_contact >= 85:

        strengths.append(
            "Excellent eye contact."
        )

    elif eye_contact >= 70:

        strengths.append(
            "Good eye contact."
        )

        suggestions.append(
            "Try to maintain eye contact more consistently."
        )

    elif eye_contact >= 50:

        improvements.append(
            "Eye contact was inconsistent."
        )

        suggestions.append(
            "Look toward the camera more often while speaking."
        )

    else:

        improvements.append(
            "Eye contact needs improvement."
        )

        suggestions.append(
            "Avoid looking away from the camera for long periods."
        )


    # ========================================================
    # 2. HEAD POSITION FEEDBACK
    # ========================================================

    if head_stability >= 85:

        strengths.append(
            "Head position was stable."
        )

    elif head_stability >= 65:

        strengths.append(
            "Head movement was reasonably controlled."
        )

        suggestions.append(
            "Keep your head facing forward more consistently."
        )

    else:

        improvements.append(
            "Frequent head movement was detected."
        )

        suggestions.append(
            "Try to keep your head stable and face the listener."
        )


    # ========================================================
    # 3. POSTURE FEEDBACK
    # ========================================================

    if posture >= 85:

        strengths.append(
            "Professional and confident posture."
        )

    elif posture >= 70:

        strengths.append(
            "Posture was generally good."
        )

        suggestions.append(
            "Keep your shoulders balanced and sit upright."
        )

    elif posture >= 50:

        improvements.append(
            "Posture could be improved."
        )

        suggestions.append(
            "Sit or stand upright and avoid leaning too much."
        )

    else:

        improvements.append(
            "Poor posture was detected frequently."
        )

        suggestions.append(
            "Keep your back straight and shoulders relaxed."
        )


    # ========================================================
    # 4. SMILE / FACIAL EXPRESSION FEEDBACK
    # ========================================================
    #
    # Important:
    # A low smile score is NOT automatically considered bad.
    # Communication does not require continuous smiling.
    # ========================================================

    if smile >= 70:

        strengths.append(
            "Positive facial expression was maintained."
        )

    elif smile >= 35:

        strengths.append(
            "Natural facial expression was observed."
        )

    elif smile >= 15:

        suggestions.append(
            "A slightly warmer facial expression may improve engagement."
        )

    else:

        suggestions.append(
            "Try using natural facial expressions when appropriate."
        )


    # ========================================================
    # 5. HAND GESTURE FEEDBACK
    # ========================================================

    if 20 <= gesture_usage <= 70:

        strengths.append(
            "Hand gestures were used naturally."
        )

    elif gesture_usage < 20:

        improvements.append(
            "Very few hand gestures were detected."
        )

        suggestions.append(
            "Use occasional natural hand gestures to support key points."
        )

    else:

        improvements.append(
            "Hand gestures were used very frequently."
        )

        suggestions.append(
            "Avoid excessive hand movement while speaking."
        )


    # ========================================================
    # 6. FACE PRESENCE FEEDBACK
    # ========================================================

    if face_presence >= 95:

        strengths.append(
            "You remained clearly visible during the session."
        )

    elif face_presence >= 80:

        suggestions.append(
            "Try to remain centered in the camera throughout the session."
        )

    else:

        improvements.append(
            "Your face was outside the camera view several times."
        )

        suggestions.append(
            "Stay centered and maintain a suitable distance from the camera."
        )


    # ========================================================
    # 8. SPEECH ANALYSIS FEEDBACK
    # ========================================================

    speech = results.get("speech_analysis", None)

    speech_score_total = 0.0

    if speech and speech.get("word_count", 0) > 0:

        speech_score = speech.get(
            "speech_score", {}
        )

        speech_score_total = speech_score.get(
            "total", 0.0
        )

        speech_fb = speech.get(
            "feedback", {}
        )

        for item in speech_fb.get("strengths", []):
            strengths.append(item)

        for item in speech_fb.get("improvements", []):
            improvements.append(item)

        for item in speech_fb.get("suggestions", []):
            suggestions.append(item)


    # ========================================================
    # 7. OVERALL FEEDBACK
    # ========================================================

    if speech and speech_score_total > 0:

        score_text = (
            f" Speech Score: {speech_score_total}/10."
        )

    else:

        score_text = ""

    if final_score >= 85:

        summary = (
            "Excellent communication performance. "
            "Your non-verbal communication was "
            "strong and consistent."
            + score_text
        )

    elif final_score >= 70:

        summary = (
            "Good communication performance. "
            "A few improvements can make your "
            "presentation more confident."
            + score_text
        )

    elif final_score >= 50:

        summary = (
            "Average communication performance. "
            "Focus on the suggested areas to "
            "improve your presentation."
            + score_text
        )

    else:

        summary = (
            "Your communication skills need "
            "further practice. Work on the "
            "improvement areas one at a time."
            + score_text
        )


    # ========================================================
    # RETURN FEEDBACK
    # ========================================================

    feedback = {

        "score": final_score,

        "rating": rating,

        "summary": summary,

        "strengths": strengths,

        "improvements": improvements,

        "suggestions": suggestions,

        "speech_score": speech_score_total
    }

    return feedback


# ============================================================
# PRINT FEEDBACK IN TERMINAL
# ============================================================

def print_feedback(feedback):

    print()
    print("==================================================")
    print("           AI COMMUNICATION FEEDBACK")
    print("==================================================")

    print(
        f"Overall Score : "
        f"{feedback['score']}/100"
    )

    print(
        f"Rating        : "
        f"{feedback['rating']}"
    )

    print("--------------------------------------------------")

    print()
    print("SUMMARY")
    print("-------")

    print(
        feedback["summary"]
    )


    # ========================================================
    # STRENGTHS
    # ========================================================

    print()
    print("STRENGTHS")
    print("---------")

    if feedback["strengths"]:

        for item in feedback["strengths"]:

            print(
                f"+ {item}"
            )

    else:

        print(
            "No major strengths identified yet."
        )


    # ========================================================
    # AREAS TO IMPROVE
    # ========================================================

    print()
    print("AREAS TO IMPROVE")
    print("----------------")

    if feedback["improvements"]:

        for item in feedback["improvements"]:

            print(
                f"- {item}"
            )

    else:

        print(
            "No major problems detected."
        )


    # ========================================================
    # SUGGESTIONS
    # ========================================================

    print()
    print("SUGGESTIONS")
    print("-----------")

    if feedback["suggestions"]:

        for item in feedback["suggestions"]:

            print(
                f"> {item}"
            )

    else:

        print(
            "Continue maintaining your current performance."
        )

    print()
    print("==================================================")
    print()