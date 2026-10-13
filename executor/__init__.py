"""Ejecutor de órdenes de HORUS (modo 2 de Pie a Pie). SOLO paper.

No envía órdenes reales, no usa claves de trading y no escribe en data/.
Estado en lab_data/executor.sqlite (fuera de git); buzón en executor_io/.
Contrato: docs/ARQUITECTURA.md §3 (horus.order/v1, pieapie.report/v1).
"""

PAPER_ONLY = True
