from langchain_google_genai import ChatGoogleGenerativeAI
from trip_assistant.agents.base_agent import BaseAgent
from trip_assistant.config import AppConfig
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_tavily import TavilySearch

logger = get_logger(__name__)

class CreateItineraryAgent(BaseAgent):
    def __init__(self):
        llm = ChatGoogleGenerativeAI(
            model=AppConfig.GOOGLE_MODEL_ID,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
        )

        tools = [TavilySearch(max_results=5, topic="general")]

        sys_msg = SystemMessage(
            content=(
                "You are an expert travel organizer. Create a correct itinerary travel plan "
                "based on the user's ideal journey with the passed destination. "
                "Always use the search tool to find up-to-date information about "
                "attractions, restaurants, opening hours, and local events."
            )
        )

        super().__init__(llm, "CreateItineraryAgent", sys_msg, tools=tools)

    async def process(self, state: GeneralState) -> dict:
        try:
            human_msg = HumanMessage(content=state["destination_place"])

            final_chunk = None

            async for chunk in self.agent.astream(
                {"messages": [human_msg]},
                stream_mode="values"
            ):
                chunk["messages"][-1].pretty_print()
                final_chunk = chunk

            ai_msg = final_chunk["messages"][-1]
            content = ai_msg.content

            if isinstance(content, list):
                content = "".join(block.get("text", "") for block in content if isinstance(block, dict))

            logger.info("📝 Itinerary creation completed")

            return {
                "itinerary": content,
                "messages": [human_msg, ai_msg]
            }

        except Exception as e:
            logger.error(f"Error in create itinerary: {e}")
            raise