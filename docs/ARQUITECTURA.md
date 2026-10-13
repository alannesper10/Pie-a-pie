# Pie a Pie — Arquitectura (v1, 13/10/2026)

Pie a Pie funciona en dos modos independientes y SIEMPRE en paper
(`PAPER_ONLY = True` se verifica al arrancar; no hay claves ni órdenes reales).

- **Modo 1, autónomo.** Busca oportunidades económicas propias (arbitraje,
  basis, predicción, liquidez, ejecución) y las clasifica según la evidencia.
- **Modo 2, ejecutor de HORUS.** Recibe órdenes estructuradas y versionadas,
  las valida contra sus propios límites, elige la ruta más eficiente, ejecuta
  en paper e informa estado, costos, desvíos y resultado.

HORUS es la autoridad estratégica; Pie a Pie no reemplaza su tesis. Ninguno
depende del otro para funcionar: se comunican solo por mensajes JSON
versionados (ver §3), sin código, procesos ni datos mutables compartidos.

## 1. Diagnóstico de la arquitectura actual

| Capa | Componentes | Estado |
|---|---|---|
| Kalshi en producción paper | `scanner.py`, `kalshi_strategies.py`, `src/` (`guarantee`, `execution_check`, `paper_trader`, `compare`, `notify`), `.github/workflows/scan.yml` y `daily.yml` | Estable. Escribe `data/` (dataset oficial; solo lo escribe el bot). Dos posiciones históricas intactas. |
| Funding/basis | `funding/` (adaptadores, costos, riesgo, `paper`, `live`, `phase0`), `run_funding.py` | Estable, local. `funding_data/` fuera de git. |
| Laboratorio | `lab/core.py` (Opportunity, LiquidityRegistry, walk, StrategyLedger, `classify_lab`), `lab/sources.py`, `lab/runner.py`, `lab/store.py`, `lab/modules/*` (A, B, C, D, E, F, I-liquidez), `lab/evaluate.py`, `lab/consolidated.py`, `lab/episodes.py`, `run_lab.py` | Maduro. Evidencia separada OBSERVADO → ESTIMADO → SIMULADO; replay reproducible. |
| Investigación | `lab/research/` (`carry`, `ccl`, `pm_gaps`, `etf`, `stat_arb`, `imbalance`, `stats`), `lab/discovery.py` | `carry`, `ccl` y `pm_gaps` son de viabilidad y ejecución (propios de Pie a Pie). `stat_arb`, `etf`, `imbalance` y `discovery` son **descubrimiento general**: se superponen con HORUS. |
| Ejecución de órdenes externas | — | **No existe.** |
| Asignación de capital | Ledgers aislados por estrategia (`StrategyLedger`) | No hay asignador entre estrategias. |
| Registro económico común | `Opportunity.to_row()` (lab), CSV propios (Kalshi), ledger de funding | Tres formatos distintos; no hay un registro homogéneo realizado/no realizado. |

**Problemas detectados**

1. Tres registros económicos con formatos distintos: no se pueden comparar
   estrategias sin adaptar cada uno.
2. El descubrimiento general (`discovery`, `stat_arb`, `etf`) duplica la
   función de HORUS. Decisión: **congelarlo**. Se conserva para la
   reproducibilidad de los informes ya publicados, pero no se extiende.
3. No hay ejecutor, máquina de estados de órdenes, idempotencia ni auditoría
   de cambios de estado.
4. Las comisiones por cuenta no se pueden verificar sin claves: todo costo de
   trading es SUPUESTO salvo Polymarket (API) y BYMA (comunicado oficial).

## 2. Componentes: existentes, reutilizables y faltantes

