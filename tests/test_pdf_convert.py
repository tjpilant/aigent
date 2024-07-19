import pdfplumber
from pypdf import PdfReader
import os

def test_pdf_extraction(pdf_path):
    print(f"Testing PDF extraction for: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path)} bytes")

    print("\nUsing pdfplumber:")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"Page {i+1}: {text[:100] if text else 'No text extracted'}...")

    print("\nUsing pypdf:")
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Page {i+1}: {text[:100] if text else 'No text extracted'}...")

# Use this function with your PDF file
test_pdf_extraction("MakeMoneyInet.pdf")