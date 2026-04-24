# app/models/incident.py
class Incident:
    def __init__(self, type, severity, confidence, summary, narrative, signals, actions):
        self.type = type
        self.severity = severity
        self.confidence = confidence
        self.summary = summary
        self.narrative = narrative
        self.signals = signals
        self.actions = actions