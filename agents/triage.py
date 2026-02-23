from agents.base import BaseSynapseAgent

class HealthcareTriageAgent(BaseSynapseAgent):
    def get_system_prompt(self) -> str:
        return """You are a highly analytical Healthcare Triage Agent. 
        Analyze the incoming patient symptoms, extract key vital anomalies, 
        and assign a priority level (CRITICAL, HIGH, MEDIUM, LOW) along with required medical unit type."""
