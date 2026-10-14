# Dólar oficial → USDT/USDC → ARS: investigación (14/10/2026)

Investigación, no implementación. No se hicieron operaciones, no se movieron
fondos ni se usaron credenciales. El ejecutor, el ledger, las dos posiciones de
Kalshi y los datos de HORUS no se tocaron.

Clases de evidencia usadas en todo el informe:
- **[OFICIAL]** fuente oficial o documento de la entidad.
- **[SECUNDARIA]** prensa o blogs; requiere confirmación.
- **[OBSERVADO]** precio capturado de una API pública.
- **[SUPUESTO]** parámetro del modelo.
- **[SIMULADO]** resultado del simulador.
- **[REAL]** operación real. Hoy no existe ninguna.

## 1. Resumen ejecutivo

**La brecha de ~4,65% entre el oficial y el USDT no es capturable** con las rutas locales observadas. Se calculó comparando el precio de venta de USDT por pesos con el dólar oficial. Para que exista ganancia, el dólar bancario comprado al oficial tiene que convertirse en USDT. Esa conversión cuesta casi exactamente la brecha.

- **Precio de equilibrio:** con el oficial a $1.535 y la venta de USDT en Binance spot a ~$1.614,8 (neto de comisión), se puede pagar como máximo **1,051 USD por USDT** sin perder [SIMULADO].
- **Lo que cuesta hoy convertir dólares bancarios argentinos en USDT** [OBSERVADO]:
  - P2P de Binance, anuncios con medios de pago argentinos: **1,049 a 1,059 USD/USDT**.
  - Plataformas locales que reciben USD (cotización indicativa de CriptoYa): **1,055 a 1,070**.
- **Resultado simulado de la mejor ruta** (Banco Nación → P2P USD → Binance spot):

| Capital | Neto |
|---|---|
| $500.000 a $1.500.000 | +0,14% a +0,23% |
| $150.000 | −0,57% |
| $5.000.000 o más | −0,3% a −0,7% |

- La ganancia de los montos medianos depende de **un solo anuncio**: un particular (no un comerciante) a 1,049, con límite de USD 150 a 1.200.
- Ese anuncio se observó **en una sola captura** de los anuncios en USD (14/10, ~15:55).
- No cubre costos no verificados (comisión P2P, impuestos, transferencias). La transferencia en USD a un tercero dentro de los 15 minutos que da el anuncio tampoco está verificada.

**Conclusión: NO DEMOSTRADO** para la ruta A y **NO VIABLE** para las demás rutas locales con los precios de hoy.

**Única familia con margen grande:** sacar los USD a una cuenta propia en el exterior y comprar allí USDT a ~1,00. Da +3,0% a +4,2% simulado con USD 10.000 o más. Tiene tres problemas:
- es un ciclo de varios días, con riesgo cambiario: en 3 días hábiles el USDT/ARS se movió entre −1,7% y +2,8% (p5/p95);
- la legalidad de la combinación con criptoactivos no está confirmada;
- varios costos son supuestos.

Queda **NO DEMOSTRADO**, como estrategia de varios días y no como arbitraje.

## 2. Mapa de rutas

| Ruta | Pasos | Estado |
|---|---|---|
| **A** | BNA: ARS→USD (10–15 h, días hábiles) → transferir USD al vendedor P2P → USDT en Binance → vender en spot o P2P → ARS | NO DEMOSTRADO |
| **B** | Naranja X: ARS→USD → transferir USD al vendedor P2P (medio "NaranjaX") → USDT → ARS | NO VIABLE (precio) + plazo de transferencia |
| **C** | Naranja X → BNA → P2P/plataforma | Igual que A con un paso más. NO VIABLE salvo que A lo sea |
| **D** | Mercado Pago, USD ya disponibles → USDT | NO VIABLE: MP solo transfiere USD a cuentas propias [SECUNDARIA], y el pago P2P es a un tercero |
| **E** | BNA → plataforma local que reciba USD (Fiwind, Belo, Decrypto, Letsbit, Ripio, SatoshiTango, TiendaCrypto) → USDT → ARS | NO VIABLE: pagan 1,055 a 1,070 USD/USDT |
| **F** | BNA (u otro banco) → transferencia a cuenta propia en el exterior (Com. "A" 8417) → USDT a ~0,999 en un exchange del exterior → enviar USDT a Binance → ARS | NO DEMOSTRADO: varios días, legalidad cripto pendiente, costos parcialmente supuestos |
| **G** | Oficial → MEP o CCL (vender los USD por bonos) | PROHIBIDO por la declaración jurada de 90 días [OFICIAL]. Excluida |

