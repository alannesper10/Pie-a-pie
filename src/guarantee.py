"""Garantías de arbitraje: cobertura de resultados, escenarios, ejecución y
clasificación. Compartido por todas las estrategias.

Principio: la exhaustividad se DEMUESTRA, no se supone. Una oportunidad solo es
ARBITRAJE_GARANTIZADO si:
  1) cubre TODOS los resultados de resolución enumerables (prueba positiva),
  2) su ejecución se verificó sobre libros guardados tras la latencia, y
  3) el neto mínimo es > 0 aun con los costos supuestos x1.5.
Si gana solo en algunos escenarios es ESPECULATIVA; si no se puede demostrar
la ejecución o depende de costos no verificados es NO_VERIFICABLE.

Auditoría que originó este módulo: KXCRITICSCOM-27 (premio con lista abierta;
"Tie" se aceptaba como comodín y una película no listada daba pago 0).
"""

import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

GUARANTEED = "ARBITRAJE_GARANTIZADO"
SPECULATIVE = "ESPECULATIVA"
UNVERIFIABLE = "NO_VERIFICABLE"
NO_EDGE = "SIN_EDGE"

EXEC_VERIFIED = "EJECUCION_VERIFICADA"
EXEC_NOT_DEMONSTRATED = "EJECUCION_NO_DEMOSTRADA"
EXEC_FAILED = "EJECUCION_FALLIDA"

COST_STRESS = 1.5               # costos supuestos (no verificados) x1.5
MAX_LEG_SKEW_S = 5.0            # desfase máximo entre la 1a y la última pata
MANUAL_FILE = Path("config") / "exhaustive_events.json"

_LOWER = {"less", "less_or_equal"}
_UPPER = {"greater", "greater_or_equal"}
_VS = re.compile(r"\bvs\.?\b", re.I)
_TIE = re.compile(r"^(tie|draw)$")
_TIE_RESULT = re.compile(r"tie is the result|ends in a (tie|draw)|result is a (tie|draw)|"
                         r"is (a )?draw|end(s|ed)? tied|game is tied|match is tied|"
                         r"\btie in the\b|neither team wins", re.I)
_NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
_OPEN_LIST_HINTS = re.compile(r"nominat|not nominated|shortlist|if .* is not listed", re.I)
_CANCEL_HINTS = re.compile(r"fair price|cancel|postpone|reschedul", re.I)


def _norm(text):
    return re.sub(r"[^a-z0-9 ]+", "", (text or "").lower()).strip()


def rules_template(text):
    return re.sub(r"\s+", " ", _NUMBER.sub("#", (text or "").lower())).strip()


# ------------------------------------------------------------- cobertura ---

