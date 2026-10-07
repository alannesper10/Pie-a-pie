"""Fase 0: análisis histórico de spot largo + perp corto en el mismo exchange.

Regla de decisión SIN mirar el futuro, evaluada en cada liquidación de funding:
  esperado = media de las últimas `trailing_periods` tasas YA liquidadas
             x períodos en el horizonte  -  costos de ida y vuelta
  entra si esperado > 0; sale si la media móvil se vuelve negativa o se
  cumple max_hold_days. El basis esperado se toma como 0 (conservador); el
  basis realizado sí entra en el resultado.

Ejecución: latencia de 1 barra (se opera al cierre de la hora SIGUIENTE a la
decisión). Funding cobrado sobre qty x mark. Rebalanceo/liquidación chequeados
con cierres horarios del perp (no ve extremos intra-hora: limitación).
"""

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

from .basis import basis_pct, basis_pnl, basis_stats
from .config import FundingConfig
from .costs import CostBreakdown, rebalance_cost_usd
from .funding import (
    expected_funding_pct, funding_payment, funding_stats, infer_interval_hours,
    trailing_mean,
)
from .risk import liquidation_distance, short_liquidation_price

HOUR_MS = 3_600_000


@dataclass
class Trade:
    entry_ts: int
    exit_ts: int
    exit_reason: str
    qty: float
    notional: float
    spot_entry: float
    perp_entry: float
    spot_exit: float
    perp_exit: float
    funding_usd: float
    funding_events: int
    basis_pnl_usd: float
    costs_usd: float
    rebalances: int
    rebalance_costs_usd: float
    min_liq_distance: float
    net_usd: float

    @property
    def hold_hours(self):
        return (self.exit_ts - self.entry_ts) / HOUR_MS


@dataclass
class BacktestResult:
    decisions: int = 0
    ex_ante_positive: int = 0
    ex_ante_runs: List[int] = field(default_factory=list)   # duración en períodos
    trades: List[Trade] = field(default_factory=list)
    skipped_no_price: int = 0

    def summary(self, notional):
        t = self.trades
        net = [x.net_usd for x in t]
        return {
            "decisions": self.decisions,
            "ex_ante_positive": self.ex_ante_positive,
            "ex_ante_positive_pct": (self.ex_ante_positive / self.decisions
                                     if self.decisions else 0.0),
            "ex_ante_runs": len(self.ex_ante_runs),
            "ex_ante_run_mean_periods": (sum(self.ex_ante_runs) / len(self.ex_ante_runs)
                                         if self.ex_ante_runs else 0.0),
            "trades": len(t),
            "net_positive_trades": sum(n > 0 for n in net),
            "net_usd_total": sum(net),
            "net_pct_of_notional": sum(net) / notional if notional else 0.0,
            "funding_usd_total": sum(x.funding_usd for x in t),
            "basis_pnl_usd_total": sum(x.basis_pnl_usd for x in t),
            "costs_usd_total": sum(x.costs_usd for x in t),
            "rebalances": sum(x.rebalances for x in t),
            "liquidations": sum(x.exit_reason == "LIQUIDATION" for x in t),
            "mean_hold_hours": (sum(x.hold_hours for x in t) / len(t)) if t else 0.0,
            "min_liq_distance": min((x.min_liq_distance for x in t), default=None),
            "skipped_no_price": self.skipped_no_price,
        }


def _price_at_or_after(series: Dict[int, float], ts, max_wait_h=3):
    for k in range(max_wait_h + 1):
        t = ts + k * HOUR_MS
        if t in series:
            return t, series[t]
    return None, None


