from fastapi import APIRouter
from datetime import datetime
from src.models.responses import HealthResponse, ToolsResponse
from src.workflows.youtube_workflow import YouTubeWorkflow
from src.config.settings import settings

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint"""
    
    # Initialize workflow to check tools
    workflow = YouTubeWorkflow()
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.APP_VERSION,
        agents=["TranscriptAgent", "TitleAgent", "ContentAgent"],
        tools_loaded={
            "transcript_tools": len(workflow.transcript_agent.tools),
            "title_tools": len(workflow.title_agent.tools),
            "content_tools": len(workflow.content_agent.tools)
        }
    )

@router.get("/tools", response_model=ToolsResponse)
async def get_available_tools():
    """Get detailed information about all available tools"""
    
    workflow = YouTubeWorkflow()
    
    return ToolsResponse(
        transcript_agent_tools=[
            {
                "name": tool.name,
                "description": tool.description
            } for tool in workflow.transcript_agent.tools
        ],
        title_agent_tools=[
            {
                "name": tool.name, 
                "description": tool.description
            } for tool in workflow.title_agent.tools
        ],
        content_agent_tools=[
            {
                "name": tool.name,
                "description": tool.description  
            } for tool in workflow.content_agent.tools
        ]
    )
