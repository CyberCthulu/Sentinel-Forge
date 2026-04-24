# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.scenario import run_scenario
from app.core.pipeline import run_pipeline

app = FastAPI()


# -----------------------
# HELPERS
# -----------------------

def empty_signal(name):
    return {
        "name": name,
        "active": False,
        "evidence": []
    }


def serialize_signal(signal):
    return {
        "name": signal.name,
        "active": signal.active,
        "evidence": signal.evidence,
    }

def serialize_incident(incident):
    if not incident:
        return None

    return {
        "type": incident.type,
        "severity": incident.severity,
        "confidence": incident.confidence,
        "summary": incident.summary,
        "signals": incident.signals,
        "actions": incident.actions,
        "location": incident.location,
    }


def build_initial_state():
    return {
        "events": [],
        "signals": {
            "failed_logins": empty_signal("failed_logins"),
            "suspicious_login": empty_signal("suspicious_login"),
            "lateral_movement": empty_signal("lateral_movement"),
            "drone_activity": empty_signal("drone_activity"),
        },
        "incident": None,
    }


# -----------------------
# GLOBAL STATE
# -----------------------

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

    signals, incident = run_pipeline(state["events"])

    # 🔥 FIX: serialize Signal objects
    state["signals"] = {
        k: serialize_signal(v)
        for k, v in signals.items()
    }

    state["incident"] = incident

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