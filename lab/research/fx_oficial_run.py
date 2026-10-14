"""Corre las rutas oficial -> USDT -> ARS sobre las capturas (solo investigación).

Uso: python -m lab.research.fx_oficial_run capturas.jsonl p2p_usd_foto.json salida.json
Los anuncios P2P en USD se toman de cada captura; si la captura no los tiene
(versión anterior del capturador), de la foto única `p2p_usd_foto.json`.
"""
import json
import sys
from collections import defaultdict

from lab.research import fx_oficial as fx
from lab.research.fx_oficial import Ad, Route

caps = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
p2p_usd = json.load(open(sys.argv[2], encoding="utf-8"))
usd_buy_ar = [Ad(a["price"], a["qty"], a["min"], a["max"], a["methods"], a["user"], a["rate"])
              for a in p2p_usd["ads"]["BUY_AR"]]

AMOUNTS = [150_000, 500_000, 1_500_000, 5_000_000, 15_000_000]


def routes(snap):
    bancos = (snap.get("criptoya_bancos") or {}).get("data") or {}
    da = (snap.get("dolarapi") or {}).get("data") or []
    bna = next((x["venta"] for x in da if x.get("casa") == "oficial"), 1535.0)
    cu = (snap.get("criptoya_usdt_usd") or {}).get("data") or {}
    out = [
        Route("A BNA -> P2P USD (transferencia bancaria) -> Binance spot", "BNA", bna, "p2p",
              usable_methods=["BankArgentina"], hours=(0.5, 48)),
        Route("A' BNA -> P2P USD -> P2P ARS", "BNA", bna, "p2p", usable_methods=["BankArgentina"],
              sell_on="p2p", hours=(1, 48)),
        Route("B Naranja X -> P2P USD (medio NaranjaX) -> Binance spot", "NaranjaX", bna, "p2p",
              usable_methods=["NaranjaX"], hours=(0.5, 48)),
        Route("D Mercado Pago (USD solo a cuentas propias) -> P2P", "MercadoPago", bna, "p2p",
              usable_methods=[], hours=(None, None)),
    ]
    for venue in ("fiwind", "belo", "decrypto", "letsbit", "ripio", "satoshitango", "tiendacrypto"):
        v = cu.get(venue)
        if isinstance(v, dict) and v.get("totalAsk"):
            out.append(Route(f"E BNA -> {venue} (recibe USD; cotización INDICATIVA CriptoYa) -> Binance spot",
                             "BNA", bna, "platform", platform_usdt_ask=v["totalAsk"], hours=(1, 72)))
    return out


res = defaultdict(lambda: defaultdict(list))
for snap in caps:
    d = (snap.get("binance_usdtars") or {}).get("data") or {}
    bids = [(float(p), float(q)) for p, q in d.get("bids", [])]
    sell_ads = fx.ads_from_capture((snap.get("p2p_usdt_ars_sell") or {}).get("data"))
    usd_ads = fx.ads_from_capture((snap.get("p2p_usdt_usd_buy_ar") or {}).get("data")) or usd_buy_ar
    if not bids:
        continue
    for r in routes(snap):
        for a in AMOUNTS:
            o = fx.simulate(r, a, usd_ads=usd_ads, ars_sell_ads=sell_ads, binance_bids=bids)
            res[r.name][a].append(o)

summary = {}
for name, by in res.items():
    summary[name] = {}
    for a, lst in by.items():
        ok = [o["net_pct"] for o in lst if o["net_pct"] is not None]
        st = defaultdict(int)
        for o in lst:
            st[o["status"]] += 1
        summary[name][a] = {"n": len(lst), "status": dict(st),
                            "net_pct_min": min(ok) if ok else None,
                            "net_pct_median": sorted(ok)[len(ok) // 2] if ok else None,
                            "net_pct_max": max(ok) if ok else None, "positive": sum(x > 0 for x in ok),
                            "paid_usd_per_usdt_median": sorted(o.get("paid_usd_per_usdt") or 0 for o in lst)[len(lst) // 2],
                            "breakeven_usd_per_usdt_median": sorted(o.get("breakeven_usd_per_usdt") or 0 for o in lst)[len(lst) // 2],
                            "example": lst[-1]}
json.dump(summary, open(sys.argv[3], "w", encoding="utf-8"), indent=1, default=str)
for name, by in summary.items():
    print(name)
    for a, s in by.items():
        f = lambda x: "n/d" if x is None else f"{x:+.2f}%"
        print(f"   {a:>11,} ARS  {s['status']}  neto min {f(s['net_pct_min'])} med {f(s['net_pct_median'])} "
              f"max {f(s['net_pct_max'])}  pos {s['positive']}/{s['n']}  pagado {s['paid_usd_per_usdt_median']:.4f} "
              f"equilibrio {s['breakeven_usd_per_usdt_median']:.4f}")
