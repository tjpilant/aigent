import os
import sys
import traceback
from importlib.util import find_spec

# Add the parent directory to sys.path to allow importing aigent modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from aigent.aigent_swarm import AIGentSwarm
from aigent.models import ProjectInfo, AgentTraits
from aigent.utils.logger import get_logger

logger = get_logger(__name__)

def test_aigent_functionality():
    logger.info("Starting AIGent functionality test")

    # Check if required modules are importable
    if find_spec("aigent") is None:
        logger.error("aigent module not found")
        return

    # Initialize AIGentSwarm
    try:
        swarm = AIGentSwarm()
        logger.info("AIGentSwarm initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing AIGentSwarm: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return

    # Set up test parameters
    input_file = os.path.join(current_dir, 'test_document.txt')
    
    # Create a test document if it doesn't exist
    if not os.path.exists(input_file):
        with open(input_file, 'w') as f:
            f.write("This is a test document for AIGent functionality testing.")
        logger.info(f"Created test document: {input_file}")
    
    input_files = [input_file]
    output_dir = os.path.join(current_dir, 'test_output')
    os.makedirs(output_dir, exist_ok=True)
    
    project_info = ProjectInfo(project_title="Test Project")
    agent_traits = AgentTraits(data_purpose="Testing")
    output_formats = ['jsonl', 'txt']
    use_ocr = False
    use_cloud_vision = False

    logger.info(f"Test parameters set up: input_files={input_files}, output_dir={output_dir}")

    # Process documents
    try:
        results = swarm.process_documents(
            input_files,
            output_dir,
            project_info,
            agent_traits,
            output_formats,
            use_ocr,
            use_cloud_vision
        )
        logger.info(f"Document processing completed. Results: {results}")
    except Exception as e:
        logger.error(f"Error during document processing: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

    # Generate training data
    try:
        training_results = swarm.generate_training_data(input_files, output_dir)
        logger.info(f"Training data generation completed. Results: {training_results}")
    except Exception as e:
        logger.error(f"Error during training data generation: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

    logger.info("AIGent functionality test completed")

if __name__ == "__main__":
    test_aigent_functionality()
