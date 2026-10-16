# Biblioteca integrada (Harris, Chan, Hull) aplicada a Pie a Pie (16/10/2026)

Complementa `BIBLIOTECA_HULL_ESTRATEGIAS_2026-10-16.md` (inventario de Hull y pruebas C1–C6), sin repetirlo.

Los PDF están en `docs/biblioteca/`, **fuera de git** (derechos de autor; el repositorio es público). Aquí solo se citan capítulos, ejemplos y páginas.

## Fase 1. Libros y legibilidad

| Libro | Archivo | Lectura | Observación |
|---|---|---|---|
| Ernest P. Chan, *Algorithmic Trading: Winning Strategies and Their Rationale* (Wiley, 2013) | `Algorithmic Trading - … Ernest P. Chan.pdf` | Texto extraíble: 225 páginas, ~69.000 palabras | Completo. 8 capítulos con ejemplos numerados (2.1–8.2). Cito "Chan Ej. x.y" y la página impresa del índice |
| Larry Harris, *Trading and Exchanges* (borrador del 05/03/2002, Oxford University Press) | `Trading-Exchanges-…-Draft Copy.pdf` | Texto extraíble: 110 páginas, ~51.000 palabras | **Borrador abreviado.** Están los 29 capítulos, pero en general solo sus primeras secciones; la edición final tiene ~600 páginas. Las citas son "Harris cap. x.y" de este borrador |
| John C. Hull, *Options, Futures, and Other Derivatives*, 8.ª ed., más el ejemplar en español, 6.ª ed. | — | Ya inventariado | Ver el informe anterior |

**Qué aporta cada uno, sin duplicar:**
- **Hull:** valuación, no arbitraje y herramientas de derivados.
- **Chan:** reglas cuantitativas concretas (reversión a la media, momentum, pares, retorno de roll), pruebas estadísticas (ADF, Hurst, half-life, Johansen) y errores frecuentes de backtest.
- **Harris:** de dónde salen la liquidez, los spreads y los costos. Quién gana y quién pierde (es un juego de suma cero). Órdenes límite frente a órdenes de mercado. Proveedores de liquidez y "value traders". Anticipadores de órdenes.

**Los conceptos compartidos se citan una sola vez:**
- la paridad cubierta y la base: Hull;
- el retorno de roll, contango y backwardation: Chan cap. 5 (aplica Hull 5.14);
- los costos de transacción: Harris cap. 21.

## Fase 2. Estrategias de los libros cruzadas con el historial

Clases:
- **A:** probada y descartada.
- **B:** incompleta o pendiente de datos.
- **C:** no investigada.
- **D:** variante con una hipótesis económica distinta.

