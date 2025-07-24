from langchain_core.tools import BaseTool
from youtube_transcript_api import YouTubeTranscriptApi
import re
from utils.logger import setup_logger
from utils.validators import extract_youtube_video_id
from typing import Optional

logger = setup_logger(__name__)

class YouTubeTranscriptTool(BaseTool):
    """Tool for extracting YouTube video transcripts"""
    name: str = "youtube_transcript_extractor"
    description: str = """Extract transcript from YouTube video URL.
    Input: YouTube video URL. Output: Clean transcript text."""

    def _run(self, youtube_url: str) -> str:
        try:
            video_id = extract_youtube_video_id(youtube_url)
            if not video_id:
                return "Error: Invalid YouTube URL"
            
            # Create API instance
            api = YouTubeTranscriptApi()
            
            # Try to get transcript with different methods
            try:
                # Method 1: Try to get transcript directly
                transcript_list = api.fetch(video_id)
            except Exception as e1:
                logger.warning(f"Direct transcript extraction failed: {e1}")
                try:
                    # Method 2: Try with language specification
                    transcript_list = api.fetch(video_id, languages=['en'])
                except Exception as e2:
                    logger.warning(f"English transcript extraction failed: {e2}")
                    try:
                        # Method 3: Try to get available transcripts first
                        available_transcripts = api.list(video_id)
                        transcript = available_transcripts.find_transcript(['en'])
                        transcript_list = transcript.fetch()
                    except Exception as e3:
                        logger.error(f"All transcript extraction methods failed: {e3}")
                        return f"Error: Could not extract transcript. Video may not have captions or they may be disabled."
            
            # Combine transcript parts - handle both dict and object formats
            full_transcript = ""
            for part in transcript_list:
                # Handle both dictionary and object formats
                if hasattr(part, 'text'):
                    # Object format (FetchedTranscriptSnippet)
                    full_transcript += part.text + " "
                elif isinstance(part, dict) and 'text' in part:
                    # Dictionary format
                    full_transcript += part['text'] + " "
                else:
                    # Try to convert to string
                    full_transcript += str(part) + " "
            
            # Clean up transcript
            cleaned_transcript = self._clean_transcript(full_transcript)
            
            if not cleaned_transcript.strip():
                return "Error: Extracted transcript is empty"
            
            logger.info(f"Successfully extracted transcript for video {video_id} ({len(cleaned_transcript)} chars)")
            return cleaned_transcript
            
        except Exception as e:
            error_msg = f"Error extracting transcript: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean and format transcript text"""
        if not transcript:
            return ""
            
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', transcript)
        
        # Remove common transcript artifacts
        cleaned = re.sub(r'\[.*?\]', '', cleaned)  # Remove bracketed text
        cleaned = re.sub(r'\(.*?\)', '', cleaned)  # Remove parenthetical text
        
        # Basic punctuation cleanup
        cleaned = cleaned.strip()
        
        return cleaned

class YouTubeMetadataTool(BaseTool):
    """Tool for extracting YouTube video metadata"""
    name: str = "youtube_metadata_extractor"
    description: str = """Extract metadata from YouTube video URL.
    Input: YouTube video URL. Output: Video metadata information."""

    def _run(self, youtube_url: str) -> str:
        try:
            video_id = extract_youtube_video_id(youtube_url)
            if not video_id:
                return "Error: Invalid YouTube URL"
            
            # For now, return basic metadata structure
            # In a full implementation, you would use youtube-dl or similar
            metadata = {
                "video_id": video_id,
                "url": youtube_url,
                "platform": "youtube",
                "extraction_method": "youtube_transcript_api"
            }
            
            logger.info(f"Successfully extracted metadata for video {video_id}")
            return str(metadata)
            
        except Exception as e:
            error_msg = f"Error extracting metadata: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}" 