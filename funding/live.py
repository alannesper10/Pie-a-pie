"""Fase 1 (paper en vivo): un tick evalúa cada (exchange, activo).

Por tick: libros + funding actual -> snapshot -> retorno neto esperado ->
apertura/actualización/cierre de la oportunidad -> paper (entrada con latencia
real y fills parciales; funding, rebalanceo, salida).
"""

import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .basis import basis_pct
from .config import FundingConfig, effective_fees
from .costs import round_trip_costs, slippage_vs_mid
from .funding import expected_funding_pct, infer_interval_hours, trailing_mean
from .paper import FundingPaperLedger, simulate_entry, simulate_exit
from .risk import capital_required, liquidation_distance, risk_flags, short_liquidation_price

HOUR_MS = 3_600_000


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def evaluate_snapshot(*, books, funding_now, trailing_rates, cfg: FundingConfig,
                      exchange, notional, interval_h, mins=None):
    """Evaluación pura de un snapshot. Devuelve dict con todos los campos."""
    sb, sa = books["spot_bids"], books["spot_asks"]
    pb, pa = books["perp_bids"], books["perp_asks"]
    if not (sb and sa and pb and pa):
        return {"ok": False, "reason": "EMPTY_BOOK"}
    sm, pm = (sb[0][0] + sa[0][0]) / 2, (pb[0][0] + pa[0][0]) / 2
    half_s, half_p = (sa[0][0] - sm) / sm, (pa[0][0] - pm) / pm
    qty = notional / sa[0][0]
    slip_s = slippage_vs_mid(sa, qty, sm, "buy")
    slip_p = slippage_vs_mid(pb, qty, pm, "sell")
    depth_ok = slip_s is not None and slip_p is not None
    costs = round_trip_costs(
        cfg, exchange, spot_half_spread=half_s, perp_half_spread=half_p,
        spot_depth_slip=None if slip_s is None else max(slip_s - half_s, 0.0),
        perp_depth_slip=None if slip_p is None else max(slip_p - half_p, 0.0))
    leg_fail = cfg.leg_fail_prob.value * (2 * cfg.fee(exchange, "spot_taker").value
                                          + cfg.unmatched_penalty.value)
    rate = funding_now.get("rate")
    trailing = trailing_mean(trailing_rates, cfg.trailing_periods) if trailing_rates else None
    if rate is None or interval_h is None:
        return {"ok": False, "reason": "NO_FUNDING_DATA"}
    # Conservador: la menor entre la tasa actual y la media reciente.
    exp_rate = min(rate, trailing) if trailing is not None else rate
    exp_net = (expected_funding_pct(exp_rate, interval_h, cfg.horizon_days * 24)
               - costs.total - leg_fail)
    mark = funding_now.get("mark") or pm
    liq = short_liquidation_price(pm, cfg.leverage, cfg.maintenance_margin.value)
    feasible = True
    if mins:
        feasible = (qty >= mins["spot_min_qty"] and qty >= mins["perp_min_qty"]
                    and notional >= mins["spot_min_cost"]
                    and notional >= mins["perp_min_cost"])
    return {
        "ok": True, "spot_bid": sb[0][0], "spot_ask": sa[0][0], "perp_bid": pb[0][0],
        "perp_ask": pa[0][0], "mark": mark, "mark_status": (
            "VERIFIED" if funding_now.get("mark") else "ASSUMED (mid del perp)"),
        "index_price": funding_now.get("index"), "funding_rate": rate,
        "trailing_rate": trailing, "expected_rate": exp_rate,
        "funding_interval_h": interval_h, "next_funding_ts": funding_now.get("next_ts"),
        "basis_pct": basis_pct(pm, sm),
        "spot_depth_usd": sum(p * q for p, q in sa), "perp_depth_usd": sum(p * q for p, q in pb),
        "cost_pct": costs.total, "leg_fail_cost_pct": leg_fail, "costs": costs.as_dict(),
        "expected_net_pct": exp_net, "notional": notional, "qty": qty,
        "capital_required": capital_required(notional, cfg.leverage),
        "margin": notional / cfg.leverage, "leverage": cfg.leverage,
        "liq_distance": liquidation_distance(pm, liq), "feasible_100usd": feasible,
        "annualized_net_pct": exp_net * (365 / cfg.horizon_days),
        "risks": risk_flags(expected_rate=exp_rate, trailing_rate=trailing or 0.0,
                            basis_pct=basis_pct(pm, sm),
                            liq_distance=liquidation_distance(pm, liq),
                            depth_ok=depth_ok, exchange=exchange),
    }


@dataclass
class LiveState:
    ledger: FundingPaperLedger
    pending_funding: dict = field(default_factory=dict)   # key -> (ts, rate)


