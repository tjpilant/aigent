from .base_tool import BaseTool
from pydantic import Field
from google.cloud import documentai
from google.oauth2 import service_account
import os
import json
from ...utils.logger import get_logger

logger = get_logger(__name__)

class GoogleCloudVisionOCRTool(BaseTool):
    """
    This tool uses Google Cloud Vision AI OCR to process a document and output the extracted text as a Markdown file.
    """
    
    input_file_path: str = Field(..., description="Path to the input file for OCR processing.")
    output_md_file_path: str = Field(..., description="Path where the resulting Markdown (.md) file will be saved.")
    credentials_path: str = Field(..., description="Path to the Google Cloud credentials JSON file.")
    processor_id: str = Field(..., description="ID of the Document AI processor to use.")
    location: str = Field(default="us", description="Location of the Document AI processor.")

    def run(self):
        logger.info("Starting Google Cloud Vision OCR process")
        client, project_id = self._initialize_client()
        document_text = self._process_document(client, project_id)
        self._save_as_markdown(document_text)
        logger.info(f"Markdown file created at: {self.output_md_file_path}")
        return f"Markdown file created at: {self.output_md_file_path}"

    def _initialize_client(self):
        logger.debug("Initializing Google Cloud Vision client")
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        client = documentai.DocumentProcessorServiceClient(credentials=credentials)
        with open(self.credentials_path, 'r') as cred_file:
            project_id = json.load(cred_file).get("project_id")
        return client, project_id

    def _process_document(self, client, project_id):
        logger.info(f"Processing document: {self.input_file_path}")
        with open(self.input_file_path, "rb") as file:
            file_content = file.read()
        
        processor_name = f"projects/{project_id}/locations/{self.location}/processors/{self.processor_id}"
        mime_type = self._get_mime_type(self.input_file_path)
        
        raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
        request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        
        result = client.process_document(request=request)
        logger.info("Document processing completed")
        return result.document.text

    def _save_as_markdown(self, text):
        logger.info(f"Saving extracted text as Markdown: {self.output_md_file_path}")
        with open(self.output_md_file_path, "w") as md_file:
            md_file.write(text)

    def _get_mime_type(self, file_path: str) -> str:
        extension = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
            '.pdf': 'application/pdf', '.tiff': 'image/tiff', '.tif': 'image/tiff'
        }
        mime_type = mime_types.get(extension, 'application/octet-stream')
        logger.debug(f"Detected MIME type for {file_path}: {mime_type}")
        return mime_type
