# Informe con muestra parcial — corrida watch-b-20261013 (14/10/2026)

**Estado: PARCIAL. No es el informe definitivo.** La recolección se detuvo en la
captura 250, a las 14:50 ART del 14/10. Claude Code la frenó porque la notebook
se quedó sin memoria; el proceso venía estable en unos 308 MB. No se reanudó.
Todo es observación y simulación: no hubo órdenes, credenciales ni dinero real.

Convenciones:
- **OBSERVADO** = dato crudo público.
- **ESTIMADO** = neto con costos modelados.
- **SIMULADO** = ejecución con latencia, fills parciales y liquidez compartida.
- **NO VERIFICABLE** = no se puede afirmar con los datos que hay.

## 1. Integridad y continuidad de la muestra

| Control | Resultado |
|---|---|
| `PRAGMA integrity_check` de `lab_data/watch.sqlite` | ok |
| Capturas | 251 (ticks 0–250), sin faltantes ni duplicados |
| Sesión 1 | ticks 0–70: 13/10, 16:40–17:51 ART (19:40–20:51Z) |
| Sesión 2 | ticks 71–250: 14/10, 11:48–14:49 ART (14:48–17:49Z) |
| Huecos > 120 s | uno solo, entre sesiones (ticks 70 → 71, la pausa de la noche) |
| Polymarket | 208–277 libros completos por captura; 0 recortes |
| Futuros | 26 libros y 20 contratos con vencimiento en todas las capturas |
| BYMA / Nasdaq | 40 especies / 12 ADR en todas las capturas |
| Errores de fuentes | 39, todos de data912 (timeouts y cortes SSL), en 14 capturas: 52–54, 127–130, 191–193, 224, 232–234 |

En esas 14 capturas falta solo data912; el resto de las fuentes está completo.

**Preservación de los datos:**
- La base original quedó sin tocar (sha256 `98ee1598…c9a719`). Hay una copia en `lab_data/watch.backup-20261014.sqlite`.
- La evaluación corrió sobre otra copia, `lab_data/watch.eval-20261014.sqlite`.
- `data/` (dataset oficial de HORUS) no se modificó.
- Las dos posiciones paper de Kalshi no se tocaron: `data/state.json` sha256 `df1fe26a…0f468`, `data/paper_trades.csv` sha256 `d1035bca…12b`.

## 2. Cash-and-carry (spot largo + futuro corto, a vencimiento)

**Oportunidades observadas:** 5.018 observaciones de 22 contratos (Binance, Bybit, Deribit; BTC y ETH).

**Costos completos (por operación ida y vuelta, a 1x):**
- Comisión spot taker 0,10% (SUPUESTO).
- Comisión futuro taker 0,05% (SUPUESTO).
- Entrega 0,05% (SUPUESTO).
- Medio spread medido (ESTIMADO).
- **Costo de oportunidad:** letra del Tesoro de EE.UU. DTB3 al 4,06% (FRED, OBSERVADO), llevada al plazo de cada contrato.

**Rendimiento neto (ESTIMADO, ex ante):**

| Contrato | Días | Neto esperado | Letra mismo plazo | Exceso máximo |
|---|---|---|---|---|
| Binance BTC 26/03/27 | 162,6 | +1,00% a +1,04% | 1,87% | −0,83% |
| Binance ETH 26/03/27 | 162,6 | +0,82% a +0,90% | 1,87% | −0,97% |
| Binance BTC 25/12/26 | 71,6 | +0,36% a +0,40% | 0,81% | −0,41% |
| Binance ETH 25/12/26 | 71,6 | +0,27% a +0,31% | 0,81% | −0,51% |
| Bybit BTC/ETH 27/11/26 | 43,6 | −0,07% a +0,15% | 0,49% | −0,34% / −0,41% |
| Bybit y Deribit, vencimientos semanales | 1,5–15,6 | negativo | — | −0,13% a −0,24% |

- **Señales de la regla congelada** (exceso ex ante sobre la letra > 0): **0 de 5.018**. El mejor exceso fue −0,135%.
- Esto coincide con el histórico: la regla no se cumple desde el 4/2/2025.

