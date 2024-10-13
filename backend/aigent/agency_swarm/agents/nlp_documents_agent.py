from ..agent import Agent
from ..tools.nlp_documents_tool import NLPDocumentsTool
from typing import Dict, Any
from ...utils.logger import get_logger
import os

logger = get_logger(__name__)

class NLPDocumentsAgent(Agent):
    """
    An agent responsible for NLP document processing tasks, including generating training data pairs.
    """

    def __init__(self, name: str = "NLPDocumentsAgent"):
        super().__init__(name=name)

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task using the NLPDocumentsTool and generate training data pairs.
        """
        logger.info("NLPDocumentsAgent processing task")
        
        text = task.get('text')
        output_dir = task.get('output_dir')

        return self.process_document(text, output_dir)

    def process_document(self, text: str, output_dir: str = None) -> Dict[str, Any]:
        """
        Process a document using the NLPDocumentsTool and generate training data pairs.
        """
        logger.info("NLPDocumentsAgent processing document")

        if not text:
            logger.error("No text provided for processing")
            return {"error": "No text provided for processing"}

        nlp_tool = NLPDocumentsTool(text=text, output_dir=output_dir)
        result = nlp_tool.run()
        
        if output_dir:
            logger.info(f"Training data saved to {output_dir}")
            return {"status": "success", "message": f"Training data saved to {output_dir}"}
        else:
            logger.info("Returning processed data")
            return {"status": "success", "data": result}

    def __str__(self):
        return f"NLPDocumentsAgent(name={self.name})"
