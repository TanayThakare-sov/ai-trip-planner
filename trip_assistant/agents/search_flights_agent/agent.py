from langchain_google_genai import ChatGoogleGenerativeAI
from trip_assistant.agents.base_agent import BaseAgent
from trip_assistant.config import AppConfig
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger
from langchain_core.messages import SystemMessage

logger = get_logger(__name__)

class SearchFlightsAgent(BaseAgent):
    def __init__(self):
        llm = ChatGoogleGenerativeAI(
            model=AppConfig.GOOGLE_MODEL_ID,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
        )

        sys_msg = SystemMessage(
            content="You are a helpful assistant that helps users search for flights based on their preferences and requirements"
        )

        super().__init__(llm, "SearchFlightsAgent", sys_msg)

    async def process(self, state: GeneralState) -> dict:
        pass