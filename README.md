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
