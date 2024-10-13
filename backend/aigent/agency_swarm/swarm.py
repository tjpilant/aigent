from typing import List, Dict, Any
from .agent import Agent
from .agents.gpt_agent_developer import GPTAgentDeveloper, GPTAgent
from ..utils.logger import get_logger
from ..utils.exceptions import SwarmError, AgentError

logger = get_logger(__name__)

class Agency:
    def __init__(self, name: str, db_path: str):
        self.name = name
        self.db_path = db_path
        self.agents: List[Agent] = []
        self.gpt_agent_developer = GPTAgentDeveloper(db_path=db_path)
        logger.info(f"Agency '{name}' initialized")

    def add_agent(self, agent: Agent):
        try:
            self.agents.append(agent)
            logger.info(f"Agent '{agent.name}' added to agency '{self.name}'")
        except Exception as e:
            logger.error(f"Error adding agent '{agent.name}' to agency '{self.name}': {str(e)}")
            raise AgentError(f"Error adding agent: {str(e)}")

    def remove_agent(self, agent: Agent):
        try:
            self.agents.remove(agent)
            logger.info(f"Agent '{agent.name}' removed from agency '{self.name}'")
        except ValueError:
            logger.error(f"Agent '{agent.name}' not found in agency '{self.name}'")
            raise AgentError(f"Agent '{agent.name}' not found in agency '{self.name}'")
        except Exception as e:
            logger.error(f"Error removing agent '{agent.name}' from agency '{self.name}': {str(e)}")
            raise AgentError(f"Error removing agent: {str(e)}")

    def create_gpt_agent(self, profession: str) -> Agent:
        try:
            result = self.gpt_agent_developer.run(profession)
            new_agent = result['agent']
            self.add_agent(new_agent)
            logger.info(f"GPT Agent '{new_agent.name}' created and added to agency '{self.name}'")
            return new_agent
        except Exception as e:
            logger.error(f"Error creating GPT agent for profession '{profession}' in agency '{self.name}': {str(e)}")
            raise AgentError(f"Error creating GPT agent: {str(e)}")

    def get_gpt_agents(self) -> List[GPTAgent]:
        return [agent for agent in self.agents if isinstance(agent, GPTAgent)]

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for agent in self.agents:
            try:
                result = agent.process(task)
                results[str(agent)] = result
                logger.info(f"Task processed by agent '{agent.name}' in agency '{self.name}'")
            except Exception as e:
                logger.error(f"Error processing task with agent '{agent.name}' in agency '{self.name}': {str(e)}")
                results[str(agent)] = {"error": str(e)}
        return results

    def __str__(self):
        return f"Agency(name={self.name}, agents={len(self.agents)})"

class Swarm:
    def __init__(self):
        self.agencies: Dict[str, Agency] = {}
        logger.info("Swarm initialized")

    def add_agency(self, agency: Agency):
        try:
            self.agencies[agency.name] = agency
            logger.info(f"Agency '{agency.name}' added to swarm")
        except Exception as e:
            logger.error(f"Error adding agency '{agency.name}' to swarm: {str(e)}")
            raise SwarmError(f"Error adding agency: {str(e)}")

    def remove_agency(self, agency_name: str):
        try:
            del self.agencies[agency_name]
            logger.info(f"Agency '{agency_name}' removed from swarm")
        except KeyError:
            logger.error(f"Agency '{agency_name}' not found in swarm")
            raise SwarmError(f"Agency '{agency_name}' not found in swarm")
        except Exception as e:
            logger.error(f"Error removing agency '{agency_name}' from swarm: {str(e)}")
            raise SwarmError(f"Error removing agency: {str(e)}")

    def get_agency(self, agency_name: str) -> Agency:
        try:
            return self.agencies[agency_name]
        except KeyError:
            logger.error(f"Agency '{agency_name}' not found in swarm")
            raise SwarmError(f"Agency '{agency_name}' not found in swarm")

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for agency_name, agency in self.agencies.items():
            try:
                agency_result = agency.process_task(task)
                results[agency_name] = agency_result
                logger.info(f"Task processed by agency '{agency_name}'")
            except Exception as e:
                logger.error(f"Error processing task with agency '{agency_name}': {str(e)}")
                results[agency_name] = {"error": str(e)}
        return self.aggregate_results(results)

    def aggregate_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Implement a more sophisticated result aggregation logic here
        # This is a placeholder implementation
        aggregated_result = {}
        for agency_name, agency_results in results.items():
            aggregated_result[agency_name] = agency_results
        logger.info("Results aggregated across all agencies")
        return aggregated_result

    def inter_agency_communicate(self, from_agency: str, to_agency: str, message: Any):
        if from_agency in self.agencies and to_agency in self.agencies:
            # Implement inter-agency communication logic here
            logger.info(f"Inter-agency communication from '{from_agency}' to '{to_agency}'")
            pass
        else:
            logger.error(f"Inter-agency communication failed: agency not found")
            raise SwarmError("Inter-agency communication failed: agency not found")

    def __str__(self):
        return f"Swarm(agencies={len(self.agencies)})"
