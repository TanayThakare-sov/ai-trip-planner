from langgraph.types import interrupt
from trip_assistant.agents.choose_destination_place_agent.agent import ChooseDestinationPlaceAgent
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger

logger = get_logger(__name__)

agent = ChooseDestinationPlaceAgent()

async def choose_destination_place_node(state: GeneralState) -> dict:
    result = await agent.process(state)

    destination_options = result["destination_options"]

    options_for_human = [
        {
            "index": i + 1,
            "city_name": opt.city_name,
            "short_description": opt.short_description
        }
        for i, opt in enumerate(destination_options.destinations)
    ]

    selected_index = interrupt(options_for_human)

    selected = destination_options.destinations[selected_index - 1]

    logger.info(f"🎯 User selected: {selected.city_name}")

    return {
        "destination_options": destination_options,
        "destination_place": selected.city_name,
        "messages": result["messages"]
    }
