import json
import yaml
import pdfplumber
from datetime import datetime

CONFIG_FILE = "project_config.yaml"

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

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

def start_conversion(input_file, output_file, project_info):
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        with pdfplumber.open(input_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    entry = {
                        "filename": input_file,
                        "page_number": page_num,
                        "content": text,
                        "metadata": {
                            "project_info": vars(project_info)
                        }
                    }
                    json.dump(entry, jsonl_file)
                    jsonl_file.write('\n')
    print(f"Conversion complete. Output saved to {output_file}")