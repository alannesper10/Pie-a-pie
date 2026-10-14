# Arbitraje cambiario en Argentina: diagnóstico (14/10/2026)

Investigación de diagnóstico, independiente del motor de HORUS. No se
implementó ninguna estrategia ni se tocó código de producción. Tampoco hubo
órdenes, claves, movimientos de fondos ni cambios en el ledger, en Kalshi o en
`data/`.

La ruta prioritaria, dólar oficial → USDT/USDC → ARS, tiene su propio informe:
`INVESTIGACION_OFICIAL_STABLECOIN_2026-10-14.md`.

Convenciones:
- **[OFICIAL]** fuente oficial.
- **[SECUNDARIA]** prensa o blogs.
- **[OBSERVADO]** precio de una API pública.
- **[INDICATIVO]** agregador o pizarra: no es un precio ejecutable.
- **[SUPUESTO]** parámetro del modelo.
- **[SIMULADO]** resultado del cálculo.

Clasificación de cada circuito:
- **GARANTIZADO:** todas las patas son simultáneas y ejecutables.
- **CONDICIONADO:** depende de una contraparte, de plazos o de normas no verificadas.
- **ESPECULATIVO:** queda una posición abierta en el tiempo.

## 1. Metodología y muestra

- **Tiempo real:** `lab/research/fx_capture.py`, 96 capturas por minuto, 14/10 de 15:29 a 17:04 ART. Fuentes:
  - data912: 11 bonos en sus especies en pesos, D y C (puntas y cantidades);
  - Binance: libro spot USDT/ARS (100 niveles) y anuncios P2P USDT/ARS (20 por lado, con límites, medio de pago y tipo de anunciante);
  - Bitso: libros USD/ARS, USDT/ARS y USD/USDT;
  - CriptoYa (USDT y USDC contra ARS y USD, dólares) y dolarapi, ambos indicativos.
- **Errores:** 7 capturas sin bonos de data912. Quedan registrados y no se rellenan.
- **Fotos únicas:** anuncios P2P USDT/USD con medios argentinos, libro USDT/USD de Kraken y Bitstamp, precio del oficial por banco.
- **Histórico:** cierres diarios de argentinadatos (oficial, MEP, CCL, cripto, mayorista), 393 días hábiles desde el 14/04/2025. Es **[INDICATIVO]**: sirve para ver persistencia, no para medir ejecución.
- **Análisis:** `lab/research/fx_circuits.py` (tests en `tests/test_fx_circuits.py`).
  - Usa solo puntas ejecutables con su cantidad. Descarta las puntas cruzadas (bid > ask).
  - Marca como sospechosa cualquier cotización de CriptoYa a más del 3% del precio medio de Binance. Hubo 6 plataformas sospechosas; mexcp2p, por ejemplo, con un bid de 1.800.
- **Limitación general:** es una sola tarde, fuera de la ventana de compra bancaria. Ninguna conclusión es definitiva.

## 2. Precios de referencia observados (mediana, 14/10)

| Concepto | Precio | Evidencia |
|---|---|---|
| Oficial BNA (venta) | 1.535 | [INDICATIVO] dolarapi |
| Mayorista | 1.513 | [INDICATIVO] |
| MEP vía bonos: comprar USD / vender USD | 1.537,5 / 1.537,1 | [OBSERVADO] |
| CCL vía bonos: vender cable | 1.616,2 | [OBSERVADO] |
| USDT/ARS Binance spot: bid / ask | 1.614,8 / 1.614,9 | [OBSERVADO] |
| P2P USDT/ARS: mejor anuncio para comprar / para vender | 1.609,0 / 1.608,2 | [OBSERVADO] |

## 3. Resultados por familia

### 3.1 Dólar MEP

**Circuitos:**
- Ida y vuelta en el mismo bono (AL30): −0,04% bruto de mediana, 0 positivos de 86.
- Cruce entre bonos (comprar USD con el bono X y venderlos con el bono Y, 4 operaciones):

| Escenario | Mediana | Máximo | Positivos |
|---|---|---|---|
| Bruto | −0,03% | +0,20% | 10 de 89 |
| Neto con comisión de broker 0 | −0,07% | +0,15% | 2 de 89 |
| Neto con comisión de broker 0,25% por operación | negativo | negativo | 0 de 89 |

