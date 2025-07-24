from langchain_core.tools import BaseTool
from utils.logger import setup_logger
import json
import re
from typing import Dict, List

logger = setup_logger(__name__)

class ContentStructureTool(BaseTool):
    """Tool for analyzing and structuring content for different platforms"""
    name: str = "content_structure_analyzer"
    description: str = """Analyze content structure and provide formatting recommendations.
    Input: content|||platform. Output: Structure analysis and recommendations."""

    def _run(self, content_platform_input: str) -> str:
        try:
            # Parse input
            parts = content_platform_input.split("|||")
            if len(parts) != 2:
                return "Error: Input format should be 'content|||platform'"
            
            content, platform = parts[0], parts[1]
            
            # Analyze content structure
            structure_analysis = self._analyze_content_structure(content, platform)
            
            logger.info(f"Completed content structure analysis for {platform}")
            return f"Structure Analysis: {json.dumps(structure_analysis, indent=2)}"
            
        except Exception as e:
            error_msg = f"Error in content structure analysis: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _analyze_content_structure(self, content: str, platform: str) -> Dict:
        """Analyze content structure for specific platform"""
        
        # Basic metrics
        words = content.split()
        sentences = [s for s in content.split('.') if s.strip()]
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        paragraph_count = len(paragraphs)
        
        # Platform-specific analysis
        platform_analysis = self._get_platform_specific_analysis(content, platform)
        
        # Structure recommendations
        recommendations = self._generate_structure_recommendations(
            word_count, sentence_count, paragraph_count, platform
        )
        
        return {
            "basic_metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "avg_sentence_length": round(word_count / max(sentence_count, 1), 1),
                "avg_paragraph_length": round(sentence_count / max(paragraph_count, 1), 1)
            },
            "platform_analysis": platform_analysis,
            "recommendations": recommendations,
            "structure_score": self._calculate_structure_score(content, platform)
        }
    
    def _get_platform_specific_analysis(self, content: str, platform: str) -> Dict:
        """Get platform-specific content analysis"""
        
        if platform == "linkedin":
            return {
                "hashtag_count": len(re.findall(r'#\w+', content)),
                "emoji_count": len(re.findall(r'[^\w\s]', content)),
                "call_to_action": self._detect_call_to_action(content),
                "engagement_hooks": self._detect_engagement_hooks(content),
                "professional_tone": self._assess_professional_tone(content)
            }
        elif platform == "twitter":
            return {
                "character_count": len(content),
                "thread_potential": self._assess_thread_potential(content),
                "hashtag_usage": len(re.findall(r'#\w+', content)),
                "mention_count": len(re.findall(r'@\w+', content))
            }
        elif platform == "blog":
            return {
                "heading_structure": self._analyze_heading_structure(content),
                "seo_elements": self._analyze_seo_elements(content),
                "readability": self._assess_readability(content)
            }
        else:
            return {
                "general_analysis": "Standard content analysis applied"
            }
    
    def _detect_call_to_action(self, content: str) -> List[str]:
        """Detect call-to-action phrases in content"""
        cta_phrases = [
            "click here", "learn more", "find out", "discover", "get started",
            "sign up", "join us", "follow", "share", "comment", "like"
        ]
        
        detected_ctas = []
        content_lower = content.lower()
        for phrase in cta_phrases:
            if phrase in content_lower:
                detected_ctas.append(phrase)
        
        return detected_ctas
    
    def _detect_engagement_hooks(self, content: str) -> List[str]:
        """Detect engagement hooks in content"""
        hooks = []
        content_lower = content.lower()
        
        # Question hooks
        if '?' in content:
            hooks.append("question_asked")
        
        # Number hooks
        if re.search(r'\d+', content):
            hooks.append("numbered_list")
        
        # Story hooks
        story_indicators = ["story", "experience", "journey", "discovered", "learned"]
        if any(indicator in content_lower for indicator in story_indicators):
            hooks.append("story_element")
        
        return hooks
    
    def _assess_professional_tone(self, content: str) -> str:
        """Assess the professional tone of content"""
        professional_words = ["industry", "business", "professional", "expert", "strategy"]
        casual_words = ["awesome", "cool", "amazing", "incredible", "mind-blowing"]
        
        prof_count = sum(1 for word in professional_words if word in content.lower())
        casual_count = sum(1 for word in casual_words if word in content.lower())
        
        if prof_count > casual_count:
            return "professional"
        elif casual_count > prof_count:
            return "casual"
        else:
            return "balanced"
    
    def _assess_thread_potential(self, content: str) -> bool:
        """Assess if content has potential for Twitter thread"""
        return len(content) > 200 or content.count('\n') > 3
    
    def _analyze_heading_structure(self, content: str) -> Dict:
        """Analyze heading structure for blog content"""
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        return {
            "heading_count": len(headings),
            "heading_levels": [len(h.split()[0]) for h in headings if h.startswith('#')]
        }
    
    def _analyze_seo_elements(self, content: str) -> Dict:
        """Analyze SEO elements in content"""
        return {
            "keyword_density": "analyzed",
            "meta_description_potential": len(content) > 150,
            "internal_linking_opportunities": content.count('http') > 0
        }
    
    def _assess_readability(self, content: str) -> str:
        """Assess content readability"""
        avg_sentence_length = len(content.split()) / max(content.count('.'), 1)
        if avg_sentence_length < 15:
            return "easy"
        elif avg_sentence_length < 25:
            return "moderate"
        else:
            return "complex"
    
    def _generate_structure_recommendations(self, word_count: int, sentence_count: int, 
                                          paragraph_count: int, platform: str) -> List[str]:
        """Generate structure recommendations based on metrics"""
        recommendations = []
        
        if platform == "linkedin":
            if word_count > 3000:
                recommendations.append("Consider breaking into multiple posts")
            if paragraph_count < 3:
                recommendations.append("Add more paragraph breaks for readability")
            if sentence_count < 10:
                recommendations.append("Consider adding more detail and examples")
        
        elif platform == "twitter":
            if word_count > 280:
                recommendations.append("Content exceeds Twitter character limit")
            if paragraph_count > 1:
                recommendations.append("Consider thread format for longer content")
        
        elif platform == "blog":
            if word_count < 300:
                recommendations.append("Consider expanding content for better SEO")
            if paragraph_count < 5:
                recommendations.append("Add more sections and subsections")
        
        return recommendations
    
    def _calculate_structure_score(self, content: str, platform: str) -> int:
        """Calculate overall structure score (0-100)"""
        base_score = 70
        
        # Adjust based on platform-specific criteria
        if platform == "linkedin":
            if len(content) < 1000:
                base_score += 10
            if '#' in content:
                base_score += 5
            if '?' in content:
                base_score += 5
        
        elif platform == "twitter":
            if len(content) <= 280:
                base_score += 20
            if '#' in content:
                base_score += 5
        
        elif platform == "blog":
            if len(content) > 500:
                base_score += 15
            if content.count('\n') > 10:
                base_score += 10
        
        return min(100, base_score)

class SEOAnalysisTool(BaseTool):
    """Tool for performing SEO analysis on content"""
    name: str = "seo_analyzer"
    description: str = """Perform SEO analysis on content and provide optimization recommendations.
    Input: Content text. Output: SEO analysis and recommendations."""

    def _run(self, content: str) -> str:
        try:
            # Import SEO tools from existing seo_tools.py
            from .seo_tools import AdvancedSEOTool
            
            seo_tool = AdvancedSEOTool()
            analysis = seo_tool._run(content)
            
            logger.info("Completed SEO analysis")
            return analysis
            
        except Exception as e:
            error_msg = f"Error in SEO analysis: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}" 