## 3. Normativa y condiciones (consultado el 14/10/2026)

| Tema | Hallazgo | Evidencia |
|---|---|---|
| Compra de USD por personas humanas | Sin cupo mensual desde la Com. "A" 8226 (14/04/2025) | [SECUNDARIA] EconoInfo, La Nación |
| Percepción del 30% sobre la compra para atesoramiento | Eliminada por la RG ARCA 5672/2025 (14/04/2025). Sigue para consumos en el exterior | [SECUNDARIA] CPCE Córdoba, Los Andes |
| Declaración jurada al comprar oficial | "No concertaré … compras de títulos valores con liquidación en moneda extranjera … por los 90 días corridos subsiguientes", con excepciones (suscripción primaria, reinversión de servicios) | **[OFICIAL]** formulario de Banco Provincia, versión del 06/10/2026 |
| Transferencia de USD a cuenta propia en el exterior | Com. "A" 8417 (09/04/2026): registro en el sistema del BCRA y declaración jurada de no comprar títulos pagaderos en USD por 90 días | [SECUNDARIA] estudio Allende, Global66 |
| ¿La restricción de 90 días alcanza a criptoactivos? | El formulario vigente de Banco Provincia **no menciona criptoactivos**. La Com. "A" 7552 (2022) los incluía para ciertos accesos al mercado; **no se pudo confirmar si sigue vigente** ni a quién alcanza | **PENDIENTE**: falta el texto ordenado "Exterior y Cambios" vigente |
| Bancos y criptoactivos | Com. "A" 7506 (2022): las entidades financieras no pueden facilitar operaciones con criptoactivos. Riesgo de bloqueo o cierre de cuenta si se transfiere a un PSAV | [SECUNDARIA] |
| Ganancias por la venta de USDT | Probablemente 15% (moneda extranjera) sobre el resultado; el tratamiento de la diferencia de cambio no está claro | **PENDIENTE**: consultar a un contador |
| Binance | Inscripta como PSAV ante la CNV desde 2024 (el registro no es una licencia) | [SECUNDARIA] Rankia |

**Conclusión legal:** ninguna fuente encontrada prohíbe expresamente comprar oficial y convertir esos USD en USDT, pero tampoco hay una confirmación oficial de que esté permitido. La ruta queda **legalmente NO VERIFICADA**. No se propone eludir la declaración jurada ni ningún control.

## 4. Plataformas

