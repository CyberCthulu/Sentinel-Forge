# app/models/event.py   
class Event:
    def __init__(self, id, type, domain, source, timestamp, metadata):
        self.id = id
        self.type = type
        self.domain = domain
        self.source = source
        self.timestamp = timestamp
        self.metadata = metadata  