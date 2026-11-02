# -*- coding: utf-8 -*-
"""
Preliminary Pages Content:
- Page 1: Title Page
- Page 2: Bonafide Certificate
- Page 3: Acknowledgement (iii)
- Page 4: Abstract (iv)
- Pages 5-9: Table of Contents (v, vi, vii, viii, ix)
- Page 10: List of Figures (x)
- Page 11: List of Tables (xi)
- Page 12: Abbreviation (xii)
"""

def get_prelim_html(logo_esec, logo_au, toc_data=None, lof_data=None, lot_data=None):
    if not toc_data:
        toc_data = {
            "abstract": "iv",
            "abbreviation": "xii",
            "list_of_figures": "x",
            "list_of_tables": "xi",
            "chap1": "13",
            "chap2": "22",
            "chap3": "31",
            "chap4": "40",
            "chap5": "53",
            "chap6": "65",
            "chap7": "73",
            "chap8": "81",
            "chap9": "86",
            "references": "116"
        }

    if not lof_data:
        lof_data = {
            "fig4_1": "43",
            "fig4_2": "45",
            "fig4_3": "48",
            "fig5_1": "55",
            "fig5_2": "57",
            "fig5_3": "59",
            "fig6_1": "68",
            "fig6_2": "69",
            "fig9_1": "112",
            "fig9_2": "113",
            "fig9_3": "114"
        }

    if not lot_data:
        lot_data = {
            "tab3_1": "38",
            "tab3_2": "39",
            "tab5_1": "54",
            "tab6_1": "66",
            "tab6_2": "67",
            "tab7_1": "78"
        }

    html = f"""
    <!-- =================================================== -->
    <!-- 1. TITLE PAGE (Page 1) -->
    <!-- =================================================== -->
    <div class="cover-page" style="height: 940pt; box-sizing: border-box; padding-top: 20pt; text-align: center;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25pt;">
            <img src="{logo_esec}" style="height: 80pt; width: auto;" alt="ESEC Logo" />
            <img src="{logo_au}" style="height: 80pt; width: auto;" alt="Anna University Logo" />
        </div>

        <h1 style="font-size: 15pt; font-weight: bold; line-height: 1.4; margin: 15pt 0 0 0; text-transform: uppercase;">
            AI-BASED SELF-EVALUATION SYSTEM FOR<br>
            COMMUNICATION SKILLS USING OPENCV, NLP,<br>
            AND SPEECH VALIDATION
        </h1>

        <div style="margin-top: 35pt; font-size: 12pt; font-weight: bold; letter-spacing: 0.5px;">
            A MINI PROJECT REPORT
        </div>

        <div style="margin-top: 25pt; font-size: 12pt; font-style: italic;">
            Submitted by
        </div>

        <table style="margin: 25pt auto 0 auto; width: 85%; font-size: 12pt; font-weight: bold; border-collapse: collapse; border: none;">
            <tr style="border: none;">
                <td style="text-align: left; padding: 4pt 0; border: none;">BALA VIGNESH T</td>
                <td style="text-align: right; padding: 4pt 0; border: none;">730424321012</td>
            </tr>
            <tr style="border: none;">
                <td style="text-align: left; padding: 4pt 0; border: none;">BHARATH K</td>
                <td style="text-align: right; padding: 4pt 0; border: none;">730424321014</td>
            </tr>
            <tr style="border: none;">
                <td style="text-align: left; padding: 4pt 0; border: none;">BHARATH KUMAR S</td>
                <td style="text-align: right; padding: 4pt 0; border: none;">730424321015</td>
            </tr>
        </table>

        <div style="margin-top: 35pt; font-size: 11pt; font-style: italic;">
            in partial fulfilment for the award of the degree<br>of
        </div>

        <div style="margin-top: 20pt; font-size: 13pt; font-weight: bold;">
            BACHELOR OF TECHNOLOGY
        </div>
        <div style="margin-top: 8pt; font-size: 11pt; font-style: italic;">
            in
        </div>
        <div style="margin-top: 8pt; font-size: 12pt; font-weight: bold;">
            ARTIFICIAL INTELLIGENCE AND DATA SCIENCE
        </div>

        <div style="margin-top: 40pt; font-size: 12pt; font-weight: bold; line-height: 1.3;">
            ERODE SENGUNTHAR ENGINEERING COLLEGE<br>
            <span style="font-size: 11pt; font-weight: normal;">(AUTONOMOUS)</span><br>
            PERUNDURAI, ERODE-638057
        </div>

        <div style="margin-top: 35pt; font-size: 12pt; font-weight: bold; text-transform: uppercase;">
            NOVEMBER 2026
        </div>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 2. BONAFIDE CERTIFICATE (Page 2) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                ERODE SENGUNTHAR ENGINEERING COLLEGE
            </div>
            <div style="font-size: 11pt; font-weight: bold; margin-top: 4pt;">
                (AUTONOMOUS)
            </div>
            <div style="font-size: 11pt; font-weight: bold; margin-top: 4pt;">
                PERUNDURAI, ERODE – 638 057
            </div>
            <div style="font-size: 13pt; font-weight: bold; margin-top: 25pt; letter-spacing: 0.5px;">
                BONAFIDE CERTIFICATE
            </div>
        </div>

        <p style="text-align: justify; margin-top: 35pt; line-height: 1.8; font-size: 12pt; text-indent: 30pt;">
            Certified that this Project report <b>“AI-Based Self-Evaluation System for Communication Skills Using OpenCV, NLP, and Speech Validation”</b> is the bonafide work of <b>BALA VIGNESH T (730424321012)</b>, <b>BHARATH K (730424321014)</b> and <b>BHARATH KUMAR S (730424321015)</b>, who carried out the project work under my supervision. Certified further that to the best of my knowledge the work reported herein does not form part of any other thesis or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.
        </p>

        <div style="display: flex; justify-content: space-between; margin-top: 65pt; font-size: 11.5pt;">
            <div style="width: 45%; text-align: left; line-height: 1.4;">
                <div style="font-weight: bold; margin-bottom: 40pt;">SIGNATURE</div>
                <div style="font-weight: bold;">MS. D. VIJI, M.E.,</div>
                <div style="font-weight: bold; margin-top: 4pt;">SUPERVISOR</div>
                <div style="margin-top: 4pt;">Assistant Professor,</div>
                <div>Artificial Intelligence and Data Science,</div>
                <div>Erode Sengunthar Engineering College,</div>
                <div>Perundurai,</div>
                <div>Erode-638057.</div>
            </div>

            <div style="width: 45%; text-align: left; line-height: 1.4;">
                <div style="font-weight: bold; margin-bottom: 40pt;">SIGNATURE</div>
                <div style="font-weight: bold;">Dr. G. SARAVANAN, M.E., Ph.D.,</div>
                <div style="font-weight: bold; margin-top: 4pt;">HEAD OF THE DEPARTMENT</div>
                <div style="margin-top: 4pt;">Professor,</div>
                <div>Artificial Intelligence and Data Science,</div>
                <div>Erode Sengunthar Engineering College,</div>
                <div>Perundurai,</div>
                <div>Erode-638057.</div>
            </div>
        </div>

        <div style="margin-top: 65pt; text-align: center; font-size: 11.5pt;">
            Submitted for End Semester Project work Viva-voce Examination held on ___________________
        </div>

        <div style="display: flex; justify-content: space-between; margin-top: 60pt; font-size: 11.5pt; font-weight: bold;">
            <div style="width: 45%; text-align: center;">INTERNAL EXAMINER</div>
            <div style="width: 45%; text-align: center;">EXTERNAL EXAMINER</div>
        </div>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 3. ACKNOWLEDGEMENT (Page 3 / iii) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                ACKNOWLEDGEMENT
            </div>
        </div>

        <p style="text-align: justify; margin-top: 35pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            It is our privilege to express our sincere and heartfelt thanks to our Correspondent <b>Thiru. G. KAMALAMURUGAN</b> for giving opportunity to study in this prestigious institution.
        </p>

        <p style="text-align: justify; margin-top: 20pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            We feel immense pleasure and deep gratitude in thanking our Secretary, <b>Thiru. S. N. THANGARAJU</b> for his well-intentioned support throughout our academic career.
        </p>

        <p style="text-align: justify; margin-top: 20pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            We are indebted to our Principal <b>Dr. V. VENKATACHALAM, B.E., M.Tech., M.S., Ph.D.</b>, for his constant encouragement throughout our career.
        </p>

        <p style="text-align: justify; margin-top: 20pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            We express our sincere thanks to <b>Dr. G. SARAVANAN, M.E., Ph.D.</b>, Head of the Department, Artificial Intelligence and Data Science for his valuable suggestions throughout the academic venture.
        </p>

        <p style="text-align: justify; margin-top: 20pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            We extend our gratitude and sincere thanks to our Project Coordinator and Supervisor <b>Ms. D. VIJI, M.E.</b>, Assistant Professor, Department of Artificial Intelligence and Data Science for her valuable support, continuous guidance, and encouragement for our project.
        </p>

        <p style="text-align: justify; margin-top: 20pt; line-height: 1.85; font-size: 12pt; text-indent: 30pt;">
            We put forward our sincere thanks to all our esteemed teaching and non-teaching staff members of Artificial Intelligence and Data Science Department, parents and friends for their continuous support throughout this academic endeavor.
        </p>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 4. ABSTRACT (Page 4 / iv) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                ABSTRACT
            </div>
        </div>

        <p style="text-align: justify; margin-top: 30pt; line-height: 1.75; font-size: 12pt; text-indent: 30pt;">
            Effective interpersonal communication represents an essential determinant of professional, academic, and career success. Whether participating in competitive placement interviews, delivering technical presentations, or engaging in professional discourse, candidates are rigorously evaluated on both verbal and non-verbal behaviors. Traditional communication coaching and mock interview assessments rely predominantly on manual evaluations conducted by human trainers. However, human evaluation is inherently constrained by subjective grading inconsistencies, observer fatigue, high logistical scheduling friction, and an inability to provide synchronous, multi-dimensional tracking during self-paced practice.
        </p>

        <p style="text-align: justify; margin-top: 15pt; line-height: 1.75; font-size: 12pt; text-indent: 30pt;">
            To overcome these foundational limitations, this project presents the design, development, and experimental validation of an <b>AI-Based Self-Evaluation System for Communication Skills Using OpenCV, NLP, and Speech Validation</b>. The developed framework delivers an integrated, real-time multimodal evaluation platform that synchronizes computer vision, speech acoustics, and natural language processing into a unified feedback architecture. Using OpenCV alongside MediaPipe Face Mesh, Pose, and Hands pipelines, the system tracks 468 dense facial landmarks and skeletal joints at 30 frames per second to evaluate critical non-verbal behavioral cues, including eye contact percentage via horizontal iris-to-screen center offset, head pose stability through nose-to-face midline yaw estimation, spinal posture alignment via bilateral shoulder elevation deviation, smiling dynamics with temporal moving average filtering, and hand gesture frequency.
        </p>

        <p style="text-align: justify; margin-top: 15pt; line-height: 1.75; font-size: 12pt; text-indent: 30pt;">
            Simultaneously, a multi-threaded audio acquisition engine captures raw speech at 16 kHz mono, applies Butterworth bandpass filtering, and performs automated speech transcription using the OpenAI Whisper transformer architecture. The extracted word timestamps and transcript undergo comprehensive linguistic and acoustic evaluation to quantify speaking rate (Words Per Minute), pause and silence duration, hesitation and filler-word density (such as <i>um</i>, <i>uh</i>, <i>like</i>, and <i>actually</i>), grammatical syntax coherence, and lexical diversity. An automated multimodal scoring engine fuses visual and speech metrics into an interpretable 0–100 overall communication score, categorized into objective proficiency ratings accompanied by transparent strengths, targeted improvement areas, and actionable pedagogical suggestions. Experimental validation on multiple test subjects demonstrates strong tracking fidelity, high transcription accuracy (WER &lt; 6.8%), robust real-time throughput, and effective performance improvement across repeated practice sessions.
        </p>

        <p style="text-align: justify; margin-top: 25pt; line-height: 1.6; font-size: 11pt;">
            <b>Keywords:</b> Communication Skills, OpenCV, MediaPipe, Computer Vision, Speech Recognition, Whisper STT, Natural Language Processing, Multimodal Evaluation, Acoustic Analysis, Self-Paced Learning.
        </p>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 5. TABLE OF CONTENTS - PAGE 1 (Page 5 / v) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                TABLE OF CONTENTS
            </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 25pt; font-size: 11pt; border: none; line-height: 1.65;">
            <tr style="border-bottom: 1px solid #000; font-weight: bold;">
                <td style="width: 15%; padding: 4pt 0; border: none;">CHAPTER NO.</td>
                <td style="width: 70%; padding: 4pt 0; text-align: left; border: none;">TITLE</td>
                <td style="width: 15%; padding: 4pt 0; text-align: right; border: none;">PAGE NO.</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none; font-weight: bold;">ABSTRACT</td>
                <td style="border: none; text-align: right; font-weight: bold;">{toc_data['abstract']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none; font-weight: bold;">LIST OF FIGURES</td>
                <td style="border: none; text-align: right; font-weight: bold;">{toc_data['list_of_figures']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none; font-weight: bold;">LIST OF TABLES</td>
                <td style="border: none; text-align: right; font-weight: bold;">{toc_data['list_of_tables']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none; font-weight: bold;">ABBREVIATION</td>
                <td style="border: none; text-align: right; font-weight: bold;">{toc_data['abbreviation']}</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">1</td>
                <td style="border: none;">INTRODUCTION</td>
                <td style="border: none; text-align: right;">{toc_data['chap1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.1 Communication Dynamics in Academic and Professional Domains</td>
                <td style="border: none; text-align: right;">14</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.2 Evolution of Communication Assessment & Mock Interview Systems</td>
                <td style="border: none; text-align: right;">15</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.3 Role of Computer Vision, Speech Processing, and NLP</td>
                <td style="border: none; text-align: right;">16</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.4 Problem Statement</td>
                <td style="border: none; text-align: right;">18</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.5 Objectives of the Study</td>
                <td style="border: none; text-align: right;">19</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.6 Scope of the Project</td>
                <td style="border: none; text-align: right;">20</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.7 Methodology Overview</td>
                <td style="border: none; text-align: right;">21</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">1.8 Significance and Impact of the Project</td>
                <td style="border: none; text-align: right;">23</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 5. TABLE OF CONTENTS - PAGE 2 (Page 6 / vi) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11pt; border: none; line-height: 1.65;">
            <tr style="border-none; font-weight: bold;">
                <td style="width: 15%; border: none;">2</td>
                <td style="width: 70%; border: none;">LITERATURE REVIEW</td>
                <td style="width: 15%; border: none; text-align: right;">{toc_data['chap2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.1 Introduction</td>
                <td style="border: none; text-align: right;">24</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.2 Evolution of Communication Assessment Techniques</td>
                <td style="border: none; text-align: right;">25</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.3 Computer Vision for Non-Verbal Behavioral Analysis</td>
                <td style="border: none; text-align: right;">26</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.3.1 Facial Landmark Extraction & Morphology</td>
                <td style="border: none; text-align: right;">26</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.3.2 Gaze Tracking & Iris Proximity Quantification</td>
                <td style="border: none; text-align: right;">27</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.3.3 Pose Estimation & Skeletal Posture Dynamics</td>
                <td style="border: none; text-align: right;">28</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.3.4 Hand Gesture Detection in Public Speaking</td>
                <td style="border: none; text-align: right;">29</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.4 Automatic Speech Recognition & Acoustic Processing</td>
                <td style="border: none; text-align: right;">30</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.4.1 Speech-to-Text: From HMMs to Whisper Transformers</td>
                <td style="border: none; text-align: right;">30</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.4.2 Speaking Rate (WPM) & Pause Quantification</td>
                <td style="border: none; text-align: right;">31</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;2.4.3 Disfluency Modeling & Filler Word Detection</td>
                <td style="border: none; text-align: right;">32</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.5 Natural Language Processing for Verbal Performance</td>
                <td style="border: none; text-align: right;">32</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.6 Multimodal Information Fusion in Behavioral Computing</td>
                <td style="border: none; text-align: right;">33</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.7 Existing Systems & Comparative Research Contributions</td>
                <td style="border: none; text-align: right;">33</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.8 Identification of Research Gaps</td>
                <td style="border: none; text-align: right;">34</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">2.9 Summary</td>
                <td style="border: none; text-align: right;">34</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">3</td>
                <td style="border: none;">SYSTEM ANALYSIS</td>
                <td style="border: none; text-align: right;">{toc_data['chap3']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.1 Introduction</td>
                <td style="border: none; text-align: right;">35</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.2 Problem Definition</td>
                <td style="border: none; text-align: right;">35</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.3 Existing System & Limitations</td>
                <td style="border: none; text-align: right;">36</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.4 Proposed Multimodal Evaluation System</td>
                <td style="border: none; text-align: right;">37</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 5. TABLE OF CONTENTS - PAGE 3 (Page 7 / vii) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11pt; border: none; line-height: 1.65;">
            <tr style="border: none;">
                <td style="width: 15%; border: none;"></td>
                <td style="width: 70%; border: none;">3.5 Objectives of the System</td>
                <td style="width: 15%; border: none; text-align: right;">38</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.6 System Requirements Specification</td>
                <td style="border: none; text-align: right;">39</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.6.1 Hardware Requirements</td>
                <td style="border: none; text-align: right;">39</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.6.2 Software Requirements</td>
                <td style="border: none; text-align: right;">39</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.6.3 Functional Requirements</td>
                <td style="border: none; text-align: right;">40</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.6.4 Non-Functional Requirements</td>
                <td style="border: none; text-align: right;">40</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.7 Feasibility Study</td>
                <td style="border: none; text-align: right;">41</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.7.1 Technical Feasibility</td>
                <td style="border: none; text-align: right;">41</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.7.2 Economic Feasibility</td>
                <td style="border: none; text-align: right;">41</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;3.7.3 Operational Feasibility</td>
                <td style="border: none; text-align: right;">42</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.8 System Architecture Overview</td>
                <td style="border: none; text-align: right;">42</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.9 Advantages of the Proposed System</td>
                <td style="border: none; text-align: right;">43</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">3.10 Limitations of the Proposed System</td>
                <td style="border: none; text-align: right;">44</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">4</td>
                <td style="border: none;">PROPOSED WORK</td>
                <td style="border: none; text-align: right;">{toc_data['chap4']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.1 Architecture Overview</td>
                <td style="border: none; text-align: right;">45</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.2 Objectives of the Proposed Work</td>
                <td style="border: none; text-align: right;">46</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.3 Multimodal System Pipeline</td>
                <td style="border: none; text-align: right;">46</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.4 Detailed System Architecture</td>
                <td style="border: none; text-align: right;">47</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.5 Workflow of the System</td>
                <td style="border: none; text-align: right;">49</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.6 Mathematical & Algorithmic Framework</td>
                <td style="border: none; text-align: right;">51</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.1 Eye Contact Score Formulation</td>
                <td style="border: none; text-align: right;">51</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.2 Head Pose Yaw Estimation Formulation</td>
                <td style="border: none; text-align: right;">51</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.3 Smile & Expression Detection Formulation</td>
                <td style="border: none; text-align: right;">52</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 5. TABLE OF CONTENTS - PAGE 4 (Page 8 / viii) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11pt; border: none; line-height: 1.65;">
            <tr style="border: none;">
                <td style="width: 15%; border: none;"></td>
                <td style="width: 70%; border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.4 Posture Alignment Formulation</td>
                <td style="width: 15%; border: none; text-align: right;">52</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.5 Hand Gesture Dynamics Formulation</td>
                <td style="border: none; text-align: right;">52</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.6 Fluency, WPM & Pause Metric Formulation</td>
                <td style="border: none; text-align: right;">53</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.7 Speech Evaluation Scoring Model (10 Pts)</td>
                <td style="border: none; text-align: right;">53</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;4.6.8 Multimodal Final Communication Score</td>
                <td style="border: none; text-align: right;">54</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.7 Module Descriptions</td>
                <td style="border: none; text-align: right;">54</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.8 Data Flow Diagrams (DFD)</td>
                <td style="border: none; text-align: right;">55</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.9 Advantages of the Proposed Work</td>
                <td style="border: none; text-align: right;">55</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.10 Innovations Introduced</td>
                <td style="border: none; text-align: right;">56</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">4.11 Summary</td>
                <td style="border: none; text-align: right;">56</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">5</td>
                <td style="border: none;">IMPLEMENTATION METHODOLOGY</td>
                <td style="border: none; text-align: right;">{toc_data['chap5']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.1 System Development Environment</td>
                <td style="border: none; text-align: right;">58</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.2 Implementation Strategy</td>
                <td style="border: none; text-align: right;">60</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.3 Computer Vision Pipeline Implementation</td>
                <td style="border: none; text-align: right;">61</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.1 Video Capture & Frame Preprocessing</td>
                <td style="border: none; text-align: right;">61</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.2 MediaPipe Face Mesh & Iris Tracking</td>
                <td style="border: none; text-align: right;">62</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.3 Head Pose Estimation Algorithm</td>
                <td style="border: none; text-align: right;">63</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.4 MediaPipe Pose & Shoulder Alignment</td>
                <td style="border: none; text-align: right;">64</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.5 MediaPipe Hands & Gesture Quantification</td>
                <td style="border: none; text-align: right;">64</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.3.6 Smile Detection with Temporal Smoothing</td>
                <td style="border: none; text-align: right;">65</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.4 Speech Processing & NLP Pipeline Implementation</td>
                <td style="border: none; text-align: right;">66</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 5. TABLE OF CONTENTS - PAGE 5 (Page 9 / ix) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11pt; border: none; line-height: 1.65;">
            <tr style="border: none;">
                <td style="width: 15%; border: none;"></td>
                <td style="width: 70%; border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.1 Threaded Audio Capture with SoundDevice</td>
                <td style="width: 15%; border: none; text-align: right;">66</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.2 Audio Bandpass Filtering & Resampling</td>
                <td style="border: none; text-align: right;">67</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.3 OpenAI Whisper Speech Transcription</td>
                <td style="border: none; text-align: right;">67</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.4 Pause, Silence, & Disfluency Detection</td>
                <td style="border: none; text-align: right;">68</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.5 Filler Word Identification & Matching</td>
                <td style="border: none; text-align: right;">68</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">&nbsp;&nbsp;&nbsp;&nbsp;5.4.6 Grammatical Syntax Analysis</td>
                <td style="border: none; text-align: right;">69</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.5 Scoring Engine & Feedback Generator Implementation</td>
                <td style="border: none; text-align: right;">69</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.6 User Interface & Dashboard Implementation</td>
                <td style="border: none; text-align: right;">70</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.7 Data Persistence & Report Management</td>
                <td style="border: none; text-align: right;">70</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.8 Testing Methodology</td>
                <td style="border: none; text-align: right;">71</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;"></td>
                <td style="border: none;">5.9 Deployment Considerations</td>
                <td style="border: none; text-align: right;">71</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">6</td>
                <td style="border: none;">EXPERIMENTAL SETUP AND RESULTS</td>
                <td style="border: none; text-align: right;">{toc_data['chap6']}</td>
            </tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">7</td>
                <td style="border: none;">CHALLENGES AND LIMITATIONS</td>
                <td style="border: none; text-align: right;">{toc_data['chap7']}</td>
            </tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">8</td>
                <td style="border: none;">CONCLUSION AND FUTURE SCOPE</td>
                <td style="border: none; text-align: right;">{toc_data['chap8']}</td>
            </tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;">9</td>
                <td style="border: none;">APPENDIX</td>
                <td style="border: none; text-align: right;">{toc_data['chap9']}</td>
            </tr>
            <tr style="border: none; font-weight: bold;">
                <td style="border: none;"></td>
                <td style="border: none;">REFERENCES</td>
                <td style="border: none; text-align: right;">{toc_data['references']}</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 6. LIST OF FIGURES (Page 10 / x) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                LIST OF FIGURES
            </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 30pt; font-size: 11pt; border: none; line-height: 1.8;">
            <tr style="border-bottom: 1px solid #000; font-weight: bold;">
                <td style="width: 15%; padding: 4pt 0; border: none;">FIG NO.</td>
                <td style="width: 70%; padding: 4pt 0; text-align: left; border: none;">DESCRIPTION</td>
                <td style="width: 15%; padding: 4pt 0; text-align: right; border: none;">PAGE NO.</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none;">
                <td style="border: none;">4.1</td>
                <td style="border: none;">System Architecture Diagram</td>
                <td style="border: none; text-align: right;">{lof_data['fig4_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">4.2</td>
                <td style="border: none;">System Operational Workflow Diagram</td>
                <td style="border: none; text-align: right;">{lof_data['fig4_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">4.3</td>
                <td style="border: none;">Data Flow Diagram (DFD Level 0 & Level 1)</td>
                <td style="border: none; text-align: right;">{lof_data['fig4_3']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">5.1</td>
                <td style="border: none;">MediaPipe 468-Point Face Mesh & Iris Landmark Tracking</td>
                <td style="border: none; text-align: right;">{lof_data['fig5_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">5.2</td>
                <td style="border: none;">Shoulder Posture Alignment & Geometric Calculation</td>
                <td style="border: none; text-align: right;">{lof_data['fig5_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">5.3</td>
                <td style="border: none;">Whisper Speech-to-Text & Acoustic Analysis Pipeline</td>
                <td style="border: none; text-align: right;">{lof_data['fig5_3']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">6.1</td>
                <td style="border: none;">Multimodal Communication Performance Radar Analysis</td>
                <td style="border: none; text-align: right;">{lof_data['fig6_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">6.2</td>
                <td style="border: none;">Speech Validation & NLP Acoustic Performance Metrics</td>
                <td style="border: none; text-align: right;">{lof_data['fig6_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">9.1</td>
                <td style="border: none;">Communication AI User Interface Dashboard Display</td>
                <td style="border: none; text-align: right;">{lof_data['fig9_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">9.2</td>
                <td style="border: none;">Sample Real Evaluation Report & Feedback Record</td>
                <td style="border: none; text-align: right;">{lof_data['fig9_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">9.3</td>
                <td style="border: none;">Generation of Numerical Comparative Values Across Sessions</td>
                <td style="border: none; text-align: right;">{lof_data['fig9_3']}</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 7. LIST OF TABLES (Page 11 / xi) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                LIST OF TABLES
            </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 30pt; font-size: 11pt; border: none; line-height: 1.8;">
            <tr style="border-bottom: 1px solid #000; font-weight: bold;">
                <td style="width: 15%; padding: 4pt 0; border: none;">TABLE NO.</td>
                <td style="width: 70%; padding: 4pt 0; text-align: left; border: none;">DESCRIPTION</td>
                <td style="width: 15%; padding: 4pt 0; text-align: right; border: none;">PAGE NO.</td>
            </tr>
            <tr style="border: none;"><td colspan="3" style="padding: 4pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none;">
                <td style="border: none;">3.1</td>
                <td style="border: none;">Hardware Environment and Component Specifications</td>
                <td style="border: none; text-align: right;">{lot_data['tab3_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">3.2</td>
                <td style="border: none;">Software Dependencies and Operational Purpose</td>
                <td style="border: none; text-align: right;">{lot_data['tab3_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">5.1</td>
                <td style="border: none;">Development Toolchain and Implementation Roles</td>
                <td style="border: none; text-align: right;">{lot_data['tab5_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">6.1</td>
                <td style="border: none;">Experimental Testbed Setup and Testing Parameters</td>
                <td style="border: none; text-align: right;">{lot_data['tab6_1']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">6.2</td>
                <td style="border: none;">Empirical Performance Metrics Across Evaluation Sessions</td>
                <td style="border: none; text-align: right;">{lot_data['tab6_2']}</td>
            </tr>
            <tr style="border: none;">
                <td style="border: none;">7.1</td>
                <td style="border: none;">Identified Limitations and Proposed Technical Enhancements</td>
                <td style="border: none; text-align: right;">{lot_data['tab7_1']}</td>
            </tr>
        </table>
    </div>
    <div class="page-break"></div>

    <!-- =================================================== -->
    <!-- 8. ABBREVIATION (Page 12 / xii) -->
    <!-- =================================================== -->
    <div style="height: 940pt; box-sizing: border-box; padding-top: 20pt;">
        <div style="text-align: center;">
            <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">
                ABBREVIATION
            </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 30pt; font-size: 11pt; border: none; line-height: 1.75;">
            <tr style="border-bottom: 1px solid #000; font-weight: bold;">
                <td style="width: 25%; padding: 4pt 0; text-align: left; border: none;">Abbreviation</td>
                <td style="width: 75%; padding: 4pt 0; text-align: left; border: none;">Expansion</td>
            </tr>
            <tr style="border: none;"><td colspan="2" style="padding: 2pt 0; border: none;">&nbsp;</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">AI</td><td style="border: none;">Artificial Intelligence</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">API</td><td style="border: none;">Application Programming Interface</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">ASR</td><td style="border: none;">Automatic Speech Recognition</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">B.Tech</td><td style="border: none;">Bachelor of Technology</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">CPU</td><td style="border: none;">Central Processing Unit</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">CSV</td><td style="border: none;">Comma-Separated Values</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">CV</td><td style="border: none;">Computer Vision</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">DFD</td><td style="border: none;">Data Flow Diagram</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">EWPM</td><td style="border: none;">Effective Words Per Minute</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">FPS</td><td style="border: none;">Frames Per Second</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">GPU</td><td style="border: none;">Graphics Processing Unit</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">GUI</td><td style="border: none;">Graphical User Interface</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">HOD</td><td style="border: none;">Head of the Department</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">HTML</td><td style="border: none;">HyperText Markup Language</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">IEEE</td><td style="border: none;">Institute of Electrical and Electronics Engineers</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">JSON</td><td style="border: none;">JavaScript Object Notation</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">ML</td><td style="border: none;">Machine Learning</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">NLP</td><td style="border: none;">Natural Language Processing</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">OpenCV</td><td style="border: none;">Open Source Computer Vision Library</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">RGB</td><td style="border: none;">Red, Green, Blue</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">STT</td><td style="border: none;">Speech-to-Text</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">UI</td><td style="border: none;">User Interface</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">VAD</td><td style="border: none;">Voice Activity Detection</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">WAV</td><td style="border: none;">Waveform Audio File Format</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">WER</td><td style="border: none;">Word Error Rate</td></tr>
            <tr style="border: none;"><td style="border: none; font-weight: bold;">WPM</td><td style="border: none;">Words Per Minute</td></tr>
        </table>
    </div>
    <div class="page-break"></div>
    """
    return html