| Necesidad | Existe | Se reutiliza | Falta |
|---|---|---|---|
| Libros públicos multi-exchange | `lab/sources.CryptoSource`, `FuturesSource`, `JupiterSource`, `PolymarketSource`, `CclSource` | sí | — |
| Barrido de libros y costos | `lab/core.walk`, `lab/fees` | sí | — |
| Latencia y re-pedido de libros | `lab/runner.build_snapshot`, `src/execution_check` | sí (patrón) | — |
| Clasificación por naturaleza | `src/guarantee`, `lab/core.classify_lab` | sí | — |
| Registro económico homogéneo | parcial | `Opportunity` | **`lab/record.py`** (EconomicRecord) |
| Interfaz HORUS | — | — | **`executor/schema.py`** (v1) |
| Idempotencia y auditoría | — | — | **`executor/store.py`** (eventos encadenados por hash) |
| Máquina de estados de órdenes | — | — | **`executor/state.py`** |
| Ruteo de ejecución | `walk` + `fees` | sí | **`executor/router.py`** (venue y división óptima con fees) |
| Límites de riesgo propios | `funding/risk` (basis) | parcial | **`executor/limits.py`** + `config/executor_limits.json` |
| Motor paper de órdenes | — | `StrategyLedger` (patrón) | **`executor/engine.py`** |
| Market making | `lab/modules/liquidity` (cola, selección adversa) | sí | inventario y cotización a dos puntas |
| Reversión / valor relativo | `lab/research/stat_arb` (descubrimiento) | solo la ejecución | ejecución de órdenes HORUS de pares |
| Tendencia / rupturas | — | — | solo ejecución de órdenes HORUS (entrada por disparo) |
| Volatilidad / opciones | — | `FuturesSource` (patrón Deribit) | fuente de opciones y modelo de costos y margen |
| Eventos | Kalshi/Polymarket (fuentes y fees) | sí | ejecución de órdenes HORUS sobre mercados de predicción |
| Asignación dinámica de capital | — | métricas del EconomicRecord | **`lab/allocator.py`** |

## 3. Interfaz HORUS → Pie a Pie (v1)

Transporte v1: archivos JSON en `executor_io/inbox/` (órdenes y
cancelaciones) y `executor_io/outbox/` (reportes). Es un buzón que cualquier
proceso puede escribir o leer, sin acoplar repositorios. HTTP o una cola se
pueden agregar después manteniendo los mismos mensajes. `executor_io/` está
fuera de git.

### 3.1 Orden — `horus.order/v1`

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `schema` | `"horus.order/v1"` | sí | versión del contrato |
| `order_id` | string 8–64 `[A-Za-z0-9_-]` | sí | único; clave de idempotencia |
| `issued_at`, `valid_until` | ISO-8601 UTC | sí | vencida: EXPIRED, nunca se ejecuta |
| `valid_from` | ISO-8601 | no | antes de esa hora espera |
| `issuer` | `"horus"` | sí | |
| `signature` | hex HMAC-SHA256 del JSON canónico sin `signature` | sí si hay clave | clave en `PIEAPIE_HORUS_HMAC_KEY` (entorno, nunca en código) |
| `mode` | `"paper"` | sí | cualquier otro valor: REJECTED (`REAL_MODE_NOT_AUTHORIZED`) |
| `strategy` | `{name, version, thesis_ref?}` | sí | Pie a Pie no la modifica |
| `instrument` | `{asset_class, symbol, venues_allowed[], venues_forbidden[]?}` | sí | v1: `crypto_spot` |
| `direction` | `"buy"` \| `"sell"` | sí | `sell` requiere inventario (no hay venta en corto en spot) |
| `sizing` | `{notional_usd}` o `{qty}` | sí | acotado por los límites propios |
| `entry` | `{type: market\|limit\|trigger, limit_price?, trigger_above?, trigger_below?, max_slippage_bps, max_wait_s, allow_partial}` | sí | |
| `exit` | `{take_profit?, stop?, time_exit_at?}` | no | |
| `risk` | `{max_loss_usd, max_fees_usd?, max_position_usd?}` | sí | |
| `invalidation` | lista de `{type: price_above\|price_below\|time_after, value}` | no | si se cumple antes de entrar: INVALIDATED |
| `on_problem` | `"halt_and_report"` | sí | único valor admitido: Pie a Pie no improvisa |
| `supersedes` | order_id | no | reemplazo explícito de una orden anterior |

### 3.2 Cancelación — `horus.cancel/v1`
`{schema, order_id, issued_at, reason, signature?}`. Cancela lo pendiente;
una posición abierta se cierra solo si la cancelación lo pide (`close_position: true`).

### 3.3 Estados y transiciones

