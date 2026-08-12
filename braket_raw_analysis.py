"""Reproduce the raw-record hardware numbers quoted in the paper.

Two numbers in Sec. `Hardware anchor` come from the raw measurement
records rather than the scored summaries of braket_qpe_anchor.py:

  * the m=4 raw probe: the share of shots on the single most frequent
    outcome (a nearly pure output state) and how far its phase sits
    from the ideal peak;
  * the m=7 main run: the best success over every reinterpretation of
    the outcome bits -- all 7! orderings of the control bits, each in
    plain and complemented polarity (10,080 hypotheses) -- showing no
    relabeling recovers the destroyed interference peak.

Raw per-outcome histograms are stored in results/braket_raw_counts.json
(fetched from the Braket S3 records of the task ARNs shipped in
results/braket_task_*.json; account ID redacted in the public export).

Run: python3 braket_raw_analysis.py
Writes results/braket_raw_analysis.json.
"""

import itertools
import json
import os

import numpy as np

from braket_qpe_anchor import PHI, fejer, success_mask

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def probe_report(rec):
    m, shots = rec["m"], sum(rec["counts"].values())
    D = 1 << m
    top_b, top_n = max(rec["counts"].items(), key=lambda kv: kv[1])
    ideal = int(np.argmax(fejer(D)))
    y_plain = int(top_b[:m], 2)
    y_rev = int(top_b[:m][::-1], 2)
    return {
        "shots": shots,
        "top_outcome_bits": top_b,
        "top_share": top_n / shots,
        "ideal_peak": ideal,
        "top_control_plain": y_plain,
        "top_control_bitreversed": y_rev,
        "off_by": min(abs(y_plain - ideal), abs(y_rev - ideal)),
    }


def reinterpretation_search(rec):
    """Best success over all control-bit orderings x polarities."""
    m, bits = rec["m"], rec["bits"]
    D = 1 << m
    mask = success_mask(D, bits)
    shots = sum(rec["counts"].values())
    outcome_bits = [(b[:m], n) for b, n in rec["counts"].items()]
    best, n_hyp = 0.0, 0
    for perm in itertools.permutations(range(m)):
        for comp in (False, True):
            n_hyp += 1
            succ = 0
            for cb, n in outcome_bits:
                s = "".join(cb[p] for p in perm)
                y = int(s, 2)
                if comp:
                    y = D - 1 - y
                if mask[y]:
                    succ += n
            best = max(best, succ / shots)
    return {"hypotheses": n_hyp, "best_success": best,
            "scored_success": rec_success(rec)}


def rec_success(rec):
    m, bits = rec["m"], rec["bits"]
    D = 1 << m
    mask = success_mask(D, bits)
    shots = sum(rec["counts"].values())
    succ = sum(n for b, n in rec["counts"].items()
               if mask[int(b[:m][::-1], 2)])
    return succ / shots


def main():
    raw = json.load(open(os.path.join(RESULTS, "braket_raw_counts.json")))
    out = {"phi": PHI,
           "probe_m4": probe_report(raw["probe_m4"]),
           "main_m7_reinterpretation": reinterpretation_search(
               raw["main_m7"])}
    p = out["probe_m4"]
    print(f"probe_m4: top outcome {p['top_outcome_bits']} carries "
          f"{p['top_share']:.3f} of {p['shots']} shots; control reads "
          f"{p['top_control_plain']} / {p['top_control_bitreversed']} "
          f"(bit-reversed) vs ideal peak {p['ideal_peak']} "
          f"-- off by {p['off_by']}")
    r = out["main_m7_reinterpretation"]
    print(f"main_m7: best of {r['hypotheses']} reinterpretations = "
          f"{r['best_success']:.3f} (scored reading: "
          f"{r['scored_success']:.3f})")
    with open(os.path.join(RESULTS, "braket_raw_analysis.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/braket_raw_analysis.json")


if __name__ == "__main__":
    main()
