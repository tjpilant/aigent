from .agency_swarm.agents.nlp_documents_agent import NLPDocumentsAgent
from .agency_swarm.swarm import Swarm, Agency
from .file_converter import FileConverter
from .ai_service import AIService
from .utils.logger import get_logger
import os

logger = get_logger(__name__)

class AIGentSwarm:
    def __init__(self):
        logger.info("Initializing AIGentSwarm")
        self.file_converter = FileConverter()
        self.ai_service = AIService()
        self.nlp_documents_agent = NLPDocumentsAgent()
        self.swarm = Swarm()
        self.agency = Agency("MainAgency", "agent_descriptors.db")
        self.swarm.add_agency(self.agency)
        logger.info("AIGentSwarm initialized successfully", extra={"num_agencies": len(self.swarm.agencies)})

    def process_documents(self, input_files, output_dir, project_info, agent_traits, output_formats, use_ocr, use_cloud_vision):
        logger.info("Starting document processing", extra={"num_documents": len(input_files), "output_formats": output_formats, "use_ocr": use_ocr, "use_cloud_vision": use_cloud_vision})
        results = []
        for input_file in input_files:
            logger.debug("Processing file", extra={"file": input_file})
            try:
                converted_data = self.file_converter.convert_file(
                    input_file,
                    output_dir,
                    project_info,
                    agent_traits,
                    output_formats,
                    use_ocr,
                    use_cloud_vision
                )
                
                # Extract text content from the converted data
                text_content = ""
                for format, file_path in converted_data.items():
                    if format == 'txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text_content = f.read()
                        break
                
                if not text_content:
                    logger.warning("No text content found for file", extra={"file": input_file})
                else:
                    logger.info("Text content extracted successfully", extra={"file": input_file, "content_length": len(text_content)})
                
                nlp_result = self.nlp_documents_agent.process_document(text_content, output_dir)
                logger.info("NLP processing completed", extra={"file": input_file})
                
                # Process with GPT agents
                gpt_results = self.process_with_gpt_agents(text_content)
                
                results.append({
                    'input_file': input_file,
                    'converted_data': converted_data,
                    'nlp_result': nlp_result,
                    'gpt_results': gpt_results
                })
                logger.debug("Finished processing file", extra={"file": input_file})
            except Exception as e:
                logger.error("Error processing file", extra={"file": input_file, "error": str(e)})
        
        logger.info("Finished processing all documents", extra={"total_results": len(results)})
        return results

    def process_with_gpt_agents(self, text_content):
        logger.info("Starting GPT agent processing", extra={"content_length": len(text_content)})
        gpt_results = {}
        for agent in self.agency.agents:
            try:
                agent_result = agent.run({"task": "process_document", "document": text_content})
                gpt_results[str(agent)] = agent_result
                logger.info("GPT Agent processed document successfully", extra={"agent": str(agent)})
            except Exception as e:
                logger.error("Error in GPT agent document processing", extra={"agent": str(agent), "error": str(e)})
                gpt_results[str(agent)] = f"Error: {str(e)}"
        logger.info("Finished GPT agent processing", extra={"num_agents": len(self.agency.agents)})
        return gpt_results

    def generate_training_data(self, input_files, output_dir):
        logger.info("Starting training data generation", extra={"num_files": len(input_files), "output_dir": output_dir})
        results = []
        for input_file in input_files:
            logger.debug("Generating training data for file", extra={"file": input_file})
            try:
                with open(input_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                file_output_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])
                os.makedirs(file_output_dir, exist_ok=True)
                
                processed_content = self.nlp_documents_agent.process_document(content, file_output_dir)
                logger.info("NLP processing completed for training data", extra={"file": input_file})
                
                # Generate training data with GPT agents
                gpt_training_data = self.generate_gpt_training_data(content)
                
                results.append({
                    'input_file': input_file,
                    'output_dir': file_output_dir,
                    'result': processed_content,
                    'gpt_training_data': gpt_training_data
                })
                logger.debug("Finished generating training data for file", extra={"file": input_file})
            except Exception as e:
                logger.error("Error processing file for training data", extra={"file": input_file, "error": str(e)})
        
        logger.info("Finished generating training data", extra={"total_results": len(results)})
        return results

    def generate_gpt_training_data(self, content):
        logger.info("Starting GPT training data generation", extra={"content_length": len(content)})
        gpt_training_data = {}
        for agent in self.agency.agents:
            try:
                agent_result = agent.run({"task": "generate_training_data", "document": content})
                gpt_training_data[str(agent)] = agent_result
                logger.info("GPT Agent generated training data successfully", extra={"agent": str(agent)})
            except Exception as e:
                logger.error("Error in GPT agent training data generation", extra={"agent": str(agent), "error": str(e)})
                gpt_training_data[str(agent)] = f"Error: {str(e)}"
        logger.info("Finished GPT training data generation", extra={"num_agents": len(self.agency.agents)})
        return gpt_training_data

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
