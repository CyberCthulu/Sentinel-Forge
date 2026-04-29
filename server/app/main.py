# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.mock import MockAdapter
from app.core.scenario import build_scenario_events
from app.core.pipeline import run_pipeline
from app.state.store import StateStore
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


app = FastAPI(title="Sentinel Forge API")

store = StateStore()
adapter = MockAdapter({"events": build_scenario_events()})


def reset_adapter():
    global adapter
    adapter = MockAdapter({"events": build_scenario_events()})


# -----------------------
# ROUTES
# -----------------------

@app.post("/simulate/start")
def start_simulation():
    reset_adapter()

    state = store.reset()
    state["meta"]["status"] = "running"
    state["meta"]["mode"] = "demo"
    return store.replace(state)


@app.post("/simulate/step")
def step_simulation():
    state = store.get()

    event = adapter.fetch_next_event()
    store.increment_step()

    if event:
        state = store.append_event(event)

    result = run_pipeline(
        state["events"],
        previous_correlation=state.get("correlation"),
    )

    # Keep canonical/normalized events in state.
    state["events"] = result.get("events", state["events"])

    state = store.apply_pipeline_result(result)
    state["meta"]["status"] = "running" if event else "complete"
    state["meta"]["mode"] = "demo"

    return store.replace(state)


@app.get("/state")
def get_state():
    return store.get()


@app.post("/reset")
def reset():
    reset_adapter()
    return store.reset()


# -----------------------
# CORS
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)