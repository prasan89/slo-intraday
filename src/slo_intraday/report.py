from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
from .models import Signal, Position

def print_signals(signals: list[Signal]) -> None:
    signals = sorted(signals, key=lambda s: s.score, reverse=True)
    print("\nSLO INTRADAY — PAPER SIGNALS")
    print("=" * 90)
    print(f"{'#':>3} {'Symbol':<14} {'Side':<6} {'Entry':>10} {'Stop':>10} {'Target':>10} {'Score':>7}")
    print("-" * 90)
    for i, s in enumerate(signals, 1):
        print(f"{i:>3} {s.symbol:<14} {s.side.value:<6} {s.price:>10.2f} {s.stop:>10.2f} {s.target:>10.2f} {s.score:>7.1f}")

def export_signals(signals: list[Signal], path: str | Path = "reports/intraday_signals.csv") -> None:
    import csv
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["symbol","side","timestamp","price","trigger","score","stop","target","reason"])
        writer.writeheader()
        for s in sorted(signals, key=lambda x: x.score, reverse=True):
            row = asdict(s); row["side"] = s.side.value
            writer.writerow(row)

def export_positions(positions: list[Position], path: str | Path = "reports/intraday_positions.csv") -> None:
    import csv
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["symbol","side","entry","stop","target","quantity","opened_at","exit","closed_at","exit_reason"])
        writer.writeheader()
        for p in positions:
            row = asdict(p); row["side"] = p.side.value
            writer.writerow(row)
