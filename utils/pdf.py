import os
from io import BytesIO
from pathlib import Path

import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


PRIMARY = HexColor("#312E81")
SECONDARY = HexColor("#7C3AED")
ACCENT = HexColor("#2563EB")
TEXT = HexColor("#0F172A")
MUTED = HexColor("#64748B")
BORDER = HexColor("#E2E8F0")
SURFACE_ALT = HexColor("#F8F9FF")
SUCCESS = HexColor("#10B981")
WHITE = HexColor("#FFFFFF")


def _fit_font_size(text, font_name, maximum, minimum, available_width):
    for size in range(maximum, minimum - 1, -1):
        if stringWidth(text, font_name, size) <= available_width:
            return size

    return minimum


def _draw_centered(pdf, text, y, font_name, font_size, color):
    pdf.setFont(font_name, font_size)
    pdf.setFillColor(color)
    pdf.drawCentredString(pdf._pagesize[0] / 2, y, text)


def _draw_credential_detail(pdf, x, label, value, value_color=TEXT):
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawCentredString(x, 173, label)
    pdf.setFillColor(value_color)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(x, 154, value)


def generate_certificate_pdf(certificate):
    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    pdf.setTitle(f"MindForge Certificate - {certificate.certificate_id}")
    pdf.setAuthor("MindForge")
    pdf.setSubject("Certificate of Completion")

    course = certificate.enrollment.course
    student = certificate.enrollment.user
    verification_base_url = os.getenv(
        "PUBLIC_BASE_URL",
        "https://mindforge.in",
    ).rstrip("/")
    verification_url = (
        f"{verification_base_url}/verify/"
        f"{certificate.certificate_id}"
    )

    pdf.setFillColor(WHITE)
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)

    pdf.setStrokeColor(PRIMARY)
    pdf.setLineWidth(2.4)
    pdf.roundRect(20, 20, page_width - 40, page_height - 40, 10, stroke=1, fill=0)

    pdf.setStrokeColor(SECONDARY)
    pdf.setLineWidth(0.8)
    pdf.roundRect(32, 32, page_width - 64, page_height - 64, 6, stroke=1, fill=0)

    logo_path = (
        Path(__file__).resolve().parent.parent
        / "static"
        / "logo"
        / "mindforge-logo.png"
    )
    if logo_path.exists():
        pdf.drawImage(
            str(logo_path),
            58,
            499,
            width=42,
            height=42,
            preserveAspectRatio=True,
            mask="auto",
        )

    pdf.setFillColor(PRIMARY)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(110, 522, "MindForge")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(110, 507, "Forging Minds. Building Futures.")

    pdf.setFillColor(SECONDARY)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawRightString(page_width - 58, 522, "VERIFIED LEARNING CREDENTIAL")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(
        page_width - 58,
        507,
        f"Certificate ID: {certificate.certificate_id}",
    )

    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.8)
    pdf.line(58, 478, page_width - 58, 478)

    _draw_centered(
        pdf,
        "CERTIFICATE OF COMPLETION",
        430,
        "Helvetica-Bold",
        24,
        PRIMARY,
    )
    _draw_centered(
        pdf,
        "This certifies that",
        397,
        "Helvetica",
        12,
        MUTED,
    )

    student_name = student.full_name.strip()
    student_size = _fit_font_size(
        student_name,
        "Times-BoldItalic",
        31,
        20,
        page_width - 170,
    )
    _draw_centered(
        pdf,
        student_name,
        352,
        "Times-BoldItalic",
        student_size,
        TEXT,
    )

    pdf.setStrokeColor(SECONDARY)
    pdf.setLineWidth(1.2)
    pdf.line(page_width / 2 - 128, 336, page_width / 2 + 128, 336)

    _draw_centered(
        pdf,
        "has successfully completed the course",
        304,
        "Helvetica",
        12,
        MUTED,
    )

    course_size = _fit_font_size(
        course.title,
        "Helvetica-Bold",
        21,
        14,
        page_width - 170,
    )
    _draw_centered(
        pdf,
        course.title,
        268,
        "Helvetica-Bold",
        course_size,
        PRIMARY,
    )

    _draw_centered(
        pdf,
        "This credential recognizes demonstrated course completion and achievement.",
        236,
        "Helvetica",
        10,
        MUTED,
    )

    pdf.setFillColor(SURFACE_ALT)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.8)
    pdf.roundRect(92, 128, page_width - 184, 74, 8, stroke=1, fill=1)

    column_width = (page_width - 184) / 3
    first_column = 92 + column_width / 2
    _draw_credential_detail(
        pdf,
        first_column,
        "ISSUED ON",
        certificate.issued_at.strftime("%d %B %Y"),
    )
    _draw_credential_detail(
        pdf,
        first_column + column_width,
        "FINAL SCORE",
        f"{certificate.final_score}%",
        SUCCESS,
    )
    _draw_credential_detail(
        pdf,
        first_column + (column_width * 2),
        "CERTIFICATE ID",
        certificate.certificate_id,
    )

    pdf.setStrokeColor(BORDER)
    pdf.line(58, 96, page_width - 58, 96)
    verification_text = f"Verify this certificate: {verification_url}"
    verification_size = _fit_font_size(
        verification_text,
        "Helvetica",
        9,
        7,
        page_width - 116,
    )
    _draw_centered(
        pdf,
        verification_text,
        74,
        "Helvetica",
        verification_size,
        ACCENT,
    )
    pdf.linkURL(
        verification_url,
        (58, 62, page_width - 58, 88),
        relative=0,
    )

    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(58, 47, "MindForge Credential Registry")
    pdf.drawRightString(page_width - 58, 47, "AI-powered CS Fundamentals Learning Platform")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer


def generate_certificate_preview(certificate):
    certificate_pdf = generate_certificate_pdf(certificate)
    document = fitz.open(
        stream=certificate_pdf.getvalue(),
        filetype="pdf",
    )
    page = document.load_page(0)
    pixmap = page.get_pixmap(
        matrix=fitz.Matrix(2, 2),
        alpha=False,
    )
    preview = BytesIO(pixmap.tobytes("png"))
    document.close()
    preview.seek(0)

    return preview
