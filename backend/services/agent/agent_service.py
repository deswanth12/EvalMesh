from typing import List, Optional, Dict, Any
from backend.repositories.agent_repository import agent_repository, AgentRepository
from backend.schemas.agent import AgentCreate

class AgentService:
    """
    Business Logic Service Layer for AI Agent Lifecycle.
    """
    def __init__(self, repo: AgentRepository = agent_repository):
        self.repo = repo

    def get_registered_agents(self) -> List[Dict[str, Any]]:
        return self.repo.list_all()

    def register_new_agent(self, agent_in: AgentCreate) -> Dict[str, Any]:
        # Domain validation: enforce naming standards
        if len(agent_in.name.strip()) < 3:
            raise ValueError("Agent name must be at least 3 characters long.")
        return self.repo.create(agent_in)

agent_service = AgentService()