- **Capacidad al mejor precio:** mediana de USD 448.

**Costos:**
- Derecho de mercado de renta fija: 1 pb + IVA [SUPUESTO; no verificado].
- Broker: escenarios de 0 / 0,25% / 0,5% [SUPUESTO].

**Clasificación:** GARANTIZADO solo si las 4 patas se ejecutan a la vez.

**Recomendación: descartar.** El margen ocasional (+0,15%) no cubre costos realistas, y la capacidad es baja.

### 3.2 Dólar CCL

- **Cruce entre bonos C:** bruto con mediana −0,03% y máximo +0,085% antes de costos. Descartar.
- **Canje MEP → CCL:** bruto de **+5,1%** (de +4,7% a +5,5%).
  - **No es ejecutable** para una persona humana sin pasar a cable: transferir USD al exterior bajo la Com. "A" 8417 y luego comprar bonos con liquidación en cable.
  - Esa compra está **prohibida por 90 días** por la declaración jurada de la Com. "A" 8417 [SECUNDARIA: Allende].
  - El canje es el precio de esa restricción, no una ineficiencia.
- **Entre emisoras (acciones):** ver `INVESTIGACION_PROFUNDA_2026-10-13.md` e `INFORME_MUESTRA_PARCIAL_2026-10-14.md`. Sin edge con los costos supuestos.

**Recomendación:** descartar el canje como arbitraje y seguir CCL entre emisoras con la recolección en curso (`ccl-20261015`).

### 3.3 Dólar cripto (USDT/USDC contra ARS)

| Circuito | Resultado | Clasificación |
|---|---|---|
| Ida y vuelta en Binance spot | −0,21% | — |
| Bitso → Binance / Binance → Bitso | −0,66% / −0,76% (comisión taker de Bitso 0,6% [OFICIAL: API]) | — |
| **Comprar en P2P → vender en Binance spot** | **+0,22% a +0,37% neto de la comisión spot, en 96 de 96 capturas** | CONDICIONADO |
| Comprar en Binance → vender en P2P | −0,51% | — |
| Ida y vuelta P2P | −0,04% (20 de 96 positivos, máximo +0,08%) | — |
| Cruce entre plataformas según CriptoYa | +0,14% de mediana, solo entre plataformas P2P | INDICATIVO |

Detalle de "comprar en P2P → vender en Binance spot":
- **Por qué sería condicionado:** los 20 anuncios de la primera página para comprar USDT estaban por debajo del bid de Binance spot.
- **Capacidad:** de 2.500 a 12.000 USDT (suma de los anuncios con margen).
- **Riesgos:**
  - todos los anuncios son de **particulares** (no comerciantes) y con mínimos de $10.000 a $200.000;
  - pagos en pesos a terceros con riesgo de fraude (triangulación), contracargos y bloqueos bancarios;
  - comisión P2P para el tomador y tiempo de liberación no verificados.

**Recomendación:** P2P → spot es la única señal cripto local con margen positivo persistente en la muestra. **Merece laboratorio de observación**: frecuencia por hora y por día, cupo real, tiempos de liberación, distinción entre comerciante y particular, y riesgo de contraparte. No merece capital.

### 3.4 Diferencias entre plataformas

- Fuera de P2P → spot, los cruces son negativos después de comisiones.
- Las diferencias aparentes de CriptoYa entre plataformas P2P (+0,14%) no son ejecutables sin abrir cuenta, cumplir límites y asumir el riesgo de contraparte de cada P2P.

**Recomendación:** incluir solo Binance (spot y P2P) y Bitso, que tienen libros públicos verificables. El resto, como referencia.

### 3.5 Circuitos combinados

| Circuito | Resultado | Clasificación |
|---|---|---|
| MEP → USD local → USDT en plataforma local → ARS | −0,5% a −2,0%. Las plataformas locales venden USDT a 1,055 a 1,070 USD | NO VIABLE |
| ARS → USDT → USDT por USD local → vender MEP | −0,3% a −5% | NO VIABLE |
| MEP o oficial → USD a cuenta propia en el exterior → USDT a ~0,999 → ARS | USD 1.000: −12,7%. USD 10.000: **+2,9% (MEP) / +3,1% (oficial)**. USD 50.000: **+4,0% / +4,2%** | ESPECULATIVO-CONDICIONADO |
| xapo, astropay, banexcoin, x4t en CriptoYa USDT/USD | +3% a +5% | NO VERIFICABLE |

