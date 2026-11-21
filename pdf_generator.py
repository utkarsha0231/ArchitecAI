import os
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)


def generate_pdf(content, filename, diagram_path=None):

    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#6C3CE7"),
        fontSize=22,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#6C3CE7"),
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = styles["BodyText"]
    story = []

    # Title
    story.append(Paragraph("ArchitecAI System Design Report", title_style))
    story.append(Spacer(1, 12))

    # System Design Content
    if isinstance(content, str):

        for line in content.split("\n"):

            line = line.strip()

            if not line:
                story.append(Spacer(1, 6))
                continue

            if line.startswith("#"):
                heading = line.lstrip("#").strip()
                story.append(Paragraph(heading, heading_style))
            else:
                story.append(Paragraph(line, body_style))

    else:
        story.append(Paragraph(str(content), body_style))

    # Architecture Diagram
    if diagram_path and os.path.exists(diagram_path):

        story.append(PageBreak())
        story.append(Paragraph("System Architecture Diagram", heading_style))
        story.append(Spacer(1, 15))

        img = Image(diagram_path)

        max_width = 7 * inch
        max_height = 9 * inch

        img._restrictSize(max_width, max_height)

        story.append(img)

    # Generate PDF
    doc.build(story)

    return filename