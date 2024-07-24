import json
import logging
from datetime import datetime

import pdfplumber
import PyPDF2

# Set up logging
logging.basicConfig(filename='pdf_converter.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')


def load_config(config_file):
    """Loads configuration from a JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"Config file not found: {config_file}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in config file: {config_file}")
        return {}

def save_config(config, config_file):
    """Saves configuration to a JSON file."""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        logging.info(f"Configuration saved to {config_file}")
    except Exception as e:
        logging.error(f"Error saving configuration: {str(e)}")
        raise

def split_large_pdf(input_path, output_dir, max_pages=100):
    with pdfplumber.open(input_path) as pdf:
        total_pages = len(pdf.pages)
        for i in range(0, total_pages, max_pages):
            output_path = os.path.join(output_dir, f"split_{i//max_pages + 1}.pdf")
            with pdfplumber.open(input_path) as pdf:
                pdf_writer = PyPDF2.PdfWriter()
                for page in range(i, min(i + max_pages, total_pages)):
                    pdf_writer.add_page(pdf.pages[page])
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
    return [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.startswith("split_")]
class ProjectInfo:
    def __init__(self, project_title="", project_id="", target_agent="", agent_role="", 
                 processor_name="", dataset_name="", version="1.0"):
        self.project_title = project_title
        self.project_id = project_id
        self.target_agent = target_agent
        self.agent_role = agent_role
        self.processor_name = processor_name
        self.processing_date = datetime.now().isoformat()
        self.dataset_name = dataset_name
        self.version = version

class AgentTraits:
    def __init__(self, data_purpose="", knowledge_application="", response_tone="",
                 detail_level="", ethical_guidelines=""):
        self.data_purpose = data_purpose
        self.knowledge_application = knowledge_application
        self.response_tone = response_tone
        self.detail_level = detail_level
        self.ethical_guidelines = ethical_guidelines

import os


def start_conversion(input_file, output_file, project_info, agent_traits, start_page=None, end_page=None):
    try:
        logging.info(f"Starting conversion of {input_file}")
        logging.info(f"File size: {os.path.getsize(input_file)} bytes")
        
        with pdfplumber.open(input_file) as pdf:
            total_pages = len(pdf.pages)
            logging.info(f"Total pages in PDF: {total_pages}")
            
            start = max(1, start_page or 1)
            end = min(total_pages, end_page or total_pages)
            logging.info(f"Processing pages {start} to {end}")

            with open(output_file, 'w', encoding='utf-8') as jsonl_file:
                for page_num in range(start, end + 1):
                    page = pdf.pages[page_num - 1]
                    text = page.extract_text()
                    logging.info(f"Page {page_num}: Extracted {len(text)} characters")
                    
                    entry = {
                        "filename": input_file,
                        "page_number": page_num,
                        "content": text,
                        "metadata": {
                            "project_info": vars(project_info),
                            "agent_traits": vars(agent_traits)
                        }
                    }
                    json.dump(entry, jsonl_file)
                    jsonl_file.write('\n')

        logging.info(f"Conversion completed. Output saved to {output_file}")
    except Exception as e:
        logging.error(f"Error during conversion: {str(e)}")
        raise

# Additional utility functions can be added here as needed