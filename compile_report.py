# -*- coding: utf-8 -*-
"""
Main Compiler for the Project Report:
1. Generates full_report.html
2. Performs 2-pass compilation via Chrome Headless
3. Detects exact chapter & figure page numbers
4. Stamps authentic collegiate Roman & Arabic page numbers
5. Outputs final PDF and Word DOCX
"""

import os
import sys
import subprocess
import shutil
import base64
from pypdf import PdfReader, PdfWriter
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

from report_builder import (
    logo_esec, logo_au, fig4_1, fig4_2, fig4_3,
    fig5_1, fig5_2, fig5_3, fig6_1, fig6_2,
    fig9_1, fig9_2, fig9_3
)
from report_content_prelim import get_prelim_html
from report_content_chap1_3 import get_chap1_3_html
from report_content_chap4_6 import get_chap4_6_html
from report_content_chap7_9 import get_chap7_9_html

BASE_DIR = r"C:\OpenCV_Project"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def build_html(toc_data=None, lof_data=None):
    prelim = get_prelim_html(logo_esec, logo_au, toc_data, lof_data)
    chap1_3 = get_chap1_3_html()
    chap4_6 = get_chap4_6_html(fig4_1, fig4_2, fig4_3, fig5_1, fig5_2, fig5_3, fig6_1, fig6_2)
    chap7_9 = get_chap7_9_html(fig9_1, fig9_2, fig9_3)

    css = """
    @page {
        size: A4 portrait;
        margin: 25mm 20mm 25mm 30mm; /* standard 30mm left margin for binding */
    }
    @page cover-page {
        margin: 20mm 20mm 20mm 20mm;
    }
    .cover-page {
        page: cover-page;
    }
    body {
        font-family: 'Times New Roman', Times, serif;
        font-size: 12pt;
        line-height: 1.5;
        color: #000000;
        margin: 0;
        padding: 0;
    }
    p {
        text-align: justify;
        margin-top: 0;
        margin-bottom: 12pt;
        text-indent: 0;
    }
    .page {
        page-break-after: always;
        break-after: page;
        box-sizing: border-box;
    }
    .page-break {
        page-break-after: always;
        break-after: page;
    }
    .chapter-heading {
        text-align: center;
        font-size: 14pt;
        font-weight: bold;
        margin-top: 20pt;
        margin-bottom: 24pt;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.3;
    }
    .section-heading {
        font-size: 12pt;
        font-weight: bold;
        margin-top: 18pt;
        margin-bottom: 8pt;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .subsection-heading {
        font-size: 12pt;
        font-weight: bold;
        margin-top: 14pt;
        margin-bottom: 6pt;
    }
    table.report-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 14pt;
        margin-bottom: 16pt;
        font-size: 10.5pt;
    }
    table.report-table th, table.report-table td {
        border: 1px solid #000;
        padding: 6pt 8pt;
        vertical-align: middle;
    }
    table.report-table th {
        background-color: #f2f2f2;
        font-weight: bold;
        text-align: center;
    }
    .figure-container {
        text-align: center;
        margin-top: 18pt;
        margin-bottom: 18pt;
        page-break-inside: avoid;
    }
    .figure-container img {
        max-width: 90%;
        max-height: 380pt;
        border: 1px solid #ccc;
        display: block;
        margin: 0 auto;
    }
    .figure-caption {
        font-size: 10.5pt;
        font-weight: bold;
        margin-top: 8pt;
        text-align: center;
    }
    pre.code-block {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.35;
        background-color: #f8f9fa;
        border: 1px solid #e2e8f0;
        padding: 10pt;
        margin-top: 10pt;
        margin-bottom: 14pt;
        white-space: pre-wrap;
        word-break: break-all;
        page-break-inside: avoid;
    }
    """

    full_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI-Based Self-Evaluation System for Communication Skills - Mini Project Report</title>
        <style>
        {css}
        </style>
    </head>
    <body>
        {prelim}
        {chap1_3}
        {chap4_6}
        {chap7_9}
    </body>
    </html>
    """
    return full_html

def render_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file:///{os.path.abspath(html_path)}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Chrome error:", res.stderr)
    return res.returncode == 0

def detect_page_numbers(pdf_path):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"Total pages rendered in pass 1: {total_pages}")

    toc_map = {}
    lof_map = {}

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        txt = page.extract_text() or ""

        # Check preliminary
        if "ABSTRACT" in txt and page_num > 2 and "abstract" not in toc_map:
            toc_map["abstract"] = "iv"
        if "ABBREVIATION" in txt and "abbreviation" not in toc_map:
            toc_map["abbreviation"] = "xi"
        if "LIST OF FIGURES" in txt and "list_of_figures" not in toc_map:
            toc_map["list_of_figures"] = "xii"

        # Check chapters
        if "CHAPTER 1" in txt and "INTRODUCTION" in txt and "chap1" not in toc_map:
            toc_map["chap1"] = str(page_num)
        if "CHAPTER 2" in txt and "LITERATURE REVIEW" in txt and "chap2" not in toc_map:
            toc_map["chap2"] = str(page_num)
        if "CHAPTER 3" in txt and "SYSTEM ANALYSIS" in txt and "chap3" not in toc_map:
            toc_map["chap3"] = str(page_num)
        if "CHAPTER 4" in txt and "PROPOSED WORK" in txt and "chap4" not in toc_map:
            toc_map["chap4"] = str(page_num)
        if "CHAPTER 5" in txt and "IMPLEMENTATION METHODOLOGY" in txt and "chap5" not in toc_map:
            toc_map["chap5"] = str(page_num)
        if "CHAPTER 6" in txt and "EXPERIMENTAL SETUP AND RESULTS" in txt and "chap6" not in toc_map:
            toc_map["chap6"] = str(page_num)
        if "CHAPTER 7" in txt and "CHALLENGES AND LIMITATIONS" in txt and "chap7" not in toc_map:
            toc_map["chap7"] = str(page_num)
        if "CHAPTER 8" in txt and "CONCLUSION AND FUTURE SCOPE" in txt and "chap8" not in toc_map:
            toc_map["chap8"] = str(page_num)
        if "CHAPTER 9" in txt and "APPENDIX" in txt and "chap9" not in toc_map:
            toc_map["chap9"] = str(page_num)
        if "REFERENCES" in txt and page_num > 20 and "references" not in toc_map:
            toc_map["references"] = str(page_num)

        # Check figures
        if "Figure 4.1" in txt and "fig4_1" not in lof_map: lof_map["fig4_1"] = str(page_num)
        if "Figure 4.2" in txt and "fig4_2" not in lof_map: lof_map["fig4_2"] = str(page_num)
        if "Figure 4.3" in txt and "fig4_3" not in lof_map: lof_map["fig4_3"] = str(page_num)
        if "Figure 5.1" in txt and "fig5_1" not in lof_map: lof_map["fig5_1"] = str(page_num)
        if "Figure 5.2" in txt and "fig5_2" not in lof_map: lof_map["fig5_2"] = str(page_num)
        if "Figure 5.3" in txt and "fig5_3" not in lof_map: lof_map["fig5_3"] = str(page_num)
        if "Figure 6.1" in txt and "fig6_1" not in lof_map: lof_map["fig6_1"] = str(page_num)
        if "Figure 6.2" in txt and "fig6_2" not in lof_map: lof_map["fig6_2"] = str(page_num)
        if "Figure 9.1" in txt and "fig9_1" not in lof_map: lof_map["fig9_1"] = str(page_num)
        if "Figure 9.2" in txt and "fig9_2" not in lof_map: lof_map["fig9_2"] = str(page_num)
        if "Figure 9.3" in txt and "fig9_3" not in lof_map: lof_map["fig9_3"] = str(page_num)

    print("Detected TOC map:", toc_map)
    print("Detected LOF map:", lof_map)
    return toc_map, lof_map, total_pages

def int_to_roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
            (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    res = ""
    for v, sym in vals:
        while n >= v:
            res += sym
            n -= v
    return res

def stamp_page_numbers(input_pdf_path, output_pdf_path, chap1_page):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont("Times-Roman", 11)

        # Page 1: Cover page (No number)
        # Page 2: Bonafide Certificate (No number)
        # Page 3 to chap1_page - 1: Preliminary pages (Roman numerals: iii, iv, v, vi, ...)
        # chap1_page to end: Chapters (Arabic numerals: 13, 14, 15, ...)
        if page_num == 1 or page_num == 2:
            pass # No page number
        elif page_num < chap1_page:
            roman_str = int_to_roman(page_num)
            can.drawCentredString(A4[0] / 2.0, 35, roman_str)
        else:
            can.drawCentredString(A4[0] / 2.0, 35, str(page_num))

        can.save()
        packet.seek(0)
        stamp_pdf = PdfReader(packet)
        page.merge_page(stamp_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
    print(f"Stamped PDF successfully created: {output_pdf_path} ({len(writer.pages)} pages)")

def main():
    print("Starting Compilation...")
    raw_html_path = os.path.join(BASE_DIR, "report_temp.html")
    raw_pdf_path = os.path.join(BASE_DIR, "report_pass1.pdf")
    final_pdf_path = os.path.join(BASE_DIR, "AI_Based_Communication_Skills_Project_Report.pdf")

    # Pass 1: generate initial HTML
    html_p1 = build_html()
    with open(raw_html_path, "w", encoding="utf-8") as f:
        f.write(html_p1)

    print("Rendering Pass 1 PDF via Chrome...")
    success = render_pdf(raw_html_path, raw_pdf_path)
    if not success:
        print("Failed to render PDF in pass 1.")
        return

    # Pass 1: detect exact page numbers
    toc_map, lof_map, total_pages = detect_page_numbers(raw_pdf_path)

    # Pass 2: regenerate HTML with exact detected page numbers
    html_p2 = build_html(toc_map, lof_map)
    with open(raw_html_path, "w", encoding="utf-8") as f:
        f.write(html_p2)

    print("Rendering Pass 2 PDF via Chrome...")
    success = render_pdf(raw_html_path, raw_pdf_path)
    if not success:
        print("Failed to render PDF in pass 2.")
        return

    # Pass 3: Stamp authentic page numbers
    chap1_page = int(toc_map.get("chap1", 13))
    print(f"Stamping page numbers with Chapter 1 starting at page {chap1_page}...")
    stamp_page_numbers(raw_pdf_path, final_pdf_path, chap1_page)

    # Also copy to downloads & project root as Report.pdf
    shutil.copy(final_pdf_path, os.path.join(BASE_DIR, "Report.pdf"))
    downloads_path = os.path.expanduser(r"~\Downloads\AI_Based_Communication_Skills_Project_Report.pdf")
    shutil.copy(final_pdf_path, downloads_path)
    print(f"Report copied to: {downloads_path}")

    # Clean up intermediate files
    if os.path.exists(raw_pdf_path): os.remove(raw_pdf_path)
    print("Compilation completed successfully!")

if __name__ == "__main__":
    main()
