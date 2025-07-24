from langchain_core.tools import BaseTool
from utils.helpers import calculate_readability_score
from utils.logger import setup_logger
import json
import re
from typing import Dict, List

logger = setup_logger(__name__)

class AdvancedSEOTool(BaseTool):
    """Advanced SEO analysis tool with comprehensive metrics"""
    name: str = "advanced_seo_analyzer"
    description: str = """Perform comprehensive SEO analysis including keyword density,
    readability, meta tag suggestions, and content optimization recommendations.
    Input: Content text. Output: Detailed SEO analysis with actionable insights."""

    def _run(self, content: str) -> str:
        try:
            analysis = self._perform_comprehensive_seo_analysis(content)
            logger.info("Completed advanced SEO analysis")
            return f"Advanced SEO Analysis: {json.dumps(analysis, indent=2)}"
            
        except Exception as e:
            error_msg = f"Error in advanced SEO analysis: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _perform_comprehensive_seo_analysis(self, content: str) -> Dict:
        """Perform detailed SEO analysis"""
        
        # Basic metrics
        words = content.split()
        sentences = [s for s in content.split('.') if s.strip()]
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        paragraph_count = len(paragraphs)
        avg_sentence_length = word_count / max(sentence_count, 1)
        avg_paragraph_length = sentence_count / max(paragraph_count, 1)
        
        # Readability analysis
        readability_score = calculate_readability_score(content)
        
        # Keyword analysis
        keyword_analysis = self._analyze_keywords(content)
        
        # Content structure analysis
        structure_analysis = self._analyze_content_structure(content)
        
        # SEO recommendations
        recommendations = self._generate_seo_recommendations(
            word_count, avg_sentence_length, readability_score, 
            keyword_analysis, structure_analysis
        )
        
        # Calculate overall SEO score
        seo_score = self._calculate_seo_score(
            word_count, readability_score, keyword_analysis, structure_analysis
        )
        
        return {
            "basic_metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "avg_sentence_length": round(avg_sentence_length, 1),
                "avg_paragraph_length": round(avg_paragraph_length, 1)
            },
            "readability": {
                "score": round(readability_score, 1),
                "grade": self._get_readability_grade(readability_score)
            },
            "keywords": keyword_analysis,
            "structure": structure_analysis,
            "seo_score": round(seo_score, 1),
            "recommendations": recommendations,
            "meta_suggestions": self._generate_meta_suggestions(content, keyword_analysis)
        }
    
    def _analyze_keywords(self, content: str) -> Dict:
        """Analyze keyword usage and density"""
        words = content.lower().split()
        
        # Filter stop words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
            'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'this', 
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        # Count word frequencies
        word_freq = {}
        for word in words:
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 2 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        total_words = len([w for w in words if len(w) > 2])
        
        # Calculate keyword density
        keyword_density = {}
        for word, freq in word_freq.items():
            density = (freq / total_words) * 100
            keyword_density[word] = round(density, 2)
        
        # Get top keywords
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        
        return {
            "total_unique_words": len(word_freq),
            "top_keywords": [
                {"word": kw[0], "frequency": kw[1], "density": keyword_density[kw[0]]}
                for kw in top_keywords[:10]
            ],
            "keyword_diversity": len(word_freq) / max(total_words, 1),
            "over_optimized_keywords": [
                kw for kw, density in keyword_density.items() if density > 3.0
            ]
        }
    
    def _analyze_content_structure(self, content: str) -> Dict:
        """Analyze content structure for SEO"""
        
        # Count headings
        h1_count = len(re.findall(r'^#\s', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s', content, re.MULTILINE))
        h3_count = len(re.findall(r'^###\s', content, re.MULTILINE))
        
        # Check for lists
        bullet_lists = len(re.findall(r'^\s*[-*+]\s', content, re.MULTILINE))
        numbered_lists = len(re.findall(r'^\s*\d+\.\s', content, re.MULTILINE))
        
        # Check for links (basic pattern)
        internal_links = len(re.findall(r'\[.*?\]\((?!http)', content))
        external_links = len(re.findall(r'\[.*?\]\(https?://', content))
        
        return {
            "headings": {
                "h1_count": h1_count,
                "h2_count": h2_count, 
                "h3_count": h3_count,
                "total_headings": h1_count + h2_count + h3_count
            },
            "lists": {
                "bullet_lists": bullet_lists,
                "numbered_lists": numbered_lists,
                "total_lists": bullet_lists + numbered_lists
            },
            "links": {
                "internal_links": internal_links,
                "external_links": external_links,
                "total_links": internal_links + external_links
            },
            "has_good_structure": (h1_count + h2_count + h3_count) >= 2
        }
    
    def _generate_seo_recommendations(self, word_count: int, avg_sentence_length: float, 
                                    readability_score: float, keyword_analysis: Dict, 
                                    structure_analysis: Dict) -> List[str]:
        """Generate SEO improvement recommendations"""
        recommendations = []
        
        # Word count recommendations
        if word_count < 300:
            recommendations.append(f"Increase content length (current: {word_count} words, recommended: 300+ words)")
        elif word_count > 2000:
            recommendations.append("Consider breaking content into multiple sections or pages")
        
        # Readability recommendations
        if readability_score < 60:
            recommendations.append("Improve readability by using simpler words and shorter sentences")
        if avg_sentence_length > 20:
            recommendations.append(f"Reduce average sentence length (current: {avg_sentence_length:.1f} words)")
        
        # Keyword recommendations
        over_optimized = keyword_analysis.get('over_optimized_keywords', [])
        if over_optimized:
            recommendations.append(f"Reduce keyword density for: {', '.join(over_optimized[:3])}")
        
        if keyword_analysis.get('keyword_diversity', 0) < 0.3:
            recommendations.append("Use more diverse vocabulary to improve keyword variety")
        
        # Structure recommendations
        structure = structure_analysis
        if structure['headings']['total_headings'] == 0:
            recommendations.append("Add headings (H1, H2, H3) to improve content structure")
        
        if structure['lists']['total_lists'] == 0:
            recommendations.append("Add bullet points or numbered lists to improve scannability")
        
        if structure['links']['total_links'] == 0:
            recommendations.append("Add relevant internal and external links")
        
        return recommendations
    
    def _calculate_seo_score(self, word_count: int, readability_score: float, 
                           keyword_analysis: Dict, structure_analysis: Dict) -> float:
        """Calculate overall SEO score"""
        score = 0
        
        # Word count score (0-25 points)
        if 300 <= word_count <= 2000:
            score += 25
        elif word_count >= 300:
            score += 20
        else:
            score += 10
        
        # Readability score (0-25 points)
        score += min(25, readability_score * 0.25)
        
        # Keyword diversity score (0-25 points)
        diversity = keyword_analysis.get('keyword_diversity', 0)
        score += min(25, diversity * 50)
        
        # Structure score (0-25 points)
        structure_score = 0
        if structure_analysis['headings']['total_headings'] > 0:
            structure_score += 10
        if structure_analysis['lists']['total_lists'] > 0:
            structure_score += 8
        if structure_analysis['links']['total_links'] > 0:
            structure_score += 7
        score += structure_score
        
        return min(100, score)
    
    def _get_readability_grade(self, score: float) -> str:
        """Convert readability score to grade"""
        if score >= 90:
            return "Very Easy"
        elif score >= 80:
            return "Easy"
        elif score >= 70:
            return "Fairly Easy"
        elif score >= 60:
            return "Standard"
        elif score >= 50:
            return "Fairly Difficult"
        elif score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
    
    def _generate_meta_suggestions(self, content: str, keyword_analysis: Dict) -> Dict:
        """Generate meta tag suggestions"""
        top_keywords = [kw['word'] for kw in keyword_analysis.get('top_keywords', [])[:5]]
        
        # Extract first sentence for meta description base
        sentences = content.split('.')
        first_sentence = sentences[0].strip() if sentences else ""
        
        return {
            "title_suggestions": [
                f"Ultimate Guide to {top_keywords[0].title()}" if top_keywords else "Ultimate Guide",
                f"How to {top_keywords[0].title()}: Complete Tutorial" if top_keywords else "Complete Tutorial",
                f"{top_keywords[0].title()} Explained: Everything You Need to Know" if top_keywords else "Everything You Need to Know"
            ],
            "meta_description_base": first_sentence[:150] + "..." if len(first_sentence) > 150 else first_sentence,
            "suggested_keywords": top_keywords[:5],
            "focus_keyword": top_keywords[0] if top_keywords else "content"
        }

class KeywordExtractorTool(BaseTool):
    """Tool for extracting and analyzing keywords for SEO optimization"""
    name: str = "keyword_extractor"
    description: str = """Extract relevant keywords and phrases from content for SEO optimization.
    Analyzes text to find the most important terms and their variations.
    Input: Content text. Output: Structured keyword analysis."""

    def _run(self, content: str) -> str:
        try:
            keywords = self._extract_keywords(content)
            logger.info("Completed keyword extraction")
            return f"Keyword Analysis: {json.dumps(keywords, indent=2)}"
            
        except Exception as e:
            error_msg = f"Error extracting keywords: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def _extract_keywords(self, content: str) -> Dict:
        """Extract and categorize keywords"""
        
        # Basic keyword extraction
        words = content.lower().split()
        
        # Remove stop words and clean
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
            'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would'
        }
        
        clean_words = []
        for word in words:
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 2 and word not in stop_words:
                clean_words.append(word)
        
        # Count frequencies
        word_freq = {}
        for word in clean_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Extract phrases (2-3 words)
        phrases = self._extract_phrases(content, 2) + self._extract_phrases(content, 3)
        phrase_freq = {}
        for phrase in phrases:
            phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1
        
        # Categorize keywords
        single_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        phrase_keywords = sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Identify long-tail keywords
        long_tail = [phrase for phrase, freq in phrase_keywords if len(phrase.split()) >= 3 and freq >= 2]
        
        return {
            "single_keywords": [
                {"keyword": kw[0], "frequency": kw[1]} 
                for kw in single_keywords[:10]
            ],
            "phrase_keywords": [
                {"phrase": phrase[0], "frequency": phrase[1]} 
                for phrase in phrase_keywords[:8]
            ],
            "long_tail_keywords": long_tail[:5],
            "total_unique_words": len(word_freq),
            "keyword_density_analysis": self._analyze_keyword_density(word_freq, len(clean_words))
        }
    
    def _extract_phrases(self, content: str, n: int) -> List[str]:
        """Extract n-word phrases from content"""
        words = content.lower().split()
        phrases = []
        
        for i in range(len(words) - n + 1):
            phrase_words = []
            for j in range(n):
                word = re.sub(r'[^\w]', '', words[i + j])
                if len(word) > 2:
                    phrase_words.append(word)
            
            if len(phrase_words) == n:
                phrase = ' '.join(phrase_words)
                if len(phrase) > 6:  # Minimum phrase length
                    phrases.append(phrase)
        
        return phrases
    
    def _analyze_keyword_density(self, word_freq: Dict, total_words: int) -> Dict:
        """Analyze keyword density"""
        density_analysis = {}
        
        for word, freq in word_freq.items():
            density = (freq / total_words) * 100
            density_analysis[word] = {
                "frequency": freq,
                "density_percent": round(density, 2),
                "optimal": 1.0 <= density <= 3.0
            }
        
        return density_analysis