| # | Estrategia (fuente) | Lo que afirma el autor | Clase en Pie a Pie | Comentario |
|---|---|---|---|---|
| 1 | Reversión a la media de una serie, lineal y con Bollinger (Chan cap. 2–3, Ej. 2.5 y 3.2) | Posición = −z, con lookback ≈ half-life | **A** en Forex de un solo par (meanrev_5, 6 pares) | No se repite |
| 2 | Pares cointegrados con precio, log o ratio, y filtro de Kalman (Chan Ej. 2.6–2.8, 3.1, 3.3) | El spread de activos cointegrados revierte | **A** (laboratorio: 45 pares, 0 sobreviven a Benjamini-Hochberg; `research_stat_arb.json`) | — |
| 3 | **Par de divisas cruzadas con interés de rollover, AUD.CAD** (Chan Ej. 5.1–5.2, cap. 5 p. 107) | Dos monedas de commodities cointegradas; estrategia lineal con lookback de 20 días e interés de rollover real | **C** | Valor relativo entre dos monedas, no la tendencia de un par contra el USD. **E4** |
| 4 | Retorno de roll; contango y backwardation (Chan Ej. 5.3; Hull 5.14) | El retorno de un futuro = spot + roll | **A** (C5: no hay prima medible en BTC/ETH; P2: la base contra el funding pierde) | — |
| 5 | **Reversión a la media del spread de calendario: γ de roll con half-life** (Chan Ej. 5.4, p. 140) | γ, el retorno de roll implícito del spread entre vencimientos, revierte con half-life de ~36 días en CL | **D** | P2 mantenía hasta el vencimiento con un umbral fijo. Acá la hipótesis es que la base anualizada **revierte a su media móvil**, con salida al revertir. **E3** |
| 6 | Spreads entre mercados (Chan cap. 5, "Futures Intermarket Spreads") | Chan muestra que son raramente estacionarios | **C**, sin acceso razonable (futuros CME) | — |
| 7 | Futuros de VIX contra ES; contango del VX (Chan cap. 5) | El roll del VX es muy lucrativo | **C** sin acceso. El análogo cripto (futuros de DVOL) no tiene historial público | Postergada |
| 8 | Momentum de series temporales (Chan Ej. 6.1 TU; cap. 6) | Persistencia de tendencias | **A** (tendencia 20/100 en Forex y perpetuos) | — |
| 9 | **Momentum entre activos** (Chan Ej. 6.2, p. 163; Daniel-Moskowitz) | Ganadores relativos siguen ganando; Chan advierte el derrumbe de 2008–2009 | **C** | Mecanismo distinto: se compran los que más subieron contra los que más bajaron, neutral al mercado. **E1** |
| 10 | **Reversión entre activos, lineal long-short** (Chan Ej. 4.3, p. 120; Khandani-Lo) | Pesos = −(r_i − r̄); sin parámetros; Chan informa resultados **antes de costos** | **C** | Mecanismo de Harris: compensación por proveer liquidez a quien vende o compra con apuro (cap. 16). **E2** |
| 11 | ETF contra sus componentes; ETF pairs (Chan cap. 4) | Arbitraje de canasta | **C**, sin acceso (acciones de EE.UU.) | — |
| 12 | Gap de apertura y buy-on-gap (Chan Ej. 7.1; cap. 4) | Reversión o continuación después del gap | **C**, no aplica a cripto (opera las 24 horas) | Postergada |
| 13 | Momentum por noticias y post-earnings (Chan Ej. 7.2) | Subreacción a noticias | **C**, sin datos de noticias | Postergada |
| 14 | Rebalanceo de ETF apalancados; flujos forzados (Chan cap. 7; Harris "order anticipators", cap. 11) | Flujos previsibles que se pueden anticipar | **C** | Análogo cripto incierto; postergada |
| 15 | Market making con Kalman (Chan cap. 3); proveedores de liquidez y dealers (Harris cap. 13–14, 16) | Spread = procesamiento + inventario + selección adversa | **A** (laboratorio: provisión de liquidez NO RENTABLE) | — |
| 16 | Órdenes límite contra órdenes de mercado; exposición de órdenes (Harris cap. 18) | Una orden límite ahorra el spread pero da una opción gratuita y corre riesgo de no ejecutarse | **Herramienta**: se usa como escenario de costos (maker) en E1–E3, no como estrategia | — |
| 17 | Kelly, CPPI, stop loss (Chan cap. 8) | Gestión de riesgo | **Herramienta** para el tamaño de las posiciones, cuando una estrategia pase | — |
| 18 | Medición de costos implícitos (Harris cap. 21) | Medida de Roll, spread efectivo | **Herramienta** | — |

**Advertencias de los autores** que aplican a todo lo anterior:
- **Chan, cap. 1:** sesgo de supervivencia, sesgo de anticipación (look-ahead), espionaje de datos (data snooping), cambios de régimen. Chan recomienda reglas simples y lineales.
- **Harris, cap. 1:** el trading es de suma cero, y quien no espera ganar no debería operar.

## Fase 3–4. Matriz priorizada

