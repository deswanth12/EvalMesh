import time
from typing import List, Optional, Dict, Any
from backend.schemas.agent import AgentCreate

class AgentRepository:
    """
    Decoupled Repository Layer for Agent persistence.
    Decouples SQL/Storage implementation from business logic.
    """
    def __init__(self):
        self._agents: Dict[str, Dict[str, Any]] = {
            "ag_101": {
                "id": "ag_101",
                "name": "Support Bot v2",
                "version": "v1.0.0",
                "model": "gpt-4o",
                "environment": "production",
                "status": "ACTIVE",
                "created_at": time.time() - 86400
            },
            "ag_102": {
                "id": "ag_102",
                "name": "Financial Agent",
                "version": "v2.1.0",
                "model": "claude-3-5-sonnet",
                "environment": "staging",
                "status": "HUMAN_APPROVAL_REQ",
                "created_at": time.time() - 43200
            }
        }

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self._agents.values())

    def get_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return self._agents.get(agent_id)

    def create(self, agent_data: AgentCreate) -> Dict[str, Any]:
        agent_id = f"ag_{int(time.time()*1000)}"
        item = {
            "id": agent_id,
            "name": agent_data.name,
            "version": agent_data.version,
            "model": agent_data.model,
            "environment": agent_data.environment,
            "status": "ACTIVE",
            "created_at": time.time()
        }
        self._agents[agent_id] = item
        return item

agent_repository = AgentRepository()