```
RECEIVED ─┬─> REJECTED                       (validación, firma, límites, duplicado en conflicto)
          └─> ACCEPTED ─> WAITING_ENTRY ─┬─> ENTERING ─┬─> OPEN ─> EXITING ─> CLOSED
                                         │             ├─> CLOSED   (orden sell completa)
                                         │             └─> EXPIRED  (sin ejecución en max_wait_s)
                                         └─> INVALIDATED / EXPIRED / CANCELLED
HALTED_NEEDS_INSTRUCTION  <- desde ACCEPTED, WAITING_ENTRY, ENTERING, OPEN o EXITING
HALTED_NEEDS_INSTRUCTION  -> CANCELLED | EXITING (solo por cancelación de HORUS con close_position)
```

Las ejecuciones parciales se informan dentro de ENTERING (`filled_qty`). Al
vencer `max_wait_s`: sin ejecución, EXPIRED; parcial con
`allow_partial=true`, OPEN con lo ejecutado; parcial sin autorización,
HALTED_NEEDS_INSTRUCTION (Pie a Pie no deshace ni completa por su cuenta).
Implementación: `executor/state.py` (tabla de transiciones; cualquier otra se
rechaza).

Terminales: REJECTED, INVALIDATED, EXPIRED, CANCELLED, CLOSED. Cada
transición se registra como evento inmutable (append-only), encadenado por
hash con el anterior, así que una alteración del historial se detecta.

### 3.4 Idempotencia
- Mismo `order_id` y mismo contenido (hash canónico): no se hace nada y se
  devuelve el estado actual.
- Mismo `order_id` con contenido distinto: se rechaza el segundo mensaje
  (`DUPLICATE_ORDER_ID_CONFLICT`) y la orden original sigue igual.
- Las ejecuciones se identifican por `(order_id, fill_seq)`: un reproceso no
  duplica fills.

### 3.5 Reporte — `pieapie.report/v1`
`{schema, order_id, seq, ts, state, previous_state, reason_code, detail,
decision_price, fills[{venue, side, price, qty, fee_usd, fee_status, ts}],
avg_price, filled_qty, slippage_bps, costs{verified, assumed}, position_qty,
capital_locked_usd, realized_pnl_usd, unrealized_pnl_usd, data_sources[]}`.
Lo realizado y lo no realizado van siempre en campos separados.

### 3.6 Límites propios (no los anula ninguna orden)
`config/executor_limits.json`: `paper_only`, clases de activos y venues
permitidos, nocional máximo por orden, exposición total máxima, pérdida máxima
por orden y desvío máximo del precio de decisión. Se aplica el más
restrictivo entre la orden y estos límites.

### 3.7 Códigos de motivo (estables)
`SCHEMA_INVALID`, `SIGNATURE_INVALID`, `SIGNATURE_REQUIRED`,
`REAL_MODE_NOT_AUTHORIZED`, `EXPIRED`, `DUPLICATE_ORDER_ID_CONFLICT`,
`LIMIT_NOTIONAL`, `LIMIT_EXPOSURE`, `LIMIT_LOSS`, `VENUE_NOT_ALLOWED`,
`ASSET_CLASS_NOT_SUPPORTED`, `INSUFFICIENT_CAPITAL`, `INSUFFICIENT_INVENTORY`,
`NO_ROUTE`, `SLIPPAGE_EXCEEDED`, `PARTIAL_TIMEOUT`, `INVALIDATED`,
`STOP_HIT`, `TAKE_PROFIT_HIT`, `TIME_EXIT`, `DATA_UNAVAILABLE`,
`CANCELLED_BY_HORUS`.

## 4. Registro económico común (`lab/record.py`)

Todas las estrategias y el ejecutor informan con el mismo `EconomicRecord`:
capital comprometido y bloqueado (y por cuánto tiempo), precios observados y
ejecutados, bruto, costos verificados y supuestos, neto y % neto,
deslizamiento, fracción ejecutada, riesgo (pérdida máxima modelada),
exposición, **resultado realizado y no realizado por separado**, naturaleza y
categoría, procedencia y calidad de los datos, evidencia (OBSERVADO,
ESTIMADO, SIMULADO o REALIZADO) y motivo de aceptación o rechazo.

