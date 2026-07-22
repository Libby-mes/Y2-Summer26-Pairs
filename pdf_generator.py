from fpdf import FPDF
import os
import re

def create_pdf(itinerary):
    # Remove emojis and other unsupported Unicode characters
    itinerary = re.sub(r'[^\x00-\x7F]+', '', itinerary)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, itinerary)

    filename = "Itinerary.pdf"
    pdf.output(filename)

    print("Saved to:", os.path.abspath(filename))