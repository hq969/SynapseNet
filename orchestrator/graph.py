from langgraph.graph import StateGraph, END
from models.state import SynapseState
from agents.base import BaseSynapseAgent

class SynapseOrchestrator:
    def __init__(self):
        self.graph = StateGraph(SynapseState)

    def register_agent(self, agent: BaseSynapseAgent):
        self.graph.add_node(agent.agent_id, agent)

    def build_pipeline(self, entry_id: str, edges: list[tuple[str, str]]):
        self.graph.set_entry_point(entry_id)
        for source, target in edges:
            self.graph.add_edge(source, target)
        
        last_node = edges[-1][1] if edges else entry_id
        self.graph.add_edge(last_node, END)
        
        return self.graph.compile()
