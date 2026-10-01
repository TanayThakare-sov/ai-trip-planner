import streamlit as st
import asyncio
import uuid

from langgraph.types import Command
from trip_assistant.graph.compile_graph import compile_graph


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "app" not in st.session_state:
    st.session_state.app = compile_graph()

if "config" not in st.session_state:
    st.session_state.config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

if "destination_options" not in st.session_state:
    st.session_state.destination_options = None

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None


# --------------------------------------------------
# Async Helper
# --------------------------------------------------

def run_async(coroutine):
    return asyncio.run(coroutine)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("✈️ AI Trip Planner")

st.write(
    "Create a personalized multi-destination travel itinerary "
    "using AI-powered destination recommendations."
)


# --------------------------------------------------
# Trip Input
# --------------------------------------------------

trip_request = st.text_area(
    "Where do you want to travel?",
    placeholder=(
        "Example: I want a 7 day trip with nature, "
        "adventure, sightseeing and good food."
    ),
    height=100
)


# --------------------------------------------------
# Generate Destinations
# --------------------------------------------------

if st.button("🔍 Generate Trip", type="primary"):

    if not trip_request.strip():

        st.warning("Please describe the trip you want.")

    else:

        # Create a fresh graph for a new trip
        st.session_state.app = compile_graph()

        st.session_state.config = {
            "configurable": {
                "thread_id": str(uuid.uuid4())
            }
        }

        st.session_state.itinerary = None

        async def start_trip():

            app = st.session_state.app
            config = st.session_state.config

            await app.ainvoke(
                {
                    "ideal_destination_description": trip_request
                },
                config
            )

            state = await app.aget_state(config)

            return state.tasks[0].interrupts[0].value

        try:

            options = run_async(start_trip())

            st.session_state.destination_options = options

            st.rerun()

        except Exception as e:

            st.error(f"Error generating destinations: {e}")


# --------------------------------------------------
# Destination Selection
# --------------------------------------------------

if st.session_state.destination_options:

    st.divider()

    st.subheader("📍 Destination Options")

    options = st.session_state.destination_options

    option_labels = [
        f"{option['index']}. {option['city_name']}"
        for option in options
    ]

    selected_labels = st.multiselect(
        "Select any destinations you want to visit:",
        option_labels
    )

    # Show descriptions
    for option in options:

        with st.expander(
            f"{option['index']}. {option['city_name']}"
        ):

            st.write(
                option["short_description"]
            )


    # --------------------------------------------------
    # Create Itinerary
    # --------------------------------------------------

    if st.button("🗺️ Create Itinerary", type="primary"):

        if not selected_labels:

            st.warning(
                "Please select at least one destination."
            )

        else:

            # Convert selected destination labels to indexes
            selected_indexes = []

            for label in selected_labels:

                index = int(
                    label.split(".")[0]
                )

                selected_indexes.append(index)


            async def create_itinerary():

                app = st.session_state.app
                config = st.session_state.config

                result = await app.ainvoke(
                    Command(
                        resume=selected_indexes
                    ),
                    config
                )

                return result


            try:

                with st.spinner(
                    "🧠 Creating your personalized itinerary..."
                ):

                    result = run_async(
                        create_itinerary()
                    )

                itinerary = result.get(
                    "itinerary"
                )

                if itinerary:

                    st.session_state.itinerary = itinerary

                    st.rerun()

                else:

                    st.error(
                        "The itinerary was not returned."
                    )

            except Exception as e:

                st.error(
                    f"Error creating itinerary: {e}"
                )


# --------------------------------------------------
# Display Itinerary
# --------------------------------------------------

if st.session_state.itinerary:

    st.divider()

    st.header("🗺️ Your Trip Plan")

    # Streamlit renders the AI's Markdown properly
    st.markdown(
        st.session_state.itinerary
    )