import math
import random

import pytest

from lab import discovery as d

FROZEN_HASH = "364c1500b2be78e48f4b6b2841fd612044f3f9f955c166568e538b4c80a96364"


def random_walk(n, seed):
    rng = random.Random(seed)
    p = [100.0]
    for _ in range(n - 1):
        p.append(p[-1] * math.exp(rng.gauss(0, 0.01)))
    return p


def planted_momentum(n, seed=5):
    """Retornos con autocorrelación positiva fuerte: el momentum es real."""
    rng = random.Random(seed)
    p, r = [100.0], 0.0
    for _ in range(n - 1):
        r = 0.6 * r + rng.gauss(0, 0.01)
        p.append(p[-1] * math.exp(r))
    return p


def test_criteria_are_frozen():
    # Cambiar los criterios exige actualizar este hash a mano (revisión explícita).
    assert d.CRITERIA_HASH == FROZEN_HASH


def test_random_walks_produce_no_promotions_after_global_bh():
    hyps = []
    for i in range(5):
        hyps += d.momentum_hypotheses(f"A{i}", random_walk(3000, seed=i))
    res = d.run_discovery(hyps)
    assert res["funnel"]["tested"] == 5 * 18
    assert res["funnel"]["promoted"] == 0


def test_planted_signal_is_found_without_costs(monkeypatch):
    monkeypatch.setattr(d, "FEE", 0.0)
    monkeypatch.setattr(d, "SLIP", 0.0)
    res = d.run_discovery(d.momentum_hypotheses("X", planted_momentum(4000)))
    promoted = [r for r in res["results"] if r["promoted"]]
    assert promoted and all(r["params"]["mode"] == "momentum" for r in promoted)


def test_costs_can_remove_the_planted_signal(monkeypatch):
    monkeypatch.setattr(d, "FEE", 0.02)
    res = d.run_discovery(d.momentum_hypotheses("X", planted_momentum(4000)))
    assert res["funnel"]["promoted"] == 0


def test_thresholds_come_only_from_training():
    base = planted_momentum(3000)
    h1 = d.momentum_hypotheses("X", base)
    altered = base[:]
    (_, _), (_, _), (t0, _) = d.splits(len(base))
    for i in range(t0, len(altered)):
        altered[i] *= 1.5 if i % 2 else 0.7          # destruir solo el tramo de prueba
    h2 = d.momentum_hypotheses("X", altered)
    assert [h["params"]["threshold_from_train"] for h in h1] == \
        [h["params"]["threshold_from_train"] for h in h2]


def test_every_hypothesis_is_recorded_including_failures(tmp_path):
    reg = d.Registry(tmp_path / "disc.sqlite")
    hyps = d.momentum_hypotheses("A", random_walk(2000, 1))
    ext = [d.external_hypothesis("pair|X~Y", "pares", 0.5, 40, 0, 0.0, 0.0)]
    res = d.run_discovery(hyps, ext, registry=reg, run_id="r1")
    assert reg.count("r1") == len(hyps) + 1 == res["funnel"]["tested"]
    assert all(r["failed_at"] for r in res["results"] if not r["promoted"])


def test_external_studies_enter_the_global_multiplicity_correction():
    hyps = d.momentum_hypotheses("A", random_walk(2000, 2))
    ext = d.external_hypothesis("e", "pares", 0.008, 40, 40, 1.0, 0.5)
    # Sola, p=0.008 pasa BH (q=0.10); junto a 18 hipótesis más, el umbral del
    # rango 1 es 0.10/19 = 0.0053 y ya no pasa: la multiplicidad se corrige.
    assert d.decide([dict(ext)])[0]["bh_train"] is True
    res = d.run_discovery(hyps, [dict(ext)])
    e = next(r for r in res["results"] if r["id"] == "e")
    assert res["funnel"]["tested"] == 19
    assert e["bh_train"] is False and not e["promoted"]


def test_funding_hypotheses_include_funding_payments():
    n = 600
    perp = [100.0] * n
    funding = {i: (0.001 if i % 80 == 0 else 0.0001) for i in range(0, n, 8)}
    hyps = d.funding_hypotheses("binance|BTC", perp, funding)
    h = next(x for x in hyps if x["params"]["mode"] == "contrarian" and x["params"]["h"] == 8)
    tr = h["trades_fn"](0, n)
    # precio plano: el resultado bruto es solo el funding cobrado por el short
    assert tr and all(t["gross"] >= 0 for t in tr)
