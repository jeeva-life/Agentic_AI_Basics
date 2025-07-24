import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

# Import route modules with fixed paths
from api.routes import workflow, health

# Import configuration
try:
    from src.config.settings import settings
    from utils.logger import setup_logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required packages are installed and the project structure is correct")
    sys.exit(1)

# Setup logging
logger = setup_logger(__name__, "INFO", "app.log")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting YouTube Multi-Agent Workflow API")
    logger.info(f"Version: 2.0.0")
    logger.info("LinkedIn Content Generation Ready!")
    yield
    logger.info("Shutting down YouTube Multi-Agent Workflow API")

# Create FastAPI application
app = FastAPI(
    title="YouTube Multi-Agent Content Workflow",
    description="""
    ## YouTube Multi-Agent Content Workflow
    
    Transform YouTube videos into engaging LinkedIn content with our AI-powered workflow:
    
    ### 🤖 Three Specialized Agents:
    - **Transcript Agent**: Extracts and cleans YouTube video transcripts
    - **Title Agent**: Generates engaging, clickable titles with trend analysis
    - **Content Agent**: Creates structured, platform-optimized content
    
    ### 🎯 LinkedIn Optimization:
    - Professional engagement hooks
    - Optimal hashtag placement
    - Mobile-friendly formatting
    - Call-to-action generation
    - Character count optimization
    
    ### 🚀 Getting Started:
    1. Get your OpenAI API key and add it to .env file
    2. Use `/workflow/linkedin-post` for LinkedIn-optimized posts
    3. Use `/workflow/process-video` for general content
    4. Check `/health` for system status
    """,
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(workflow.router)

@app.get("/")
async def root():
    """Root endpoint with LinkedIn-focused information"""
    return {
        "message": "YouTube Multi-Agent Content Workflow API",
        "version": "2.0.0",
        "status": "running",
        "linkedin_focus": {
            "description": "Specialized AI workflow for creating engaging LinkedIn content from YouTube videos",
            "key_features": [
                "YouTube transcript extraction",
                "AI-powered title generation",
                "LinkedIn-optimized content creation",
                "Engagement score calculation",
                "Professional hashtag suggestions"
            ]
        },
        "endpoints": {
            "documentation": "/docs",
            "health_check": "/health",
            "linkedin_post": "/workflow/linkedin-post",
            "linkedin_bulk": "/workflow/linkedin-bulk",
            "linkedin_preview": "/workflow/linkedin-preview",
            "general_processing": "/workflow/process-video"
        },
        "quick_start": {
            "step_1": "Set OPENAI_API_KEY in your .env file",
            "step_2": "POST YouTube URL to /workflow/linkedin-post",
            "step_3": "Get optimized LinkedIn content with engagement features",
            "example": {
                "url": "https://www.youtube.com/watch?v=VIDEO_ID",
                "output_format": "linkedin"
            }
        }
    }

@app.get("/linkedin-features")
async def linkedin_features():
    """LinkedIn-specific features and capabilities"""
    return {
        "linkedin_optimization": {
            "content_structure": [
                "Engaging hook in first line",
                "Short paragraphs for mobile readability", 
                "Bullet points for key insights",
                "Call-to-action for engagement",
                "Relevant hashtags for discoverability"
            ],
            "best_practices": [
                "3000 character limit optimization",
                "Emoji usage for visual appeal",
                "Question-based engagement",
                "Industry-relevant hashtags",
                "Professional tone with personality"
            ],
            "ai_features": [
                "Automatic engagement score calculation",
                "Hashtag optimization",
                "Mobile-friendly formatting",
                "Professional tone adaptation",
                "Call-to-action generation"
            ]
        },
        "supported_endpoints": {
            "single_post": "/workflow/linkedin-post",
            "bulk_posts": "/workflow/linkedin-bulk",
            "preview": "/workflow/linkedin-preview",
            "features": "/linkedin-features"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )