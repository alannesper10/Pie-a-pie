# Pie a Pie — Investigación profunda (entrega parcial, 13/10/2026)

Todo es paper: sin órdenes, sin claves, sin tocar `data/` ni las dos
posiciones de Kalshi. Datos crudos en `lab_data/` (fuera de git); resúmenes
en `reports/lab/`. Cada corrida guarda el sha del código (`code_version`).

| Línea | Estado | Veredicto actual |
|---|---|---|
| 1. Cash-and-carry con vencimiento | Completa (histórico 2022–2026 + vivo) | **Estrategia de convergencia con riesgo**, no arbitraje garantizado. Hoy **no supera a la letra del Tesoro**: no operar. |
| 2. Polymarket, 559 no verificables | Causa encontrada y corregida; recolección nueva en curso | **Sin ventaja** con libros completos (parcial) |
| 3. CCL/MEP entre emisoras | Infraestructura lista; rueda completa programada para el 14/10 | **Sin ventaja** en la muestra de hoy (15 minutos de rueda) |
| 4. Corridas largas | `watch-b-20261013` (futuros + Polymarket + CCL, 12 h) y `ccl-20261014` (rueda completa) | En curso |

---

## 1. Cash-and-carry con futuros de vencimiento

### 1.1 Reconstrucción del caso original (`collect-final`, tick 0)

| Dato | Valor |
|---|---|
| Spot Binance ETH/USDT (ask) | 2.503,60 × 210,7 ETH disponibles |
| Futuro ETH/USDT:USDT-261225 (bid) | 2.525,29 × 0,027 ETH en el primer nivel; 1,0–1,5 ETH en 5 niveles |
| Tamaño simulado | 0,01797 ETH (~US$45 por pata) |
| Base | +0,866% (entre +0,86% y +0,88% durante toda la hora) |
| Libros | pedidos con 0,3 s de diferencia; re-pedidos tras 500 ms para la ejecución |
| Capital | US$90,39 (spot US$45 + garantía 1x US$45) |
| Neto fijado | +US$0,238 (+0,26% en 72,6 días), no realizado |

Ambas patas eran **ejecutables** en ese tamaño (la profundidad alcanzaba).
Con la medición por episodios, el caso es **un único episodio** que estuvo
positivo y ejecutable en los 54 ticks (55 minutos): es la base estructural del
futuro, no una ineficiencia fugaz.

### 1.2 ¿Supera a una alternativa de riesgo comparable?

No. Letra del Tesoro de EE.UU. a 3 meses (FRED DTB3, 4,05% anual de
descuento) por el mismo plazo de 72,5 días: **0,822%**. El cash-and-carry a
1x fija **+0,287%** después de costos: **−0,54 puntos contra la letra**.
Lo mismo con los 20 futuros con vencimiento observados hoy (Binance, Bybit,
Deribit; 1,5 a 163,5 días): **todos por debajo de la letra** (de −0,16 a
−1,02 puntos).

### 1.3 Evidencia histórica (`research --study carry`)

Binance USDⓈ-M, velas de 1 h de los continuos CQ (trimestre corriente) y NQ
(siguiente) y del spot, ETH y BTC, entregas de 2022-03 a 2026-09 (18 por par).
Una entrada por día. Supuestos y verificaciones:

- **Entrega a las 08:00 UTC verificada** contra las velas (el continuo cambia
  de contrato en esa hora).
- **Desvío real índice/spot**: se vende el spot con un TWAP de 1 minuto en la
  media hora previa (replica el promedio del índice). Desvío medido: máximo
  0,67% (ETH) y 0,42% (BTC); en los vencimientos recientes, ~0,01%.
- **Mismo contrato a través del roll** (NQ→CQ) para el margen y las salidas.
- **Precios sin operaciones excluidos** (velas con volumen 0: el continuo NQ
  repetía 20.955,0 durante meses en 2022) y entradas anteriores a la primera
  entrega conocida (no se sabe qué contrato representan).

Resultados (exceso = rendimiento del período a 1x menos la letra del mismo período; no se anualiza):

