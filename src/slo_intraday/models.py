from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Side(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass(frozen=True)
class Signal:
    symbol: str
    side: Side
    timestamp: datetime
    price: float
    trigger: str
    score: float
    stop: float
    target: float
    reason: str

@dataclass
class Position:
    symbol: str
    side: Side
    entry: float
    stop: float
    target: float
    quantity: int
    opened_at: datetime
    exit: float | None = None
    closed_at: datetime | None = None
    exit_reason: str | None = None
