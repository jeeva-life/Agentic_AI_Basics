import pytest
from src.tools.youtube_tools import YouTubeTranscriptTool, YouTubeMetadataTool
from src.tools.content_tools import ContentStructureTool, SEOAnalysisTool
from src.tools.seo_tools import AdvancedSEOTool, KeywordExtractorTool
from tests.fixtures.sample_data import SAMPLE_TRANSCRIPT, SAMPLE_YOUTUBE_URLS

class TestYouTubeTools:
    
    def test_transcript_tool_initialization(self):
        tool = YouTubeTranscriptTool()
        assert tool.name == "youtube_transcript_extractor"
        assert "transcript" in tool.description.lower()
    
    def test_metadata_tool_initialization(self):
        tool = YouTubeMetadataTool()
        assert tool.name == "youtube_metadata_extractor"
        assert "metadata" in tool.description.lower()
    
    # Note: Actual YouTube API tests would require valid videos with transcripts

class TestContentTools:
    
    def test_content_structurer_initialization(self):
        tool = ContentStructureTool()
        assert tool.name == "content_structurer"
        assert "structure" in tool.description.lower()
    
    def test_content_structuring_linkedin(self):
        tool = ContentStructureTool()
        test_input = f"{SAMPLE_TRANSCRIPT}|||linkedin"
        result = tool._run(test_input)
        assert "linkedin" in result.lower()
        assert "error" not in result.lower()
    
    def test_seo_analyzer_initialization(self):
        tool = SEOAnalysisTool()
        assert tool.name == "seo_analyzer"
        assert "seo" in tool.description.lower()
    
    def test_seo_analysis_execution(self):
        tool = SEOAnalysisTool()
        result = tool._run(SAMPLE_TRANSCRIPT)
        assert "SEO Analysis" in result
        assert "word_count" in result

class TestSEOTools:
    
    def test_advanced_seo_tool_initialization(self):
        tool = AdvancedSEOTool()
        assert tool.name == "advanced_seo_analyzer"
        assert "comprehensive" in tool.description.lower()
    
    def test_keyword_extractor_initialization(self):
        tool = KeywordExtractorTool()
        assert tool.name == "keyword_extractor"
        assert "keyword" in tool.description.lower()
    
    def test_keyword_extraction(self):
        tool = KeywordExtractorTool()
        result = tool._run(SAMPLE_TRANSCRIPT)
        assert "Keyword Analysis" in result
        assert "single_keywords" in result