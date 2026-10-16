# Investigación bibliográfica: John C. Hull aplicado a Pie a Pie (16/10/2026)

Los PDF están en `docs/biblioteca/`, **excluida de git** (`.gitignore`): son obras con derechos de autor y el repositorio es público. Este informe solo cita capítulos, secciones y páginas, con fragmentos mínimos.

## Fase 1. Inventario y lectura

| | Libro en inglés (fuente principal) | Libro en español (referencia cruzada) |
|---|---|---|
| Archivo | `Options Futures and Other Derivatives by John C Hull.PDF` | `Introduccion_a_los_mercados_futuros_y_op.pdf` |
| Título y edición | *Options, Futures, and Other Derivatives*, 8.ª edición (Prentice Hall) | *Introducción a los mercados de futuros y opciones*, 6.ª edición (traducción de M. Á. Sánchez Carrión) |
| Lectura | Texto extraíble (`pdftotext`): 980 páginas PDF, ~371.000 palabras | Texto extraíble: 579 páginas PDF, ~282.000 palabras |
| Estructura | 35 capítulos | 23 capítulos |

**Superposición:**
- El libro en español es la versión introductoria y está **prácticamente contenido** en el inglés. Sus capítulos 1–23 equivalen a los capítulos 1–19, 21, 24–25, 33 y 35 del inglés.
- **Solo en el inglés:** procesos estocásticos (13), BSM detallado (14), opciones para empleados (15), métodos numéricos (20, 26), estimación de volatilidad con EWMA y GARCH (22; el español solo resume en 18.6), riesgo de crédito (23), exóticas y swaps de varianza (25.15), martingalas (27), modelos de tasas (28–31) y ajustes de convexidad y quanto (29).
- **Solo en el español:** nada con valor estratégico adicional.
- **Criterio:** cito el inglés (EN cap.sección, página de inicio de la sección según el índice impreso) y agrego la equivalencia en español (ES) cuando existe.

**Cómo citar:** la página es la de inicio de la sección según el índice impreso de cada libro. Los PDF mezclan encabezados en la extracción, así que el número impreso de cada página no se pudo detectar de forma confiable. Ejemplo: "EN 5.14, p. 121 / ES 5.13, p. 117".

## Fase 2. Matriz de estrategias

**Clave de la columna "Pie a Pie":**
- **PROBADA**: hay un resultado.
- **VARIANTE**: es equivalente a una ya probada.
- **NUEVA**: no se probó.

**Las reglas de entrada y salida son de Hull solo cuando el libro las describe.** Lo que dice "hipótesis propia" no es una recomendación de Hull.

### A. Relaciones de no arbitraje

