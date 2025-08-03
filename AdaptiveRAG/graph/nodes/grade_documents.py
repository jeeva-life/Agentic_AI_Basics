from typing import Dict, Any
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("Check if documents are relevant to the question")
    question = state["question"]
    documents = state["documents"]

    filtered_documents = []
    web_search = False
    for d in documents:
        result = retrieval_grader.invoke({"question": question, "document": d.page_content})

        grade = result.binary_score
        if grade.lower() == "yes":
            print("Document is relevant to the question")
            filtered_documents.append(d)
        else:
            print("Document is not relevant to the question")
            web_search = True
            continue
    return {"documents": filtered_documents, "web_search": web_search, "question": question}
