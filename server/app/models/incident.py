# app/models/incident.py
class Incident:
    def __init__(self, type, severity, confidence, summary, signals, actions, location=None):
        self.type = type
        self.severity = severity
        self.confidence = confidence
        self.summary = summary
        self.signals = signals
        self.actions = actions
        self.location = location