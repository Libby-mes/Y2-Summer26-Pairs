from fpdf import FPDF
import os

def create_pdf(itinerary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, itinerary)

    filename = "Itinerary.pdf"
    pdf.output(filename)

    print("Saved to:", os.path.abspath(filename))