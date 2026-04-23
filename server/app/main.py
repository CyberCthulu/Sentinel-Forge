from fastapi import FastAPI
from app.core.scenario import run_scenario
from app.core.pipeline import run_pipeline

app = FastAPI()

events = []
step = 0

@app.get("/simulate")
def simulate():
    global step

    event = run_scenario(step)
    step += 1

    if event:
        events.append(event)

    incident = run_pipeline(events)

    return {
        "events": events,
        "incident": incident
    }