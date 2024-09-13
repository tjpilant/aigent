from ..tools.nlp_documents_tool import NLPDocumentsTool
from pydantic import BaseModel, Field
import logging
import os

class NLPDocumentsAgent(BaseModel):
    """
    An agent responsible for NLP document processing tasks, including generating training data pairs.
    """
    name: str = Field(default="NLP Documents Agent", description="Name of the NLP Documents agent")

    def process_document(self, text: str, output_dir: str = None):
        """
        Process a document using the NLPDocumentsTool and generate training data pairs.
        If output_dir is provided, save the results to that directory.
        Otherwise, return the processed data.
        """
        logging.info(f"NLPDocumentsAgent processing document")
        nlp_tool = NLPDocumentsTool(text=text, output_dir=output_dir)
        result = nlp_tool.run()
        
        if output_dir:
            logging.info(f"Training data saved to {output_dir}")
            return result
        else:
            logging.info(f"Returning processed data")
            return result

    def __str__(self):
        return f"NLPDocumentsAgent(name={self.name})"