import logging

import pytest

from funding.config import ASSUMED, FundingConfig, Param
from funding.live import LiveRunner, evaluate_snapshot
from funding.storage import Storage

H = 3_600_000
LOG = logging.getLogger("test")


def book(spot=100.0, perp=100.0, size=10.0):
    return {"spot_bids": [[spot - 0.01, size]], "spot_asks": [[spot + 0.01, size]],
            "perp_bids": [[perp - 0.01, size]], "perp_asks": [[perp + 0.01, size]]}


class FakeAdapter:
    name = "binance"

    def __init__(self, rate):
        self.rate = rate

    def market_info(self, asset):
        return {"spot": {"ccxt_taker_fee": 0.001}, "perp": {"ccxt_taker_fee": 0.0005}}

    def min_qty(self, asset):
        return {"spot_min_qty": 0.0, "spot_min_cost": 0.0,
                "perp_min_qty": 0.0, "perp_min_cost": 0.0}

    def fetch_funding_history(self, asset, since):
        return [(i * 8 * H, self.rate) for i in range(10)]

    def fetch_funding_now(self, asset):
        return {"rate": self.rate, "next_ts": 10**15, "interval_h": 8.0,
                "mark": 100.0, "index": 100.0}


class SequenceBooks:
    """Devuelve libros distintos en cada llamada: detecta si se re-pide tras latencia."""

    def __init__(self, seq):
        self.seq, self.calls = list(seq), 0

    def get(self, ex, asset, limit=50):
        self.calls += 1
        return self.seq[min(self.calls - 1, len(self.seq) - 1)]

    def close(self):
        pass


def cfg(**kw):
    base = dict(assets=("BTC",), exchanges=("binance",),
                leg_fail_prob=Param(0.0, ASSUMED, "test"), horizon_days=7)
    base.update(kw)
    return FundingConfig(**base)


def runner(tmp_path, rate, books, **kw):
    sleeps = []
    r = LiveRunner(cfg(**kw), {"binance": FakeAdapter(rate)}, Storage(tmp_path / "f.sqlite"),
                   books, LOG, seed=1, sleep=sleeps.append)
    return r, sleeps


def test_snapshot_records_all_fields_and_costs():
    s = evaluate_snapshot(books=book(perp=100.2), funding_now={"rate": 0.0001, "mark": 100,
                          "index": 100, "next_ts": 1}, trailing_rates=[0.0001] * 3,
                          cfg=cfg(), exchange="binance", notional=45, interval_h=8)
    for k in ("spot_bid", "spot_ask", "perp_bid", "perp_ask", "mark", "index_price",
              "funding_rate", "funding_interval_h", "next_funding_ts", "basis_pct",
              "cost_pct", "expected_net_pct", "capital_required", "margin",
              "leverage", "liq_distance", "risks", "annualized_net_pct"):
        assert k in s
    assert s["leverage"] == 1.0 and s["capital_required"] == 90
    assert s["expected_net_pct"] < 0          # funding normal no cubre costos


def test_conservative_expected_rate_uses_lower_of_now_and_trailing():
    s = evaluate_snapshot(books=book(), funding_now={"rate": 0.01}, trailing_rates=[0.0001] * 3,
                          cfg=cfg(), exchange="binance", notional=45, interval_h=8)
    assert s["expected_rate"] == 0.0001


def test_no_opportunity_no_paper(tmp_path):
    r, sleeps = runner(tmp_path, 0.0001, SequenceBooks([book()]))
    res = r.tick()
    assert res[("binance", "BTC")]["expected_net_pct"] < 0
    assert not r.state.ledger.open and sleeps == []
    assert r.storage.count("opportunities") == 0 and r.storage.count("snapshots") == 1


def test_latency_refetches_book_and_fills_on_the_new_one(tmp_path):
    # Funding muy alto -> oportunidad. El libro tras la latencia está peor.
    books = SequenceBooks([book(spot=100.0), book(spot=101.0)])
    r, sleeps = runner(tmp_path, 0.003, books)
    r.tick()
    assert sleeps == [0.5]                        # 500 ms de latencia configurada
    assert books.calls == 2                       # se volvió a pedir el libro
    pos = r.state.ledger.open["binance:BTC"]
    assert pos.spot_entry == pytest.approx(101.01)   # llenó con el libro posterior
    assert r.state.ledger.locked > 0
    assert r.storage.count("paper_events", "event='OPEN'") == 1


