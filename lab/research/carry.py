"""Cash-and-carry histórico con futuros trimestrales de Binance (USDⓈ-M).

Para cada hora con cierre de spot (S) y de futuro trimestral (F) se simula:
  entrada   comprar spot y vender el futuro (con costos y medio spread),
  vencimiento  el futuro liquida contra el precio de entrega publicado por
            Binance (promedio del índice), el spot se vende al cierre de la
            hora de entrega: el desvío spot vs precio de entrega es REAL,
            medido, no supuesto,
  salida anticipada  cerrar ambas patas antes (25/50/75% del plazo),
  margen    el corto necesita garantía; se mide la suba máxima del futuro
            durante la tenencia y si habría liquidación (sin reponer) o
            cuánto capital extra habría hecho falta, con 1x/2x/3x.
Comparación: letra del Tesoro de EE.UU. a 3 meses (FRED DTB3) por el mismo
plazo. NO se anualiza; se compara el rendimiento del período contra el de la
letra en ese mismo período.

Limitaciones: velas horarias (cierres de operaciones, no puntas ejecutables;
se agrega el medio spread medido en libros reales), un solo exchange, y las
comisiones son las públicas de nivel base (no verificadas por cuenta).
"""

import bisect
import calendar
import csv
import io
from datetime import datetime, timezone

from .stats import mean

HOUR = 3_600_000
SPOT_TAKER = 0.0010         # ASSUMED: Binance spot nivel base
FUT_TAKER = 0.0005          # ASSUMED: Binance USDⓈ-M nivel base (taker 0,05%)
SETTLE_FEE = 0.0005         # ASSUMED: la entrega se cobra a tasa taker (Binance)
HALF_SPREAD = {"spot": 0.000002, "fut": 0.000035}   # ESTIMADO: mitad del spread medido
MMR = 0.005                 # ASSUMED: margen de mantenimiento nivel 1 (no público sin clave)
LEVERAGES = (1, 2, 3)
FEE_MULT = [1.0]            # sensibilidad: multiplica TODAS las comisiones (ver fee_scale)
EXIT_FRACTIONS = (0.25, 0.5, 0.75)
MAX_ABS_BASIS = 0.20        # |base| > 20%: error de datos (p. ej. continuo sin contrato), se excluye
DATA_EXCLUSIONS = {}        # motivo -> cantidad (se reinicia en cada simulate)


# ------------------------------------------------------------------ datos

def last_friday_8utc(year, month):
    last = calendar.monthrange(year, month)[1]
    d = datetime(year, month, last, 8, tzinfo=timezone.utc)
    while d.weekday() != 4:
        d = d.replace(day=d.day - 1)
    return int(d.timestamp() * 1000)


def quarterly_expiries(start_year, end_year):
    return [last_friday_8utc(y, m) for y in range(start_year, end_year + 1) for m in (3, 6, 9, 12)]


def binance_klines_fetcher(session, url, params):
    """Paginado de velas REST de Binance (público)."""
    def fetch(since, until):
        out, cursor = {}, since
        for _ in range(500):
            r = session.get(url, params={**params, "startTime": cursor, "endTime": until,
                                         "limit": 1500}, timeout=30)
            r.raise_for_status()
            rows = r.json()
            fresh = [x for x in rows if x[0] not in out]
            if not fresh:
                break
            for x in fresh:
                out[x[0]] = (x[0], float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5]))
            last = max(x[0] for x in fresh)
            if last + HOUR > until:
                break
            cursor = last + 1
        return [out[k] for k in sorted(out)]
    return fetch


def fred_dtb3(session):
    """Tasa de descuento de la letra a 3 meses (% anual), por fecha ISO."""
    r = session.get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3", timeout=30)
    r.raise_for_status()
    out = {}
    for row in csv.reader(io.StringIO(r.text)):
        if len(row) == 2 and row[1] not in ("", ".", "DTB3"):
            try:
                out[row[0]] = float(row[1])
            except ValueError:
                pass
    return out


