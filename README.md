# Trip Assistant

AI-powered travel planner that suggests destinations and creates itineraries using LLM agents and LangGraph.

## How It Works

1. **User describes** the ideal trip
2. **AI suggests** 3-5 destinations matching the description
3. **User picks** a destination from the list
4. **AI generates** a detailed travel itinerary

The workflow is orchestrated as a LangGraph state graph with an interrupt mechanism for user interaction.

## Tech Stack

- **Python** >= 3.10
- **LangGraph** — agent workflow orchestration
- **LangChain + Google Gemini** — LLM integration
- **Pydantic** — structured output validation

## Project Structure

```
trip_assistant/
├── main.py                          # Entry point
├── config/                          # Environment & app configuration
├── agents/
│   ├── base_agent.py                # Abstract base agent
│   ├── choose_destination_place_agent/
│   │   └── agent.py                 # Suggests destinations
│   └── create_itinerary_agent/
│       └── agent.py                 # Generates itinerary
├── graph/
│   ├── compile_graph.py             # Graph assembly & compilation
│   ├── nodes/                       # Graph node implementations
│   └── states/                      # State definitions
├── types/                           # Pydantic/TypedDict models
└── utils/
    └── logger.py                    # Logging setup
```

## Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd trip-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GOOGLE_API_KEY in .env
```

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GOOGLE_API_KEY` | Yes | — | Google Gemini API key |
| `GOOGLE_MODEL_ID` | No | `gemini-2.5-flash` | Gemini model to use |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## Usage

```bash
python -m trip_assistant.main
```

The app will ask you to describe your ideal trip, propose destinations, and generate an itinerary based on your choice.

## Graph Flow

```
START → choose_destination_place → (user input) → create_itinerary → END
```
