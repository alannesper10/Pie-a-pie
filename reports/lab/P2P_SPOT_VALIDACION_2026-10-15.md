# P2P → libro de Binance: costos, riesgos y simulación de ejecución (15/10/2026)

Investigación y simulación. No hubo órdenes, movimientos de fondos ni claves. No se tocaron el ledger, las posiciones de Kalshi, los datos de HORUS ni el ejecutor.

**Clasificación: PENDIENTE DE UN DATO CONCRETO.** El dato es la comisión y la demora del retiro de pesos de Binance a la cuenta bancaria. Ese costo define el resultado:

| Comisión de retiro | Resultado |
|---|---|
| 0% | La estrategia da margen neto positivo en todos los ciclos simulados |
| 0,10% | Positiva |
| 0,25% o más | Desaparece: ningún ciclo supera el umbral de entrada |

Binance no publica ese costo. Se ve en la pantalla de retiro de la app, sin operar (sección 6).

## 1. Costos: qué se confirmó y qué no

| Costo | Valor | Estado | Fuente / cómo se intentó |
|---|---|---|---|
| Venta en el libro (taker) | 0,100%; 0,075% pagando con BNB | **VERIFICADO** | Tabla oficial binance.com/en/fee/trading, usuario regular (consultada el 15/10) |
| Maker en el libro | 0,100% (0,075% con BNB) | **VERIFICADO** | Misma página. No mejora al taker y agrega riesgo de no ejecución: se descarta |
| Compra P2P como tomador | 0% | **PUBLICADO, no confirmado en la cuenta** | Anuncio de Binance del 2021 ("0 fees for takers; makers 0–0,35%") y Binance Square. No hay página oficial vigente: la URL del FAQ ya no existe. Los campos `takerCommissionRate` de la API pública vienen en `null` |
| Traspaso de Funding a Spot | 0, inmediato | Práctica conocida de Binance | No se verificó por API sin clave |
| **Retiro de ARS al banco** | **DESCONOCIDO** | **NO PUBLICADO** | El FAQ oficial ("How to Withdraw ARS", actualizado el 09/09/2026) dice que la comisión se ve en la pantalla de retiro, no da plazo y solo admite transferencia bancaria a CBU/CVU/alias. Se probaron endpoints públicos de canales fiat: 404 o 403. Una fuente de terceros con más de 700 días habla de 1% (no confiable) |
| Depósito de ARS (no hace falta para el circuito) | Hasta 1 día hábil | Oficial | FAQ "How to Deposit ARS" (22/05/2026) |
| Pago al vendedor P2P | 0 (transferencia inmediata desde Mercado Pago, Naranja X o BNA) | Supuesto razonable | Las transferencias en pesos entre cuentas son inmediatas; los límites diarios de cada cuenta aplican |
| Precio anunciado vs. ejecutado | El precio del anuncio se fija al abrir la orden (escrow) | Mecánica de Binance P2P | El riesgo no es el precio sino que el anuncio desaparezca o se agote; el simulador exige cupo (`qty`) y límites |

**Por qué existe el margen:** el que vende USDT en P2P cobra los pesos directo en su banco. El que vende en el libro tiene que retirarlos de Binance, con costo, demora y límites. El descuento del P2P frente al libro (~0,1–0,3%) es, al menos en parte, el precio de esa fricción. **El margen solo existe si nuestro retiro de pesos es más barato o más rápido que lo que el mercado descuenta.**

## 2. Contraparte: particulares y comerciantes

Foto puntual del 15/10, ~15:30: 100 anuncios de compra de USDT, con el perfil público de cada anunciante (`lab_data/fx_ar/p2p_profiles_20261015.json`).

| | Comerciantes (61 anuncios) | Particulares (39) |
|---|---|---|
| Órdenes completadas (p10 / p50) | 2.525 / 9.842 | 114 / 483 |
| Finalización en 30 días (p10) | 98,9% | 93,4% |
| Antigüedad de la cuenta (p10) | 690 días | 353 días |
| **Liberación promedio en 30 días (p50 / p90)** | **97 s / 295 s** | 96 s / 909 s |
| Orden mínima / máxima (p50) | $100.000 / $6.000.000 | $20.000 / $500.000 |
| Cupo por anuncio (p50) | 832 USDT | 154 USDT |
| Margen frente al bid a esa hora (p50 / p90) | −0,03% / +0,04% | +0,08% / +0,19% |