def rate_at(rates_by_date, ts_ms):
    """Última tasa publicada a la fecha (sin mirar el futuro)."""
    if not rates_by_date:
        return None
    keys = sorted(rates_by_date)
    d = datetime.fromtimestamp(ts_ms / 1000, timezone.utc).date().isoformat()
    i = bisect.bisect_right(keys, d) - 1
    return rates_by_date[keys[i]] if i >= 0 else None


def tbill_period_return(rate_pct, days):
    """Rendimiento de comprar la letra con descuento d por `days` días (base 360)."""
    d = rate_pct / 100 * days / 360
    return d / (1 - d) if d < 1 else None


# ------------------------------------------------------------------ simulación

class fee_scale:
    """with fee_scale(1.5): ... -> comisiones x1.5 (el spread medido no se escala)."""

    def __init__(self, m):
        self.m = m

    def __enter__(self):
        FEE_MULT.append(self.m)

    def __exit__(self, *a):
        FEE_MULT.pop()


def _st():
    return SPOT_TAKER * FEE_MULT[-1] + HALF_SPREAD["spot"]


def _ft():
    return FUT_TAKER * FEE_MULT[-1] + HALF_SPREAD["fut"]


def entry_costs(s, f):
    return s * _st() + f * _ft()


def hold_to_expiry(s0, f0, spot_exit, delivery):
    """Neto por unidad manteniendo hasta la entrega. -> dict."""
    gross_locked = f0 - s0                          # base fijada al entrar
    index_dev = spot_exit - delivery                # spot real vs precio de entrega
    costs = entry_costs(s0, f0) + spot_exit * _st() + delivery * SETTLE_FEE * FEE_MULT[-1]
    return {"gross_locked": gross_locked, "index_dev": index_dev, "costs": costs,
            "net": gross_locked + index_dev - costs}


def early_exit(s0, f0, s1, f1):
    """Cerrar las dos patas antes del vencimiento (vender spot, recomprar futuro)."""
    costs = entry_costs(s0, f0) + s1 * _st() + f1 * _ft()
    return (f0 - s0) - (f1 - s1) - costs


def ex_ante_net(s0, f0):
    return (f0 - s0) - entry_costs(s0, f0) - s0 * _st() - s0 * SETTLE_FEE * FEE_MULT[-1]