Detalle de la ruta por el exterior:
- **Cuánto tarda:** de 1 a 5 días hábiles.
- **Riesgo cambiario:** en 3 días hábiles el USDT/ARS se movió entre −1,7% y +2,8% (p5/p95), con un mínimo de −9,5%.
- **Costos:** transferencia según el tarifario oficial de Galicia (29/08/2025). Comisión de Kraken y retiro de USDT supuestos.
- **Legalidad:** la combinación con criptoactivos sigue pendiente.

Sobre las plataformas que dan +3% a +5%: el dólar que reciben es **del exterior**, así que en la práctica equivalen a la ruta por el exterior.

**Recomendación:** la ruta por el exterior es la única familia con margen material. **Ampliar datos** (costos reales de transferencia, cobertura cambiaria, consulta legal) antes de simularla. El resto, descartar.

### 3.6 Dólar oficial

- **Oficial → MEP o CCL:** **prohibido** por la declaración jurada de 90 días [OFICIAL: formulario de Banco Provincia del 06/10/2026]. Excluido.
- **Oficial → USDT local:** ver el informe prioritario. NO DEMOSTRADO: equilibrio en 1,051 USD/USDT contra 1,049 a 1,059 observados.
- **Oficial → exterior → USDT:** ver 3.5.

Persistencia histórica (indicativa, días hábiles desde el 14/04/2025):
- cripto / oficial: mediana +3,2%;
- canje CCL / MEP: mediana +2,5%, de +3,7% a +4,4% en septiembre y octubre de 2026;
- MEP / oficial: mediana ~0%.

## 4. Qué pasa al laboratorio y qué se descarta

| Familia | Recomendación |
|---|---|
| MEP entre bonos | Descartar |
| CCL entre bonos y canje | Descartar el canje como arbitraje; el CCL entre emisoras sigue en observación |
| Cripto: P2P → Binance spot | **Laboratorio de observación** (frecuencia, cupo, contraparte) |
| Cripto entre plataformas | Descartar, salvo P2P → spot |
| MEP / oficial → USDT local | NO VIABLE con los precios de hoy; observar la captura del 15/10 |
| MEP / oficial → exterior → USDT | Ampliar datos: costos reales, cobertura y legalidad. Es especulativo de varios días, no un arbitraje |
| Oficial → MEP / CCL | Excluido por norma |

## 5. Datos faltantes

1. Texto ordenado "Exterior y Cambios" vigente (alcance de la Com. "A" 7552 sobre criptoactivos).
2. Derecho de mercado de renta fija de BYMA y comisiones reales de broker para MEP.
3. Demora de data912 respecto del mercado.
4. Comisión P2P para el tomador y tiempos de liberación de Binance.
5. Costos reales de transferencia al exterior desde los bancos del usuario.
6. Muestra de varios días hábiles dentro de la ventana bancaria. Empieza el 15/10.

## Fuentes (consultadas el 14/10/2026)

Las mismas del informe prioritario, más:
- Canje CCL/MEP: https://www.iprofesional.com/finanzas/447304-brecha-entre-dolar-mep-y-ccl-no-afloja-que-pasa-en-el-mercado
- Parking, RG CNV 1062/2025: https://aduananews.com/la-cnv-flexibiliza-operaciones-en-dolares-para-personas-humanas/
- Com. "A" 7506 y criptoactivos: https://www.forbesargentina.com/money/nuevo-golpe-bcra-industria-crypto-impiden-ofrecer-estos-activos-proveedores-servicios-pago-n33327/amp
- Com. "A" 7552: https://criptonoticias.com/finanzas/si-compras-bitcoin-argentina-no-podes-comprar-dolares-90-dias
- APIs: data912 (`/live/arg_bonds`), Binance (`/api/v3/depth` y P2P), Bitso (`/v3/order_book`, `/v3/available_books`), Kraken (`/0/public/Depth`), Bitstamp, CriptoYa, dolarapi, argentinadatos.
