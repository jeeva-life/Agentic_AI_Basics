from datetime import datetime
from typing import List
from langchain_core.tools import BaseTool

from .base_agents import BaseAgent
from src.models.state import AgentState
from src.tools.youtube_tools import YouTubeTranscriptTool, YouTubeMetadataTool
from prompts.transcript_prompts import TRANSCRIPT_CLEANUP_PROMPT
from langchain_core.output_parsers import StrOutputParser
from utils.exceptions import TranscriptExtractionError
from utils.helpers import create_metadata
from utils.validators import extract_youtube_video_id
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TranscriptAgent(BaseAgent):
    """Agent responsible for extracting and processing YouTube transcripts"""
    
    def __init__(self):
        tools = [
            YouTubeTranscriptTool(),
            YouTubeMetadataTool()
        ]
        super().__init__(tools)
    
    async def process(self, state: AgentState) -> AgentState:
        """Extract and clean YouTube transcript"""
        try:
            logger.info(f"TranscriptAgent processing: {state['youtube_url']}")
            
            # Extract video ID for metadata
            video_id = extract_youtube_video_id(state['youtube_url'])
            
            # Use YouTube transcript tool
            transcript_tool = self.tools[0]  # YouTubeTranscriptTool
            metadata_tool = self.tools[1]    # YouTubeMetadataTool
            
            # Extract transcript
            raw_transcript = transcript_tool._run(state['youtube_url'])
            if raw_transcript.startswith("Error"):
                raise TranscriptExtractionError(raw_transcript)
            
            # Clean transcript using LLM
            cleaned_transcript = await self._clean_transcript(raw_transcript)
            
            # Extract metadata
            metadata_raw = metadata_tool._run(state['youtube_url'])
            
            # Update state
            state['transcript'] = cleaned_transcript
            state['metadata'] = create_metadata(
                video_id=video_id,
                transcript_length=len(cleaned_transcript),
                raw_transcript_length=len(raw_transcript),
                video_metadata=metadata_raw
            )
            
            # Add agent metadata
            self._add_agent_metadata(
                state, 
                processed_at=datetime.now().isoformat(),
                transcript_extracted=True,
                cleaning_applied=True
            )
            
            logger.info(f"TranscriptAgent completed successfully ({len(cleaned_transcript)} chars)")
            
        except Exception as e:
            return self._handle_error(state, e)
        
        return state
    
    async def _clean_transcript(self, raw_transcript: str) -> str:
        """Clean transcript using LLM"""
        try:
            # Use the full transcript for cleaning - handle 20+ minute videos
            transcript_length = len(raw_transcript)
            max_transcript = min(transcript_length, 20000)  # Handle full transcripts
            
            logger.info(f"Cleaning transcript: {max_transcript}/{transcript_length} characters")
            
            cleanup_chain = TRANSCRIPT_CLEANUP_PROMPT | self.llm | StrOutputParser()
            
            cleaned = await cleanup_chain.ainvoke({
                "transcript": raw_transcript[:max_transcript]
            })
            
            return cleaned.strip()
            
        except Exception as e:
            logger.warning(f"Transcript cleaning failed: {e}. Using raw transcript.")
            return raw_transcript