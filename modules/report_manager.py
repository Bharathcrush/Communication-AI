import os
import json
from datetime import datetime


# ============================================================
# REPORT DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)

HISTORY_FILE = os.path.join(
    REPORT_FOLDER,
    "session_history.json"
)


# ============================================================
# CREATE REPORT FOLDER
# ============================================================

def create_report_folder():

    if not os.path.exists(REPORT_FOLDER):

        os.makedirs(
            REPORT_FOLDER
        )


# ============================================================
# LOAD SESSION HISTORY
# ============================================================

def load_history():

    create_report_folder()

    if not os.path.exists(HISTORY_FILE):

        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):

                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# ============================================================
# RESET SESSION HISTORY
# ============================================================

def reset_history():

    """
    Clears the active session history.

    IMPORTANT:
    Individual report TXT files are NOT deleted.
    Only session_history.json is cleared.
    """

    try:

        create_report_folder()

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )

        print()
        print("Analytics history reset successfully.")
        print(
            "Previous individual reports were preserved."
        )
        print()

        return True

    except OSError as e:

        print()
        print("ERROR: Could not reset analytics history.")
        print(e)
        print()

        return False


# ============================================================
# SAVE SESSION
# ============================================================

def save_session(
    results,
    feedback
):

    create_report_folder()

    now = datetime.now()

    session_data = {

        "id": now.strftime(
            "%Y%m%d_%H%M%S"
        ),

        "date": now.strftime(
            "%d-%m-%Y"
        ),

        "time": now.strftime(
            "%I:%M %p"
        ),

        "duration": results.get(
            "duration",
            0
        ),

        "final_score": results.get(
            "final_score",
            0
        ),

        "rating": results.get(
            "rating",
            "Unknown"
        ),

        "eye_contact": results.get(
            "eye_contact",
            0
        ),

        "head_stability": results.get(
            "head_stability",
            0
        ),

        "posture": results.get(
            "posture",
            0
        ),

        "smile": results.get(
            "smile",
            0
        ),

        "gesture_usage": results.get(
            "gesture_usage",
            0
        ),

        "face_presence": results.get(
            "face_presence",
            0
        ),

        "summary": feedback.get(
            "summary",
            ""
        ),

        "strengths": feedback.get(
            "strengths",
            []
        ),

        "improvements": feedback.get(
            "improvements",
            []
        ),

        "suggestions": feedback.get(
            "suggestions",
            []
        ),

        "speech_score": feedback.get(
            "speech_score",
            0.0
        )
    }

    # --------------------------------------------------------
    # Add speech analysis data if available
    # --------------------------------------------------------

    speech = results.get(
        "speech_analysis", None
    )

    if speech and speech.get("word_count", 0) > 0:

        speech_score = speech.get(
            "speech_score", {}
        )

        session_data["speech_total"] = (
            speech_score.get("total", 0.0)
        )

        session_data["speech_fluency"] = (
            speech_score.get("fluency", 0.0)
        )

        session_data["speech_grammar"] = (
            speech_score.get("grammar", 0.0)
        )

        session_data["speech_confidence"] = (
            speech_score.get("confidence", 0.0)
        )

        session_data["speech_clarity"] = (
            speech_score.get("clarity", 0.0)
        )

        fluency_data = speech.get(
            "fluency", {}
        )

        session_data["wpm"] = (
            fluency_data.get("effective_wpm", 0)
        )

        session_data["filler_count"] = (
            speech.get("fillers", {}).get(
                "total_fillers", 0
            )
        )

        session_data["pause_count"] = (
            speech.get("pauses", {}).get(
                "total_pauses", 0
            )
        )

        session_data["grammar_errors"] = (
            speech.get("grammar", {}).get(
                "total_errors", 0
            )
        )

        session_data["transcript"] = (
            speech.get("transcript", "")
        )


    # ========================================================
    # LOAD EXISTING HISTORY
    # ========================================================

    history = load_history()


    # ========================================================
    # ADD NEW SESSION
    # ========================================================

    history.append(
        session_data
    )


    # ========================================================
    # SAVE HISTORY
    # ========================================================

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


    # ========================================================
    # CREATE INDIVIDUAL REPORT
    # ========================================================

    report_filename = (
        f"report_{session_data['id']}.txt"
    )

    report_path = os.path.join(
        REPORT_FOLDER,
        report_filename
    )


    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AI COMMUNICATION EVALUATION REPORT\n"
        )

        file.write(
            "=" * 45 + "\n\n"
        )

        file.write(
            f"Date: {session_data['date']}\n"
        )

        file.write(
            f"Time: {session_data['time']}\n"
        )

        file.write(
            f"Duration: {session_data['duration']} seconds\n\n"
        )


        # ====================================================
        # PERFORMANCE SCORES
        # ====================================================

        file.write(
            "PERFORMANCE SCORES\n"
        )

        file.write(
            "-" * 45 + "\n"
        )

        file.write(
            f"Final Score: "
            f"{session_data['final_score']}/100\n"
        )

        file.write(
            f"Rating: "
            f"{session_data['rating']}\n\n"
        )

        file.write(
            f"Eye Contact: "
            f"{session_data['eye_contact']}%\n"
        )

        file.write(
            f"Head Stability: "
            f"{session_data['head_stability']}%\n"
        )

        file.write(
            f"Posture: "
            f"{session_data['posture']}%\n"
        )

        file.write(
            f"Facial Expression: "
            f"{session_data['smile']}%\n"
        )

        file.write(
            f"Gesture Usage: "
            f"{session_data['gesture_usage']}%\n"
        )

        file.write(
            f"Face Presence: "
            f"{session_data['face_presence']}%\n\n"
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        file.write(
            "SUMMARY\n"
        )

        file.write(
            "-" * 45 + "\n"
        )

        file.write(
            session_data["summary"]
            + "\n\n"
        )


        # ====================================================
        # STRENGTHS
        # ====================================================

        file.write(
            "STRENGTHS\n"
        )

        file.write(
            "-" * 45 + "\n"
        )

        if session_data["strengths"]:

            for item in session_data["strengths"]:

                file.write(
                    f"+ {item}\n"
                )

        else:

            file.write(
                "No major strengths identified.\n"
            )


        # ====================================================
        # IMPROVEMENTS
        # ====================================================

        file.write(
            "\nAREAS TO IMPROVE\n"
        )

        file.write(
            "-" * 45 + "\n"
        )

        if session_data["improvements"]:

            for item in session_data["improvements"]:

                file.write(
                    f"- {item}\n"
                )

        else:

            file.write(
                "No major problems detected.\n"
            )


        # ====================================================
        # SUGGESTIONS
        # ====================================================

        file.write(
            "\nSUGGESTIONS\n"
        )

        file.write(
            "-" * 45 + "\n"
        )

        if session_data["suggestions"]:

            for item in session_data["suggestions"]:

                file.write(
                    f"> {item}\n"
                )

        else:

            file.write(
                "Continue maintaining your performance.\n"
            )

        # ====================================================
        # SPEECH ANALYSIS
        # ====================================================

        if session_data.get("speech_total", 0) > 0:

            file.write(
                "\nSPEECH ANALYSIS\n"
            )

            file.write(
                "-" * 45 + "\n"
            )

            file.write(
                f"Speech Score: "
                f"{session_data.get('speech_total', 0)}/10\n"
            )

            file.write(
                f"  Fluency:    "
                f"{session_data.get('speech_fluency', 0)}/3.0\n"
            )

            file.write(
                f"  Grammar:    "
                f"{session_data.get('speech_grammar', 0)}/2.5\n"
            )

            file.write(
                f"  Confidence: "
                f"{session_data.get('speech_confidence', 0)}/2.0\n"
            )

            file.write(
                f"  Clarity:    "
                f"{session_data.get('speech_clarity', 0)}/2.5\n\n"
            )

            file.write(
                f"Words per minute : "
                f"{session_data.get('wpm', 0)}\n"
            )

            file.write(
                f"Pauses detected  : "
                f"{session_data.get('pause_count', 0)}\n"
            )

            file.write(
                f"Filler words     : "
                f"{session_data.get('filler_count', 0)}\n"
            )

            file.write(
                f"Grammar errors   : "
                f"{session_data.get('grammar_errors', 0)}\n"
            )

            transcript = session_data.get(
                "transcript", ""
            )

            if transcript:

                file.write(
                    "\nTRANSCRIPT\n"
                )

                file.write(
                    "-" * 45 + "\n"
                )

                file.write(
                    transcript + "\n"
                )


    print()
    print("Report saved successfully.")
    print(
        f"Report: {report_path}"
    )
    print()


    return session_data, report_path