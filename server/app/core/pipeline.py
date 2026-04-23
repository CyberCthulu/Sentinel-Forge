from app.core.detection import detect
from app.core.correlation import correlate
from app.core.interpreter import interpret

def run_pipeline(events):
    signals = detect(events)
    incident_type = correlate(signals)

    if incident_type:
        return interpret(incident_type)

    return None