**Simulación del laboratorio** (`evaluate --fresh-ledger`):
- 184 ejecuciones simuladas, neto +US$50,79, +0,305% sobre el capital comprometido.
- El veredicto del laboratorio es **NO RENTABLE**, porque el P&L realizado es 0: ningún contrato venció dentro de la muestra.
- Estas cifras **no son evidencia de rentabilidad**:
  - no descuentan la letra;
  - las 184 son reentradas en los mismos contratos, captura tras captura (sobre todo Binance ETH 25/12 y 26/03), no operaciones independientes;
  - hay 6 episodios con alguna captura ejecutable.
- **No hay que mezclarlas con resultados realizados.**

**Ejecutabilidad:**
- La base es persistente: los contratos trimestrales están en las 251 capturas.
- En Binance BTC fue INFEASIBLE_MIN_SIZE con capital de US$100.

**Riesgo:**
- Liquidación del corto a 1x: haría falta una suba de alrededor del 99%. El margen de mantenimiento del 0,5% es SUPUESTO.
- A 2x el riesgo es material (histórico: 108 de 763 entradas).

**Limitaciones:**
- Son 2 días de observación de una estrategia de 1,5 a 162 días de plazo.
- El resultado observado a vencimiento queda **pendiente**: el primer trimestral vence el 25/12/2026.

**Anomalía de datos:** Deribit ETH 17/10 mostró en las capturas 82 y 103 un único bid a 1.251,5 contra un spot de unos 2.430, o sea un libro casi vacío. Da un neto de −32%, no es una oportunidad y no afecta las conclusiones.

**Conclusión:** sin cambios. Hoy no supera a la letra en ningún contrato. Se mantiene como monitor (`python -m lab.carry_monitor`) y no se opera.

## 3. Polymarket — comprar todos los NO (eventos negRisk)

**Oportunidades observadas:** 7.702 evaluaciones con libros completos. Motivos de descarte:
- NO_EDGE_AFTER_FEES_OR_MIN_SIZE: 6.060
- BUDGET_TOO_SMALL: 1.572
- NO_BOOK_FOR_LEG: 68
- DISAPPEARED: 2

**Costos:** comisión de Polymarket según el `feeSchedule` de cada mercado (VERIFICADO: tasa 5%, exponente 1, solo taker), más precio de ejecución contra el libro.

**Neto estimado positivo: 3 observaciones, todas de 1 sola captura (< 60 s)** y todas durante partidos de Champions en vivo del 13/10:

| Captura | Evento | Bruto | Comisiones | Neto estimado | % s/ capital | Simulado con latencia |
|---|---|---|---|---|---|---|
| 51 (17:31 ART) | ucl-atm-mnu | US$0,76 | US$0,41 | +US$0,35 | +0,69% | DISAPPEARED, −US$0,62 |
| 59 (17:40 ART) | ucl-int-bru | US$1,81 | US$0,59 | +US$1,22 | +2,41% | DISAPPEARED, −US$1,01 |
| 70 (17:51 ART) | ucl-atm-mnu | US$0,001 | US$0,0002 | +US$0,0009 | — | tamaño 0, partido prácticamente definido |

**Ejecutabilidad:** 0 de 3. Las dos con tamaño desaparecieron antes de la ejecución simulada, y ejecutarlas tarde habría perdido plata.

**Validación pendiente.** Esto **no es** evidencia de rentabilidad. Para validarlo haría falta:
- Captura sub-segundo durante partidos en vivo. Con un minuto entre capturas no se ve si el desajuste dura lo suficiente.
- Profundidad del libro a tamaño completo en las k patas, en el mismo instante.
- Al menos 30 ejecuciones simuladas en al menos 6 períodos, con neto positivo fuera de muestra y con costos ×1,5.
- Confirmar que la latencia real de envío no elimina el desajuste.

**Conclusión:** se mantiene el veredicto provisorio de **descartar** la estrategia pasiva. Queda abierta, sin evidencia, una línea "eventos en vivo" que requiere otra infraestructura de datos.

## 4. CCL y MEP entre emisoras

> **La muestra NO cubre la rueda completa.** Del 14/10 faltan las últimas
> **2 horas y 10 minutos** de rueda (14:50–17:00 ART), incluido el cierre, y
> también la apertura (11:00–11:48). Del 13/10 solo hay los últimos 20 minutos
> de rueda (16:40–17:00). Esas horas **no se extrapolan**: el comportamiento
> del cierre, cuando suelen ampliarse los diferenciales, queda **sin observar**.
> Ninguna conclusión de esta sección es definitiva.

