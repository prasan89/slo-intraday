from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CPR:
    pivot: float
    bc: float
    tc: float
    r1: float
    r2: float
    s1: float
    s2: float

def calculate_cpr(high: float, low: float, close: float) -> CPR:
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = 2 * pivot - bc
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    return CPR(pivot, min(bc, tc), max(bc, tc), r1, r2, s1, s2)
