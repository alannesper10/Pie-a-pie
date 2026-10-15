# CCL y ruta oficial → USDT: evaluación con capturas hasta las 15:00 (15/10/2026)

Solo observación y simulación. No hubo órdenes, claves ni movimientos de fondos. Las dos posiciones de Kalshi, el ledger y los datos de HORUS no se tocaron. El análisis corrió sobre **copias** de las bases:
- `lab_data/ccl.eval-20261015b.sqlite`;
- `fx-20261015.hasta15.jsonl`.

## 1. Muestra y calidad de datos

La notebook se reinició a las 11:50 del 15/10. Por eso las recolecciones programadas para la mañana no corrieron y se relanzaron a las 12:05. **Lo que falta queda como faltante: no se rellena ni se extrapola.**

| Recolección | Cobertura | Capturas | Integridad | Errores |
|---|---|---|---|---|
| CCL 14/10 (`ccl-20261014`) | 15:18–17:05 ART (cierre) | 107 | ok, sin huecos | data912 en 7 capturas |
| CCL 15/10 (`ccl-20261015`, corte 15:00) | 12:05–15:00 ART | 174 | ok, sin huecos ni ilegibles | data912 en 6 capturas; BYMA en 2 |
| Cambiaria 15/10 (`fx-20261015`, corte 15:00) | 12:05–15:00 ART | 175 | ok | data912 (bonos) en 5 |

**Cobertura acumulada de la rueda de CCL** en las cuatro corridas (13/10 y 14/10 de las recolecciones anteriores, más estas dos):
- 13/10: 16:40–17:00;
- 14/10: 11:48–14:49 y 15:18–17:05;
- 15/10: 12:05–15:00.

Cada franja horaria de la rueda tiene al menos una observación, **salvo 11:00–11:48 (la apertura), que nunca se observó**. Todavía no hay una rueda completa de un mismo día. Por eso las conclusiones no son definitivas.

## 2. CCL y MEP entre emisoras: evaluación económica

**Costos por ciclo:**
- **CCL:** 0,724% = 2 operaciones locales (broker 0,25% [SUPUESTO] + derecho de mercado BYMA 0,0605% [VERIFICADO]) + 2 en EE.UU. (0,05% [SUPUESTO]) + tasa SEC.
- **MEP:** 1,242% (4 operaciones locales).

| Clase | 14/10, cierre | 15/10, 12:05–15:00 |
|---|---|---|
| **Observadas** (pares con puntas) | MEP 13.200 · CCL data912 10.560 · CCL BYMA+Nasdaq 7.236 | MEP 22.176 · CCL data912 18.480 · CCL BYMA+Nasdaq 12.384 |
| **Bruto > 0** | MEP 21 · CCL data912 328 · BYMA+Nasdaq 1.050 | MEP 43 · CCL data912 195 · BYMA+Nasdaq 695 |
| **Neto estimado > 0, verificable** | **0** | **0** |
| Mejor CCL verificable (data912) | SUPV→CEPU: bruto +0,69%, **neto −0,03%**; capacidad USD 38 | SUPV→LOMA: bruto +0,57%, **neto −0,16%**; capacidad USD 51 |
| Mejor MEP | bruto +0,17%, neto −1,07% | bruto +0,14%, neto −1,10% |
| **No verificable** (BYMA demorado ~20 min + Nasdaq) | 7.236. Mejor: SUPV→PAM, bruto +1,46%, "neto" +0,74%, USD 28 | 12.384. Mejor: SUPV→CEPU, bruto +0,88%, "neto" +0,16%, USD 116 |
| Episodios POTENCIAL (neto > 0 con costos ×1,5 y puntas simultáneas) | 0 | 0 |

**Profundidad:**
- Cuando el bruto fue positivo, la capacidad al mejor precio tuvo una mediana de **USD 51 a 119**.
- El máximo fue de USD 2.047 con data912 y de USD 8.069 con el cruce BYMA+Nasdaq (no verificable).

**Ejecutabilidad:** no verificable.
- Solo hay mejor punta, sin libro completo.
- La demora de data912 no está verificada.
- Las 4 patas tienen que ser simultáneas en dos mercados.
- Las normas cambiarias vigentes para este circuito no están verificadas.

**Lectura:** el mejor caso del cierre quedó a −0,03% del equilibrio, con una comisión de broker del 0,25% supuesta. Con una comisión menor, unos pocos pares podrían cruzar a positivo, pero con capacidad de decenas de dólares. **No hay evidencia de una ventaja explotable.** El cruce BYMA+Nasdaq muestra brutos mayores, pero sus puntas no son simultáneas: es **NO VERIFICABLE** y no cuenta como oportunidad.

**Estado:** sin edge en ~85.000 observaciones verificables a lo largo de tres días parciales.

**Recomendación:** mantener en observación pasiva. Para cambiar de veredicto hace falta:
1. la apertura (11:00–11:48);
2. la comisión real de un broker (con ~0,1% el umbral baja a ~0,4% por ciclo);
3. una fuente con libro y sin demora.

Sin eso, descartar.

## 3. Ruta oficial → USDT → ARS, con los anuncios P2P en USD de cada minuto

Es la prueba que el informe del 14/10 marcaba como decisiva. El 14/10 los anuncios en USD eran una sola foto. Hoy hay **175 capturas por minuto** dentro de la ventana de compra de Banco Nación (12:05 a 15:00).

