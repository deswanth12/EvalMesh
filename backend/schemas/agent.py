from typing import Optional
from pydantic import BaseModel, Field

class AgentBase(BaseModel):
    name: str = Field(..., example="Support Bot v2")
    version: str = Field(default="v1.0.0", example="v1.0.0")
    model: str = Field(default="gpt-4o", example="gpt-4o")
    environment: str = Field(default="production", example="production")

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: str
    status: str = "ACTIVE"
    created_at: float

    class Config:
        from_attributes = True
