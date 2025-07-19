from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title: str = Field(description="title of BLOG post")
    content: str = Field(description="content of blog post")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    current_language:str