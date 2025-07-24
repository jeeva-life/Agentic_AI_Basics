from datetime import datetime
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool

from .base_agents import BaseAgent
from src.models.state import AgentState
from prompts.title_prompts import TITLE_GENERATION_PROMPT, TITLE_OPTIMIZATION_PROMPT
from langchain_core.output_parsers import StrOutputParser
from utils.exceptions import TitleGenerationError
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TitleAnalysisTool(BaseTool):
    """Tool for analyzing content and extracting key themes for titles"""
    name: str = "title_analyzer"
    description: str = """Analyze text content and extract key themes, keywords, and topics
    that would make engaging titles. Input: content text. Output: analysis summary"""

    def _run(self, content: str) -> str:
        try:
            words = content.lower().split()
            word_freq = {}
            
            # Filter out common stop words
            stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
            
            for word in words:
                word = word.strip('.,!?";:()[]{}')
                if len(word) > 3 and word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
            keywords = [kw[0] for kw in top_keywords]
            
            # Identify potential hooks and power words
            power_words = []
            for word in keywords:
                if any(trigger in word for trigger in ['secret', 'ultimate', 'proven', 'exclusive', 'breakthrough', 'revolutionary']):
                    power_words.append(word)
            
            analysis = {
                "primary_keywords": keywords[:3],
                "supporting_keywords": keywords[3:6],
                "power_words": power_words,
                "content_type": self._identify_content_type(content),
                "emotional_triggers": self._identify_emotional_triggers(content)
            }
            
            return f"Content Analysis: {analysis}"
            
        except Exception as e:
            return f"Error analyzing content: {str(e)}"
    
    def _identify_content_type(self, content: str) -> str:
        """Identify the type of content for better title targeting"""
        content_lower = content.lower()
        if any(word in content_lower for word in ['how', 'tutorial', 'guide', 'step']):
            return "how-to"
        elif any(word in content_lower for word in ['review', 'comparison', 'vs']):
            return "review"
        elif any(word in content_lower for word in ['tips', 'tricks', 'hacks']):
            return "tips"
        elif any(word in content_lower for word in ['news', 'update', 'announcement']):
            return "news"
        else:
            return "educational"
    
    def _identify_emotional_triggers(self, content: str) -> list:
        """Identify emotional triggers that could make titles more engaging"""
        triggers = []
        content_lower = content.lower()
        
        trigger_mapping = {
            'curiosity': ['secret', 'hidden', 'unknown', 'mystery', 'revealed'],
            'urgency': ['now', 'today', 'immediately', 'urgent', 'breaking'],
            'exclusivity': ['exclusive', 'only', 'limited', 'special', 'insider'],
            'benefit': ['benefit', 'advantage', 'profit', 'gain', 'improve'],
            'fear': ['mistake', 'wrong', 'avoid', 'danger', 'warning']
        }
        
        for trigger_type, words in trigger_mapping.items():
            if any(word in content_lower for word in words):
                triggers.append(trigger_type)
        
        return triggers

class TitleAgent(BaseAgent):
    """Agent responsible for generating engaging titles from transcript content"""
    
    def __init__(self):
        tools = [
            TitleAnalysisTool(),
            DuckDuckGoSearchRun(name="web_search")
        ]
        super().__init__(tools)
    
    async def process(self, state: AgentState) -> AgentState:
        """Generate optimized title from transcript"""
        try:
            if state.get('error'):
                return state
            
            logger.info("TitleAgent processing transcript for title generation")
            
            # Use title analysis tool
            title_analyzer = self.tools[0]  # TitleAnalysisTool
            search_tool = self.tools[1]     # DuckDuckGoSearchRun
            
            # Analyze content for themes and keywords
            content_analysis = title_analyzer._run(state['transcript'][:3000])
            
            # Search for trending topics to inform title
            trend_info = await self._get_trending_topics(search_tool)
            
            # Generate title using LLM with analysis
            title = await self._generate_optimized_title(
                state['transcript'], 
                content_analysis, 
                trend_info,
                state.get('output_format', 'linkedin')
            )
            
            # Optimize title for platform
            optimized_title = await self._optimize_title_for_platform(
                title, 
                state.get('output_format', 'linkedin')
            )
            
            # Update state
            state['title'] = optimized_title
            
            # Add agent metadata
            self._add_agent_metadata(
                state,
                processed_at=datetime.now().isoformat(),
                title_generated=True,
                content_analysis=content_analysis,
                optimization_applied=True
            )
            
            logger.info(f"TitleAgent completed: '{optimized_title}'")
            
        except Exception as e:
            return self._handle_error(state, e)
        
        return state
    
    async def _get_trending_topics(self, search_tool) -> str:
        """Get trending topics for title inspiration"""
        try:
            search_queries = [
                "trending content topics 2025",
                "viral content ideas",
                "popular social media trends"
            ]
            
            trend_results = []
            for query in search_queries[:1]:  # Limit to avoid rate limits
                try:
                    result = search_tool.run(query)
                    trend_results.append(result[:200])  # Limit result length
                except:
                    continue
            
            return " | ".join(trend_results) if trend_results else "No trend data available"
            
        except Exception as e:
            logger.warning(f"Could not fetch trending topics: {e}")
            return "Trend analysis unavailable"
    
    async def _generate_optimized_title(self, transcript: str, analysis: str, trends: str, format_type: str) -> str:
        """Generate title using LLM with analysis insights"""
        title_chain = TITLE_GENERATION_PROMPT | self.llm | StrOutputParser()
        
        title_result = await title_chain.ainvoke({
            "transcript": transcript[:3000],
            "content_analysis": analysis,
            "trend_info": trends,
            "output_format": format_type
        })
        
        # Extract the best title from the LLM response
        lines = title_result.split('\n')
        for line in lines:
            if line.strip() and not line.startswith(('1.', '2.', '3.', '•', '-')):
                return line.strip()
        
        return lines[0].strip() if lines else "Engaging Content from Video"
    
    async def _optimize_title_for_platform(self, title: str, platform: str) -> str:
        """Platform-specific title optimization"""
        try:
            optimization_chain = TITLE_OPTIMIZATION_PROMPT | self.llm | StrOutputParser()
            
            optimized = await optimization_chain.ainvoke({
                "title": title,
                "platform": platform
            })
            
            # Extract just the optimized title, not the explanation
            lines = optimized.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.lower().startswith(('explanation:', 'changes made:', 'optimized:')):
                    return line
            
            return title  # Fallback to original if parsing fails
            
        except Exception as e:
            logger.warning(f"Title optimization failed: {e}")
            return title