| # | Candidata | Mecanismo | Datos (disponibilidad) | Plataforma | Costos | Capital y riesgo | Complejidad | Prioridad |
|---|---|---|---|---|---|---|---|---|
| **E1** | Momentum entre activos en perpetuos cripto | Subreacción y flujos forzados (Chan cap. 6); neutral al mercado | Velas diarias y funding de Binance USDⓈ-M (públicos, 2020–2026). **Sesgo de supervivencia**: universo fijado de antemano | Binance (un solo venue) | Taker 0,05% (VERIFICADO) + 2 pb; funding real | US$1.000 con 1x bruto; drawdown por reversiones de momentum (Chan: 2009) | Baja | 1 |
| **E3** | Reversión de la base anualizada del trimestral contra el perpetuo | Mean reversion del retorno de roll (Chan Ej. 5.4) | Trimestral continuo, perpetuo y funding (públicos). Ya integrados | Binance | 4 operaciones taker; funding real | Neutral al precio; riesgo de base y de vencimiento | Baja | 2 |
| **E4** | Par AUD.CAD con interés de rollover | Cointegración de monedas de commodities (Chan Ej. 5.2) | FRED (diarios) + tasas OECD (mensuales) | Forex (acceso desde Argentina sin verificar) | 2 pb por rotación + recargo de 0,5% anual + diferencial de tasas real | 1x; drawdown si se rompe la cointegración | Baja | 3 |
| **E2** | Reversión lineal long-short entre activos cripto | Compensación por proveer liquidez (Harris cap. 16; Chan Ej. 4.3) | El mismo universo de E1 | Binance | Rotación diaria muy alta: taker 0,05% + 2 pb | 1x; los costos probablemente dominan | Baja | 4 |

## Fase 5. Reglas registradas antes de los resultados

**Criterios comunes** (`AUDITORIA_ALCANCE_2026-10-16.md` §7):
- (a) neto fuera de muestra > 0 y mayor que la letra cuando inmoviliza capital;
- (b) t ≥ 2 sobre períodos no solapados, con Bonferroni si hay más de una variante;
- (c) resiste costos ×1,5;
- (d) drawdown fuera de muestra menor que 3 veces el retorno anual neto.

**Sobre los costos:**
- Escenario **base**: taker.
- Escenario **maker** (Binance USDⓈ-M maker 0,02%, según Harris cap. 18): **solo informativo**, no se usa para aceptar.

**Una especificación por prueba, sin optimizar.**

### E1. Momentum entre activos (hipótesis propia sobre Chan Ej. 6.2)

- **Universo fijo**, elegido por presencia y capitalización a comienzos de 2021, **antes** de mirar resultados: BTC, ETH, BNB, XRP, ADA, DOGE, DOT, LTC, LINK, BCH, XLM, UNI, SOL, AVAX, ATOM, ETC, FIL, TRX, EOS y AAVE. Perpetuos USDT de Binance, cada uno mientras tenga datos.
- **Regla:** cada 7 días, rankear por el retorno de los últimos 30 días; comprar las 4 mejores y vender las 4 peores, con pesos iguales (0,125 cada una, 1x bruto); mantener 7 días.
- **Contabilidad:** retorno diario por cierres + funding real (los largos pagan, los cortos cobran).
- **Costos:** 0,05% + 2 pb por unidad de rotación.
- **Separación:** 2021–2023 dentro de muestra y 2024–10/2026 fuera. t sobre semanas.
- **Sesgo:** se informa el de supervivencia. Monedas deslistadas, como LUNA, no están en la API.

### E2. Reversión lineal entre activos (Chan Ej. 4.3, aplicada a cripto)

- **Universo:** el mismo de E1.
- **Pesos diarios:** w_i = −(r_i − r̄) / Σ|r_j − r̄|, con el retorno del día anterior; rebalanceo diario.
- **Costos y funding:** como E1.
- **Separación y t:** la misma separación; t sobre días.

### E3. Reversión de la base del trimestral (hipótesis propia sobre Chan Ej. 5.4)

