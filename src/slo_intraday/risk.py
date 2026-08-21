from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskConfig:
    capital: float = 1_500_000.0
    risk_per_trade_pct: float = 0.5
    daily_loss_limit_pct: float = 2.0
    max_open_positions: int = 5
    max_capital_per_trade_pct: float = 10.0

def quantity_for_signal(entry: float, stop: float, lot_size: int, config: RiskConfig) -> int:
    if entry <= 0 or stop <= 0 or lot_size <= 0 or entry == stop: return 0
    risk_budget = config.capital * config.risk_per_trade_pct / 100
    risk_per_share = abs(entry - stop)
    lots = int(risk_budget // (risk_per_share * lot_size))
    capital_cap = config.capital * config.max_capital_per_trade_pct / 100
    lots = min(lots, int(capital_cap // (entry * lot_size)))
    return max(0, lots * lot_size)

def daily_loss_limit(config: RiskConfig) -> float:
    return config.capital * config.daily_loss_limit_pct / 100
