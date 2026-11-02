import os

from modules.speech_to_text import SpeechToText


# ============================================================
# AUDIO FILE
# ============================================================

audio_path = os.path.join(
    "data",
    "test_audio.wav"
)


# ============================================================
# CHECK AUDIO
# ============================================================

if not os.path.exists(audio_path):

    print(
        "ERROR: test_audio.wav was not found."
    )

    print(
        "Run test_audio.py first."
    )

    exit()


# ============================================================
# SPEECH TO TEXT
# ============================================================

print("=" * 55)
print("       COMMUNICATION AI - SPEECH TEST")
print("=" * 55)

print()

converter = SpeechToText()

text = converter.transcribe(
    audio_path
)


# ============================================================
# RESULT
# ============================================================

print("=" * 55)

if text:

    print("       SPEECH-TO-TEXT SUCCESSFUL")
    print("=" * 55)

    print()
    print("TRANSCRIPT:")
    print()
    print(text)

else:

    print("       SPEECH-TO-TEXT FAILED")
    print("=" * 55)

    print()
    print(
        "No understandable speech was detected."
    )