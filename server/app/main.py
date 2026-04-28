# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.scenario import run_scenario
from app.core.pipeline import run_pipeline
from app.state.store import StateStore


app = FastAPI(title="Sentinel Forge API")

store = StateStore()


# -----------------------
# ROUTES
# -----------------------

@app.post("/simulate/start")
def start_simulation():
    state = store.reset()
    state["meta"]["status"] = "running"
    return store.replace(state)


@app.post("/simulate/step")
def step_simulation():
    state = store.get()
    step = store.get_step()

    event = run_scenario(step)
    store.increment_step()

    if event:
        state = store.append_event(event)

    result = run_pipeline(
        state["events"],
        previous_correlation=state.get("correlation"),
    )

    state = store.apply_pipeline_result(result)
    state["meta"]["status"] = "running" if event else "complete"

    return store.replace(state)


@app.get("/state")
def get_state():
    return store.get()


@app.post("/reset")
def reset():
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