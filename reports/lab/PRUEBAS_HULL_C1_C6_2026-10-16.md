# Pruebas derivadas de Hull: C1, C2, C3, C5 y registro de C6 (16/10/2026)

Las reglas están fijadas en `BIBLIOTECA_HULL_ESTRATEGIAS_2026-10-16.md` (Fase 4) **antes** de correr. Ninguna se modificó después de ver resultados. Las únicas correcciones fueron de tests: valores esperados sin la comisión de entrega o con un tope de capital mal puesto en el test.

Los US$1.000 virtuales siguen **sin asignar**. No hubo operaciones reales; Kalshi y `data/` están intactos.

## C2. Strangle muy fuera del dinero comprado (Hull BS 19.1): **DESCARTAR**

**Datos:** trades reales de history.deribit.com, ventana 08:00–12:00 UTC del vencimiento mensual anterior, y entrega oficial btc_usd.

**Regla:** comprar el put de delta −0,05 y el call de delta +0,05, 0,1 BTC, al precio de ask (mediana de los trades "buy"); mantener hasta el vencimiento.

| | Meses | Operaciones | No verificables | Ganadoras | Exceso medio sobre la letra, por operación, sobre la prima | t | P&L total |
|---|---|---|---|---|---|---|---|
| Muestra 2020–2023 | 47 | 23 | **51%** (más del 20%: el tramo es **NO VERIFICABLE**) | 2/23 | −19,5% | −0,29 | −US$555 |
| **Fuera 2024–2026** | 33 | 28 | 15% | **2/28** | **−39,0%** | −0,68 | −US$1.078 |
| Fuera, costos ×1,5 | 33 | 28 | 15% | 2/28 | −42,2% | −0,78 | −US$1.164 |

Lectura:
- Las alas a 5 delta casi nunca terminan dentro del dinero, y cuando lo hacen no pagan lo suficiente.
- Se confirma la advertencia de Hull (BS 19.1): la oportunidad desaparece cuando el mercado valúa la sonrisa de volatilidad. En BTC, la IV de las alas ya incorpora las colas.
- Faltan trades en las alas en la mitad de los meses de 2020–2023, porque eran poco líquidas.

## C1. Volatilidad condicional, EWMA contra IV ATM (hipótesis propia con herramientas de Hull EN 22.2/22.6 y BS 11.2): **DESCARTAR**

**Regla:**
- σ_EWMA (λ = 0,94, índice btc_usd diario hasta el día anterior);
- si σ_EWMA > 1,10·IV: comprar el straddle ATM al ask;
- si σ_EWMA < 0,90·IV: vender un iron butterfly (straddle al bid + alas de 0,10 delta al ask);
- en otro caso, no se opera;
- 0,1 BTC, hasta el vencimiento.

| | Meses | Operaciones (straddle / iron butterfly) | Sin señal | No verificables | Ganadoras | Exceso medio por operación | t | P&L |
|---|---|---|---|---|---|---|---|---|
| Muestra | 47 | 24 (12/12) | 20 | 6% | 7/24 | **−32,1%** | **−2,69** | −US$2.689 |
| Fuera | 33 | 15 (6/9) | 11 | **21%** (más del 20%: **NO VERIFICABLE**) | 8/15 | −1,8% | −0,14 | +US$568 |
| Fuera, costos ×1,5 | 33 | 15 | 11 | 21% | 8/15 | −2,5% | −0,20 | +US$478 |

Otros resultados:
- **Capital:** el capital por operación llega a **US$1.650** (iron butterfly) y la media fuera de muestra es US$919. Viola el límite de 25% de US$1.000.
- **Diagnóstico por lado** (descriptivo, **no cambia el veredicto**):
  - en la muestra perdieron los dos lados (straddle −15,7% medio, iron butterfly −48,1%);
  - fuera de muestra, el iron butterfly ganó 7 de 9 (+20% medio) y el straddle perdió 5 de 6.
- Quedarse solo con el iron butterfly sería elegir la regla mirando los resultados. Si se quisiera probar, tendría que registrarse como hipótesis nueva y evaluarse **hacia adelante**, no con estos datos.

## C3. Box spread y límites en Deribit con precios ejecutables: **en curso**

**Captura:** libros (mejor bid y ask) de las 940 opciones de BTC más el índice, cada 5 minutos durante 24 horas, desde el 16/10 a las ~14:33. Archivo: `lab_data/c3_deribit_boxes.jsonl`.

**Foto de las 14:3x** (2.101 boxes con capital ≤ US$1.000):

