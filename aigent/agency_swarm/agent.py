from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic import BaseModel, Field

class Agent(BaseModel, ABC):
    name: str = Field(..., description="Name of the agent")

    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task and return the result.
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"