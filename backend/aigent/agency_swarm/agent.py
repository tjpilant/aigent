from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, List, TypeVar, Generic
from pydantic import BaseModel, Field

from ..utils.logger import get_logger
from ..utils.exceptions import CapabilityError, ProcessingError

T = TypeVar('T')

logger = get_logger(__name__)

class Capability(BaseModel, Generic[T]):
    name: str
    function: Callable[..., T]

class Agent(BaseModel, ABC):
    name: str = Field(..., description="Name of the agent")
    capabilities: Dict[str, Capability] = Field(default_factory=dict, description="Agent capabilities")

    @abstractmethod
    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task and return the result.
        """
        pass

    def register_capability(self, name: str, function: Callable[..., Any]) -> None:
        """
        Register a new capability for the agent.
        """
        try:
            if name in self.capabilities:
                raise CapabilityError(f"Capability '{name}' already exists")
            self.capabilities[name] = Capability(name=name, function=function)
            logger.info(f"Capability '{name}' registered for agent '{self.name}'")
        except Exception as e:
            logger.error(f"Error registering capability '{name}' for agent '{self.name}': {str(e)}")
            raise

    def get_capability(self, name: str) -> Callable[..., Any]:
        """
        Get a registered capability by name.
        """
        try:
            if name not in self.capabilities:
                raise CapabilityError(f"Capability '{name}' not found")
            return self.capabilities[name].function
        except Exception as e:
            logger.error(f"Error retrieving capability '{name}' for agent '{self.name}': {str(e)}")
            raise

    def remove_capability(self, name: str) -> None:
        """
        Remove a capability from the agent.
        """
        try:
            if name not in self.capabilities:
                raise CapabilityError(f"Capability '{name}' not found")
            del self.capabilities[name]
            logger.info(f"Capability '{name}' removed from agent '{self.name}'")
        except Exception as e:
            logger.error(f"Error removing capability '{name}' from agent '{self.name}': {str(e)}")
            raise

    def update_capability(self, name: str, function: Callable[..., Any]) -> None:
        """
        Update an existing capability of the agent.
        """
        try:
            if name not in self.capabilities:
                raise CapabilityError(f"Capability '{name}' not found")
            self.capabilities[name] = Capability(name=name, function=function)
            logger.info(f"Capability '{name}' updated for agent '{self.name}'")
        except Exception as e:
            logger.error(f"Error updating capability '{name}' for agent '{self.name}': {str(e)}")
            raise

    def list_capabilities(self) -> List[str]:
        """
        List all registered capabilities.
        """
        return list(self.capabilities.keys())

    def sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform sentiment analysis on the given text.
        """
        # Placeholder implementation
        logger.debug(f"Performing sentiment analysis for agent '{self.name}'")
        return {"sentiment": "neutral", "confidence": 0.5}

    def entity_recognition(self, text: str) -> List[Dict[str, Any]]:
        """
        Perform entity recognition on the given text.
        """
        # Placeholder implementation
        logger.debug(f"Performing entity recognition for agent '{self.name}'")
        return [{"entity": "example", "type": "MISC", "start": 0, "end": 7}]

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, capabilities={self.list_capabilities()})"

# Example of how to use the new capabilities
class ExampleAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.register_capability("sentiment_analysis", self.sentiment_analysis)
        self.register_capability("entity_recognition", self.entity_recognition)

    def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = {}
            if "text" in task:
                result["sentiment"] = self.get_capability("sentiment_analysis")(task["text"])
                result["entities"] = self.get_capability("entity_recognition")(task["text"])
            logger.info(f"Task processed successfully by agent '{self.name}'")
            return result
        except Exception as e:
            logger.error(f"Error processing task by agent '{self.name}': {str(e)}")
            raise ProcessingError(f"Error processing task: {str(e)}")
