"""P2: perpetuo vs trimestral hasta el vencimiento; regla fija, sin solapamiento, costos y funding."""

from datetime import datetime, timedelta, timezone

import pytest

from lab.research import calendar_basis as cb


def days(start, n):
    d0 = datetime.fromisoformat(start)
    return [(d0 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n)]


def exp_ms(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000) + 8 * 3_600_000


def test_trade_books_basis_minus_funding_minus_costs():
    ds = days("2024-01-01", 70)                      # 30 días de historia + tenencia
    expiry = ds[60]
    p = {d: 100.0 for d in ds}
    q = {d: 102.0 for d in ds}                        # base 2% con ~29 días -> ~25% anual
    fd = {d: 0.0001 for d in ds}                      # funding 3,65% anual
    tr = cb.trades(q, p, fd, {exp_ms(expiry): 100.0}, perp_at_delivery={exp_ms(expiry): 100.0})
    assert len(tr) == 1                               # no solapa: una operación por vencimiento
    t = tr[0]
    assert t["entry"] == ds[29] and t["expiry"] == expiry
    held = len([d for d in ds if ds[29] < d <= expiry])
    assert t["funding_pct"] == pytest.approx(held * 0.0001 * 100)
    costs = 2 * (cb.TAKER + cb.SLIP) * 100 + (cb.TAKER + cb.SLIP) * 100 + cb.DELIVERY_FEE * 100
    assert t["net_pct"] == pytest.approx(2.0 - held * 0.01 - costs)


def test_no_entry_when_basis_does_not_beat_funding_plus_threshold():
    ds = days("2024-01-01", 70)
    p = {d: 100.0 for d in ds}
    q = {d: 100.05 for d in ds}                       # base mínima
    fd = {d: 0.0003 for d in ds}                      # funding alto
    assert cb.trades(q, p, fd, {exp_ms(ds[60]): 100.0}, perp_at_delivery={exp_ms(ds[60]): 100.0}) == []


def test_needs_30_days_of_funding_history_and_evaluates_excess():
    ds = days("2024-01-01", 40)
    p = {d: 100.0 for d in ds}
    q = {d: 103.0 for d in ds}
    fd = {d: 0.0 for d in ds[10:]}                    # solo 30 días de funding a partir del día 10
    tr = cb.trades(q, p, fd, {exp_ms(ds[39]): 100.0}, perp_at_delivery={exp_ms(ds[39]): 100.0})
    assert tr and tr[0]["entry"] >= ds[39 - 1 - 29] or tr == []
    ev = cb.evaluate([{"entry": "2024-01-01", "days": 30, "net_pct": 1.0, "worst_mtm_pct": -0.5},
                      {"entry": "2024-04-01", "days": 30, "net_pct": 0.6, "worst_mtm_pct": -1.0}],
                     lambda e, d: 0.4)
    assert ev["mean_excess_pct"] == pytest.approx(0.4) and ev["positive_excess"] == 2


def test_perp_exit_uses_price_at_delivery_hour_not_daily_close():
    """Regresión: con el cierre diario, un movimiento de la tarde del vencimiento
    aparecía como ganancia o pérdida del spread."""
    ds = days("2024-01-01", 70)
    expiry = ds[60]
    p = {d: 100.0 for d in ds}
    p[expiry] = 110.0                                  # el perpetuo sube DESPUÉS de las 08:00
    q = {d: 102.0 for d in ds}
    fd = {d: 0.0 for d in ds}
    t = cb.trades(q, p, fd, {exp_ms(expiry): 100.0}, perp_at_delivery={exp_ms(expiry): 100.0})[0]
    assert t["gross_pct"] == pytest.approx(2.0)        # solo la base: el +10% de la tarde no cuenta
    assert cb.trades(q, p, fd, {exp_ms(expiry): 100.0}) == []   # sin precio a la hora de entrega: no se opera
