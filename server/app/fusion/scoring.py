#app/fusion/scoring.py
def score(signals):
    score = 0.5
    if signals["failed_logins"]: score += 0.1
    if signals["suspicious_login"]: score += 0.1
    if signals["lateral_movement"]: score += 0.1
    if signals["drone_activity"]: score += 0.1
    return min(score, 0.99)