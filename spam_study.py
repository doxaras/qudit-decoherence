"""Does the qudit advantage survive d-dependent readout error?

Pre-publication hardening task #6. Every result so far assumes noiseless
state preparation and measurement. That flatters qudits twice over: a
d-level readout has to resolve d pointer states instead of 2, and the
higher levels are exactly the ones that are hardest to distinguish
(crowded dispersive shifts, more decay during the measurement window).

We charge one readout channel at the end of the circuit, applied to every
control qudit, with the misread rate of |k> growing as (1+k)^1 -- roughly
1 : 2 : 3 for a qutrit, matching transmon qutrit readout data. So a
ququint's worst level is charged 5x the qubit's |0> rate, and the qubit's
own readout is charged too (no free pass).

Note the qudit is penalized twice by construction: per-level rates grow
with d, AND a base-d register at matched precision has fewer qudits but
each carries more of the answer, so a single misread corrupts log2(d) bits
instead of 1.

Writes results/spam.json. Run: python3 spam_study.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from plots import uniform_floor
from qpe_generic import good_phase_mask, qpe_run_exact
from qudit_shor import shor_run

N, A = 21, 2
EPS = [0.0, 0.005, 0.01, 0.02, 0.04]
NOISE = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
BASES = [2, 3, 5]
QPE_M = {2: 6, 3: 4, 5: 3}


def one(args):
    algo, nm, s, d, eps = args
    t0 = time.time()
    if algo == "shor":
        r = shor_run(d, nm, s, a=A, N=N, readout_eps=eps)
    else:
        r = qpe_run_exact(d, QPE_M[d], nm, s, readout_eps=eps)
    return dict(algo=algo, noise=nm, strength=s, d=d, eps=eps,
                success=float(r["success"]),
                elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    # floors and baselines must carry the SAME readout error, otherwise the
    # correction would credit qudits for damage the metric already removed
    floors, baselines = {}, {}
    for d in BASES:
        floors[("shor", d)] = uniform_floor(d, A, N)
        floors[("qpe", d)] = float(good_phase_mask(d ** QPE_M[d]).mean())
        for eps in EPS:
            baselines[("shor", d, eps)] = float(
                shor_run(d, a=A, N=N, readout_eps=eps)["success"])
            baselines[("qpe", d, eps)] = float(
                qpe_run_exact(d, QPE_M[d], readout_eps=eps)["success"])
    print("baselines computed", flush=True)

    jobs = [(algo, nm, s, d, eps) for algo in ("shor", "qpe")
            for nm, s in NOISE for d in BASES for eps in EPS]
    runs = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(one, jobs):
            fl = floors[(r["algo"], r["d"])]
            bs = baselines[(r["algo"], r["d"], r["eps"])]
            r["signal"] = (r["success"] - fl) / (bs - fl)
            runs.append(r)
            print(f"{r['algo']:5s} {r['noise']:13s} d={r['d']} "
                  f"eps={r['eps']:<6g} success={r['success']:.4f} "
                  f"signal={r['signal']:6.3f} ({r['elapsed_s']}s)", flush=True)

    with open("results/spam.json", "w") as f:
        json.dump({"N": N, "a": A, "eps": EPS, "noise": NOISE,
                   "qpe_m": QPE_M,
                   "floors": {f"{k[0]},{k[1]}": v for k, v in floors.items()},
                   "baselines": {f"{k[0]},{k[1]},{k[2]}": v
                                 for k, v in baselines.items()},
                   "runs": runs}, f, indent=1)
    print("\nwrote results/spam.json")


if __name__ == "__main__":
    main()
