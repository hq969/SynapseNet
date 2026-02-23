import logging
from abc import ABC, abstractmethod
from langchain_core.messages import HumanMessage, SystemMessage
from models.state import SynapseState, AgentMessage
from communication.event_bus import KafkaEventBus
from memory.vector_store import SynapseMemory

logger = logging.getLogger(__name__)

class BaseSynapseAgent(ABC):
    def __init__(self, agent_id: str, llm, event_bus: KafkaEventBus, memory: SynapseMemory):
        self.agent_id = agent_id
        self.llm = llm
        self.event_bus = event_bus
        self.memory = memory

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def __call__(self, state: SynapseState) -> SynapseState:
        logger.info(f"Agent {self.agent_id} executing...")
        
        past_wisdom = self.memory.recall(state['original_query'])
        system_msg = SystemMessage(content=f"{self.get_system_prompt()}\n\nPast Wisdom:\n{past_wisdom}")
        
        context_str = "\n".join([f"{m.agent_id}: {m.content}" for m in state['messages']])
        user_msg = HumanMessage(content=f"Context:\n{context_str}\n\nTask: {state['original_query']}")

        response = self.llm.invoke([system_msg, user_msg])
        
        new_msg = AgentMessage(agent_id=self.agent_id, content=response.content)
        self.event_bus.publish_event(topic="synapse.agent.updates", message=new_msg)
        self.memory.remember(self.agent_id, state['original_query'], response.content)

        state["messages"].append(new_msg)
        state["current_context"][f"{self.agent_id}_completed"] = True
        return state