El margen depende de la hora: en las capturas de las 12:05 a las 15:00 los comerciantes llegaron a +0,22%.

**Criterio de exclusión propuesto.** El filtro "solid" del simulador ya usa los primeros puntos; el resto queda para el monitor.
- Comerciante.
- Al menos 1.000 órdenes completadas.
- Finalización en 30 días de al menos 98%.
- Cuenta con 365 días o más.
- Liberación promedio de 300 s o menos.
- KYC aprobado.
- Medio de pago a nombre propio del usuario (Mercado Pago, Naranja X, BNA).
- Sin KYC adicional.

**Aplicado a la foto de las ~15:30:**
- 51 de 100 anuncios pasan el criterio, y 22 de ellos tenían margen positivo, con ~32.900 USDT de cupo sumado.
- Pero a esa hora el mejor margen era de solo +0,08%: **el filtro deja pasar suficientes anuncios, y el límite lo pone el margen del momento**.

**Qué protege y qué no:**
- Los USDT del vendedor quedan en el escrow de Binance desde que se abre la orden. Si el comprador pagó y el vendedor no libera, se apela con el comprobante.
- La plataforma **no protege los pesos**: una transferencia hecha no se revierte.
- La reputación reduce la probabilidad de problemas, pero **no garantiza nada**.

**Riesgos que ningún filtro elimina:**
- Bloqueo o cierre de la cuenta bancaria por muchas transferencias a desconocidos (el banco puede pedir justificación).
- Que el vendedor esté usando fondos de origen ilícito (triangulación), con riesgo de verse involucrado en un reclamo.
- Tratamiento impositivo de una actividad habitual (Ganancias).
- Las reglas de Binance exigen pagar desde una cuenta a nombre propio y prohíben los pagos de terceros. No se propone eludir ningún control.

## 3. Simulación de ejecución

Módulo `lab/research/p2p_spot.py` (tests en `tests/test_p2p_spot.py`). La grilla de escenarios la corre `lab/research/p2p_spot_run.py`. Datos: 96 capturas del 14/10 (15:29–17:04) y 175 del 15/10 (12:05–15:00), es decir **4,5 horas en dos días**.

Cómo trata cada ciclo:
- **No se solapan:** el siguiente empieza recién cuando el capital del anterior volvió al banco. Las capturas **no se cuentan como operaciones independientes**.
- **Elección del anuncio:** el más barato que pasa los filtros de medio de pago, contraparte, límites y cupo, y que supera un margen esperado de 0,05% contra el bid de ese momento.
- **Tiempos:** pago 180 s [SUPUESTO] + liberación 97 s (p50) o 295 s (p90) [OBSERVADO].
- **Venta:** en la primera captura posterior, recorriendo los niveles del libro. Así entran el deslizamiento real y el movimiento de precio.
- **Retiro de ARS:** comisión en escenarios de 0 a 1%, demora de 15 min o 24 h.
- **Huecos de datos:** si la venta cae en un hueco de más de 3 minutos, el ciclo queda SIN_DATOS, sin rellenar.

Escenario base: comerciantes, capital de $500.000, venta con 0,10%, P2P al 0%, liberación p50, retiro en 15 min.

| Comisión de retiro de ARS | Ciclos | Positivos | Neto mediano | Peor ciclo | Ganancia total (4,5 h) |
|---|---|---|---|---|---|
| 0% | 7 | 7 (100%) | **+0,120%** | +0,008% | $4.018 |
| 0,10% | 3 | 3 | +0,097% | +0,044% | $1.169 |
| 0,25% / 0,50% / 1% | **0** | — | — | — | $0 |

Sensibilidad, sobre la base con retiro sin costo:

