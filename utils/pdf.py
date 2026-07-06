from io import BytesIO

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_certificate_pdf(certificate):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    heading.alignment = TA_CENTER

    normal = styles["BodyText"]
    normal.alignment = TA_CENTER

    story = []

    story.append(Paragraph("MindForge", title))
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Certificate of Completion",
            heading,
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "This certificate is proudly presented to",
            normal,
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>{certificate.enrollment.user.full_name}</b>",
            heading,
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "for successfully completing",
            normal,
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>{certificate.enrollment.course.title}</b>",
            heading,
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            f"Final Score: {certificate.final_score}%",
            normal,
        )
    )

    story.append(
        Paragraph(
            f"Issued: {certificate.issued_at.strftime('%d %B %Y')}",
            normal,
        )
    )

    story.append(
        Paragraph(
            f"Certificate ID: {certificate.certificate_id}",
            normal,
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer