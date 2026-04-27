#app/models/signal.py
class Signal:
    def __init__(
        self,
        id,
        kind,
        domain,
        weight,
        evidence,
        label,
        location=None,  # ✅ ADD THIS
    ):
        self.id = id
        self.kind = kind
        self.domain = domain
        self.weight = weight
        self.evidence = evidence
        self.label = label

        # ✅ Safe default
        self.location = location or {"lat": None, "lon": None}