import sqlite3
from typing import Dict, Any
from ..tools.base_tool import BaseTool
from pydantic import Field
from ...utils.logger import get_logger

logger = get_logger(__name__)

class GPTAgentDeveloper(BaseTool):
    """
    A tool for developing and managing GPT agents based on descriptors from a database.
    """
    db_path: str = Field(..., description="Path to the SQLite database containing agent descriptors.")

    def run(self, profession: str) -> Dict[str, Any]:
        """
        Create a GPT agent based on the given profession.
        """
        logger.info(f"Creating GPT agent for profession: {profession}")
        descriptor = self.fetch_agent_descriptor(profession)
        agent = self.create_agent_from_descriptor(descriptor)
        return {"agent": agent, "descriptor": descriptor}

    def fetch_agent_descriptor(self, profession: str) -> Dict[str, Any]:
        """
        Fetch the agent descriptor from the database.
        """
        logger.debug(f"Fetching agent descriptor for profession: {profession}")
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM agent_descriptors WHERE profession=?", (profession,))
        row = cursor.fetchone()
        
        if row:
            descriptor = {
                "profession": row[1],
                "key_responsibilities": row[2],
                "typical_challenges": row[3],
                "current_projects": row[4],
                "jargon_terminology": row[5],
                "goals_objectives": row[6],
                "interactions": row[7],
                "tone_formality": row[8],
                "level_of_detail": row[9],
                "preferred_references": row[10],
                "examples_analogies": row[11],
                "promptness": row[12],
                "collaborative_approach": row[13],
                "follow_up_questions": row[14],
            }
            connection.close()
            logger.info(f"Agent descriptor fetched for profession: {profession}")
            return descriptor
        else:
            connection.close()
            logger.error(f"No agent descriptor found for profession: {profession}")
            raise ValueError(f"No agent descriptor found for profession: {profession}")

    def create_agent_from_descriptor(self, descriptor: Dict[str, Any]) -> 'GPTAgent':
        """
        Create a GPT agent based on the descriptor.
        """
        logger.info(f"Creating GPT agent from descriptor for profession: {descriptor['profession']}")
        return GPTAgent(**descriptor)

class GPTAgent(BaseTool):
    """
    A dynamically created GPT agent based on the profession descriptor.
    """
    profession: str = Field(..., description="The profession or role of the agent.")
    key_responsibilities: str = Field(..., description="Key responsibilities for the agent.")
    typical_challenges: str = Field(..., description="Typical challenges for this role.")
    current_projects: str = Field(..., description="Current projects for this role.")
    jargon_terminology: str = Field(..., description="Key jargon or terminology.")
    goals_objectives: str = Field(..., description="Goals and objectives for the role.")
    interactions: str = Field(..., description="Who the agent interacts with.")
    tone_formality: str = Field(..., description="The tone and formality level of the agent.")
    level_of_detail: str = Field(..., description="The level of detail expected in responses.")
    preferred_references: str = Field(..., description="Preferred references for the agent.")
    examples_analogies: str = Field(..., description="Examples or analogies the agent should use.")
    promptness: str = Field(..., description="Expected promptness of the agent.")
    collaborative_approach: str = Field(..., description="Collaborative approach the agent should follow.")
    follow_up_questions: str = Field(..., description="Common follow-up questions to ask.")

    def run(self, input_data: Dict[str, Any]) -> str:
        """
        Execute the agent's task based on its descriptor and input data.
        """
        task = input_data.get("task", "")
        document = input_data.get("document", "")

        logger.info(f"GPT Agent {self.profession} executing task: {task}")

        if task == "process_document":
            return self.process_document(document)
        elif task == "generate_training_data":
            return self.generate_training_data(document)
        else:
            logger.warning(f"Unknown task for GPT Agent {self.profession}: {task}")
            return f"Unknown task: {task}"

    def process_document(self, document: str) -> str:
        """
        Process a document based on the agent's expertise.
        """
        logger.info(f"GPT Agent {self.profession} processing document")
        response = f"As a {self.profession}, I have processed the document.\n"
        response += f"Key insights based on {self.key_responsibilities}:\n"
        response += "1. [Insert insight related to the document]\n"
        response += "2. [Insert another insight]\n"
        response += f"Potential challenges identified: {self.typical_challenges}\n"
        response += f"Relevant projects: {self.current_projects}\n"
        response += f"Follow-up questions: {self.follow_up_questions}"
        return response

    def generate_training_data(self, document: str) -> str:
        """
        Generate training data based on the agent's expertise.
        """
        logger.info(f"GPT Agent {self.profession} generating training data")
        response = f"As a {self.profession}, I have generated training data from the document.\n"
        response += "Training data format: [Specify format, e.g., Q&A pairs, labeled entities]\n"
        response += "1. [Example training data point]\n"
        response += "2. [Another example training data point]\n"
        response += f"Key terminology used: {self.jargon_terminology}\n"
        response += f"Data generation approach: {self.collaborative_approach}"
        return response

    def __str__(self):
        return f"GPTAgent(profession={self.profession})"
