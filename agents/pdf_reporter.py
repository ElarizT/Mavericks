from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

def generate_pdf_report(clauses):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    data = [["Clause", "Risk Level", "Explanation"]]
    for clause, risk, explanation in clauses:
        data.append([clause, risk, explanation])

    table = Table(data, repeatRows=1, colWidths=[180, 80, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    # Risk color coding
    for i in range(1, len(data)):
        risk = data[i][1].lower()
        if risk == "high":
            table.setStyle([('BACKGROUND', (1, i), (1, i), colors.red)])
        elif risk == "medium":
            table.setStyle([('BACKGROUND', (1, i), (1, i), colors.orange)])
        elif risk == "low":
            table.setStyle([('BACKGROUND', (1, i), (1, i), colors.green)])

    doc.build([table])
    buffer.seek(0)
    return buffer
