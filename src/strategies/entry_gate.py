"""Rentabilidad mínima por plazo de recupero y autorizaciones (solo paper).

Cada entrada nueva cae en uno de cuatro casos:
  A  ejecutable y cumple la tabla           -> se abre sola
  B  ejecutable, debajo del mínimo          -> pide autorización
  C  no ejecutable (caja, liquidez, tope)   -> registro interno, sin pedir nada
  D  plazo de recupero no verificable       -> pide autorización

Plazo de recupero = hasta que el capital vuelve a estar disponible, no la fecha
"esperada" del mercado. Se toma, por pata, la fecha límite contractual de
resolución (latest_expiration_time) más el tiempo de liquidación
(settlement_timer_seconds), y el máximo entre patas: el piso de pago del par
recién se cobra cuando liquidan todas. La salida anticipada NO acorta el plazo:
no hay evidencia de que se pueda vender el par en el libro de compra sin perder
el neto, así que se usa el caso conservador. Sin esos datos, o con una pata que
no está abierta, el plazo es PLAZO_NO_VERIFICABLE.

Las autorizaciones las escribe solo el usuario en config/authorizations.json:
    {"strike_inconsistency": {"<request_id>": {"approved_at": "...", "note": "..."}}}
Una autorización vale para UNA entrada de ESA solicitud; un cambio material de
la cotización genera otra solicitud y la anterior deja de valer.
"""

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# (hasta N días inclusive, % neto mínimo sobre el capital comprometido); None = sin tope
# Más de LONG_DAYS días solo se acepta una ganancia desorbitante (pedido del usuario 21/10):
# inmovilizar capital por poco margen no sirve. El 50 % es la definición de "desorbitante".
LONG_DAYS = 60
MIN_RETURN_TABLE = ((7, 0.0), (14, 8.0), (21, 10.0), (28, 12.0), (35, 15.0), (LONG_DAYS, 20.0), (None, 50.0))
EPS = 1e-9

# Autorización solo para lo que está cerca de la regla: con menos de esta fracción del
# mínimo exigido no se pide nada (se descarta y queda registrado, sin aviso).
NEAR_MIN_FRACTION = 0.5

# cambio material respecto de la solicitud vigente
MATERIAL_PRICE = 0.01           # 1 centavo en cualquier pata (tick de Kalshi)
MATERIAL_RETURN_PP = 0.25       # puntos porcentuales de rentabilidad esperada
MATERIAL_CONTRACTS = 0.25       # variación relativa de contratos ejecutables

OPEN_STATUSES = ("active", "open")
NOT_VERIFIABLE = "PLAZO_NO_VERIFICABLE"
DEFAULT_AUTH_FILE = Path(__file__).resolve().parents[2] / "config" / "authorizations.json"


def required_return_pct(days):
    for limit, pct in MIN_RETURN_TABLE:
        if limit is None or days <= limit + EPS:
            return pct


def meets_minimum(return_pct, days):
    req = required_return_pct(days)
    return return_pct > EPS if req == 0 else return_pct >= req - EPS


def _parse(t):
    try:
        d = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def recovery_period(markets, ts):
    """-> (días | None, fecha de recupero ISO | None, detalle)."""
    now = _parse(ts)
    if not markets or now is None:
        return None, None, "sin patas o sin hora del ciclo"
    ends = []
    for m in markets:
        tk = m.get("ticker", "?")
        if m.get("status") not in OPEN_STATUSES:
            return None, None, f"{tk}: estado {m.get('status')}"
        latest = _parse(m.get("latest_expiration_time"))
        if latest is None:
            return None, None, f"{tk}: sin fecha límite de resolución"
        try:
            timer = float(m.get("settlement_timer_seconds"))
        except (TypeError, ValueError):
            return None, None, f"{tk}: sin tiempo de liquidación"
        ends.append(latest + timedelta(seconds=timer))
    end = max(ends)
    days = (end - now).total_seconds() / 86400
    if days <= 0:
        return None, None, "fecha límite vencida sin liquidar"
    return days, end.isoformat(timespec="seconds"), "fecha límite de resolución + liquidación"


def is_near_minimum(return_pct, days):
    """True si la rentabilidad llega al menos a NEAR_MIN_FRACTION del mínimo del tramo.
    Pasados LONG_DAYS días no hay "cerca": lo que no llega al mínimo no se acepta ni se consulta."""
    if days > LONG_DAYS + EPS:
        return False
    return return_pct >= NEAR_MIN_FRACTION * required_return_pct(days) - EPS


