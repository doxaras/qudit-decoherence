"""Size-scaling under steeper dephasing exponents (R5-R2-M8).

Every Sec.~V scaling result runs at the calibrated exponent
max(j,k)^1.1; Table VI shows the ladder verdicts move under steeper
readings (Goss's supplement implies ~2, Peterer 1.6-2.6), but only at
demo size. This sweep repeats the calibrated-ladder scaling family at
dephase exponents 1.6 and 2.0 over a reduced size range (the demo-
adjacent sizes where all three bases are cheap), Sec.~V conventions:
N=21, a=2, uniform cost, s=0.003, weighted fits in bits.

Run: python3 scaling_exponent_sweep.py [n_traj]
Writes results/scaling_exponent_sweep.json
"""

import json
import math
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from scaling_claims import fit
from trajectories import shor_trajectories

N, A = 21, 2
S = 0.003
SIZES = {2: [6, 8, 10], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
EXPONENTS = [1.6, 2.0]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 400
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def one(args):
    d, m, deph = args
    seed = zlib.crc32(f"expsweep,{d},{m},{deph}".encode()) % (2 ** 32)
    t0 = time.time()
    base = shor_trajectories(d, m, a=A, N=N)
    res = shor_trajectories(d, m, "transmon_cal", S, n_traj=N_TRAJ,
                            seed=seed, a=A, N=N, damping_exponent=0.7,
                            dephase_exponent=deph)
    span = base["success"] - res["floor"]
    out = {"d": d, "m": m, "bits": m * math.log2(d), "dephase": deph,
           "signal": (res["success"] - res["floor"]) / span,
           "err": res["stderr"] / span, "seed": seed,
           "elapsed_s": round(time.time() - t0, 1)}
    print(f"  d={d} m={m} exp={deph}: signal={out['signal']:.3f}"
          f"±{out['err']:.3f} ({out['elapsed_s']}s)", flush=True)
    return out


def main():
    os.makedirs(RESULTS, exist_ok=True)
    jobs = [(d, m, e) for e in EXPONENTS for d in SIZES for m in SIZES[d]]
    print(f"{len(jobs)} trajectory points, {N_TRAJ} traj each", flush=True)
    pts = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        pts = list(ex.map(one, jobs))

    out = {"N": N, "a": A, "strength": S, "n_traj": N_TRAJ,
           "cost_model": "uniform", "points": pts, "fits": {}}
    for e in EXPONENTS:
        out["fits"][str(e)] = {}
        print(f"-- exponent {e} --", flush=True)
        for d in SIZES:
            fam = [p for p in pts if p["d"] == d and p["dephase"] == e]
            f = fit(fam, weighted=True)
            out["fits"][str(e)][str(d)] = f
            print(f"   d={d}: slope {f['slope']:+.4f}+-{f['slope_se']:.4f}"
                  f"/bit (R^2={f['r2']:.2f}, n={f['n']})", flush=True)

    path = os.path.join(RESULTS, "scaling_exponent_sweep.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}", flush=True)


if __name__ == "__main__":
    main()
