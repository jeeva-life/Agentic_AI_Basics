from langgraph.graph import StateGraph, END
from src.models.state import AgentState
from src.agents.transcript_agent import TranscriptAgent
from src.agents.title_agent import TitleAgent
from src.agents.content_agent import ContentAgent
from src.config.settings import settings
from utils.logger import setup_logger
from utils.exceptions import WorkflowException
from typing import Dict, Any
from fastapi import HTTPException

logger = setup_logger(__name__)

class YouTubeWorkflow:
    """Main workflow orchestrating all agents"""
    
    def __init__(self):
        # Initialize agents
        self.transcript_agent = TranscriptAgent()
        self.title_agent = TitleAgent()
        self.content_agent = ContentAgent()
        
        # Build workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add agent nodes
        workflow.add_node("transcript_agent", self.transcript_agent.process)
        workflow.add_node("title_agent", self.title_agent.process)
        workflow.add_node("content_agent", self.content_agent.process)
        
        # Define workflow edges
        workflow.set_entry_point("transcript_agent")
        workflow.add_edge("transcript_agent", "title_agent")
        workflow.add_edge("title_agent", "content_agent")
        workflow.add_edge("content_agent", END)
        
        return workflow.compile()
    
    async def process_youtube_video(
        self, 
        youtube_url: str, 
        output_format: str = "linkedin",
        language: str = "en"
    ) -> Dict[str, Any]:
        """Process YouTube video through complete workflow"""
        
        logger.info(f"Starting workflow for: {youtube_url}")
        
        # Initialize state
        initial_state = AgentState(
            youtube_url=youtube_url,
            transcript="",
            title="",
            content="",
            metadata={
                'workflow_started': True,
                'input_format': output_format,
                'language': language
            },
            seo_analysis=None,
            output_format=output_format,
            error=""
        )
        
        try:
            # Run the workflow
            result = await self.workflow.ainvoke(initial_state)
            
            # Check for errors
            if result.get('error'):
                logger.error(f"Workflow failed: {result['error']}")
                raise HTTPException(status_code=400, detail=result['error'])
            
            # Prepare response
            response = {
                'transcript': result['transcript'],
                'title': result['title'],
                'content': result['content'],
                'metadata': result['metadata'],
                'seo_analysis': result.get('seo_analysis'),
                'workflow_success': True
            }
            
            logger.info("Workflow completed successfully")
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
    
    async def process_multiple_videos(
        self, 
        youtube_urls: list[str], 
        output_format: str = "linkedin"
    ) -> Dict[str, Any]:
        """Process multiple YouTube videos"""
        
        results = []
        errors = []
        success_count = 0
        
        for url in youtube_urls:
            try:
                result = await self.process_youtube_video(url, output_format)
                results.append(result)
                success_count += 1
                logger.info(f"Successfully processed: {url}")
            except Exception as e:
                error_msg = f"Failed to process {url}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        return {
            'results': results,
            'total_processed': len(youtube_urls),
            'success_count': success_count,
            'error_count': len(errors),
            'errors': errors
        }
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """Get information about the workflow"""
        return {
            'workflow_version': '2.0.0',
            'agents': [
                {
                    'name': 'TranscriptAgent',
                    'tools': [tool.name for tool in self.transcript_agent.tools],
                    'description': 'Extracts and cleans YouTube video transcripts'
                },
                {
                    'name': 'TitleAgent', 
                    'tools': [tool.name for tool in self.title_agent.tools],
                    'description': 'Generates engaging, platform-optimized titles'
                },
                {
                    'name': 'ContentAgent',
                    'tools': [tool.name for tool in self.content_agent.tools],
                    'description': 'Creates structured, SEO-optimized content'
                }
            ],
            'supported_platforms': ['linkedin', 'blog', 'article', 'twitter'],
            'workflow_steps': [
                'Extract YouTube transcript',
                'Analyze content for key themes', 
                'Generate optimized title',
                'Create structured content',
                'Apply platform formatting',
                'Perform SEO analysis'
            ]
        }