def classify(return_pct, days):
    """Caso A/B/C/D para una entrada ya ejecutable técnicamente.
    A cumple; B está debajo pero cerca (pide autorización); C está muy lejos del mínimo
    (se descarta sin pedir nada); D no tiene plazo verificable (pide autorización)."""
    if days is None:
        return "D", NOT_VERIFIABLE, None
    req = required_return_pct(days)
    if meets_minimum(return_pct, days):
        return "A", "MEETS_MIN_RETURN", req
    if is_near_minimum(return_pct, days):
        return "B", "BELOW_MIN_RETURN", req
    return "C", "FAR_BELOW_MIN_RETURN", req


def material_changes(old, new):
    """Lista de cambios materiales entre dos instantáneas de una oportunidad."""
    out = []
    if old.get("case") != new.get("case"):
        out.append("estado")
    op, np_ = old.get("prices") or [], new.get("prices") or []
    if len(op) != len(np_) or any(abs(a - b) >= MATERIAL_PRICE - EPS for a, b in zip(op, np_)):
        out.append("precio")
    if abs(old.get("return_pct", 0) - new.get("return_pct", 0)) >= MATERIAL_RETURN_PP - EPS:
        out.append("rentabilidad")
    od, nd = old.get("days"), new.get("days")
    if (od is None) != (nd is None) or (od is not None and required_return_pct(od) != required_return_pct(nd)):
        out.append("plazo")
    oc, nc = old.get("contracts") or 0, new.get("contracts") or 0
    if oc and abs(nc - oc) / oc >= MATERIAL_CONTRACTS - EPS:
        out.append("liquidez")
    return out


def request_id_for(strategy, key, ts):
    return hashlib.sha1(f"auth|{strategy}|{key}|{ts}".encode()).hexdigest()[:12]


def load_approvals(strategy, path=DEFAULT_AUTH_FILE):
    """Autorizaciones que escribió el usuario. El bot nunca escribe este archivo."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    got = data.get(strategy) if isinstance(data, dict) else None
    return got if isinstance(got, dict) else {}


AUTHZ_TTL_H = 24                # vida de una solicitud y de sus botones
EVENT_FIELDS = ["timestamp", "request_id", "event", "key", "detail"]


def event_row(ts, rid, event, key, detail=""):
    return {"timestamp": ts, "request_id": rid, "event": event, "key": key, "detail": detail}


class PendingRequests:
    """Solicitudes vigentes por par, decisiones tomadas desde el celular y rechazos
    (en el directorio de la estrategia; las escribe el bot, nunca el usuario a mano).

    pending[key]   solicitud vigente (request_id, since, snapshot)
    decisions[rid] primera decisión sobre esa solicitud (A autorizar / R rechazar) y su estado
    rejected[key]  condición rechazada: no se vuelve a pedir salvo cambio material
    used           ids de autorización ya consumidos por una entrada
    cursor         último mensaje del buzón de ntfy ya procesado
    """

    def __init__(self, path):
        self.path = Path(path)
        try:
            d = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            d = {}
        self.pending = d.get("pending", {})
        self.used = list(d.get("used", []))
        self.rejected = d.get("rejected", {})
        self.decisions = d.get("decisions", {})
        self.cursor = d.get("cursor")

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"pending": self.pending, "used": self.used}
        for name in ("rejected", "decisions"):
            if getattr(self, name):
                data[name] = getattr(self, name)
        if self.cursor:
            data["cursor"] = self.cursor
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    def approved(self):
        """Autorizaciones tomadas desde el celular que todavía esperan su entrada."""
        return {rid: i for rid, i in self.decisions.items()
                if i.get("decision") == "A" and i.get("status") == "APPROVED" and rid not in self.used}

    def find(self, rid):
        for key, cur in self.pending.items():
            if cur.get("request_id") == rid:
                return key, cur
        return None, None


def drop_pending(reqs, key, log, ts, why):
    """Quita la solicitud vigente del par; si ya estaba autorizada y sin usar, deja
    constancia de que las condiciones cambiaron. Devuelve True si había una."""
    cur = reqs.pending.pop(key, None)
    if cur is None:
        return False
    info = reqs.decisions.get(cur["request_id"])
    if info and info.get("status") == "APPROVED":
        info["status"] = "SUPERSEDED"
        log(event_row(ts, cur["request_id"], "CONDITIONS_CHANGED", key, why))
    return True
