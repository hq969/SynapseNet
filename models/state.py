from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AgentMessage(BaseModel):
    agent_id: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SynapseState(TypedDict):
    task_id: str
    original_query: str
    messages: List[AgentMessage]
    current_context: Dict[str, Any]
    status: str
