# app/main.py
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.mock import MockAdapter
from app.api.routes.agent import router as agent_router
from app.core.pipeline import run_pipeline
from app.core.scenario import build_scenario_events
from app.state.store import StateStore


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


app = FastAPI(title="Sentinel Forge API")
app.include_router(agent_router)

store = StateStore()
adapter = MockAdapter({"events": build_scenario_events()})


def reset_adapter():
    global adapter
    adapter = MockAdapter({"events": build_scenario_events()})


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

    state = store.apply_pipeline_result(result)

    # A new event means the previous analyst answer may be stale.
    # The operator can explicitly ask the analyst again from the incident popup.
    if event:
        state = store.clear_agent()

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)