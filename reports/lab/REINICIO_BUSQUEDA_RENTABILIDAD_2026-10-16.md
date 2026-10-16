# Pie a Pie: reinicio de la búsqueda de rentabilidad (16/10/2026)

Capital virtual: **US$1.000**. Sin dinero real ni órdenes. No se tocaron las dos posiciones de Kalshi, el ledger existente, los datos de HORUS ni el ejecutor.

Convenciones:
- **[MEDIDO]** calculado sobre datos reales guardados.
- **[ESTIMADO]** depende de supuestos.
- **[FALTA]** no verificado.

## 1. Resumen

**Ninguna estrategia demostró todavía una ventaja neta.** Hay dos candidatas que solo se definen con una comisión que hoy no se puede leer sin una cuenta:
1. **P2P de Binance → libro de Binance.** Depende de la comisión de retiro de ARS.
2. **P2P de MEXC entre contrapartes plausibles.** Depende de la comisión P2P de MEXC.

En los dos casos, el margen medido es de +0,1% a +0,3% por ciclo antes de esa comisión.

**El +8–19% de la "Compra/Venta rápida" de MEXC no es una oportunidad.** Sale de anuncios entre 8% y 14% fuera de mercado (un vendedor coreano a $1.389,50, dos vendedores a $1.480 y compradores de Filipinas a $1.650). Ese desvío es en sí mismo la señal de riesgo: fraude, triangulación o condiciones ocultas. Se descarta.

Forex, tendencia en futuros, carry de funding (contra la letra del Tesoro) y la prima de volatilidad **no superan los controles fuera de muestra**.

## 2. Auditoría del repositorio

| Clase | Componentes | Decisión |
|---|---|---|
| **Infraestructura útil** | `lab/sources.py`, `lab/store.py` (snapshots SQLite), `lab/collect_check.py` (ventana, reanudación, integridad), `lab/research/fx_capture.py` (captura cambiaria y P2P), tareas de Windows "PieAPie FX/CCL", `lab/core.py` (recorrido de libros y costos), `lab/evaluate.py` (compuerta RENTABLE), `lab/allocator.py`, `executor/` (máquina de estados y límites), `src/notify.py` (ntfy) | Conservar |
| **Nuevo** | `lab/ledger.py`: libro central de US$1.000, un mismo dólar no puede estar en dos estrategias, lo comprometido no se reasigna, eventos auditables y reproducibles (5 tests) | Conservar. Se conecta cuando una estrategia pase a AVANZAR |
| **Problema detectado** | El laboratorio (`StrategyLedger` en `lab/core.py`) le daba a cada estrategia su propio capital de US$100 "separado". Contradice el capital común | Reemplazar por `lab/ledger.py` al conectar estrategias. No se borró nada |
| **Datos a conservar** | `data/` (Kalshi, solo lectura), `lab_data/*.sqlite` (watch, ccl), `lab_data/fx_ar/*.jsonl` (cambiaria 14, 15 y 16/10), informes de `reports/lab/` | Conservar como antecedentes |
| **Descartado antes** (no se repite salvo cambio de condición) | Polymarket todos los NO; CCL/MEP entre emisoras; ruta oficial → USDT; cash-and-carry con vencimiento (bajo la letra desde 02/2025) | Monitores pasivos donde ya existen |
| **Pendiente de un dato** | P2P Binance → libro (comisión de retiro de ARS) | Ver la tabla |
| **Simplificable** | Módulos del laboratorio sin uso reciente: `cex_dex`, `triangular`, `liquidity`, `term_structure`, `prediction`, investigaciones `etf`, `stat_arb`, `imbalance`, `discovery` | No se borran (tienen tests y reportes). No se vuelven a correr salvo que cambie una condición |

## 3. MEXC: Compra rápida / Venta rápida

**Datos [MEDIDO]:**
- API pública del P2P de MEXC, las dos puntas, 3 páginas.
- 97 capturas por minuto, 16/10 de 11:51 a 13:27. La captura sigue hasta las 15:05.
- Precio de referencia: el libro de Binance (~$1.614).

