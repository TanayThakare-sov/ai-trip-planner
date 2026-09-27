from langgraph.types import Command
from trip_assistant.graph.compile_graph import compile_graph
from trip_assistant.graph.states.general_state import GeneralState
from trip_assistant.utils.logger import get_logger

logger = get_logger(__name__)

async def start_network(data: str) -> dict:
    app = compile_graph()

    config = {"configurable": {"thread_id": "1"}}

    result = await app.ainvoke({"ideal_destination_description": data}, config)

    # The graph is now interrupted — extract proposed destinations
    state = await app.aget_state(config)
    interrupt_value = state.tasks[0].interrupts[0].value

    print("\n📍 Proposed destinations:\n")
    for opt in interrupt_value:
        print(f"  {opt['index']}. {opt['city_name']}")
        print(f"     {opt['short_description']}\n")

    choice = int(input("Choose a destination (enter the number): "))

    # Resume the graph with the user's choice
    result = await app.ainvoke(Command(resume=choice), config)

    logger.info("📊 Graph final result")
    logger.info(result)

    return {"final_destination": result["destination_place"]}

if __name__ == "__main__":
    import asyncio
    user_input = input("What kind of trip would you like to take? ")
    asyncio.run(start_network(user_input))