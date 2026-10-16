# Auditoría del alcance de la búsqueda de rentabilidad (16/10/2026)

**Para qué sirve este documento:** dice qué se probó realmente, con qué datos, con qué errores, y qué queda por investigar. Corrige el tono del informe `REINICIO_BUSQUEDA_RENTABILIDAD_2026-10-16.md`.

**Lo que esas pruebas permiten afirmar:** el informe anterior descartó **reglas concretas**, no **mercados enteros**. Una regla simple que falla en Forex no dice nada del carry de divisas. Una tendencia aislada en BTC no dice nada de los spreads de calendario.

**Capital:** los US$1.000 virtuales siguen **sin asignar**. No hubo operaciones reales. No se tocaron Kalshi, HORUS ni el ejecutor. Los criterios estadísticos son los mismos de antes.

## 1. Forex: qué se probó exactamente

| Ítem | Detalle |
|---|---|
| Datos | FRED, tipos de cambio diarios "noon buying rates" de Nueva York. **Son cotizaciones de referencia (medio), no precios ejecutables con bid/ask** |
| 6 pares | DEXUSEU (EURUSD), DEXJPUS (USDJPY), DEXUSUK (GBPUSD), DEXUSAL (AUDUSD), DEXCAUS (USDCAD), DEXSZUS (USDCHF) |
| 3 reglas × 6 pares = 18 pruebas | 1) **tsmom_20_100**: largo si la media de 20 días > la de 100, corto si no (siempre posicionado). 2) **meanrev_5**: z del retorno de 5 días (escalado con la volatilidad de 60 días); z > 1 → corto, z < −1 → largo, si no, sin posición (~30% del tiempo posicionado). 3) **breakout_20**: largo al romper el máximo de 20 días, corto al romper el mínimo; mantiene la posición |
| Ejecución | Posición decidida al cierre y aplicada al retorno del día siguiente (sin mirar el futuro; test incluido). 1x nominal, sin apalancamiento |
| Costos | 2 pb por cambio unitario de posición (spread + comisión, **SUPUESTO**) y **2% anual fijo sobre el nominal mientras hay posición (SUPUESTO)** |
| Descubrimiento / validación | Muestra 1999–2015; fuera de muestra 2016–10/2026 (2.692 días) |
| Control múltiple | Bonferroni sobre 24 pruebas (Forex + perpetuos): t crítico 3,08 |

### Resultados individuales fuera de muestra

Retorno total 2016–2026. Se muestra con el supuesto original y sin el recargo, como diagnóstico.

| Par | tsmom 20/100 (con 2% / sin recargo, t) | meanrev 5 | breakout 20 |
|---|---|---|---|
| EURUSD | −25,9% / −8,3%, t −0,25 | −8,9% / −2,7%, t −0,14 | −38,6% / −24,0%, t −1,04 |
| USDJPY | −7,3% / +14,8%, t +0,61 | −11,0% / −5,1%, t −0,21 | −46,9% / −34,3%, t −1,23 |
| GBPUSD | −6,3% / +16,0%, t +0,65 | −14,2% / −8,6%, t −0,40 | −45,1% / −32,0%, t −1,14 |
| AUDUSD | −54,0% / −43,1%, t −1,58 | −22,5% / −17,1%, t −0,93 | −42,5% / −28,8%, t −0,88 |
| USDCAD | −45,1% / −32,0%, t −1,60 | −13,9% / −7,9%, t −0,58 | −21,4% / −2,6%, t −0,01 |
| USDCHF | −38,7% / −24,1%, t −1,01 | −13,2% / −7,5%, t −0,48 | −25,2% / −7,4%, t −0,19 |

