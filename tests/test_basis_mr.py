"""E3: reversión de la base; entrada con |z| > 1, salida al revertir, costos y funding."""

from datetime import datetime, timedelta, timezone

import pytest

from lab.research import basis_mr as bm


def ds(n):
    d0 = datetime(2024, 1, 1)
    return [(d0 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n)]


def exp_ms(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp() * 1000) + 8 * 3_600_000


def stable_q(d, p, exp_day, ann=0.08):
    """Trimestral con base ANUALIZADA estable (con ruido chico), como en el mercado."""
    e = datetime.fromisoformat(exp_day)
    return {x: p[x] * (1 + (ann + 0.002 * (i % 2)) * ((e - datetime.fromisoformat(x)).days - 1 + 8 / 24) / 365)
            for i, x in enumerate(d)}


def test_enters_on_wide_basis_and_exits_when_it_reverts():
    d = ds(60)
    p = {x: 100.0 for x in d}
    q = stable_q(d, p, d[59])
    normal = q[d[31]]
    q[d[30]] = q[d[30]] + 1.0                                         # se ensancha: z > 1
    tr = bm.trades(q, p, {}, {exp_ms(d[59]): 100.0}, cost=0.0)
    t = next(x for x in tr if x["entry"] == d[30])
    assert t["side"] == 1 and t["exit"] == d[31]
    assert t["net_pct"] == pytest.approx((q[d[30]] - normal) / 100 * 100)   # corto Q gana la reversión


def test_costs_and_exit_before_expiry():
    d = ds(40)
    p = {x: 100.0 for x in d}
    q = stable_q(d, p, d[36])
    for x in d[30:]:
        q[x] = q[x] + 1.0                                             # se ensancha y no revierte
    tr = bm.trades(q, p, {}, {exp_ms(d[36]): 100.0})
    t = next(x for x in tr if x["entry"] == d[30])
    assert (datetime.fromisoformat(d[36]) - datetime.fromisoformat(t["exit"])).days <= bm.EXIT_DTE + 1
    assert t["net_pct"] < -4 * bm.COST * 100 + 0.5                    # pierde las 4 comisiones (y la deriva)
