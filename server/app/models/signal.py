#app/models/signal.py
class Signal:
    def __init__(self, id, kind, domain, weight, evidence, label):
        self.id = id
        self.kind = kind
        self.domain = domain
        self.weight = weight
        self.evidence = evidence  # list of event IDs
        self.label = label
        self.location = location or {"lat": None, "lon": None}