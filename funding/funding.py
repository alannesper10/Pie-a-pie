"""Cálculos de funding (puros)."""

from statistics import median

HOUR_MS = 3_600_000


def infer_interval_hours(timestamps_ms):
    """Intervalo de funding inferido del historial (mediana de diferencias).

    Se redondea a horas enteras; None si no hay datos suficientes.
    """
    ts = sorted(set(int(t) for t in timestamps_ms))
    if len(ts) < 3:
        return None
    diffs = [b - a for a, b in zip(ts, ts[1:])]
    return round(median(diffs) / HOUR_MS)


def periods_in(hours, interval_hours):
    return hours / interval_hours if interval_hours else 0.0


def annualize(rate_per_period, interval_hours):
    """Tasa por período -> anual simple (métrica secundaria)."""
    return rate_per_period * periods_in(24 * 365, interval_hours)


def trailing_mean(rates, n):
    window = rates[-n:]
    return sum(window) / len(window) if window else 0.0


def expected_funding_pct(rate_per_period, interval_hours, horizon_hours):
    """Funding esperado (fracción del nocional) cobrado por un short en el horizonte.

    Con rate > 0 los longs pagan a los shorts: el short COBRA. Con rate < 0, paga.
    """
    return rate_per_period * periods_in(horizon_hours, interval_hours)


def funding_payment(rate, position_qty, mark_price):
    """Pago a un SHORT de `position_qty` en una liquidación de funding.

    Positivo = cobra; negativo = paga.
    """
    return rate * position_qty * mark_price


def funding_stats(rates, interval_hours):
    if not rates:
        return {"n": 0}
    pos = sum(r > 0 for r in rates)
    mean = sum(rates) / len(rates)
    return {
        "n": len(rates), "interval_hours": interval_hours,
        "mean": mean, "median": median(rates), "min": min(rates), "max": max(rates),
        "pct_positive": pos / len(rates),
        "annualized_mean": annualize(mean, interval_hours) if interval_hours else None,
    }
