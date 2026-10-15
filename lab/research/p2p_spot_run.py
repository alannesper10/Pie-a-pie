"""Corre la grilla de escenarios de p2p_spot sobre capturas guardadas (solo investigación).

Uso: python -m lab.research.p2p_spot_run salida.json captura1.jsonl [captura2.jsonl ...]
Cada archivo se simula por separado (un día = una sesión; los ciclos no
cruzan de un día al otro) y los resultados se informan por día y sumados.
"""
import itertools
import json
import sys

from lab.research import p2p_spot as ps


def load(path, until=None):
    out = []
    for line in open(path, encoding="utf-8"):
        if line.strip():
            s = json.loads(line)
            if until is None or s["ts"] < until:
                out.append(s)
    return out


GRID = {
    "counterparty": ["merchant", "solid", "any"],
    "capital_ars": [100_000, 500_000, 2_000_000, 5_000_000],
    "ars_withdraw_pct": [0.0, 0.001, 0.0025, 0.005, 0.01],
    "withdraw_s": [15 * 60, 24 * 3600],
    "spot_taker": [ps.SPOT_TAKER_VERIFIED, ps.SPOT_TAKER_BNB],
    "p2p_taker": [0.0, 0.001],
    "release_s": [97, 295],          # p50 y p90 observados en comerciantes
}


def main():
    out_path, files = sys.argv[1], sys.argv[2:]
    days = {f: load(f) for f in files}
    hours = {f: (ps._ts(d[-1]["ts"]) - ps._ts(d[0]["ts"])).total_seconds() / 3600 for f, d in days.items()}
    results = []
    keys = list(GRID)
    for combo in itertools.product(*GRID.values()):
        g = dict(zip(keys, combo))
        pol = ps.Policy(capital_ars=g["capital_ars"], counterparty=g["counterparty"], release_s=g["release_s"],
                        min_edge=0.0005)
        costs = ps.Costs(p2p_taker=g["p2p_taker"], spot_taker=g["spot_taker"],
                         ars_withdraw_pct=g["ars_withdraw_pct"], withdraw_s=g["withdraw_s"])
        per_day, all_cycles = {}, []
        for f, d in days.items():
            c = ps.run(d, pol, costs)
            per_day[f] = ps.summarize(c, hours[f])
            all_cycles += c
        results.append({**g, "per_day": per_day,
                        "total": ps.summarize(all_cycles, sum(hours.values()))})
    json.dump({"files": files, "hours": hours, "grid": GRID, "results": results},
              open(out_path, "w", encoding="utf-8"), indent=1, default=str)
    print(f"{len(results)} escenarios; horas observadas {hours}")


if __name__ == "__main__":
    main()