def test_opportunity_appears_and_disappears(tmp_path):
    r, _ = runner(tmp_path, 0.003, SequenceBooks([book()]))
    r.tick()
    assert r.storage.open_opportunity_id("binance", "BTC") is not None
    r.adapters["binance"].rate = -0.003             # el funding se da vuelta
    r.meta[("binance", "BTC")]["rates"] = [-0.003] * 3
    r.tick()
    assert r.storage.open_opportunity_id("binance", "BTC") is None
    closed = r.storage.db.execute("SELECT closed_at FROM opportunities").fetchone()[0]
    assert closed is not None
    # y la posición paper se cerró por funding negativo
    assert r.storage.count("paper_events", "event='CLOSE'") == 1
    assert not r.state.ledger.open


def test_pair_error_is_logged_not_raised(tmp_path):
    class Broken(FakeAdapter):
        def fetch_funding_now(self, asset):
            raise ConnectionError("caído")
    r = LiveRunner(cfg(), {"binance": Broken(0.0)}, Storage(tmp_path / "f.sqlite"),
                   SequenceBooks([book()]), LOG, sleep=lambda s: None)
    assert r.tick() == {}
    assert r.storage.count("errors") == 1


def test_infeasible_min_size_does_not_open(tmp_path):
    class BigMin(FakeAdapter):
        def min_qty(self, asset):
            return {"spot_min_qty": 0, "spot_min_cost": 0, "perp_min_qty": 1.0,
                    "perp_min_cost": 50}
    r = LiveRunner(cfg(), {"binance": BigMin(0.003)}, Storage(tmp_path / "f.sqlite"),
                   SequenceBooks([book()]), LOG, sleep=lambda s: None)
    res = r.tick()[("binance", "BTC")]
    assert res["expected_net_pct"] > 0 and res["feasible_100usd"] is False
    assert not r.state.ledger.open


def test_regression_okx_perp_book_converted_from_contracts_to_asset_units():
    # OKX publica el libro del perp en contratos (ctVal 0.01 BTC). Sin convertir,
    # la profundidad quedaba 100x inflada.
    from funding.adapters.okx import OkxAdapter

    class FakeOkx:
        apiKey = ""

        def load_markets(self):
            pass

        def market(self, sym):
            return {"contractSize": 0.01 if ":" in sym else None}

        def fetch_order_book(self, sym, limit=None):
            return {"bids": [[100.0, 50.0]], "asks": [[101.0, 30.0]], "timestamp": 1}

    b = OkxAdapter(exchange=FakeOkx()).fetch_books("BTC")
    assert b["perp_bids"] == [[100.0, 0.5]] and b["perp_asks"] == [[101.0, 0.3]]
    assert b["spot_bids"] == [[100.0, 50.0]]          # spot ya viene en BTC


def test_adapter_rejects_api_keys_and_trading():
    from funding.adapters.base import PaperOnlyError
    from funding.adapters.binance import BinanceAdapter

    class WithKey:
        apiKey = "x"
    with pytest.raises(AssertionError):
        BinanceAdapter(exchange=WithKey())

    class NoKey:
        apiKey = ""
    a = BinanceAdapter(exchange=NoKey())
    with pytest.raises(PaperOnlyError):
        a.create_order("BTC/USDT", "market", "buy", 1)
    with pytest.raises(PaperOnlyError):
        a.withdraw("USDT", 1, "addr")


def test_regression_okx_ws_uses_public_depth():
    # OKX con profundidad 50 pedía login por WebSocket (verificado en vivo).
    from funding.adapters.binance import BinanceAdapter
    from funding.adapters.okx import OkxAdapter
    assert OkxAdapter.ws_depth(OkxAdapter.__new__(OkxAdapter), 50) is None
    assert BinanceAdapter.ws_depth(BinanceAdapter.__new__(BinanceAdapter), 50) == 50
