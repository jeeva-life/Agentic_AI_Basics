from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents state of the attributes of the graph
    """
    question: str 
    generation: str
    web_search: bool
    documents: list[str]
