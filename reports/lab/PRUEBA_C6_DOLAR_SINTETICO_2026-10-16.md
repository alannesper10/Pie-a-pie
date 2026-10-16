# C6: dólar sintético con futuros de A3 (Hull EN 5.10): **DESCARTAR** (16/10/2026)

La regla quedó registrada en `PRUEBAS_HULL_C1_C6_2026-10-16.md` **antes** de correrla y no se modificó. Hubo una sola corrección, de un error de datos con su test: el último ciclo usaba un contrato que todavía no había vencido.

Los US$1.000 virtuales siguen sin asignar. No hubo operaciones reales.

## Ciclo evaluado

Inversor con US$1.000:
1. Vende los US$ por MEP (punta compradora).
2. Pone 85% de los pesos a plazo fijo a 30 días y 15% en caución, como garantía y colchón de las diferencias diarias del futuro.
3. **Compra** el futuro DLR que vence a fin del mes siguiente, por US$1.000 de nominal.
4. Al vencer, el futuro liquida contra el A3500 y los pesos vuelven a US$ por MEP (punta vendedora).

## Datos

Todos públicos y guardados en `lab_data/`:

| Dato | Fuente | Calidad |
|---|---|---|
| Ajustes diarios de los futuros DLR (27.059 registros, 01/2020–10/2026) | A3, `apicem.matbarofex.com.ar/api/v2/closing-prices` | **Oficial**. Control: el ajuste final de cada contrato vencido coincide **exactamente** con el A3500 (diferencia máxima 0,0%) |
| A3500 | BCRA, API v4, variable 5 | **Oficial** |
| Tasa de depósitos a 30 días (TNA) | BCRA, variable 12 | **Oficial**. Es un promedio del sistema: la tasa de un banco concreto puede ser distinta |
| Dólar MEP compra/venta | argentinadatos (`/cotizaciones/dolares/bolsa`) | **Indicativo** (cierres diarios, no puntas ejecutables) |
| Letra del Tesoro a 13 semanas | US Treasury, daily bill rates (FRED no respondía) | Oficial |

**Notas sobre la descarga de A3:**
- La API de A3 se cuelga con consultas por rango de fechas y falla de forma intermitente.
- La descarga tiene reintentos y guarda cada página en disco. No se rellenó ninguna página.

## Costos y supuestos

| Concepto | Valor | Estado |
|---|---|---|
| Conversión MEP | 0,25% por conversión (2 por ciclo), sobre las puntas compra/venta | SUPUESTO |
| Futuro (mercado + broker) | 0,1% del nominal por lado | SUPUESTO; no se encontró un tarifario oficial |
| Garantía + colchón de diferencias | 15% de los pesos en caución a (tasa − 2 pp) | SUPUESTO; no se encontraron los márgenes oficiales vigentes de Argentina Clearing |
| Sensibilidad | Costos ×1,5 | — |

## Resultados

| Período | Ciclos | Rendimiento medio sobre el capital total | t | Positivos | Peor | Acumulado | Drawdown | Exceso sobre la letra | Pata del futuro sobre la garantía (15%) |
|---|---|---|---|---|---|---|---|---|---|
| **Válido: 05/2025–09/2026** | **16** | **−1,96% por mes** | **−3,09** | **2/16** | −9,85% | **−27,5%** | −27,5% | −2,28% por mes (t −3,58) | −10,8% por mes (peor −40,8%) |
| Válido, costos ×1,5 | 16 | −2,30% por mes | −3,64 | 2/16 | −10,2% | −31,5% | — | −2,63% por mes | −11,4% por mes |
| Descriptivo 01/2020–04/2025 (cepo; **no válido** para la decisión) | 63 | −1,17% por mes | −1,21 | 29/63 | −22,3% | −60,5% | −72,0% | −1,39% por mes | −5,8% por mes |

**Descomposición media por mes, período válido** (en % del capital):
- tasa en pesos cobrada: **+2,42**;
- costo implícito del futuro (F₀/A3500 − 1): **−2,97**;
- cambio de base MEP/A3500: **−0,74**;
- costos: ~**−0,7**.

**Por qué falla:**
- En **11 de 16 meses**, la tasa implícita del futuro **superó** a la tasa de plazo fijo. El futuro de dólar descuenta tasas en pesos mayores que las que paga un depósito minorista. La paridad cubierta de Hull se cumple contra las tasas mayoristas, no a favor del ahorrista.
- La brecha MEP/A3500 se amplió en promedio, y llegó a +10% en septiembre de 2025. Esa base **no se cubre** con el futuro, que liquida contra el A3500.
- **Rendimiento sobre la garantía:** −10,8% por mes. El apalancamiento del futuro amplifica el resultado y no compensa la desventaja estructural.

## Limitaciones

- **Muestra corta:** 16 ciclos posteriores a la unificación cambiaria. Igual alcanza para un rechazo claro (t −3,09, 2 positivos de 16). No alcanzaría para afirmar una ganancia.
- **MEP indicativo:** son cierres diarios, no puntas ejecutables.
- **Tasa promedio:** la tasa de plazo fijo es el promedio del sistema. Con la mejor tasa del mercado la tasa en pesos mejora unos pocos puntos anuales, insuficiente frente a −2% por mes.
- **Costos sin verificar:** los márgenes y comisiones del futuro son supuestos. La sensibilidad ×1,5 no cambia la conclusión.
- **Comparación:** el dólar sin invertir (0%) es una alternativa más débil que la letra, y la estrategia también pierde contra ella.

## Hipótesis que NO se probaron (sería una regla nueva, a registrar antes)

**Operación inversa:** vender el futuro cuando la tasa implícita es mucho mayor que la del plazo fijo, es decir apostar a que la devaluación sea menor que la implícita. Es **direccional** (no tiene cobertura) y queda fuera del mecanismo de paridad cubierta de Hull.

## Reproducir

```
python -m pytest -q tests/test_ars_synthetic.py
```

- **Módulo:** `lab/research/ars_synthetic.py`.
- **Datos:** `lab_data/c6_dlr_pages/`, `lab_data/c6_raw.json`, `lab_data/dtb3_cache.json`.
- **Ciclos:** `lab_data/c6_cycles.json`.
