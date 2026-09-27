from trip_assistant.agents.create_itinerary_agent.agent import CreateItineraryAgent
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger

logger = get_logger(__name__)

agent = CreateItineraryAgent()

async def create_itinerary_node(state: GeneralState) -> dict:
    return await agent.process(state)