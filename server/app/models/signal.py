#app/models/signal.py
class Signal:
    def __init__(self, name, active, evidence):
        self.name = name
        self.active = active
        self.evidence = evidence