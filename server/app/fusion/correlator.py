# app/fusion/correlator.py
def correlate(signals):
    if all(signals.values()):
        return "COORDINATED_INTRUSION"
    return None