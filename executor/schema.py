"""Contrato HORUS -> Pie a Pie, versión 1. Validación sin dependencias externas.

Una orden inválida nunca se "arregla": se rechaza con un código estable y el
detalle de cada error.
"""

import hashlib
import hmac
import json
import re
from datetime import datetime, timezone

ORDER_SCHEMA = "horus.order/v1"
CANCEL_SCHEMA = "horus.cancel/v1"
REPORT_SCHEMA = "pieapie.report/v1"

REASONS = (
    "SCHEMA_INVALID", "SIGNATURE_INVALID", "SIGNATURE_REQUIRED", "REAL_MODE_NOT_AUTHORIZED",
    "EXPIRED", "DUPLICATE_ORDER_ID_CONFLICT", "LIMIT_NOTIONAL", "LIMIT_EXPOSURE", "LIMIT_LOSS",
    "VENUE_NOT_ALLOWED", "ASSET_CLASS_NOT_SUPPORTED", "INSUFFICIENT_CAPITAL",
    "INSUFFICIENT_INVENTORY", "NO_ROUTE", "SLIPPAGE_EXCEEDED", "PARTIAL_TIMEOUT", "INVALIDATED",
    "STOP_HIT", "TAKE_PROFIT_HIT", "TIME_EXIT", "DATA_UNAVAILABLE", "CANCELLED_BY_HORUS",
    "ACCEPTED", "ENTRY_CONDITION_MET", "FILLED", "UNKNOWN_ORDER")

ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
SYMBOL_RE = re.compile(r"^[A-Z0-9]{2,12}/[A-Z0-9]{2,12}$")
SUPPORTED_ASSET_CLASSES = ("crypto_spot",)
ENTRY_TYPES = ("market", "limit", "trigger")
INVALIDATION_TYPES = ("price_above", "price_below", "time_after")


def parse_ts(x):
    try:
        d = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return d if d.tzinfo else None