| Qué se vio | Valor |
|---|---|
| Vendedores con precio ≥ 3% bajo el mercado | en **97 de 97** capturas |
| Esos vendedores | "Tam USDT" (Corea, $1.389,50, 570 órdenes en 30 días); "CriptoNova" y "EnzoFernandux" (Argentina, $1.480, órdenes de $148.000 a $155.400 ≈ 100 USDT, 47 y 59 órdenes en 30 días) |
| Compradores con precio ≥ 3% sobre el mercado | en 74 de 97 capturas (Filipinas, $1.650, mínimo $330.000) |
| Mejor vendedor argentino plausible | ~$1.611 |
| Mejor comprador argentino plausible | ~$1.607 a $1.615 |

Rutas:
- **M1:** comprar y vender dentro del P2P de MEXC. Los pesos llegan directo al banco, sin retiro de un exchange.
- **M2:** comprar en MEXC, retirar USDT por TRC20 (~1 USDT) y vender en el libro de Binance.

Resultados [MEDIDO, precios; ESTIMADO, comisiones]:

| Filtro | Monto | Comisión P2P | M1 neto (mediana) | M1 positivas | M2 neto (antes del retiro de ARS) |
|---|---|---|---|---|---|
| Todos los anuncios | $150.000 | 0% | **+8,5%** | 97/97 | +8,0% |
| Todos los anuncios | $500.000 | 0% | +2,6% | 92/97 | −0,01% |
| **Plausible** (AR, comerciante, ≥ 20 órdenes, ≥ 98%, precio a < 3% del mercado) | $150.000 | 0% | **+0,14%** | 53/97 | −0,20% |
| Plausible | $150.000 | 0,2% | −0,68% | 5/97 | −0,40% |
| Plausible | $500.000 | 0% | −0,90% | 0/97 | −0,12% |

**Lectura:**
- Un vendedor que descuenta 8% de forma persistente, con historial y cupo chico, no tiene una explicación comercial normal.
- La compra a precios anómalos expone a recibir USDT de origen ilícito o a transferir a cuentas de terceros (mulas).
- La venta a compradores anómalos es el esquema clásico de triangulación: un tercero, víctima, paga al vendedor y después reclama, y la cuenta bancaria queda bloqueada.
- **El margen es el precio de ese riesgo.** Por la regla fijada ("no operar por fuera de las protecciones; riesgo de contraparte inaceptable → descartar"), la versión con anuncios anómalos se **DESCARTA**.
- La versión plausible da +0,14% de mediana con comisión P2P de 0% y es negativa con 0,2%. **[FALTA]** la comisión P2P de MEXC: 0% según DataWallet y 0,2% según TradersUnion, sin página oficial.

## 4. Forex [MEDIDO, costos ESTIMADOS]

**Datos:** FRED, diarios desde 1999, 6 pares (EURUSD, USDJPY, GBPUSD, AUDUSD, USDCAD, USDCHF). Muestra hasta 2015 y fuera de muestra 2016–2026.

**Reglas fijadas antes de mirar:**
- tendencia: medias de 20 y 100 días;
- reversión: z-score de 5 días;
- ruptura: 20 días.

**Costos:**
- 2 pb por cambio de posición;
- swap con un recargo de 2% anual sobre el nominal. Es conservador y reduce mucho los resultados de las reglas que mantienen posición.

**Resultado:**
- **18 de 18 negativas o nulas fuera de muestra.**
- Ninguna supera el t crítico de Bonferroni (3,08, con 24 pruebas).
- La reversión acierta solo el 15% de los días y pierde.

**[FALTA]** qué intermediarios aceptan residentes argentinos. No se investigó en detalle porque no hay una ventaja que justifique la integración.

## 5. Futuros y perpetuos [MEDIDO]

