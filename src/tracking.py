"""Persistencia del modo continuo: CSVs de registro, estado JSON y rachas."""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

NEAR_MISS_FIELDS = [
    "timestamp", "event_ticker", "ask_sum", "n_legs", "contracts_evaluated",
    "est_fees", "est_net", "depth_top", "depth_with_edge", "executable", "reason",
]
DURATION_FIELDS = [
    "event_ticker", "first_seen", "last_seen", "cycles", "minutes", "end_reason",
]
CYCLE_FIELDS = [
    "timestamp", "ok", "error", "cache_refreshed", "candidates", "evaluated",
    "timeouts", "errors", "near_misses", "executable", "paper_opened",
    "paper_settled", "t_list_s", "t_books_s", "t_total_s",
]
PAPER_FIELDS = [
    "timestamp", "action", "event_ticker", "contracts", "cost", "fees",
    "slippage", "expected_net", "expected_close", "payout", "realized_net",
    "cash_after",
]


def append_csv(path, fields, row):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if new_file:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def read_csv(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    """Escritura atómica: un Ctrl+C a mitad no deja el archivo corrupto."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, path)


def _minutes(a, b):
    return (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds() / 60


class StreakTracker:
    """Cuenta en cuántos ciclos exitosos seguidos un evento sigue ejecutable.

    Un evento que deja de ser ejecutable, o que no se pudo observar en el
    ciclo, cierra su racha. Si entre dos ciclos pasa más de `max_gap_min`
    (ej. el proceso estuvo apagado) la racha también se corta.
    """

    def __init__(self, active=None, max_gap_min=15.0):
        self.active = active or {}
        self.max_gap_min = max_gap_min

    def update(self, now, executable, observed):
        """executable/observed: sets de event_ticker. Devuelve rachas cerradas."""
        closed = []
        for ticker, s in list(self.active.items()):
            if _minutes(s["last_seen"], now) > self.max_gap_min:
                closed.append(self._close(ticker, "GAP"))
            elif ticker in executable:
                s["cycles"] += 1
                s["last_seen"] = now
            else:
                closed.append(self._close(
                    ticker, "EDGE_GONE" if ticker in observed else "NOT_OBSERVED"))
        for ticker in executable:
            if ticker not in self.active:
                self.active[ticker] = {"first_seen": now, "last_seen": now,
                                       "cycles": 1}
        return closed

    def _close(self, ticker, reason):
        s = self.active.pop(ticker)
        return {"event_ticker": ticker, "first_seen": s["first_seen"],
                "last_seen": s["last_seen"], "cycles": s["cycles"],
                "minutes": round(_minutes(s["first_seen"], s["last_seen"]), 2),
                "end_reason": reason}
