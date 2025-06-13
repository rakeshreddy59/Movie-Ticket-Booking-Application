from fpdf import FPDF
from datetime import datetime
from io import BytesIO

def generate_ticket_pdf_bytes(booking_id, movie, theatre, show_time, tickets):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(200, 10, txt="Movie Ticket Confirmation", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Booking ID: {booking_id}", ln=True)
    pdf.cell(200, 10, txt=f"Movie: {movie}", ln=True)
    pdf.cell(200, 10, txt=f"Theatre: {theatre}", ln=True)
    pdf.cell(200, 10, txt=f"Show Time: {show_time}", ln=True)
    pdf.cell(200, 10, txt=f"Tickets: {tickets}", ln=True)
    pdf.cell(200, 10, txt=f"Issue Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Return PDF as BytesIO
    pdf_bytes = pdf.output(dest="S").encode("latin1")
    buffer = BytesIO(pdf_bytes)
    return buffer