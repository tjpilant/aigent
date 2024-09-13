from typing import List, Dict, Any
from .agent import Agent

class Swarm:
    def __init__(self):
        self.agents: List[Agent] = []

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def remove_agent(self, agent: Agent):
        self.agents.remove(agent)

    def process_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for agent in self.agents:
            result = agent.process(task)
            results.append({"agent": str(agent), "result": result})
        return results

    def get_all_agents(self) -> List[Agent]:
        return self.agents

    def __str__(self):
        return f"Swarm(agents={len(self.agents)})"