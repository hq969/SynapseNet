import os
import logging
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class SynapseMemory:
    """
    Manages long-term semantic memory for agents using pgvector.
    """
    def __init__(self, connection_string: str, collection_name: str = "agent_experiences"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Initialize pgvector store
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=collection_name,
            connection=connection_string,
            use_jsonb=True,
        )

    def remember(self, agent_id: str, query: str, solution: str, metadata: dict = None):
        """Stores a successful interaction in long-term memory."""
        full_text = f"Query: {query}\nSolution: {solution}"
        
        meta = metadata or {}
        meta.update({"agent_id": agent_id, "type": "success_record"})
        
        doc = Document(page_content=full_text, metadata=meta)
        self.vector_store.add_documents([doc])
        logger.info(f"Agent {agent_id} stored memory of task: {query[:30]}...")

    def recall(self, query: str, k: int = 3) -> str:
        """Retrieves the top-k most relevant past experiences."""
        docs = self.vector_store.similarity_search(query, k=k)
        
        if not docs:
            return "No relevant past experiences found."
            
        context = "\n---\n".join([d.page_content for d in docs])
        return context
