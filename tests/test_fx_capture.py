"""Captura cambiaria: páginas P2P, identificación del anunciante y perfiles (sin red)."""

from lab.research import fx_capture as fc


class Resp:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def raw_ad(price, user_no):
    return {"adv": {"price": str(price), "tradableQuantity": "10", "minSingleTransAmount": "1000",
                    "maxSingleTransAmount": "50000", "tradeMethods": [{"identifier": "MercadoPagoNew"}],
                    "payTimeLimit": 15, "classify": "profession", "takerAdditionalKycRequired": 0},
            "advertiser": {"userType": "merchant", "monthOrderCount": 900, "monthFinishRate": 0.99,
                           "positiveRate": 0.99, "userNo": user_no, "nickName": "n" + user_no}}


def test_p2p_reads_several_pages_and_keeps_user_no(monkeypatch):
    calls = []

    def post(url, timeout, json):
        calls.append(json["page"])
        rows = [raw_ad(1600 + i, f"u{json['page']}{i}") for i in range(20 if json["page"] < 2 else 5)]
        return Resp({"data": rows})

    monkeypatch.setattr(fc.S, "post", post)
    out = fc.p2p("BUY", pages=3)["data"]
    assert calls == [1, 2]                     # la página 2 vino incompleta: no pide la 3
    assert len(out) == 25 and out[0]["user_no"] == "u10" and out[-1]["page"] == 2
    assert out[0]["user_type"] == "merchant" and out[0]["classify"] == "profession"


def test_profiles_fetched_once_per_process(monkeypatch):
    fc._seen_profiles.clear()
    got = []

    def get(url, params, timeout):
        got.append(params["userNo"])
        return Resp({"data": {"userDetailVo": {"kycStatus": "PASS", "userStatsRet": {
            "registerDays": 900, "avgReleaseTimeOfLatest30day": 80.0, "completedOrderNum": 5000}}}})

    monkeypatch.setattr(fc.S, "get", get)
    a = fc.profiles(["x", "y", None, "x"])["data"]
    b = fc.profiles(["x", "z"])["data"]
    assert got == ["x", "y", "z"] and set(a) == {"x", "y"} and set(b) == {"z"}
    assert a["x"]["avgReleaseTimeOfLatest30day"] == 80.0 and a["x"]["kycStatus"] == "PASS"
