"""Descarga P6 (solo lectura, con caché en disco): mercados resueltos de Polymarket y
el historial diario de precios de sus tokens. Uso: python -m lab.research.longshot_fetch"""

import json
import os
import time

import requests

DIR = "lab_data/p6"


def markets(s):
    f = os.path.join(DIR, "markets.json")
    if os.path.exists(f):
        return json.load(open(f, encoding="utf-8"))
    out, cursor = [], None
    while True:                         # /markets/keyset: la paginación por offset corta en 5.000
        params = {"closed": "true", "end_date_min": "2024-01-01", "end_date_max": "2026-09-30",
                  "volume_num_min": 100000, "limit": 100}
        if cursor:
            params["after_cursor"] = cursor     # el nombre correcto; next_cursor se ignora (bucle infinito, corregido)
        j = s.get("https://gamma-api.polymarket.com/markets/keyset", timeout=60, params=params).json()
        r = j.get("markets") or []
        for m in r:
            ev = (m.get("events") or [{}])[0]
            m["event_key"] = ev.get("id") or ev.get("slug")
            tags = ev.get("tags") or []
            m["category_key"] = m.get("category") or (tags[0].get("label") if tags and isinstance(tags[0], dict) else None)
            m.pop("events", None)
        out += r
        nxt = j.get("next_cursor")
        if not r or not nxt or nxt == cursor:   # protección: un cursor repetido corta
            break
        cursor = nxt
        if len(out) % 2000 == 0:
            print("mercados (parcial)", len(out), flush=True)
        time.sleep(0.2)
    json.dump(out, open(f, "w", encoding="utf-8"))
    return out


def sample(ms, n_events=2500, seed=7):
    """Muestra registrada: mercados que existieron >= 8 días; 2.500 eventos al azar (semilla 7)."""
    import random
    from datetime import datetime

    def d(x):
        try:
            return datetime.fromisoformat(x.replace("Z", "+00:00"))
        except Exception:
            return None
    ok = [m for m in ms if d(m.get("startDate") or m.get("createdAt") or "") and d(m.get("endDate") or "")
          and (d(m["endDate"]) - d(m.get("startDate") or m.get("createdAt"))).days >= 8]
    events = sorted({str(m.get("event_key")) for m in ok})
    chosen = set(random.Random(seed).sample(events, min(n_events, len(events))))
    out = [m for m in ok if str(m.get("event_key")) in chosen]
    json.dump(sorted(chosen), open(os.path.join(DIR, "sample.json"), "w", encoding="utf-8"))
    return out


def history(s, tok):
    f = os.path.join(DIR, "hist", f"{tok}.json")
    if os.path.exists(f):
        return json.load(open(f, encoding="utf-8"))
    for k in range(4):
        try:
            h = s.get("https://clob.polymarket.com/prices-history", timeout=60,
                      params={"market": tok, "interval": "max", "fidelity": 1440}).json().get("history", [])
            json.dump(h, open(f, "w", encoding="utf-8"))
            return h
        except Exception:
            time.sleep(3 * (k + 1))
    return None


def main():
    os.makedirs(os.path.join(DIR, "hist"), exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0"
    ms = markets(s)
    print("mercados", len(ms), flush=True)
    # el endpoint keyset no respeta todos los filtros: se aplican acá (regla de 9f248c5)
    ms = [m for m in ms if float(m.get("volumeNum") or 0) >= 100000
          and "2024-01-01" <= (m.get("endDate") or "")[:10] <= "2026-09-30"]
    print("mercados tras filtrar (volumen >= 100k, fin 2024-01..2026-09)", len(ms), flush=True)
    ms = sample(ms)
    print("mercados en la muestra", len(ms), flush=True)
    n = 0
    for m in ms:
        try:
            toks = json.loads(m.get("clobTokenIds") or "[]")
            outs = json.loads(m.get("outcomes") or "[]")
        except Exception:
            continue
        if len(outs) != 2:
            continue
        for t in toks:
            history(s, t)
            n += 1
            if n % 200 == 0:
                print("historiales", n, flush=True)
            time.sleep(0.05)
    print("fin", n, flush=True)


if __name__ == "__main__":
    main()
