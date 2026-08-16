"""How far did the numbers move when the seeds became reproducible?

The trajectory sweeps used to seed with hash((label, d, m)); Python salts
str.__hash__ per process, so those seeds could not be regenerated and the
published runs were, in the strict sense, irreproducible. They now seed
with zlib.crc32 of the same tuple. That fixes reproducibility going
forward but re-rolls every random stream, so each Monte Carlo point moves.

This script pairs every row of results_prehash/ with its counterpart in
results/ and reports the move in units of the combined standard error,
z = (new - old) / sqrt(se_new^2 + se_old^2).

Two things follow from the z distribution, and they are worth more than
the individual deltas. Old and new use independent streams at the same
settings, so if the quoted standard errors are honest the z values are
standard normal: mean 0, sd 1. That is a calibration test over every
trajectory point in the paper at once -- several hundred of them --
rather than the five points characterised in trajectory_variance.py.
And any row whose |z| is far out of line flags a point where the
statistics, not the seed, deserve another look.

Run: python3 compare_prehash.py
Writes results/prehash_comparison.json
"""

import json
import math
import os
import sys

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
PREHASH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "results_prehash")

# Fields that identify a row within a file. A row is compared only if
# every key present in the old row matches the new one.
KEYS = ("d", "m", "a", "N", "noise_model", "model", "strength", "regime",
        "cost", "cost_model", "label", "eps", "alpha", "exponents",
        "dephase_ratio", "instance", "algo", "base", "K")
VALUE = "success"
ERROR = "stderr"


def rows_of(blob):
    for key in ("runs", "results", "rows", "points"):
        if isinstance(blob, dict) and isinstance(blob.get(key), list):
            return blob[key]
    return []


def signature(row):
    return tuple(sorted((k, str(row[k])) for k in KEYS if k in row))


def compare_file(name):
    old = json.load(open(os.path.join(PREHASH, name)))
    new = json.load(open(os.path.join(RESULTS, name)))
    o_rows, n_rows = rows_of(old), rows_of(new)
    if not o_rows or not n_rows:
        return None

    n_index = {}
    for r in n_rows:
        n_index.setdefault(signature(r), []).append(r)

    out = []
    for r in o_rows:
        sig = signature(r)
        cand = n_index.get(sig)
        if not cand or VALUE not in r:
            continue
        s = cand.pop(0)
        if VALUE not in s:
            continue
        # some files store `success` as a per-outcome vector, not a scalar
        if not all(isinstance(x.get(VALUE), (int, float))
                   and not isinstance(x.get(VALUE), bool) for x in (r, s)):
            continue
        eo, en = r.get(ERROR) or 0.0, s.get(ERROR) or 0.0
        se = math.hypot(eo, en)
        out.append({"file": name, "sig": [list(x) for x in sig],
                    "old": r[VALUE], "new": s[VALUE], "delta": s[VALUE] - r[VALUE],
                    "se": se, "z": (s[VALUE] - r[VALUE]) / se if se > 0 else None})
    return out


def main():
    if not os.path.isdir(PREHASH):
        sys.exit("results_prehash/ not found -- nothing to compare against")

    names = sorted(f for f in os.listdir(PREHASH)
                   if f.endswith(".json")
                   and os.path.exists(os.path.join(RESULTS, f)))

    allrows, per_file = [], []
    for name in names:
        try:
            rows = compare_file(name)
        except (json.JSONDecodeError, KeyError):
            continue
        if not rows:
            continue
        zs = [r["z"] for r in rows if r["z"] is not None]
        deltas = [abs(r["delta"]) for r in rows]
        # A file whose every delta is exactly zero has not been re-run yet
        # (results/ still holds the copy results_prehash/ was made from).
        # Pooling those would bury the real z distribution under a spike
        # at zero, so they are counted as pending, not as agreement.
        regenerated = max(deltas, default=0.0) > 0
        if regenerated:
            allrows.extend(rows)
        per_file.append({
            "file": name, "n_rows": len(rows), "n_with_errors": len(zs),
            "regenerated": regenerated,
            "max_abs_delta": max(deltas) if deltas else 0.0,
            "mean_z": sum(zs) / len(zs) if zs else None,
            "sd_z": (math.sqrt(sum((z - sum(zs) / len(zs)) ** 2 for z in zs)
                               / (len(zs) - 1)) if len(zs) > 1 else None),
            "max_abs_z": max((abs(z) for z in zs), default=None),
        })

    pending = [f["file"] for f in per_file if not f["regenerated"]]
    print(f"{'file':34s} {'rows':>5} {'max|d|':>8} {'mean z':>8} "
          f"{'sd z':>7} {'max|z|':>7}")
    for f in per_file:
        if not f["regenerated"]:
            print(f"{f['file']:34s} {f['n_rows']:5d}   (not yet re-run)")
            continue
        mz = f"{f['mean_z']:8.3f}" if f["mean_z"] is not None else "       -"
        sz = f"{f['sd_z']:7.3f}" if f["sd_z"] is not None else "      -"
        xz = f"{f['max_abs_z']:7.2f}" if f["max_abs_z"] is not None else "      -"
        print(f"{f['file']:34s} {f['n_rows']:5d} {f['max_abs_delta']:8.4f} "
              f"{mz} {sz} {xz}")

    zs = [r["z"] for r in allrows if r["z"] is not None]
    n = len(zs)
    mean = sum(zs) / n
    sd = math.sqrt(sum((z - mean) ** 2 for z in zs) / (n - 1))
    # under the null (bars honest, seeds independent) z ~ N(0,1)
    se_mean, se_sd = 1 / math.sqrt(n), 1 / math.sqrt(2 * (n - 1))
    outliers = sorted((r for r in allrows if r["z"] is not None),
                      key=lambda r: -abs(r["z"]))[:5]

    print(f"\n=== pooled over {n} paired trajectory points "
          f"from {len(per_file) - len(pending)} regenerated files "
          f"({len(pending)} still pending) ===")
    print(f"  mean z = {mean:+.3f} (expected 0 +- {se_mean:.3f})")
    print(f"  sd   z = {sd:.3f} (expected 1 +- {se_sd:.3f})")
    print(f"  |z| > 2: {sum(abs(z) > 2 for z in zs)} "
          f"({100 * sum(abs(z) > 2 for z in zs) / n:.1f}%, expected 4.6%)")
    print(f"  |z| > 3: {sum(abs(z) > 3 for z in zs)} "
          f"({100 * sum(abs(z) > 3 for z in zs) / n:.1f}%, expected 0.3%)")
    verdict = ("consistent with honest error bars"
               if abs(mean) < 3 * se_mean and abs(sd - 1) < 3 * se_sd
               else "NOT consistent -- the quoted bars are mis-sized")
    print(f"  -> {verdict}")
    print("\n  largest moves:")
    for r in outliers:
        sig = ", ".join(f"{k}={v}" for k, v in r["sig"])
        print(f"    z={r['z']:+6.2f}  {r['old']:.4f} -> {r['new']:.4f}  "
              f"[{r['file']}: {sig}]")

    path = os.path.join(RESULTS, "prehash_comparison.json")
    with open(path, "w") as f:
        json.dump({"per_file": per_file, "n_paired": n, "mean_z": mean,
                   "sd_z": sd, "se_mean": se_mean, "se_sd": se_sd,
                   "verdict": verdict, "rows": allrows}, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
