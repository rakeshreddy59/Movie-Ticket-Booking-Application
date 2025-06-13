from pdf_ticket import generate_ticket_pdf

generate_ticket_pdf(
    booking_id=1234,
    movie="Jawan",
    theatre="INOX",
    show_time="2025-04-21 18:00",
    tickets=2,
    filename="test_ticket.pdf"
)
print("PDF generated!")