Rueda observada: 200 capturas, unas 3 horas 20 minutos (20 del 13/10 y 180 del 14/10).

| Día y franja | Capturas | MEP data912 | CCL data912 | CCL BYMA demorado + Nasdaq |
|---|---|---|---|---|
| 13/10, rueda (16:40–17:00) | 20 | 2.640 obs, SIN_EDGE; bruto máx +0,026% | 2.200 obs, SIN_EDGE; bruto máx +0,62% (SUPV→CRESY), neto −0,11% | 1.278 NO_VERIFICABLE |
| 14/10, rueda (11:48–14:49) | 180 | 22.308 obs, SIN_EDGE; bruto máx +0,20% | 18.590 obs, SIN_EDGE; bruto máx +0,50% (LOMA→TGS), neto −0,23% | 13.059 NO_VERIFICABLE + 99 SOSPECHOSO |
| 13/10, fuera de rueda | 51 | SIN_EDGE | SIN_EDGE (precios locales viejos) | NO_VERIFICABLE + 18 SOSPECHOSO |

Medianas en rueda: bruto MEP −0,84% a −1,48%; bruto CCL −1,19%.

**Costos completos:**
- Derecho de mercado BYMA: 5 pb + IVA = 0,0605% por operación (VERIFICADO).
- Broker local: 0,25% (SUPUESTO).
- Broker EE.UU.: 0,05% (SUPUESTO).
- Tasa SEC sobre ventas (SUPUESTO).
- Cuatro operaciones por ciclo.
- El costo por operación que soportaría el mejor diferencial observado es 0,154%, contra unos 0,31% supuestos.

**Oportunidades:**
- POTENCIAL: **0 episodios** (neto > 0 con costos ×1,5 y puntas simultáneas).
- Rendimiento neto: negativo en todas las observaciones verificables.

**Ejecutabilidad:**
- No verificable. Solo hay mejor punta, sin profundidad.
- La demora de data912 respecto del mercado **no está verificada**, aunque sus cotizaciones cambiaron en 169 de 180 capturas.
- Los cruces BYMA–Nasdaq no son simultáneos: BYMA gratuito tiene unos 20 minutos de demora.

**Chequeo de ratios:**
- YPF: NO_CONSISTENTE en 237 de 237 capturas. Se excluye; el ratio público 1:1 no coincide con los precios.
- BMA, EDN, CRESY y TEO: NO_CONSISTENTE en 48 capturas cada uno, todas fuera de rueda.

**Defecto detectado (pendiente de corregir, con test):** cuando data912 falla, el cruce BYMA+Nasdaq deja de filtrar los ratios inconsistentes. De ahí salen los 117 SOSPECHOSO, por ejemplo LOMA→YPF con +906%. No cambia ningún veredicto, porque ese cruce ya es NO_VERIFICABLE, pero hay que corregirlo antes de la próxima recolección.

**Normas cambiarias vigentes:** NO VERIFICADAS (plazos mínimos de tenencia, cruces entre monedas).

**Conclusión provisoria:** con unas 3 horas 20 minutos de rueda no apareció ningún diferencial que cubra los costos supuestos. **Pendiente:**
- el cierre de rueda;
- la apertura;
- más días;
- costos reales del broker;
- normas vigentes;
- verificar la demora de data912.

## 5. Resumen

| Estrategia | Observaciones | Neto estimado > 0 | Ejecutables | Rendimiento neto | Estado |
|---|---|---|---|---|---|
| Cash-and-carry | 5.018 | 0 sobre la letra | — | −0,13% a −0,97% de exceso | Monitor; no operar |
| Polymarket (todos los NO) | 7.702 | 3 (1 captura cada una) | 0 | Simulado negativo | Descartar la versión pasiva; la de eventos en vivo queda sin evidencia |
| CCL / MEP | 45.738 en rueda (data912) | 0 | No verificable | Negativo | Provisorio; falta el cierre de rueda |

**Pendiente para una segunda recolección:**
- Rueda completa, con apertura y cierre, de varios días.
- Solo la fuente ccl en horario de rueda, para usar menos memoria.
- Corregir el filtro de ratios.
- Obtener costos reales del broker.
