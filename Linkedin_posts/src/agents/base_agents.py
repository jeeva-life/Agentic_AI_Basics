# =============================================================================
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from src.models.state import AgentState
from src.config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the workflow"""
    
    def __init__(self, tools: List[BaseTool]):
        self.tools = tools
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.DEFAULT_TEMPERATURE,
            max_tokens=settings.DEFAULT_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        self.agent_name = self.__class__.__name__
        
    @abstractmethod
    async def process(self, state: AgentState) -> AgentState:
        """Process the agent's task and update state"""
        pass
    
    def _add_agent_metadata(self, state: AgentState, **kwargs) -> None:
        """Add agent-specific metadata to state"""
        if 'agent_history' not in state['metadata']:
            state['metadata']['agent_history'] = []
        
        agent_info = {
            'agent': self.agent_name,
            'tools_used': [tool.name for tool in self.tools],
            'processed_at': kwargs.get('processed_at'),
            **kwargs
        }
        state['metadata']['agent_history'].append(agent_info)
    
    def _handle_error(self, state: AgentState, error: Exception) -> AgentState:
        """Handle errors consistently across agents"""
        error_msg = f"{self.agent_name} failed: {str(error)}"
        logger.error(error_msg)
        state['error'] = error_msg
        return state