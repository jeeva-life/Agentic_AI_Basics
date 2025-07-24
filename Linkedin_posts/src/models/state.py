from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    """State definition for the YouTube workflow agents"""
    youtube_url: str
    transcript: str
    title: str
    content: str
    metadata: Dict[str, Any]
    seo_analysis: Optional[Dict[str, Any]]
    output_format: str
    error: str 