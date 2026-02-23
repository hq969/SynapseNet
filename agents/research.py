from agents.base import BaseSynapseAgent

class FinancialResearchAgent(BaseSynapseAgent):
    def get_system_prompt(self) -> str:
        return """You are a Quantitative Financial Research Agent. 
        Analyze the requested market data, perform sentiment extraction from context, 
        and generate a structured investor insight report."""