| Plataforma | Recibe USD por transferencia local | USD → USDT | Venta de USDT por ARS | Tiempos | Evidencia |
|---|---|---|---|---|---|
| **Banco Nación (BNA+)** | — (origen) | — | — | Compra 10–15 h, días hábiles. Transferencia de USD a terceros: no verificada (en 2023, tope de USD 12.500 por transferencia) | [SECUNDARIA] MDZ, Naranja X 2023 |
| **Naranja X** | Origen. Compra todos los días salvo de 2 a 4 h | — | — | Transferencia de USD a cuentas argentinas gratis, **"como máximo al final del 2º día hábil"** | [OFICIAL] blog de Naranja X |
| **Mercado Pago** | Origen. USD **solo a cuentas propias** | Cripto en Argentina: sin confirmación | — | Mismo día hábil, hasta 24 h | [SECUNDARIA] |
| **Binance P2P (USD)** | No: el pago va directo al vendedor | Anuncios de 1,049 a 1,059 con medios argentinos; límites de USD 10 a 15.000 por orden; plazo de pago de 15 min | Sí, en spot o P2P | Liberación: no verificada | [OBSERVADO] |
| **Binance spot USDT/ARS** | — | — | Libro con ~81.500 a 281.000 USDT dentro del 1% del mejor bid | Inmediato. Comisión 0,10% [PUBLICADA, no verificada para la cuenta] | [OBSERVADO] |
| **Fiwind** | Sí, solo desde cuentas propias | 1,055 USD/USDT (indicativo) | Sí | No verificados | [SECUNDARIA 2024] + CriptoYa |
| **Belo, Decrypto, Letsbit, Ripio, SatoshiTango, TiendaCrypto** | No confirmado | 1,058 a 1,070 (indicativo) | Sí | No verificados | CriptoYa (agregador) |
| **Kraken (exterior)** | SWIFT en USD: sin comisión por Customers Bank, mínimo USD 100, 1 a 3 días hábiles | Libro USDT/USD a 0,99892 | — | — | [OFICIAL, centro de ayuda] + [OBSERVADO] |
| **Galicia, transferencia al exterior** | — | — | — | 0,3% con mínimo de USD 125, + 0,10% si sale de cuenta en USD, + IVA, + USD 10 de corresponsal | **[OFICIAL]** tarifario del 29/08/2025 |

**Precio del oficial por banco** (CriptoYa, 14/10, solo cotizaciones actualizadas ese día):
- Hipotecario, Bytelime y Pluscambio: 1.529.
- BNA e ICBC: 1.535.
- Supervielle: 1.557,5.

Las cotizaciones con más de 100 días de antigüedad (Columbia, Provincia, Galicia, Santander, Brubank y otros) **se descartaron**. Son datos viejos, no precios.

## 5. Velocidad del ciclo (ruta A)

| Paso | Tiempo | Estado |
|---|---|---|
| Compra de USD en BNA+ | Inmediata, de 10 a 15 h | [SECUNDARIA] |
| Transferencia de USD al vendedor P2P | Debe llegar dentro de los 15 min del anuncio | **NO VERIFICADO**. Si es diferida, como en Naranja X ("hasta el 2º día hábil"), la orden P2P vence |
| Liberación de los USDT por el vendedor | Minutos (habitual) | NO VERIFICADO |
| Venta en Binance spot | Inmediata | [OBSERVADO] libro con profundidad |
| Retiro de ARS | Minutos (habitual) | NO VERIFICADO |

Si todos los pasos se cumplen en minutos, el ciclo entraría en el mismo día, dentro de la ventana de 10 a 15 h. **No hay ningún tiempo comprobado.**

La ruta F tarda de 1 a 5 días hábiles solo por la transferencia SWIFT y la acreditación en el exchange del exterior. Es otra estrategia: tiene capital inmovilizado y exposición al USDT/ARS.

## 6. Simulador

`lab/research/fx_oficial.py` (tests en `tests/test_fx_oficial.py`):
- toma los anuncios P2P en el orden de precio;
- respeta, por anuncio, el mínimo y el máximo por orden, la cantidad disponible y los medios de pago usables;
- recorre el libro spot para vender;
- si no hay liquidez, marca `SIN_LIQUIDEZ_O_LIMITES`; nunca extrapola.

Fórmulas:
- **Rendimiento neto (%)** = (ARS finales − ARS iniciales) / ARS iniciales × 100.
- **Equilibrio (USD por USDT)** = precio medio de venta de USDT × (1 − comisión) / precio del oficial.

Costos y su estado (`COSTS` en el módulo):

| Costo | Valor | Estado |
|---|---|---|
| Comisión de compra en el banco | 0 (el costo está en el precio) | NO VERIFICADO |
| Transferencia local de USD | 0 | PUBLICADO por Naranja X; BNA no verificado |
| Comisión P2P para el tomador | 0 | NO VERIFICADO |
| Comisión spot de Binance | 0,10% | PUBLICADO |
| Retiro de ARS | 0 | NO VERIFICADO |

