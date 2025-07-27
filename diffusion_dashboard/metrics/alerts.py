from __future__ import annotations

def deployment_alert(c1: float, c4: float, c6: float, c7: float) -> str:
    if (c1 >= 30.0) and (c4 >= 5.0) and (c6 >= 95.0) and (c7 <= 0.5):
        return "GREEN"
    if (c1 >= 30.0) ^ (c4 >= 5.0):
        return "AMBER"
    return "RED"

def readiness_alert(a6_ok: bool, a7_ok: bool, b6_ok: bool) -> str:
    if a6_ok and a7_ok and b6_ok:
        return "GREEN"
    if (a6_ok and b6_ok) or (a7_ok and b6_ok):
        return "AMBER"
    return "RED"

def macro_signal_alert(gap: float, significant: bool, consec_years: int) -> str:
    if (gap >= 1.5) and significant and (consec_years >= 2):
        return "GREEN"
    if (gap >= 1.5) and significant:
        return "AMBER"
    return "RED"
