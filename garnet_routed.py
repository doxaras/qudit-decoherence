"""Predicted bands for the Garnet tasks from their routed circuits.

Round-4 referee point (R2 Q6): Table VII carries no predicted band for
the IQM Garnet lattice because server-side SWAP routing makes the
depth compiler-dependent -- so "fails by plain decoherence" rested on
the work-qubit populations alone. But the routed program IS in the
Braket task metadata; results/garnet_compiled.json commits it
verbatim (m = 5: 47 CZ / 72 prx on 6 qubits; m = 7: 104 CZ / 159 prx
on 8 qubits, against 15 and 28 entangling gates pre-routing).

This parses the routed OpenQASM (prx / cz on physical qubits, with the
compiler's measurement mapping), verifies the parse by reproducing the
analytic noiseless success, then runs the same exact-DM depolarizing
prediction used for the IonQ rows. Two charging conventions bracket
the single-qubit contribution: `paper` charges every gate one layer,
`cz_only` charges only the entanglers. The work-qubit |1> population
is predicted alongside, since that is the observable the paper's
failure diagnosis leaned on.

Writes results/garnet_routed.json. Run: python3 garnet_routed.py
"""

import json
import math
import os
import re

import numpy as np

from braket_qpe_anchor import success_mask
from qudit_shor import channels_by_cost, control_probs, run_circuit

STRENGTHS = [0.004, 0.007, 0.010]
CONVENTIONS = ["paper", "cz_only"]
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def parse_program(prog: str):
    """Routed gate list [(phys_qubits, U, kind)] and the measure map."""
    gates, measures = [], {}
    for line in prog.splitlines():
        line = line.strip()
        mm = re.match(r"c\[(\d+)\] = measure \$(\d+);", line)
        if mm:
            measures[int(mm.group(1))] = int(mm.group(2))
            continue
        mp = re.match(r"prx\(([^,]+),([^)]+)\) \$(\d+);", line)
        if mp:
            theta = eval(mp.group(1), {"pi": math.pi})
            phi = eval(mp.group(2), {"pi": math.pi})
            n = np.cos(phi), np.sin(phi)
            U = (math.cos(theta / 2) * np.eye(2)
                 - 1j * math.sin(theta / 2)
                 * np.array([[0, n[0] - 1j * n[1]],
                             [n[0] + 1j * n[1], 0]]))
            gates.append(((int(mp.group(3)),), U.astype(complex), "prx"))
            continue
        mc = re.match(r"cz \$(\d+),\$(\d+);", line)
        if mc:
            U = np.diag([1, 1, 1, -1]).astype(complex)
            gates.append(((int(mc.group(1)), int(mc.group(2))), U, "cz"))
    return gates, measures


def predict(rec: dict, strength: float, convention: str) -> dict:
    m, bits = rec["m"], rec["bits"]
    gates, measures = parse_program(rec["compiledProgram"])
    phys = sorted({q for qs, _, _ in gates for q in qs}
                  | set(measures.values()))
    site = {q: i for i, q in enumerate(phys)}
    n = len(phys)
    dims = [2] * n

    cost_1q = 1.0 if convention == "paper" else 0.0
    # apply_unitary wants ascending sites; CZ is symmetric so sorting is free
    glist = [(tuple(sorted(site[q] for q in qs)), U,
              1.0 if kind == "cz" else cost_1q)
             for qs, U, kind in gates]

    rho = np.zeros((2 ** n, 2 ** n), complex)
    rho[0, 0] = 1.0
    rho = rho.reshape(dims + dims)
    E = (channels_by_cost(2, glist, "depolarizing", strength)
         if strength > 0 else None)
    rho = run_circuit(dims, glist, rho, E)
    probs = np.real(np.diag(rho.reshape(2 ** n, 2 ** n))).copy()

    # read out through the compiler's measurement map: c[0..m-1] is the
    # control (c[0] = MSB, the validated convention), c[m] the work qubit
    D = 1 << m
    y_of = np.zeros(2 ** n, dtype=np.intp)
    w_of = np.zeros(2 ** n, dtype=bool)
    for idx in range(2 ** n):
        bits_phys = [(idx >> (n - 1 - s)) & 1 for s in range(n)]
        y = 0
        for ci in range(m):
            y = (y << 1) | bits_phys[site[measures[ci]]]
        y_of[idx] = y
        w_of[idx] = bool(bits_phys[site[measures[m]]])
    yprobs = np.bincount(y_of, weights=probs, minlength=D)
    mask = success_mask(D, bits)
    return {"success": float(yprobs[mask].sum()),
            "work_qubit_one": float(probs[w_of].sum())}


def main():
    compiled = json.load(open(os.path.join(RESULTS, "garnet_compiled.json")))
    measured = {r["label"]: r
                for r in json.load(open(os.path.join(
                    RESULTS, "braket_pilot_results.json")))
                if "garnet" in r.get("label", "")}
    out = {}
    for key, rec in compiled.items():
        m = rec["m"]
        gates, _ = parse_program(rec["compiledProgram"])
        n_cz = sum(1 for _, _, k in gates if k == "cz")
        n_prx = len(gates) - n_cz
        meas = measured[f"garnet_m{m}"]
        noiseless = predict(rec, 0.0, "paper")
        ok = abs(noiseless["success"] - meas["noiseless"]) < 1e-6
        print(f"m={m}: routed {n_cz} cz / {n_prx} prx; parsed noiseless "
              f"success {noiseless['success']:.6f} vs analytic "
              f"{meas['noiseless']:.6f} -> {'OK' if ok else 'MISMATCH'}")
        entry = {"m": m, "bits": rec["bits"], "n_cz": n_cz, "n_prx": n_prx,
                 "noiseless_parsed": noiseless["success"],
                 "noiseless_analytic": meas["noiseless"],
                 "parse_validated": ok,
                 "measured": {k: meas[k] for k in
                              ("success", "stderr", "floor", "signal",
                               "work_qubit_one")},
                 "predictions": []}
        span = meas["noiseless"] - meas["floor"]
        for conv in CONVENTIONS:
            for s in STRENGTHS:
                p = predict(rec, s, conv)
                p.update({"strength": s, "convention": conv,
                          "signal": (p["success"] - meas["floor"]) / span})
                entry["predictions"].append(p)
                print(f"   {conv:8s} s={s:<6g} success={p['success']:.4f} "
                      f"signal={p['signal']:.4f} "
                      f"work|1>={p['work_qubit_one']:.4f}")
        print(f"   measured: success={meas['success']:.4f} "
              f"signal={meas['signal']:.4f} "
              f"work|1>={meas['work_qubit_one']:.4f}")
        out[key] = entry

    with open(os.path.join(RESULTS, "garnet_routed.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/garnet_routed.json")


if __name__ == "__main__":
    main()
