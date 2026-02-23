import argparse
import uuid
import logging
from langchain_openai import ChatOpenAI
from config.settings import settings
from communication.event_bus import KafkaEventBus
from memory.vector_store import SynapseMemory
from agents.triage import HealthcareTriageAgent
from agents.research import FinancialResearchAgent
from orchestrator.graph import SynapseOrchestrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_orchestrator(task_query: str):
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4-turbo", temperature=0)
    event_bus = KafkaEventBus(broker_url=settings.KAFKA_BROKER)
    memory = SynapseMemory()

    triage = HealthcareTriageAgent("Triage_Node", llm, event_bus, memory)
    research = FinancialResearchAgent("Research_Node", llm, event_bus, memory)

    orchestrator = SynapseOrchestrator()
    orchestrator.register_agent(triage)
    orchestrator.register_agent(research)
    
    app = orchestrator.build_pipeline(entry_id="Triage_Node", edges=[("Triage_Node", "Research_Node")])

    initial_state = {
        "task_id": str(uuid.uuid4()),
        "original_query": task_query,
        "messages": [],
        "current_context": {},
        "status": "processing"
    }

    logging.info(f"Starting pipeline for Task: {initial_state['task_id']}")
    final_state = app.invoke(initial_state)

    for msg in final_state['messages']:
        logging.info(f"[{msg.agent_id}]: {msg.content}")

    event_bus.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SynapseNet Node CLI")
    parser.add_argument("--role", choices=["orchestrator", "agent"], required=True)
    parser.add_argument("--task", type=str, help="Task description for the orchestrator")
    
    args = parser.parse_args()

    if args.role == "orchestrator":
        if not args.task:
            logging.error("A --task must be provided for the orchestrator.")
        else:
            run_orchestrator(args.task)
    elif args.role == "agent":
        logging.info("Agent daemon mode not yet mapped in CLI. See gRPC stubs.")