class LiveRunner:
    def __init__(self, cfg: FundingConfig, adapters, storage, books_source, log,
                 seed=None, sleep=time.sleep):
        self.cfg, self.adapters, self.storage = cfg, adapters, storage
        self.books, self.log, self.sleep = books_source, log, sleep
        self.rng = random.Random(seed)
        self.state = LiveState(FundingPaperLedger.from_dict(
            storage.get("paper_ledger"), cfg.starting_capital_usd))
        self.meta = {}

    def _meta(self, ex, asset):
        k = (ex, asset)
        if k not in self.meta:
            a = self.adapters[ex]
            info = a.market_info(asset)
            fees = effective_fees(self.cfg.fees[ex], info["spot"]["ccxt_taker_fee"],
                                  info["perp"]["ccxt_taker_fee"])
            hist = a.fetch_funding_history(
                asset, int(time.time() * 1000) - 10 * 24 * HOUR_MS)
            self.meta[k] = {"mins": a.min_qty(asset), "fees": fees,
                            "rates": [r for _, r in hist],
                            "interval": infer_interval_hours([t for t, _ in hist])}
        return self.meta[k]

    def tick(self):
        ts = now_iso()
        results = {}
        for ex, a in self.adapters.items():
            for asset in self.cfg.assets:
                try:
                    results[(ex, asset)] = self._tick_pair(ex, asset, ts)
                except Exception as e:  # noqa: BLE001 - un par no corta el tick
                    self.storage.log_error(ts, ex, f"tick:{asset}", e)
                    self.log.warning("  %s %s: error %s", ex, asset, e)
        self.storage.put("paper_ledger", self.state.ledger.to_dict())
        return results

    def _tick_pair(self, ex, asset, ts):
        meta = self._meta(ex, asset)
        cfg = FundingConfig(**{**self.cfg.__dict__, "fees": {**self.cfg.fees, ex: meta["fees"]}})
        fnow = self.adapters[ex].fetch_funding_now(asset)
        interval = fnow.get("interval_h") or meta["interval"]
        books = self.books.get(ex, asset)
        # Tamaño de referencia fijo (capital inicial) para que las oportunidades
        # sean comparables; la apertura paper verifica la caja disponible.
        notional = cfg.notional_for_capital()
        snap = evaluate_snapshot(books=books, funding_now=fnow, trailing_rates=meta["rates"],
                                 cfg=cfg, exchange=ex, notional=notional,
                                 interval_h=interval, mins=meta["mins"])
        if not snap["ok"]:
            self.storage.log_error(ts, ex, f"snapshot:{asset}", snap["reason"])
            return snap
        self.storage.save_snapshot({**snap, "ts": ts, "exchange": ex, "asset": asset,
                                    "detail": {"risks": snap["risks"],
                                               "mark_status": snap["mark_status"]}})
        self._track_opportunity(ex, asset, ts, snap)
        self._paper(ex, asset, ts, snap, cfg, fnow)
        return snap

    def _track_opportunity(self, ex, asset, ts, snap):
        opp_id = self.storage.open_opportunity_id(ex, asset)
        size = snap["notional"] if snap["feasible_100usd"] else 0.0
        if snap["expected_net_pct"] > 0:
            if opp_id:
                self.storage.update_opportunity(opp_id, snap["expected_net_pct"], size)
            else:
                self.storage.open_opportunity(ex, asset, ts, snap["expected_net_pct"], size,
                                              {"feasible_100usd": snap["feasible_100usd"]})
        elif opp_id:
            self.storage.close_opportunity(opp_id, ts)   # la oportunidad desapareció

    def _paper(self, ex, asset, ts, snap, cfg, fnow):
        led = self.state.ledger
        key = led.key(ex, asset)
        pos = led.open.get(key)
        now_ms = int(time.time() * 1000)
        if pos:
            pend = self.state.pending_funding.get(key)
            if pend and now_ms >= pend[0]:
                pay = led.accrue_funding(pos, pend[1], snap["mark"], pend[0])
                self.storage.log_paper(ts, ex, asset, "FUNDING", {"rate": pend[1], "usd": pay})
            if fnow.get("next_ts") and fnow.get("rate") is not None:
                self.state.pending_funding[key] = (int(fnow["next_ts"]), float(fnow["rate"]))
            event = led.check_risk(pos, snap["mark"], cfg)
            if event == "REBALANCE":
                self.storage.log_paper(ts, ex, asset, "REBALANCE",
                                       {"cost": pos.rebalance_costs})
            held_d = (datetime.fromisoformat(ts) -
                      datetime.fromisoformat(pos.opened_at)).total_seconds() / 86400
            reason = ("LIQUIDATION" if event == "LIQUIDATION" else
                      "FUNDING_TURNED_NEGATIVE" if (snap["trailing_rate"] or 0) < 0 else
                      "MAX_HOLD" if held_d >= cfg.max_hold_days else None)
            if reason:
                self.sleep(cfg.latency_ms.value / 1000)
                b = self.books.get(ex, asset)
                s_avg, p_avg, fees, extra = simulate_exit(
                    spot_bids=b["spot_bids"], perp_asks=b["perp_asks"], qty=pos.qty,
                    cfg=cfg, exchange=ex)
                net = led.close_position(pos, spot_exit=s_avg, perp_exit=p_avg,
                                         exit_fees=fees, exit_extra=extra, ts=ts, reason=reason)
                self.storage.log_paper(ts, ex, asset, "CLOSE", {"reason": reason, "net": net})
            return
        if snap["expected_net_pct"] <= 0 or not snap["feasible_100usd"]:
            return
        if snap["capital_required"] > led.cash:
            self.storage.log_paper(ts, ex, asset, "SKIP_NO_CASH", {"cash": led.cash})
            return
        # Latencia real: se vuelve a pedir el libro después de esperar.
        self.sleep(cfg.latency_ms.value / 1000)
        b = self.books.get(ex, asset)
        entry = simulate_entry(spot_asks=b["spot_asks"], spot_bids=b["spot_bids"],
                               perp_bids=b["perp_bids"], qty=snap["qty"], cfg=cfg,
                               exchange=ex, rng=self.rng)
        pos = led.open_position(entry, exchange=ex, asset=asset, leverage=cfg.leverage, ts=ts)
        self.storage.log_paper(ts, ex, asset, "OPEN" if pos else entry.status, {
            "status": entry.status, "qty": entry.qty, "unmatched_qty": entry.unmatched_qty,
            "unmatched_cost": entry.unmatched_cost, "fees": entry.fees,
            "expected_net_pct": snap["expected_net_pct"]})