| Cambio | Ciclos | Neto mediano | Ganancia total |
|---|---|---|---|
| Capital $100.000 / $2.000.000 / $5.000.000 | 6 / 7 / 7 | +0,12% | $604 / $6.815 / $8.643 |
| Contraparte "solid" (comerciante o particular con 100 órdenes o más y 98%) | 12 | +0,20% | $5.535 |
| Cualquier contraparte | 12 | +0,25% | $5.099 |
| Liberación p90 (295 s) | 6 | +0,12% | $2.291 |
| Comisión P2P de 0,10% | 3 | +0,10% | $1.171 |
| Venta pagando con BNB (0,075%) | 8 | +0,15% | $5.010 |
| Retiro de 24 h (un ciclo por día) | 2 | +0,12% | $368 |

**Lectura:**
- **Ejecutable:** el libro absorbió todas las ventas, sin ciclos SIN_PROFUNDIDAD. El peor movimiento de precio entre la decisión y la venta fue −0,043%. Con liberación p50, el ciclo dura ~20 minutos incluyendo 15 de retiro.
- **Escala chica:**
  - el capital útil se satura en ~$2.000.000 a $5.000.000 por ciclo, por los máximos y el cupo de los anuncios;
  - la ganancia ronda los $900 a $1.900 por hora observada, en el mejor escenario de costos;
  - con $5.000.000 son $8.643 en 4,5 horas: ~0,17% sobre el capital en el período.
- **Muestra corta:** 7 a 12 ciclos en dos tardes. No alcanza para afirmar repetibilidad: harían falta al menos 30 ciclos en 6 o más días.
- **Frecuencia** (mejor anuncio de comerciante por captura, neto de la venta):
  - 15/10: margen de 0,05% o más en 113 de 175 capturas, de 0,15% o más en 46, y de 0,30% o más en ninguna;
  - 14/10: casi sin comerciantes con margen. La captura guardaba solo la primera página de 20 anuncios; ya se amplió a 3 páginas (sección 5).

## 4. Trabas y soluciones

| Traba | Causa | Alternativas investigadas | Resultado | Estado |
|---|---|---|---|---|
| Comisión de retiro de ARS desconocida | Binance no la publica; solo aparece en la pantalla de retiro | Endpoints públicos (404/403), FAQ oficial (sin el dato), terceros (no confiables) | Umbral calculado: con 0,10% sobrevive, con 0,25% muere | **PENDIENTE**: hay que leerla en la app (sección 6) |
| Evitar retirar ARS en cada ciclo | Para recomprar en P2P hay que pagar desde el banco | (a) Vender los USDT en P2P en lugar del libro: ida y vuelta P2P de −0,04% → no sirve. (b) Juntar retiros: sirve solo si la comisión es fija. (c) Publicar un anuncio propio como maker: comisión de maker histórica de 0,2–0,35% → anula el margen | Ninguna mejora el circuito salvo (b), si la comisión es fija | Parcial; depende del dato |
| Comisión P2P no confirmada | No hay página oficial vigente | Anuncio de 2021 y Square: tomador 0%. Escenario de 0,10% simulado | Con 0,10% quedan 3 ciclos con +0,10% | **PENDIENTE**: confirmarla en la pantalla de la orden |
| Tiempo de liberación | Antes no se sabía | Perfiles públicos (`avgReleaseTimeOfLatest30day`) | p50 97 s y p90 295 s en comerciantes, ya incluidos en la simulación | **RESUELTA** |
| Riesgo de contraparte | Pago en pesos irreversible | Perfiles: órdenes, finalización, antigüedad, liberación, KYC; criterio de exclusión | Filtrar comerciantes reduce los ciclos (7 contra 12) pero baja la probabilidad de problemas | **PARCIAL**: el riesgo bancario sigue |
| Captura incompleta | Solo la página 1 y sin identificar al anunciante | `fx_capture` ahora lee 3 páginas, guarda `user_no` y el perfil (una vez por día y anunciante) | Tests de regresión en `tests/test_fx_capture.py`; corrige además una consulta duplicada de perfiles | **RESUELTA** |
| Escala | Máximo y cupo de los anuncios | Más páginas, varios anuncios por ciclo | Escala natural de $2–5 millones por ciclo | Límite estructural |
| Riesgo de bloqueo bancario | Políticas del banco y de la UIF ante transferencias frecuentes a terceros | No se puede resolver con datos públicos | — | **SIN SOLUCIÓN técnica**: es una decisión de riesgo del usuario |

