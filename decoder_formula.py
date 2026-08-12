"""Exact closed-form law for the continued-fraction acceptance set.

decoder_scaling.py measured |A| = #{y : decode(y) = r} by enumeration and
found (i) |A| ~ D^1.03, (ii) a per-peak r=5 vs r=10 ratio of ~9.5x where
the single-peak envelope D/r^2 predicts 4x, with the deviation tracking
the admissible-denominator count floor(N/r) (correlation 0.83). This
module replaces that correlation with an exact theorem and verifies it
against enumeration, outcome for outcome.

Step 1 -- decoder characterization (verified in part (a)):
    decode(y) = r  <=>  some convergent denominator q of y/D satisfies
                        q <= N and r | q.
The code's minimize step always returns the true order: a^q = 1 forces
r | q, and the smallest divisor of q that is a multiple of r is r.

Step 2 -- exact count (verified in part (b)). For reduced p/q the set
{x in (0,1) : p/q is a convergent of x} is the open interval between the
two Stern-Brocot mediants
    M1 = (p+p')/(q+q'),   M2 = (2p-p')/(2q-q'),
where p'/q' is the canonical penultimate convergent of p/q. Partitioning
acceptance by the FIRST admissible convergent of y/D gives

    |A| = sum over reduced p/q with r | q, q <= N, and no proper
          convergent of p/q admissible, of #{y : M1 < y/D < M2},

an exact disjoint decomposition: (i) y's convergents before p/q are the
proper convergents of p/q (plus, on the M2 side, the extra denominator
q - q', which is never admissible because gcd(q', q) = 1 and r | q force
gcd(q', r) = 1); (ii) hence p/q is the first admissible convergent for
every y it counts, exactly once.

Step 3 -- the law (part (c)). Summing window measures at fixed q:
p |-> q' is a bijection on the units of q, and the two sides add to

    mu(q) = (2/q) * sum_{u in U(q)} 1/(q+u)  ~  2 ln 2 * phi(q)/q^2,

so, up to the (measured, sub-percent) first-admissible exclusions,

    |A|/D  ->  2 ln 2 * sum_{k=1}^{floor(N/r)} phi(kr)/(kr)^2.

This explains BOTH standing numbers at once: the D-scaling is exactly
linear (slope 1), and the r=5 vs r=10 per-peak ratio is the ratio of the
phi-sums, not (r'/r)^2. It also exposes the D/r^2 estimate of paper
Table "decoder" as two compensating errors: the true q = r window is
2 ln 2 * phi(r)/r^2 per fraction (0.55x the naive (r-1)/r^2 at r = 6),
and the higher multiples 2r, 3r, ... restore the difference.

Run: python3 decoder_formula.py     (writes results/decoder_formula.json)
"""

import json
import os
from fractions import Fraction
from math import gcd, log

import numpy as np

from qudit_shor import convergents, multiplicative_order, recovered_order

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# Same grids as decoder_scaling.py
SWEEP = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
SCALING_INSTANCE = (21, 2)
FIXED_D_PAIRS = [(33, 4), (33, 2), (55, 16), (55, 4)]


