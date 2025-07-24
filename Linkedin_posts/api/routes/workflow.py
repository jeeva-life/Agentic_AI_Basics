import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, validator
import logging

# Fixed imports
try:
    from src.workflows.youtube_workflow import YouTubeWorkflow
    from utils.logger import setup_logger
except ImportError:
    # Fallback for development
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, project_root)
    from src.workflows.youtube_workflow import YouTubeWorkflow
    from utils.logger import setup_logger

# Define request/response models locally
class YouTubeRequest(BaseModel):
    url: HttpUrl
    language: str = "en"
    output_format: str = "linkedin"
    
    @validator('output_format')
    def validate_output_format(cls, v):
        allowed_formats = ["linkedin", "blog", "article", "twitter"]
        if v not in allowed_formats:
            raise ValueError(f"Output format must be one of: {allowed_formats}")
        return v

class BulkYouTubeRequest(BaseModel):
    urls: List[HttpUrl]
    language: str = "en"
    output_format: str = "linkedin"
    
    @validator('urls')
    def validate_urls_count(cls, v):
        if len(v) > 10:
            raise ValueError("Maximum 10 URLs allowed for bulk processing")
        return v

class WorkflowResponse(BaseModel):
    transcript: str
    title: str
    content: str
    metadata: dict
    seo_analysis: Optional[dict] = None

class BulkWorkflowResponse(BaseModel):
    results: List[WorkflowResponse]
    total_processed: int
    success_count: int
    error_count: int
    errors: List[str] = []

logger = setup_logger(__name__)
router = APIRouter(prefix="/workflow", tags=["workflow"])

# Initialize workflow
workflow = YouTubeWorkflow()

@router.post("/process-video", response_model=WorkflowResponse)
async def process_single_video(request: YouTubeRequest):
    """Process a single YouTube video through the multi-agent workflow"""
    try:
        logger.info(f"Processing single video: {request.url}")
        
        result = await workflow.process_youtube_video(
            youtube_url=str(request.url),
            output_format=request.output_format,
            language=request.language
        )
        
        return WorkflowResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/process-bulk", response_model=BulkWorkflowResponse)  
async def process_bulk_videos(request: BulkYouTubeRequest, background_tasks: BackgroundTasks):
    """Process multiple YouTube videos in bulk"""
    try:
        logger.info(f"Processing bulk videos: {len(request.urls)} URLs")
        
        urls = [str(url) for url in request.urls]
        result = await workflow.process_multiple_videos(
            youtube_urls=urls,
            output_format=request.output_format
        )
        
        return BulkWorkflowResponse(**result)
        
    except Exception as e:
        logger.error(f"Bulk processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk processing failed: {str(e)}")

# LinkedIn-specific endpoints
@router.post("/linkedin-post", response_model=WorkflowResponse)
async def generate_linkedin_post(request: YouTubeRequest):
    """
    Generate LinkedIn post from YouTube video
    Optimized specifically for LinkedIn format with engagement features
    """
    try:
        logger.info(f"Generating LinkedIn post from: {request.url}")
        
        # Force LinkedIn format
        result = await workflow.process_youtube_video(
            youtube_url=str(request.url),
            output_format="linkedin",
            language=request.language
        )
        
        # Add LinkedIn-specific metadata
        result['metadata']['linkedin_optimized'] = True
        result['metadata']['estimated_engagement_score'] = _calculate_engagement_score(result['content'])
        result['metadata']['character_count'] = len(result['content'])
        result['metadata']['hashtag_count'] = result['content'].count('#')
        
        return WorkflowResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"LinkedIn post generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LinkedIn post generation failed: {str(e)}")

@router.post("/linkedin-bulk", response_model=BulkWorkflowResponse)
async def generate_bulk_linkedin_posts(request: BulkYouTubeRequest):
    """Generate LinkedIn posts from multiple YouTube videos"""
    try:
        logger.info(f"Generating LinkedIn posts for {len(request.urls)} videos")
        
        urls = [str(url) for url in request.urls]
        result = await workflow.process_multiple_videos(
            youtube_urls=urls,
            output_format="linkedin"
        )
        
        # Add LinkedIn-specific metadata to each result
        for video_result in result['results']:
            video_result['metadata']['linkedin_optimized'] = True
            video_result['metadata']['estimated_engagement_score'] = _calculate_engagement_score(video_result['content'])
            video_result['metadata']['character_count'] = len(video_result['content'])
        
        return BulkWorkflowResponse(**result)
        
    except Exception as e:
        logger.error(f"Bulk LinkedIn generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk LinkedIn generation failed: {str(e)}")

