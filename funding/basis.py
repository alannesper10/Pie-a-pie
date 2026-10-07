"""Cálculos de basis (puros). basis = precio perp - precio spot."""


def basis(perp_price, spot_price):
    return perp_price - spot_price


def basis_pct(perp_price, spot_price):
    return (perp_price - spot_price) / spot_price if spot_price else 0.0


def basis_pnl(qty, spot_entry, perp_entry, spot_exit, perp_exit):
    """P&L de precio de spot largo + perp corto con la misma cantidad.

    = q*(S1 - S0) - q*(F1 - F0) = q*(basis_entrada - basis_salida).
    Entrar con perp sobre spot (basis > 0) y salir con basis menor gana.
    """
    return qty * ((perp_entry - spot_entry) - (perp_exit - spot_exit))


def basis_stats(pcts):
    if not pcts:
        return {"n": 0}
    mean = sum(pcts) / len(pcts)
    var = sum((p - mean) ** 2 for p in pcts) / len(pcts)
    return {"n": len(pcts), "mean_pct": mean, "std_pct": var ** 0.5,
            "min_pct": min(pcts), "max_pct": max(pcts)}
