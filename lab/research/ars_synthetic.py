"""C6 (PRUEBAS_HULL_C1_C6_2026-10-16.md): "dólar sintético" con futuros de dólar de A3.

Hull EN 5.10 (paridad de tasas cubierta): F = S·(1+i_ARS·T)/(1+i_USD·T). Si la tasa
implícita del futuro es menor que la tasa en pesos disponible, un inversor en US$
puede: vender US$ por MEP, poner los pesos a plazo fijo y COMPRAR el futuro de
dólar por el mismo nominal (cobertura). Al vencer, el futuro liquida contra el
A3500 y los pesos se vuelven a convertir por MEP.

Regla registrada (antes de ver resultados):
  - entrada: último día con ajuste del contrato que vence el mes siguiente,
    dentro del mes m; salida: vencimiento de ese contrato (fin del mes m+1)
  - capital US$1.000 = N (1 contrato DLR = US$1.000 de nominal)
  - 85% de los pesos a plazo fijo a la tasa de depósitos a 30 días (BCRA, var. 12)
    y 15% en caución a (tasa − 2 pp) como garantía y colchón de diferencias diarias (SUPUESTO)
  - costos: futuro 0,1% del nominal por lado (SUPUESTO); MEP 0,25% por conversión
    sobre las puntas compra/venta (SUPUESTO; MEP de argentinadatos, INDICATIVO)
  - resultado en US$ = [pesos finales + N·(A3500_T − F0) − costos] / MEP_venta_T − N
Riesgo de base: el futuro liquida a A3500, pero la conversión es por MEP.
"""

import math

FUT_FEE = 0.001
MEP_FEE = 0.0025
MARGIN_SHARE = 0.15
CAUCION_SPREAD = 0.02


def cycle(N, mep_compra0, mep_venta_T, a3500_0, a3500_T, F0, rate_tna_pct, days, cost_mult=1.0):
    """Un ciclo completo. -> dict con resultado y descomposición."""
    i = rate_tna_pct / 100
    ars0 = N * mep_compra0 * (1 - cost_mult * MEP_FEE)
    pf = ars0 * (1 - MARGIN_SHARE) * (1 + i * days / 365)
    caucion = ars0 * MARGIN_SHARE * (1 + max(i - CAUCION_SPREAD, 0) * days / 365)
    fut_pnl = N * (a3500_T - F0)
    fut_cost = cost_mult * FUT_FEE * N * (F0 + a3500_T)
    ars_T = pf + caucion + fut_pnl - fut_cost
    usd_T = ars_T / mep_venta_T * (1 - cost_mult * MEP_FEE)
    margin_usd = N * MARGIN_SHARE
    return {
        "usd_final": usd_T, "pnl_usd": usd_T - N, "ret_total_pct": (usd_T / N - 1) * 100,
        # el futuro solo, sobre la garantía inmovilizada (en US$ de entrada)
        "fut_pnl_usd": (fut_pnl - fut_cost) / mep_venta_T,
        "ret_on_margin_pct": (fut_pnl - fut_cost) / mep_venta_T / margin_usd * 100,
        # descomposición aproximada (en % del capital)
        "peso_carry_pct": i * days / 365 * 100,
        "implied_cost_pct": (F0 / a3500_0 - 1) * 100,
        "basis_change_pct": ((mep_compra0 / a3500_0) / (mep_venta_T / a3500_T) - 1) * 100,
        "mep_gap_entry_pct": (mep_compra0 / a3500_0 - 1) * 100,
        "mep_gap_exit_pct": (mep_venta_T / a3500_T - 1) * 100,
        "implied_rate_tna_pct": (F0 / a3500_0 - 1) * 365 / days * 100,
        "days": days,
    }


def expired(last_settlement, a3500_on_last_day, tol=0.0005):
    """Un contrato DLR vencido liquida exactamente al A3500 de su último día. Si el
    último ajuste disponible difiere, el contrato todavía no venció en los datos
    (error corregido el 16/10: se había incluido DLR10/2026 sin vencer)."""
    return a3500_on_last_day is not None and abs(last_settlement / a3500_on_last_day - 1) <= tol


def stats(rets_pct):
    n = len(rets_pct)
    if n < 2:
        return {"n": n}
    m = sum(rets_pct) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in rets_pct) / (n - 1))
    eq, peak, mdd = 1.0, 1.0, 0.0
    for x in rets_pct:
        eq *= 1 + x / 100
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    return {"n": n, "mean_pct": m, "t": m / (sd / math.sqrt(n)) if sd > 0 else None,
            "positive": sum(x > 0 for x in rets_pct), "worst_pct": min(rets_pct),
            "total_pct": (eq - 1) * 100, "max_drawdown_pct": mdd * 100}


# ---------------- datos públicos ----------------

def a3_dlr(s, cache_dir="lab_data/c6_dlr_pages", retries=6):
    """Todos los ajustes de DLR. Sin parámetros from/to: con rango de fechas el
    servidor de A3 devuelve 'Execution Timeout Expired' (verificado el 16/10).
    El servidor también falla de forma intermitente: reintentos con espera y
    cada página guardada en disco (no se rellena ninguna página faltante)."""
    import json
    import os
    import time
    os.makedirs(cache_dir, exist_ok=True)
    out, page, total = [], 1, None
    while True:
        f = os.path.join(cache_dir, f"page_{page:03d}.json")
        rows = None
        if os.path.exists(f):
            rows = json.load(open(f, encoding="utf-8"))
        else:
            for k in range(retries):
                try:
                    r = s.get("https://apicem.matbarofex.com.ar/api/v2/closing-prices", timeout=120,
                              params={"product": "DLR", "page": page, "pageSize": 1000}).json()
                    if "data" in r:
                        rows, total = r["data"], r.get("totalEntries", total)
                        break
                except Exception:
                    pass
                time.sleep(5 * (k + 1))
            if rows is None:
                raise RuntimeError(f"A3: la página {page} no respondió tras {retries} intentos")
            if len(rows) == 1000:                 # páginas completas se guardan; la última se vuelve a pedir
                json.dump(rows, open(f, "w", encoding="utf-8"))
        out += rows
        if len(rows) < 1000:
            break
        page += 1
    return out


def bcra(s, var_id, start="2019-12-01", end="2026-12-31"):
    out, offset = {}, 0
    while True:
        r = s.get(f"https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/{var_id}", timeout=60,
                  params={"desde": start, "hasta": end, "limit": 3000, "offset": offset}).json()
        det = (r.get("results") or [{}])[0].get("detalle") or []
        for x in det:
            out[x["fecha"]] = x["valor"]
        if len(det) < 3000:
            break
        offset += 3000
    return out
