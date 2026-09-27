from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.structured_output import ToolStrategy
from trip_assistant.agents.base_agent import BaseAgent
from trip_assistant.config import AppConfig
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.types.destination_option import DestinationOptions
from trip_assistant.utils.logger import get_logger
from langchain_core.messages import SystemMessage, HumanMessage

logger = get_logger(__name__)

class ChooseDestinationPlaceAgent(BaseAgent):
    def __init__(self):
        llm = ChatGoogleGenerativeAI(
            model=AppConfig.GOOGLE_MODEL_ID,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
        )

        sys_msg = SystemMessage(
            content=(
                "You are an expert travel organizer. "
                "Based on the user's description, suggest a list of 3-5 ideal destinations. "
                "For each destination, provide the city name and a short description "
                "explaining why it suits the user's needs."
            )
        )

        super().__init__(
            llm=llm,
            agent_name="ChooseDestinationPlaceAgent",
            sys_message=sys_msg,
            response_format=ToolStrategy(DestinationOptions)
        )

    async def process(self, state: GeneralState) -> dict:
        try:
            human_msg = HumanMessage(content=state["ideal_destination_description"])

            result = await self.agent.ainvoke({"messages": [human_msg]})

            destinations: DestinationOptions = result["structured_response"]

            logger.info(f"✈️ Proposed {len(destinations.destinations)} destinations")

            return {
                "destination_options": destinations,
                "messages": [human_msg]
            }

        except Exception as e:
            logger.error(f"Error in choose destination place: {e}")
            raise
