from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class WorkflowResponse(BaseModel):
    """Response model for single workflow processing"""
    transcript: str
    title: str
    content: str
    metadata: Dict[str, Any]
    seo_analysis: Optional[Dict[str, Any]] = None

class BulkWorkflowResponse(BaseModel):
    """Response model for bulk workflow processing"""
    results: List[WorkflowResponse]
    total_processed: int
    success_count: int
    error_count: int
    errors: List[str] = []

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    version: str
    timestamp: str
    uptime: float

class ToolsResponse(BaseModel):
    """Response model for tools information endpoint"""
    available_tools: List[str]
    tool_descriptions: Dict[str, str] 