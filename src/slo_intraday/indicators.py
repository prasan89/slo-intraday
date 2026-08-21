from __future__ import annotations
from math import sqrt
from typing import Sequence

def sma(values: Sequence[float], period: int) -> float | None:
    if period <= 0 or len(values) < period: return None
    return sum(values[-period:]) / period

def ema(values: Sequence[float], period: int) -> float | None:
    if period <= 0 or len(values) < period: return None
    value = sum(values[:period]) / period
    alpha = 2 / (period + 1)
    for x in values[period:]: value = alpha * x + (1 - alpha) * value
    return value

def vwap(bars) -> float | None:
    if not bars: return None
    total_pv = total_volume = 0.0
    for b in bars:
        typical = (b.high + b.low + b.close) / 3
        total_pv += typical * b.volume
        total_volume += b.volume
    return total_pv / total_volume if total_volume else None

def atr(bars, period: int = 14) -> float | None:
    if len(bars) <= period: return None
    trs = []
    for i, b in enumerate(bars):
        if i == 0: trs.append(b.high - b.low)
        else:
            prev = bars[i - 1].close
            trs.append(max(b.high - b.low, abs(b.high - prev), abs(b.low - prev)))
    return sum(trs[-period:]) / period

def opening_range(bars, minutes: int = 15):
    if not bars: return None
    start = bars[0].timestamp
    selected = [b for b in bars if (b.timestamp - start).total_seconds() <= minutes * 60]
    if not selected: return None
    return max(b.high for b in selected), min(b.low for b in selected)

def relative_volume(bars, lookback: int = 20) -> float | None:
    if len(bars) <= lookback: return None
    baseline = sum(b.volume for b in bars[-lookback-1:-1]) / lookback
    return bars[-1].volume / baseline if baseline else None

def volatility_percent(closes: Sequence[float]) -> float | None:
    if len(closes) < 2: return None
    returns = [closes[i] / closes[i-1] - 1 for i in range(1, len(closes)) if closes[i-1]]
    if not returns: return None
    mean = sum(returns) / len(returns)
    return sqrt(sum((r-mean)**2 for r in returns) / len(returns)) * 100
