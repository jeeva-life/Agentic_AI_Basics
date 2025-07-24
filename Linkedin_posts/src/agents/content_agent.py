from datetime import datetime
from .base_agents import BaseAgent
from src.models.state import AgentState
from src.tools.content_tools import ContentStructureTool, SEOAnalysisTool
from prompts.content_prompts import CONTENT_GENERATION_PROMPT, CONTENT_ENHANCEMENT_PROMPT
from langchain_core.output_parsers import StrOutputParser
from utils.exceptions import ContentGenerationError
from utils.logger import setup_logger
import json

logger = setup_logger(__name__)

class ContentAgent(BaseAgent):
    """Expert AI/Agents technical analyst responsible for creating comprehensive, technically accurate content summaries"""
    
    def __init__(self):
        tools = [
            ContentStructureTool(),
            SEOAnalysisTool()
        ]
        super().__init__(tools)
    
    async def process(self, state: AgentState) -> AgentState:
        """Generate structured content from transcript and title"""
        try:
            if state.get('error'):
                return state
            
            logger.info("ContentAgent generating structured content")
            
            # Use content tools
            structurer_tool = self.tools[0]  # ContentStructureTool
            seo_tool = self.tools[1]         # SEOAnalysisTool
            
            output_format = state.get('output_format', 'linkedin')
            
            # Generate initial content with LLM
            raw_content = await self._generate_base_content(
                state['transcript'],
                state['title'],
                output_format
            )
            
            # Get structure analysis
            structure_input = f"{raw_content}|||{output_format}"
            structure_analysis = structurer_tool._run(structure_input)
            
            # Enhance content based on structure analysis
            enhanced_content = await self._enhance_content(
                raw_content,
                output_format,
                structure_analysis
            )
            
            # Perform SEO analysis
            seo_analysis_raw = seo_tool._run(enhanced_content)
            seo_analysis = self._parse_seo_analysis(seo_analysis_raw)
            
            # Apply final formatting based on platform
            final_content = self._apply_platform_formatting(enhanced_content, output_format, structure_analysis)
            
            # Update state
            state['content'] = final_content
            state['seo_analysis'] = seo_analysis
            
            # Add agent metadata
            self._add_agent_metadata(
                state,
                processed_at=datetime.now().isoformat(),
                content_generated=True,
                content_length=len(final_content),
                seo_score=seo_analysis.get('seo_score', 0),
                structure_analysis=structure_analysis[:200] + "..." if len(structure_analysis) > 200 else structure_analysis
            )
            
            logger.info(f"ContentAgent completed ({len(final_content)} characters)")
            
        except Exception as e:
            return self._handle_error(state, e)
        
        return state
    
    async def _generate_base_content(self, transcript: str, title: str, output_format: str) -> str:
        """Generate expert-level technical content using LLM with AI/Agents domain expertise"""
        content_chain = CONTENT_GENERATION_PROMPT | self.llm | StrOutputParser()
        
        # Use the FULL transcript for comprehensive analysis
        transcript_length = len(transcript)
        
        # For 20+ minute videos, we need to handle larger transcripts
        # Most LLMs can handle 15-20k tokens, so we can use much more content
        # Increase to handle the full 13,970 character transcript we confirmed
        max_transcript = min(transcript_length, 20000)  # Handle full 20+ minute videos
        
        logger.info(f"Generating comprehensive content from {max_transcript}/{transcript_length} characters of transcript")
        logger.info(f"Transcript preview (first 200 chars): {transcript[:200]}...")
        logger.info(f"Transcript preview (last 200 chars): {transcript[-200:]}...")
        
        # Create a detailed structure analysis first
        structure_analysis = await self._analyze_transcript_structure(transcript[:max_transcript])
        
        content = await content_chain.ainvoke({
            "title": title,
            "transcript": transcript[:max_transcript],  # Use full available transcript
            "structure_analysis": structure_analysis,
            "output_format": output_format
        })
        
        return content.strip()
    
    async def _analyze_transcript_structure(self, transcript: str) -> str:
        """Expert analysis of transcript structure to identify AI/Agents technical topics and sections"""
        try:
            # Create a comprehensive analysis of the transcript structure
            words = transcript.split()
            word_count = len(words)
            
            # Identify AI/Agents specific sections by looking for technical patterns
            sections = []
            technical_keywords = {
                "ai": "Artificial Intelligence concepts",
                "agent": "Agent-based systems",
                "model": "Model development and training",
                "algorithm": "Algorithmic approaches",
                "framework": "Technical frameworks",
                "benchmark": "Benchmarking and evaluation",
                "neural": "Neural network concepts",
                "machine learning": "Machine learning methods",
                "deep learning": "Deep learning techniques",
                "llm": "Large Language Models",
                "transformer": "Transformer architecture",
                "reinforcement": "Reinforcement learning",
                "supervised": "Supervised learning",
                "unsupervised": "Unsupervised learning",
                "implementation": "Technical implementation",
                "architecture": "System architecture",
                "optimization": "Performance optimization",
                "evaluation": "Model evaluation",
                "deployment": "System deployment",
                "scaling": "Scalability considerations"
            }
            
            transcript_lower = transcript.lower()
            for keyword, section_name in technical_keywords.items():
                if keyword in transcript_lower:
                    sections.append(section_name)
            
            # Remove duplicates while preserving order
            unique_sections = []
            for section in sections:
                if section not in unique_sections:
                    unique_sections.append(section)
            
            analysis = f"""
            Technical Transcript Analysis:
            - Total words: {word_count}
            - Main technical topics: {', '.join(unique_sections[:5]) if unique_sections else 'AI/Agents technical content'}
            - Content type: Technical AI/Agents discussion
            - Structure recommendation: Use technical headings for each major concept
            - Focus areas: {', '.join(unique_sections[:3]) if unique_sections else 'AI and Agents technical concepts'}
            - Technical depth: Comprehensive coverage of AI/Agents methodologies
            """
            
            return analysis
            
        except Exception as e:
            logger.warning(f"Transcript analysis failed: {e}")
            return "Comprehensive AI/Agents technical content analysis required"
    
    async def _enhance_content(self, content: str, platform: str, structure_analysis: str) -> str:
        """Enhance content based on structure analysis"""
        try:
            enhancement_chain = CONTENT_ENHANCEMENT_PROMPT | self.llm | StrOutputParser()
            
            enhanced = await enhancement_chain.ainvoke({
                "content": content,
                "platform": platform,
                "seo_analysis": structure_analysis
            })
            
            return enhanced.strip()
            
        except Exception as e:
            logger.warning(f"Content enhancement failed: {e}")
            return content
    
    def _parse_seo_analysis(self, seo_raw: str) -> dict:
        """Parse SEO analysis from tool output"""
        try:
            if "SEO Analysis:" in seo_raw:
                json_str = seo_raw.split("SEO Analysis:")[1].strip()
                return json.loads(json_str)
        except:
            pass
        
        return {"raw_analysis": seo_raw, "parsing_failed": True}
    
    def _apply_platform_formatting(self, content: str, platform: str, structure_analysis: str) -> str:
        """Apply platform-specific formatting to final content"""
        try:
            # Parse structure analysis to get formatting recommendations
            if platform.lower() == 'linkedin':
                return self._format_for_linkedin(content, structure_analysis)
            elif platform.lower() == 'blog':
                return self._format_for_blog(content)
            elif platform.lower() == 'twitter':
                return self._format_for_twitter(content, structure_analysis)
            else:
                return content
        except Exception as e:
            logger.warning(f"Platform formatting failed: {e}")
            return content
    
    def _format_for_linkedin(self, content: str, structure_info: str) -> str:
        """Format content specifically for LinkedIn"""
        lines = content.split('\n')
        formatted_lines = []
        
        # Ensure proper LinkedIn formatting
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Add line breaks for readability
            if i == 0:  # First line (hook)
                formatted_lines.append(line)
                formatted_lines.append("")  # Add space after hook
            elif line.startswith('#'):  # Headers
                formatted_lines.append("")
                formatted_lines.append(f"🔹 {line.replace('#', '').strip()}")
                formatted_lines.append("")
            else:
                formatted_lines.append(line)
        
        # Add call-to-action and hashtags if not present
        content_str = '\n'.join(formatted_lines)
        if "what do you think" not in content_str.lower() and "thoughts?" not in content_str.lower():
            formatted_lines.append("")
            formatted_lines.append("What are your thoughts on this? Share in the comments! 👇")
        
        if "#" not in content_str:
            formatted_lines.append("")
            formatted_lines.append("#AI #Technology #Innovation #ContentCreation #DigitalTransformation")
        
        return '\n'.join(formatted_lines)
    
    def _format_for_blog(self, content: str) -> str:
        """Format content as a blog post"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
                continue
            
            # Ensure proper heading format
            if line.startswith('#'):
                formatted_lines.append("")
                formatted_lines.append(line)
                formatted_lines.append("")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _format_for_twitter(self, content: str, structure_info: str) -> str:
        """Format content as Twitter thread"""
        try:
            # Try to extract tweet structure from structure_analysis
            if "twitter_thread" in structure_info:
                structure_data = json.loads(structure_info)
                if "tweets" in structure_data:
                    return '\n\n'.join(structure_data["tweets"])
        except:
            pass
        
        # Fallback: Split content into tweet-sized chunks
        words = content.split()
        tweets = []
        current_tweet = ""
        
        for word in words:
            if len(current_tweet + " " + word) <= 270:
                current_tweet += " " + word if current_tweet else word
            else:
                tweets.append(current_tweet.strip())
                current_tweet = word
        
        if current_tweet:
            tweets.append(current_tweet.strip())
        
        # Number the tweets
        numbered_tweets = [f"{i+1}/{len(tweets)} {tweet}" for i, tweet in enumerate(tweets)]
        return '\n\n'.join(numbered_tweets)