| # | Estrategia (fuente) | Mecanismo | Instrumentos | Entrada y salida según Hull | Costos y riesgos | Datos | Pie a Pie |
|---|---|---|---|---|---|---|---|
| A1 | **Cash-and-carry y su inverso** (EN 5.4, p. 104; 5.6, p. 109; 5.12 costo de mantenimiento, p. 120 / ES 5.4, p. 99; 5.11, p. 117) | F₀ ≠ S₀e^{(r−q)T}: si F₀ es mayor, comprar spot y vender futuro; si es menor, al revés | Spot + futuro con vencimiento | Hull: hasta la convergencia (EN 2.3) | Comisiones, financiación, margen, préstamo del activo para el inverso | Spot, futuros, entrega, tasa | **PROBADA**: cash-and-carry 2022–2026, nunca supera a la letra desde 02/2025. El inverso (vender spot cripto) no se probó; requiere préstamo de BTC y la base suele ser positiva |
| A2 | **Arbitraje de índice** (EN 5.9, p. 112; BS 5.4, p. 114 / ES 5.9, p. 108) | El mismo A1 con un índice accionario; Hull muestra que falla cuando no se puede ejecutar rápido (1987) | Futuro de índice + canasta | Igual que A1 | Ejecución simultánea de la canasta | Índice, futuro, dividendos | **VARIANTE** de A1. Sin acceso a futuros de índice |
| A3 | **Paridad de tasas cubierta en divisas** (EN 5.10, p. 114 / ES 5.8) | F = S·e^{(r−r_f)T}; un desvío es arbitraje cubierto | Spot de divisa + forward o futuro + tasas | Hull: arbitraje si no se cumple | Spreads, tasas reales accesibles | Forward o futuro, spot, dos tasas | **NUEVA en Argentina**: el futuro de dólar de A3 (ex ROFEX) contra spot y tasas en pesos (cauciones/LECAP). Ver C6 |
| A4 | **Paridad put-call** (EN 10.4, p. 221; 17.4 opciones sobre futuros, p. 365 / ES 9.4, p. 217; 14.4, p. 314) | C − P = F·e^{−rT} − K·e^{−rT}: un desvío es arbitraje | Call, put y futuro del mismo vencimiento | Hull: comprar lo barato y vender lo caro | Bid/ask de 3 patas, comisiones; en Deribit las opciones son inversas (pagan en BTC) | Libros simultáneos de las 3 patas | **NUEVA**. Ver C3 |
| A5 | **Box spread** (EN 11.3, p. 238; BS 11.1, p. 244) | Pago fijo K₂ − K₁: su precio implica una tasa | 4 opciones europeas | Hull: el box se valúa a K₂ − K₁ descontado; advierte que con opciones americanas falla (BS 11.1) | 4 patas; las opciones de Deribit son europeas (bien) | Libros simultáneos | **NUEVA** (parte de C3). La tasa implícita probablemente equivale a la base (sería una variante de A1) |
| A6 | **Límites de precio de opciones** (EN 10.3, p. 218 / ES 9.3, p. 213) | Una opción fuera de sus límites es arbitraje | Opción + subyacente | Hull: comprar lo barato | Bid/ask | Libros | **NUEVA** (control incluido en C3) |
| A7 | **Opciones de entrega y "wild card"** (EN 5.13, 6.2; BS 6.2, p. 135) | Opción implícita del corto en el futuro de bonos del Tesoro de EE.UU. | Futuro de bonos del Tesoro | — | — | — | **NO APLICA**: no hay acceso |

### B. Primas de riesgo y estrategias estadísticas

| # | Estrategia (fuente) | Mecanismo | Instrumentos | Entrada y salida | Costos y riesgos | Datos | Pie a Pie |
|---|---|---|---|---|---|---|---|
| B1 | **Backwardation normal, Keynes-Hicks** (EN 5.14, p. 121 / ES 5.13, p. 117) | Si los coberturistas están cortos, el futuro cotiza por debajo del spot esperado y el largo cobra una prima (y al revés). Hull lo explica con el riesgo sistemático | Futuros | **Hull no da regla** | Riesgo direccional completo | Futuros y spot al vencer | **NUEVA como medición**, de bajo costo con los datos de P2 (C5). Como estrategia es direccional y de varianza alta |
| B2 | **Stack and roll** (EN 3.6, p. 65; BS 3.2 Metallgesellschaft, p. 67 / ES 3.6, p. 65) | Renovar coberturas; Hull muestra el riesgo de liquidez de margen | Futuros sucesivos | Hull: cerrar uno y abrir el siguiente | Margen y flujo de caja | — | Herramienta de cobertura, no de ganancia. **No se prueba** |
| B3 | **Colas pesadas: comprar opciones muy fuera del dinero** (BS 19.1, p. 413; 19.2, p. 411; 19.3, p. 414 / ES 17.1, p. 379) | Si el mercado valúa con lognormal y la distribución real tiene colas pesadas, las opciones lejanas están baratas. **Hull: la oportunidad desapareció a fines de los 80** | Calls y puts muy fuera del dinero | Hull: "comprar calls y puts muy fuera del dinero … y esperar" | Pérdida de la prima casi siempre; ganancia rara | Trades históricos de opciones | **NUEVA** (opuesta a P5). Ver C2 |
| B4 | **Straddle o strangle cuando tu visión de volatilidad difiere de la del mercado** (EN 11.4, p. 246; BS 11.2, p. 248; 14.11 vol implícita, p. 318; 22.2–22.6 EWMA/GARCH, pp. 500–509 / ES 10.3, p. 240; 12.9, p. 282; 18.6, p. 408) | Hull: el straddle solo gana si tu pronóstico de volatilidad es distinto del implícito *y acertás* | Straddles, iron butterflies | **Hull no da regla.** Da las herramientas: el pronóstico EWMA o GARCH contra la volatilidad implícita | Prima, bid/ask, colas | Vol implícita, precios, trades | **NUEVA** (condicional, a dos lados; P5 era venta incondicional). Ver C1, hipótesis propia |
| B5 | **Spread de calendario con opciones** (EN 11.3 "Calendar spreads", p. 238; 19.5 estructura temporal de la volatilidad, p. 416 / ES 10.2, p. 231; 17.3, p. 384) | Ganancia si el precio queda cerca del strike; valor según la estructura temporal de la IV | Opciones de dos vencimientos | Hull describe el pago, no una regla | Riesgo de vega en la pata larga | Trades de dos vencimientos | **NUEVA**. C4 (hipótesis propia: reversión de la pendiente de la estructura temporal) |
| B6 | **Skew y "crashofobia"** (EN 19.3; BS 19.2, p. 416) | El skew de puts se empina cuando el mercado cae | Risk reversals | Hull no da regla | Colas | IV por delta | NUEVA, prioridad baja (hipótesis sin regla de Hull) |
| B7 | **Swaps de varianza y de volatilidad** (EN 25.15, p. 588) | Varianza implícita contra realizada | Swap o réplica con opciones | Pago L(σ̄² − K) | Réplica con muchas opciones | — | **VARIANTE** de la prima de volatilidad: el proxy DVOL contra RV y P5 ya fueron descartados |
| B8 | **Commodities: reversión a la media y estacionalidad** (EN 33.4, p. 752; 33.3 energía, p. 750 / ES 22.2, p. 478) | Modelos de precio con reversión; estacionalidad de la curva | Futuros de commodities | Hull modela, no da regla | Margen de CME, rolls | Curvas de futuros | NUEVA, **sin datos gratuitos confiables ni acceso con US$1.000**: postergada |
| B9 | **Ajuste de convexidad y quanto; paradoja de Siegel** (EN 29.1–29.3, pp. 668–674; BS 29.1, p. 676) | Los contratos inversos (COIN-M) tienen convexidad respecto de los lineales | Trimestrales COIN-M contra USDⓈ-M | Hull no da regla para cripto | Cobertura dinámica | Velas de los dos contratos | NUEVA, hipótesis propia de complejidad alta: postergada |

