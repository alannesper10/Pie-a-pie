"""Estadística en Python puro (sin numpy/scipy: Actions no los instala).

Incluye: media/desvío, OLS simple, t de Student (CDF exacta vía beta
incompleta), test t de una cola, ADF con constante, valores críticos de
MacKinnon para Engle-Granger (2 variables), vida media AR(1) y
Benjamini-Hochberg.
"""

import math
from typing import List, Optional, Sequence, Tuple


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def std(xs, ddof=1):
    n = len(xs)
    if n <= ddof:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - ddof))


def ols(x: Sequence[float], y: Sequence[float]) -> Tuple[float, float, List[float]]:
    """y = a + b x. -> (a, b, residuos)."""
    mx, my = mean(x), mean(y)
    sxx = sum((xi - mx) ** 2 for xi in x)
    b = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sxx if sxx else 0.0
    a = my - b * mx
    return a, b, [yi - a - b * xi for xi, yi in zip(x, y)]


# --- t de Student --------------------------------------------------------------

def _betacf(a, b, x, itmax=300, eps=3e-14):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / (c if abs(c) > 1e-300 else 1e-300)
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / (c if abs(c) > 1e-300 else 1e-300)
        de = d * c
        h *= de
        if abs(de - 1) < eps:
            break
    return h


def betainc(a, b, x):
    """Beta incompleta regularizada I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - front * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    x = df / (df + t * t)
    p = 0.5 * betainc(df / 2, 0.5, x)
    return 1 - p if t > 0 else p


def ttest_mean_gt0(xs) -> Tuple[float, float]:
    """H1: media > 0. -> (t, p-valor de una cola). Con n < 2 -> (0, 1)."""
    n = len(xs)
    if n < 2:
        return 0.0, 1.0
    s = std(xs)
    if s == 0:
        return (math.inf, 0.0) if mean(xs) > 0 else (0.0, 1.0)
    t = mean(xs) / (s / math.sqrt(n))
    return t, 1 - t_cdf(t, n - 1)


# --- ADF / Engle-Granger ---------------------------------------------------------

def adf_tstat(series: Sequence[float], lags: int = 1) -> Optional[float]:
    """ADF con constante: Δy_t = α + γ y_{t-1} + Σ φ_i Δy_{t-i} + e. -> t de γ.

    Regresión múltiple resuelta por ecuaciones normales (k chico)."""
    y = list(series)
    if len(y) < lags + 10:
        return None
    dy = [y[i] - y[i - 1] for i in range(1, len(y))]
    rows, target = [], []
    for t in range(lags, len(dy)):
        rows.append([1.0, y[t]] + [dy[t - i] for i in range(1, lags + 1)])
        target.append(dy[t])
    k = len(rows[0])
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * tv for r, tv in zip(rows, target)) for i in range(k)]
    inv = _invert(xtx)
    if inv is None:
        return None
    beta = [sum(inv[i][j] * xty[j] for j in range(k)) for i in range(k)]
    resid = [tv - sum(b * v for b, v in zip(beta, r)) for r, tv in zip(rows, target)]
    dof = len(rows) - k
    if dof <= 0:
        return None
    s2 = sum(e * e for e in resid) / dof
    se = math.sqrt(s2 * inv[1][1]) if inv[1][1] > 0 else 0.0
    return beta[1] / se if se else None


def _invert(m):
    n = len(m)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-15:
            return None
        a[c], a[p] = a[p], a[c]
        pv = a[c][c]
        a[c] = [v / pv for v in a[c]]
        for r in range(n):
            if r != c:
                f = a[r][c]
                a[r] = [vr - f * vc for vr, vc in zip(a[r], a[c])]
    return [row[n:] for row in a]


# MacKinnon (2010), Engle-Granger con constante, 2 variables: c = b_inf + b1/T + b2/T^2
_EG2 = {0.01: (-3.89644, -10.9519, -22.527), 0.05: (-3.33613, -6.1101, -6.823),
        0.10: (-3.04445, -4.2412, -2.720)}


def eg_critical(n, level=0.05):
    b0, b1, b2 = _EG2[level]
    return b0 + b1 / n + b2 / n ** 2


def half_life(resid):
    """Vida media (en períodos) de un AR(1) de los residuos. None si no revierte."""
    if len(resid) < 10:
        return None
    _, b, _ = ols(resid[:-1], [resid[i] - resid[i - 1] for i in range(1, len(resid))])
    return -math.log(2) / b if b < 0 else None


def bh_reject(pvalues: Sequence[float], q: float = 0.10) -> List[bool]:
    """Benjamini-Hochberg: qué hipótesis se rechazan controlando la FDR en q.
    Se aplica sobre TODAS las hipótesis probadas, no solo las favorables."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    k_max = 0
    for rank, i in enumerate(order, 1):
        if pvalues[i] <= rank / m * q:
            k_max = rank
    rej = [False] * m
    for rank, i in enumerate(order, 1):
        if rank <= k_max:
            rej[i] = True
    return rej
