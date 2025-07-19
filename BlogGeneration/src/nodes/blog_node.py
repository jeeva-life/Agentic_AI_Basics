from src.states.blogstate import BlogState


class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self,llm):
        self.llm=llm

    def title_creation(self, state: BlogState):
        """
        create title of the blog
        """
        if "topic" in state and state["topic"]:
            prompt="""you are an expert blog content writer.
                    use markdown formatting.
                    Generate a blog title for the topic {topic}.
                    This title should be creative and SEO friendly.
                    """
            
            system_message=prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)

            return {"blog":{"title": response.content}}
        
    def content_generator(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt="""you are an expert BLOG WRITER.
                            use MARKDOWN formatting
                            Generate a detailed blog content with detailed breakdown for the topic {topic}"""
            
            system_message=system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}