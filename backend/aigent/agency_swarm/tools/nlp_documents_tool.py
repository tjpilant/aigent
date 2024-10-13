from .base_tool import BaseTool
from pydantic import Field
import json
import os
from ...utils.logger import get_logger

logger = get_logger(__name__)

class NLPDocumentsTool(BaseTool):
    """
    A tool to process NLP documents and generate Prompt → Completion and Question → Answer pairs for model training.
    """
    text: str = Field(..., description="The input text to process.")
    output_dir: str = Field(None, description="The directory to save the generated pairs. If None, return the pairs instead.")

    def run(self):
        logger.info("Running NLPDocumentsTool")
        processor = NLPDocumentProcessor(self.text)
        prompt_completion_pairs = processor.generate_prompt_completion_pairs()
        question_answer_pairs = processor.generate_question_answer_pairs()
        
        if self.output_dir:
            pc_file = os.path.join(self.output_dir, "pc_training_data.jsonl")
            qa_file = os.path.join(self.output_dir, "qa_training_data.jsonl")
            processor.save_pairs_to_file(prompt_completion_pairs, pc_file)
            processor.save_pairs_to_file(question_answer_pairs, qa_file)
            logger.info(f"Generated prompt-completion pairs saved to {pc_file}")
            logger.info(f"Generated question-answer pairs saved to {qa_file}")
            return f"Generated prompt-completion pairs saved to {pc_file}\nGenerated question-answer pairs saved to {qa_file}"
        else:
            logger.info("Returning generated pairs")
            return {
                "prompt_completion": prompt_completion_pairs,
                "question_answer": question_answer_pairs
            }

class NLPDocumentProcessor:
    def __init__(self, text):
        self.text = text
    
    def generate_prompt_completion_pairs(self):
        logger.debug("Generating prompt-completion pairs")
        sentences = self.text.split('. ')
        pairs = []
        for i in range(len(sentences) - 1):
            prompt = sentences[i].strip()
            completion = sentences[i+1].strip()
            if prompt and completion:
                pairs.append({"prompt": prompt, "completion": completion})
        logger.info(f"Generated {len(pairs)} prompt-completion pairs")
        return pairs
    
    def generate_question_answer_pairs(self):
        logger.debug("Generating question-answer pairs")
        sentences = self.text.split('. ')
        pairs = []
        for i in range(len(sentences) - 1):
            question = f"What follows this statement: {sentences[i].strip()}?"
            answer = sentences[i+1].strip()
            if question and answer:
                pairs.append({"question": question, "answer": answer})
        logger.info(f"Generated {len(pairs)} question-answer pairs")
        return pairs
    
    def save_pairs_to_file(self, pairs, file_name):
        logger.info(f"Saving pairs to file: {file_name}")
        with open(file_name, 'w', encoding='utf-8') as f:
            for pair in pairs:
                json.dump(pair, f)
                f.write('\n')
        logger.info(f"Saved {len(pairs)} pairs to {file_name}")
