# SLO Intraday

Intraday F&O research and paper-trading system using FYERS market data.

## Strategy v1

- Full configured F&O universe
- 5-minute monitoring
- Opening-range context
- CPR levels calculated once after the open
- VWAP and volume confirmation
- NIFTY/BANKNIFTY market-regime confirmation
- Relative strength / weakness
- Multiple simultaneous paper signals
- One active setup per symbol at a time
- Configurable stop, target and trailing rules
- Hard daily loss limit
- Intraday-only: all paper positions squared off before market close
- CSV/text reporting
- No broker order placement

The system is paper-trading only. A ₹1 crore/week figure is treated strictly as a research benchmark, not a guaranteed outcome.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Configure:

```bash
export FYERS_APP_ID='YOUR_APP_ID'
export FYERS_ACCESS_TOKEN='YOUR_ACCESS_TOKEN'
export DATA_PROVIDER='fyers'
export SLO_PAPER_INTERVAL_SECONDS=300
```

Run tests:

```bash
pytest -q
```

Run the paper scanner:

```bash
slo-intraday-paper
```