| Prueba | Fuera de muestra (2024–2026) | Decisión |
|---|---|---|
| Tendencia 20/100 en BTC y ETH (perpetuos, taker 0,05% + funding) | BTC t = 0,01; ETH t = 0,93; drawdown de −61% / −66% | DESCARTAR |
| Funding sin cobertura (corto) | Pérdida. Era un **error de especificación mío**: es direccional, no carry. Se corrigió antes de mirar la versión cubierta y quedó documentado | — |
| **Carry de funding cubierto** (corto perpetuo + largo spot, mientras el funding de 7 días sea > 0) | +11% en 2,8 años sobre el capital (spot + margen), drawdown −1,3%, t = 13 contra cero | Ver la comparación con la letra |
| Cash-and-carry con vencimiento | Ya medido: 0 señales sobre la letra desde 02/2025 | DESCARTAR (monitor activo) |

Carry de funding cubierto contra la letra del Tesoro:

| Año | Exceso BTC | Exceso ETH |
|---|---|---|
| 2020 | +10,7% | +19,3% |
| 2021 | +21,8% | +26,6% |
| 2022 | −1,6% | −2,4% |
| 2023 | −0,6% | +0,2% |
| 2024 | +2,5% | +3,5% |
| **2025** | **−1,2%** | **−1,8%** |
| **2026** (en el año) | **−2,7%** | **−3,1%** |

Solo le gana a la letra en mercados alcistas con funding alto. **Hoy no**: se descarta, con una condición objetiva para reabrirlo (sección 8).

## 6. Opciones: prima de volatilidad [MEDIDO, costo ESTIMADO]

**Medida:** DVOL de BTC (Deribit) contra la volatilidad realizada de los 30 días siguientes, menos 2 puntos de vol de costo.

| | Muestra (2021–2023) | Fuera de muestra (2024–2026) |
|---|---|---|
| Ventaja media | +9,6 puntos de vol | **+2,9 puntos** |
| t con meses no solapados | 3,25 (n = 34) | **1,15 (n = 33)**, no significativo |
| Peor mes | −41,7 puntos | **−47,3 puntos** |
| Percentil 5 | −21,7 | −21,7 |

**Lectura:**
- La prima existe en promedio, pero fuera de muestra no es significativa y tiene colas grandes.
- Un mes malo borra más de un año de ventaja.
- Con US$1.000, el contrato mínimo de Deribit (0,1 BTC, ~US$8.000 de nominal) obliga a usar spreads de riesgo definido, que reducen todavía más la ventaja.

**[FALTA]** historial de precios de opciones con bid/ask para evaluar spreads (no es gratuito). **DESCARTAR** por ahora.

## 7. Arbitraje: estado de lo investigado

| Familia | Medido | Decisión |
|---|---|---|
| P2P Binance → libro de Binance | +0,12% neto de mediana, 7 de 7 ciclos positivos con retiro de ARS gratis; 0 ciclos si el retiro cuesta ≥ 0,25% | **CORREGIR**: falta la comisión de retiro de ARS |
| CCL/MEP entre emisoras | 0 oportunidades verificables en 3 días | DESCARTAR |
| Oficial → USDT | Ganancia en 15 de 175 minutos, un solo anuncio de ~US$372 | DESCARTAR |
| Polymarket todos los NO | 0 ejecutables | DESCARTAR |
| Triangular y entre exchanges cripto | Investigaciones anteriores negativas; sin cambio de condición | No se repite |

## 8. Tabla comparativa y decisiones