## 5. Separación con HORUS

| HORUS | Pie a Pie |
|---|---|
| Descubre patrones generales y valida hipótesis estratégicas | Busca oportunidades económicas propias (arbitraje, basis, predicción, liquidez) |
| Decide estrategia, dirección, horizonte, objetivo, stop y capital | Decide ruta, venue, división, tamaño por tramo y ritmo dentro de esos límites |
| Emite `horus.order/v1` | Emite `pieapie.report/v1` |

Pie a Pie puede desarrollar modelos de microestructura, ejecución y
arbitraje; no extiende su motor de descubrimiento general.

## 6. Auditoría de las seis familias complementarias

| Familia | Qué existe | Qué se reutiliza | Qué falta | Rol |
|---|---|---|---|---|
| 1. Market making inteligente | `lab/modules/liquidity`: cola de órdenes con trades públicos, selección adversa, comisión maker. Resultado actual: NO RENTABLE (203 ejecuciones, −US$2,60) | modelo de cola y fills | cotización a dos puntas, límites de inventario, sesgo de precio por inventario, cancelación por volatilidad | propio (Pie a Pie) |
| 2. Reversión / valor relativo | `lab/research/stat_arb` (descubrimiento: congelado) | barrido de dos libros y costos de 4 patas | tipo de orden HORUS `pair` (dos patas simultáneas, ratio de cobertura dado por HORUS) | ejecución de órdenes HORUS |
| 3. Tendencia / rupturas | — | entrada `trigger` del ejecutor v1 (ya implementada) | órdenes en tramos (TWAP) y stop dinámico (trailing) | ejecución de órdenes HORUS |
| 4. Volatilidad / opciones | `FuturesSource` (patrón para Deribit) | fuente pública, `walk` | fuente de opciones Deribit (libros, griegas públicas), costos por contrato, margen de estructuras; primero como observación NO_VERIFICABLE | propio + órdenes HORUS |
| 5. Eventos | Kalshi (Actions), Polymarket (CLOB por lotes), fees verificados | fuentes, fees, controles de cobertura | tipo de orden HORUS `prediction` (comprar YES/NO con precio máximo) | ejecución de órdenes HORUS |
| 6. Asignación de capital | `StrategyLedger`, `lab/evaluate.verdict` | compuerta de evidencia | **`lab/allocator.py` (implementado)**: sin evidencia, 0 | propio |

Orden de implementación: (a) ejecutor v1 crypto spot, asignador y monitor de
carry (hecho en esta fase); (b) tipo de orden `pair` y TWAP/trailing (las
estrategias 2 y 3 de HORUS solo necesitan ejecución); (c) market making a dos
puntas con inventario (replay sobre trades guardados); (d) `prediction`
(eventos); (e) opciones (primero observación). Cada paso se valida con
tests unitarios, de integración (orden → reporte) y replay sobre datos
guardados antes de pasar al siguiente.

## 7. Plan priorizado

| # | Entrega | Validación |
|---|---|---|
| 1 | Informe definitivo de las investigaciones (cuando terminen las recolecciones) | episodios, fuera de muestra, costos |
| 2 | `lab/record.py`: registro común + adaptadores de lab, Kalshi y funding | unitarios: realizado ≠ teórico |
| 3 | `executor/`: schema v1, store (idempotencia + hash), estados, límites, router, motor paper crypto spot, buzón | unitarios, integración (orden → reporte), regresión de idempotencia |
| 4 | Monitor de cash-and-carry (`python -m lab.carry_monitor`): esperado, observado (al vencer) y riesgo por separado | regla congelada del estudio |
| 5 | Asignador de capital (`lab/allocator.py`): solo estrategias con evidencia suficiente reciben capital | unitarios: una observación sola = 0 |
| 6 | Market making con inventario a dos puntas (extiende `liquidity`) | replay sobre libros y trades guardados |
| 7 | Ejecución HORUS de pares, rupturas y eventos (tipos de orden adicionales) | integración con libros guardados |
| 8 | Volatilidad: fuente de opciones (Deribit público), costos y margen | primero observación (NO_VERIFICABLE), después modelo |
