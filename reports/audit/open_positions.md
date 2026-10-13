# Auditoría de posiciones paper abiertas (kalshi_current)

Generado: 2026-10-13T17:22:46+00:00 · solo lectura (ledger sin cambios)

Caja 81.2360 · bloqueado 18.7640 · control 100 - bloqueado - caja = 0.0

## KXCRITICSPROD-27 — Critics Choice Awards: Best Production Design

- Abierta 2026-10-13T01:58:13+00:00 (commit f0e01ab), 10 contratos, 16 patas YES
- Inversión: costo 9.1 + comisiones 0.5800000000000001 + slippage 0.160 = **9.840**
- Cobertura al abrir: CATCH_ALL_MARKET → hoy: **NOT_PROVEN** (lista de opciones abierta o no demostrada: un resultado no listado haría que todas las patas YES paguen 0)
- Evidencia de lista abierta: 16 patas (ej. ['KXCRITICSPROD-27-ODY: The market will close and expire early following nominations being released (if The Odyssey is not nominated) or the awards show.'])

| Escenario | Pago | Neto |
|---|---|---|
| gana una de las patas listadas | 10.0 | +0.160 |
| gana una opción no listada / ninguna listada | 0.0 | -9.840 |

- Pérdida máxima: **9.840 USD** · ganancia máxima +0.160
- Valor de salida hoy (vender al bid): 4.715 → P&L a mercado **-5.125**

| Pata | Ask al abrir | Tam. | Comisión | Estado hoy | Bid hoy |
|---|---|---|---|---|---|
| ODY The Odyssey | 0.42 | 25.00 | 0.18 | active  | 0.21 |
| PRO Project Hail Mary | 0.04 | 52.00 | 0.03 | active  | 0.03 |
| DUN Dune: Part Three | 0.19 | 55.00 | 0.11 | active  | 0.15 |
| LAB La Bola Negra | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| WER Werwulf | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| FUR The Further Mis-Adventures of Cliff Booth | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| WUT Wuthering Heights | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| SEN Sense and Sensibility | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| WIL Wildwood | 0.03 | 2482.77 | 0.03 | active  | 0.01 |
| BAC Backrooms | 0.02 | 54.00 | 0.02 | active  | 0.01 |
| FAT Fatherland | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| WILD Wild Horse Nine | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| INK Ink | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| DEV The Devil Wears Prada 2 | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| DIG Digger | 0.02 | 53.00 | 0.02 | active  | 0.01 |
| TIE Tie | 0.02 | 53.00 | 0.02 | active  | 0.01 |

**Recomendación:** Reclasificar como ESPECULATIVA (cobertura NOT_PROVEN): gana +0.160 si gana una película listada y pierde 9.840 si gana una no listada. NO cerrar automáticamente: cerrarla hoy en paper realizaría -5.125 USD (vender las 16 patas al bid, todas vendibles). Opción recomendada: mantenerla abierta SIN tocar el ledger, marcada en reports/audit como posición especulativa abierta por error y EXCLUIDA de las métricas de arbitraje; registrar su resultado real al liquidarse como evidencia del riesgo. Cerrarla (y cómo registrarlo) requiere tu decisión explícita.

## KXCRITICSCOM-27 — Critics Choice Awards: Best Comedy

- Abierta 2026-10-13T08:41:54+00:00 (commit 9059fdc), 9 contratos, 16 patas YES
- Inversión: costo 8.18 + comisiones 0.6 + slippage 0.144 = **8.924**
- Cobertura al abrir: CATCH_ALL_MARKET → hoy: **NOT_PROVEN** (lista de opciones abierta o no demostrada: un resultado no listado haría que todas las patas YES paguen 0)
- Evidencia de lista abierta: 16 patas (ej. ['KXCRITICSCOM-27-DEB: The market will close and expire early following nominations being released (if The Debut is not nominated) or the awards show.'])

| Escenario | Pago | Neto |
|---|---|---|
| gana una de las patas listadas | 9.0 | +0.076 |
| gana una opción no listada / ninguna listada | 0.0 | -8.924 |

- Pérdida máxima: **8.924 USD** · ganancia máxima +0.076
- Valor de salida hoy (vender al bid): 4.920 → P&L a mercado **-4.004**

| Pata | Ask al abrir | Tam. | Comisión | Estado hoy | Bid hoy |
|---|---|---|---|---|---|
| DEB The Debut | 0.19 | 132.45 | 0.10 | active  | 0.14 |
| WIL Wild Horse Nine | 0.06 | 828.89 | 0.04 | active  | 0.05 |
| INV The Invite | 0.20 | 15.00 | 0.11 | active  | 0.16 |
| CLU Club Kid | 0.15 | 1.00 | 0.09 | active  | 0.13 |
| FUR The Further Mis-Adventures of Cliff Booth | 0.02 | 1437.45 | 0.02 | active  | 0.01 |
| DIG Digger | 0.02 | 3436.45 | 0.02 | active  | 0.01 |
| ILO I Love Boosters | 0.02 | 38.45 | 0.02 | active  | 0.01 |
| DEV The Devil Wears Prada 2 | 0.02 | 882.45 | 0.02 | active  | 0.01 |
| COY Coyote vs. Acme | 0.09 | 18.79 | 0.06 | active  | 0.02 |
| DRA The Drama | 0.02 | 49.45 | 0.02 | active  | 0.01 |
| SHE The Sheep Detectives | 0.03 | 33.03 | 0.02 | active  | 0.01 |
| GAL The Gallerist | 0.01 | 2424.87 | 0.01 | active  | None |
| FOC Focker-in-Law | 0.01 | 3530.99 | 0.01 | active  | None |
| TEE Teenage Sex and Death at Camp Miasma | 0.02 | 1596.45 | 0.02 | active  | 0.01 |
| PRO Project Hail Mary | 0.02 | 49.45 | 0.02 | active  | 0.01 |
| TIE Tie | 0.02 | 109.77 | 0.02 | active  | 0.01 |

**Recomendación:** Reclasificar como ESPECULATIVA (cobertura NOT_PROVEN): gana +0.076 si gana una película listada y pierde 8.924 si gana una no listada. NO cerrar automáticamente: cerrarla hoy en paper realizaría -4.004 USD (vender las 16 patas al bid, NO todas vendibles por profundidad). Opción recomendada: mantenerla abierta SIN tocar el ledger, marcada en reports/audit como posición especulativa abierta por error y EXCLUIDA de las métricas de arbitraje; registrar su resultado real al liquidarse como evidencia del riesgo. Cerrarla (y cómo registrarlo) requiere tu decisión explícita.