- **Datos:** BTCUSDT y ETHUSDT de Binance.
- **Base anualizada:** b_t = (F/P − 1)·365/días.
- **z:** con media y desvío de 20 días.
- **Entrada:**
  - si z > 1: vender el trimestral y comprar el perpetuo;
  - si z < −1: lo contrario.
- **Salida:** cuando z cruza 0, o 3 días antes del vencimiento.
- **Contabilidad:** retorno de las dos patas por cierres + funding de la pata del perpetuo.
- **Costos:** 0,05% + 2 pb por pata, al entrar y al salir.
- **Capital:** el nominal de una pata.
- **Separación:** 2021–2023 dentro de muestra y 2024–2026 fuera. t sobre operaciones no solapadas.

### E4. Par AUD.CAD (Chan Ej. 5.2)

- **Precio:** AUDCAD = AUDUSD × USDCAD (FRED: DEXUSAL y 1/DEXCAUS).
- **z:** con media y desvío de 20 días (el lookback de Chan).
- **Posición:** −z/2, limitada a ±1 (tope de 1x, porque la versión de Chan es lineal sin tope).
- **Rollover:** diferencial de tasas real AUD − CAD (OECD 3 meses, mes m−1) / 365.
- **Costos:** 2 pb por unidad de rotación + 0,5% anual.
- **Separación:** 2002–2015 dentro de muestra y 2016–2026 fuera. t sobre semanas.

## Resultados E1–E4 (16/10/2026, con las reglas registradas en `ea6e551`, sin cambios)

| Prueba | Muestra (antes de 2024; E4 2002–2015) | Fuera de muestra (2024–2026; E4 2016–2026) | Costos ×1,5 | Diagnóstico bruto | Decisión |
|---|---|---|---|---|---|
| **E1** momentum entre activos (20 perpetuos) | +27,1% anual, t 1,64, drawdown −29% | **−22,3% anual**, t −1,27, drawdown **−63%** | −23,4% | Sin costos ni funding, fuera de muestra: −20,3% (t −1,12). **El mecanismo no se sostuvo después de 2023** | **DESCARTAR** |
| **E2** reversión lineal entre activos (Chan Ej. 4.3) | −49,4% anual, t −2,36 | **−47,5% anual**, t −3,19 | −56,1% | Bruto, fuera de muestra: −25,6%. **En cripto diario hay continuación, no reversión.** Con maker (informativo): −38,7% | **DESCARTAR** |
| **E3** reversión de la base del trimestral (BTC/ETH) | 63/65 operaciones, −0,27%/−0,25% por operación, 3 ganadoras | **59/61 operaciones, −0,35%/−0,37% por operación**, t del exceso −4,9/−4,6, 2–5 ganadoras | Peor | La reversión bruta ≈ 0: las 4 comisiones (0,28%) explican casi toda la pérdida | **DESCARTAR** |
| **E4** par AUD.CAD con rollover (Chan Ej. 5.2) | −2,68% anual, t −0,56, drawdown −52,6% | **+0,06% anual**, t 0,18, drawdown −28,9% | −0,63% anual | Solo precio, fuera de muestra: +1,48% (t 0,65), no significativo | **DESCARTAR** |

**Limitaciones:**
- **E1/E2:** sesgo de supervivencia (universo fijo de monedas que siguen listadas: favorece a E1, que igual pierde fuera de muestra).
- **E4:** los tipos de cambio son cotizaciones de referencia de FRED, no bid/ask; las tasas son mensuales.
- **E3:** cierres diarios. La reversión intradiaria no se mide.

**Lección:** los mecanismos de Chan probados en acciones y ETF de 2007–2012 (reversión entre activos, momentum entre activos, pares de commodities) no aparecen netos de costos en cripto 2024–2026 ni en AUD.CAD 2016–2026. Chan mismo advierte cambios de régimen (cap. 1) y el derrumbe del momentum de 2009 (Ej. 6.2).
