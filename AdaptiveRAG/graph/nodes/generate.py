from typing import Dict, Any

from graph.chains.generation import generation_chain
from graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    print("Generating response...")
    question = state["question"]
    documents = state["documents"]

    result = generation_chain.invoke({"question": question, "context": documents})
    return {"documents": documents, "question": question, "generation": result}
