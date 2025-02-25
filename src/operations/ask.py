import logging
from src.api import execute_prompt
from src.operations.search import SearchEngine

logger = logging.getLogger('ask')

class LLMAsker:
    def __init__(self, embeddings_file: str):
        self.search_engine = SearchEngine(embeddings_file)

    def ask(self, question: str) -> str:
        logger.info(f"Retrieving documents for question: {question}")
        relevant_docs = self.search_engine.search(question, top_k=3)

        if not relevant_docs:
            return "No relevant documents found."

        context = "\n".join([f"[{doc}]: {score:.4f}" for doc, score in relevant_docs])
        prompt = f"You are an AI assistant. Answer the following question based on these documents:\n{context}\n\nQuestion: {question}"

        response = execute_prompt(prompt)

        if "response" in response:
            return response["response"] + f"\n\nSources: {[doc for doc, _ in relevant_docs]}"
        else:
            return "Error generating response from LLM."
