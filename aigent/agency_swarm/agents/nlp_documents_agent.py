from ..agent import Agent
from ..tools.nlp_documents_tool import NLPDocumentsTool
from typing import Dict, Any
import logging
import os

class NLPDocumentsAgent(Agent):
    """
    An agent responsible for NLP document processing tasks, including generating training data pairs.
    """

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task using the NLPDocumentsTool and generate training data pairs.
        """
        logging.info(f"NLPDocumentsAgent processing task")
        
        text = task.get('text')
        output_dir = task.get('output_dir')

        if not text:
            return {"error": "No text provided in the task"}

        nlp_tool = NLPDocumentsTool(text=text, output_dir=output_dir)
        result = nlp_tool.run()
        
        if output_dir:
            logging.info(f"Training data saved to {output_dir}")
            return {"status": "success", "message": f"Training data saved to {output_dir}"}
        else:
            logging.info(f"Returning processed data")
            return {"status": "success", "data": result}

    def __str__(self):
        return f"NLPDocumentsAgent(name={self.name})"