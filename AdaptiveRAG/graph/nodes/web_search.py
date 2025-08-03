from typing import Dict, Any
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_tavily import TavilySearch
from graph.state import GraphState

load_dotenv()

web_search_tool = TavilySearch(max_results=2)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("Running web search...")
    question = state["question"]

    #Initialize docs - this was the missing part
    docs = state.get("documents", [])

    tavily_results = web_search_tool.invoke({"query": question})["results"]
    joined_results = "\n".join([tavily_result["content"] for tavily_result in tavily_results])

    web_results = Document(page_content = joined_results)

    # Add web results in existing docs (or create new list if documents is empty)
    if docs:
        docs.append(web_results)
    else:
        docs = [web_results]

    return {"documents": docs, "question": question}

if __name__ == "__main__":
    web_search(state={"question": "agent memory", "documents": []})