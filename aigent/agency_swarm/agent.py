from typing import List, Dict, Any

class Agent:
    def __init__(self, name: str, role: str, goals: List[str]):
        self.name = name
        self.role = role
        self.goals = goals
        self.memory: List[Dict[str, Any]] = []

    def process(self, input_data: Any) -> Any:
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses must implement the process method")

    def add_to_memory(self, data: Dict[str, Any]):
        self.memory.append(data)

    def get_memory(self) -> List[Dict[str, Any]]:
        return self.memory

    def __str__(self):
        return f"Agent(name={self.name}, role={self.role})"