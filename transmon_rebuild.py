"""Rebuild of the measured-transmon-fidelity analysis (round-4 referees).

Three corrections applied together, each traceable to a round-4 referee
report (reviews/round4/):

1. Channel-consistent conversion (R1 major 1/2). The published conversion
   s = eps / (2 L (1 - 1/d^2)) is the depolarizing damage identity; the
   calibrated ladder deposits Delta(d) s per carrier-layer with
   Delta = 0.75 / 1.462 / 2.832 at d = 2/3/5, not (1 - 1/d^2) s. Converting
   a measured infidelity through the simulation channel's own damage
   identity, s = eps / (2 L Delta(d)), is also the no-double-count form:
   the inflation factor f becomes the measured gate infidelity in units of
   what the ambient ladder already deposits in the gate's layers, so the
   ladder's built-in high-level penalty is not charged twice. Reruns the
   Goss grid (both scopes) and the Hrmo *ladder* rows (global and
   gate-only) at the corrected f. Depolarizing rows are unchanged (the
   published formula is exact there).

2. Qubit-anchor sensitivity (R2 major 3, R3 major 6). Goss et al. report
   no qubit-subspace entangler, so the anchor eps2 is assumed. Sweep it
   over 99.67% (Willow-class CZ), 99.55% (published choice), 99.34%, and
   99.0%, recomputing the operating point s2 = eps2 / (2 Delta(2)), the
   implied f, and both critical factors f*(s2) by bisection.

3. Timed exposure (R2 major 1). The layer-counted convention charges the
   580-ns Goss CZ+ one layer, same as a 30-ns single-qutrit gate. The
   timed convention charges every gate its wall-clock duration in units
   of the d=2 two-qubit gate time: d=2 registers at (1q, 2q) =
   (0.2, 1.0) layers, d=3 at (0.3, rho) with rho = t_2q(3)/t_2q(2) swept
   over 1-19 (580/300 ~ 1.9 IBM-class, 5.8 at 100 ns, ~19 Google-class).
   Ambient strength equal per unit time, no gate inflation (in this
   convention the gate's decoherence is charged as time, so charging f on
   top would double-count from the other side). Locates the crossing
   rho* where the ladder/uniform qutrit cell falls to the qubit.

4. Leakage endpoint (R2 major 4). If a fraction lam of eps3 is leakage
   out of the qutrit manifold, the in-manifold inflation drops to
   (1-lam) f while leaked population (scored at the decoder floor)
   multiplies the signal by ~(1 - lam eps3)^n2q. Reports the lam = 0.5
   endpoint alongside lam = 0 (the main analysis).

Writes results/transmon_rebuild.json. Run: python3 transmon_rebuild.py
"""

import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import qudit_shor
from hrmo_reanalysis import uniform_floor, N, A
from qudit_shor import multiplicative_order, noise_superop, shor_run

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
CHANNEL = "transmon_cal"
S2_PAPER = 0.003               # the paper's transmon operating point

# Measured process infidelities (central, 1 sigma).
GOSS_EPS = {"CZ+": (0.027, 0.001), "CZ": (0.048, 0.003)}
HRMO_EPS = {2: (0.004, 0.001), 3: (0.013, 0.002), 5: (0.063, 0.003)}

# Published critical factors at s2 = 0.003 (results/noise_inflation.json,
# results/goss_transmon_test.json) -- thresholds live in strength space,
# so the conversion fix moves f, not f*.
F_STAR = {("uniform", 3, "global"): 2.05, ("uniform", 5, "global"): 2.46,
          ("ion", 3, "global"): 1.21, ("ion", 5, "global"): None,
          ("uniform", 3, "gate"): 3.63}

# Anchor sweep: assumed same-class two-qubit gate infidelity.
ANCHOR_EPS2 = [0.0033, 0.0045, 0.0066, 0.010]

# Timed convention: gate durations in units of the d=2 two-qubit gate.
T1Q = {2: 0.2, 3: 0.3}         # 20 ns / 30 ns over a 100 ns reference CZ
RHOS = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.8, 8.0, 12.0, 19.0]

# Register the timed cost models at import time so spawn workers see them.
qudit_shor.GATE_COST_MODELS["timed2"] = (lambda d: T1Q[2], lambda d: 1.0)
for _r in RHOS:
    qudit_shor.GATE_COST_MODELS[f"timed3_{_r}"] = (
        lambda d, _t=T1Q[3]: _t, lambda d, _r=_r: _r)