**Errores y limitaciones de esta prueba:**
- **Swap mal modelado:** un costo fijo del 2% anual en lugar del **diferencial de tasas real**, que según el par y la dirección puede ser un *ingreso* (carry). Exageró las pérdidas de las reglas que mantienen posición. Sin el recargo, ninguna regla es significativa (máximo t +0,65): **la conclusión "sin ventaja" se mantiene para estas 18 reglas**, pero las cifras de pérdida del informe anterior estaban infladas.
- **Tasa de aciertos engañosa:** el "15%" de meanrev contaba como fallidos los días sin posición (~70%).
- **Datos:** fixings diarios de referencia, no bid/ask ni datos intradiarios.
- **Acceso desde Argentina:** no se verificó qué intermediarios aceptan residentes.

### Familias de Forex NO investigadas

- **Carry de divisas** (comprar monedas de tasa alta contra las de tasa baja), que es la prima de riesgo más documentada del mercado.
- Momentum **transversal** entre monedas (en lugar de cada par por separado).
- Valor o PPP.
- Reacción a eventos (datos macro, bancos centrales).
- Estrategias intradiarias y de sesión.
- Volatilidad y regímenes.
- Diferencias entre intermediarios.

## 2. Futuros: qué se probó exactamente

| Ítem | Detalle |
|---|---|
| Instrumentos | **Perpetuos** USDⓈ-M de Binance BTCUSDT y ETHUSDT (no futuros con vencimiento), velas diarias desde 09/2019 y funding real cada 8 h sumado por día |
| Regla 1: tendencia | La misma tsmom 20/100 de Forex, siempre posicionada, 1x nominal |
| Regla 2: funding sin cobertura | Corto mientras el funding de 7 días sea > 0. **Error de especificación:** es una apuesta direccional, no carry. Se corrigió antes de ver la versión cubierta, y quedó documentado en el código |
| Regla 3: carry de funding cubierto | Corto perpetuo + largo spot mientras el funding de 7 días sea > 0; cobra el funding; costo de entrada o salida de las dos patas 0,19% (taker spot 0,10% y perpetuo 0,05% **verificados**, 4 pb de deslizamiento **supuestos**) |
| Costos de la regla 1 | Taker 0,05% (verificado) + 2 pb de deslizamiento por cambio de posición + funding real pagado o cobrado |
| Margen | **No se modeló.** La regla 1 asume capital = nominal (1x, sin liquidación). La regla 3 asume capital = 1,5 × nominal (spot + 50% de margen del perpetuo), un **SUPUESTO** que no se verificó |
| Caídas | Máximo drawdown de la curva de capital compuesta diaria, a 1x nominal: BTC −60,8% y ETH −66,3% fuera de muestra. Es la caída del activo cuando la regla queda del lado equivocado: no hay apalancamiento que la explique |
| Validación | Muestra 2019-09 a 2023; fuera de muestra 2024 a 10/2026 |

**Resultados fuera de muestra:**
- **Tendencia:** BTC t 0,01, ETH t 0,93. Sin ventaja.
- **Carry cubierto:** +11% en 2,8 años, drawdown −1,3%. Le gana a cero, pero **no a la letra del Tesoro desde 2025** (exceso −1,2% en 2025 y −2,7% en 2026 para BTC).

**Limitaciones:**
- No se modeló la diferencia de precio entre spot y perpetuo al entrar y salir.
- No se modelaron la tasa de interés del margen, el riesgo de exchange ni el deslizamiento real con el libro.
- El funding de un día sumado a precio de cierre es una aproximación.

**Por qué no se investigaron otras posibilidades:** por elección de alcance, no porque estuvieran descartadas.
- **Spreads de calendario** (perpetuo contra trimestral, o trimestral contra trimestral): en el laboratorio quedaron con **756 observaciones, todas NO VERIFICABLES**. Nunca se probaron con una regla y datos históricos.
- **Diferencias de funding entre exchanges:** no se probaron.
- **Cash-and-carry con vencimiento:** sí se estudió a fondo antes (2022–2026, regla ex ante "exceso sobre la letra > 0"). Hoy, 0 señales.
- **Futuros tradicionales** (CME: índices, oro, bonos) y la **tendencia diversificada entre activos**: no se investigaron.

