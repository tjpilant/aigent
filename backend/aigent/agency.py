from agency_swarm import Agency
from agents.ceo.ceo import CEOAgent
from agents.developer.developer import DeveloperAgent

class AigentAgency(Agency):
    def __init__(self):
        super().__init__(
            name="Aigent",
            description="An AI-powered agency focused on software development and project management.",
            agents=[
                CEOAgent(),
                DeveloperAgent(),
                # We'll add more agents here as we create them
            ],
            communication_flows=[
                ("CEO", "Developer"),
                ("Developer", "CEO"),
                # We'll add more communication flows as we add more agents
            ],
            shared_instructions="agency_manifesto.md"
        )

# Agency initialization and other necessary setup will be added here

if __name__ == "__main__":
    agency = AigentAgency()
    # Add any startup or test code here
    print(f"Aigent Agency initialized with {len(agency.agents)} agent(s).")
    for agent in agency.agents:
        print(f"- {agent.name}: {agent.description}")
    
    print("\nCommunication Flows:")
    for flow in agency.communication_flows:
        print(f"- {flow[0]} -> {flow[1]}")
