from __future__ import annotations
from dataclasses import dataclass
from .cpr import CPR
from .indicators import atr, relative_volume, vwap
from .models import Bar, Side, Signal

@dataclass(frozen=True)
class SignalConfig:
    min_score: float = 70.0
    volume_multiple: float = 1.25
    stop_atr_multiple: float = 1.0
    reward_risk: float = 2.0
    max_signals_per_symbol_day: int = 1

def evaluate(symbol: str, bars: list[Bar], cpr: CPR, market_bullish: bool | None = None, config: SignalConfig | None = None) -> Signal | None:
    config = config or SignalConfig()
    if len(bars) < 20: return None
    last, prev = bars[-1], bars[-2]
    vw = vwap(bars)
    rv = relative_volume(bars)
    av = atr(bars)
    if vw is None or rv is None or av is None or av <= 0: return None

    long_cross = prev.close <= cpr.r1 and last.close > cpr.r1
    short_cross = prev.close >= cpr.s1 and last.close < cpr.s1
    long_ok = long_cross and last.close > vw and rv >= config.volume_multiple and (market_bullish is not False)
    short_ok = short_cross and last.close < vw and rv >= config.volume_multiple and (market_bullish is not True)
    if not (long_ok or short_ok): return None

    score = 40.0
    score += 25.0
    score += min(15.0, max(0.0, (rv - 1.0) * 20.0))
    if long_ok and market_bullish is True: score += 10.0
    if short_ok and market_bullish is False: score += 10.0
    if score < config.min_score: return None

    if long_ok:
        stop = min(cpr.r1, last.close - config.stop_atr_multiple * av)
        risk = last.close - stop
        target = last.close + risk * config.reward_risk
        return Signal(symbol, Side.LONG, last.timestamp, last.close, "R1_BREAKOUT", score, stop, target, f"R1 breakout; price above VWAP; RV={rv:.2f}x")
    stop = max(cpr.s1, last.close + config.stop_atr_multiple * av)
    risk = stop - last.close
    target = last.close - risk * config.reward_risk
    return Signal(symbol, Side.SHORT, last.timestamp, last.close, "S1_BREAKDOWN", score, stop, target, f"S1 breakdown; price below VWAP; RV={rv:.2f}x")