## 3. Opciones: qué se probó exactamente

| Ítem | Detalle |
|---|---|
| Instrumento | **No se simularon opciones.** Se usó el índice **DVOL de BTC** de Deribit: la volatilidad implícita a 30 días, anualizada, calculada sin modelo a partir de las opciones de Deribit (como el VIX) |
| "Regla de venta de volatilidad" | Ninguna regla operable. Cada día se compara el DVOL (IV) con la volatilidad realizada de los 30 días siguientes (RV: desvío de los retornos logarítmicos diarios del perpetuo de Binance × √365, en %), menos 2 puntos de costo. "Ventaja" = IV − RV − 2 |
| Qué significan los "puntos" | Puntos de volatilidad anualizada. Ejemplo: IV 50 y RV 45 → 5 puntos antes de costos. **No es un rendimiento sobre capital.** Es una aproximación de lo que ganaría un vendedor de volatilidad cubierto en delta (straddle o swap de varianza). Pasarlo a % del capital depende de la estructura, el apalancamiento y el vega elegidos, y no se hizo |
| Costos | 2 puntos de volatilidad por entrar y salir (**SUPUESTO**; no se midió el bid/ask real de opciones) |
| Estadística | Observaciones diarias solapadas a 30 días (no independientes). El t se calculó **solo con meses no solapados** (uno de cada 30 días): muestra t 3,25 (n 34) y fuera de muestra t 1,15 (n 33). La corrección por pruebas múltiples no se aplicó a esta prueba |
| Datos | DVOL desde 04/2021 (fecha de inicio del índice). Muestra hasta 2023, fuera de muestra 2024–2026 |

**Limitaciones:**
- La RV usa el desvío con media, mientras que un swap de varianza usa el retorno cuadrático sin media.
- El DVOL es una medida de varianza y la comparación es aproximada.
- No hay bid/ask, profundidad, contrato mínimo ni griegas.

**Estructuras NO estudiadas:**
- Spreads verticales de riesgo definido (put spreads, call spreads).
- Iron condors.
- Spreads de calendario (estructura temporal de la IV).
- Skew (risk reversals).
- Paridad put-call y box spreads (arbitraje).
- Opciones de ETH.
- Opciones sobre acciones o índices de EE.UU.
- Coberturas con futuros.

**Conclusión correcta:** *no hay evidencia significativa de una prima de volatilidad explotable fuera de muestra con este proxy.* Las estructuras reales **no se evaluaron**.

## 4. Arbitraje y otras oportunidades

### Probadas y descartadas (con datos ejecutables y costos)

| Estrategia | Evidencia |
|---|---|
| Polymarket, comprar todos los NO | 513 observaciones con libros completos: 0 positivas. 3 positivas según Gamma, que al ejecutar fueron negativas o desaparecieron |
| Cash-and-carry con vencimiento | Histórico 2022–2026 con regla ex ante; desde 02/2025 nunca supera la letra; monitor en vivo con 0 señales |
| CCL/MEP entre emisoras | 3 ruedas parciales (~85.000 observaciones verificables), 0 con neto > 0 |
| MEP entre bonos | Margen ocasional de +0,15% con broker 0%; negativo con costos realistas |
| Dólar oficial → USDT local | P2P en USD minuto a minuto: ganancia en 15 de 175 minutos, un anuncio de ~US$372 |
| Canje MEP → CCL | Bloqueado por la declaración jurada de 90 días (norma), no por precio |
| Entre exchanges cripto, triangular, CEX-DEX | El laboratorio (`consolidated.md`) dio 774, 695 y 1.500 observaciones sin edge. **Las muestras son de horas**, no de días: descartado *en esa ventana* |

### Pendientes por falta de información (no descartadas)

