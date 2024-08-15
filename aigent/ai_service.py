# File: aigent/ai_service.py
# Author: Tj Pilant
# Description: Handles AI service integrations for AIGENT
# Version: 0.4.0

import io
import logging

import openai
from anthropic import Anthropic
from google.cloud import vision

from .api_manager import APIManager


class AIService:
    def __init__(self):
        self.api_manager = APIManager()
        self.openai_api_key = self.api_manager.get_api_key("openai")
        self.anthropic_api_key = self.api_manager.get_api_key("anthropic")
        self.google_cloud_key = self.api_manager.get_api_key("google_cloud")

        if not self.openai_api_key:
            logging.warning(
                "OpenAI API key not found. OpenAI services will not be available."
            )
        if not self.anthropic_api_key:
            logging.warning(
                "Anthropic API key not found. Anthropic services will not be available."
            )
        if not self.google_cloud_key:
            logging.warning(
                "Google Cloud API key not found. Google Cloud services will not be available."
            )

        self.openai_client = None
        self.anthropic_client = None
        self.vision_client = None

        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai.OpenAI()
        if self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        if self.google_cloud_key:
            self.vision_client = vision.ImageAnnotatorClient()

    def perform_ocr(self, image_path):
        if not self.vision_client:
            raise ValueError(
                "Google Cloud Vision API key not found. Cannot perform OCR."
            )

        with io.open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.vision_client.text_detection(image=image)

        if response.error.message:
            raise Exception(
                f"Google Cloud Vision API returned error: {response.error.message}"
            )

        texts = response.text_annotations
        if texts:
            return texts[0].description
        else:
            return "No text detected in the image."

    # Other methods for OpenAI and Anthropic services can remain unchanged
