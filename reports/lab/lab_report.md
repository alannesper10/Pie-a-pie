# Laboratorio Pie a Pie — replay-live-20261013T142551-s7-143357

Modo: replay · inicio 2026-10-13T17:33:57.635+00:00 · semilla 7 · replay de live-20261013T142551

Todo es SIMULADO. OBSERVADO = datos públicos crudos; ESTIMADO = neto con costos modelados; SIMULADO = ejecución con latencia, fills parciales y liquidez compartida.

## Comparación por estrategia

| Estrategia | Observadas | Estimadas > 0 | Ejecutadas (sim) | Rentables (sim) | Neto sim. | Capital comprometido | Retorno s/ capital | Peor/mejor (p5/p95) | Veredicto |
|---|---|---|---|---|---|---|---|---|---|
| cross_exchange | 147 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |
| liquidity_provision | 33 | 0 | 33 | 0 | US$-0.4113 | US$660.00 | -0.062% | -0.095% / -0.036% | **ESPECULATIVA (no es arbitraje)** |
| polymarket_buy_all_no | 319 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |
| prediction_cross_venue | 0 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **NO VERIFICABLE** |
| triangular | 41 | 0 | 0 | 0 | US$+0.0000 | US$0.00 | n/d | n/d / n/d | **SIN EVIDENCIA SUFICIENTE** |

**Consolidado:** 5 estrategias, capital US$500 (separado), ejecutadas 33, rentables 0, neto simulado US$-0.4113, realizado en ledgers US$-0.4554.

## Por categoría pedida

- **1. Entre exchanges (cripto)** — cross_exchange: SIN EVIDENCIA SUFICIENTE
- **2. Basis spot-futuros / funding** — no corrió en esta ejecución
- **3. Triangular** — triangular: SIN EVIDENCIA SUFICIENTE
- **4. Mercados de predicción** — polymarket_buy_all_no: SIN EVIDENCIA SUFICIENTE; prediction_cross_venue: NO VERIFICABLE
- **5. Provisión de liquidez** — liquidity_provision: ESPECULATIVA (no es arbitraje)

## Evidencia externa (no recalculada)

- kalshi_current: source=data/ (GitHub Actions, solo lectura), cycles=384, opportunities=62860, net_positive=2, executable=2, pnl_realized=0
- buy_all_no: source=data/ (GitHub Actions, solo lectura), cycles=368, opportunities=55082, net_positive=0, executable=0, pnl_realized=0
- strike_inconsistency: source=data/ (GitHub Actions, solo lectura), cycles=368, opportunities=54093, net_positive=0, executable=0, pnl_realized=0
- funding_phase0: source=reports\funding_basis, phase0_decisions=2412, cycles=45, opportunities=0, net_positive=0, executable=0, pnl_realized=0.0

## Detalle

### cross_exchange

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NO_EDGE_AFTER_FEES=147
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 5, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'cross_exchange', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### liquidity_provision

- Veredicto: **ESPECULATIVA (no es arbitraje)** — neto simulado -0.4113 USD; 33 ejecuciones simuladas (mín 30), 2 períodos (mín 6); neto simulado negativo
- Motivos: FILL=33
- Pérdidas: 33 (US$-0.4113)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 2, positivos 0%
- Estrés x1.5: estimadas > 0 0, neto sim. US$-0.5763 · x2: 0, US$-0.7413
- Fuera de muestra: {'split_tick': 5, 'threshold': 0.0, 'in_sample_trades': 15, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'liquidity_provision', 'capital': 100.0, 'cash': 99.54462275412706, 'locked': 0.0, 'peak_locked': 60.0, 'realized': -0.4553772458729348, 'trades': 1, 'return_on_capital': -0.004553772458729348}

### polymarket_buy_all_no

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NO_BOOK_FOR_LEG=149, NO_EDGE_AFTER_FEES_OR_MIN_SIZE=110, BUDGET_TOO_SMALL=60
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 5, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'polymarket_buy_all_no', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### prediction_cross_venue

- Veredicto: **NO VERIFICABLE** — sin pares verificados a mano
- Motivos: ninguno
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'status': 'INSUFICIENTES_TICKS'}
- Ledger: {'strategy': 'prediction_cross_venue', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

### triangular

- Veredicto: **SIN EVIDENCIA SUFICIENTE** — 0 ejecuciones simuladas (mín 30), 0 períodos (mín 6)
- Motivos: NET_NEGATIVE_AFTER_COSTS=41
- Pérdidas: 0 (US$+0.0000)
- Duración (ticks con neto estimado > 0): n/d
- Períodos (10 min): 0, positivos n/d
- Estrés x1.5: estimadas > 0 0, neto sim. US$+0.0000 · x2: 0, US$+0.0000
- Fuera de muestra: {'split_tick': 5, 'threshold': 0.0, 'in_sample_trades': 0, 'in_sample_net': 0, 'out_of_sample_trades': 0, 'out_of_sample_net': 0}
- Ledger: {'strategy': 'triangular', 'capital': 100.0, 'cash': 100.0, 'locked': 0.0, 'peak_locked': 0.0, 'realized': 0.0, 'trades': 0, 'return_on_capital': 0.0}

## Errores de fuentes

Total: 0