def backtest(funding: List[Tuple[int, float]], spot: Dict[int, float],
             perp: Dict[int, float], mark: Dict[int, float], *,
             interval_hours, round_trip_cost_pct, cfg: FundingConfig, exchange,
             notional, leg_fail_cost_pct=0.0) -> BacktestResult:
    """Backtest puro. `funding` = [(ts_ms, tasa)], series = {ts_hora_ms: cierre}."""
    res = BacktestResult()
    horizon_h = cfg.horizon_days * 24
    rates: List[float] = []
    pos: Optional[dict] = None
    run = 0
    hours = sorted(perp)

    def close(exit_dec_ts, reason):
        nonlocal pos
        t_exit, s1 = _price_at_or_after(spot, exit_dec_ts + HOUR_MS)
        _, f1 = _price_at_or_after(perp, exit_dec_ts + HOUR_MS)
        if s1 is None or f1 is None:      # sin precio: cierre al último disponible
            t_exit = max(t for t in hours if t <= exit_dec_ts + HOUR_MS) if hours else exit_dec_ts
            s1 = spot.get(t_exit, pos["s0"])
            f1 = perp.get(t_exit, pos["f0"])
        q = pos["qty"]
        bpnl = basis_pnl(q, pos["s0"], pos["f0"], s1, f1)
        if reason == "LIQUIDATION":
            bpnl = q * (s1 - pos["s0"]) - q * pos["f0"] / cfg.leverage
        costs = notional * (round_trip_cost_pct + leg_fail_cost_pct)
        net = bpnl + pos["funding"] - costs - pos["reb_cost"]
        res.trades.append(Trade(
            entry_ts=pos["t0"], exit_ts=t_exit, exit_reason=reason, qty=q,
            notional=notional, spot_entry=pos["s0"], perp_entry=pos["f0"],
            spot_exit=s1, perp_exit=f1, funding_usd=pos["funding"],
            funding_events=pos["events"], basis_pnl_usd=bpnl, costs_usd=costs,
            rebalances=pos["reb"], rebalance_costs_usd=pos["reb_cost"],
            min_liq_distance=pos["min_liq"], net_usd=net))
        pos = None

    for i, (ts, rate) in enumerate(funding):
        # 1) Si hay posición: riesgo hora por hora hasta esta liquidación, y funding.
        if pos is not None and ts > pos["t0"]:
            for h in (h for h in hours if pos["last_check"] < h <= ts):
                f = perp[h]
                liq = short_liquidation_price(pos["ref"], cfg.leverage,
                                              cfg.maintenance_margin.value)
                pos["min_liq"] = min(pos["min_liq"], liquidation_distance(f, liq))
                if f >= liq:
                    pos["last_check"] = h
                    close(h - HOUR_MS, "LIQUIDATION")
                    break
                loss = pos["qty"] * (f - pos["ref"])
                if loss > cfg.rebalance_threshold.value * pos["qty"] * pos["f0"] / cfg.leverage:
                    pos["reb"] += 1
                    pos["reb_cost"] += rebalance_cost_usd(loss, cfg, exchange)
                    pos["ref"] = f
                pos["last_check"] = h
            if pos is not None:
                m = mark.get(ts) or perp.get(ts)
                if m is not None:
                    pos["funding"] += funding_payment(rate, pos["qty"], m)
                    pos["events"] += 1
        rates.append(rate)

        # 2) Decisión con información disponible en ts.
        if len(rates) < cfg.trailing_periods:
            continue
        exp_rate = trailing_mean(rates, cfg.trailing_periods)
        exp_net = (expected_funding_pct(exp_rate, interval_hours, horizon_h)
                   - round_trip_cost_pct - leg_fail_cost_pct)
        res.decisions += 1
        if exp_net > 0:
            res.ex_ante_positive += 1
            run += 1
        elif run:
            res.ex_ante_runs.append(run)
            run = 0

        if pos is None and exp_net > 0:
            t0, s0 = _price_at_or_after(spot, ts + HOUR_MS)
            _, f0 = _price_at_or_after(perp, ts + HOUR_MS)
            if s0 is None or f0 is None:
                res.skipped_no_price += 1
                continue
            pos = {"t0": t0, "s0": s0, "f0": f0, "qty": notional / s0, "ref": f0,
                   "funding": 0.0, "events": 0, "reb": 0, "reb_cost": 0.0,
                   "last_check": t0, "min_liq": 1.0 / cfg.leverage}
        elif pos is not None:
            held_days = (ts - pos["t0"]) / (24 * HOUR_MS)
            if exp_rate < 0:
                close(ts, "FUNDING_TURNED_NEGATIVE")
            elif held_days >= cfg.max_hold_days:
                close(ts, "MAX_HOLD")
    if run:
        res.ex_ante_runs.append(run)
    if pos is not None and funding:
        close(funding[-1][0], "END_OF_DATA")
    return res


