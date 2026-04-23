import time

def run_scenario(step):
    sequence = [
        {"type": "failed_login", "user": "admin"},
        {"type": "failed_login", "user": "admin"},
        {"type": "failed_login", "user": "admin"},
        {"type": "successful_login", "user": "admin", "ip": "192.168.1.10"},
        {"type": "lateral_movement", "node": "node-2"},
        {"type": "drone_activity", "zone": "Sector B"},
    ]

    if step < len(sequence):
        return sequence[step]
    return None