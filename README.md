# Pie a Pie — investigación de arbitraje (PAPER ONLY)

Todo es experimental y en paper trading: `paper_only = True` se verifica al
arrancar. No hay órdenes reales, retiros ni claves de API.

## Estrategias

| Estrategia | Qué hace | Dónde corre | Datos |
|---|---|---|---|
| `kalshi_current` | YES en todas las patas de un evento excluyente **y exhaustivo** | GitHub Actions (`scanner.py`) | `data/*.csv`, `data/state.json` |
| `buy_all_no` | NO en un subconjunto de patas de un evento excluyente (paga ≥ k−1; no necesita exhaustividad) | GitHub Actions (`kalshi_strategies.py`) | `data/strategies/buy_all_no/` |
| `strike_inconsistency` | Escaleras de strikes no monótonas: YES en el amplio + NO en el angosto (paga ≥ 1) | GitHub Actions (`kalshi_strategies.py`) | `data/strategies/strike_inconsistency/` |
| `funding_basis` | Spot largo + perpetuo corto en el mismo exchange (Binance, Bybit, OKX) | PC local (`run_funding.py`) | `funding_data/` (SQLite, fuera de git) + `reports/funding_basis/` |

Cada estrategia tiene su propio capital virtual (US$100), posiciones, P&L,
rachas y registros. Nunca se mezclan.

## Laboratorio paralelo (`run_lab.py`, PC local)

Motor común (`lab/core.py`) + un módulo por estrategia, todos en paralelo sobre
un snapshot compartido por tick:

| Módulo | Estrategia | Fuentes públicas |
|---|---|---|
| `cross_exchange` | Comprar en A, vender en B (inventario prepuesto) | libros spot Binance, Bybit, OKX, Kraken, Coinbase |
| `triangular` | USDT → X → Y → USDT en un exchange | libros spot (BTC, ETH, SOL) |
| `basis_funding` | Spot largo + perp corto (reusa `funding/`) | libros spot/perp + funding |
| `polymarket_buy_all_no` | NO en k opciones de un evento negRisk (paga ≥ k−1) | Gamma + CLOB de Polymarket |
| `prediction_cross_venue` | Kalshi ↔ Polymarket, **solo pares verificados a mano** | `config/prediction_pairs.json` |
| `liquidity_provision` | Órdenes límite al mejor precio, modelo de cola | libros + trades públicos |

- Evidencia separada: **OBSERVADO** (datos crudos) → **ESTIMADO** (neto con
  costos modelados) → **SIMULADO** (latencia real con libro re-pedido, fills
  parciales, pata fallida, oportunidad desaparecida).
- Liquidez compartida: lo que una estrategia consume en un tick no está para otra.
- Cada tick guarda los snapshots crudos: `run_lab.py replay` reproduce exacto.
- Veredicto "RENTABLE" solo con ≥ 30 ejecuciones simuladas, ≥ 6 períodos,
  neto > 0, fuera de muestra > 0, estrés de costos x1.5 > 0, ≥ 60% de
  períodos positivos y P&L realizado (no solo esperado).

```powershell
python run_lab.py run --ticks 100 --interval-sec 45 --seed 7
python run_lab.py replay --seed 7          # sobre los snapshots guardados
python run_lab.py report --notify          # reports/lab/ + resumen [LAB] por ntfy
python run_lab.py suggest-pairs            # candidatas Kalshi~Polymarket (UNVERIFIED)
```

`lab_data/` (SQLite) queda fuera de git. El laboratorio no escribe en `data/`.

### Familias y comandos (versión multiestrategia)

| Familia | Módulo | Naturaleza |
|---|---|---|
| A. Entre exchanges | `cross_exchange` (inventario por par; rebalanceo solo al agotarse) | arbitraje |
| B. Triangular 3-4 patas | `triangular` | arbitraje |
| C. Basis/funding perpetuo | `basis_funding` (vivo) + `run_funding.py phase0` | estadística |
| D. Predicción | `polymarket_buy_all_no`, `prediction_cross_venue`, Kalshi en Actions | arbitraje / no verificable |
| E. CEX vs DEX | `cex_dex` (Jupiter, mínimo garantizado, re-cotización) | arbitraje no atómico |
| F. Futuros con vencimiento | `cash_and_carry`, `calendar_spread` | arbitraje / estadística |
| G. ETF y ADR/CCL | `research --study etf` | estadística (ejecución no verificable) |
| H. Pares cointegrados | `research --study stat_arb` | estadística |
| I. Microestructura | `liquidity_provision`, `research --study imbalance` | estadística |
| Descubrimiento | `research --study discovery` (criterios congelados, BH global) | estadística |

