from abc import ABC, abstractmethod
from typing import Dict, Any
from trip_assistant.utils.logger import get_logger
from langchain_core.messages import SystemMessage
from langchain.agents import create_agent

logger = get_logger(__name__)

class BaseAgent(ABC):
    """
    Base class for all agents
    """
    def __init__(self, llm, agent_name: str, sys_message: SystemMessage, tools = None, response_format = None):
        self.agent_name = agent_name

        self.agent = create_agent(
            model=llm,
            tools=tools or [],
            system_prompt=sys_message,
            response_format=response_format,
        )

        logger.info(f"🤖 Initialized {agent_name}")
    
    @abstractmethod
    async def process(self, data: Any) -> Dict[str, Any]:
        """Main processing method to be implemented by all agents"""
        pass
