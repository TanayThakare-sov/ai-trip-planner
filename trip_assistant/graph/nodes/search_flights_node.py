from trip_assistant.agents.search_flights_agent.agent import SearchFlightsAgent
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger

logger = get_logger(__name__)

agent = SearchFlightsAgent()

async def search_flights_node(state: GeneralState) -> dict:
    return await agent.process(state)