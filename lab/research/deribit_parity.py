"""C3 (BIBLIOTECA_HULL_ESTRATEGIAS_2026-10-16.md): box spread y límites con precios ejecutables de Deribit.

Box (Hull EN 11.3; BS 11.1): comprar call K1, vender call K2, comprar put K2,
vender put K1 (K1 < K2, mismo vencimiento europeo) paga K2 − K1 USD al vencer
(Deribit liquida en BTC al precio de entrega: el valor en USD es fijo).
Costo hoy = (ask C1 − bid C2 + ask P2 − bid P1) en BTC × índice, + comisiones.
Tasa implícita = ((K2−K1)·q / costo)^(365/días) − 1 (préstamo vía box).
Vender el box (lo inverso) equivale a pedir prestado.
Comisiones (SUPUESTO, ver P5): 0,04% del subyacente por pata con tope 12,5% de la
prima; entrega 0,015% en las patas que vencen dentro del dinero (2 de 4).
Oportunidad: tasa neta del préstamo > letra del mismo plazo, persistente
(≥ 2 capturas seguidas). Límite: violación de cotas (call ask < max(0, S−K)·factor, etc.).
Capital ≤ US$1.000 por box (q = 0,1 BTC, el mínimo de Deribit).
"""

import json
import time
from datetime import datetime, timezone

Q = 0.1
FEE, CAP, DFEE = 0.0004, 0.125, 0.00015


def parse(name):
    _, exp, k, cp = name.split("-")
    return exp, int(k), cp


def expiry_dt(code):
    return datetime.strptime(code, "%d%b%y").replace(hour=8, tzinfo=timezone.utc)


def tb_rate(tbill_pct, days):
    return tbill_pct / 100 * days / 360


def fee_btc(p):
    return min(FEE * Q, CAP * p * Q) if p > 0 else FEE * Q


def boxes(summary, index_usd, now, tbill_pct, max_capital=1000.0):
    """summary: filas de get_book_summary_by_currency (opciones). -> lista de boxes evaluados."""
    q = {}
    for r in summary:
        exp, k, cp = parse(r["instrument_name"])
        if r.get("bid_price") and r.get("ask_price"):
            q[(exp, k, cp)] = (r["bid_price"], r["ask_price"])
    by_exp = {}
    for (exp, k, cp) in q:
        if (exp, k, "C") in q and (exp, k, "P") in q:
            by_exp.setdefault(exp, set()).add(k)
    out = []
    for exp, ks in by_exp.items():
        days = (expiry_dt(exp) - now).total_seconds() / 86400
        if days < 1:
            continue
        ks = sorted(ks)
        for i, k1 in enumerate(ks):
            for k2 in ks[i + 1:]:
                c1b, c1a = q[(exp, k1, "C")]
                c2b, c2a = q[(exp, k2, "C")]
                p1b, p1a = q[(exp, k1, "P")]
                p2b, p2a = q[(exp, k2, "P")]
                legs = [c1a, c2b, p2a, p1b]
                cost_btc = (c1a - c2b + p2a - p1b) * Q + sum(fee_btc(x) for x in legs)
                cost_usd = cost_btc * index_usd
                pay = (k2 - k1) * Q
                if cost_usd <= 0 or cost_usd > max_capital:
                    continue
                pay_net = pay - 2 * DFEE * Q * index_usd          # 2 patas dentro del dinero al vencer
                period = pay_net / cost_usd - 1
                tb = tbill_pct / 100 * days / 360
                # lado inverso: VENDER el box (recibir hoy, pagar K2−K1 al vencer). Es arbitraje
                # si lo recibido supera el valor presente del pago a la tasa de la letra
                proceeds_usd = ((c1b - c2a + p2b - p1a) * Q - sum(fee_btc(x) for x in (c1b, c2a, p2b, p1a))) * index_usd
                sell_edge_pct = (proceeds_usd - (pay + 2 * DFEE * Q * index_usd) / (1 + tb_rate(tbill_pct, days))) / pay * 100
                out.append({"expiry": exp, "days": days, "k1": k1, "k2": k2, "cost_usd": cost_usd,
                            "sell_proceeds_usd": proceeds_usd, "sell_edge_pct": sell_edge_pct,
                            "payoff_usd": pay, "period_ret_pct": period * 100,
                            "ann_rate_pct": ((1 + period) ** (365 / days) - 1) * 100 if period > -1 else None,
                            "excess_vs_tbill_pct": (period - tb) * 100})
    return out


def capture(s):
    t = datetime.now(timezone.utc)
    opts = s.get("https://www.deribit.com/api/v2/public/get_book_summary_by_currency",
                 params={"currency": "BTC", "kind": "option"}, timeout=30).json()["result"]
    idx = s.get("https://www.deribit.com/api/v2/public/get_index_price",
                params={"index_name": "btc_usd"}, timeout=30).json()["result"]["index_price"]
    return {"ts": t.isoformat(timespec="seconds"), "index": idx,
            "options": [{k: r.get(k) for k in ("instrument_name", "bid_price", "ask_price", "mark_price",
                                                "underlying_price")} for r in opts]}


def main():
    """python -m lab.research.deribit_parity SALIDA.jsonl HORAS INTERVALO_S (solo lectura)."""
    import sys
    import requests
    out, hours, step = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    s = requests.Session()
    end = time.time() + hours * 3600
    while time.time() < end:
        t0 = time.time()
        try:
            snap = capture(s)
        except Exception as e:                       # se registra; no se rellena
            snap = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "error": str(e)[:200]}
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(snap) + "\n")
        time.sleep(max(0.0, step - (time.time() - t0)))


if __name__ == "__main__":
    main()