Categorías (nunca se mezclan): ARBITRAJE_GARANTIZADO, ESTADISTICA,
NO_EJECUTABLE, NO_VERIFICABLE, SIN_EDGE (+ ESPECULATIVA aparte).

```powershell
python run_lab.py collect --ticks 9 --interval-sec 0 --max-minutes 9 --run R   # recolección (checkpoint por tick)
python run_lab.py collect --resume --run R --ticks 9                           # reanudar
python run_lab.py evaluate --run R --seed 7                                    # evaluación tick a tick
python run_lab.py research --study all                                         # G, H, I y descubrimiento
python run_lab.py consolidate                                                  # reports/lab/consolidated.md
```

La guardia de recursos (`--max-rss-mb`, `--max-minutes`) corta ordenadamente
guardando el checkpoint; la caché histórica nunca vuelve a descargar lo que ya tiene.

## Comandos

```powershell
# Kalshi (lo mismo que corre Actions)
python scanner.py --max-events 250 --interval-min 25      # kalshi_current
python kalshi_strategies.py --interval-min 25             # buy_all_no + strike_inconsistency
python scanner.py --report                                # reporte de kalshi_current
python -m src.compare                                     # comparación de las 4 estrategias

# Funding/basis (PC local)
pip install -r requirements-funding.txt
python run_funding.py probe         # verifica endpoints públicos REST
python run_funding.py probe-ws      # verifica WebSocket
python run_funding.py phase0        # Fase 0: ~90 días históricos
python run_funding.py live --once   # un tick de paper en vivo
python run_funding.py live          # proceso persistente (Ctrl+C corta); --ws para WebSocket
python run_funding.py report
```

## Clasificación de oportunidades (`src/guarantee.py`)

Cada oportunidad se clasifica como **ARBITRAJE_GARANTIZADO**, **ESPECULATIVA**,
**NO_VERIFICABLE** o **SIN_EDGE**. Solo una garantizada abre posición paper.
Garantizada exige: (1) cubrir TODOS los resultados con prueba positiva
(partición completa de strikes de una variable, partido "A vs B" con empate, o
verificación manual en `config/exhaustive_events.json`); (2) ejecución
verificada sobre libros pedidos de nuevo tras la latencia (volumen completo,
desfase entre patas ≤ 5 s); (3) neto mínimo > 0 con costos supuestos x1.5.
Una pata "Tie" ya no cubre resultados no listados (auditoría KXCRITICSCOM-27).
Auditorías: `data/opportunity_audit.csv`, `data/strategies/*/audit.csv`;
libros T0/T1 de cada oportunidad auditada en `evidence/`. Posiciones abiertas:
`python audit_positions.py` (solo lectura).

## Controles contra falsos positivos

- Ganancia bruta > 10% del costo: `SUSPICIOUS_EDGE_CHECK_RULES`, nunca ejecutable.
- `strike_inconsistency` agrupa por evento + tipo de strike + `rules_primary`
  con números → `#`, y exige raíz de ticker consistente (`GROUPING_MISMATCH`,
  `AMBIGUOUS_GROUP`). Hay tests de regresión con los casos reales que
  produjeron 14.274 falsos candidatos.
- `BUDGET_TOO_SMALL` cuando el paquete mínimo no entra en el 10% del capital.
- `INSUFFICIENT_DEPTH` cuando hay edge pero el libro no llega a 1 contrato.

## Costos de funding/basis

Cada costo lleva estado: `VERIFIED` (leído de una fuente pública), `ASSUMED`
(tarifa pública estándar, no verificada por cuenta) o `UNVERIFIED`. Las
tarifas por cuenta requieren autenticación y no se usan.

## Antes de cualquier dinero real (NO verificado)

- Acceso y legalidad desde Argentina de cada exchange y de los **derivados**
  (las inscripciones PSAV en la CNV listan intercambio, transferencia y
  custodia; no derivados). Una inscripción o una API que responde no es una
  habilitación para operar.
- Comisiones reales por cuenta, límites y condiciones de uso.
- Acceso real a Kalshi desde Argentina.