def phi(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def admissible(q: int, r: int, N: int) -> bool:
    return q % r == 0 and q <= N


def enumeration_set(D: int, a: int, N: int, r: int) -> frozenset:
    """Ground truth: run the project's decoder over every outcome."""
    return frozenset(y for y in range(D) if recovered_order(y, D, a, N) == r)


def characterization_set(D: int, r: int, N: int) -> frozenset:
    """Step-1 characterization, still by enumeration (no decoder call)."""
    return frozenset(y for y in range(1, D)
                     if any(admissible(q, r, N)
                            for _, q in convergents(y, D)))


def enumeration(D: int, a: int, N: int, r: int) -> int:
    return len(enumeration_set(D, a, N, r))


def characterization_count(D: int, r: int, N: int) -> int:
    return len(characterization_set(D, r, N))


def _count_open(lo: Fraction, hi: Fraction, D: int) -> int:
    """#{integer y : lo < y/D < hi}."""
    a, b = lo * D, hi * D
    y_min = a.numerator // a.denominator + 1          # floor(a)+1 (a excluded)
    y_max = (b.numerator - 1) // b.denominator if b.denominator == 1 \
        else b.numerator // b.denominator             # floor(b), b excluded
    return max(0, y_max - y_min + 1)


def exact_count(D: int, r: int, N: int) -> int:
    """Step-2 closed-form count: no decoder, no scan over outcomes."""
    total = 0
    for q in range(r, N + 1, r):
        for p in range(1, q):
            if gcd(p, q) != 1:
                continue
            chain = convergents(p, q)         # canonical; ends with (p, q)
            assert chain[-1] == (p, q)
            proper = chain[:-1]
            if any(admissible(qq, r, N) for _, qq in proper):
                continue                      # not the first admissible
            p_, q_ = proper[-1]               # canonical penultimate
            m1 = Fraction(p + p_, q + q_)
            m2 = Fraction(2 * p - p_, 2 * q - q_)
            total += _count_open(min(m1, m2), max(m1, m2), D)
    return total


def mu_exact(q: int) -> float:
    """Exact measure of {x : q is a convergent denominator of x}."""
    return sum(2.0 / (q * (q + u)) for u in range(1, q) if gcd(u, q) == 1)


def law_fraction(r: int, N: int) -> float:
    """The asymptotic law: 2 ln 2 * sum phi(kr)/(kr)^2 over kr <= N."""
    return 2 * log(2) * sum(phi(q) / q ** 2 for q in range(r, N + 1, r))


def law_fraction_mu(r: int, N: int) -> float:
    """Same, with the exact per-denominator measure (no equidistribution)."""
    return sum(mu_exact(q) for q in range(r, N + 1, r))


def main():
    out = {}

    # --- (a) decoder == characterization, everywhere ----------------------
    print("(a) decoder characterization: decode(y)=r  <=>  "
          "some convergent q <= N with r | q")
    checks = []
    for N, a in [(21, 2), (29, 16)] + FIXED_D_PAIRS:
        r = multiplicative_order(a, N)
        for D in (64, 81, 125, 243, 256, 625, 729):
            es = enumeration_set(D, a, N, r)
            cs = characterization_set(D, r, N)
            checks.append({"N": N, "a": a, "r": r, "D": D,
                           "enumeration": len(es),
                           "characterization": len(cs)})
            assert es == cs, (N, a, D, len(es), len(cs))  # SET identity
    print(f"    sets identical (element for element) on {len(checks)} "
          f"(instance, D) combinations [6 instances x 7 sizes]")
    out["characterization_checks"] = checks

    # --- (b) exact closed-form count vs enumeration -----------------------
    N, a = SCALING_INSTANCE
    r = multiplicative_order(a, N)
    print(f"\n(b) exact count vs enumeration: N = {N}, a = {a}, r = {r}")
    print(f"{'d':>2} {'m':>3} {'D':>6} {'enum':>6} {'exact':>6} "
          f"{'law*D':>8} {'law/enum':>8}")
    rows = []
    frac_law = law_fraction(r, N)
    frac_mu = law_fraction_mu(r, N)
    for d, ms in SWEEP.items():
        for m in ms:
            D = d ** m
            e = enumeration(D, a, N, r)
            x = exact_count(D, r, N)
            rows.append({"d": d, "m": m, "D": D, "enumeration": e,
                         "exact_formula": x, "law": frac_law * D,
                         "law_over_enum": frac_law * D / e})
            flag = "" if e == x else "  <-- MISMATCH"
            print(f"{d:>2} {m:>3} {D:>6} {e:>6} {x:>6} "
                  f"{frac_law * D:>8.1f} {frac_law * D / e:>8.3f}{flag}")
            assert e == x, (d, m, D, e, x)
    print(f"    exact formula matches enumeration on all "
          f"{len(rows)} rows, outcome for outcome")
    out["exact_vs_enumeration"] = {
        "N": N, "a": a, "r": r, "rows": rows,
        "law_fraction": frac_law, "law_fraction_mu_exact": frac_mu}

    # --- (b2) same check on the within-modulus pairs ----------------------
    print("\n(b2) exact count vs enumeration, within-modulus pairs")
    pair_rows = []
    for N2, a2 in FIXED_D_PAIRS:
        r2 = multiplicative_order(a2, N2)
        for D in (5 ** 4, 5 ** 5, 2 ** 10, 3 ** 7):
            e = enumeration(D, a2, N2, r2)
            x = exact_count(D, r2, N2)
            pair_rows.append({"N": N2, "a": a2, "r": r2, "D": D,
                              "enumeration": e, "exact_formula": x})
            assert e == x, (N2, a2, D, e, x)
        print(f"    N={N2:2d} r={r2:2d}: exact on D in "
              f"{{625, 3125, 1024, 2187}}")
    out["pairs_exact"] = pair_rows

    # --- (c) the law: r-dependence resolved -------------------------------
    print("\n(c) the phi-sum law vs the D/r^2 envelope")
    print(f"{'N':>3} {'r':>3} {'|A|/D':>8} {'law':>8} {'law/meas':>8} "
          f"{'envelope':>9} {'env/meas':>9}")
    law_rows = []
    for N2, a2 in [(21, 2), (29, 16)] + FIXED_D_PAIRS:
        r2 = multiplicative_order(a2, N2)
        D = 5 ** 6 if r2 % 5 == 0 else 2 ** 14   # deep register, D >> N^2
        e = enumeration(D, a2, N2, r2)
        meas = e / D
        lawv = law_fraction(r2, N2)
        env = (r2 - 1) / r2 ** 2                  # the old estimate
        law_rows.append({"N": N2, "a": a2, "r": r2, "D": D,
                         "measured_fraction": meas, "law": lawv,
                         "mu_exact_law": law_fraction_mu(r2, N2),
                         "envelope": env})
        print(f"{N2:>3} {r2:>3} {meas:>8.4f} {lawv:>8.4f} "
              f"{lawv / meas:>8.3f} {env:>9.4f} {env / meas:>9.3f}")
    out["law_rows"] = law_rows

    # the standing 9.5x mystery, from the law alone
    for N2 in (33, 55):
        f5, f10 = law_fraction(5, N2), law_fraction(10, N2)
        pred = (f5 / 4) / (f10 / 9)               # per-peak: /(r-1)
        print(f"    N={N2}: predicted per-peak r=5/r=10 ratio "
              f"{pred:.2f} (envelope predicts 4.00; measured ~9.5)")
        out[f"per_peak_ratio_N{N2}"] = pred

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "decoder_formula.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote results/decoder_formula.json")


if __name__ == "__main__":
    main()
