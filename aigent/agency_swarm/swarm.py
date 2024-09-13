from typing import List, Dict, Any
from .agent import Agent
from .agents.gpt_agent_developer import GPTAgentDeveloper, GPTAgent

class Agency:
    def __init__(self, name: str, db_path: str):
        self.name = name
        self.agents: List[Agent] = []
        self.gpt_agent_developer = GPTAgentDeveloper(db_path=db_path)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def remove_agent(self, agent: Agent):
        self.agents.remove(agent)

    def create_gpt_agent(self, profession: str):
        result = self.gpt_agent_developer.run(profession)
        new_agent = result['agent']
        self.add_agent(new_agent)
        return new_agent

    def get_gpt_agents(self) -> List[GPTAgent]:
        return [agent for agent in self.agents if isinstance(agent, GPTAgent)]

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for agent in self.agents:
            result = agent.run(task)
            results[str(agent)] = result
        return results

    def __str__(self):
        return f"Agency(name={self.name}, agents={len(self.agents)})"

class Swarm:
    def __init__(self):
        self.agencies: Dict[str, Agency] = {}

    def add_agency(self, agency: Agency):
        self.agencies[agency.name] = agency

    def remove_agency(self, agency_name: str):
        del self.agencies[agency_name]

    def get_agency(self, agency_name: str) -> Agency:
        return self.agencies.get(agency_name)

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for agency_name, agency in self.agencies.items():
            agency_result = agency.process_task(task)
            results[agency_name] = agency_result
        return self.aggregate_results(results)

    def aggregate_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Implement a more sophisticated result aggregation logic here
        # This is a placeholder implementation
        aggregated_result = {}
        for agency_name, agency_results in results.items():
            aggregated_result[agency_name] = agency_results
        return aggregated_result

    def inter_agency_communicate(self, from_agency: str, to_agency: str, message: Any):
        if from_agency in self.agencies and to_agency in self.agencies:
            # Implement inter-agency communication logic here
            pass

    def __str__(self):
        return f"Swarm(agencies={len(self.agencies)})"