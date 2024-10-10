# File: tests/test_tesseract_integration.py
# Author: Tj Pilant
# Description: This script compares Tesseract and Google Cloud Vision OCR results for typewritten documents.
# Version: 0.5.0

import os

from aigent.ai_service import AIService
from aigent.image_converter import ImageConverter


def test_ocr():
    converter = ImageConverter()
    ai_service = AIService()

    test_images = [
        os.path.join(
            os.path.dirname(__file__), "test_data", "freeperson_text_vol1_Page_030.tiff"
        ),
        os.path.join(
            os.path.dirname(__file__), "test_data", "freeperson_text_vol1_Page_031.tiff"
        ),
    ]

    for image_path in test_images:
        print(f"\nTesting OCR on {image_path}")

        # Tesseract OCR
        converter.set_ocr_method(False)
        tesseract_result = converter.perform_ocr(image_path)

        # Google Cloud Vision OCR
        cloud_vision_result = ai_service.perform_ocr(image_path)

        # Compare results
        print("\nTesseract OCR Result (first 3 lines):")
        print("\n".join(tesseract_result.split("\n")[:3]))

        print("\nGoogle Cloud Vision OCR Result (first 3 lines):")
        print("\n".join(cloud_vision_result.split("\n")[:3]))

        # Simple accuracy comparison (based on word count)
        tesseract_words = len(tesseract_result.split())
        cloud_vision_words = len(cloud_vision_result.split())

        print(f"\nTesseract word count: {tesseract_words}")
        print(f"Cloud Vision word count: {cloud_vision_words}")

        if tesseract_words > cloud_vision_words:
            print("Tesseract detected more words in this image.")
        elif cloud_vision_words > tesseract_words:
            print("Google Cloud Vision detected more words in this image.")
        else:
            print("Both methods detected the same number of words.")

        print("=" * 50)


if __name__ == "__main__":
    test_ocr()