Para reproducirlo:

```
python -m lab.research.fx_capture lab_data/fx_ar/fx-AAAAMMDD.jsonl 15:05 60 AAAA-MM-DDT10:00
python -m lab.research.fx_oficial_run lab_data/fx_ar/fx-AAAAMMDD.jsonl lab_data/fx_ar/p2p_usdt_usd_AR_AAAAMMDD.json salida.json
```

`fx_oficial_run` toma los anuncios P2P en USD de cada captura y, si no los hay, del archivo de la foto única.

## 7. Resultados

Muestra:
- **ARS:** 96 capturas de 14/10, 15:29–17:04 ART: libro de Binance, anuncios P2P USDT/ARS, CriptoYa, dolarapi y bonos.
- **USD:** **1 sola foto** de los anuncios P2P USDT/USD (~15:55).
- Fuera de la ventana de compra en BNA. El oficial de BNA estuvo fijo en 1.535 toda la tarde [OBSERVADO].

| Ruta | $150.000 | $500.000 | $1.500.000 | $5.000.000 | $15.000.000 | USD/USDT pagado |
|---|---|---|---|---|---|---|
| A (P2P USD → Binance spot) | −0,57% | **+0,18%** | **+0,18%** | −0,30% | −0,63% | 1,049 a 1,057 |
| A' (P2P USD → P2P ARS) | −0,89% | −0,15% | −0,14% | −0,62% | −0,96% | 1,049 a 1,057 |
| B (Naranja X → P2P) | −0,57% | −0,57% | −0,58% | −0,65% | −0,75% | 1,057 a 1,059 |
| D (Mercado Pago) | sin anuncio usable | | | | | — |
| E Fiwind (indicativo) | −0,39% | −0,39% | −0,39% | −0,39% | −0,42% | 1,055 |
| E Belo / Decrypto (indicativo) | −0,64% a −0,67% | | | | | 1,058 |
| E Letsbit / Ripio / SatoshiTango (indicativo) | −1,6% a −1,8% | | | | | 1,068 a 1,070 |
| F exterior desde el oficial, USD 10.000 / 50.000 | — | — | — | +3,09% / +4,21% | — | ~1,00 |

Valores medianos de las 96 capturas [SIMULADO].

Lectura de los resultados:
- En la ruta A, el +0,18% equivale a ~$2.700 sobre $1.500.000.
- Ese resultado sale de un único anuncio de un particular (21 órdenes en el mes) y de una sola foto. **No es evidencia de rentabilidad.**
- Con USD 1.000, la ruta F da −12,6%, porque el mínimo de USD 125 de la transferencia domina el resultado.
- Comparación con conservar los USD: la ruta A dura minutos u horas, así que el efecto cambiario es despreciable. En la ruta F sí importa: en 3 días hábiles el USDT/ARS se movió entre −1,7% (p5) y +2,8% (p95), con un mínimo de −9,5% [OBSERVADO, cierres diarios desde el 14/04/2025]. Eso es del mismo orden que el margen, y el resultado no está garantizado.

**Contexto histórico** (cierres diarios indicativos de argentinadatos, días hábiles desde el 14/04/2025; no son precios ejecutables):
- Cripto (compra) / oficial (venta) − 1: mediana +3,17%, superó el 4% en 117 de 393 días.
- En los últimos 60 días hábiles fue de +2,62% a +4,85%.
- La brecha es persistente. Eso indica que convertir USD bancarios en USDT tiene un costo o un riesgo que el mercado cobra.

## 8. Incertidumbres y datos faltantes

