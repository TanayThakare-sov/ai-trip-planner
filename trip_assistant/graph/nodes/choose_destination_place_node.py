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

    selected_indexes = interrupt(options_for_human)

    # Support both a single destination and multiple destinations
    if isinstance(selected_indexes, int):
        selected_indexes = [selected_indexes]

    selected_destinations = [
        destination_options.destinations[index - 1]
        for index in selected_indexes
    ]

    destination_names = [
        destination.city_name
        for destination in selected_destinations
    ]

    destination_place = ", ".join(destination_names)

    logger.info(
        f"🎯 User selected destinations: {destination_place}"
    )

    return {
        "destination_options": destination_options,
        "destination_place": destination_place,
        "messages": result["messages"]
    }