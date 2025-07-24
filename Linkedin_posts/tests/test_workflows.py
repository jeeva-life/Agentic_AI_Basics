import pytest
from src.workflows.youtube_workflow import YouTubeWorkflow

@pytest.fixture
def workflow():
    return YouTubeWorkflow()

class TestYouTubeWorkflow:
    
    def test_workflow_initialization(self, workflow):
        assert workflow.transcript_agent is not None
        assert workflow.title_agent is not None
        assert workflow.content_agent is not None
        assert workflow.workflow is not None
    
    def test_workflow_info(self, workflow):
        info = workflow.get_workflow_info()
        assert info['workflow_version'] == '2.0.0'
        assert len(info['agents']) == 3
        assert 'supported_platforms' in info
        assert 'workflow_steps' in info