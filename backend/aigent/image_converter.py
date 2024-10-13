# File: aigent/image_converter.py
# Author: Tj Pilant
# Description: Handles image conversion and OCR operations for AIGENT
# Version: 0.6.4

import io
import os
import re

import cv2
import numpy as np
import pytesseract
from PIL import Image

from aigent.ai_service import AIService
from aigent.utils.logger import get_logger

logger = get_logger(__name__)

class ImageConverter:
    def __init__(self):
        self.ai_service = AIService()

    def preprocess_image(self, image_path):
        if not os.path.exists(image_path):
            logger.error("Image file not found", extra={"image_path": image_path})
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            logger.error("Unable to read image file", extra={"image_path": image_path})
            raise ValueError(f"Unable to read image file: {image_path}")

        # Additional preprocessing for typewritten documents
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def perform_ocr(self, image_path, use_cloud_vision=False):
        try:
            if use_cloud_vision:
                logger.info("Performing OCR using Cloud Vision", extra={"image_path": image_path})
                raw_text = self.perform_cloud_vision_ocr(image_path)
            else:
                logger.info("Performing OCR using Tesseract", extra={"image_path": image_path})
                raw_text = self.perform_tesseract_ocr(image_path)
            return self.clean_ocr_text(raw_text)
        except Exception as e:
            logger.error("OCR failed, falling back to alternative method", extra={"error": str(e), "image_path": image_path})
            if use_cloud_vision:
                raw_text = self.perform_tesseract_ocr(image_path)
            else:
                raw_text = self.perform_cloud_vision_ocr(image_path)
            return self.clean_ocr_text(raw_text)

    def perform_tesseract_ocr(self, image_path):
        try:
            preprocessed_image = self.preprocess_image(image_path)
            # Configure Tesseract parameters
            custom_config = r"--oem 1 --psm 6"
            text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
            if not text.strip():
                logger.warning("Tesseract failed to extract text", extra={"image_path": image_path})
                raise ValueError("Tesseract failed to extract text")
            return text
        except Exception as e:
            logger.error("Tesseract OCR failed", extra={"error": str(e), "image_path": image_path})
            return ""

    def perform_cloud_vision_ocr(self, image_path):
        try:
            return self.ai_service.perform_ocr(image_path)
        except Exception as e:
            logger.error("Google Cloud Vision OCR failed", extra={"error": str(e), "image_path": image_path})
            return ""

    def clean_ocr_text(self, text):
        # Remove line breaks within words
        cleaned_text = re.sub(r'(?<=[a-zA-Z])-\n(?=[a-zA-Z])', '', text)
        # Join words split across lines, but keep paragraph breaks
        cleaned_text = re.sub(r'(?<=[a-zA-Z])\n(?=[a-z])', ' ', cleaned_text)
        # Remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

# Usage example
if __name__ == "__main__":
    converter = ImageConverter()
    image_path = "path/to/your/image.jpg"
    
    # Perform OCR using Tesseract
    tesseract_result = converter.perform_ocr(image_path, use_cloud_vision=False)
    print("Tesseract OCR Result:", tesseract_result)

    # Perform OCR using Google Cloud Vision
    cloud_vision_result = converter.perform_ocr(image_path, use_cloud_vision=True)
    print("Google Cloud Vision OCR Result:", cloud_vision_result)
