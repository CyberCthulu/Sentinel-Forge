class Event:
    def __init__(self, type, source, timestamp, metadata):
        self.type = type
        self.source = source
        self.timestamp = timestamp
        self.metadata = metadata