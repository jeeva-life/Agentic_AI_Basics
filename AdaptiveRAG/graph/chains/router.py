from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from model import llm_model

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource"""

    datasource: Literal["websearch", "vectorstore"] = Field(
        description="Given a user query, determine if the query is best suited for a web search or a vector store retrieval"
    )

llm = llm_model

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{query}"),
    ]
)

question_router = route_prompt | structured_llm_router