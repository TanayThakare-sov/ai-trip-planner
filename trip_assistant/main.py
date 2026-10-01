from langgraph.types import Command
from trip_assistant.graph.compile_graph import compile_graph
from trip_assistant.utils.logger import get_logger

logger = get_logger(__name__)


async def start_network(data: str) -> dict:

    app = compile_graph()

    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    # Start the graph
    result = await app.ainvoke(
        {
            "ideal_destination_description": data
        },
        config
    )

    # Get destination options from the interrupted graph
    state = await app.aget_state(config)

    interrupt_value = state.tasks[0].interrupts[0].value

    print("\n📍 Proposed destinations:\n")

    for opt in interrupt_value:
        print(f"  {opt['index']}. {opt['city_name']}")
        print(f"     {opt['short_description']}\n")

    # User can select any combination of destinations
    choice_input = input(
        "Choose destinations (e.g. 3 or 2,7 or 1,4,9): "
    )

    try:
        choices = [
            int(index.strip())
            for index in choice_input.split(",")
            if index.strip()
        ]
    except ValueError:
        print("❌ Please enter destination numbers separated by commas.")
        return {}

    # Remove duplicates while preserving order
    choices = list(dict.fromkeys(choices))

    # Validate selections
    available_indexes = {
        opt["index"]
        for opt in interrupt_value
    }

    invalid_choices = [
        choice
        for choice in choices
        if choice not in available_indexes
    ]

    if invalid_choices:
        print(
            f"❌ Invalid destination number(s): {invalid_choices}"
        )
        return {}

    print("\n📍 Selected destinations:\n")

    for choice in choices:
        selected_option = next(
            opt for opt in interrupt_value
            if opt["index"] == choice
        )

        print(
            f"  {choice}. {selected_option['city_name']}"
        )

    # Resume the graph with selected destinations
    result = await app.ainvoke(
        Command(resume=choices),
        config
    )

    logger.info("📊 Graph final result")
    logger.info(result)

    return {
        "final_destination": result.get("destination_place"),
        "itinerary": result.get("itinerary")
    }


if __name__ == "__main__":

    import asyncio

    user_input = input(
        "What kind of trip would you like to take? "
    )

    asyncio.run(
        start_network(user_input)
    )