| Estrategia | Lo que falta | Cómo obtenerlo |
|---|---|---|
| P2P Binance → libro de Binance | Comisión y demora del retiro de ARS | Pantalla de retiro de la app, sin operar |
| P2P MEXC entre contrapartes plausibles | Comisión P2P de MEXC para el tomador | Pantalla de confirmación de la orden, sin crearla |
| USD a cuenta propia en el exterior → USDT → ARS (+3–4% estimado) | Legalidad de combinarlo con cripto (Com. "A" 7552 vigente o no) y costos reales de transferencia | Consulta legal; tarifario de BNA o Naranja X |
| Spreads de calendario cripto | Nunca se probó: 756 observaciones no verificables | Prueba nueva, ver P2 en la sección 7 |

### Cotizaciones anómalas: no son oportunidades

- **MEXC P2P:** vendedor coreano a $1.389,50, vendedores a $1.480 y compradores de Filipinas a $1.650 (8–14% fuera de mercado). Persistentes, pero con señales de fraude o triangulación. **No se cuentan como oportunidades ejecutables.**
- **Letsbit:** +12,6% en 2 capturas por un error de la cotización de CriptoYa.
- **MEXC P2P a $1.800 y $1.900** (14/10): el mismo patrón.

## 5. Calidad de la ejecución: errores y límites

| # | Problema | Efecto | Estado |
|---|---|---|---|
| 1 | Swap de Forex modelado como un 2% fijo en lugar del diferencial de tasas | Pérdidas infladas; la conclusión sobre las 18 reglas no cambia (máximo t +0,65 sin el recargo) | Documentado; corregirlo con tasas reales en P4 |
| 2 | Tasa de aciertos que cuenta los días sin posición | Métrica engañosa en meanrev | Documentado |
| 3 | Funding "carry" sin cobertura (direccional) | Resultado inútil para carry | Corregido antes de ver el cubierto |
| 4 | Margen y liquidación no modelados en perpetuos | Las caídas son a 1x; no aplica a versiones apalancadas | Limitación declarada |
| 5 | Factor de capital de 1,5 en el carry cubierto, supuesto | El retorno sobre capital puede variar ±30% | Limitación |
| 6 | Volatilidad: proxy DVOL, no opciones operables; costo de 2 puntos supuesto; RV con media | No es la prueba de una estrategia de opciones | Limitación central |
| 7 | Bonferroni "aprobó" el carry cubierto contra **cero** | El umbral correcto es la letra del Tesoro; se corrigió en el informe | Corregido |
| 8 | Las muestras de arbitraje cripto del laboratorio son de horas | El "sin edge" vale solo para esa ventana | Limitación |
| 9 | P2P de Binance: 2 tardes (271 capturas); el 14/10 solo se guardaba la página 1 | Muestra chica; 7 a 12 ciclos | La captura ampliada ya corre |
| 10 | MEXC: medio día; comisión P2P desconocida | — | Pendiente |
| 11 | Endpoints P2P (Binance, MEXC) no documentados | Pueden cambiar o cortarse | Riesgo operativo |
| 12 | Comisiones no verificables sin cuenta: retiro de ARS de Binance, P2P de Binance y de MEXC | Deciden 2 candidatas | Pendiente del usuario |

**Pruebas que no se pudieron hacer:**
- Opciones con precios reales.
- Forex con bid/ask y swaps reales.
- Acceso a intermediarios desde Argentina.
- Cualquier ejecución real (prohibida en esta etapa).

## 6. Clasificación

| Clase | Elementos |
|---|---|
| **Probadas y descartadas** | 18 reglas técnicas de Forex sobre 6 pares; tendencia 20/100 en perpetuos BTC/ETH; carry de funding cubierto contra la letra (régimen actual); cash-and-carry con vencimiento; Polymarket todos los NO; CCL/MEP entre emisoras; MEP entre bonos; oficial → USDT local; canje MEP → CCL (por norma); MEXC con anuncios anómalos |
| **Pendientes por falta de información** | P2P Binance → libro; P2P MEXC plausible; ruta por el exterior; volatilidad con opciones reales (faltan precios históricos) |
| **Familias no investigadas** | Carry de divisas; momentum transversal de monedas; spreads de calendario cripto (no verificados); diferencias de funding entre exchanges; estructuras de opciones de riesgo definido; skew y estructura temporal de la IV; sesgo favorito/longshot en mercados de predicción; tendencia diversificada entre activos (futuros CME o ETF); Forex por eventos o intradiario; arbitraje cripto entre exchanges con muestras de varios días |
| **Candidatas para una prueba nueva** | Sección 7 |