def canonical(payload: dict) -> str:
    """JSON canónico (claves ordenadas, sin espacios, sin `signature`)."""
    body = {k: v for k, v in payload.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def payload_hash(payload: dict) -> str:
    return hashlib.sha256(canonical(payload).encode()).hexdigest()


def sign(payload: dict, key: str) -> str:
    return hmac.new(key.encode(), canonical(payload).encode(), hashlib.sha256).hexdigest()


def check_signature(payload: dict, key):
    """-> (autenticada, código de error o None). Sin clave configurada se
    acepta sin autenticar SOLO porque el modo es paper (queda registrado)."""
    sig = payload.get("signature")
    if not key:
        return False, None
    if not sig:
        return False, "SIGNATURE_REQUIRED"
    ok = hmac.compare_digest(str(sig), sign(payload, key))
    return ok, None if ok else "SIGNATURE_INVALID"


def _num(x, positive=True):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return False
    return x > 0 if positive else x >= 0


def validate_order(o: dict) -> list:
    """Lista de errores (vacía = válida estructuralmente). No consulta límites."""
    e = []
    if not isinstance(o, dict):
        return ["la orden no es un objeto JSON"]
    if o.get("schema") != ORDER_SCHEMA:
        e.append(f"schema debe ser {ORDER_SCHEMA}")
    if not ID_RE.match(str(o.get("order_id", ""))):
        e.append("order_id inválido (8-64 caracteres [A-Za-z0-9_-])")
    if o.get("issuer") != "horus":
        e.append("issuer debe ser 'horus'")
    for k in ("issued_at", "valid_until"):
        if not parse_ts(o.get(k)):
            e.append(f"{k} debe ser ISO-8601 con zona horaria")
    if o.get("valid_from") is not None and not parse_ts(o.get("valid_from")):
        e.append("valid_from inválido")
    if parse_ts(o.get("issued_at")) and parse_ts(o.get("valid_until")) and \
            parse_ts(o["valid_until"]) <= parse_ts(o["issued_at"]):
        e.append("valid_until debe ser posterior a issued_at")
    if o.get("mode") != "paper":
        e.append("mode debe ser 'paper'")
    st = o.get("strategy") or {}
    if not isinstance(st, dict) or not st.get("name") or not st.get("version"):
        e.append("strategy requiere name y version")
    ins = o.get("instrument") or {}
    if not isinstance(ins, dict):
        e.append("instrument inválido")
        ins = {}
    if ins.get("asset_class") not in SUPPORTED_ASSET_CLASSES:
        e.append(f"asset_class no soportada en v1: {ins.get('asset_class')}")
    if not SYMBOL_RE.match(str(ins.get("symbol", ""))):
        e.append("symbol inválido (formato BASE/QUOTE)")
    if not isinstance(ins.get("venues_allowed"), list) or not ins.get("venues_allowed"):
        e.append("venues_allowed debe ser una lista no vacía")
    if o.get("direction") not in ("buy", "sell"):
        e.append("direction debe ser buy o sell")
    sz = o.get("sizing") or {}
    has_n, has_q = sz.get("notional_usd") is not None, sz.get("qty") is not None
    if has_n == has_q:
        e.append("sizing requiere exactamente uno de notional_usd o qty")
    elif has_n and not _num(sz.get("notional_usd")) or has_q and not _num(sz.get("qty")):
        e.append("sizing debe ser positivo")
    en = o.get("entry") or {}
    if en.get("type") not in ENTRY_TYPES:
        e.append("entry.type debe ser market, limit o trigger")
    if en.get("type") == "limit" and not _num(en.get("limit_price")):
        e.append("entry.limit_price requerido para limit")
    if en.get("type") == "trigger" and not (_num(en.get("trigger_above")) or _num(en.get("trigger_below"))):
        e.append("entry.trigger_above o trigger_below requerido para trigger")
    if not _num(en.get("max_slippage_bps"), positive=False):
        e.append("entry.max_slippage_bps requerido (>= 0)")
    if not _num(en.get("max_wait_s")):
        e.append("entry.max_wait_s requerido (> 0)")
    if not isinstance(en.get("allow_partial", False), bool):
        e.append("entry.allow_partial debe ser booleano")
    ex = o.get("exit")
    if ex is not None:
        if o.get("direction") != "buy":
            e.append("exit solo se admite en órdenes buy (v1 no abre cortos)")
        for k in ("take_profit", "stop"):
            if ex.get(k) is not None and not _num(ex.get(k)):
                e.append(f"exit.{k} debe ser positivo")
        if ex.get("time_exit_at") is not None and not parse_ts(ex.get("time_exit_at")):
            e.append("exit.time_exit_at inválido")
        if _num(ex.get("take_profit")) and _num(ex.get("stop")) and ex["stop"] >= ex["take_profit"]:
            e.append("exit.stop debe ser menor que exit.take_profit")
    rk = o.get("risk") or {}
    if not _num(rk.get("max_loss_usd")):
        e.append("risk.max_loss_usd requerido (> 0)")
    for inv in o.get("invalidation") or []:
        if inv.get("type") not in INVALIDATION_TYPES:
            e.append(f"invalidation.type desconocido: {inv.get('type')}")
        elif inv["type"] == "time_after" and not parse_ts(inv.get("value")):
            e.append("invalidation time_after requiere fecha ISO")
        elif inv["type"] != "time_after" and not _num(inv.get("value")):
            e.append("invalidation de precio requiere valor positivo")
    if o.get("on_problem") != "halt_and_report":
        e.append("on_problem debe ser 'halt_and_report'")
    return e


def validate_cancel(c: dict) -> list:
    e = []
    if c.get("schema") != CANCEL_SCHEMA:
        e.append(f"schema debe ser {CANCEL_SCHEMA}")
    if not ID_RE.match(str(c.get("order_id", ""))):
        e.append("order_id inválido")
    if not parse_ts(c.get("issued_at")):
        e.append("issued_at inválido")
    if not isinstance(c.get("close_position", False), bool):
        e.append("close_position debe ser booleano")
    return e


def now_utc():
    return datetime.now(timezone.utc)
