"""Is the Shor result a number-theoretic artifact of the chosen instance?

Phase estimation concentrates on the phases s/r. If r divides the control
dimension D = d^m exactly, those phases sit ON grid points and the peaks are
perfectly sharp; otherwise they smear across neighbouring outcomes and are
more fragile under noise.

For N = 15 the multiplicative group is Z2 x Z4, so EVERY order is a power of
two (r = 1, 2, 4). With D = 2^m the peaks are always exactly representable
for qubits, and never for qutrits or ququints. Our entire Shor comparison
may therefore be confounded: base 2 gets a free structural advantage that
has nothing to do with decoherence.

This tests the hypothesis with instances whose order is NOT a power of two:

    N = 21, a = 4  -> r = 3   exactly representable in base 3 only
    N = 21, a = 2  -> r = 6   representable in NO base (6 divides no d^m)
    N = 15, a = 7  -> r = 4   the original, base 2 favoured

Prediction if the confound is real: the winner tracks which base can
represent s/r exactly -- qutrits should win at r = 3, and the r = 6 case
should be a fair fight.

Writes results/order_confound.json. Run: python3 order_confound.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import multiplicative_order, recovered_order, shor_config, shor_run

INSTANCES = [(15, 7), (21, 4), (21, 2)]
BASES = [2, 3, 5]
NOISE = ["transmon_cal", "depolarizing"]
STRENGTHS = [0.002, 0.005]


def uniform_floor(d, a, N):
    m, _ = shor_config(d, N)
    D = d ** m
    r = multiplicative_order(a, N)
    return sum(recovered_order(y, D, a, N) == r for y in range(D)) / D


def one(args):
    d, a, N, nm, s = args
    t0 = time.time()
    r = shor_run(d, nm, s, a=a, N=N)
    return dict(d=d, a=a, N=N, noise=nm, strength=s,
                success=float(r["success"]), r_true=r["r_true"],
                D=r["D"], n_qudits=r["n_qudits"],
                elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    meta = {}
    for N, a in INSTANCES:
        for d in BASES:
            m, w = shor_config(d, N)
            D = d ** m
            r = multiplicative_order(a, N)
            meta[f"{N},{a},{d}"] = {
                "D": D, "r": r, "exact_grid": D % r == 0,
                "floor": uniform_floor(d, a, N),
                "baseline": shor_run(d, a=a, N=N)["success"],
                "m": m, "w": w}
            mm = meta[f"{N},{a},{d}"]
            print(f"N={N} a={a} d={d}: r={r} D={D} "
                  f"r|D={mm['exact_grid']} floor={mm['floor']:.3f} "
                  f"noiseless={mm['baseline']:.3f}", flush=True)

    jobs = [(d, a, N, nm, s) for N, a in INSTANCES for nm in NOISE
            for s in STRENGTHS for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one, jobs):
            mm = meta[f"{r['N']},{r['a']},{r['d']}"]
            r["signal"] = ((r["success"] - mm["floor"])
                           / (mm["baseline"] - mm["floor"]))
            r["exact_grid"] = mm["exact_grid"]
            results.append(r)
            print(f"N={r['N']} a={r['a']} r={r['r_true']} {r['noise']:13s} "
                  f"s={r['strength']:<6g} d={r['d']} "
                  f"exact_grid={str(r['exact_grid']):5s} "
                  f"signal={r['signal']:6.3f} ({r['elapsed_s']}s)", flush=True)

    with open("results/order_confound.json", "w") as f:
        json.dump({"instances": INSTANCES, "meta": meta, "runs": results}, f,
                  indent=1)
    print("\nwrote results/order_confound.json")


if __name__ == "__main__":
    main()
