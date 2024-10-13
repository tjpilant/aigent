# File: models.py
# Author: Tj Pilant
# Description: Defines data models used across the application
# Version: 0.2.2

from dataclasses import asdict, dataclass, field
from typing import Any, Dict

@dataclass
class AgentTraits:
    data_purpose: str
    additional_traits: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def add_trait(self, key: str, value: Any):
        self.additional_traits[key] = value

    def get_trait(self, key: str) -> Any:
        return self.additional_traits.get(key)

@dataclass
class ProjectInfo:
    project_title: str
    description: str = ""
    version: str = "1.0"
    additional_info: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def add_info(self, key: str, value: Any):
        self.additional_info[key] = value

    def get_info(self, key: str) -> Any:
        return self.additional_info.get(key)

# Usage example
if __name__ == "__main__":
    # Create an instance of AgentTraits
    agent_traits = AgentTraits(data_purpose="Text analysis")
    agent_traits.add_trait("language", "English")
    agent_traits.add_trait("domain", "Scientific")
    
    print("Agent Traits:", agent_traits.to_dict())
    print("Language:", agent_traits.get_trait("language"))

    # Create an instance of ProjectInfo
    project_info = ProjectInfo(
        project_title="Document Analysis Project",
        description="Analyzing scientific papers",
        version="2.0"
    )
    project_info.add_info("lead_researcher", "Dr. Jane Doe")
    
    print("Project Info:", project_info.to_dict())
    print("Lead Researcher:", project_info.get_info("lead_researcher"))
