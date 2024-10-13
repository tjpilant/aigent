# FIRST TOOL MODEL

from agency_swarm.tools import BaseTool
from pydantic import Field
import io
import json
import os
import logging
from google.cloud import documentai
from google.oauth2 import service_account

# Set your Google Cloud processor and credential path constants
CREDENTIALS_PATH = "aiocr-gcv-api.json"
PROCESSOR_ID = "cdbb7ba4f9c316d0"
LOCATION = "us"

class GoogleCloudVisionOCRTool(BaseTool):
    """
    This tool uses Google Cloud Vision AI OCR to process a document and output the extracted text as a Markdown file.
    """
    
    input_file_path: str = Field(..., description="Path to the input file for OCR processing.")
    output_md_file_path: str = Field(..., description="Path where the resulting Markdown (.md) file will be saved.")

    def _initialize_client(self):
        """
        Initializes the Document AI client using the Google service account credentials.
        """
        if not os.path.exists(CREDENTIALS_PATH):
            logging.error("Google Cloud credentials file not found.")
            raise FileNotFoundError("Google Cloud credentials file not found.")
        
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
        client = documentai.DocumentProcessorServiceClient(credentials=credentials)
        
        with open(CREDENTIALS_PATH, 'r') as cred_file:
            cred_data = json.load(cred_file)
            project_id = cred_data.get("project_id")
        
        return client, project_id

    def run(self):
        """
        Runs the OCR process on the specified input file and saves the extracted text to a Markdown file.
        """
        # Initialize the client
        document_ai_client, project_id = self._initialize_client()
        
        # Read the input file
        with open(self.input_file_path, "rb") as file:
            file_content = file.read()

        # Set up the document processor details
        processor_name = f"projects/{project_id}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
        mime_type = self._get_mime_type(self.input_file_path)
        
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        
        # Process the document
        result = document_ai_client.process_document(request=request)
        document_text = result.document.text

        # Save the extracted text to a Markdown file
        with open(self.output_md_file_path, "w") as md_file:
            md_file.write(document_text)
        
        return f"Markdown file created at: {self.output_md_file_path}"

    def _get_mime_type(self, file_path: str) -> str:
        """
        Determines the MIME type of the file based on its extension.
        """
        extension = os.path.splitext(file_path)[1].lower()
        if extension in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        elif extension == '.png':
            return 'image/png'
        elif extension == '.pdf':
            return 'application/pdf'
        elif extension in ['.tiff', '.tif']:
            return 'image/tiff'
        else:
            return 'application/octet-stream'

if __name__ == "__main__":
    tool = GoogleCloudVisionOCRTool(
        input_file_path="path/to/input/file.pdf",
        output_md_file_path="path/to/output/file.md"
    )
    print(tool.run())



# SECOND TOOL MODEL

import io
import json
import logging
import os

from typing import Optional
from google.cloud import documentai
from google.oauth2 import service_account

class AIService:
    def __init__(self):
        self.google_cloud_credentials_path = "aiocr-gcv-api.json"
        self.document_ai_client: Optional[documentai.DocumentProcessorServiceClient] = None
        self.project_id: Optional[str] = None
        self.location = "us"
        self.processor_id: str = "cdbb7ba4f9c316d0"  # Set the processor ID

        self._initialize_clients()
        
    def _initialize_clients(self):
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

    def save_as_md(self, extracted_text: str, output_md_path: str):
        """
        Converts the extracted text to a Markdown format and saves it to the specified file path.
        """
        try:
            logging.info(f"Saving extracted text as Markdown file: {output_md_path}")
            
            # Basic markdown conversion (you can enhance this with more formatting logic)
            with open(output_md_path, "w") as md_file:
                md_file.write("# Extracted OCR Text\n\n")  # Adding a header for the markdown
                md_file.write(extracted_text)  # Writing the extracted text
            
            logging.info(f"Markdown file saved successfully: {output_md_path}")
        
        except Exception as e:
            logging.error(f"Error saving Markdown file: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    ai_service = AIService()
    input_file = "input_file.pdf"  # Replace with your actual input file
    output_md_file = "output_file.md"  # Replace with your desired markdown output file name

    # Perform OCR and get the extracted text
    extracted_text = ai_service.perform_ocr(input_file)
    
    # Save the extracted text as a Markdown file
    ai_service.save_as_md(extracted_text, output_md_file)