**Precios:**
- Oficial de BNA: 1.535, fijo toda la ventana [OBSERVADO, pizarra].
- Equilibrio: **1,0514 a 1,0520 USD por USDT**. Es lo máximo que se puede pagar para no perder vendiendo en Binance spot [SIMULADO].
- Mejor anuncio P2P USDT/USD pagable por transferencia bancaria argentina (medio "BankArgentina"): **mínimo 1,050, mediana 1,054, máximo 1,056** [OBSERVADO].

**Minutos con un anuncio por debajo del equilibrio:** 15 de 175 (8,6%). Fueron de 12:26 a 12:28 y de 12:44 a 12:55, y siempre el **mismo anuncio**:
- comerciante con 321 órdenes en el mes;
- precio 1,050;
- orden de USD 200 a 2.500;
- solo **354 USDT disponibles**, unos USD 372.

| Ruta | $150.000 | $500.000 | $1.500.000 | $5.000.000 | $15.000.000 |
|---|---|---|---|---|---|
| A: BNA → P2P USD → Binance spot | −0,47% (0 de 175 positivas) | **−0,36% (15 de 175 positivas, máx. +0,18%)** | −0,19% (0) | −0,23% (0) | −0,39% (0) |
| A': BNA → P2P USD → P2P ARS | −0,73% | −0,65% (máx. +0,02%) | −0,56% | −0,59% | −0,75% (20 sin liquidez) |
| B: Naranja X → P2P USD | −0,47% | −0,44% | −0,21% | −0,24% | −0,41% |
| D: Mercado Pago | sin anuncio usable (solo transfiere USD a cuentas propias) | | | | |
| E: plataformas que reciben USD (indicativo) | −0,5% a −2,1% | | | | |

Medianas de las 175 capturas [SIMULADO].

**Dato descartado:** Letsbit mostró +12,6% en 2 capturas. Es un error de la cotización indicativa de CriptoYa, no una oportunidad.

**La ganancia máxima posible del día** fue de ~+0,18% sobre unos USD 350, unos **$1.000 de ganancia**:
- con un solo anuncio y durante 15 minutos;
- antes de los costos no verificados: comisión P2P, impuestos y el riesgo de que la transferencia en USD no llegue dentro de los 15 minutos del anuncio.

**Veredicto de la ruta A: NO VIABLE** con la evidencia de dos días. El 14/10, la ventaja aparente (+0,18% con $500.000 a $1.500.000) salía de un anuncio que hoy no apareció. Hoy hubo un anuncio parecido, de un comerciante, con un cupo de unos USD 372 y durante 15 minutos de 175. El mercado P2P en USD argentino se ubica justo en el equilibrio, entre 1,050 y 1,056. La brecha entre el oficial y el USDT es el precio de convertir dólares bancarios en USDT, no una ineficiencia.

**Rutas que siguen abiertas, sin evidencia:** solo la del exterior (ruta F del informe del 14/10). Es especulativa, de varios días, y su legalidad está pendiente. No cambia.

## 4. Señal secundaria: comprar en P2P USDT/ARS y vender en Binance spot

Datos de `lab_data/fx_ar/circuits-20261015.json`, con 175 capturas [SIMULADO, neto de la comisión spot de 0,10%]:

| Medida | 14/10 (96 capturas) | 15/10 (175 capturas) |
|---|---|---|
| Capturas con margen positivo | 96 de 96 | 162 de 175 |
| Margen, mediana | +0,26% | +0,20% |
| Margen, máximo | +0,37% | +0,32% |
| Cupo sumado de los anuncios con margen, mediana | ~3.600 USDT | ~20.500 USDT (máx. 68.700) |
| Anuncios de comerciantes con margen, mediana por captura | 0 (todos particulares) | 6 |

El cupo es la suma de los anuncios de una captura. No es simultáneamente ejecutable: cada orden se paga y se libera por separado, en minutos.

**Lectura:** es la única señal local que se repitió dos días y que hoy incluyó comerciantes. Sigue siendo **CONDICIONADO**:
- pago en pesos a un tercero, con riesgo de fraude o triangulación y de bloqueo bancario;
- comisión P2P y tiempo de liberación no verificados;
- límites por orden.

**Margen frente a costos no verificados:** con +0,20% de mediana, cualquier costo oculto mayor a 0,2% lo anula.

**Recomendación:** es la candidata con más valor informativo para pasar al laboratorio de simulación. Primero hay que medir la persistencia en varios días, los tiempos de liberación y la comisión real. Sin capital.

## 5. Estado y próximos pasos

- **Tareas programadas de Windows:**
  - "PieAPie FX": días hábiles de 10:00 a 15:05.
  - "PieAPie CCL": días hábiles de 11:00 a 17:05.
  - Las dos también corren al iniciar sesión, así que retoman tras un reinicio.
- **CCL:** acumular 3 a 5 ruedas completas, con la apertura, antes del veredicto final. Hoy: observación pasiva, sin edge.
- **Ruta oficial → USDT:** NO VIABLE localmente. Se mantiene la captura diaria para detectar si el P2P en USD baja de forma persistente de ~1,05. Eso sería el único cambio que justificaría reabrirla.
- **Cash-and-carry y Polymarket:** sin cambios (monitor y observación pasiva).
