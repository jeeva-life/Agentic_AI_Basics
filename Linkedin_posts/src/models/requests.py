from pydantic import BaseModel, HttpUrl, validator
from typing import List

class YouTubeRequest(BaseModel):
    """Request model for single YouTube video processing"""
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
    """Request model for bulk YouTube video processing"""
    urls: List[HttpUrl]
    language: str = "en"
    output_format: str = "linkedin"
    
    @validator('urls')
    def validate_urls_count(cls, v):
        if len(v) > 10:
            raise ValueError("Maximum 10 URLs allowed for bulk processing")
        return v 