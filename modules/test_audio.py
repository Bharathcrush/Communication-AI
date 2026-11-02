import time
import os

from modules.audio_recorder import AudioRecorder


# ============================================================
# OUTPUT FILE
# ============================================================

output_path = os.path.join(
    "data",
    "test_audio.wav"
)


# ============================================================
# CREATE RECORDER
# ============================================================

recorder = AudioRecorder()


print("=" * 50)
print("       COMMUNICATION AI - AUDIO TEST")
print("=" * 50)

print()
print("Recording will start now.")
print("Speak normally for 10 seconds.")
print()


# ============================================================
# START RECORDING
# ============================================================

if not recorder.start_recording(output_path):

    print("Could not start recording.")
    exit()


# ============================================================
# RECORD FOR 10 SECONDS
# ============================================================

for remaining in range(10, 0, -1):

    print(
        f"Recording... {remaining} seconds",
        end="\r"
    )

    time.sleep(1)


print()
print()


# ============================================================
# STOP RECORDING
# ============================================================

saved_file = recorder.stop_recording()


# ============================================================
# RESULT
# ============================================================

print()

if saved_file:

    print("=" * 50)
    print("       AUDIO TEST SUCCESSFUL")
    print("=" * 50)

    print()
    print(f"Audio file: {saved_file}")

else:

    print("=" * 50)
    print("       AUDIO TEST FAILED")
    print("=" * 50)