| # | Candidata | Neto | Costos incluidos | Calidad de los datos | Riesgos | Capital | Decisión | Siguiente paso |
|---|---|---|---|---|---|---|---|---|
| 1 | **P2P Binance → libro** | +0,12% por ciclo [MEDIDO, retiro 0%]; ~$900–1.900/h | Spot 0,10% [VERIFICADO]; P2P 0% [PUBLICADO]; retiro de ARS [FALTA] | 2 tardes, 271 capturas; liberación medida en perfiles | Bloqueo bancario, contraparte, endpoint no oficial | $500.000–5.000.000 por ciclo (~US$300–3.000) | **CORREGIR** | El usuario lee en la app (sin operar) la comisión de retiro de ARS y la del P2P |
| 2 | P2P MEXC entre contrapartes plausibles (M1) | +0,14% de mediana con $150.000 y P2P al 0%; negativo con 0,2% [MEDIDO / ESTIMADO] | Comisión P2P de MEXC [FALTA] | 97 capturas, medio día | Triangulación al vender por P2P | ~US$100 por orden | **CORREGIR** | Leer la comisión P2P de MEXC en la pantalla de la orden, sin crearla |
| 3 | MEXC con anuncios fuera de mercado | +8,5% [MEDIDO, sin ajustar por riesgo] | — | Persistente en 97 de 97 capturas | Fraude, triangulación, fondos ilícitos | ~100 USDT por orden | **DESCARTAR** | — |
| 4 | Carry de funding cubierto | Exceso sobre la letra de −1,2% (2025) y −2,7% (2026) | Taker spot y perpetuo [VERIFICADO]; deslizamiento [SUPUESTO] | 7 años de funding real | Exchange, margen, cambio de régimen | US$1.000 alcanza | **DESCARTAR** (reabrir si el funding de 30 días anualizado supera la letra + 3%) | Monitor con esa condición |
| 5 | Forex (18 reglas) | Negativo fuera de muestra | Spread y swap [ESTIMADO] | 27 años, FRED | — | — | **DESCARTAR** | — |
| 6 | Tendencia en perpetuos | t ≈ 0–0,9 fuera de muestra, drawdown −60% | Taker + funding | 7 años | Drawdowns | — | **DESCARTAR** | — |
| 7 | Prima de volatilidad (short vol) | +2,9 puntos de mediana, t = 1,15, peor mes −47 | 2 puntos de costo [ESTIMADO] | 5 años de DVOL | Cola extrema | Mínimo 0,1 BTC (~US$8.000) | **DESCARTAR** | Solo con datos de spreads de riesgo definido |
| 8 | Cash-and-carry con vencimiento | 0 señales sobre la letra | Completos | Histórico + monitor | Liquidación a 2x | — | DESCARTAR (monitor) | — |
| 9 | CCL, oficial → USDT, Polymarket | Sin ventaja verificable | Completos | Varios días | — | — | DESCARTAR | — |

**AVANZAR: ninguna.**

**Asignación del capital virtual de US$1.000:** queda **todo sin asignar** en el libro central. Ninguna estrategia tiene evidencia suficiente. No se reparte por conveniencia.

## 9. Qué impide avanzar (concreto)

1. **Dos comisiones** que las plataformas no publican y que solo se ven en la pantalla de una orden o de un retiro: el retiro de ARS de Binance y el P2P de MEXC. Las dos se leen sin operar, en unos minutos. Con eso las candidatas 1 y 2 pasan a AVANZAR (validación con 30 ciclos simulados en 6 o más días) o a DESCARTAR.
2. **Escala:** aunque se confirme, la ventaja de P2P es de +0,1–0,3% por ciclo, con cupos chicos. Con US$1.000, el resultado esperado es de unos pocos dólares por día de trabajo manual, más el riesgo bancario. Hay que decidir si eso justifica avanzar.
3. **Fuera de cripto P2P**, las familias estándar (Forex, tendencia, short vol, carry) no muestran ventaja neta con datos públicos y costos realistas. Una ventaja nueva requeriría datos o accesos que hoy no hay: libros de opciones con historial o intermediarios de Forex verificados para Argentina.

## 10. Reproducir

```
python -m lab.research.screen salida.json                          # Forex, perpetuos, volatilidad
python -m lab.research.p2p_spot_run salida.json <capturas.jsonl...> # P2P Binance -> libro
python -m pytest -q tests/test_ledger.py tests/test_screen.py tests/test_mexc_p2p.py tests/test_p2p_spot.py
```

MEXC: `lab/research/mexc_p2p.py` sobre `lab_data/fx_ar/fx-20261016.jsonl`.

Fuentes:
- FRED (DEX*, DTB3);
- Binance (`fapi/v1/klines`, `fapi/v1/fundingRate`, `api/v3/depth`; tabla de comisiones binance.com/en/fee/trading);
- Deribit (`public/get_volatility_index_data`);
- MEXC P2P (`p2p.mexc.com/api/market`, endpoint público no documentado);
- comisiones de MEXC: mexc.com/info/fee y artículos citados en el informe del 15/10.
