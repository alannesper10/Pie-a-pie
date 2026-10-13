"""Módulos de estrategia del laboratorio. Cada uno implementa:

  evaluate(snap, ctx) -> List[Opportunity]   detección + estimación (paralelo)
  execute(opp, snap, ctx)                     simulación de ejecución (orden fijo,
                                              reclama liquidez en el registro)
"""
