from .agency_swarm.agents.nlp_documents_agent import NLPDocumentsAgent
from .file_converter import FileConverter
from .ai_service import AIService
import logging
import os

class AIGentSwarm:
    def __init__(self):
        logging.info("Initializing AIGentSwarm")
        self.file_converter = FileConverter()
        self.ai_service = AIService()
        self.nlp_documents_agent = NLPDocumentsAgent()

    def process_documents(self, input_files, output_dir, project_info, agent_traits, output_formats, use_ocr, use_cloud_vision):
        logging.info(f"Processing {len(input_files)} documents")
        results = []
        for input_file in input_files:
            logging.debug(f"Processing file: {input_file}")
            converted_data = self.file_converter.convert_file(
                input_file,
                output_dir,
                project_info,
                agent_traits,
                output_formats,
                use_ocr,
                use_cloud_vision
            )
            
            text_content = converted_data.get('content', '')
            
            nlp_result = self.nlp_documents_agent.process_document(text_content, output_dir)
            
            results.append({
                'input_file': input_file,
                'converted_data': converted_data,
                'nlp_result': nlp_result
            })
            logging.debug(f"Finished processing file: {input_file}")
        
        logging.info(f"Finished processing all documents. Total results: {len(results)}")
        return results

    def generate_training_data(self, input_files, output_dir):
        logging.info(f"Generating training data for {len(input_files)} files")
        results = []
        for input_file in input_files:
            logging.debug(f"Generating training data for file: {input_file}")
            try:
                with open(input_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                file_output_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])
                os.makedirs(file_output_dir, exist_ok=True)
                
                processed_content = self.nlp_documents_agent.process_document(content, file_output_dir)
                
                results.append({
                    'input_file': input_file,
                    'output_dir': file_output_dir,
                    'result': processed_content
                })
                logging.debug(f"Finished generating training data for file: {input_file}")
            except Exception as e:
                logging.error(f"Error processing file {input_file}: {str(e)}")
        
        logging.info(f"Finished generating training data. Total results: {len(results)}")
        return results

# Usage example:
# swarm = AIGentSwarm()
# results = swarm.process_documents(
#     input_files=['document1.pdf', 'document2.jpg'],
#     output_dir='/path/to/output',
#     project_info=project_info_object,
#     agent_traits=agent_traits_object,
#     output_formats=['jsonl', 'txt'],
#     use_ocr=True,
#     use_cloud_vision=False
# )
#
# training_data_results = swarm.generate_training_data(
#     input_files=['document1.txt', 'document2.txt'],
#     output_dir='/path/to/training_data_output'
# )