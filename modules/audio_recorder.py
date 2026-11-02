import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import threading
import time


class AudioRecorder:

    def __init__(
        self,
        sample_rate=44100,
        channels=1,
        device=None
    ):
        """
        Audio recorder for Communication AI.

        device=None:
        Auto-detect default microphone.
        """

        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device

        self.recording = False
        self.audio_data = []

        self.thread = None
        self.output_path = None

    # ========================================================
    # START RECORDING
    # ========================================================

    def start_recording(self, output_path):

        if self.recording:

            print(
                "Audio recording is already running."
            )

            return False

        self.output_path = output_path
        self.audio_data = []

        self.recording = True

        self.thread = threading.Thread(
            target=self._record,
            daemon=True
        )

        self.thread.start()

        print(
            "Audio recording started."
        )

        print(
            f"Microphone device: {self.device}"
        )

        return True

    # ========================================================
    # RECORD AUDIO
    # ========================================================

    def _record(self):

        try:

            def callback(
                indata,
                frames,
                time_info,
                status
            ):

                if status:

                    print(
                        "Audio status:",
                        status
                    )

                if self.recording:

                    self.audio_data.append(
                        indata.copy()
                    )

            with sd.InputStream(
                device=self.device,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=1024,
                callback=callback
            ):

                while self.recording:

                    time.sleep(0.05)

        except Exception as e:

            print(
                "Audio recording error:"
            )

            print(e)

            self.recording = False

    # ========================================================
    # STOP RECORDING
    # ========================================================

    def stop_recording(self):

        if not self.recording:

            print(
                "Audio recording is not running."
            )

            return None

        self.recording = False

        if self.thread:

            self.thread.join(
                timeout=3
            )

        if not self.audio_data:

            print(
                "No audio data recorded."
            )

            return None

        try:

            # ------------------------------------------------
            # Combine all audio chunks
            # ------------------------------------------------

            audio = np.concatenate(
                self.audio_data,
                axis=0
            )

            # ------------------------------------------------
            # Convert stereo to mono if necessary
            # ------------------------------------------------

            if audio.ndim > 1:

                audio = audio[:, 0]

            # ------------------------------------------------
            # Calculate microphone level
            # ------------------------------------------------

            peak = np.max(
                np.abs(audio)
            )

            rms = np.sqrt(
                np.mean(
                    audio ** 2
                )
            )

            print()
            print(
                f"Microphone peak level: {peak:.4f}"
            )

            print(
                f"Microphone RMS level: {rms:.4f}"
            )

            # ------------------------------------------------
            # Check whether audio was actually captured
            # ------------------------------------------------

            if peak < 0.001:

                print()
                print(
                    "WARNING: Microphone input is extremely low."
                )

                print(
                    "Check Windows microphone permissions "
                    "and microphone volume."
                )

            # ------------------------------------------------
            # Normalize audio
            # ------------------------------------------------

            if peak > 0:

                audio = audio / peak

            # ------------------------------------------------
            # Prevent clipping
            # ------------------------------------------------

            audio = np.clip(
                audio,
                -1,
                1
            )

            # ------------------------------------------------
            # Convert to 16-bit WAV
            # ------------------------------------------------

            audio = (
                audio * 32767
            ).astype(
                np.int16
            )

            # ------------------------------------------------
            # Create output directory
            # ------------------------------------------------

            folder = os.path.dirname(
                self.output_path
            )

            if folder:

                os.makedirs(
                    folder,
                    exist_ok=True
                )

            # ------------------------------------------------
            # Save WAV file
            # ------------------------------------------------

            write(
                self.output_path,
                self.sample_rate,
                audio
            )

            # ------------------------------------------------
            # Calculate duration
            # ------------------------------------------------

            duration = (
                len(audio)
                / self.sample_rate
            )

            print()
            print(
                "Audio recording stopped."
            )

            print(
                f"Duration: {duration:.2f} seconds"
            )

            print(
                f"Saved: {self.output_path}"
            )

            return self.output_path

        except Exception as e:

            print()
            print(
                "Error saving audio:"
            )

            print(e)

            return None

    # ========================================================
    # CHECK RECORDING STATUS
    # ========================================================

    def is_recording(self):

        return self.recording

    # ========================================================
    # GET CURRENT AUDIO
    # ========================================================

    def get_current_audio(self):
        """
        Returns a numpy array of all audio recorded so far.
        Useful for live transcription.
        """
        if not self.audio_data:
            return None

        audio = np.concatenate(self.audio_data, axis=0)
        if audio.ndim > 1:
            audio = audio[:, 0]

        # Prevent extreme values
        audio = np.nan_to_num(audio)
        audio = np.clip(audio, -1.0, 1.0)

        # Convert to 16-bit
        audio = (audio * 32767).astype(np.int16)
        
        return audio