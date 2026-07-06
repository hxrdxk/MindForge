from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def generate_certificate_pdf(certificate):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )

    title = ParagraphStyle(
        "Title",
        alignment=TA_CENTER,
        fontSize=30,
        textColor=HexColor("#0d6efd"),
        spaceAfter=20,
    )

    heading = ParagraphStyle(
        "Heading",
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15,
    )

    name = ParagraphStyle(
        "Name",
        alignment=TA_CENTER,
        fontSize=24,
        textColor=HexColor("#212529"),
        spaceAfter=20,
    )

    body = ParagraphStyle(
        "Body",
        alignment=TA_CENTER,
        fontSize=13,
        leading=24,
    )

    small = ParagraphStyle(
        "Small",
        alignment=TA_CENTER,
        fontSize=10,
        textColor=HexColor("#666666"),
        leading=16,
    )

    story = []

    story.append(
        Paragraph(
            "<b>MINDFORGE</b>",
            title,
        )
    )

    story.append(
        Paragraph(
            "CERTIFICATE OF COMPLETION",
            heading,
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    story.append(
        Paragraph(
            "This certificate is proudly presented to",
            body,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(
            f"<b>{certificate.enrollment.user.full_name}</b>",
            name,
        )
    )

    story.append(
        Paragraph(
            "for successfully completing",
            body,
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(
            f"<b>{certificate.enrollment.course.title}</b>",
            heading,
        )
    )

    story.append(Spacer(1, 0.35 * inch))

    story.append(
        Paragraph(
            f"<b>Final Score:</b> {certificate.final_score}%",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Issued On:</b> {certificate.issued_at.strftime('%d %B %Y')}",
            body,
        )
    )

    story.append(
        Paragraph(
            f"<b>Certificate ID:</b> {certificate.certificate_id}",
            body,
        )
    )

    story.append(Spacer(1, 0.45 * inch))

    story.append(
        Paragraph(
            "<b>Verify this certificate</b>",
            body,
        )
    )

    story.append(Spacer(1, 0.08 * inch))

    verification_url = (
        f"http://127.0.0.1:5000/verify/"
        f"{certificate.certificate_id}"
    )

    story.append(
        Paragraph(
            verification_url,
            small,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer