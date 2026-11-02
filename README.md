# AI-Based Communication Skills Evaluation

An AI-powered application designed to evaluate and improve an individual's communication skills using computer vision, facial analysis, posture detection, hand gestures, and speech analysis.

## Project Overview

The AI-Based Communication Skills Evaluation system analyzes a user's communication performance through a webcam and microphone. It evaluates visual and speech-related parameters and provides feedback to help users improve their communication skills.

The application provides a graphical user interface to conduct evaluations and review performance analytics.

## Key Features

- **Eye Contact Detection:** Evaluates eye contact using facial landmarks.
- **Facial Expression Analysis:** Identifies facial expressions and smile-related behavior.
- **Head Pose Estimation:** Analyzes head movement and stability.
- **Posture Detection:** Evaluates body posture during communication.
- **Hand Gesture Recognition:** Analyzes hand gestures.
- **Speech Analysis:** Records and analyzes speech.
- **Speech-to-Text:** Uses Whisper for speech transcription.
- **Performance Evaluation:** Provides communication scores and feedback.
- **Person-Based Analytics:** Maintains individual evaluation history.
- **Report Generation:** Generates evaluation reports.
- **Graphical User Interface:** Provides an interactive desktop application.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Computer vision |
| MediaPipe | Face and landmark detection |
| NumPy | Numerical processing |
| CustomTkinter | Graphical user interface |
| Pillow | Image processing |
| Matplotlib | Data visualization |
| SoundDevice | Audio recording |
| SciPy | Audio processing |
| Whisper | Speech-to-text conversion |

## Project Structure

```text
Communication-AI/
│
├── app.py
├── Start_Communication_AI.bat
├── start_app.cmd
├── requirements.txt
│
├── modules/
│   ├── analytics.py
│   ├── audio_recorder.py
│   ├── eye_contact.py
│   ├── face_detection.py
│   ├── face_mesh.py
│   ├── feedback.py
│   ├── hand_gesture.py
│   ├── head_pose.py
│   ├── posture.py
│   ├── report_manager.py
│   ├── session_tracker.py
│   ├── smile.py
│   ├── speech_analyzer.py
│   └── speech_to_text.py
│
├── nlp/
├── report_assets/
└── AI_Based_Communication_Skills_Project_Report.pdf
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Bharathcrush/Communication-AI.git
```

### 2. Open the Project Folder

```bash
cd Communication-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

You can also use `Start_Communication_AI.bat` on Windows if the environment and dependencies are configured.

## How the System Works

1. The user launches the application.
2. The user selects an existing person or creates a new person profile.
3. The webcam captures facial and body movements.
4. The system analyzes eye contact, facial expressions, head pose, posture, and hand gestures.
5. The microphone records the user's speech.
6. Speech processing generates transcription and communication-related analysis.
7. The application calculates performance scores and provides feedback.
8. Evaluation history and reports can be reviewed.

## Project Report

The detailed project report is available in the repository:

`AI_Based_Communication_Skills_Project_Report.pdf`

## Author

**S. Bharath Kumar**

## Repository

GitHub: https://github.com/Bharathcrush/Communication-AI

---

*AI-Based Communication Skills Evaluation – An intelligent approach to improving communication through artificial intelligence.*
