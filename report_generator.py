import os
from html import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

def generate_report(
    filename,
    ats_score,
    analysis
):

    os.makedirs("static/reports", exist_ok=True)

    safe_name = os.path.splitext(os.path.basename(filename))[0] or "resume-report"
    pdf_file = os.path.join("static", "reports", f"{safe_name}-report.pdf")

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Resume Analysis Report",
            styles['Title']
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            f"ATS Score: {ats_score}",
            styles['Heading2']
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            escape(analysis or "No analysis text available.").replace("\n", "<br/>"),
            styles['BodyText']
        )
    )

    doc.build(content)

    return pdf_file