def rule_eval(recs):
    """Regla fija, sin parámetros ajustados: entrar SOLO si el exceso ex ante
    sobre la letra es > 0. Se mide el exceso REALIZADO (incluye el desvío real
    del spot vs el precio de entrega). Mitad cronológica 1 vs 2 por contratos."""
    taken = [r for r in recs if r.get("ex_ante_excess_1x") is not None and r["ex_ante_excess_1x"] > 0]
    exps = sorted({r["expiry"] for r in recs})
    cut = exps[len(exps) // 2] if exps else None

    def stats(rs):
        ex = [r["excess_1x"] for r in rs]
        return {"entries": len(rs), "contracts": len({r["expiry"] for r in rs}),
                "realized_excess_mean": mean(ex) if ex else None,
                "realized_excess_min": min(ex) if ex else None,
                "share_realized_beats_tbill": (sum(e > 0 for e in ex) / len(ex)) if ex else None,
                "ret_1x_mean": mean([r["ret_1x"] for r in rs]) if rs else None,
                "liq_1x": sum(r["liq_1x"] for r in rs),
                "extra_1x_max_pct": max((r["extra_1x_pct"] for r in rs), default=0)}
    return {"rule": "exceso ex ante sobre la letra > 0 (1x)", "all": stats(taken),
            "first_half": stats([r for r in taken if cut and r["expiry"] < cut]),
            "second_half": stats([r for r in taken if cut and r["expiry"] >= cut]),
            "share_of_entries_taken": len(taken) / len(recs) if recs else None}


def margin_need(f0, max_fut, leverage, mmr=MMR):
    """Garantía inicial f0/L. -> (liquidado_sin_reponer, capital_extra_por_unidad)."""
    m = f0 / leverage
    loss = max(0.0, max_fut - f0)
    short = m - loss - mmr * max_fut               # garantía restante sobre el mantenimiento
    return short < 0, max(0.0, -short)


class ContractPrices:
    """Precio del contrato que vence en `exp` a la hora x: mientras es el
    trimestre siguiente está en el continuo NQ; después del roll, en CQ."""

    def __init__(self, series, expiries):
        self.series, self.expiries = series, expiries        # {"CQ": (closes, highs), "NQ": ...}

    def code(self, x, exp):
        i = bisect.bisect_right(self.expiries, x + HOUR)
        if i < len(self.expiries) and self.expiries[i] == exp:
            return "CQ"
        if i + 1 < len(self.expiries) and self.expiries[i + 1] == exp:
            return "NQ"
        return None

    def _traded(self, c, x):
        """Vela con volumen > 0. Sin operaciones el cierre es un precio viejo
        (en 2022 el continuo NQ repite 20955.0 durante meses): no es ejecutable."""
        vols = self.series[c][2] if len(self.series[c]) > 2 else None
        return vols is None or (vols.get(x) or 0) > 0

    def close(self, x, exp):
        c = self.code(x, exp)
        return self.series[c][0].get(x) if c and self._traded(c, x) else None

    def high(self, x, exp):
        c = self.code(x, exp)
        if not c or not self._traded(c, x):
            return None
        return self.series[c][1].get(x, self.series[c][0].get(x))


def simulate(spot, prices, deliveries, expiries, rates, step_hours=24, contract="CQ",
             index_exit=None):
    """spot: {ts_cierre: close}; prices: ContractPrices; deliveries: {expiry_ms:
    precio de entrega}; index_exit: {expiry_ms: precio de venta del spot al
    vencimiento} (TWAP de 1m de la media hora previa; si falta, cierre horario).
    contract CQ = entra en el trimestre corriente; NQ = en el siguiente.
    Entradas cada `step_hours` (horas consecutivas están muy correlacionadas)."""
    index_exit = index_exit or {}
    out, last_entry = [], None
    DATA_EXCLUSIONS.clear()
    for t in sorted(spot):
        if last_entry is not None and t - last_entry < step_hours * HOUR:
            continue
        i = bisect.bisect_right(expiries, t + HOUR)
        if i == 0:
            # antes de la primera entrega conocida no se sabe qué contrato
            # representa el continuo: no se evalúa
            k = "antes_de_primera_entrega_conocida"
            DATA_EXCLUSIONS[k] = DATA_EXCLUSIONS.get(k, 0) + 1
            continue
        j = i + (1 if contract == "NQ" else 0)
        if j >= len(expiries):
            continue
        exp = expiries[j]
        if exp not in deliveries or exp - t < 2 * 24 * HOUR:
            continue
        f0, s0 = prices.close(t, exp), spot[t]
        if f0 is None:
            DATA_EXCLUSIONS["futuro_sin_operaciones"] = DATA_EXCLUSIONS.get("futuro_sin_operaciones", 0) + 1
            continue
        if abs(f0 / s0 - 1) > MAX_ABS_BASIS:
            DATA_EXCLUSIONS["base_absurda"] = DATA_EXCLUSIONS.get("base_absurda", 0) + 1
            continue
        spot_exit = index_exit.get(exp) or spot.get(exp)
        if spot_exit is None:
            continue
        last_entry = t
        h = hold_to_expiry(s0, f0, spot_exit, deliveries[exp])
        days = (exp - t) / (24 * HOUR)
        highs = [prices.high(x, exp) for x in range(t, exp - HOUR, HOUR)]
        highs = [x for x in highs if x is not None]
        max_fut = max(highs or [f0])
        cap = {L: s0 + f0 / L for L in LEVERAGES}
        rate = rate_at(rates, t)
        tb = tbill_period_return(rate, days) if rate is not None else None
        rec = {"t": t, "expiry": exp, "contract": contract, "days": days, "s0": s0, "f0": f0,
               "basis_pct": f0 / s0 - 1, "delivery": deliveries[exp], "spot_exit": spot_exit,
               "spot_exit_kind": "TWAP_1m_30min" if exp in index_exit else "CIERRE_1h",
               "index_dev_pct": h["index_dev"] / deliveries[exp], **h,
               "tbill_rate_pct": rate, "tbill_period": tb,
               "excess_1x": (h["net"] / cap[1] - tb) if tb is not None else None,
               "max_rise_pct": max_fut / f0 - 1, "path_bars": len(highs)}
        # Lo que se conoce AL ENTRAR (sin mirar el futuro): base fijada menos
        # costos estimados con salida a s0, contra la letra del mismo plazo.
        ante = ex_ante_net(s0, f0)
        rec["ex_ante_net"] = ante
        rec["ex_ante_excess_1x"] = (ante / cap[1] - tb) if tb is not None else None
        for L in LEVERAGES:
            liq, extra = margin_need(f0, max_fut, L)
            rec[f"liq_{L}x"], rec[f"extra_{L}x_pct"] = liq, extra / cap[L]
            rec[f"ret_{L}x"] = h["net"] / cap[L]
        for fr in EXIT_FRACTIONS:
            u = t + int(fr * (exp - t) / HOUR) * HOUR
            f1 = prices.close(u, exp)
            if u in spot and f1 is not None:
                rec[f"early_{int(fr * 100)}"] = early_exit(s0, f0, spot[u], f1) / cap[1]
        out.append(rec)
    return out


def summarize(recs):
    """Por contrato (vencimiento) y global. Cada contrato es un período
    independiente; las entradas dentro de un contrato se solapan."""
    by = {}
    for r in recs:
        by.setdefault(r["expiry"], []).append(r)
    periods = []
    for exp, rs in sorted(by.items()):
        ex = [r["excess_1x"] for r in rs if r["excess_1x"] is not None]
        periods.append({
            "expiry": datetime.fromtimestamp(exp / 1000, timezone.utc).date().isoformat(),
            "entries": len(rs), "basis_mean_pct": mean([r["basis_pct"] for r in rs]),
            "ret_1x_mean": mean([r["ret_1x"] for r in rs]),
            "ret_1x_min": min(r["ret_1x"] for r in rs), "ret_1x_max": max(r["ret_1x"] for r in rs),
            "share_net_pos": sum(r["net"] > 0 for r in rs) / len(rs),
            "share_beats_tbill": (sum(e > 0 for e in ex) / len(ex)) if ex else None,
            "index_dev_pct": rs[0]["index_dev_pct"],
            "liq_1x": sum(r["liq_1x"] for r in rs), "liq_2x": sum(r["liq_2x"] for r in rs),
            "liq_3x": sum(r["liq_3x"] for r in rs),
            "max_rise_pct": max(r["max_rise_pct"] for r in rs)})
    n = len(recs)
    ex = [r["excess_1x"] for r in recs if r["excess_1x"] is not None]
    early = {k: [r[k] for r in recs if k in r] for k in ("early_25", "early_50", "early_75")}
    return {
        "entries": n, "periods": len(periods),
        "share_net_pos": sum(r["net"] > 0 for r in recs) / n if n else None,
        "share_beats_tbill": sum(e > 0 for e in ex) / len(ex) if ex else None,
        "ret_1x_mean": mean([r["ret_1x"] for r in recs]) if n else None,
        "excess_1x_mean": mean(ex) if ex else None,
        "periods_mean_beats_tbill": sum(1 for p in periods if p["share_beats_tbill"] and p["share_beats_tbill"] > 0.5),
        "index_dev_abs_max_pct": max((abs(p["index_dev_pct"]) for p in periods), default=None),
        "liquidations": {f"{L}x": sum(r[f"liq_{L}x"] for r in recs) for L in LEVERAGES},
        "extra_capital_max_pct": {f"{L}x": max((r[f"extra_{L}x_pct"] for r in recs), default=0)
                                  for L in LEVERAGES},
        "early_exit_share_negative": {k: (sum(v < 0 for v in vs) / len(vs) if vs else None)
                                      for k, vs in early.items()},
        "early_exit_worst": {k: (min(vs) if vs else None) for k, vs in early.items()},
        "rule": rule_eval(recs),
        "by_period": periods}