@router.get("/linkedin-preview")
async def preview_linkedin_format(
    url: str = Query(..., description="YouTube video URL"),
    include_hashtags: bool = Query(True, description="Include hashtags in preview"),
    include_emojis: bool = Query(True, description="Include emojis in preview")
):
    """Preview how a YouTube video would be formatted for LinkedIn"""
    try:
        result = await workflow.process_youtube_video(
            youtube_url=url,
            output_format="linkedin"
        )
        
        content = result['content']
        
        # Apply preview filters
        if not include_hashtags:
            content = _remove_hashtags(content)
        if not include_emojis:
            content = _remove_emojis(content)
        
        preview_stats = {
            "character_count": len(content),
            "word_count": len(content.split()),
            "line_count": len(content.split('\n')),
            "hashtag_count": content.count('#'),
            "emoji_count": _count_emojis(content),
            "estimated_read_time": f"{len(content.split()) // 200 + 1} min",
            "linkedin_optimal": len(content) <= 3000,
            "mobile_friendly": _check_mobile_friendly(content)
        }
        
        return {
            "preview_content": content,
            "original_title": result['title'],
            "stats": preview_stats,
            "optimization_tips": _get_linkedin_tips(content, preview_stats)
        }
        
    except Exception as e:
        logger.error(f"LinkedIn preview failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

@router.get("/workflow-info")
async def get_workflow_information():
    """Get detailed information about the workflow and its capabilities"""
    return workflow.get_workflow_info()

@router.get("/supported-platforms")
async def get_supported_platforms():
    """Get list of supported output platforms"""
    return {
        "platforms": [
            {
                "name": "linkedin",
                "description": "LinkedIn posts with hashtags and engagement hooks",
                "max_length": "3000 characters (recommended)",
                "features": [
                    "Engagement-optimized hooks",
                    "Professional hashtags",
                    "Call-to-action phrases",
                    "Mobile-friendly formatting",
                    "Industry-relevant content"
                ],
                "example_endpoint": "/workflow/linkedin-post"
            },
            {
                "name": "blog", 
                "description": "Blog articles with proper headings and structure",
                "max_length": "No limit"
            },
            {
                "name": "twitter",
                "description": "Twitter threads with character limits",
                "max_length": "280 characters per tweet"
            },
            {
                "name": "article",
                "description": "General articles with SEO optimization",
                "max_length": "No limit"
            }
        ]
    }

# Helper functions for LinkedIn optimization
def _calculate_engagement_score(content: str) -> int:
    """Calculate estimated engagement score for LinkedIn content"""
    score = 50
    
    if content.startswith('🚀') or content.startswith('💡'):
        score += 10
    if '?' in content:
        score += 15
    if content.count('#') >= 3:
        score += 10
    if len(content.split('\n\n')) >= 3:
        score += 5
    if any(word in content.lower() for word in ['insights', 'tips', 'secrets', 'guide']):
        score += 10
    
    if len(content) > 3000:
        score -= 20
    if content.count('#') > 10:
        score -= 15
    if content.count('!') > 5:
        score -= 10
    
    return max(0, min(100, score))

def _remove_hashtags(content: str) -> str:
    import re
    return re.sub(r'#\w+', '', content)

def _remove_emojis(content: str) -> str:
    import re
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', content)

def _count_emojis(content: str) -> int:
    import re
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return len(emoji_pattern.findall(content))

def _check_mobile_friendly(content: str) -> bool:
    lines = content.split('\n')
    avg_line_length = sum(len(line) for line in lines) / max(len(lines), 1)
    return avg_line_length < 60 and len(lines) > 3

def _get_linkedin_tips(content: str, stats: dict) -> list:
    tips = []
    
    if stats['character_count'] > 3000:
        tips.append("Consider shortening content for better LinkedIn engagement")
    if stats['hashtag_count'] < 3:
        tips.append("Add more relevant hashtags (3-5 recommended)")
    if stats['hashtag_count'] > 10:
        tips.append("Reduce hashtag count for better readability")
    if not content.endswith('?'):
        tips.append("End with a question to encourage engagement")
    if '🚀' not in content and '💡' not in content:
        tips.append("Consider adding engaging emojis at the start")
    if stats['line_count'] < 5:
        tips.append("Break content into shorter paragraphs for mobile readability")
    
    return tips