def ladder_damage(d: int) -> float:
    """Per-carrier-layer entanglement infidelity per unit strength, 1-F_e = Delta s."""
    s = 1e-6
    E = noise_superop(d, CHANNEL, s)
    return (1.0 - float(np.real(np.trace(E))) / d ** 2) / s


DELTA = {d: ladder_damage(d) for d in (2, 3, 5)}


def one(args):
    d, s, cost, gate_s = args
    t0 = time.time()
    if s == 0.0:
        res = shor_run(d, a=A, N=N, cost_model="uniform")
    elif gate_s is not None:
        res = shor_run(d, CHANNEL, s, a=A, N=N, cost_model=cost,
                       gate_strength=gate_s)
    else:
        res = shor_run(d, CHANNEL, s, a=A, N=N, cost_model=cost)
    return {"d": d, "strength": s, "cost": cost, "gate_strength": gate_s,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def bisect_fstar(args):
    """Critical inflation factor at operating point s2, one scope."""
    scope, s2, sig2, floors, base, lo, hi = args
    def signal3(succ):
        return (succ - floors["3"]) / (base["3"] - floors["3"])
    for _ in range(9):
        mid = (lo + hi) / 2
        if scope == "global":
            succ = shor_run(3, CHANNEL, s2 * mid, a=A, N=N,
                            cost_model="uniform")["success"]
        else:
            succ = shor_run(3, CHANNEL, s2, a=A, N=N, cost_model="uniform",
                            gate_strength=s2 * mid)["success"]
        if signal3(succ) > sig2:
            lo = mid
        else:
            hi = mid
    return {"scope": scope, "s2": s2, "f_star": (lo + hi) / 2}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {str(d): uniform_floor(d, r) for d in (2, 3, 5)}
    print(f"ladder damage Delta(d): { {k: round(v, 5) for k, v in DELTA.items()} }")

    # --- corrected inflation factors (layer-counted convention) ----------
    def goss_f(eps, sig):
        f = (eps / (2 * 1 * DELTA[3])) / S2_PAPER
        return f, f * (sig / eps)

    def hrmo_f(d, cost):
        L = 1.0 if cost == "uniform" else float(d - 1)
        eps_d, sig_d = HRMO_EPS[d]
        eps_2, sig_2 = HRMO_EPS[2]
        f = (eps_d / (2 * L * DELTA[d])) / (eps_2 / (2 * 1 * DELTA[2]))
        rel = math.sqrt((sig_d / eps_d) ** 2 + (sig_2 / eps_2) ** 2)
        return f, f * rel

    # --- job list --------------------------------------------------------
    jobs = [(2, 0.0, "uniform", None), (3, 0.0, "uniform", None),
            (5, 0.0, "uniform", None)]
    # qubit anchors: paper point plus the sweep (snap numerical twins)
    anchor_s2 = sorted({S2_PAPER} | {
        S2_PAPER if abs(e / (2 * DELTA[2]) - S2_PAPER) < 1e-5
        else e / (2 * DELTA[2]) for e in ANCHOR_EPS2})
    jobs += [(2, s2, "uniform", None) for s2 in anchor_s2]

    goss_variants = {}   # (gate, scope) -> [(label, f, job)]
    for gate, (eps, sig) in GOSS_EPS.items():
        f, fs = goss_f(eps, sig)
        for scope in ("global", "gate"):
            vs = []
            for lab, ff in (("lo", f - fs), ("central", f), ("hi", f + fs)):
                job = ((3, S2_PAPER * ff, "uniform", None) if scope == "global"
                       else (3, S2_PAPER, "uniform", S2_PAPER * ff))
                vs.append((lab, ff, job))
                jobs.append(job)
            goss_variants[(gate, scope)] = vs

    hrmo_variants = {}   # (cost, d, scope) -> [(label, f, job)]
    for cost in ("uniform", "ion"):
        for d in (3, 5):
            f, fs = hrmo_f(d, cost)
            for scope in ("global", "gate"):
                vs = []
                for lab, ff in (("lo", f - fs), ("central", f), ("hi", f + fs)):
                    ff = max(ff, 0.0)
                    job = ((d, S2_PAPER * ff, cost, None) if scope == "global"
                           else (d, S2_PAPER, cost, S2_PAPER * ff))
                    vs.append((lab, ff, job))
                    jobs.append(job)
                hrmo_variants[(cost, d, scope)] = vs

    # leakage endpoint: lam = 0.5 of the Goss CZ+ infidelity is leakage
    lam = 0.5
    f_leak = goss_f(GOSS_EPS["CZ+"][0] * (1 - lam), 0.0)[0]
    jobs += [(3, S2_PAPER, "uniform", S2_PAPER * f_leak),
             (3, S2_PAPER * f_leak, "uniform", None)]

    # timed convention
    jobs.append((2, S2_PAPER, "timed2", None))
    jobs += [(3, S2_PAPER, f"timed3_{rho}", None) for rho in RHOS]

    jobs = list(dict.fromkeys(jobs))
    print(f"{len(jobs)} exact-DM runs", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        runs = list(ex.map(one, jobs))
    print(f"grid done in {time.time() - t0:.0f} s", flush=True)

    res = {tuple(j): x["success"] for j, x in zip(jobs, runs)}
    base = {str(d): res[(d, 0.0, "uniform", None)] for d in (2, 3, 5)}

    def signal(d, succ):
        return (succ - floors[str(d)]) / (base[str(d)] - floors[str(d)])

    sig2_paper = signal(2, res[(2, S2_PAPER, "uniform", None)])

    out = {"N": N, "a": A, "r": r, "channel": CHANNEL, "s2_paper": S2_PAPER,
           "ladder_damage": DELTA, "floors": floors, "noiseless": base,
           "qubit_signal_paper": sig2_paper, "goss_eps": GOSS_EPS,
           "hrmo_eps": {str(k): v for k, v in HRMO_EPS.items()},
           "runs": runs}

    # --- Part A: corrected Goss + Hrmo ladder cells ----------------------
    print(f"\nqubit anchor (ladder, s={S2_PAPER}): signal {sig2_paper:.3f}")
    print("A. corrected conversion (layer-counted):")
    cells = []
    for gate, (eps, sig) in GOSS_EPS.items():
        f, fs = goss_f(eps, sig)
        for scope in ("global", "gate"):
            sigs = {lab: signal(3, res[job])
                    for lab, _, job in goss_variants[(gate, scope)]}
            fstar = F_STAR[("uniform", 3, scope)]
            verdict = ("LOST (even at -1 sigma)"
                       if sigs["lo"] < sig2_paper and sigs["central"] < sig2_paper
                       else "lost (survives at -1 sigma)"
                       if sigs["central"] < sig2_paper else "SURVIVES")
            cells.append({"set": "goss", "gate": gate, "scope": scope,
                          "d": 3, "cost": "uniform",
                          "f_central": f, "f_sigma": fs, "f_star": fstar,
                          "qubit_signal": sig2_paper,
                          "qudit_signal": sigs, "verdict": verdict})
            print(f"  goss {gate:>4} {scope:>6}  f {f:5.2f}+/-{fs:4.2f} "
                  f"f* {fstar}  sig {sigs['lo']:.3f}/{sigs['central']:.3f}/"
                  f"{sigs['hi']:.3f} vs {sig2_paper:.3f}  {verdict}")
    for cost in ("uniform", "ion"):
        for d in (3, 5):
            f, fs = hrmo_f(d, cost)
            for scope in ("global", "gate"):
                sigs = {lab: signal(d, res[job])
                        for lab, _, job in hrmo_variants[(cost, d, scope)]}
                fstar = F_STAR.get((cost, d, scope))
                verdict = ("LOST (even at -1 sigma)"
                           if sigs["lo"] < sig2_paper and sigs["central"] < sig2_paper
                           else "lost (survives at -1 sigma)"
                           if sigs["central"] < sig2_paper else "SURVIVES")
                cells.append({"set": "hrmo", "cost": cost, "d": d,
                              "scope": scope, "f_central": f, "f_sigma": fs,
                              "f_star": fstar, "qubit_signal": sig2_paper,
                              "qudit_signal": sigs, "verdict": verdict})
                print(f"  hrmo d={d} {cost:>7} {scope:>6}  f {f:5.2f}+/-{fs:4.2f} "
                      f"f* {fstar}  sig {sigs['lo']:.3f}/{sigs['central']:.3f}/"
                      f"{sigs['hi']:.3f} vs {sig2_paper:.3f}  {verdict}")
    out["cells"] = cells

    # --- Part B: anchor sweep with f* recomputed -------------------------
    print("\nB. anchor sweep (f* by bisection at each operating point):")
    t0 = time.time()
    bis_jobs = []
    for s2 in anchor_s2:
        sig2 = signal(2, res[(2, s2, "uniform", None)])
        bis_jobs.append(("global", s2, sig2, floors, base, 1.0, 6.0))
        bis_jobs.append(("gate", s2, sig2, floors, base, 1.5, 9.0))
    with ProcessPoolExecutor(max_workers=6) as ex:
        fstars = list(ex.map(bisect_fstar, bis_jobs))
    print(f"bisections done in {time.time() - t0:.0f} s", flush=True)

    anchors = []
    for s2 in anchor_s2:
        eps2 = 2 * DELTA[2] * s2
        f_czp = (GOSS_EPS["CZ+"][0] / (2 * DELTA[3])) / s2
        row = {"s2": s2, "eps2": eps2, "fidelity2": 1 - eps2,
               "qubit_signal": signal(2, res[(2, s2, "uniform", None)]),
               "f_czplus": f_czp}
        for x in fstars:
            if abs(x["s2"] - s2) < 1e-12:
                eps3_target = x["f_star"] * s2 * 2 * DELTA[3]
                row[f"f_star_{x['scope']}"] = x["f_star"]
                row[f"eps3_target_{x['scope']}"] = eps3_target
        anchors.append(row)
        print(f"  eps2 {eps2:.4f} ({100 * (1 - eps2):.2f}%): f(CZ+) {f_czp:5.2f}  "
              f"f* glob {row.get('f_star_global', float('nan')):.2f} "
              f"(target {100 * (1 - row.get('eps3_target_global', 0)):.1f}%)  "
              f"f* gate {row.get('f_star_gate', float('nan')):.2f} "
              f"(target {100 * (1 - row.get('eps3_target_gate', 0)):.1f}%)")
    out["anchor_sweep"] = anchors

    # --- Part C: timed convention ---------------------------------------
    print("\nC. timed convention (ambient per unit time, no gate inflation):")
    sig2_t = signal(2, res[(2, S2_PAPER, "timed2", None)])
    timed = {"t1q": T1Q, "qubit_signal": sig2_t, "rows": []}
    prev = None
    rho_star = None
    for rho in RHOS:
        sg = signal(3, res[(3, S2_PAPER, f"timed3_{rho}", None)])
        timed["rows"].append({"rho": rho, "qutrit_signal": sg,
                              "margin": sg - sig2_t})
        if prev is not None and prev[1] >= sig2_t > sg and rho_star is None:
            r0, m0 = prev[0], prev[1] - sig2_t
            rho_star = r0 + (rho - r0) * m0 / (m0 - (sg - sig2_t))
        prev = (rho, sg)
        print(f"  rho {rho:5.2f}: qutrit {sg:.3f} vs qubit {sig2_t:.3f} "
              f"margin {sg - sig2_t:+.3f}")
    timed["rho_star"] = rho_star
    print(f"  crossing rho* = {rho_star if rho_star else '> sweep range'}")
    out["timed"] = timed

    # --- Part D: leakage endpoint ---------------------------------------
    n2q = 18   # two-qudit gate applications in the d=3 demo circuit
    surv = (1 - lam * GOSS_EPS["CZ+"][0]) ** n2q
    sg_gate = signal(3, res[(3, S2_PAPER, "uniform", S2_PAPER * f_leak)]) * surv
    sg_glob = signal(3, res[(3, S2_PAPER * f_leak, "uniform", None)]) * surv
    out["leakage"] = {"lambda": lam, "f_inmanifold": f_leak, "n2q": n2q,
                      "survival": surv,
                      "qutrit_signal_gate_only": sg_gate,
                      "qutrit_signal_global": sg_glob,
                      "qubit_signal": sig2_paper}
    print(f"\nD. leakage endpoint (lam={lam}): f_in {f_leak:.2f}, "
          f"survival {surv:.3f}; gate-only {sg_gate:.3f}, global {sg_glob:.3f} "
          f"vs qubit {sig2_paper:.3f}")

    # ambient-vs-measured decomposition (R1 major 2 diagnostic)
    out["ambient_check"] = {
        "layer_counted_ambient_eps3": 2 * 1 * DELTA[3] * S2_PAPER,
        "timed_ambient_eps3_rho5.8": 2 * 5.8 * DELTA[3] * S2_PAPER,
        "measured_eps3_czplus": GOSS_EPS["CZ+"][0]}

    path = os.path.join(RESULTS, "transmon_rebuild.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
