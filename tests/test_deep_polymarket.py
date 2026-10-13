"""Fase de investigación profunda: libros completos de Polymarket y diagnóstico
de los casos NO_BOOK_FOR_LEG."""

from lab.research.pm_gaps import diagnose_run, diagnose_snapshot, leg_cause
from lab.sources import CclSource, PolymarketSource
from tests.lab_fixtures import snap
from tests.test_lab_prediction_basis import no_book, pm_event


class FakeResp:
    def __init__(self, payload, status=200):
        self.payload, self.status_code = payload, status

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeClob:
    """POST /books devuelve los libros DESORDENADOS y omite los de `drop`."""

    def __init__(self, drop=(), fail_batch=False):
        self.drop, self.fail_batch = set(drop), fail_batch
        self.posts, self.gets = [], []

    @staticmethod
    def _raw(t):
        return {"asset_id": t, "bids": [{"price": "0.40", "size": "5"}],
                "asks": [{"price": "0.45", "size": "7"}, {"price": "0.42", "size": "3"}],
                "timestamp": "1", "hash": "h"}

    def post(self, url, json=None, timeout=None):
        self.posts.append([x["token_id"] for x in json])
        if self.fail_batch:
            return FakeResp({"error": "boom"}, 500)
        return FakeResp([self._raw(x["token_id"]) for x in reversed(json)
                         if x["token_id"] not in self.drop])

    def get(self, url, params=None, timeout=None):
        t = params["token_id"]
        self.gets.append(t)
        if t in self.drop:
            return FakeResp({}, 404)
        return FakeResp(self._raw(t))


def test_batch_books_map_by_asset_id_and_never_truncate_silently():
    toks = [f"T{i}" for i in range(254)]                 # el caso real: 254 > tope viejo 200
    clob = FakeClob()
    books, errs = PolymarketSource(session=clob, batch_size=100).fetch_books(toks)
    assert set(books) == set(toks) and errs == []
    assert len(clob.posts) == 3 and not clob.gets          # 3 lotes, sin pedidos sueltos
    assert books["T0"]["asks"][0] == [0.42, 3.0]           # ordenado: mejor ask primero


def test_truncation_is_logged_as_error_with_dropped_tokens():
    toks = [f"T{i}" for i in range(12)]
    books, errs = PolymarketSource(session=FakeClob(), max_books=10, batch_size=4).fetch_books(toks)
    assert len(books) == 10
    (e,) = errs
    assert e["error"] == "TRUNCATED" and e["dropped"] == ["T10", "T11"]


def test_missing_from_batch_is_refetched_and_404_is_recorded():
    clob = FakeClob(drop={"T1"})
    books, errs = PolymarketSource(session=clob).fetch_books(["T0", "T1"])
    assert set(books) == {"T0"} and clob.gets == ["T1"]
    assert errs[0]["token"] == "T1" and "404" in errs[0]["error"]


def test_failed_batch_falls_back_to_single_requests():
    clob = FakeClob(fail_batch=True)
    books, errs = PolymarketSource(session=clob).fetch_books(["A", "B"])
    assert set(books) == {"A", "B"} and errs[0]["what"] == "books_batch"


def _gap_snapshot(tick=0):
    e = pm_event([0.5, 0.52], slug="ev")                  # tokens N0, N1
    s = snap({}, tick=tick, polymarket={"events": [e], "books": {"N0": no_book(0.49)}})
    return s


def test_leg_cause_classification():
    req = ["a", "b", "c"]
    assert leg_cause("a", {"a": {"asks": [[1, 1]]}}, req, {}) == "PRESENTE"
    assert leg_cause("a", {"a": {"asks": []}}, req, {}) == "LIBRO_SIN_ASKS"
    assert leg_cause("c", {}, req, {}, cap=2) == "RECORTADO_POR_TOPE"
    assert leg_cause("b", {}, req, {"b": "HTTP 404 (sin libro)"}, cap=2) == "SIN_LIBRO_404"
    assert leg_cause("b", {}, req, {"b": "Timeout"}, cap=2) == "ERROR_RED"
    assert leg_cause("z", {}, req, {}) == "NUNCA_PEDIDO"


def test_gap_cases_are_never_classified_as_opportunities():
    (c,) = diagnose_snapshot(_gap_snapshot(), cap=1)
    assert c["missing"] == [{"token": "N1", "cause": "RECORTADO_POR_TOPE"}]
    assert c["status"] == "NO_RECUPERABLE"
    assert c["gross_top_gamma_indicative"] > 0          # indicativo, no cambia el estado
    r = diagnose_run([_gap_snapshot(0), _gap_snapshot(1)], cap=1)
    assert r["cases"] == 2 and r["by_event"]["polymarket|ev"]["first_tick"] == 0


class FakeData912:
    def get(self, url, timeout=None):
        ep = url.rsplit("/", 1)[-1]
        if ep == "ccl":
            return FakeResp({"oops": 1}, 503)
        rows = {"arg_stocks": [{"symbol": "GGAL", "px_bid": 1}, {"symbol": "XXXX", "px_bid": 2}],
                "usa_adrs": [{"symbol": "GGAL", "px_bid": 3}]}[ep]
        return FakeResp(rows)


def test_ccl_source_keeps_only_listed_tickers_and_records_errors():
    out, errs = CclSource(session=FakeData912(), use=("data912",)).fetch()
    assert set(out["arg_stocks"]) == {"GGAL"} and set(out["usa_adrs"]) == {"GGAL"}
    assert "ccl" not in out and errs[0]["what"] == "ccl"