| Lado | Resultado |
|---|---|
| **Comprar el box** (prestar) | Mejor caso: **2,7 puntos por debajo de la letra** en el período (25JUN27 30k/40k: tasa implícita neta 0,27% anual) |
| **Vender el box** (pedir prestado e invertir en la letra) | Mejor caso: **−3,6%** del pago |

Con US$1.000, las 4 patas pagan comisiones de ~1,3% del nominal del box. Se necesitarían desvíos enormes.

Decisión pendiente de la captura completa. Con este margen, se espera **DESCARTAR**.

## C5. Prima de backwardation normal (Hull EN 5.14): medición, **DESCARTAR** como estrategia

**Medición:** (F₀ − S_T)/S₀, entrando el día siguiente a la entrega anterior (~90 días), en los trimestrales USDⓈ-M de Binance.

| | n | Prima media del corto en futuros, por trimestre | t | Base media al entrar | Desvío |
|---|---|---|---|---|---|
| BTC muestra | 7 | −5,5% | −0,34 | +1,0% | 42,8% |
| BTC fuera | 10 | −5,3% | −0,57 | +2,5% | 29,3% |
| ETH muestra | 7 | −1,5% | −0,10 | +0,8% | 37,8% |
| ETH fuera | 10 | −0,7% | −0,06 | +2,4% | 37,7% |

No hay prima significativa: |t| < 0,6. La dispersión, de 30–40% por trimestre, domina. Como estrategia sería exposición direccional sin una ventaja medible.

## C6. Paridad de tasas cubierta en Argentina (Hull EN 5.10): **datos verificados, regla registrada**

**Datos encontrados (públicos, sin credenciales):**
- `apicem.matbarofex.com.ar/api/v2/closing-prices?product=DLR&from=…&to=…`;
- 27.059 registros diarios de los contratos DLR desde 01/2020: precio de ajuste, volumen, interés abierto y la **tasa implícita** que publica A3;
- spot mayorista y MEP diarios (argentinadatos, **indicativos**);
- tasas en pesos: API del BCRA (a verificar la serie de plazo fijo de 30 días).

**Regla registrada antes de mirar resultados (hipótesis propia sobre la relación de Hull EN 5.10).** "Dólar sintético" para un inversor con US$:
- **Entrada:** el último día hábil del mes m, vender US$ por MEP (punta compradora), poner los pesos a plazo fijo a 30 días y **comprar** el contrato DLR que vence al fin del mes m+1 por el mismo nominal en USD.
- **Salida:** al vencer, el futuro liquida contra el A3500. Se recompran US$ por MEP (punta vendedora).
- **Resultado en USD:** [ARS₀·(1 + i·d/365) + N·(A3500_T − F₀)] / MEP_T − N.
- **Costos:**
  - 2 conversiones MEP (0,25% de broker + medio spread de los bonos, SUPUESTO);
  - futuro: 0,1% del nominal por lado, entre mercado y broker (SUPUESTO, a verificar);
  - la garantía del futuro (~10%) se supone en caución.
- **Benchmark:** dólares sin invertir (0%) y, estricto, la letra del Tesoro.
- **Período válido:** desde 05/2025, después de la unificación cambiaria de abril de 2025. 2020–2025 se informa solo descriptivo, porque con cepo la brecha MEP/A3500 hace que la estrategia sea otra.
- **Aceptación:** los criterios comunes. Con ~17 meses la muestra es corta: aunque dé positivo, el máximo veredicto posible es CORREGIR, con validación hacia adelante.
- **Riesgos que se informan:**
  - la brecha MEP/A3500 entre la entrada y la salida (es la principal);
  - el riesgo de contraparte y de cierre de posiciones del mercado local;
  - la restricción cruzada de 90 días (Com. "A" 8336) **no aplica**, porque no se usa el dólar oficial.

## Estado de la búsqueda

| Candidata | Decisión |
|---|---|
| C2 strangle comprado | **DESCARTAR** |
| C1 volatilidad condicional | **DESCARTAR** (capital excesivo; muestra negativa; fuera de muestra no verificable) |
| C3 box/paridad | En curso; se espera DESCARTAR |
| C5 backwardation normal | **DESCARTAR** (no hay prima medible) |
| C6 dólar sintético con A3 | **Siguiente prueba**: datos verificados, regla registrada |
| C4 calendario de volatilidad | Pendiente; reutiliza `lab_data/deribit_windows/` |

## Reproducir

```
python -m pytest -q tests/test_options_hull.py tests/test_deribit_parity.py
```

- **Módulos:** `lab/research/options_hull.py` (C1, C2) y `lab/research/deribit_parity.py` (C3).
- **Resultados:** `lab_data/c1_c2_options_hull.json`, `lab_data/c5_backwardation.json`, `lab_data/c3_deribit_boxes.jsonl`.
