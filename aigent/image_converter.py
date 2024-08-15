# File: aigent/image_converter.py
# Author: Tj Pilant
# Description: Handles image conversion and OCR operations for AIGENT
# Version: 0.6.0

import io
import os

import cv2
import numpy as np
import pytesseract
from PIL import Image

from .ai_service import AIService


class ImageConverter:
    def __init__(self, use_cloud_vision=True):
        self.use_cloud_vision = use_cloud_vision
        self.ai_service = AIService()

    def preprocess_image(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image file: {image_path}")

        # Additional preprocessing for typewritten documents
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def perform_ocr(self, image_path):
        try:
            if self.use_cloud_vision:
                return self.perform_cloud_vision_ocr(image_path)
            else:
                return self.perform_tesseract_ocr(image_path)
        except Exception as e:
            print(f"OCR failed: {str(e)}. Falling back to alternative method.")
            if self.use_cloud_vision:
                return self.perform_tesseract_ocr(image_path)
            else:
                return self.perform_cloud_vision_ocr(image_path)

    def perform_tesseract_ocr(self, image_path):
        try:
            preprocessed_image = self.preprocess_image(image_path)

            # Configure Tesseract parameters
            custom_config = r"--oem 1 --psm 6"

            text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
            if not text.strip():
                raise ValueError("Tesseract failed to extract text")
            return text
        except Exception as e:
            print(f"Tesseract OCR failed: {str(e)}")
            return ""

    def perform_cloud_vision_ocr(self, image_path):
        try:
            return self.ai_service.perform_ocr(image_path)
        except Exception as e:
            print(f"Google Cloud Vision OCR failed: {str(e)}")
            return ""

    def set_ocr_method(self, use_cloud_vision):
        self.use_cloud_vision = use_cloud_vision
