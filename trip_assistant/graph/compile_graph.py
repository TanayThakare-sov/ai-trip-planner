from trip_assistant.graph.nodes.create_itinerary_node import create_itinerary_node
from trip_assistant.graph.nodes.choose_destination_place_node import choose_destination_place_node
from trip_assistant.graph.states.general_state import GeneralState
from langgraph.graph import StateGraph, START, END
from trip_assistant.utils.logger import get_logger
from langgraph.checkpoint.memory import InMemorySaver

logger = get_logger(__name__)

def compile_graph():
    graph = StateGraph(GeneralState)

    graph_memory = InMemorySaver()

    graph.add_node('choose_destination_place_node', choose_destination_place_node)
    graph.add_node('create_itinerary_node', create_itinerary_node)
    
    graph.add_edge(START, 'choose_destination_place_node')
    graph.add_edge('choose_destination_place_node', 'create_itinerary_node')
    graph.add_edge('create_itinerary_node', END)

    return graph.compile(checkpointer=graph_memory)