## 5. Automatización posible (diseño, no implementado)

| Paso | ¿API oficial? | Automatizable |
|---|---|---|
| Leer el libro USDT/ARS | Sí: REST y WebSocket públicos | Sí |
| Leer anuncios P2P y perfiles | **No**: endpoint público **no documentado** (`bapi/c2c`), puede cambiar | Sí, como monitor; frágil |
| Calcular el margen con los costos confirmados y aplicar los filtros | — | Sí |
| Registrar observaciones y decisiones | — | Sí (formato del laboratorio) |
| Avisar para pedir autorización | ntfy (secret de GitHub ya existente) | Sí |
| Abrir la orden P2P como tomador | **No hay API para tomadores** (la de C2C es de historial y de comerciantes) | **No**: humano |
| Pagar al vendedor desde el banco o la billetera | No (sin API bancaria; no se piden credenciales) | **No**: humano |
| Pasar de Funding a Spot y vender en el libro | Sí (API con clave de trading) | Más adelante, con autorización explícita |
| Retirar ARS | API de fiat no confirmada para ARS | Humano por ahora |

**Topes automáticos:**
- detenerse si faltan datos, si la comisión observada no coincide con la confirmada, si el bid cae más de X entre la alerta y la venta, o si el anuncio cambió de precio o de cupo;
- topes por ciclo y por día, alineados con `config/executor_limits.json`.

## 6. Próximo paso concreto (sin operar)

1. **Comisión y demora del retiro de ARS.** En la app de Binance: Billetera → Retirar → Fiat → ARS → transferencia bancaria. Ingresar un monto, por ejemplo $500.000, **sin confirmar**, y anotar comisión, mínimo, máximo diario y plazo informado. *Plazo: 1 día hábil.*
2. **Comisión P2P del tomador.** En P2P → Comprar USDT, abrir un anuncio hasta la pantalla de confirmación, **sin crear la orden**, y anotar la comisión mostrada.
3. **Captura ampliada.** Las tareas de Windows ya la registran: 3 páginas y perfiles, días hábiles de 10:00 a 15:05. Juntar 5 días hábiles más para tener al menos 30 ciclos simulados en 6 o más días.

Regla de decisión, fijada de antemano:
- retiro ≤ 0,10% con demora ≤ 30 min, P2P al 0%, y la simulación de 5 días con al menos 30 ciclos, ≥ 80% positivos y mediana > 0 → **APTA PARA VALIDACIÓN CONTROLADA**: un ciclo chico, con autorización explícita;
- retiro ≥ 0,25% o demora de un día → **DESCARTADA**;
- entre ambos → simular con el valor exacto y decidir con la misma regla.

La alternativa si se descarta no es abrir una investigación nueva. Es la variante (b) de la sección 4, juntar los retiros, y solo si la comisión resulta fija.

## 7. Reproducir

```
python -m lab.research.p2p_spot_run salida.json lab_data/fx_ar/fx-20261014.analysis-copy.jsonl lab_data/fx_ar/fx-20261015.hasta15.jsonl
python -m pytest -q tests/test_p2p_spot.py tests/test_fx_capture.py
```

Fuentes consultadas el 15/10/2026:
- https://www.binance.com/en/fee/trading
- https://www.binance.com/en/support/faq/how-to-withdraw-ars-argentine-pesos-on-binance-c0f32ecb63b147c9ac8de757e224922f
- https://www.binance.com/en/support/faq/how-to-deposit-ars-on-binance-argentine-pesos-ab6e7e1b950e4c76aa365be9f792c078
- https://www.financemagnates.com/cryptocurrency/binance-updates-maker-fees-for-p2p-fiat-markets/ (comisiones P2P de 2021)
- https://www.global66.com/blog/binance-p2p/ (riesgos P2P)
- https://www.infoviajera.com/?p=127580 (depósito de ARS)
- API pública de perfiles P2P: `p2p.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list`
