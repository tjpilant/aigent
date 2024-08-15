# File: file_converter.py
# Author: Tj Pilant
# Description: Handles conversion of various file types to JSONL and other formats
# Version: 0.2.0

import json
import logging
import os
from datetime import datetime

import pdfplumber
import PyPDF2
from docx import Document
from image_converter import ImageConverter

# Set up logging
logging.basicConfig(
    filename="file_converter.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class FileConverter:
    def __init__(self):
        self.image_converter = ImageConverter()

    def convert_file(
        self,
        input_file,
        output_dir,
        project_info,
        agent_traits,
        output_formats=["jsonl"],
    ):
        file_extension = os.path.splitext(input_file)[1].lower()

        if file_extension == ".pdf":
            return self.convert_pdf(
                input_file, output_dir, project_info, agent_traits, output_formats
            )
        elif file_extension in [".png", ".jpg", ".jpeg", ".tiff", ".tif"]:
            return self.convert_image(
                input_file, output_dir, project_info, agent_traits, output_formats
            )
        elif file_extension == ".docx":
            return self.convert_docx(
                input_file, output_dir, project_info, agent_traits, output_formats
            )
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def batch_convert_files(
        self,
        input_files,
        output_dir,
        project_info,
        agent_traits,
        output_formats=["jsonl"],
    ):
        results = {}
        for input_file in input_files:
            try:
                result = self.convert_file(
                    input_file, output_dir, project_info, agent_traits, output_formats
                )
                results[input_file] = result
            except Exception as e:
                logging.error(f"Error converting file {input_file}: {str(e)}")
                results[input_file] = str(e)
        return results

    # ... (rest of the existing methods remain unchanged)


# Usage example
if __name__ == "__main__":
    converter = FileConverter()
    project_info = ProjectInfo(project_title="Test Project")
    agent_traits = AgentTraits(data_purpose="Test Purpose")

    # Single file conversion
    single_result = converter.convert_file(
        "path/to/your/file.pdf",
        "path/to/output/dir",
        project_info,
        agent_traits,
        output_formats=["jsonl", "txt", "md", "docx"],
    )
    print("Single file conversion result:", single_result)

    # Batch file conversion
    batch_files = ["path/to/file1.pdf", "path/to/file2.docx", "path/to/image.png"]
    batch_results = converter.batch_convert_files(
        batch_files,
        "path/to/output/dir",
        project_info,
        agent_traits,
        output_formats=["jsonl", "txt"],
    )
    print("Batch conversion results:", batch_results)
