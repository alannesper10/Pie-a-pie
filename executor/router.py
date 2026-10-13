"""Ruteo de ejecución: dónde y cuánto ejecutar en cada venue permitido.

Se ordenan TODOS los niveles de los libros permitidos por precio efectivo
(precio x (1 ± comisión)) y se barre en ese orden: el resultado puede
repartirse entre venues si así sale más barato. Se informa también el mejor
venue único para medir el ahorro del ruteo. Las comisiones son las de
lab/fees (nivel base público, SUPUESTAS: las reales por cuenta requieren clave).
"""

from lab.fees import taker_fee


def effective(price, fee, side):
    return price * (1 + fee) if side == "buy" else price * (1 - fee)


def _levels(books, venues, side, fee_of):
    key = "asks" if side == "buy" else "bids"
    out = []
    for v in venues:
        b = books.get(v)
        if not b or not b.get(key):
            continue
        fee = fee_of(v)
        out += [(effective(p, fee, side), p, q, v, fee) for p, q in b[key] if q > 0]
    out.sort(key=lambda x: x[0], reverse=(side == "sell"))
    return out


def route(books, venues, side, qty=None, notional=None, limit_price=None, fee_of=None):
    """books: {venue: {"bids": [[p, q]], "asks": [[p, q]]}}. Exactamente uno de
    qty (unidades) o notional (USD sin comisión). limit_price: no se cruza
    peor que ese precio. -> dict con fills por venue y totales."""
    fee_of = fee_of or (lambda v: taker_fee(v)[0])
    lv = _levels(books, venues, side, fee_of)
    fills, got, spent = [], 0.0, 0.0
    for eff, p, q, v, fee in lv:
        if limit_price is not None and (p > limit_price if side == "buy" else p < limit_price):
            break
        if qty is not None:
            take = min(q, qty - got)
        else:
            take = min(q, (notional - spent) / p)
        if take <= 1e-15:
            break
        fills.append({"venue": v, "price": p, "qty": take, "fee_usd": take * p * fee, "fee_rate": fee})
        got += take
        spent += take * p
        if (qty is not None and got >= qty - 1e-12) or (notional is not None and spent >= notional - 1e-9):
            break
    fees = sum(f["fee_usd"] for f in fills)
    best_single = None
    for v in venues:
        one = route(books, [v], side, qty=got or qty, limit_price=limit_price, fee_of=fee_of) \
            if len(venues) > 1 and got else None
        if one and one["filled_qty"] >= got - 1e-12:
            allin = one["gross_usd"] + (one["fees_usd"] if side == "buy" else -one["fees_usd"])
            if best_single is None or (allin < best_single[1] if side == "buy" else allin > best_single[1]):
                best_single = (v, allin)
    allin = spent + fees if side == "buy" else spent - fees
    return {"side": side, "fills": fills, "filled_qty": got, "gross_usd": spent, "fees_usd": fees,
            "all_in_usd": allin, "avg_price": spent / got if got else None,
            "venues_used": sorted({f["venue"] for f in fills}),
            "best_single_venue": best_single[0] if best_single else None,
            "saving_vs_best_single_usd": (abs(best_single[1] - allin) if best_single else 0.0)}


def best_price(books, venues, side):
    """Mejor precio contrario (ask para comprar, bid para vender) entre venues."""
    key = "asks" if side == "buy" else "bids"
    ps = [books[v][key][0][0] for v in venues if books.get(v) and books[v].get(key)]
    if not ps:
        return None
    return min(ps) if side == "buy" else max(ps)


def mark_price(books, venues):
    """Precio de marca de una posición larga: el mejor bid (lo que se obtendría al vender)."""
    return best_price(books, venues, "sell")