### C. Herramientas de Hull que no son fuentes de ganancia (no se prueban como estrategias)

- Cobertura con ratio de varianza mínima (EN 3.4, p. 56).
- Cobertura delta, gamma y vega (EN 18).
- Stop-loss: Hull muestra que falla (EN 18.3, p. 378).
- Seguro de cartera (EN 18.13, p. 400).
- VaR (EN 21).
- Covered call y protective put (EN 11.2, p. 236). Un covered call equivale a vender un put (paridad, EN 10.4), así que es **VARIANTE** de P5, ya descartada.
- Bull y bear spreads, butterflies (EN 11.3). Son estructuras que necesitan una visión; se usan dentro de C1.

## Fase 3. Selección

Filtros:
- un solo venue, sin transferencias urgentes;
- mecanismo claro;
- datos verificables;
- pérdida y capital medibles;
- compatible con US$1.000.

| Prioridad | Candidata | Por qué |
|---|---|---|
| **C2** | Comprar strangles muy fuera del dinero en BTC (B3, Hull BS 19.1) | Un solo venue (Deribit), riesgo = prima (US$ chicos), datos de trades reales ya integrados en P5. Mecanismo explícito en Hull, con su advertencia de que pudo desaparecer |
| **C1** | Volatilidad condicional: pronóstico EWMA contra IV ATM, con straddle comprado o iron butterfly vendido (B4) | Un solo venue, riesgo definido. Herramientas de Hull (EN 22.2, 22.6; BS 11.2). Regla propia, condicional y a dos lados, distinta de P5 |
| **C3** | Paridad put-call, box y límites en Deribit con libros en vivo (A4–A6) | Arbitraje puro y un solo venue. Se decide con una captura corta de libros simultáneos |
| **C4** | Spread de calendario de opciones con la estructura temporal de la IV (B5) | Un solo venue; regla propia; más compleja de reconstruir (dos vencimientos) |
| **C5** | Medir la prima de backwardation normal en los trimestrales de BTC (B1) | Casi gratis (datos de P2). Es una medición: solo pasa a estrategia si muestra una prima significativa |
| **C6** | Paridad de tasas cubierta en Argentina: futuro de dólar de A3 contra tasas en pesos (A3) | Mecanismo claro y contrato de US$1.000 nominal. **Primero hay que verificar si hay datos públicos de A3** |