@dataclass
class Coverage:
    proven: bool
    method: str                         # STRIKES_PARTITION | HEAD_TO_HEAD_WITH_TIE | MANUAL_VERIFIED | NOT_PROVEN
    reasons: List[str] = field(default_factory=list)
    residuals: List[dict] = field(default_factory=list)   # riesgos residuales (cancelación, etc.)
    open_list_evidence: List[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def load_manual_verified(path=MANUAL_FILE) -> Dict[str, dict]:
    """Eventos/series verificados A MANO como exhaustivos (con quién y cuándo)."""
    p = Path(path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {e["ticker"]: e for e in data.get("events", [])
            if e.get("verified") is True and e.get("verified_by") and e.get("verified_at")
            and e.get("ticker")}


def _strike_interval(m):
    st, lo, hi = m.get("strike_type"), m.get("floor_strike"), m.get("cap_strike")
    if st in _LOWER and hi is not None:
        return (-math.inf, float(hi))
    if st in _UPPER and lo is not None:
        return (float(lo), math.inf)
    if st == "between" and lo is not None and hi is not None:
        return (float(lo), float(hi))
    return None


def _strikes_partition(markets):
    """Partición completa (-inf, +inf) de UNA variable (misma regla normalizada)."""
    iv = [_strike_interval(m) for m in markets]
    if not markets or any(i is None for i in iv):
        return False, "no todas las patas son strikes"
    templates = {rules_template(m.get("rules_primary")) for m in markets}
    if len(templates) != 1 or not next(iter(templates)):
        return False, "las patas no comparten la misma regla (variable distinta o sin reglas)"
    iv.sort()
    if iv[0][0] != -math.inf:
        return False, "falta el tramo inferior"
    reach = iv[0][1]
    for lo, hi in iv[1:]:
        if lo > reach:
            return False, f"hueco entre {reach} y {lo}"
        reach = max(reach, hi)
    return (reach == math.inf), ("falta el tramo superior" if reach != math.inf else "ok")


def _head_to_head_with_tie(event, markets):
    """Partido 'A vs B' con exactamente 2 participantes + 1 empate, todos con
    reglas sobre el mismo partido. Validado: 105 eventos deportivos liquidados."""
    title = event.get("title") or ""
    if not _VS.search(title):
        return False, "el título no es un enfrentamiento 'A vs B'"
    ties = [m for m in markets if _TIE.match(_norm(m.get("yes_sub_title")))]
    others = [m for m in markets if m not in ties]
    if len(ties) != 1 or len(others) != 2:
        return False, f"se esperaban 2 participantes + 1 empate (hay {len(others)} + {len(ties)})"
    tie_rules = (ties[0].get("rules_primary") or "").lower()
    if not _TIE_RESULT.search(tie_rules):
        return False, "la regla del empate no describe un resultado empatado"
    # Las 3 reglas tienen que hablar del MISMO enfrentamiento del título
    # ("BUF Bills vs LA Rams"); los nombres de las patas pueden diferir
    # ("Los Angeles R"), el enfrentamiento no.
    matchup = title.split(":")[0].strip().lower()
    rules = [(m.get("rules_primary") or "").lower() for m in others] + [tie_rules]
    if not matchup or not all(matchup in r for r in rules):
        return False, f"las reglas no se refieren todas al enfrentamiento '{matchup}'"
    return True, "ok"


def kalshi_yes_coverage(event, manual=None) -> Coverage:
    """¿Comprar YES en TODAS las patas cubre todos los resultados?"""
    markets = event.get("markets") or []
    manual = load_manual_verified() if manual is None else manual
    cov = Coverage(proven=False, method="NOT_PROVEN")
    for m in markets:
        txt = " ".join(str(m.get(k) or "") for k in ("rules_secondary", "early_close_condition"))
        if _CANCEL_HINTS.search(txt) and not cov.residuals:
            cov.residuals.append({"name": "CANCELACION_O_REPROGRAMACION",
                                  "payout": "precio justo según reglas de Kalshi (no garantizado)"})
        if _OPEN_LIST_HINTS.search(str(m.get("early_close_condition") or "")):
            cov.open_list_evidence.append(f"{m.get('ticker')}: {m.get('early_close_condition')}")
    if not event.get("mutually_exclusive"):
        cov.reasons.append("el evento no es mutuamente excluyente")
        return cov
    key = event.get("event_ticker") or ""
    series = event.get("series_ticker") or key.split("-")[0]
    if key in manual or series in manual:
        cov.proven, cov.method = True, "MANUAL_VERIFIED"
        cov.reasons.append(f"verificado a mano: {(manual.get(key) or manual.get(series)).get('verified_by')}")
        return cov
    ok, why = _strikes_partition(markets)
    if ok:
        cov.proven, cov.method = True, "STRIKES_PARTITION"
        return cov
    cov.reasons.append(f"strikes: {why}")
    ok, why2 = _head_to_head_with_tie(event, markets)
    if ok:
        cov.proven, cov.method = True, "HEAD_TO_HEAD_WITH_TIE"
        return cov
    cov.reasons.append(f"enfrentamiento: {why2}")
    cov.reasons.append("lista de opciones abierta o no demostrada: un resultado no listado "
                       "haría que todas las patas YES paguen 0")
    return cov


# ------------------------------------------------------------- escenarios ---

def scenario_table(outcomes: List[dict], outlay: float):
    """outcomes: [{"scenario": str, "payout": float | None}] (None = no determinable).
    -> dict con neto por escenario, mínimo, máximo y pérdida máxima."""
    rows = []
    for o in outcomes:
        p = o.get("payout")
        rows.append({**o, "net": None if p is None else p - outlay})
    nets = [r["net"] for r in rows if r["net"] is not None]
    mn = min(nets) if nets else None
    return {"outlay": outlay, "scenarios": rows,
            "net_min": mn, "net_max": max(nets) if nets else None,
            "max_loss": max(0.0, -mn) if mn is not None else None,
            "undetermined": [r["scenario"] for r in rows if r["net"] is None],
            "net_min_pct": (mn / outlay) if (mn is not None and outlay) else None}


def yes_all_outcomes(contracts, coverage: Coverage):
    out = [{"scenario": "gana una de las patas listadas", "payout": float(contracts)}]
    if not coverage.proven:
        out.append({"scenario": "gana una opción no listada / ninguna listada", "payout": 0.0})
    for r in coverage.residuals:
        out.append({"scenario": r["name"], "payout": None, "note": r["payout"]})
    return out


def no_subset_outcomes(contracts, k, cancellation=True):
    out = [{"scenario": "gana una de las k patas elegidas", "payout": float(contracts * (k - 1))},
           {"scenario": "gana una opción fuera de las elegidas o ninguna", "payout": float(contracts * k)}]
    if cancellation:
        out.append({"scenario": "CANCELACION_O_REPROGRAMACION", "payout": None,
                    "note": "NO paga 1 - precio justo por pata; >= k-1 si los precios justos suman <= 1"})
    return out


def strike_pair_outcomes(contracts, cancellation=True):
    out = [{"scenario": "valor dentro del strike angosto", "payout": float(contracts)},
           {"scenario": "valor entre el amplio y el angosto", "payout": float(2 * contracts)},
           {"scenario": "valor fuera del strike amplio", "payout": float(contracts)}]
    if cancellation:
        out.append({"scenario": "CANCELACION_O_DATO_NO_PUBLICADO", "payout": None,
                    "note": "liquidación a precio justo"})
    return out


# -------------------------------------------------------------- ejecución ---

def _ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def verify_execution(legs: List[dict], qty: float, fee_fn, *, max_skew_s=MAX_LEG_SKEW_S):
    """Verifica la ejecución sobre libros pedidos DESPUÉS de la latencia.

    legs: [{"ticker", "side", "limit", "asks_after": [(p, q)], "fetched_after": iso}]
    Cada pata es una orden IOC con precio límite = peor precio planificado. Si
    alguna no llega al volumen completo, la ejecución FALLA (no se asume que 16
    patas se llenan juntas porque aparecieron en consultas sucesivas).
    """
    times = [_ts(l.get("fetched_after")) for l in legs]
    if any(t is None for t in times) or any(not l.get("asks_after") for l in legs):
        return {"status": EXEC_NOT_DEMONSTRATED, "reason": "faltan libros posteriores a la latencia"}
    skew = (max(times) - min(times)).total_seconds()
    fills, cost, fees = [], 0.0, 0.0
    for l in legs:
        lv = [(p, q) for p, q in l["asks_after"] if p <= l["limit"] + 1e-12]
        got, c, f = 0.0, 0.0, []
        for p, q in lv:
            if got >= qty - 1e-12:
                break
            take = min(q, qty - got)
            got += take
            c += take * p
            f.append((p, take))
        fills.append({"ticker": l["ticker"], "side": l["side"], "filled": got, "cost": c, "fills": f})
        cost += c
        fees += fee_fn(f)
    short = [x["ticker"] for x in fills if x["filled"] < qty - 1e-9]
    res = {"skew_s": skew, "legs": fills, "cost": cost, "fees": fees, "qty": qty}
    if short:
        return {**res, "status": EXEC_FAILED,
                "reason": f"profundidad insuficiente tras la latencia en {len(short)} pata(s): {short[:5]}"}
    if skew > max_skew_s:
        return {**res, "status": EXEC_NOT_DEMONSTRATED,
                "reason": f"las patas se consultaron con {skew:.1f}s de diferencia (máx {max_skew_s}s)"}
    return {**res, "status": EXEC_VERIFIED, "reason": "volumen completo disponible en todas las patas"}


def simulate_leg_failure(legs_fills: List[dict], unwind_bid_fn, fail_index: int, fee_fn):
    """Costo de que la pata `fail_index` no se ejecute: se deshacen las patas
    ya llenadas vendiendo al bid. Devuelve la pérdida en USD (>= 0)."""
    loss = 0.0
    for leg in legs_fills[:fail_index]:
        q = leg["filled"]
        bids = unwind_bid_fn(leg["ticker"], leg["side"])
        got, proceeds, sold = 0.0, 0.0, []
        for p, s in bids:
            if got >= q - 1e-12:
                break
            t = min(s, q - got)
            got += t
            proceeds += t * p
            sold.append((p, t))
        loss += leg["cost"] - proceeds + fee_fn(leg["fills"]) + fee_fn(sold)
    return loss


# ---------------------------------------------------------- clasificación ---

def classify(*, net_expected, coverage_proven, exec_status, net_min, net_min_stressed):
    """-> (clasificación, motivo)."""
    if net_expected is None or net_expected <= 0:
        return NO_EDGE, "neto esperado <= 0 después de costos"
    if not coverage_proven:
        return SPECULATIVE, ("gana solo si el resultado está entre las opciones cubiertas; "
                             "un resultado no cubierto genera pérdida")
    if net_min is None or net_min <= 0:
        return SPECULATIVE, "algún escenario cubierto da pérdida neta"
    if exec_status != EXEC_VERIFIED:
        return UNVERIFIABLE, "ejecución no demostrada con libros verificados"
    if net_min_stressed is None or net_min_stressed <= 0:
        return UNVERIFIABLE, f"el neto mínimo no sobrevive a costos supuestos x{COST_STRESS}"
    return GUARANTEED, "todos los escenarios cubiertos, ejecución verificada, neto mínimo > 0 con estrés"
