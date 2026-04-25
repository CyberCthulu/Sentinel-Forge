from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.scenario import run_scenario
from app.core.pipeline import run_pipeline

app = FastAPI()


# -----------------------
# STATE
# -----------------------

def build_initial_state():
    return {
        "events": [],
        "signals": [],
        "incident": None,
        "map_state": {"tracks": []},

    }


state = build_initial_state()
step_counter = 0


# -----------------------
# ROUTES
# -----------------------

@app.post("/simulate/start")
def start_simulation():
    global state, step_counter

    state = build_initial_state()
    step_counter = 0

    return state


@app.post("/simulate/step")
def step_simulation():
    global state, step_counter

    event = run_scenario(step_counter)
    step_counter += 1

    if event:
        state["events"].append(event)

    result = run_pipeline(state["events"])

    state["signals"] = result["signals"]
    state["incident"] = result["incident"]
    state["map_state"] = result["map_state"]


    return state


@app.get("/state")
def get_state():
    return state


@app.post("/reset")
def reset():
    global state, step_counter

    state = build_initial_state()
    step_counter = 0

    return state


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