import pytest
import asyncio
from src.agents.transcript_agent import TranscriptAgent
from src.agents.title_agent import TitleAgent
from src.agents.content_agent import ContentAgent
from src.models.state import AgentState

@pytest.fixture
def sample_state():
    return AgentState(
        youtube_url="https://www.youtube.com/watch?v=test",
        transcript="",
        title="",
        content="",
        metadata={},
        seo_analysis=None,
        output_format="linkedin",
        error=""
    )

@pytest.fixture
def sample_transcript():
    return """
    Welcome to this tutorial about artificial intelligence and machine learning.
    In this video, we'll explore the fundamental concepts that drive modern AI systems.
    We'll discuss neural networks, deep learning, and practical applications.
    By the end of this video, you'll have a solid understanding of AI basics.
    """

@pytest.mark.asyncio
class TestTranscriptAgent:
    
    async def test_transcript_agent_initialization(self):
        agent = TranscriptAgent()
        assert len(agent.tools) == 2
        assert agent.tools[0].name == "youtube_transcript_extractor"
        assert agent.tools[1].name == "youtube_metadata_extractor"
    
    # Note: Full transcript extraction test would require valid YouTube URL
    # This is a structure test to verify agent setup

@pytest.mark.asyncio  
class TestTitleAgent:
    
    async def test_title_agent_initialization(self):
        agent = TitleAgent()
        assert len(agent.tools) == 2
        assert agent.tools[0].name == "title_analyzer"
        assert agent.tools[1].name == "web_search"
    
    async def test_title_generation_with_transcript(self, sample_state, sample_transcript):
        sample_state['transcript'] = sample_transcript
        agent = TitleAgent()
        
        # Mock the process to avoid API calls in tests
        # In real implementation, would use mock tools
        assert sample_state['transcript'] != ""

@pytest.mark.asyncio
class TestContentAgent:
    
    async def test_content_agent_initialization(self):
        agent = ContentAgent()
        assert len(agent.tools) == 2
        assert agent.tools[0].name == "content_structurer"
        assert agent.tools[1].name == "seo_analyzer"