## 7. Pruebas nuevas, en orden de prioridad

**Criterios comunes, fijados ahora y antes de mirar resultados:**
- Una sola especificación por prueba, sin optimizar parámetros.
- Separación temporal fija.
- Costos con fuente.
- La prueba se aprueba solo si cumple **las cuatro** condiciones:
  - (a) neto fuera de muestra > 0 y **mayor que la letra del Tesoro del período** cuando inmoviliza capital;
  - (b) t ≥ 2,0 sobre períodos **no solapados**, con Bonferroni si hay más de una variante;
  - (c) resiste costos ×1,5;
  - (d) el drawdown máximo fuera de muestra es menor que 3 veces el retorno anual neto.

Prioridad = mecanismo económico plausible × datos gratuitos disponibles × factible con US$1.000 × capacidad de dar una decisión en días.

### P1. Cerrar las dos candidatas P2P (costo cero, decisión inmediata)

- **Qué:** leer la comisión de retiro de ARS de Binance y la comisión P2P de MEXC (lo hace el usuario, sin operar).
- **Prueba:** volver a correr `p2p_spot_run` y `mexc_p2p` con esos valores sobre las capturas acumuladas de 5 días hábiles o más (la captura ampliada ya corre).
- **Aceptación:** al menos 30 ciclos secuenciales en 6 días o más, 80% o más positivos, mediana > 0 y costos ×1,5 > 0.
- **Fuera de muestra:** los últimos 2 días, separados antes de mirar.

### P2. Spread de calendario cripto: perpetuo contra trimestral (no probado)

- **Mecanismo:** la base del trimestral, anualizada, frente al funding que se espera pagar en el perpetuo. Si la base excede al funding, conviene vender el trimestral y comprar el perpetuo, neutral al precio, hasta el vencimiento. Converge por construcción al vencer.
- **Datos (gratuitos):**
  - velas diarias de los trimestrales de Binance COIN-M y USDⓈ-M desde 2020 (`dapi`/`fapi` klines por contrato, ya usados en `lab/research/carry.py`);
  - funding del perpetuo;
  - entrega al vencimiento.
- **Regla fija:** entrar cuando la base anualizada − el funding promedio de 30 días > 3%; mantener hasta el vencimiento.
- **Costos:** 4 patas taker (0,05% verificado) + 2 pb de deslizamiento; margen 2x sobre las dos patas (supuesto declarado).
- **Separación:** vencimientos de 2020–2023 contra 2024–2026.
- **Aceptación:** criterios comunes, con exceso sobre la letra.
- **Por qué primero entre las nuevas:** reutiliza el código de carry y da una decisión en un día de trabajo.

### P3. Diferencia de funding entre exchanges (no probado)

- **Mecanismo:** el mismo perpetuo con funding distinto en Binance, Bybit y OKX. Comprar donde se cobra menos y vender donde se paga más, neutral al precio.
- **Datos:** historial público de funding de los 3 exchanges (2021–2026).
- **Regla fija:** abrir si la diferencia de funding de 7 días anualizada es > 8% y cerrar si baja de 2%.
- **Costos:** 4 patas taker (0,04–0,05%) + transferencias; capital dividido entre dos exchanges (riesgo de contraparte doble).
- **Separación:** 2021–2023 contra 2024–2026.
- **Aceptación:** criterios comunes; exceso sobre la letra.

### P4. Carry de divisas G10 (la familia de Forex más documentada, no probada)