## Fase 4. Plan de pruebas

**Fijado hoy, antes de ver resultados.** Los criterios comunes son los de `AUDITORIA_ALCANCE_2026-10-16.md` §7:
- (a) neto fuera de muestra > 0 y mayor que la letra cuando inmoviliza capital;
- (b) t ≥ 2 sobre períodos no solapados, con Bonferroni si hay más de una variante;
- (c) resiste costos ×1,5;
- (d) drawdown fuera de muestra menor que 3 veces el retorno anual neto.

Para opciones se agrega:
- la pérdida máxima por operación debe ser ≤ 25% de US$1.000;
- más de 20% de meses no verificables vuelve la prueba NO VERIFICABLE.

Separación: muestra 2020–2023, fuera de muestra 2024–2026.

### C2. Strangle muy fuera del dinero comprado

**Datos:** trades de history.deribit.com y entrega oficial btc_usd.

**Regla:**
- en cada vencimiento mensual, entrada el día del vencimiento mensual anterior, de 08:00 a 12:00 UTC;
- comprar el put de delta más cercano a −0,05 y el call de delta más cercano a +0,05;
- 0,1 BTC cada uno;
- precio: la mediana de los trades con dirección "buy" (precio de ask);
- mantener hasta el vencimiento.

**Costos:** 0,04% por pata con tope de 12,5% de la prima, más entrega de 0,015% si vence dentro del dinero.

**Capital:** la prima pagada.

**Métrica:** retorno mensual sobre la prima contra la letra, con t sobre meses.

### C1. Volatilidad condicional (hipótesis propia con herramientas de Hull)

**Pronóstico:** EWMA con λ = 0,94 (RiskMetrics, EN 22.2), con los retornos diarios de BTC hasta el día anterior a la entrada. Hull, EN 22.6: con EWMA, la varianza futura esperada es igual a la actual.

**IV:** la mediana de la IV de los trades del strike más cercano al índice, del vencimiento objetivo, en la ventana de entrada.

**Regla:**
- si σ_EWMA > 1,10 × IV: **comprar un straddle ATM** (precio de ask);
- si σ_EWMA < 0,90 × IV: **vender un iron butterfly**. Se vende el straddle ATM al bid y se compran alas de delta ±0,10 al ask;
- en el resto de los casos, no se opera;
- 0,1 BTC por pata, hasta el vencimiento.

**Costos:** los mismos de C2.

**Capital:** la prima en el straddle, la pérdida máxima en el iron butterfly.

**Métrica:** retorno mensual sobre el capital. Los meses sin señal no cuentan como operación. El exceso se calcula sobre la letra.

### C3. Paridad, box y límites en vivo

**Datos:** libros de órdenes públicos de Deribit (`public/get_order_book`) de las opciones BTC y del futuro del mismo vencimiento. Capturas cada 5 minutos durante 24 horas.

**Regla:**
- para cada par call/put del mismo strike y vencimiento, calcular la paridad con precios ejecutables (comprar al ask, vender al bid) de las 3 patas, en USD;
- para cada par de strikes, calcular el box;
- es oportunidad si el neto después de comisiones (0,04% por pata con tope, 0,05% del futuro) es > 0 y supera la letra por el plazo.

**Aceptación:** al menos una oportunidad persistente (≥ 2 capturas seguidas) con profundidad ≥ 0,1 BTC.

### C4. Calendario de volatilidad

Se especifica después de C1 y C2, porque reutiliza el mismo motor. La regla se fija antes de correrla.

### C5. Prima de backwardation normal

**Medición:** la media de (F₀ − S_T)/S₀ en los trimestrales de BTC/ETH, entrando 90 días antes, y su t.

**Pasa a estrategia solo si** |t| ≥ 2 fuera de muestra.

### C6. A3: paridad de tasas cubierta en Argentina

**Primero:** verificar la disponibilidad de datos públicos históricos del futuro de dólar de A3 y de las tasas de caución. Sin datos verificables no se prueba.

**Orden de ejecución:** C2 → C1 → C3 → C5 → C6 → C4. Cada una termina en AVANZAR, CORREGIR o DESCARTAR, sin cambiar reglas después de ver resultados.