def analyze_pair(adapter, asset, cfg: FundingConfig, storage, now_ms, log):
    """Descarga (o reutiliza) datos, calcula costos con el libro actual y corre el
    backtest. Nunca inventa datos: si algo falla queda en `errors`."""
    from .config import effective_fees
    from .costs import round_trip_costs, slippage_vs_mid

    ex = adapter.name
    out = {"exchange": ex, "asset": asset, "errors": []}
    since = now_ms - cfg.history_days * 24 * HOUR_MS

    def step(name, fn):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            out["errors"].append(f"{name}: {type(e).__name__}: {str(e)[:160]}")
            storage.log_error(str(now_ms), ex, name, e)
            return None

    info = step("market_info", lambda: adapter.market_info(asset))
    mins = step("min_qty", lambda: adapter.min_qty(asset))
    fund = step("funding_history", lambda: adapter.fetch_funding_history(asset, since, now_ms))
    spot = step("spot_ohlcv", lambda: adapter.fetch_closes(asset, "spot", since, until_ms=now_ms))
    perp = step("perp_ohlcv", lambda: adapter.fetch_closes(asset, "perp", since, until_ms=now_ms))
    mark = step("mark_ohlcv", lambda: adapter.fetch_closes(asset, "mark", since, until_ms=now_ms))
    books = step("order_books", lambda: adapter.fetch_books(asset, 50))
    now_f = step("funding_now", lambda: adapter.fetch_funding_now(asset))

    for name, rows, market in (("spot", spot, "spot"), ("perp", perp, "perp"),
                               ("mark", mark, "mark")):
        if rows:
            storage.save_prices(ex, asset, market, rows)
    if fund:
        storage.save_funding(ex, asset, fund)

    def coverage(rows):
        return round((rows[-1][0] - rows[0][0]) / (24 * HOUR_MS), 1) if rows else 0.0

    out["coverage_days"] = {"funding": coverage(fund), "spot": coverage(spot),
                            "perp": coverage(perp), "mark": coverage(mark)}
    out["rows"] = {"funding": len(fund or []), "spot": len(spot or []),
                   "perp": len(perp or []), "mark": len(mark or [])}
    if not fund or not spot or not perp:
        out["status"] = "INSUFFICIENT_DATA"
        return out

    interval = infer_interval_hours([t for t, _ in fund])
    meta_interval = (info or {}).get("perp", {}).get("funding_interval_h_meta")
    out["funding_interval_h"] = {"inferred_from_history": interval,
                                 "metadata": meta_interval,
                                 "now_endpoint": (now_f or {}).get("interval_h"),
                                 "status": "VERIFIED"}
    rates = [r for _, r in fund]
    out["funding_stats"] = funding_stats(rates, interval)
    out["funding_now"] = now_f

    spot_d, perp_d, mark_d = dict(spot), dict(perp), dict(mark or [])
    common = sorted(set(spot_d) & set(perp_d))
    out["basis_stats"] = basis_stats([basis_pct(perp_d[t], spot_d[t]) for t in common])

    # Costos: fees efectivas (máx config/ccxt) + spread/profundidad del libro actual.
    fees = effective_fees(cfg.fees[ex],
                          (info or {}).get("spot", {}).get("ccxt_taker_fee"),
                          (info or {}).get("perp", {}).get("ccxt_taker_fee"))
    pair_cfg = FundingConfig(**{**cfg.__dict__, "fees": {**cfg.fees, ex: fees}})
    notional = cfg.notional_for_capital()
    half_s = half_p = slip_s = slip_p = None
    if books and books["spot_bids"] and books["spot_asks"] and books["perp_bids"]:
        sm = (books["spot_bids"][0][0] + books["spot_asks"][0][0]) / 2
        pm = (books["perp_bids"][0][0] + books["perp_asks"][0][0]) / 2
        half_s = (books["spot_asks"][0][0] - sm) / sm
        half_p = (books["perp_asks"][0][0] - pm) / pm
        q = notional / sm
        slip_s = slippage_vs_mid(books["spot_asks"], q, sm, "buy")
        slip_p = slippage_vs_mid(books["perp_bids"], q, pm, "sell")
        slip_s = None if slip_s is None else max(slip_s - half_s, 0.0)
        slip_p = None if slip_p is None else max(slip_p - half_p, 0.0)
        out["book_now"] = {"spot_mid": sm, "perp_mid": pm, "spot_half_spread": half_s,
                           "perp_half_spread": half_p,
                           "spot_depth_usd_top20": sum(p * a for p, a in books["spot_asks"][:20]),
                           "perp_depth_usd_top20": sum(p * a for p, a in books["perp_bids"][:20])}
    costs: CostBreakdown = round_trip_costs(
        pair_cfg, ex, spot_half_spread=half_s, perp_half_spread=half_p,
        spot_depth_slip=slip_s, perp_depth_slip=slip_p)
    leg_fail = pair_cfg.leg_fail_prob.value * (
        2 * fees["spot_taker"].value + pair_cfg.unmatched_penalty.value)
    out["costs"] = costs.as_dict()
    out["round_trip_cost_pct"] = costs.total
    out["leg_fail_expected_cost_pct"] = leg_fail
    mean_rate = out["funding_stats"]["mean"]
    out["breakeven_periods_at_mean_rate"] = (
        (costs.total + leg_fail) / mean_rate if mean_rate > 0 else None)

    # Factibilidad con US$100 (tamaños mínimos reales del exchange).
    price = spot[-1][1]
    qty = notional / price
    feas = {"notional_per_leg_usd": round(notional, 2), "qty": qty}
    if mins:
        feas.update({k: v for k, v in mins.items()})
        feas["feasible"] = (qty >= mins["spot_min_qty"] and qty >= mins["perp_min_qty"]
                            and notional >= mins["spot_min_cost"]
                            and notional >= mins["perp_min_cost"])
        need = max(mins["spot_min_qty"] * price, mins["perp_min_qty"] * price,
                   mins["spot_min_cost"], mins["perp_min_cost"])
        feas["min_notional_per_leg_usd"] = round(need, 2)
        feas["min_capital_usd"] = round(need * (1 + 1 / cfg.leverage) / cfg.allocation, 2)
    else:
        feas["feasible"] = None
    out["feasibility_100usd"] = feas

    bt = backtest(fund, spot_d, perp_d, mark_d, interval_hours=interval,
                  round_trip_cost_pct=costs.total, cfg=pair_cfg, exchange=ex,
                  notional=notional, leg_fail_cost_pct=leg_fail)
    out["backtest"] = bt.summary(notional)
    out["backtest"]["executable_trades_100usd"] = (
        out["backtest"]["trades"] if feas.get("feasible") else 0)
    out["trades"] = [{**asdict(t), "hold_hours": t.hold_hours} for t in bt.trades]
    out["status"] = "OK"
    log.info("  %s %s: funding medio %.5f%% c/%sh, costo ida+vuelta %.3f%%, "
             "trades %d, net-positive %d, neto US$%+.3f, factible %s",
             ex, asset, 100 * mean_rate, interval, 100 * costs.total,
             out["backtest"]["trades"], out["backtest"]["net_positive_trades"],
             out["backtest"]["net_usd_total"], feas.get("feasible"))
    return out


