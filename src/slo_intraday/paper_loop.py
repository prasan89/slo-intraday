from __future__ import annotations
import os
import time
from datetime import datetime, time as dt_time
from zoneinfo import ZoneInfo
from .cpr import calculate_cpr
from .models import Bar, Position, Side
from .report import export_positions, export_signals, print_signals
from .risk import RiskConfig, daily_loss_limit, quantity_for_signal
from .signals import SignalConfig, evaluate

IST = ZoneInfo("Asia/Kolkata")
OPEN = dt_time(9, 15)
CLOSE = dt_time(15, 30)

class PaperIntraday:
    """Paper engine with provider-independent signal logic.

    A concrete FYERS adapter can feed 5-minute bars into `scan_symbol`.
    No broker orders are submitted.
    """
    def __init__(self) -> None:
        self.interval = int(os.getenv("SLO_INTRADAY_INTERVAL_SECONDS", "300"))
        self.risk = RiskConfig(
            capital=float(os.getenv("SLO_INTRADAY_CAPITAL", "1500000")),
            risk_per_trade_pct=float(os.getenv("SLO_INTRADAY_RISK_PCT", "0.5")),
            daily_loss_limit_pct=float(os.getenv("SLO_INTRADAY_DAILY_LOSS_PCT", "2.0")),
            max_open_positions=int(os.getenv("SLO_INTRADAY_MAX_OPEN", "5")),
        )
        self.signal_config = SignalConfig()
        self.positions: list[Position] = []
        self.signaled_symbols: set[str] = set()
        self.daily_pnl = 0.0

    def scan_symbol(self, symbol: str, bars: list[Bar], previous_day_ohlc: tuple[float, float, float], lot_size: int, market_bullish: bool | None = None):
        if symbol in self.signaled_symbols: return None
        high, low, close = previous_day_ohlc
        cpr = calculate_cpr(high, low, close)
        signal = evaluate(symbol, bars, cpr, market_bullish, self.signal_config)
        if signal is None: return None
        if len([p for p in self.positions if p.exit is None]) >= self.risk.max_open_positions: return None
        if self.daily_pnl <= -daily_loss_limit(self.risk): return None
        qty = quantity_for_signal(signal.price, signal.stop, lot_size, self.risk)
        if qty <= 0: return None
        position = Position(symbol, signal.side, signal.price, signal.stop, signal.target, qty, signal.timestamp)
        self.positions.append(position)
        self.signaled_symbols.add(symbol)
        print_signals([signal])
        export_signals([signal])
        export_positions(self.positions)
        return signal

    def manage_symbol(self, symbol: str, bars: list[Bar]) -> None:
        if not bars: return
        price = bars[-1].close
        for p in self.positions:
            if p.symbol != symbol or p.exit is not None: continue
            hit_stop = price <= p.stop if p.side == Side.LONG else price >= p.stop
            hit_target = price >= p.target if p.side == Side.LONG else price <= p.target
            if hit_stop or hit_target:
                p.exit = p.stop if hit_stop else p.target
                p.closed_at = bars[-1].timestamp
                p.exit_reason = "STOP" if hit_stop else "TARGET"
                pnl_per_unit = p.exit - p.entry if p.side == Side.LONG else p.entry - p.exit
                self.daily_pnl += pnl_per_unit * p.quantity
        export_positions(self.positions)

    def square_off(self, timestamp: datetime, prices: dict[str, float]) -> None:
        for p in self.positions:
            if p.exit is not None or p.symbol not in prices: continue
            p.exit = prices[p.symbol]
            p.closed_at = timestamp
            p.exit_reason = "EOD"
            pnl_per_unit = p.exit - p.entry if p.side == Side.LONG else p.entry - p.exit
            self.daily_pnl += pnl_per_unit * p.quantity
        export_positions(self.positions)

    def run_forever(self) -> None:
        print("SLO intraday paper engine started — no broker orders will be placed.")
        while True:
            now = datetime.now(IST)
            if now.time() >= CLOSE:
                self.square_off(now, {})
            time.sleep(self.interval)

def main() -> None:
    PaperIntraday().run_forever()

if __name__ == "__main__":
    main()
