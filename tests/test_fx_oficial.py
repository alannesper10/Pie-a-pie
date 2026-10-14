"""Simulador oficial -> USDT -> ARS: límites de anuncios, profundidad y fórmula del rendimiento."""

import pytest

from lab.research import fx_oficial as fx
from lab.research.fx_oficial import Ad, Route


def test_buy_ads_respect_min_max_qty_and_methods():
    ads = [Ad(1.00, 100, 50, 1000, ["BACcostarica"]),          # más barato pero medio no usable
           Ad(1.05, 300, 200, 400, ["BankArgentina"]),          # máx 300 USDT * 1.05 = 315 USD
           Ad(1.06, 10_000, 100, 15_000, ["NaranjaX"])]
    usdt, spent, orders = fx.take_ads_buy(ads, 1000, usable_methods=["BankArgentina", "NaranjaX"])
    assert [o["price"] for o in orders] == [1.05, 1.06]
    assert orders[0]["fiat"] == pytest.approx(315)
    assert spent == pytest.approx(1000)
    assert usdt == pytest.approx(315 / 1.05 + 685 / 1.06)


def test_remaining_below_ad_minimum_is_not_filled():
    ads = [Ad(1.05, 10_000, 500, 600, ["BankArgentina"])]
    usdt, spent, _ = fx.take_ads_buy(ads, 400, ["BankArgentina"])
    assert usdt == 0 and spent == 0                        # 400 < mínimo 500: no se opera


def test_book_sell_walks_levels():
    ars, sold = fx.take_book_sell([(1600, 10), (1590, 10)], 15)
    assert sold == 15 and ars == pytest.approx(10 * 1600 + 5 * 1590)


def test_simulate_net_formula_and_breakeven():
    r = Route("t", "BNA", 1535.0, "p2p", usable_methods=["BankArgentina"])
    ads = [Ad(1.06, 1e6, 1, 1e9, ["BankArgentina"])]
    out = fx.simulate(r, 1_535_000, usd_ads=ads, binance_bids=[(1615.0, 1e9)])
    usd = 1000.0
    usdt = usd / 1.06
    ars = usdt * 1615 * (1 - 0.001)
    assert out["status"] == "OK"
    assert out["ars_final"] == pytest.approx(ars)
    assert out["net_pct"] == pytest.approx((ars - 1_535_000) / 1_535_000 * 100)
    assert out["net_pct"] < 0                               # a 1,06 USD/USDT la brecha desaparece
    assert out["breakeven_usd_per_usdt"] == pytest.approx(1615 * 0.999 / 1535)
    assert fx.breakeven_usd_per_usdt(1535, 1615) == pytest.approx(1615 * 0.999 / 1535)


def test_insufficient_liquidity_is_reported_not_extrapolated():
    r = Route("t", "BNA", 1535.0, "p2p", usable_methods=["BankArgentina"])
    out = fx.simulate(r, 15_350_000, usd_ads=[Ad(1.0, 100, 1, 1e9, ["BankArgentina"])],
                      binance_bids=[(1615.0, 1e9)])
    assert out["status"] == "SIN_LIQUIDEZ_O_LIMITES" and out["net_pct"] is None
    assert out["steps"]["usd_unconverted"] == pytest.approx(10_000 - 100)
    out = fx.simulate(Route("t", "BNA", 1535.0, "platform", platform_usdt_ask=1.0), 1_535_000,
                      binance_bids=[(1615.0, 10)])
    assert out["status"] == "SIN_LIQUIDEZ_O_LIMITES" and out["steps"]["usdt_unsold"] == pytest.approx(990)


def test_mercadopago_route_cannot_pay_third_party_ads():
    # MP solo transfiere USD a cuentas propias: ningún anuncio P2P es usable
    r = Route("mp", "MercadoPago", 1535.0, "p2p", usable_methods=[])
    out = fx.simulate(r, 153_500, usd_ads=[Ad(1.0, 1e6, 1, 1e9, ["MercadoPagoNew"])],
                      binance_bids=[(1615.0, 1e9)])
    assert out["status"] == "SIN_LIQUIDEZ_O_LIMITES"