| Par/contrato | Entradas (contratos) | Neto > 0 | Supera a la letra | **Regla ex ante**: tomadas | Exceso realizado medio (mín) | Supera a la letra | 1ª mitad / 2ª mitad |
|---|---|---|---|---|---|---|---|
| ETH CQ | 1.537 (17) | 67% | 14% | 149 (10%), 6 contratos | +0,28% (−0,34%) | 85% | +0,20% / +0,33% |
| ETH NQ | 985 (16) | 98% | 22% | 220 (22%), 6 contratos | +0,70% (−0,40%) | 95% | +0,71% / +0,70% |
| BTC CQ | 1.537 (17) | 69% | 11% | 161 (10%), 6 contratos | +0,27% (−0,21%) | 86% | +0,22% / +0,30% |
| BTC NQ | 985 (16) | 99% | 23% | 233 (24%), 7 contratos | +0,66% (−0,14%) | 95% | +0,74% / +0,62% |

**Regla ex ante** (fija, sin parámetros ajustados): entrar solo si la base
fijada menos los costos estimados supera a la letra del mismo plazo, con
datos conocidos al entrar. El resultado realizado incluye el desvío real del
spot frente al precio de entrega.

- **Sensibilidad**: con comisiones ×1,5 y ×2 hay menos entradas, pero el
  exceso medio se mantiene (ETH NQ +0,71%/+0,67%; BTC CQ +0,25%/+0,26%).
- **Margen**: en las entradas tomadas, 0 liquidaciones a 1x. A 2x, **108 de
  763 se habrían liquidado** sin reponer garantía. Sin la regla, a 1x en NQ
  hubo 110 (ETH) y 43 (BTC) liquidaciones: en 2023–2024 el precio se duplicó
  dentro de un contrato. El capital extra necesario llegó al 68% (ETH NQ 1x).
- **Salida anticipada**: pierde en 38–76% de los casos según el momento (peor
  caso −4,8% del capital). El resultado solo está fijado si se mantiene hasta
  el vencimiento.
- **Régimen**: la regla **no se cumple desde el 4/2/2025**. Durante ~20 meses
  la base no pagó más que la letra; tampoco hoy (1.2).

### 1.4 Costos

| Costo | Valor | Estado |
|---|---|---|
| Spot taker Binance | 0,10% | SUPUESTO (nivel base; tarifas por cuenta requieren clave) |
| Futuros taker | 0,05% | SUPUESTO (nivel base) |
| Entrega | 0,05% (cobrada a tasa taker según Binance) | SUPUESTO |
| Medio spread | spot 0,0002%, futuro 0,0035% | ESTIMADO con 1 h de libros reales |
| Margen de mantenimiento | 0,5% | SUPUESTO (las tablas por nivel requieren clave) |
| Desvío índice vs spot | medido por vencimiento | VERIFICADO con datos |
| Letra del Tesoro | DTB3 diario (FRED) | VERIFICADO |

### 1.5 Disponibilidad legal desde Argentina

**No verificada.** La RG CNV 1058/2025 (régimen de PSAV) no menciona
derivados, futuros ni apalancamiento. Sí exige que un PSAV extranjero
dirigido a residentes argentinos se inscriba antes de operar (arts. 1–3) y
prevé bloquear los sitios no inscriptos (art. 40). Que un exchange esté
inscripto como PSAV no implica que pueda ofrecer futuros a residentes. Hace
falta asesoramiento legal antes de cualquier uso real.

### 1.6 Clasificación y recomendación

**Estrategia de convergencia con riesgo** (no arbitraje garantizado): el
resultado depende de mantener el margen (riesgo de liquidación con
apalancamiento), de la contraparte (el exchange), de que se cumpla la
liquidación contractual y de comisiones no verificadas por cuenta.

**Recomendación: CONTINUAR como monitor, no operar.** La regla ex ante tiene
evidencia histórica consistente (2 pares × 2 contratos, dos mitades,
sensibilidad de costos), pero hoy no se cumple. Un monitor que avise cuando
el exceso ex ante supere a la letra es lo único que justifica más esfuerzo.
Antes de cualquier uso real: tarifas reales por cuenta, margen de
mantenimiento real y verificación legal.

---

## 2. Polymarket: los 559 casos no verificables

| Dato | Valor |
|---|---|
| Casos | 559 (21 eventos, 54 ticks) |
| Causa | **3.648 patas recortadas por un tope interno de 200 libros** (se pedían 254 por tick) + **16 libros sin asks** (dato real: nadie vendía NO) |
| ¿Recuperables? | **No**: el CLOB solo sirve el libro actual. Quedan como NO_RECUPERABLE. |
| Indicativo (Gamma, sin profundidad) | 127 casos con bruto top-of-book > 0, en 3 eventos |

**Corrección**: libros por lotes (`POST /books`), sin recortes silenciosos; si
se supera el máximo, queda registrado como error `TRUNCATED`.

