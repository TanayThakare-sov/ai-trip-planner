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

        tools = [
            TavilySearch(
                max_results=5,
                topic="general"
            )
        ]

        sys_msg = SystemMessage(
            content=(
                "You are an expert travel organizer. "
                "Create a detailed, practical and easy-to-read travel itinerary "
                "based on the user's journey requirements and selected destination(s). "

                "The selected destinations may contain one destination or multiple "
                "destinations separated by '→'. If multiple destinations are provided, "
                "treat them as one multi-destination trip and create a logical travel "
                "route in exactly the order provided by the user. "

                "Always use the search tool to find up-to-date information about "
                "attractions, restaurants, opening hours, transportation options, "
                "travel times between destinations, and local events. "

                "For a multi-destination trip, clearly separate each destination "
                "and explain how the traveler can move from one destination to the next. "

                "Structure the itinerary clearly by day. "
                "For every day, include Morning, Lunch, Afternoon, and Dinner "
                "whenever appropriate. "

                "For every activity, provide the place name followed by a useful "
                "2-4 sentence description explaining what the traveler can do "
                "or experience there. "

                "Also include relevant travel tips such as transportation, "
                "best time to visit, important things to carry, estimated travel "
                "time between destinations, and useful local information. "

                "Do not give a short summary. "
                "Generate a complete and detailed itinerary that is practical "
                "for an actual traveler. "

                "Use clear headings, bullet points, spacing, and readable Markdown."
            )
        )

        super().__init__(
            llm,
            "CreateItineraryAgent",
            sys_msg,
            tools=tools
        )

    async def process(self, state: GeneralState) -> dict:

        try:

            destination = state["destination_place"]

            human_msg = HumanMessage(
                content=destination
            )

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

                content = "".join(
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict)
                )

            logger.info(
                "📝 Itinerary creation completed"
            )

            return {
                "itinerary": content,
                "messages": [
                    human_msg,
                    ai_msg
                ]
            }

        except Exception as e:

            logger.error(
                f"Error in create itinerary: {e}"
            )

            raise