1. Si la restricción de 90 días o la Com. "A" 7552 alcanzan a la compra de criptoactivos con USD del oficial. Hace falta el texto ordenado del BCRA o una consulta formal.
2. Si BNA transfiere USD a terceros de forma inmediata, y con qué límites hoy.
3. Comisión real de Binance P2P para el tomador y tiempos reales de liberación.
4. Cuántos anuncios P2P USD a ≤ 1,051 aparecen por día, y con qué cupo. Se mide con la captura del 15/10.
5. Precio y comisión reales de las plataformas que reciben USD (CriptoYa es indicativo). Plazos de acreditación.
6. Costo real de la transferencia al exterior desde BNA o Naranja X (solo se tiene el tarifario de Galicia). Cuenta en el exterior y comisiones de Kraken para USDT/USD y el retiro.
7. Tratamiento en Ganancias y política de los bancos frente a transferencias a exchanges.

## 9. Próximas pruebas, por valor informativo

1. **Captura del 15/10, de 10:00 a 15:05** (ya programada: `lab_data/fx_ar/fx-20261015.jsonl`). Registra cada minuto los anuncios P2P USDT/USD con medios argentinos, los precios por banco, el libro de Binance y P2P ARS. Mide la frecuencia y el cupo de anuncios a ≤ 1,051 dentro de la ventana de BNA. **Es la prueba que decide la ruta A.**
2. Repetirla durante 5 a 10 días hábiles para tener períodos y una muestra fuera de muestra.
3. Consulta legal o contable sobre la combinación oficial → criptoactivos y sobre Ganancias.
4. Confirmar con BNA los tiempos y límites de transferencia de USD a terceros (por los canales del banco, sin operar).
5. Para la ruta F: obtener las tarifas reales de transferencia al exterior de BNA o Naranja X y de la cuenta de destino, y modelar la cobertura cambiaria (por ejemplo, con futuros de dólar) antes de considerarla.

**Ruta prioritaria para una prueba controlada, solo cuando se cumplan 1 a 3:** la ruta A, con el monto mínimo del anuncio. Todavía no se recomienda ninguna prueba con dinero real.

## Fuentes (consultadas el 14/10/2026)

- Declaración jurada de compra de USD, Banco Provincia (06/10/2026): https://www.bancoprovincia.com.ar/CDN/Get/DDJJ_COMPRA_DOLARES_INDIVIDUOS
- Com. "A" 8417, estudio Allende (14/04/2026): https://allende.com/bancario/el-banco-central-flexibiliza-el-regimen-cambiario-para-exportaciones-transferencias-en-moneda-extranjera-y-pagos-financieros-04-14-2026/
- Com. "A" 8336, restricción cruzada: https://www.cronista.com/finanzas-mercados/nuevo-cepo-que-es-la-restriccion-cruzada-y-como-impacta-en-la-compra-de-dolar-mep-y-ccl/ y https://fecoi.org.ar/el-banco-central-restablece-la-restriccion-cruzada-para-la-compra-de-divisas/
- RG 5672/2025, percepciones: https://web.cpcecba.org.ar/?p=55070
- Tarifario de transferencias internacionales, Galicia (29/08/2025): https://www.galicia.ar/content/dam/galicia/banco-galicia/personas/comisiones-minoristas/Comisiones_Transferencias_internacionales_290825.pdf
- Naranja X, compra y transferencia de USD: https://www.naranjax.com/blog/como-comprar-dolar-oficial-sin-limites-en-la-app-de-naranja-x y https://www.naranjax.com/blog/transferencias-en-dolares-en-la-cuenta-de-naranja-x
- Kraken, depósitos: https://support.kraken.com/hc/en-us/articles/360000381846
- Mercado Pago, USD a cuentas propias: https://www.iproup.com/economia-digital/56467-como-compro-y-transfiero-dolares-con-mercado-pago
- BNA+, horario 10–15 h: https://www.mdzol.com/dinero/el-dolar-abrio-agosto-alza-cuanto-cotiza-segun-el-banco-nacion-n1578427
- APIs públicas: Binance (spot y P2P), Bitso, Kraken, data912, CriptoYa, dolarapi, argentinadatos.
