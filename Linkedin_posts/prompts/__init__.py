"""
Prompts package for YouTube Agent Workflow.
Contains organized LLM prompts for each agent and use case.
"""

from .transcript_prompts import (
    TRANSCRIPT_ANALYSIS_PROMPT,
    TRANSCRIPT_CLEANUP_PROMPT
)
from .title_prompts import (
    TITLE_GENERATION_PROMPT,
    TITLE_OPTIMIZATION_PROMPT
)
from .content_prompts import (
    CONTENT_GENERATION_PROMPT,
    CONTENT_ENHANCEMENT_PROMPT
)

__all__ = [
    "TRANSCRIPT_ANALYSIS_PROMPT",
    "TRANSCRIPT_CLEANUP_PROMPT",
    "TITLE_GENERATION_PROMPT", 
    "TITLE_OPTIMIZATION_PROMPT",
    "CONTENT_GENERATION_PROMPT",
    "CONTENT_ENHANCEMENT_PROMPT"
]