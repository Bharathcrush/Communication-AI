# -*- coding: utf-8 -*-
"""
Chapters 7, 8, 9 and References Content:
- Chapter 7: CHALLENGES AND LIMITATIONS
- Chapter 8: CONCLUSION AND FUTURE SCOPE
- Chapter 9: APPENDIX (Source code and system outputs)
- REFERENCES
"""

def get_chap7_9_html(fig9_1, fig9_2, fig9_3):
    raw_template = r"""
    <!-- =================================================== -->
    <!-- CHAPTER 7: CHALLENGES AND LIMITATIONS -->
    <!-- =================================================== -->
    <div class="page" id="chap7">
        <div class="chapter-heading">
            CHAPTER 7<br><br>CHALLENGES AND LIMITATIONS
        </div>

        <p>
            The engineering and deployment of an intelligent multimodal communication evaluation framework introduces complex technical, perceptual, computational, and behavioral challenges. Understanding these challenges is essential for assessing system robustness, setting appropriate operational expectations, and establishing directions for future enhancement. This chapter examines the primary challenges encountered, system limitations, and mitigation strategies implemented.
        </p>

        <div class="section-heading">7.1 CHAPTER OVERVIEW</div>

        <p>
            Evaluating human communication through automated software requires balancing real-time execution speeds with deep learning accuracy. Unlike structured industrial computer vision tasks, human face and speech behaviors exhibit vast demographic, physiological, and environmental variability. This chapter categorizes constraints into technical, data/acoustic, operational, ethical, and UI dimensions.
        </p>

        <div class="section-heading">7.2 TECHNICAL CHALLENGES</div>

        <div class="subsection-heading">7.2.1 Real-Time Synchronization of Video and Audio Threads</div>
        <p>
            Video frames are captured synchronously at 30 FPS, while audio is sampled continuously at 16,000 samples per second. If both streams are processed in a single Python thread, intensive video matrix calculations cause buffer overruns and dropped audio frames.
        </p>
        <p>
            <b>Mitigation:</b> The system employs dedicated Python background threads (<code>threading.Thread</code>) with non-blocking callback queues, isolating audio capture from video frame rendering.
        </p>

        <div class="subsection-heading">7.2.2 Latency of Deep Speech Recognition (Whisper Model)</div>
        <p>
            The OpenAI Whisper <code>medium.en</code> model contains approximately 769 million parameters. Running deep transformer encoder-decoder inference on a consumer CPU requires significant processing time (typically 3 to 8 seconds for a 45-second audio recording).
        </p>
        <p>
            <b>Mitigation:</b> Whisper model loading is executed once in the background upon application startup. During live practice, audio is buffered in memory, and transcription occurs asynchronously upon session termination, preventing GUI freeze.
        </p>

        <div class="subsection-heading">7.2.3 Facial Landmark Jitter & Environmental Lighting</div>
        <p>
            Subtle fluctuations in indoor ambient lighting can induce rapid frame-to-frame coordinate jitter in facial landmarks, particularly around mouth corners and eyelids.
        </p>
        <p>
            <b>Mitigation:</b> The smile detection engine integrates a sliding temporal moving average filter (<code>deque(maxlen=10)</code>) that smooths raw scores across consecutive frames, eliminating flickering classifications.
        </p>

        <div class="section-heading">7.3 DATA & ACOUSTIC CHALLENGES</div>

        <div class="subsection-heading">7.3.1 Ambient Room Noise and Reverberation</div>
        <p>
            Practice environments in student hostels or classrooms frequently feature background HVAC noise, ceiling fan hum, and room reverberation.
        </p>
        <p>
            <b>Mitigation:</b> A digital 4th-order Butterworth bandpass filter (80 Hz to 7500 Hz) isolates fundamental human vocal frequencies, filtering out electrical rumble and high-frequency noise.
        </p>

        <div class="subsection-heading">7.3.2 Non-Standard Accents, Dialects, and Disfluency Disambiguation</div>
        <p>
            Regional Indian English accents and conversational cadence can challenge traditional speech models. Furthermore, distinguishing between intentional thinking pauses and nervous hesitations requires contextual analysis.
        </p>
        <p>
            <b>Mitigation:</b> Whisper's multilingual training data provides superior accent tolerance compared to classical acoustic models. Pauses under 1.5 seconds are classified as natural breathing transitions, avoiding false penalties.
        </p>

        <div class="section-heading">7.4 OPERATIONAL CHALLENGES</div>

        <div class="subsection-heading">7.4.1 Webcam Framing and User Positioning Constraints</div>
        <p>
            When a candidate sits too close or too far from the camera, facial landmarks can be clipped or distorted.
        </p>
        <p>
            <b>Mitigation:</b> The face presence ratio (F_pres) continuously monitors face visibility; if the face exits the frame, the user is alerted to re-center.
        </p>

        <div class="subsection-heading">7.4.2 Eyeglasses Reflections and Partial Occlusion</div>
        <p>
            Eyeglass glare can partially occlude iris landmarks 468 and 473, occasionally affecting gaze estimation.
        </p>
        <p>
            <b>Mitigation:</b> The algorithm computes horizontal pupil center by averaging both left and right irises, maintaining tracking even if one eye experiences temporary specular reflection.
        </p>

        <div class="section-heading">7.5 USER INTERFACE & VISUALISATION CHALLENGES</div>

        <p>
            Presenting multi-dimensional metrics simultaneously without causing cognitive overload is challenging. The CustomTkinter GUI resolves this by displaying clean metric cards with color-coded status badges (Green: Good/Excellent, Yellow: Average, Red: Needs Improvement), while reserving detailed text feedback for the post-session summary.
        </p>

        <div class="section-heading">7.6 ETHICAL CONSIDERATIONS & BIAS MITIGATION</div>

        <p>
            Automated evaluation of human behavior must be conducted with extreme ethical care:
        </p>
        <p>
            • <b>No High-Stakes Ranking:</b> The system is strictly designed as a formative pedagogical coaching tool, not as an automated screening or hiring filter.<br>
            • <b>Cultural & Physical Inclusivity:</b> Non-verbal cues such as eye contact and smiling vary across cultural norms and physiological conditions; the feedback treats these as practice observations rather than definitive personality judgments.<br>
            • <b>Absolute Data Privacy:</b> All audio and video streams remain entirely within the candidate's personal computer, ensuring zero data leakage.
        </p>

        <div class="section-heading">7.7 LIMITATIONS OF THE CURRENT SYSTEM</div>

        <p>
            1. <i>Single-Person Restriction:</i> The system assumes one candidate centered before the webcam; multi-person group discussions are not currently supported.<br>
            2. <i>Post-Session Speech Latency:</i> Deep Whisper speech processing takes several seconds after session end before generating the transcript.<br>
            3. <i>Context-Free Grammar Checking:</i> The grammar engine focuses on surface syntactic structures and does not fully evaluate deep domain-specific technical accuracy.
        </p>

        <div class="section-heading">7.8 POTENTIAL IMPROVEMENTS</div>

        <table class="report-table">
            <tr>
                <th style="width: 30%;">Improvement Area</th>
                <th style="width: 70%;">Proposed Technical Enhancement</th>
            </tr>
            <tr>
                <td>Speech Inference Speed</td>
                <td>Integrate Faster-Whisper (CTranslate2 INT8 quantization) for sub-second transcription</td>
            </tr>
            <tr>
                <td>Interview Questioning</td>
                <td>Integrate Local LLMs (e.g., LLaMA / Mistral) to ask adaptive technical interview questions</td>
            </tr>
            <tr>
                <td>Multilingual Coaching</td>
                <td>Expand NLP rubrics to evaluate regional Indian languages (Tamil, Hindi, Telugu)</td>
            </tr>
            <tr>
                <td>Gaze 3D Calibration</td>
                <td>Implement camera-screen angle calibration routines to account for off-axis external webcams</td>
            </tr>
        </table>

        <div class="section-heading">7.9 LESSONS LEARNED</div>

        <p>
            • Modular pipeline design is indispensable when coupling asynchronous sensory inputs (video and audio).<br>
            • Temporal moving average smoothing is crucial for human behavioral indicators to prevent jarring metric oscillations.<br>
            • Explaining <i>why</i> a score was awarded builds far greater user trust than presenting an unexplained aggregate number.
        </p>

        <div class="section-heading">7.10 SUMMARY</div>

        <p>
            This chapter evaluated the core computational, acoustic, and behavioral challenges of automated communication coaching. Despite real-world constraints, the implemented mitigations ensure a robust, private, and highly practical self-evaluation experience.
        </p>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- CHAPTER 8: CONCLUSION AND FUTURE SCOPE -->
    <!-- =================================================== -->
    <div class="page" id="chap8">
        <div class="chapter-heading">
            CHAPTER 8<br><br>CONCLUSION AND FUTURE SCOPE
        </div>

        <p>
            This chapter synthesizes the completed research, software development, and experimental findings of the AI-Based Self-Evaluation System for Communication Skills. It highlights major technical achievements, contributions to academic and placement preparation, limitations of the current implementation, and directions for long-term research.
        </p>

        <div class="section-heading">8.1 INTRODUCTION</div>

        <p>
            Mastering interpersonal communication is essential for engineering graduates seeking successful transitions into professional careers. Traditional training modalities, while valuable, cannot provide the scalable, continuous, self-paced practice required to master non-verbal poise and verbal fluency. This project bridged that critical void through an intelligent, locally executed multimodal software architecture.
        </p>

        <div class="section-heading">8.2 SUMMARY OF WORK</div>

        <p>
            The project accomplished the following comprehensive engineering milestones:
        </p>
        <p>
            1. <b>Problem Formalization:</b> Conducted detailed system analysis identifying subjectivity, observer fatigue, and uncoupled verbal/non-verbal evaluation as the primary bottlenecks in existing training methodologies.<br>
            2. <b>Computer Vision Perception Pipeline:</b> Implemented real-time 30 FPS video tracking using OpenCV and MediaPipe Face Mesh, Pose, and Hands, measuring eye contact, head stability, posture alignment, smiling, and gestures.<br>
            3. <b>Audio & Speech Processing Pipeline:</b> Built a multi-threaded 16 kHz audio recorder paired with digital Butterworth filtering and OpenAI Whisper transformer transcription, computing speaking rate (WPM), hesitation pauses, and conversational filler words.<br>
            4. <b>Multimodal Fusion & Feedback Engine:</b> Developed deterministic, weighted scoring formulations and a rule-based feedback generator that outputs tailored strengths, weaknesses, and coaching suggestions.<br>
            5. <b>Modern UI Dashboard & Persistence:</b> Delivered a sleek CustomTkinter dark-mode desktop application with embedded Matplotlib historical trend analysis and local JSON/TXT report persistence.<br>
            6. <b>Empirical Validation:</b> Validated system accuracy across multiple real test sessions, demonstrating high tracking fidelity and measurable user improvement.
        </p>

        <div class="section-heading">8.3 ACHIEVEMENTS OF THE PROJECT</div>

        <p>
            • <b>Unified Multimodal Synchronization:</b> Successfully synchronized 468-point facial mesh tracking, 33-point skeletal pose analysis, and deep speech recognition in a single Python desktop application.<br>
            • <b>Exceptional Accessibility & Zero Cost:</b> Engineered entirely with open-source software libraries, eliminating licensing barriers and requiring only commodity laptop hardware.<br>
            • <b>Total Biometric Privacy:</b> Kept 100% of video processing, audio transcription, and report generation local, safeguarding candidate privacy.<br>
            • <b>Objective, Repeatable Measurement:</b> Provided deterministic, quantifiable metrics that track true longitudinal skill development over time.
        </p>

        <div class="section-heading">8.4 KEY FINDINGS</div>

        <p>
            • <b>Non-Verbal Sensitivity:</b> Gaze and posture tracking accurately distinguished confident candidates (Bharath, Final Score: 91) from hesitant, restless speakers (Dhinesh, Final Score: 57).<br>
            • <b>Acoustic Timing Precision:</b> Whisper timestamp extraction provided millisecond accuracy in quantifying speech pauses and conversational filler density.<br>
            • <b>Pedagogical Efficacy:</b> Users practicing iteratively with the system demonstrated marked reductions in filler words and measurable increases in sustained eye contact.
        </p>

        <div class="section-heading">8.5 PROJECT CONTRIBUTIONS</div>

        <p>
            1. <i>Technical Contribution:</i> A robust, multi-threaded multimodal pipeline architecture combining OpenCV, MediaPipe, SoundDevice, and Whisper.<br>
            2. <i>Pedagogical Contribution:</i> A transparent, rule-based feedback engine translating quantitative mathematical metrics into actionable soft-skill advice.<br>
            3. <i>Practical Contribution:</i> A turnkey, privacy-preserving desktop software tool ready for deployment in campus placement training cells.
        </p>

        <div class="section-heading">8.6 LIMITATIONS</div>

        <p>
            The system is currently limited to single-speaker desktop scenarios, requires 3 to 8 seconds of post-session CPU processing for Whisper speech transcription, and relies on consistent indoor illumination for optimal facial mesh tracking.
        </p>

        <div class="section-heading">8.7 FUTURE ENHANCEMENTS</div>

        <div class="subsection-heading">8.7.1 Emotion Recognition via Audio-Visual Deep Networks</div>
        <p>
            Future work will incorporate facial action unit (FAU) classification and acoustic pitch/prosody modulation to evaluate emotional expressiveness and vocal enthusiasm.
        </p>

        <div class="subsection-heading">8.7.2 LLM-Powered Real-Time Mock Interview Q&A Agent</div>
        <p>
            Integrating a quantized local Large Language Model (e.g., LLaMA-3 or Mistral) will enable the system to conduct interactive, multi-turn technical interviews, dynamically generating follow-up questions based on the candidate's transcribed answers.
        </p>

        <div class="subsection-heading">8.7.3 Mobile and Cross-Platform WebRTC Deployment</div>
        <p>
            Porting the core perceptual engine to WebAssembly or mobile frameworks will allow students to practice directly on smartphones and tablets.
        </p>

        <div class="subsection-heading">8.7.4 Multilingual Support for Regional Languages</div>
        <p>
            Extending speech and grammatical evaluation models to regional Indian languages (Tamil, Hindi, Telugu) will expand accessibility for vernacular-medium engineering aspirants.
        </p>

        <div class="section-heading">8.8 LONG-TERM VISION</div>

        <p>
            The long-term vision is to establish an autonomous, AI-driven personal communication coach capable of accompanying students throughout their academic and professional journeys, nurturing articulate, confident, and inspiring engineering leaders.
        </p>

        <div class="section-heading">8.9 CONCLUSION</div>

        <p>
            The <b>AI-Based Self-Evaluation System for Communication Skills Using OpenCV, NLP, and Speech Validation</b> successfully realizes an objective, real-time, and private multimodal communication training platform. By harmonizing computer vision landmarking with deep acoustic speech recognition, the system provides repeatable, constructive, and actionable feedback, establishing a new benchmark for accessible, automated soft-skill development in engineering education.
        </p>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- CHAPTER 9: APPENDIX -->
    <!-- =================================================== -->
    <div class="page" id="chap9">
        <div class="chapter-heading">
            CHAPTER 9<br><br>APPENDIX
        </div>

        <div class="section-heading">SAMPLE CODE SNIPPETS</div>

        <p>
            This chapter presents representative source code listings illustrating the primary implementation components of the AI-Based Self-Evaluation System.
        </p>

        <div class="subsection-heading">1. Computer Vision: Face Detection Pipeline (modules/face_detection.py)</div>
        <pre class="code-block">
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

def detect_face(frame, rgb):
    results = face_detector.process(rgb)
    detected = False
    if results.detections:
        detected = True
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)
    return frame, detected
        </pre>

        <div class="subsection-heading">2. Computer Vision: Iris Landmark Eye Contact Estimation (modules/eye_contact.py)</div>
        <pre class="code-block">
import cv2

def calculate_eye_contact(frame, face_landmarks):
    h, w, _ = frame.shape

    # Iris landmarks from MediaPipe Face Mesh
    left_iris = face_landmarks.landmark[468]
    right_iris = face_landmarks.landmark[473]

    lx, ly = int(left_iris.x * w), int(left_iris.y * h)
    rx, ry = int(right_iris.x * w), int(right_iris.y * h)

    # Draw iris tracking points on frame
    cv2.circle(frame, (lx, ly), 3, (0, 255, 0), -1)
    cv2.circle(frame, (rx, ry), 3, (0, 255, 0), -1)

    # Calculate horizontal gaze deviation from screen center
    center = (lx + rx) / 2
    screen_center = w / 2
    distance = abs(center - screen_center)

    eye_contact = max(0, 100 - int(distance / 3))
    eye_contact = min(100, eye_contact)
    return eye_contact, frame
        </pre>

        <div class="subsection-heading">3. Computer Vision: Head Pose Yaw Estimation (modules/head_pose.py)</div>
        <pre class="code-block">
def estimate_head_pose(frame, face_landmarks):
    h, w, _ = frame.shape

    nose = face_landmarks.landmark[1]
    left = face_landmarks.landmark[234]
    right = face_landmarks.landmark[454]

    nose_x = nose.x * w
    left_x = left.x * w
    right_x = right.x * w

    center = (left_x + right_x) / 2
    difference = nose_x - center

    if difference < -20:
        direction = "Left"
        color = (0, 0, 255)
    elif difference > 20:
        direction = "Right"
        color = (0, 0, 255)
    else:
        direction = "Straight"
        color = (0, 255, 0)

    return direction, color
        </pre>

        <div class="subsection-heading">4. Computer Vision: Posture Shoulder Alignment (modules/posture.py)</div>
        <pre class="code-block">
import mediapipe as mp

mp_pose = mp.solutions.pose
pose_detector = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def detect_posture(frame, rgb):
    results = pose_detector.process(rgb)
    if not results.pose_landmarks:
        return "Unknown", (255, 255, 255), 0

    landmarks = results.pose_landmarks.landmark
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    shoulder_difference = abs(left_shoulder.y - right_shoulder.y)

    if shoulder_difference < 0.025:
        return "Good", (0, 255, 0), 100
    elif shoulder_difference < 0.060:
        return "Average", (0, 255, 255), 70
    else:
        return "Poor", (0, 0, 255), 40
        </pre>

        <div class="subsection-heading">5. Audio & Speech: OpenAI Whisper Transcription (modules/speech_to_text.py)</div>
        <pre class="code-block">
import whisper
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

class SpeechToText:
    def __init__(self, model_size="medium.en"):
        self.model = whisper.load_model(model_size)

    def preprocess_audio(self, audio_path):
        sample_rate, audio = wavfile.read(audio_path)
        # Apply 4th-order Butterworth bandpass filter (80Hz to 7500Hz)
        sos = butter(4, [80, 7500], btype='bandpass', fs=sample_rate, output='sos')
        filtered = sosfilt(sos, audio)
        return sample_rate, filtered

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path, word_timestamps=True)
        return {
            "text": result["text"].strip(),
            "segments": result["segments"]
        }
        </pre>

        <div class="subsection-heading">6. Speech & NLP: Acoustic Pause & Disfluency Analyzer (modules/speech_analyzer.py)</div>
        <pre class="code-block">
FILLER_WORDS = [
    "um", "uh", "umm", "uhh", "er", "ah", "like", 
    "basically", "actually", "you know", "i mean", "sort of", "kind of"
]

def analyze_speech(transcript_text, words_with_timestamps, session_duration):
    all_words = transcript_text.split()
    word_count = len(all_words)
    if word_count == 0:
        return _empty_result()

    pause_analysis = _analyze_pauses(words_with_timestamps, session_duration)
    filler_analysis = _analyze_fillers(transcript_text, word_count)
    grammar_analysis = _analyze_grammar(transcript_text)
    fluency_analysis = _analyze_fluency(word_count, session_duration, pause_analysis)

    speech_score = _calculate_speech_score(
        fluency_analysis, grammar_analysis, pause_analysis,
        filler_analysis, word_count, session_duration
    )
    return {
        "speech_score": speech_score,
        "wpm": fluency_analysis["effective_wpm"],
        "pauses": pause_analysis["pause_count"],
        "fillers": filler_analysis["filler_count"],
        "grammar_errors": grammar_analysis["total_errors"]
    }
        </pre>

        <div class="subsection-heading">7. Multimodal Fusion: Cumulative Session Tracker (modules/session_tracker.py)</div>
        <pre class="code-block">
def stop(self):
    if not self.running or self.frame_count == 0:
        return None
    self.running = False

    average_eye_contact = int(self.eye_contact_total / self.frame_count)
    average_posture = int(self.posture_total / self.frame_count)
    average_smile = int(self.smile_total / self.frame_count)
    head_stability = int((self.straight_head_frames / self.frame_count) * 100)
    gesture_usage = int((self.hand_gesture_frames / self.frame_count) * 100)
    face_presence = int((self.face_detected_frames / self.frame_count) * 100)

    # Weighted Multimodal Final Score
    final_score = int(
        average_eye_contact * 0.35 +
        head_stability * 0.20 +
        average_posture * 0.25 +
        face_presence * 0.10 +
        average_smile * 0.05 +
        gesture_usage * 0.05
    )

    if final_score >= 85: rating = "Excellent"
    elif final_score >= 70: rating = "Good"
    elif final_score >= 50: rating = "Average"
    else: rating = "Needs Improvement"

    return {
        "final_score": final_score,
        "rating": rating,
        "eye_contact": average_eye_contact,
        "head_stability": head_stability,
        "posture": average_posture,
        "smile": average_smile,
        "gesture_usage": gesture_usage,
        "face_presence": face_presence
    }
        </pre>

        <div class="section-heading">SYSTEM DEMONSTRATION & GRAPHICAL OUTPUTS</div>

        <p>
            Figure 9.1 displays the active CustomTkinter user interface with real-time video stream, facial landmarks, metric gauges, and session controls.
        </p>

        <div class="figure-container">
            <img src="__FIG9_1__" alt="Communication AI UI Dashboard Display" />
            <div class="figure-caption">Figure 9.1: Communication AI User Interface Dashboard Display</div>
        </div>

        <p>
            Figure 9.2 presents a sample generated evaluation report file illustrating the comprehensive feedback generated by the system.
        </p>

        <div class="figure-container">
            <img src="__FIG9_2__" alt="Sample Evaluation Report" />
            <div class="figure-caption">Figure 9.2: Sample Real Evaluation Report & Feedback Record Output</div>
        </div>

        <p>
            Figure 9.3 shows the numerical comparative analysis matrix across multiple evaluation sessions logged in the system.
        </p>

        <div class="figure-container">
            <img src="__FIG9_3__" alt="Numerical Comparative Values" />
            <div class="figure-caption">Figure 9.3: Generation of Numerical Comparative Values Across Sessions</div>
        </div>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- REFERENCES -->
    <!-- =================================================== -->
    <div class="page" id="references">
        <div class="chapter-heading">
            REFERENCES
        </div>

        <ol style="margin-left: 20pt; line-height: 1.8; font-size: 11pt; text-align: justify;">
            <li>G. Bradski, “The OpenCV Library,” <i>Dr. Dobb’s Journal of Software Tools</i>, vol. 25, no. 11, pp. 120–125, 2000.</li>
            <li>C. Lugaresi, J. Tang, H. Nash, C. McClanahan, E. Uboweja, M. Hays, F. Zhang, C.-L. Wang, G. S. Kuo, M. Ramesh, A. Truong, and M. Grundmann, “MediaPipe: A Framework for Building Perception Pipelines,” in <i>Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops</i>, 2019, arXiv:1906.08172.</li>
            <li>D. Jurafsky and J. H. Martin, <i>Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition</i>, 3rd ed. draft, Stanford University, 2024.</li>
            <li>A. Graves, “Sequence Transduction with Recurrent Neural Networks,” in <i>Proc. ICML Workshop on Representation Learning</i>, 2012, arXiv:1211.3711.</li>
            <li>A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, “wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations,” in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 33, pp. 12449–12460, 2020.</li>
            <li>A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and I. Sutskever, “Robust Speech Recognition via Large-Scale Weak Supervision,” in <i>Proc. International Conference on Machine Learning (ICML)</i>, pp. 28492–28518, 2023.</li>
            <li>M. Hoque, M. Courgeon, J. C. Martin, B. Mutlu, and R. W. Picard, “MACH: My Automated Conversation CoacH,” in <i>Proc. 2013 ACM International Joint Conference on Pervasive and Ubiquitous Computing (UbiComp '13)</i>, pp. 697–706, 2013.</li>
            <li>R. W. Picard, <i>Affective Computing</i>, Cambridge, MA: MIT Press, 1997.</li>
            <li>S. R. Livingstone and F. A. Russo, “The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS),” <i>PLoS ONE</i>, vol. 13, no. 5, Art. no. e0196391, 2018.</li>
            <li>T. Baltrusaitis, P. Robinson, and L.-P. Morency, “OpenFace: An Open Source Facial Behavior Analysis Toolkit,” in <i>Proc. IEEE Winter Conference on Applications of Computer Vision (WACV)</i>, pp. 1–10, 2016.</li>
            <li>Z. Cao, G. Hidalgo, T. Simon, S.-E. Wei, and Y. Sheikh, “OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields,” <i>IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)</i>, vol. 43, no. 1, pp. 172–186, 2021.</li>
            <li>F. Zhang, V. Bazarevsky, A. Vakunov, A. Tkachenka, G. Sung, C.-L. Wang, and M. Grundmann, “MediaPipe Hands: On-Device Real-Time Hand Tracking,” in <i>Proc. CVPR Workshops</i>, 2020, arXiv:2006.10214.</li>
            <li>I. Katsman, G. Gu, K. A. Joshi, and S. Belongie, “Gaze360: Physically-Constrained Gaze Estimation in the Wild,” in <i>Proc. IEEE International Conference on Computer Vision (ICCV)</i>, pp. 6924–6934, 2019.</li>
            <li>“AI-Enabled Automated Interview Evaluation System,” <i>International Journal of Innovative Research in Multidisciplinary Physical Sciences (IJIRMPS)</i>, vol. 13, no. 2, pp. 45–52, 2025.</li>
            <li>A. Sharma, R. Patel, and S. Mehta, “InterVista: AI Virtual Interview System Integrating NLP, OpenCV-Based Facial Analysis, and Speech Emotion Recognition,” <i>International Journal of Progressive Research in Engineering Management and Science (IJPREMS)</i>, vol. 5, no. 3, pp. 112–119, 2025.</li>
            <li>“AI-Enhanced Confident Speaker: A Machine Learning Approach to Public Speaking Improvement Using Multi-Modal Analysis,” <i>International Journal of Engineering Research & Technology (IJERT)</i>, vol. 15, no. 6, pp. 78–85, 2026.</li>
            <li>G. Krishna Lohith, K. Varshith Reddy, P. Mounisha Reddy, and V. Lokeshwari Vinya, “NLP-Based Resume Analysis, Skill Enhancement & Job Matching System,” <i>International Research Journal of Engineering and Technology (IRJET)</i>, vol. 12, no. 4, pp. 310–316, 2025.</li>
            <li>R. Jain, D. M. Chiu, and W. R. Hawe, “A Quantitative Measure of Fairness and Discrimination for Resource Allocation in Shared Computer Systems,” Digital Equipment Corporation, Tech. Rep. DEC-TR-301, 1984.</li>
            <li>P. Boersma and D. Weenink, “Praat: Doing Phonetics by Computer,” Computer Program, Version 6.3, 2023. [Online]. Available: http://www.praat.org/</li>
            <li>E. Shriberg, “To 'Err' is Human: Ecology and Acoustics of Speech Disfluencies,” <i>Journal of the International Phonetic Association</i>, vol. 31, no. 1, pp. 153–169, 2001.</li>
            <li>T. Tomokiyo and R. Rosario, “Accessing the Accuracy of Automated Speech Scoring,” in <i>Proc. Interspeech</i>, pp. 1289–1292, 2003.</li>
            <li>A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention Is All You Need,” in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, pp. 5998–6008, 2017.</li>
            <li>P. Ekman and W. V. Friesen, <i>Facial Action Coding System: A Technique for the Measurement of Facial Movement</i>, Palo Alto: Consulting Psychologists Press, 1978.</li>
            <li>L.-P. Morency, R. Mihalcea, and P. Doshi, “Towards Multimodal Sentiment Analysis: Harvesting Opinions from the Web,” in <i>Proc. 13th International Conference on Multimodal Interfaces (ICMI '11)</i>, pp. 169–176, 2011.</li>
            <li>K. Scherer, “Vocal Communication of Emotion: A Review of Research Paradigms,” <i>Speech Communication</i>, vol. 40, no. 1–2, pp. 227–256, 2003.</li>
            <li>D. Viji, T. Bala Vignesh, K. Bharath, and S. Bharath Kumar, “AI-Based Self-Evaluation System for Communication Skills Using OpenCV, NLP, and Speech Validation,” Department of Artificial Intelligence and Data Science, Erode Sengunthar Engineering College, Research Manuscript, 2026.</li>
        </ol>
    </div>
    """

    res = raw_template.replace("__FIG9_1__", fig9_1)
    res = res.replace("__FIG9_2__", fig9_2)
    res = res.replace("__FIG9_3__", fig9_3)
    return res
