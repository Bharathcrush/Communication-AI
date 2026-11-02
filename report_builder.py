# -*- coding: utf-8 -*-
"""
Full Project Report Generator for AI-Based Communication Evaluation System
Team:
1. Bala Vignesh T (ES23AD12 / 730424321012)
2. Bharath K (ES23AD14 / 730424321014)
3. Bharath Kumar S (ES23AD15 / 730424321015)

Institution: Erode Sengunthar Engineering College (Autonomous)
Department: Department of Artificial Intelligence and Data Science
Supervisor: Ms. D. Viji, M.E., Assistant Professor
Head of Department: Dr. G. Saravanan, M.E., Ph.D., Professor & HOD
"""

import os
import sys
import base64
import json
import subprocess
import io
from PIL import Image
import pypdf
from pypdf import PdfReader, PdfWriter
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

BASE_DIR = r"C:\OpenCV_Project"
ASSETS_DIR = os.path.join(BASE_DIR, "report_assets")

def img_to_b64(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    if ext == "jpg": ext = "jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{data}"

logo_esec = img_to_b64(os.path.join(ASSETS_DIR, "page1_img_0_Image11.jpg"))
logo_au = img_to_b64(os.path.join(ASSETS_DIR, "page1_img_1_Image12.png"))
fig4_1 = img_to_b64(os.path.join(ASSETS_DIR, "fig4_1_architecture.png"))
fig4_2 = img_to_b64(os.path.join(ASSETS_DIR, "fig4_2_flowchart.png"))
fig4_3 = img_to_b64(os.path.join(ASSETS_DIR, "fig4_3_dfd.png"))
fig5_1 = img_to_b64(os.path.join(ASSETS_DIR, "fig5_1_facemesh.png"))
fig5_2 = img_to_b64(os.path.join(ASSETS_DIR, "fig5_2_posture.png"))
fig5_3 = img_to_b64(os.path.join(ASSETS_DIR, "fig5_3_speech.png"))
fig6_1 = img_to_b64(os.path.join(ASSETS_DIR, "fig6_1_performance_radar.png"))
fig6_2 = img_to_b64(os.path.join(ASSETS_DIR, "fig6_2_speech_distribution.png"))
fig9_1 = img_to_b64(os.path.join(ASSETS_DIR, "fig9_1_dashboard.png"))
fig9_2 = img_to_b64(os.path.join(ASSETS_DIR, "fig9_2_report_output.png"))
fig9_3 = img_to_b64(os.path.join(ASSETS_DIR, "fig9_3_comparative_table.png"))

print("Generator base script initialized.")
