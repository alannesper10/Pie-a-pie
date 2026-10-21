# STRIKE_INCONSISTENCY — capital bloqueado y regla de rentabilidad mínima (21/10/2026)

Solo paper. Este informe no cierra ni modifica ninguna posición: la regla nueva rige
únicamente para entradas nuevas. Fuente: `data/strategies/strike_inconsistency/state.json`
(origin/main, commit del bot) y la API pública de Kalshi (sin credenciales), consultada
el 21/10/2026 a las 15:30 UTC.

## Posiciones abiertas (capital bloqueado US$19,542)

| Par | Contratos | Capital comprometido | Desde (UTC) | Neto esperado (no realizado) | % s/capital | Recupero del capital | Días |
|---|---:|---:|---|---:|---:|---|---:|
| KXUST30YRRATE27-27DEC31 (T2.49 sí / T2.74 no) | 1 | US$0,952 | 18/10 09:20 | US$0,048 | 5,04 % | 02/01/2028 07:05 UTC | 438 |
| KXUST10YRRATE27-27DEC31 (T1.99 sí / T3.99 no) | 10 | US$9,690 | 18/10 10:53 | US$0,310 | 3,20 % | 02/01/2028 07:05 UTC | 438 |
| USCLIMATE (2025 sí / 2030 no) | 9 | US$8,900 | 20/10 21:31 | US$0,100 | 1,12 % | 31/12/2035 16:00 UTC | 3.358 |
| **Total** | | **US$19,542** | | **US$0,458** | | | |

Capital comprometido = costo + comisiones + slippage. P&L realizado: US$0,00 (no hubo cierres).

### Condiciones de recupero

- **Bonos del Tesoro (30Y y 10Y).** Resuelven con el rendimiento par del 31/12/2027.
  - Fecha esperada: 31/12/2027 20:30 UTC.
  - Fecha límite contractual: 02/01/2028 06:05 UTC.
  - Liquidación: 1 hora después.
  - El piso de pago del par (US$1 por contrato) recién se cobra cuando liquidan las dos patas.
- **USCLIMATE.** Las dos patas tienen fecha esperada el 31/12/2030, pero las fechas límite difieren:
  - la pata 2025 vence a más tardar el 31/12/2030;
  - la pata 2030 vence a más tardar el **31/12/2035**: el dato de emisiones de 2030 se publica años después.
  - Cierre anticipado previsto: "si el evento ocurre, el mercado cierra a las 10 AM siguientes".
  - Plazo defendible del capital: hasta 2035.
- **Salida anticipada: no viable hoy.** Vender las dos patas al mejor bid (solo tope del libro, antes de comisiones) devolvería:
  - 30Y: US$0,56 contra US$0,95 comprometidos;
  - 10Y: US$3,70 contra US$9,69;
  - USCLIMATE: US$8,08 contra US$8,90.
  - En los tres casos salir hoy da pérdida. El capital vuelve al resolver.

### Referencia (no se aplica a estas posiciones)

Con la tabla nueva las tres quedarían en el tramo de más de 35 días (mínimo 20 %).
Las tres están por debajo (5,04 %, 3,20 % y 1,12 %), así que hoy serían **caso B** (pedirían autorización).
Se mantienen tal como están.

## Regla para entradas nuevas

| Plazo de recupero | Rentabilidad neta mínima |
|---|---|
| Hasta 7 días inclusive | mayor que 0 % |
| Más de 7 y hasta 14 | 8 % |
| Más de 14 y hasta 21 | 10 % |
| Más de 21 y hasta 28 | 12 % |
| Más de 28 y hasta 35 | 15 % |
| Más de 35 días | 20 % |

**Plazo de recupero.** Por pata, se toma la fecha límite contractual de resolución (`latest_expiration_time`) más el tiempo de liquidación (`settlement_timer_seconds`). Después se usa el máximo entre las patas.
- La salida anticipada no acorta el plazo, porque no hay evidencia de que se pueda ejecutar sin perder el neto.
- Si falta algún dato, si una pata no está abierta o si la fecha límite ya pasó sin liquidar, el plazo es `PLAZO_NO_VERIFICABLE` (caso D).

**Casos.**
- **A.** Cumple el mínimo: se abre sola.
- **B.** Está debajo del mínimo: se pide autorización.
- **C.** No es ejecutable (caja, liquidez ya tomada, tope por par, ledger): se registra y se avisa una sola vez.
- **D.** El plazo no es verificable: se pide autorización.

**Autorizar.** Se agrega el id de la solicitud en `config/authorizations.json`.
- Cada id vale para una sola entrada y nunca por más contratos que los solicitados.
- Un cambio material invalida la solicitud: 1 centavo en cualquier pata, 0,25 pp de rentabilidad, cambio de tramo de plazo, ±25 % de contratos o cambio de caso. El bot genera entonces una solicitud nueva.
