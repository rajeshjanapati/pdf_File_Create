from flask import Flask, request, jsonify
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import base64
import io

app = Flask(__name__)


def create_pdf(data, photo_base64):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    # ---------- Photo convert ----------
    photo = None
    if photo_base64:
        try:
            img_bytes = base64.b64decode(photo_base64)
            img_buffer = io.BytesIO(img_bytes)
            photo = Image(img_buffer, width=100, height=120)
        except:
            photo = None

    # ---------- Title ----------
    story.append(Paragraph("<b><font size=18>Candidate Application Form</font></b>", styles['Title']))
    story.append(Spacer(1, 20))

    # ---------- Table data ----------
    table_data = [
        ["Candidate_Fields", "Details"],
        ["Full Name", data.get("full_name", "")],
        ["Email Address", data.get("email", "")],
        ["Mobile Number", data.get("mobile", "")],
        ["Date of Birth", data.get("dob", "")],
        ["Gender", data.get("gender", "")],
        ["Address", data.get("address", "")],
        ["City", data.get("city", "")],
        ["State", data.get("state", "")],
        ["Pincode", data.get("pincode", "")],
        ["Highest Qualification", data.get("qualification", "")],
        ["Total Experience (Years)", data.get("experience", "")],
        ["Current Company", data.get("current_company", "")],
        ["Skills", data.get("skills", "")],
        ["Expected Salary", data.get("expected_salary", "")],
        ["Notice Period", data.get("notice_period", "")]
    ]

    table = Table(table_data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # ---------- Photo ----------
    story.append(Paragraph("<b>Passport Size Photo</b>", styles['Heading3']))
    story.append(Spacer(1, 10))

    if photo:
        story.append(photo)
    else:
        story.append(Paragraph("No photo provided", styles['Normal']))

    doc.build(story)

    # Return base64 PDF
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return base64.b64encode(pdf_bytes).decode("utf-8")


@app.route("/generate-form", methods=["POST"])
def generate_form():
    try:
        body = request.json

        data = body.get("data", {})
        photo_base64 = body.get("photo", "")

        pdf_base64 = create_pdf(data, photo_base64)

        return jsonify({
            "status": "success",
            "pdf_file_name": "candidate_application_form.pdf",
            "pdf_file_content": pdf_base64,
            "content_type": "application/pdf"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