- **Mecanismo:** prima por tener monedas de tasa alta, que pagan por riesgo de crash.
- **Datos:** FRED, tipos de cambio diarios + tasas a 3 meses o de política de cada país (IR3TIB, por ejemplo); mensual desde 2000.
- **Regla fija:** cada mes, largo en las 2 monedas de mayor tasa contra el USD y corto en las 2 de menor tasa. El P&L incluye el **diferencial de tasas real** (corrige el error 1).
- **Costos:** 2 pb por rebalanceo + 0,5% anual de recargo del intermediario.
- **Separación:** 2000–2015 contra 2016–2026.
- **Aceptación:** criterios comunes.
- **Antes de integrar:** verificar qué intermediario accesible desde Argentina permite operar con US$1.000 (micro-lotes o futuros micro).

### P5. Venta de volatilidad BTC con riesgo definido y precios reales de opciones

- **Mecanismo:** la prima de varianza, ahora con estructura operable.
- **Datos:** trades históricos de opciones de Deribit (`public/get_last_trades_by_currency_and_time`, gratuito). Reconstruir el put spread mensual de 25 y 10 delta al momento de entrada; precio de liquidación al vencer.
- **Regla fija:** cada vencimiento mensual, vender un put spread 25/10 delta de 0,1 BTC (pérdida máxima acotada y < US$1.000).
- **Costos:** bid/ask observado (o 50% del spread si solo hay trades) + comisión de Deribit (verificar la tabla oficial).
- **Separación:** 2021–2023 contra 2024–2026.
- **Aceptación:** criterios comunes, con un punto más: ningún mes puede perder más del 25% del capital.
- **Riesgo:** reconstruir precios con trades puede tener huecos. Si más del 20% de los vencimientos queda sin precio, la prueba se declara NO VERIFICABLE.

### P6. Sesgo favorito/longshot en mercados de predicción

- **Mecanismo:** los contratos muy baratos suelen estar sobrevalorados y los favoritos, levemente infravalorados (documentado en apuestas).
- **Datos:** Polymarket, mercados resueltos (Gamma: precio histórico + resultado; acceso internacional).
- **Regla fija:** comprar contratos entre 0,85 y 0,97 a 7 días o más de la resolución; mantener hasta resolver.
- **Costos:** comisión de la feeSchedule (verificada) + medio spread.
- **Separación:** mercados resueltos antes y después de 2025-06.
- **Aceptación:** criterios comunes, más un tope: ninguna categoría puede aportar más del 50% del resultado.
- **Riesgo:** el sesgo de supervivencia de los mercados listados; documentarlo.

### P7. Tendencia diversificada entre activos (baja prioridad por capital)

- **Mecanismo:** el momentum de series temporales funciona sobre **carteras** diversificadas, no sobre un solo activo.
- **Datos:** Stooq, diarios de índices, bonos, materias primas y monedas.
- **Por qué está última:** con US$1.000 no se puede replicar con futuros (márgenes por contrato) y vía ETF los costos y el acceso desde Argentina están sin verificar. Solo si P2–P6 fallan.

### Lo que NO se va a hacer

- Repetir variantes de las 18 reglas de Forex.
- Barrer parámetros.
- Retomar Polymarket NO, CCL, oficial → USDT o MEP sin un cambio de condición concreto.

## 8. Camino más razonable

1. **Hoy:** P1. El usuario lee 2 comisiones, sin operar.
2. **Días 1–2:** P2 y P3. Mecanismos neutrales al precio, datos gratuitos, factibles con US$1.000 y reutilizan código.
3. **Días 3–4:** P4. Corrige el error de swap de Forex con tasas reales.
4. **Días 5–7:** P5. Requiere reconstruir datos de opciones.
5. **En paralelo, de bajo costo:** P6.

Cada prueba termina en **AVANZAR / CORREGIR / DESCARTAR** con los criterios de la sección 7, fijados hoy. Solo las que pasen a AVANZAR reciben capital del libro central, y nunca todo.