**Recolección nueva con libros completos** (`watch-b-20261013`, parcial: 18
ticks): 513 observaciones, **0 sin libro**, 406 sin ventaja después de
comisiones o tamaño mínimo, 107 con presupuesto insuficiente, **0 positivas**.
Los 3 eventos con bruto positivo según Gamma: bruto real de +0,15% a +0,2%
(por ejemplo, paquete de NO a 2,994 contra un pago de 3), con neto de
−US$0,015 a −0,045 por paquete después de comisiones.

**Recomendación: DESCARTAR la ventaja** (pendiente de confirmar con las 12 h de
recolección). Se mantiene el monitor.

---

## 3. CCL/MEP entre emisoras

**Construcciones** (con puntas y cantidades, nunca cierres):
- **MEP**: todo en BYMA, especie en pesos contra especie D de la misma acción.
- **CCL**: acción local contra ADR, con ratio verificado por consistencia.

**Costos**: derecho de mercado BYMA **5 pb + IVA (VERIFICADO**, comunicado de
BYMA vigente desde 01/10/2025); comisión del broker SUPUESTA (0,25%); EE.UU.
SUPUESTO.

**Fuentes**: BYMA open data (oficial, ~20 min de demora, sin especies D ni
ADR); Nasdaq (ADR en tiempo real según la API); data912 (terceros, demora no
verificada).

Muestra de hoy (15 ticks, 16:41–16:56 ART):

| Construcción | Observaciones | Resultado | Bruto máximo | Costo de equilibrio por operación |
|---|---|---|---|---|
| MEP (data912) | 1.980 | 100% SIN_EDGE | +0,026% | 0,0065% (menor que el derecho de mercado) |
| CCL (data912) | 1.650 | 100% SIN_EDGE | +0,57% (SUPV→CEPU) | 0,14% |
| CCL (BYMA demorado + Nasdaq) | 1.016 | NO_VERIFICABLE (puntas no simultáneas) | — | — |

**Error detectado**: YPF da un CCL implícito de 161 frente a ~1.609 del resto.
El ratio o la cotización de data912 para YPFD no cierran, y eso producía
"oportunidades" de +900%. Ahora se excluye todo ratio NO_CONSISTENTE y un bruto
mayor al 10% queda como SOSPECHOSO_REVISAR_DATOS.

**Faltan**:
- una rueda completa (programada para el 14/10, 11:00–17:10 ART);
- la demora real de data912;
- la comisión real del broker;
- las normas cambiarias vigentes para cruces pesos/D: la última norma que
  encontré es de 2023 (RG 962/969), así que el estado actual queda NO
  VERIFICADO;
- profundidad más allá de la mejor punta.

**Recomendación preliminar: AMPLIAR DATOS** (una rueda completa) antes de
decidir. Con la muestra de hoy, el diferencial no cubre ni el derecho de
mercado en MEP, y en CCL solo funcionaría con costos ≤0,14% por operación.

---

## 4. Corridas largas y reproducibilidad

- `collect --sources futures,polymarket,ccl` en una base aparte
  (`LAB_DB=lab_data/watch.sqlite`), checkpoint por tick, guardia de memoria
  (~300 MB pico) y `code_version` en cada corrida.
- `evaluate --fresh-ledger`: evalúa cada tick como si fuera el primero. Así se
  ve si la oportunidad persiste (con el ledger normal, el capital bloqueado
  en la primera ejecución la oculta).
- `episodes`: ticks consecutivos positivos = un episodio (sin duplicar), con
  primer y último momento, duración y ejecutabilidad al verificar.
- Corridas anteriores (código viejo) y nuevas en bases separadas: `lab.sqlite`
  contra `watch.sqlite`.

## Errores encontrados en esta fase (con test de regresión)

1. Tope silencioso de 200 libros de Polymarket (origen de los 559 casos).
2. Hora de entrega: la API publica la fecha a las 00:00; la entrega real es a las 08:00 UTC.
3. NQ: margen y salida anticipada se cortaban en el roll; ahora siguen el mismo contrato.
4. Entradas de 2021 mapeadas a vencimientos equivocados (antes de la primera entrega conocida).
5. Velas sin operaciones del continuo NQ tomadas como precios (bases de −52%, pérdidas falsas de −57%).
6. Ratio de YPF inconsistente en data912 (falsos +900%).
7. Un `evaluate` parcial sobrescribía `reports/lab/lab_report.md` (se restauró; ojo al correr evaluaciones parciales).
