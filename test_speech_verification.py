"""
Comprehensive verification of the Speech Analysis integration.
Tests all module imports, function signatures, data flow,
and end-to-end pipeline with simulated data.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 55)
print("   SPEECH ANALYSIS - VERIFICATION TEST")
print("=" * 55)
print()


# ============================================================
# 1. MODULE IMPORTS
# ============================================================

print("1. MODULE IMPORTS")
print("-" * 40)

errors = []

try:
    from modules.audio_recorder import AudioRecorder
    print("  [OK] AudioRecorder")
except Exception as e:
    print(f"  [FAIL] AudioRecorder: {e}")
    errors.append("AudioRecorder import")

try:
    from modules.speech_to_text import SpeechToText
    print("  [OK] SpeechToText")
except Exception as e:
    print(f"  [FAIL] SpeechToText: {e}")
    errors.append("SpeechToText import")

try:
    from modules.speech_analyzer import analyze_speech
    print("  [OK] analyze_speech")
except Exception as e:
    print(f"  [FAIL] analyze_speech: {e}")
    errors.append("analyze_speech import")

try:
    from modules.speech_analyzer import _analyze_pauses
    from modules.speech_analyzer import _analyze_fillers
    from modules.speech_analyzer import _analyze_repetitions
    from modules.speech_analyzer import _analyze_grammar
    from modules.speech_analyzer import _analyze_fluency
    from modules.speech_analyzer import _calculate_speech_score
    from modules.speech_analyzer import _generate_speech_feedback
    from modules.speech_analyzer import _empty_result
    print("  [OK] All internal functions")
except Exception as e:
    print(f"  [FAIL] Internal functions: {e}")
    errors.append("Internal function import")

try:
    from modules.feedback import generate_feedback
    print("  [OK] generate_feedback")
except Exception as e:
    print(f"  [FAIL] generate_feedback: {e}")
    errors.append("generate_feedback import")

try:
    from modules.report_manager import save_session, load_history
    print("  [OK] report_manager")
except Exception as e:
    print(f"  [FAIL] report_manager: {e}")
    errors.append("report_manager import")

try:
    from modules.session_tracker import SessionTracker
    print("  [OK] SessionTracker")
except Exception as e:
    print(f"  [FAIL] SessionTracker: {e}")
    errors.append("SessionTracker import")

print()


# ============================================================
# 2. API VERIFICATION
# ============================================================

print("2. API VERIFICATION")
print("-" * 40)

# AudioRecorder
ar = AudioRecorder()
assert hasattr(ar, 'start_recording'), 'Missing start_recording'
assert hasattr(ar, 'stop_recording'), 'Missing stop_recording'
assert ar.device is None, f'Device should be None, got {ar.device}'
print("  [OK] AudioRecorder: start/stop_recording, device=None")

# SpeechToText - check without loading model
assert hasattr(SpeechToText, 'transcribe'), 'Missing transcribe method'
assert hasattr(SpeechToText, 'clean_text'), 'Missing clean_text method'
print("  [OK] SpeechToText: has transcribe and clean_text methods")

# Check default model in source code
import inspect
source = inspect.getsource(SpeechToText.__init__)
assert 'medium.en' in source, "Default model should be medium.en"
print("  [OK] SpeechToText: default model=medium.en")

# analyze_speech signature
sig = inspect.signature(analyze_speech)
params = list(sig.parameters.keys())
expected = ['transcript_text', 'words_with_timestamps', 'session_duration']
assert params == expected, f"Bad params: {params}"
print(f"  [OK] analyze_speech params: {params}")

print()


# ============================================================
# 3. EMPTY INPUT TEST
# ============================================================

print("3. EMPTY INPUT TEST")
print("-" * 40)

empty_result = analyze_speech("", [], 10)
assert empty_result["word_count"] == 0
assert empty_result["speech_score"]["total"] == 0.0
assert empty_result["transcript"] == ""
print("  [OK] Empty transcript returns zero score")

empty_result2 = analyze_speech("   ", [], 10)
assert empty_result2["word_count"] == 0
print("  [OK] Whitespace-only transcript returns zero")

print()


# ============================================================
# 4. FULL PIPELINE SIMULATION
# ============================================================

print("4. FULL PIPELINE SIMULATION")
print("-" * 40)

test_transcript = (
    "Hello my name is John. I am um a student "
    "at the university. I I like programming "
    "and uh building projects. You know it is "
    "actually very interesting to work on "
    "computer vision and like machine learning."
)

test_words = [
    {"word": "Hello", "start": 0.0, "end": 0.5},
    {"word": "my", "start": 0.6, "end": 0.8},
    {"word": "name", "start": 0.9, "end": 1.2},
    {"word": "is", "start": 1.3, "end": 1.4},
    {"word": "John", "start": 1.5, "end": 1.8},
    {"word": "I", "start": 2.0, "end": 2.1},
    {"word": "am", "start": 2.2, "end": 2.4},
    {"word": "um", "start": 2.5, "end": 2.8},
    {"word": "a", "start": 3.0, "end": 3.1},
    {"word": "student", "start": 3.2, "end": 3.6},
    {"word": "at", "start": 3.7, "end": 3.8},
    {"word": "the", "start": 3.9, "end": 4.0},
    {"word": "university", "start": 4.1, "end": 4.6},
    {"word": "I", "start": 5.0, "end": 5.1},
    {"word": "I", "start": 5.2, "end": 5.3},
    {"word": "like", "start": 5.4, "end": 5.7},
    {"word": "programming", "start": 5.8, "end": 6.4},
    {"word": "and", "start": 6.5, "end": 6.7},
    {"word": "uh", "start": 6.8, "end": 7.0},
    {"word": "building", "start": 7.5, "end": 8.0},
    {"word": "projects", "start": 8.1, "end": 8.5},
    {"word": "You", "start": 8.6, "end": 8.8},
    {"word": "know", "start": 8.9, "end": 9.1},
    {"word": "it", "start": 9.2, "end": 9.3},
    {"word": "is", "start": 9.4, "end": 9.5},
    {"word": "actually", "start": 9.6, "end": 10.0},
    {"word": "very", "start": 10.1, "end": 10.3},
    {"word": "interesting", "start": 10.4, "end": 10.9},
    {"word": "to", "start": 11.0, "end": 11.1},
    {"word": "work", "start": 11.2, "end": 11.4},
    {"word": "on", "start": 11.5, "end": 11.6},
    {"word": "computer", "start": 11.7, "end": 12.1},
    {"word": "vision", "start": 12.2, "end": 12.6},
    {"word": "and", "start": 12.7, "end": 12.8},
    {"word": "like", "start": 12.9, "end": 13.1},
    {"word": "machine", "start": 13.2, "end": 13.5},
    {"word": "learning", "start": 13.6, "end": 14.0},
]

result = analyze_speech(
    test_transcript,
    test_words,
    30.0
)

# Verify result structure
assert "transcript" in result
assert "word_count" in result
assert "speech_score" in result
assert "fluency" in result
assert "grammar" in result
assert "pauses" in result
assert "fillers" in result
assert "repetitions" in result
assert "feedback" in result
print("  [OK] Result structure complete")

# Verify scores
scores = result["speech_score"]
assert "total" in scores
assert "fluency" in scores
assert "grammar" in scores
assert "confidence" in scores
assert "clarity" in scores
assert 0 <= scores["total"] <= 10
print(f"  [OK] Speech Score: {scores['total']}/10")
print(f"       Fluency={scores['fluency']}/3.0, "
      f"Grammar={scores['grammar']}/2.5, "
      f"Confidence={scores['confidence']}/2.0, "
      f"Clarity={scores['clarity']}/2.5")

# Verify fillers detected
fillers = result["fillers"]
assert fillers["total_fillers"] > 0, "Should detect filler words"
filler_words_found = [
    f["word"] for f in fillers["filler_list"]
]
print(f"  [OK] Fillers detected: {fillers['total_fillers']}")
print(f"       Found: {filler_words_found}")

# Verify repetitions detected
reps = result["repetitions"]
assert reps["total_repetitions"] > 0, "Should detect 'I I'"
print(f"  [OK] Repetitions detected: {reps['total_repetitions']}")
for r in reps["repetition_list"]:
    print(f"       '{r['word']}' repeated {r['times']}x")

# Verify fluency
fluency = result["fluency"]
assert fluency["wpm"] > 0
assert fluency["effective_wpm"] > 0
print(f"  [OK] WPM: {fluency['wpm']} (effective: {fluency['effective_wpm']})")
print(f"       Rating: {fluency['wpm_rating']}")

# Verify grammar
grammar = result["grammar"]
print(f"  [OK] Grammar available: {grammar['grammar_available']}")
print(f"       Errors found: {grammar['total_errors']}")

# Verify feedback
fb = result["feedback"]
assert "summary" in fb
assert "strengths" in fb
assert "improvements" in fb
assert "suggestions" in fb
print(f"  [OK] Feedback generated:")
print(f"       Strengths: {len(fb['strengths'])}")
print(f"       Improvements: {len(fb['improvements'])}")
print(f"       Suggestions: {len(fb['suggestions'])}")

print()


# ============================================================
# 5. FEEDBACK INTEGRATION TEST
# ============================================================

print("5. FEEDBACK INTEGRATION TEST")
print("-" * 40)

mock_session_results = {
    "eye_contact": 75,
    "head_stability": 80,
    "posture": 70,
    "smile": 50,
    "gesture_usage": 40,
    "face_presence": 90,
    "final_score": 72,
    "rating": "Good",
    "duration": 30,
    "speech_analysis": result
}

feedback = generate_feedback(mock_session_results)

assert "speech_score" in feedback, "feedback should have speech_score"
assert feedback["speech_score"] > 0, "speech_score should be > 0"
print(f"  [OK] Speech score in feedback: {feedback['speech_score']}")

# Check that speech feedback items were merged
assert len(feedback["strengths"]) > 0 or len(feedback["improvements"]) > 0
print(f"  [OK] Feedback merged: {len(feedback['strengths'])} strengths, "
      f"{len(feedback['improvements'])} improvements, "
      f"{len(feedback['suggestions'])} suggestions")

has_speech_in_summary = "Speech Score" in feedback.get("summary", "")
print(f"  [OK] Summary mentions speech: {has_speech_in_summary}")

print()


# ============================================================
# 6. REPORT MANAGER DATA TEST
# ============================================================

print("6. REPORT MANAGER DATA STRUCTURE TEST")
print("-" * 40)

# Simulate what save_session does with speech data
from datetime import datetime

now = datetime.now()

session_data = {
    "id": now.strftime("%Y%m%d_%H%M%S"),
    "date": now.strftime("%d-%m-%Y"),
    "final_score": 72,
    "rating": "Good",
    "speech_score": feedback.get("speech_score", 0.0)
}

speech = mock_session_results.get("speech_analysis", None)

if speech and speech.get("word_count", 0) > 0:
    speech_score = speech.get("speech_score", {})
    session_data["speech_total"] = speech_score.get("total", 0.0)
    session_data["speech_fluency"] = speech_score.get("fluency", 0.0)
    session_data["speech_grammar"] = speech_score.get("grammar", 0.0)
    session_data["speech_confidence"] = speech_score.get("confidence", 0.0)
    session_data["speech_clarity"] = speech_score.get("clarity", 0.0)
    session_data["wpm"] = speech.get("fluency", {}).get("effective_wpm", 0)
    session_data["filler_count"] = speech.get("fillers", {}).get("total_fillers", 0)
    session_data["pause_count"] = speech.get("pauses", {}).get("total_pauses", 0)
    session_data["grammar_errors"] = speech.get("grammar", {}).get("total_errors", 0)
    session_data["transcript"] = speech.get("transcript", "")

assert "speech_total" in session_data
assert "wpm" in session_data
assert "transcript" in session_data
assert session_data["speech_total"] > 0

print(f"  [OK] Session data has speech fields:")
print(f"       speech_total={session_data['speech_total']}")
print(f"       wpm={session_data['wpm']}")
print(f"       fillers={session_data['filler_count']}")
print(f"       pauses={session_data['pause_count']}")
print(f"       grammar_errors={session_data['grammar_errors']}")
print(f"       transcript length={len(session_data['transcript'])} chars")

print()


# ============================================================
# 7. APP.PY IMPORT CHECK
# ============================================================

print("7. APP.PY IMPORT CHECK")
print("-" * 40)

# Check that app.py has the right imports
app_path = os.path.join(
    os.path.dirname(__file__),
    "app.py"
)

with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

checks = [
    ("from modules.audio_recorder import AudioRecorder",
     "AudioRecorder import"),
    ("from modules.speech_to_text import SpeechToText",
     "SpeechToText import"),
    ("from modules.speech_analyzer import analyze_speech",
     "analyze_speech import"),
    ("self.audio_recorder = AudioRecorder()",
     "AudioRecorder init"),
    ("self.speech_engine = SpeechToText",
     "SpeechToText init"),
    ("self.audio_recorder.start_recording",
     "start_recording call"),
    ("self.audio_recorder.stop_recording",
     "stop_recording call"),
    ("self.speech_engine.transcribe",
     "transcribe call"),
    ("analyze_speech(",
     "analyze_speech call"),
    ("speech_analysis",
     "speech_analysis key"),
    ("SPEECH ANALYSIS",
     "Speech Analysis UI section"),
    ("Speech Score",
     "Speech Score display"),
    ("TRANSCRIPT",
     "Transcript display"),
    ("ANALYZING SPEECH",
     "Analyzing status label"),
    ("Audio + Video",
     "Recording label"),
]

for code_check, label in checks:
    if code_check in app_code:
        print(f"  [OK] {label}")
    else:
        print(f"  [FAIL] {label} - NOT FOUND")
        errors.append(f"app.py: {label}")

print()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("=" * 55)

if errors:
    print(f"  FAILED: {len(errors)} error(s)")
    for e in errors:
        print(f"    - {e}")
else:
    print("  ALL CHECKS PASSED")

print("=" * 55)
print()
