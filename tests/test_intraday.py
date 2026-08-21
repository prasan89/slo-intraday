from datetime import datetime, timezone
from slo_intraday.cpr import calculate_cpr
from slo_intraday.indicators import vwap, atr
from slo_intraday.models import Bar, Side
from slo_intraday.risk import RiskConfig, quantity_for_signal
from slo_intraday.signals import evaluate


def bars(prices, start_volume=1000):
    out=[]
    for i, p in enumerate(prices):
        out.append(Bar(datetime(2026, 8, 21, 9, 15+i, tzinfo=timezone.utc), p-1, p+1, p-1.5, p, start_volume))
    return out


def test_cpr_levels():
    cpr = calculate_cpr(110, 100, 105)
    assert round(cpr.pivot, 6) == 105
    assert cpr.r1 == 110
    assert cpr.s1 == 100


def test_vwap_atr():
    data = bars([100 + i for i in range(20)])
    assert vwap(data) > 0
    assert atr(data) > 0


def test_long_breakout_signal():
    data = bars([105] * 19 + [111], start_volume=2000)
    cpr = calculate_cpr(110, 100, 105)
    signal = evaluate("TEST", data, cpr, market_bullish=True)
    assert signal is not None
    assert signal.side == Side.LONG
    assert signal.trigger == "R1_BREAKOUT"


def test_position_size_respects_risk():
    config = RiskConfig(capital=1_000_000, risk_per_trade_pct=0.5)
    qty = quantity_for_signal(100, 98, 50, config)
    assert qty > 0
    assert qty % 50 == 0
