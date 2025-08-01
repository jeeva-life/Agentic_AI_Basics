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
            
            # Log raw transcript details for debugging
            logger.info(f"Raw transcript extracted: {len(raw_transcript)} characters")
            logger.info(f"Raw transcript word count: {len(raw_transcript.split())}")
            logger.info(f"Raw transcript preview (first 500 chars): {raw_transcript[:500]}...")
            logger.info(f"Raw transcript preview (last 500 chars): {raw_transcript[-500:]}...")
            
            # Check if transcript seems too short for a 15-minute video
            word_count = len(raw_transcript.split())
            expected_min_words = 15 * 150  # 15 minutes * 150 words/minute minimum
            if word_count < expected_min_words:
                logger.warning(f"Transcript seems short: {word_count} words (expected ~{expected_min_words} for 15-minute video)")
            
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
            # Use the FULL transcript for cleaning - handle 20+ minute videos
            transcript_length = len(raw_transcript)
            max_transcript = min(transcript_length, 50000)  # Handle full 20+ minute videos
            
            logger.info(f"Cleaning transcript: {max_transcript}/{transcript_length} characters")
            logger.info(f"Transcript preview (first 200 chars): {raw_transcript[:200]}...")
            logger.info(f"Transcript preview (last 200 chars): {raw_transcript[-200:]}...")
            
            # For very long transcripts, we need to be more careful with LLM processing
            # Let's use a simpler cleaning approach for long content
            if transcript_length > 15000:
                logger.info("Using simple cleaning for long transcript to preserve full content")
                cleaned = self._simple_clean_transcript(raw_transcript[:max_transcript])
            else:
                logger.info("Using LLM cleaning for shorter transcript")
                cleanup_chain = TRANSCRIPT_CLEANUP_PROMPT | self.llm | StrOutputParser()
                cleaned = await cleanup_chain.ainvoke({
                    "transcript": raw_transcript[:max_transcript]
                })
            
            return cleaned.strip()
            
        except Exception as e:
            logger.warning(f"Transcript cleaning failed: {e}. Using raw transcript.")
            return raw_transcript
    
    def _simple_clean_transcript(self, transcript: str) -> str:
        """Simple cleaning for long transcripts to preserve full content"""
        if not transcript:
            return transcript
        
        import re
        
        # Remove speaker labels and timestamps
        cleaned = re.sub(r'\[.*?\]', '', transcript)  # Remove bracketed text
        cleaned = re.sub(r'\(.*?\)', '', cleaned)     # Remove parenthetical text
        
        # Remove common transcript artifacts
        cleaned = re.sub(r'\b(um|uh|like|you know)\b', '', cleaned, flags=re.IGNORECASE)
        
        # Fix spacing and punctuation
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single space
        cleaned = re.sub(r'\.\s*\.', '.', cleaned)  # Multiple dots to single dot
        
        # Clean up sentence endings
        cleaned = re.sub(r'\s+\.', '.', cleaned)
        cleaned = re.sub(r'\s+,', ',', cleaned)
        
        return cleaned.strip()