def sensitivity(storage, pair_result, cfg: FundingConfig, horizons=(7, 14, 30, 60)):
    """Misma regla y mismos datos guardados, variando el horizonte de decisión.

    No reemplaza el resultado base: muestra qué horizonte haría falta para que
    aparezcan entradas y si esas entradas terminaron en neto positivo.
    """
    ex, asset = pair_result["exchange"], pair_result["asset"]
    fund = storage.load_funding(ex, asset)
    spot = dict(storage.load_prices(ex, asset, "spot"))
    perp = dict(storage.load_prices(ex, asset, "perp"))
    mark = dict(storage.load_prices(ex, asset, "mark"))
    interval = (pair_result.get("funding_interval_h") or {}).get("inferred_from_history")
    out = {}
    for h in horizons:
        c = FundingConfig(**{**cfg.__dict__, "horizon_days": float(h),
                             "max_hold_days": max(cfg.max_hold_days, 2.0 * h)})
        bt = backtest(fund, spot, perp, mark, interval_hours=interval,
                      round_trip_cost_pct=pair_result["round_trip_cost_pct"], cfg=c,
                      exchange=ex, notional=cfg.notional_for_capital(),
                      leg_fail_cost_pct=pair_result["leg_fail_expected_cost_pct"])
        sm = bt.summary(cfg.notional_for_capital())
        out[str(h)] = {k: sm[k] for k in ("decisions", "ex_ante_positive", "trades",
                                          "net_positive_trades", "net_usd_total",
                                          "funding_usd_total", "basis_pnl_usd_total",
                                          "costs_usd_total", "mean_hold_hours",
                                          "rebalances", "liquidations")}
    return out
