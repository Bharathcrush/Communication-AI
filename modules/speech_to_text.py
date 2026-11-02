import os
import whisper
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly, butter, sosfilt


class SpeechToText:

    def __init__(self, model_size="medium.en"):

        print()
        print("Loading Whisper speech model...")

        try:

            self.model = whisper.load_model(
                model_size
            )

            print(
                "Whisper model loaded successfully."
            )

        except Exception as e:

            print(
                "Whisper model loading error:"
            )

            print(e)

            self.model = None

    # ========================================================
    # LOAD AND PREPROCESS AUDIO
    # ========================================================

    def preprocess_audio(self, audio_path):

        try:

            sample_rate, audio = wavfile.read(
                audio_path
            )

            # ------------------------------------------------
            # Convert stereo to mono
            # ------------------------------------------------

            if audio.ndim > 1:

                audio = np.mean(
                    audio,
                    axis=1
                )

            # ------------------------------------------------
            # Convert audio to float32
            # ------------------------------------------------

            if audio.dtype == np.int16:

                audio = (
                    audio.astype(np.float32)
                    / 32768.0
                )

            elif audio.dtype == np.int32:

                audio = (
                    audio.astype(np.float32)
                    / 2147483648.0
                )

            elif audio.dtype == np.uint8:

                audio = (
                    audio.astype(np.float32)
                    - 128.0
                ) / 128.0

            else:

                audio = audio.astype(
                    np.float32
                )

            # ------------------------------------------------
            # Remove DC offset
            # ------------------------------------------------

            audio = audio - np.mean(audio)

            # ------------------------------------------------
            # Light high-pass filter
            # Removes very low-frequency noise
            # ------------------------------------------------

            try:

                sos = butter(
                    4,
                    80,
                    btype="highpass",
                    fs=sample_rate,
                    output="sos"
                )

                audio = sosfilt(
                    sos,
                    audio
                )

            except Exception:

                pass

            # ------------------------------------------------
            # Prevent extreme values
            # ------------------------------------------------

            audio = np.nan_to_num(
                audio
            )

            audio = np.clip(
                audio,
                -1.0,
                1.0
            )

            # ------------------------------------------------
            # Resample to 16 kHz
            # ------------------------------------------------

            target_rate = 16000

            if sample_rate != target_rate:

                audio = resample_poly(
                    audio,
                    target_rate,
                    sample_rate
                )

            # ------------------------------------------------
            # Final clipping
            # ------------------------------------------------

            audio = np.clip(
                audio,
                -1.0,
                1.0
            )

            return audio.astype(
                np.float32
            )

        except Exception as e:

            print()
            print(
                "Audio preprocessing error:"
            )

            print(e)

            return None

    # ========================================================
    # TRANSCRIBE
    # ========================================================

    def transcribe(self, audio_path):

        if self.model is None:

            print(
                "Whisper model is not available."
            )

            return ""

        if not os.path.exists(
            audio_path
        ):

            print(
                f"Audio file not found: {audio_path}"
            )

            return ""

        try:

            print()
            print(
                "Preparing audio..."
            )

            audio = self.preprocess_audio(
                audio_path
            )

            if audio is None:

                return ""

            # ------------------------------------------------
            # Audio information
            # ------------------------------------------------

            duration = (
                len(audio) / 16000
            )

            peak = np.max(
                np.abs(audio)
            )

            rms = np.sqrt(
                np.mean(
                    audio ** 2
                )
            )

            print(
                f"Audio duration: {duration:.2f} seconds"
            )

            print(
                f"Audio peak: {peak:.4f}"
            )

            print(
                f"Audio RMS: {rms:.4f}"
            )

            # ------------------------------------------------
            # Check whether audio is too quiet
            # ------------------------------------------------

            if rms < 0.003:

                print()
                print(
                    "WARNING: Audio level is very low."
                )

                print(
                    "Please speak closer to the microphone."
                )

            print()
            print(
                "Transcribing speech with Whisper..."
            )

            # ------------------------------------------------
            # Whisper configuration
            # ------------------------------------------------

            result = self.model.transcribe(

                audio,

                # English only
                language="en",

                task="transcribe",

                # CPU compatibility
                fp16=False,

                # Deterministic decoding
                temperature=0,

                # Beam search
                beam_size=8,

                # Better candidate selection
                best_of=8,

                # Don't rely heavily on previous text
                condition_on_previous_text=False,

                # Avoid hallucination during silence
                no_speech_threshold=0.6,

                # Reject suspicious repetitive output
                compression_ratio_threshold=2.4,

                # Reject extremely low-confidence segments
                logprob_threshold=-1.0,

                # Word-level timestamps for pause detection
                word_timestamps=True,

                # Context for your project
                initial_prompt=(
                    "English speech. "
                    "The speaker is a student "
                    "participating in a communication "
                    "skills evaluation. "
                    "The speaker may talk about "
                    "their name, college, education, "
                    "skills, projects, career goals, "
                    "technology and communication."
                )
            )

            text = result.get(
                "text",
                ""
            ).strip()

            # ------------------------------------------------
            # Clean text
            # ------------------------------------------------

            text = self.clean_text(
                text
            )

            # ------------------------------------------------
            # Extract word-level timestamps
            # ------------------------------------------------

            words = []

            segments = result.get(
                "segments",
                []
            )

            for segment in segments:

                seg_words = segment.get(
                    "words",
                    []
                )

                for w in seg_words:

                    words.append({
                        "word": w.get(
                            "word", ""
                        ).strip(),
                        "start": w.get(
                            "start", 0.0
                        ),
                        "end": w.get(
                            "end", 0.0
                        )
                    })

            # ------------------------------------------------
            # Result
            # ------------------------------------------------

            if not text:

                print()
                print(
                    "No understandable speech detected."
                )

                return {
                    "text": "",
                    "segments": [],
                    "words": []
                }

            print()
            print(
                "Speech detected:"
            )

            print(
                text
            )

            print(
                f"Words with timestamps: {len(words)}"
            )

            print()

            return {
                "text": text,
                "segments": segments,
                "words": words
            }

        except Exception as e:

            print()
            print(
                "Speech-to-text error:"
            )

            print(e)

            return {
                "text": "",
                "segments": [],
                "words": []
            }

    # ========================================================
    # CLEAN TRANSCRIPT
    # ========================================================

    def clean_text(self, text):

        if not text:

            return ""

        # Remove excessive spaces

        text = " ".join(
            text.split()
        )

        # Remove spaces before punctuation

        text = text.replace(
            " ,",
            ","
        )

        text = text.replace(
            " .",
            "."
        )

        text = text.replace(
            " ?",
            "?"
        )

        text = text.replace(
            " !",
            "!"
        )

        return text.strip()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 55)

    print(
        "       COMMUNICATION AI - SPEECH TEST"
    )

    print("=" * 55)

    audio_file = "data/test_audio.wav"

    speech = SpeechToText(
        model_size="medium.en"
    )

    result = speech.transcribe(
        audio_file
    )

    transcript = result.get(
        "text", ""
    ) if isinstance(result, dict) else result

    print("=" * 55)

    print(
        "       SPEECH-TO-TEXT RESULT"
    )

    print("=" * 55)

    print()

    if transcript:

        print(
            "TRANSCRIPT:"
        )

        print()

        print(
            transcript
        )

    else:

        print(
            "No transcript generated."
        )

    print()