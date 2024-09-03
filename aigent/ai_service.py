# File: aigent/ai_service.py
# Author: Tj Pilant
# Description: Handles AI service integrations for AIGENT, focusing on Google Document AI for OCR
# Version: 0.6.5

import io
import json
import logging
import os
from typing import Optional

import openai
from anthropic import Anthropic
from google.cloud import documentai
from google.oauth2 import service_account

from aigent.api_manager import APIManager


class AIService:
    def __init__(self):
        self.api_manager = APIManager()
        self.openai_api_key = self.api_manager.get_api_key("openai")
        self.anthropic_api_key = self.api_manager.get_api_key("anthropic")
        self.google_cloud_credentials_path = "/home/tjpilant/aiengineers/aigent/aiocr-gcv-api.json"

        self.openai_client: Optional[openai.OpenAI] = None
        self.anthropic_client: Optional[Anthropic] = None
        self.document_ai_client: Optional[documentai.DocumentProcessorServiceClient] = None
        self.project_id: Optional[str] = None
        self.location = "us"
        self.processor_id: str = "cdbb7ba4f9c316d0"  # Set the processor ID

        self._initialize_clients()

    def _initialize_clients(self):
        # ... (rest of the method remains the same)
        if os.path.exists(self.google_cloud_credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                self.google_cloud_credentials_path
            )
            self.document_ai_client = documentai.DocumentProcessorServiceClient(credentials=credentials)
            
            # Load the project ID from the credentials file
            with open(self.google_cloud_credentials_path, 'r') as f:
                cred_data = json.load(f)
                self.project_id = cred_data.get('project_id')
                logging.info(f"Loaded Google Cloud project ID: {self.project_id}")
            
            logging.info(f"Using processor ID: {self.processor_id}")
        else:
            logging.warning(f"Google Cloud credentials file not found at {self.google_cloud_credentials_path}. Document AI services will not be available.")

    def perform_ocr(self, file_path: str) -> str:
        if not self.document_ai_client:
            logging.error("Google Cloud Document AI client is not initialized. Cannot perform OCR.")
            raise ValueError("Google Cloud Document AI client is not initialized. Cannot perform OCR.")

        try:
            logging.info(f"Starting OCR process for file: {file_path}")
            
            # Read the file into memory
            with open(file_path, "rb") as file:
                file_content = file.read()
            logging.info(f"File read successfully. Size: {len(file_content)} bytes")

            name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
            logging.info(f"Using processor: {name}")
            
            # Determine MIME type based on file extension
            mime_type = self._get_mime_type(file_path)
            logging.info(f"Detected MIME type: {mime_type}")

            # Load the input document
            raw_document = documentai.RawDocument(
                content=file_content,
                mime_type=mime_type
            )

            # Configure the process request
            request = documentai.ProcessRequest(
                name=name,
                raw_document=raw_document
            )

            logging.info("Sending request to Google Cloud Document AI")
            # Process the document
            result = self.document_ai_client.process_document(request=request)
            document = result.document

            # Extract and return the text
            extracted_text = document.text
            logging.info(f"OCR completed. Extracted text length: {len(extracted_text)}")
            return extracted_text

        except Exception as e:
            logging.error(f"Error performing OCR: {str(e)}")
            raise

    def _get_mime_type(self, file_path: str) -> str:
        extension = os.path.splitext(file_path)[1].lower()
        if extension in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        elif extension == '.png':
            return 'image/png'
        elif extension == '.pdf':
            return 'application/pdf'
        elif extension in ['.tiff', '.tif']:  # Add support for .tif
            return 'image/tiff'
        else:
            return 'application/octet-stream'

    def set_processor_id(self, processor_id: str):
        self.processor_id = processor_id
        logging.info(f"Set processor ID to: {self.processor_id}")

    def generate_openai_response(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        if not self.openai_client:
            raise ValueError("OpenAI client is not initialized. Cannot generate response.")

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating OpenAI response: {str(e)}")
            raise

    def generate_anthropic_response(self, prompt: str, model: str = "claude-2") -> str:
        if not self.anthropic_client:
            raise ValueError("Anthropic client is not initialized. Cannot generate response.")

        try:
            response = self.anthropic_client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens_to_sample=300
            )
            return response.completion
        except Exception as e:
            logging.error(f"Error generating Anthropic response: {str(e)}")
            raise

# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ai_service = AIService()

    # Example OCR using Document AI
    try:
        ocr_result = ai_service.perform_ocr("path/to/your/document.pdf")
        print("Document AI OCR Result:", ocr_result)
    except Exception as e:
        print(f"Document AI OCR Error: {str(e)}")


    # Example OpenAI response
    try:
        openai_response = ai_service.generate_openai_response("Tell me a joke")
        print("OpenAI Response:", openai_response)
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")

    # Example Anthropic response
    try:
        anthropic_response = ai_service.generate_anthropic_response("Tell me a joke")
        print("Anthropic Response:", anthropic_response)
    except Exception as e:
        print(f"Anthropic Error: {str(e)}")