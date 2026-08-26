# A student's textbook for this repository

*Everything you need to derive the paper from scratch.*

This document is the self-contained mathematical and physical background
for `paper/main.tex` — **"Native gates or nothing: the condition for a
qudit advantage in uncorrected quantum algorithms under decoherence."**
It assumes linear algebra and undergraduate quantum mechanics (kets,
tensor products, Born rule) and nothing else. Everything else — qudits,
the Fourier transform over Z_D, phase estimation, continued fractions,
Lindblad channels, entanglement fidelity, quantum trajectories — is
built here from the definitions.

The other documents in `docs/` are *lab notebooks*: they record what was
run, in the order it was run, including the things that turned out to be
wrong. This one is the opposite. It is the shortest correct path from
first principles to the paper's result, with the wrong turns removed and
the mathematics stated once, properly.

**How to read it.** Parts I–II are standard material presented in base
*d* rather than base 2; if you know Shor's algorithm you can skim them
and just absorb the notation in §A.1. Part III (number theory) and
Part IV (open systems) contain the two derivations that are original to
this work — the decoder acceptance law and the damage-unit accounting.
Part V assembles them into the paper's central condition. Part VI is
exercises, every one of which is checkable against a script in this
repo.

**Conventions.** *d* is the qudit dimension (levels per carrier), *m*
the number of control carriers, *D = dᵐ* the control dimension, *w* the
number of work carriers, *N* the modulus, *r* the multiplicative order,
ω = e^{2πi/d}, and ω_D = e^{2πi/D}. "Carrier" means one physical
*d*-level system; "layer" means one time step of the serial schedule.
Logarithms are base 2 unless written ln.

---

## Contents

**Part I — The qudit**
1. [Hilbert space, basis, and the generalized Pauli group](#1-hilbert-space-basis-and-the-generalized-pauli-group)
2. [Why *prime* d is special](#2-why-prime-d-is-special)
3. [Gates, and what a two-qudit gate costs](#3-gates-and-what-a-two-qudit-gate-costs)
4. [Registers: width, depth, and qubit-equivalents](#4-registers-width-depth-and-qubit-equivalents)

**Part II — The algorithms**
5. [The Fourier transform over Z_D](#5-the-fourier-transform-over-z_d)
6. [Phase estimation, derived](#6-phase-estimation-derived)
7. [Order finding: why Shor *is* phase estimation](#7-order-finding-why-shor-is-phase-estimation)
8. [Continued fractions](#8-continued-fractions)
9. [Grover search in base d](#9-grover-search-in-base-d)

**Part III — The number theory**
10. [Grid alignment](#10-grid-alignment)
11. [The decoder acceptance lemma](#11-the-decoder-acceptance-lemma)
12. [The decoder acceptance law](#12-the-decoder-acceptance-law)

**Part IV — Open quantum systems**
13. [Density matrices, CPTP maps, and the superoperator](#13-density-matrices-cptp-maps-and-the-superoperator)
14. [Damage units: entanglement fidelity as the currency](#14-damage-units-entanglement-fidelity-as-the-currency)
15. [The calibrated ladder channel](#15-the-calibrated-ladder-channel)
16. [Realizing a dephasing matrix exactly: Euclidean embedding](#16-realizing-a-dephasing-matrix-exactly-euclidean-embedding)
17. [Depolarizing, and the Zeeman failure mode](#17-depolarizing-and-the-zeeman-failure-mode)
18. [Quantum trajectories](#18-quantum-trajectories)

**Part V — The accounting, and the result**
19. [Exposure, cost models, and break-even](#19-exposure-cost-models-and-break-even)
20. [The success metric](#20-the-success-metric)
21. [Assembling the paper's condition](#21-assembling-the-papers-condition)
22. [What is *not* settled](#22-what-is-not-settled)

**Part VI — [Exercises](#part-vi--exercises)**

**Appendix — [Notation](#a1-notation) · [Reading path](#a2-reading-path) · [Script map](#a3-script-map)**

---
---

# Part I — The qudit

## 1. Hilbert space, basis, and the generalized Pauli group

A **qudit** of dimension *d* is a quantum system with state space
ℋ_d ≅ ℂ^d and a distinguished orthonormal *computational basis*

    {|0⟩, |1⟩, …, |d−1⟩}.

At *d = 2* this is a qubit; *d = 3* a **qutrit**; *d = 5* a **ququint**.
The labels are integers mod *d*, and that is the whole point: the basis
carries the arithmetic of the ring **Z_d**, and every gate below is
defined by what it does to those labels.

### 1.1 The two generators

Write ω = e^{2πi/d}, a primitive *d*-th root of unity. Define the
**shift** (generalized Pauli X) and the **clock** (generalized Pauli Z):

    X|j⟩ = |j + 1 mod d⟩          Z|j⟩ = ω^j |j⟩

Both are unitary, both have order *d* (X^d = Z^d = 𝟙), and neither is
Hermitian for d > 2 — the first thing that breaks when you leave the
qubit. At *d = 2*, ω = −1 and these reduce to the familiar Pauli X and
Z.

Their commutation relation is the **Weyl relation**:

    Z X = ω X Z          equivalently   X^a Z^b = ω^{−ab} Z^b X^a

This one equation is the algebraic seed of everything that follows. The
*d²* operators {X^a Z^b : a, b ∈ Z_d} form a basis for the operators on
ℋ_d (the **Weyl–Heisenberg** or generalized Pauli basis), orthogonal
under the Hilbert–Schmidt inner product ⟨A, B⟩ = tr(A†B):

    tr( (X^a Z^b)† X^{a'} Z^{b'} ) = d · δ_{aa'} δ_{bb'}

Consequently *any* qudit operator, and in particular any noise process,
can be expanded in generalized Paulis — which is how the depolarizing
channel of §17 is built.

### 1.2 Why "generalized Pauli" and not "Pauli"

For d > 2 the group generated by X and Z contains phases ω^k, so it is
not a group of Hermitian observables. The physically meaningful object
is the group modulo phases, of order *d²*. Its normalizer in the unitary
group is the **Clifford group** — the qudit generalization of
{H, S, CNOT} — and it is the structure of that group that makes prime
*d* special.

---

## 2. Why *prime* d is special

Three independent reasons, all reducing to one algebraic fact.

**The fact.** Z_d is a **field** if and only if *d* is prime. In a
field every non-zero element has a multiplicative inverse, so linear
algebra over Z_d works exactly as it does over ℝ or ℂ: systems of linear
equations have unique solutions, matrices have well-defined ranks, and
there are no zero divisors.

**Consequence 1 — Mutually unbiased bases.** Two orthonormal bases
{|a_i⟩}, {|b_j⟩} are *mutually unbiased* if |⟨a_i|b_j⟩|² = 1/d for all
i, j. For prime *d* (and prime powers, via GF(d)) there exist exactly
**d + 1** mutually unbiased bases, the maximum the dimension allows, and
they are constructed explicitly from the eigenbases of the operators
{X Z^k}. For composite *d* the maximal number is an open problem
(unknown already at d = 6). MUBs are the measurement backbone of
tomography and of many error-correction constructions.

**Consequence 2 — Stabilizer codes close.** A stabilizer code is
defined by an abelian subgroup of the generalized Pauli group. Over a
field, the subgroup ↔ subspace correspondence is clean and the standard
qubit machinery — symplectic representation, CSS constructions, the
Gottesman–Knill theorem — transfers verbatim. Gottesman's 1998
construction of fault-tolerant computation in higher dimensions is
stated for prime *d* precisely for this reason
(`papers/gottesman-1998-*.pdf`). At *d = 4* one recovers the structure
via GF(4); at *d = 6* there is no field and the machinery genuinely
breaks.

**Consequence 3 — Discrete phase space is clean.** For *odd prime* d
the discrete Wigner function is non-negative exactly on the stabilizer
states, giving a clean resource-theoretic notion of "magic"
(`papers/gross-2006-*.pdf`). At d = 2 the analogous statement fails
(state-independent contextuality intervenes); at composite *d* the phase
space does not factor.

**Consequence 4 — QFT-based arithmetic is built on the odd-prime
case.** The in-place multipliers, quadratic-phase operators and
fractional Fourier transforms of Floratos–Pavlidis assume odd prime *d*,
where the discrete rotation group is cyclic and **every nonzero
multiplier is invertible** — which is again the field property. This is
the same construction that supplies the `pavlidis` cost model (§3.3), so
primality enters this paper twice: once through fault tolerance, once
through the arithmetic whose compilation cost decides the verdict.

### 2.1 …and why primality plays **no role** in this paper's dynamics

This is worth stating loudly, because it is a result of the work and a
frequent misreading. The circuits simulated here — Fourier gates,
controlled phases, controlled modular multipliers, Grover diffusers —
use only the *ring* Z_d, not the field. Nothing in the noise channels
uses primality either. So the bare, uncorrected dynamics should not care
whether *d* is prime, and the paper's composite controls confirm it:
*d = 4* and *d = 6* both land inside the qudit band (§21.4).

Primality is inherited from the **fault-tolerance and QFT-arithmetic
motivations** — the reasons anyone wants prime-dimensional hardware, and
the setting in which the compiled-arithmetic constructions are stated —
not from the algorithm-level physics measured here. Keep the two
separate.

---

## 3. Gates, and what a two-qudit gate costs

### 3.1 Single-qudit gates

The workhorse is the **Fourier gate** F_d (the generalized Hadamard):

    F_d |j⟩ = (1/√d) Σ_{k=0}^{d−1} ω^{jk} |k⟩

It is unitary, F_d† F_d = 𝟙, and it diagonalizes the shift:
F_d† X F_d = Z. At d = 2, F_2 = H. Applying F_d to |0⟩ gives the
uniform superposition — the initialization step of every algorithm here.

Also used: diagonal **phase gates** diag(1, e^{iθ_1}, …, e^{iθ_{d−1}}),
which generate the controlled rotations of the QFT.

### 3.2 Two-qudit gates

The entangling primitive is the **controlled phase**

    CP(θ) |j⟩|k⟩ = e^{i θ j k} |j⟩|k⟩

and, for order finding, the **controlled modular multiplier**

    |c⟩|x⟩ ↦ |c⟩ |a^c x mod N⟩.

In this repo the multiplier is applied as an *exact unitary* — we do not
compile it — but it is *charged* the cost of the carriers it spans.
That distinction is the subject of the next paragraph and, ultimately,
of the paper's whole result.

### 3.3 The cost question, stated early

Here is the crux, and it is a hardware question, not a mathematical one.

A base-*d* register needs fewer carriers and fewer time-layers than a
base-2 register at the same problem size (§4). That is a **rebate**. But
a two-qudit entangling gate on real hardware may cost *more* than a
two-qubit gate, by a factor that grows with *d*. That is a
**surcharge**. Whether the qudit wins is whether the rebate exceeds the
surcharge.

Three published cost structures bracket the possibilities, and this repo
charges all three as multipliers on the layer count:

| model | charge per entangling gate | physical realization |
|---|---|---|
| `uniform` | 1 layer, any *d* | native entangler — cross-Kerr CZ on transmons |
| `ion` | *d* − 1 layers | Ringbauer's 2(*d*−1) Mølmer–Sørensen pulse construction, normalized to 1 at *d* = 2 |
| `pavlidis` | *d*²/4 layers, all gates | two-level (Givens-style) decomposition of the QFT-arithmetic circuits |

The `pavlidis` charge is deliberately generous to the qudit: the actual
decomposition of Pavlidis–Floratos costs 4(*d*−1)² elementary two-level
gates per controlled rotation, i.e. (*d*−1)² after the same *d* = 2
normalization — 4 at *d* = 3 and 16 at *d* = 5, against the 2.25 and
6.25 that *d*²/4 charges. **Verdicts against decomposed gates are
therefore conservative.** A 2024 follow-up by the same authors reports
the same *d*² scaling in **depth** (not merely gate count) for a full
QFT-based in-place modular multiplier under 1D-local connectivity, which
is what licenses treating `pavlidis` as a uniform layer multiplier.

On the benchmark instance (*N* = 21) these three models swing the
ququint circuit from **3.8× shorter** than the qubit's to **1.6×
longer**:

    layers (d = 2 / 3 / 5)
    uniform    57 / 26   / 15
    ion        57 / 44   / 42
    pavlidis   57 / 58.5 / 93.8

That swing — a factor of 6 in ququint depth — is larger than anything
the noise model does. Hold this table in mind; §21 is essentially its
consequence.

---

## 4. Registers: width, depth, and qubit-equivalents

### 4.1 Width

To hold an integer < *N* you need

    w = ⌈log_d N⌉   carriers.

For *N* = 21: *w* = 5 (d=2), 3 (d=3), 2 (d=5). To hold a
phase-estimation control register of dimension *D* you need *m* =
log_d D carriers. **Width compression is exactly a factor log₂ d**: a
base-*d* register uses 1/log₂ d as many carriers as a qubit register at
the same Hilbert-space dimension.

### 4.2 Depth

The controlled-U^{d^i} chain has *m* gates rather than the qubit's
log₂ D, and the inverse QFT has m(m−1)/2 controlled rotations rather
than the qubit's much larger triangle. Both shrink with *d*. **Depth
compression is roughly (log₂ d)²** before cost models are applied,
because both the number of control digits *and* the QFT triangle shrink.

### 4.3 Qubit-equivalents

To compare across bases fairly, everything is indexed by

    qubit-equivalents = log₂ (dim ℋ) = log₂(D · d^w).

The paper's deepest register is *d* = 3, *m* = 9, *w* = 3 →
dim ℋ = 3¹² = 5.3 × 10⁵ = **19.0 qubit-equivalents**. The widest *qubit*
register run is 17 qubits. These are different numbers describing the
same axis, and conflating them is a standard reporting error.

### 4.4 The exposure that width and depth buy

Combining: total noise exposure is

    exposure = (carriers) × (time-layers)

and at matched problem size, going *d* = 2 → *d* = 5 compresses Shor's
exposure by **10.9×** and Grover's by only **5.7×** — a fact the paper
uses as an experimental knob (§9.3, §21.3).

---
---

# Part II — The algorithms

## 5. The Fourier transform over Z_D

### 5.1 Definition

For a control register of *m* base-*d* carriers, the computational basis
is naturally labelled by Z_D with *D = dᵐ* via

    |y⟩ = |y_{m−1}⟩ ⊗ ⋯ ⊗ |y_0⟩,   y = Σ_i y_i d^i.

The **quantum Fourier transform over Z_D** is

    QFT_D |x⟩ = (1/√D) Σ_{y=0}^{D−1} ω_D^{xy} |y⟩,   ω_D = e^{2πi/D}.

### 5.2 The factorized (circuit) form

The single fact that makes QFT_D efficient is that the phase ω_D^{xy}
factorizes across digits. Writing y = Σ_i y_i d^i,

    ω_D^{xy} = Π_i ω_D^{x y_i d^i} = Π_i exp(2πi x y_i / d^{m−i})

so the QFT is a product of *m* single-carrier Fourier gates interleaved
with two-carrier controlled phases:

    QFT_D = Π_{i} [ F_d on carrier i ] · Π_{j > i} CP( 2π / d^{j−i+1} )

with the digits emerging in reversed order. This gives *m* Fourier gates
and m(m−1)/2 controlled rotations.

### 5.3 The no-swap convention

Textbook presentations append *m*/2 SWAPs to undo the digit reversal.
This repo does **not**: the reversal is absorbed into the classical
reading of the outcome. Two reasons, one physical and one that bit us on
hardware:

- SWAPs are three entangling gates each and would be charged as such,
  penalizing whichever base has more carriers — i.e. *d* = 2. Dropping
  them is the *conservative* choice for the qudit claim.
- Different devices reverse in different directions. IonQ Forte-1
  returns the control register digit-reversed relative to the Braket
  local simulator; the *m* = 5 hardware peak sits exactly on the
  bit-reversed ideal outcome. Getting this wrong looks exactly like a
  failed experiment (§21.5).

### 5.4 Approximate QFT (AQFT)

The controlled rotation between digits *i* and *j* has angle
2π/d^{j−i+1}, which decays geometrically with digit separation. Dropping
all rotations with j − i > k (the **AQFT**) costs little fidelity and
saves many gates — a base-2 result of Barenco *et al.* and Nam–Kim that
Pavlidis and Floratos conjectured extends to qudits. The paper tests it
on hardware once (dropping the three smallest angles at *m* = 7) and
finds it recovers a factor ~6 but cannot repair a *coherent* failure —
a datum adjacent to that conjecture, not a test of it.

---

## 6. Phase estimation, derived

### 6.1 The problem

Given a unitary *U*, an eigenstate |u⟩ with U|u⟩ = e^{2πiφ}|u⟩, and the
ability to apply controlled-U^k, estimate φ ∈ [0, 1).

### 6.2 The circuit and its output distribution

Prepare *m* control carriers in the uniform superposition via F_d^{⊗m},
apply controlled-U^{d^i} from control carrier *i*, then QFT_D†, then
measure. Tracking the state:

    |0⟩^{⊗m}|u⟩
      --F_d^{⊗m}-->  (1/√D) Σ_{x=0}^{D−1} |x⟩ |u⟩
      --c-U^{d^i}-->  (1/√D) Σ_x e^{2πi φ x} |x⟩ |u⟩
      --QFT_D†-->     (1/D) Σ_y [ Σ_x e^{2πi x (φ − y/D)} ] |y⟩ |u⟩

The bracket is a geometric series. With δ_y = φ − y/D,

    P(y) = (1/D²) · | Σ_{x=0}^{D−1} e^{2πi x δ_y} |²
         = (1/D²) · sin²(π D δ_y) / sin²(π δ_y)

which is the **Fejér kernel**. Three properties do all the work:

1. **Exact hit.** If φ = y₀/D for some integer y₀, then δ_{y₀} = 0 and
   P(y₀) = 1 exactly. The distribution is a delta function.
2. **Worst case.** If φ lies exactly between grid points, the best
   outcome still has P ≥ 4/π² ≈ 0.405, and P(nearest) + P(next
   nearest) ≥ 8/π².
3. **Tails.** P(y) ≈ 1/(πDδ_y)² far from the peak — the peak stays
   **~1 outcome wide** no matter how large *D* grows. Remember this;
   §12 contrasts it with an acceptance window that grows like *D*.

### 6.3 The eigenstate case as a benchmark

For the paper's QPE benchmark, *U* is diagonal with target phase equal
to the golden-ratio conjugate

    φ* = (√5 − 1)/2 ≈ 0.6180339887…

chosen because it is the "most irrational" number — its continued
fraction is [0; 1, 1, 1, …], so it is badly approximable by fractions
with small denominators in *any* base. That makes eigenstate QPE
**structurally immune to the grid-alignment confound of §10**, which is
exactly why it is in the paper: it is the control against which the
Shor results are checked.

Success criterion: the estimate lands within 2^{−(b+1)} of φ*, at
*b* = 5 bits.

---

## 7. Order finding: why Shor *is* phase estimation

### 7.1 The problem

Given *N* and *a* coprime to *N*, find the **multiplicative order**

    r = ord_N(a) = min{ k > 0 : a^k ≡ 1 (mod N) }.

This is the quantum core of Shor's factoring algorithm; the reduction
from factoring to order finding is entirely classical and is not
simulated here.

### 7.2 The eigenstates of the multiplier

Let U_a |x⟩ = |a x mod N⟩ on the work register. For each s ∈ {0, …, r−1}
define

    |u_s⟩ = (1/√r) Σ_{k=0}^{r−1} e^{−2πi s k / r} |a^k mod N⟩.

Then

    U_a |u_s⟩ = e^{2πi s / r} |u_s⟩,

so |u_s⟩ is an eigenstate with phase **s/r**. Phase estimation on
|u_s⟩ therefore returns an approximation to s/r, from which *r* can be
recovered (§8).

### 7.3 The trick: |1⟩ is all of them at once

We cannot prepare |u_s⟩ — doing so would require knowing *r*. But the
inverse transform gives

    (1/√r) Σ_{s=0}^{r−1} |u_s⟩ = |1⟩,

the trivially preparable state. So running phase estimation on |x = 1⟩
runs it on an **equal superposition of all r eigenstates
simultaneously**, and the measurement collapses onto one *s* uniformly
at random. The output distribution is the Fejér kernel of §6.2
**centred on each of the r phases s/r**, with weight 1/r each.

This is the sense in which *Shor is phase estimation*, and it is not a
loose analogy — it is an exact statement about the same circuit with a
different input.

### 7.4 The interpolation experiment (a falsified hypothesis)

Because |1⟩ is a *K = r*-fold eigenstate superposition and a true
eigenstate is *K = 1*, one can interpolate continuously between
eigenstate QPE and Shor by running phase estimation on a *K*-fold
superposition, with circuit, metric, noise, and cost held fixed. The
control–work entanglement entropy is then exactly **log₂ K** bits.

The early hypothesis in this project was that Shor/QPE differences were
caused by which-path dephasing through this entanglement. The
interpolation experiment (`interpolation_experiment.py`) measures the
effect at ≈ **−0.025 signal per bit** — real, reproducible in all four
noise/cost conditions, and *an order of magnitude too small* to explain
the ≈ 0.5 gap it was built to explain. **Hypothesis falsified.**

It is in this textbook because chasing that failure is what exposed grid
alignment (§10), which overturned the study's original conclusion. Read
`docs/MECHANISM.md` for the narrative.

### 7.5 Benchmark instances

| N | a | r | why |
|---|---|---|---|
| 15 | any | 1,2,4 | **pathological — do not use.** Multiplicative group is Z₂ × Z₄, so *every* order is a power of two |
| 21 | 2 | 6 | unbiased; mild residual tilt *toward* the qubit (0.267 vs 0.300) |
| 29 | 16 | 7 | **exactly alignment-neutral** across d = 2,3,5 (0.2857 each) — the recommended benchmark |
| 33, 55 | various | 5, 10 | within-modulus alignment controls (§10.3) |

---

## 8. Continued fractions

### 8.1 The algorithm

Every real x ∈ (0,1) has an expansion

    x = 1/(a₁ + 1/(a₂ + 1/(a₃ + ⋯)))  =: [0; a₁, a₂, a₃, …]

with a_i positive integers, obtained by repeated `x ← 1/x − ⌊1/x⌋`. It
terminates iff *x* is rational. The truncations p_k/q_k are the
**convergents**, computed by the recurrences

    p_k = a_k p_{k−1} + p_{k−2},   q_k = a_k q_{k−1} + q_{k−2}

with p_{−1}/q_{−1} = 1/0 and p_0/q_0 = 0/1. Convergents are automatically
in lowest terms (p_k q_{k−1} − p_{k−1} q_k = (−1)^{k−1}).

### 8.2 The two theorems we need

**(Best approximation.)** |x − p_k/q_k| < 1/(q_k q_{k+1}) ≤ 1/q_k².

**(Legendre's converse — the one Shor uses.)** If gcd(p,q) = 1 and

    |x − p/q| < 1/(2q²)

then p/q **is** a convergent of *x*.

### 8.3 Applying it to order finding

Phase estimation returns *y* with y/D within 1/(2D) of some s/r
(the nearest-grid-point guarantee). For Legendre's converse to fire we
need

    1/(2D) < 1/(2r²)   ⟺   D > r².

Since r < N, taking **D ≥ N²** is sufficient — the textbook requirement.
Then s/r in lowest terms is a convergent of y/D, and reading off its
denominator gives *r* (up to the divisor subtlety of §8.4).

The demo registers used here (*D* = 64–125 against *N* = 21) are
deliberately **below** D ≥ N². That is not sloppiness: it is what makes
the random-outcome floor non-negligible and forces the floor-corrected
metric of §20. All bases are held to the same rule, and the scaling
sweeps run far above N².

### 8.4 Divisor recovery vs returning *r* itself

Careful: Legendre's converse certifies the **reduced** fraction
(s/g)/(r/g) with g = gcd(s,r). Its denominator r̃ = r/g is a *divisor*
of *r*, not *r*. Standard analyses (Shor's 4/π², Gerjuoy, Bourdon–
Williams, Ekerå, Magdon-Ismail–Dong) therefore certify divisor recovery
and lift r̃ to *r* by a classical search over multiples.

This repo's decoder does something different, and the difference is the
subject of §11–§12:

> **The decoder.** On outcome y ∈ [1, D), scan the convergents p/q of
> y/D in order of increasing denominator. At the **first** q ≤ N with
> a^q ≡ 1 (mod N), return the least r′ dividing q with a^{r′} ≡ 1
> (mod N). If no convergent denominator q ≤ N passes, **reject**.
> (y = 0 is always rejected.)

It performs no lift. It succeeds precisely on the convergent
denominators that are *already* multiples of *r* — including deep ones,
2r, 3r, …, ⌊N/r⌋r, that lie outside any sufficient-condition window.
That is why it has an exact acceptance set with a closed form, and why
that form is a **totient sum** rather than a window count.

---

## 9. Grover search in base d

### 9.1 The algorithm

Over *M = dⁿ* items with one marked item |t⟩, alternate

    oracle:    O = 𝟙 − 2|t⟩⟨t|
    diffuser:  Dif = 2|ψ⟩⟨ψ| − 𝟙,   |ψ⟩ = uniform superposition

for ⌊(π/4)√M⌉ iterations. In the two-dimensional span{|t⟩, |ψ⟩ − …}
each iteration rotates by θ = 2 arcsin(1/√M), and the iteration count is
just π/(2θ) rounded.

### 9.2 Why it is in this paper

Grover is the **falsification test** for the mechanism, chosen with the
prediction registered in the source *before* the runs: *qudits win, by
less than in phase estimation.*

The logic: the iteration count √M is **base-independent**, so Grover
holds the *oracle count* fixed across bases. Its only compression comes
from narrower multi-qudit decompositions — roughly **half** of Shor's
exposure compression (5.7× vs 10.9× from d = 2 to d = 5). If the qudit
advantage were pure depth, Grover would show none. If it were pure
width, Grover would show all of it.

Measured: Grover's advantage is **0.33–0.50 of Shor's**. So halving the
compression costs one-half to two-thirds of the advantage — compression
is the mechanism, and the response is at least proportional.

### 9.3 Grover as a methodological control

Grover has no order, no continued fractions, and an exact 1/M random
floor. Therefore:

- **Grid alignment is structurally impossible** for it. Its agreement
  with the Shor ordering rules out the continued-fraction metric as the
  source of the effect.
- **Its "decoder" is the identity** — the signal *is* marked-state
  survival. This is what makes it the clean baseline in §14: Grover's
  fidelity equals its signal to within 0.006 (ladder) and 0.025
  (depolarizing) at every point, while Shor's does not.

### 9.4 The size-matching trap

M = dⁿ never matches across bases (8, 9, 25, …). Comparing raw
demo-size points **reverses orderings**. All cross-base comparisons here
interpolate each base's results onto a common log₂-size axis. This is
the second of the paper's two fairness traps; alignment is the first.

Also: the multi-qudit oracle and reflection are applied as exact
unitaries but **charged their (n−1)-layer decomposition depth**.
Charging them one layer would hand the largest free ride to whichever
base packs the most carriers into the gate — which is *d = 2*.

---
---

# Part III — The number theory

This part and Part IV contain the derivations original to this work.

## 10. Grid alignment

### 10.1 The observation

Phase estimation concentrates probability on the phases s/r. Two regimes:

- **If r | D** (= dᵐ), every s/r is *exactly* a grid point y/D. By
  §6.2 property 1, P(y) = 1: the peaks are delta functions, and delta
  functions are maximally robust to noise.
- **If r ∤ D**, the peaks smear over neighbouring outcomes according to
  the Fejér kernel, and smeared peaks degrade far faster under
  decoherence.

**Which base receives the sharp peaks is decided by arithmetic, not
physics.** And because prior qudit studies all work at fixed *d*, where
alignment is a constant, the confound is invisible in the literature.

### 10.2 The N = 15 pathology

(Z/15)* ≅ Z₂ × Z₄, so every element has order 1, 2, or 4 — **every order
is a power of two.** A base-2 control register always lands exactly on
grid; bases 3 and 5 never do. Any cross-dimension comparison run on
*N* = 15 — including the first version of this study — hands base 2 a
structural gift that has nothing to do with decoherence.

This is what produced, and then destroyed, the original "qubits win Shor
on transmons" finding.

### 10.3 Quantifying it

Define the **residual misalignment** of base *d* on instance (N, r):

    mean over s = 1…r−1 of  dist( D·s/r mod 1 , 0 )

i.e. the mean distance of the target phases to the nearest grid point,
in grid units. 0 = perfectly aligned, 0.5 = worst case.

Three measurements price it:

| test | what it isolates | result |
|---|---|---|
| one instance per alignment class (r = 3,4,5,6,7) | does alignment predict the winner? | **6 for 6** on biased runs (3 instances × 2 noise models) |
| within-modulus control (N = 33, 55: r = 5 vs r = 10 on *identical* registers) | alignment at fixed width, depth, exposure | costs the ququint **0.14–0.22** signal; residual physical lead **0.38–0.57** |
| full multiplicative-group ensembles (all a ≠ 1 at N = 21, 33, 55) | what a real Shor user samples | qudit ordering preserved; aligned-over-unaligned excess **+0.18 to +0.19**, independently reproducing the ≈ 0.2 price |

So: alignment is worth **≈ 0.2 signal** to whoever receives it, and the
remaining qudit lead is physical. Both effects are real, and separating
them is the point.

### 10.4 The converse control does not exist

You cannot build the mirror-image test (a base-2-aligned instance with a
usable metric). At every modulus large enough to carry both r = 4 and a
non-power-of-two order, the r = 4 continued-fraction **random floor
exceeds its noiseless baseline**, collapsing the metric (§20). *N* = 15
is the only qubit-aligned instance with usable dynamic range — which is
itself worth knowing. Consequence, stated honestly in the paper: the
≈ 0.2 price is measured only in the ququint-aligned direction.

### 10.5 Alignment cannot drift with register size

A referee objection to the scaling sweeps: *D = dᵐ* changes with *m*, so
maybe the qutrit's shallow slope is alignment drifting favourably.

It is not, and the reason is arithmetic. The multiset of grid offsets
{D·s/r mod 1 : s = 1…r−1} depends only on **D mod r**, and
D = dᵐ mod r is **periodic in m** (with period the multiplicative order
of *d* mod *r*, or eventually periodic if gcd(d, r) ≠ 1). So the offsets
simply repeat as the register grows.

Measured (`misalignment_scaling.py`): residual misalignment is exactly
constant across the entire sweep for all three bases on both instances —
0.267 (d=2) and 0.300 (d=3,5) at *N* = 21; 0.2857 for **every** base at
*N* = 29 — constant to a spread < 10⁻¹¹, i.e. floating-point noise on
exactly equal values. Alignment can therefore explain neither a
size-dependent nor a size-independent component of the signal.

---

## 11. The decoder acceptance lemma

Everything in §12 rests on reducing the decoder to a purely
number-theoretic predicate. That reduction is the following lemma, which
is proved in the paper's Appendix A and verified computationally on 42
(instance, D) combinations.

> **Lemma.** The decoder of §8.4 returns the order *r* of *a* mod *N*
> **if and only if** some convergent denominator *q* of y/D satisfies
> *q* ≤ *N* and *r* | *q*. On every other outcome it rejects. In
> particular it never returns a wrong order.

**Proof.** Since *r* is the multiplicative order of *a* mod *N*, we have
a^q ≡ 1 (mod N) **iff** r | q. This is the only number theory needed.

(⇐) Suppose some convergent denominator q ≤ N is a multiple of *r*. The
scan stops at the first such *q*. Every divisor r′ of *q* with
a^{r′} ≡ 1 is itself a multiple of *r*; and *r* both divides *q* and
passes the test. Hence the least such r′ is exactly *r*.

(⇒) If no convergent denominator q ≤ N is a multiple of *r*, the test
a^q ≡ 1 never fires, and the decoder rejects. ∎

**Why this matters.** The lemma converts a question about a *program* —
"what does this decoder accept?" — into a question about the continued
fraction expansion of y/D, which is classical number theory. It also
establishes that the decoder is *sound*: it never returns a wrong order,
so every accepted outcome is a true success and the acceptance set is
exactly the success set.

**Verification.** `decoder_formula.py` enumerates the decoder over every
outcome y ∈ [0, D) and compares against the convergent predicate,
obtaining **bit-identical acceptance sets** on 42 (instance, D)
combinations: six instances (N = 21, 29, and the four within-modulus
orders of N = 33, 55) across seven control dimensions each.

---

## 12. The decoder acceptance law

### 12.1 The question

Define the acceptance set

    A = { y ∈ [0, D) : decode(y) = r }.

How large is it, and how does it grow?

The naive estimate: the sufficient-condition window around each of the
r − 1 peaks spans 1/r² in phase, holding ~D/r² outcomes, for
|A| ≈ (r−1)D/r². We will see this is *wrong in both variables* and
right on the benchmark instance only by accident.

### 12.2 Measure it first

`decoder_scaling.py` runs the project's own continued-fraction routine
over every outcome and counts exactly. No simulation is involved.

| d | m | D | \|A\| | per peak | D/r² | law (§12.5) |
|---|---|---|---|---|---|---|
| 2 | 6 | 64 | 8 | 1.6 | 1.8 | 1.8 |
| 2 | 8 | 256 | 36 | 7.2 | 7.1 | 7.2 |
| 2 | 10 | 1024 | 148 | 29.6 | 28.4 | 28.9 |
| 2 | 12 | 4096 | 582 | 116.4 | 113.8 | 115.7 |
| 3 | 4 | 81 | 10 | 2.0 | 2.2 | 2.3 |
| 3 | 5 | 243 | 36 | 7.2 | 6.8 | 6.9 |
| 3 | 6 | 729 | 100 | 20.0 | 20.2 | 20.6 |
| 3 | 7 | 2187 | 308 | 61.6 | 60.8 | 61.8 |
| 5 | 3 | 125 | 16 | 3.2 | 3.5 | 3.5 |
| 5 | 4 | 625 | 88 | 17.6 | 17.4 | 17.6 |
| 5 | 5 | 3125 | 442 | 88.4 | 86.8 | 88.2 |

Read the "per peak" column: **1.6 accepted outcomes at D = 64 growing to
116 at D = 4096** — a 73× gain in decoder tolerance against an
interference peak that, by §6.2 property 3, **never widens**.

That single contrast is the mechanism behind Shor's plateau (§21.3):
noise-induced broadening grows only polynomially in *m* (exposure =
carriers × layers), while the acceptance set grows **linearly in D**,
i.e. *exponentially in m*. The decoder's redundancy outpaces the added
exposure over a range of sizes.

### 12.3 The structure of A

By the lemma, y ∈ A iff some convergent denominator of y/D is an
**admissible** denominator, meaning a multiple of *r* that is ≤ *N*:

    admissible denominators:  r, 2r, 3r, …, ⌊N/r⌋ r

The classical fact we need is about which real numbers have a given
fraction among their convergents:

> For a reduced fraction p/q with penultimate convergent p′/q′, the set
> of x whose convergents include p/q is the **open interval between the
> Stern–Brocot mediants**
>
>     (p + p′)/(q + q′)   and   (2p − p′)/(2q − q′).

To count without double-counting, partition outcomes by the **first**
admissible convergent of y/D. This is genuinely disjoint, and the reason
is a small gcd argument: the side denominator q − q′ is never a multiple
of *r*, because gcd(q′, q) = 1.

Summing the interval **counts** over admissible denominators reproduces
the enumerated |A| **without error** — outcome for outcome, on all 27
instance/size combinations tested, including all four within-modulus
orders.

### 12.4 From counts to measure

For a reduced p/q, the mediant interval has length

    μ(q) = (2/q) Σ_{u < q, gcd(u,q) = 1} 1/(q + u)

(summing over the φ(q) numerators u coprime to q). Approximating the sum
by an integral — the coprime residues are equidistributed with density
φ(q)/q —

    Σ_{u<q, gcd(u,q)=1} 1/(q+u)  ≈  (φ(q)/q) ∫_q^{2q} dt/t  =  (φ(q)/q) ln 2

so

    μ(q) → 2 ln 2 · φ(q) / q².

**Sanity check against a classical theorem.** Summed over *all*
denominators q ≤ Q, this weight must reproduce the almost-everywhere
count of convergent denominators below *Q*. Using Σ_{q≤Q} φ(q)/q² ≈
(6/π²) ln Q,

    Σ_{q ≤ Q} μ(q) → 2 ln 2 · (6/π²) ln Q = (12 ln 2 / π²) ln Q,

which is exactly Khinchin's count. **The measure itself is classical.**
The content of the law below is its *restriction to the denominators the
decoder admits*.

### 12.5 The law

Restricting the sum to admissible denominators q = kr ≤ N:

    ┌─────────────────────────────────────────────────────┐
    │   |A| / D  ⟶  2 ln 2 · Σ_{k=1}^{⌊N/r⌋} φ(kr)/(kr)²  │
    └─────────────────────────────────────────────────────┘

with φ Euler's totient. This is Eq. (5) of the paper.

**Accuracy.** Better than 1% on five of six instances at D ≫ N²; 4.2% on
the sixth (N = 55, r = 5, where eleven admissible denominators make the
first-admissible exclusions largest). The exact finite-D form (interval
counts rather than measures) reproduces |A| with **zero** error at every
size.

### 12.6 What the law settles

**Scaling in D — exactly linear.** Measured |A| ∝ D^{1.03 ± 0.01}
(R² = 0.999); the small excess over slope 1 is purely window
discreteness.

**Scaling in r — the 1/r² envelope is wrong.** Comparing r = 5 with
r = 10 on identical registers (the within-modulus pairs, swept to
D ≥ 5r² so windows exceed one outcome): measured per-peak ratios **9.6**
(N = 33) and **8.9** (N = 55), where 1/r² predicts **4.0**. The law's
totient-sum ratios: **9.7** and **9.3**. The "9.5× mystery" was never a
mystery — it is the totient sum.

**Why the envelope looked fine on the benchmark.** At r = 6, N = 21 the
naive (r−1)/r² = 0.139 sits within 2% of the law's 0.141 because **two
errors compensate**: the true q = r window measure 2 ln 2 · φ(6)/36 =
0.077 is only 0.55× the envelope's, and the admissible multiples q = 12,
18 restore the difference. On the r = 5 instances, where the
cancellation fails, the envelope is off by **2.5–3×** while the law
holds to 4.2%.

**The decoder decides scorability before noise enters.** At N = 55 the
modal order class is r = 20 (16 of 39 units). For d = 2 at D = 64 the
acceptance set is *empty* — the noiseless baseline is exactly zero.
No amount of coherence helps.

### 12.7 The consequence that matters for the paper

Eq. (5) depends only on **r and N** — not on *d*, not on the base.

> At matched control dimension, the decoder's error tolerance is
> **identical across bases**. Therefore the entire cross-base difference
> in decoded success sits in the **quantum state**.

That is what upgrades the mechanism section from a plausible story to a
quantitative account: the classical half of the pipeline is solved
exactly and is base-blind, so whatever difference remains is physics.

### 12.8 A general lesson for benchmarking

A decoded success probability conflates two things with different
physics:

1. the decay of the quantum state — universal, described by
   damage-weighted exposure (§14);
2. the error tolerance of the classical post-processing — **algorithm
   specific, and it can grow with problem size.**

Any benchmark of "noise resilience" across algorithms or encodings that
uses decoded success as its metric is therefore partly measuring
**classical decoder redundancy**. Reporting end-state fidelity alongside
decoded signal separates the two at zero extra simulation cost. The
paper recommends this as standard practice.

---
---

# Part IV — Open quantum systems

## 13. Density matrices, CPTP maps, and the superoperator

### 13.1 States

A mixed state is a density matrix ρ with ρ = ρ†, ρ ≥ 0, tr ρ = 1. For a
register of *n* carriers of dimension *d*, ρ acts on ℋ = (ℂ^d)^{⊗n} of
dimension dⁿ — so an exact density-matrix simulation costs O(d^{2n})
memory. That wall is at dim ℋ ≈ 3000 here; beyond it we use
trajectories (§18).

### 13.2 Channels

A physical evolution is a **CPTP map** (completely positive,
trace preserving), equivalently a **Kraus decomposition**

    E(ρ) = Σ_i K_i ρ K_i†,     Σ_i K_i† K_i = 𝟙.

Complete positivity is checkable via the **Choi matrix** J(E) =
(E ⊗ 𝟙)(|Ω⟩⟨Ω|): E is CP iff J(E) ≥ 0. This repo tests CP and TP for
every channel by computing Choi eigenvalues — one of the 20 correctness
tests.

### 13.3 Continuous time: the Lindblad equation

For Markovian evolution,

    dρ/dt = −i[H, ρ] + Σ_k ( L_k ρ L_k† − ½{L_k† L_k, ρ} )

with **jump operators** L_k. Here H = 0 in the rotating frame (all
dynamics is in the gates), so the channel is pure dissipation. One layer
of noise is exp(𝓛 · t_layer), **exponentiated exactly** rather than
Trotterized.

### 13.4 The superoperator, and fractional layers

Vectorizing ρ gives the **natural representation** S, a d² × d² matrix
with E(ρ) ↔ S vec(ρ). Two facts are used constantly:

- Both channel families here form **one-parameter semigroups**, so a
  gate costing a fractional number of layers *t* is applied exactly:
  scale the Lindblad rate (ladder) or set 1 − q = (1 − p)^t
  (depolarizing). Fractional gate costs are **exact**, not approximated.
- tr S has direct physical meaning — the next section.

---

## 14. Damage units: entanglement fidelity as the currency

### 14.1 The problem with counting events

"Exposure = carriers × layers" counts *events*. But one noise event does
*d*-dependent harm: a ququint sitting in a ladder channel for one layer
loses far more than a qubit does. Counting events therefore compares
apples to oranges across bases.

### 14.2 The right currency

Define the **entanglement fidelity** of the one-layer channel:

    F_e = tr S / d²

where S is the one-layer superoperator in the natural representation.
For Kraus operators {K_i} this is

    F_e = Σ_i |tr K_i|² / d²,

the fidelity of the channel with respect to the maximally entangled
state. The **damage** per carrier-layer is

    1 − F_e.

Then define

    damage-weighted exposure = (carriers × layers) × (1 − F_e).

### 14.3 The numbers

| channel | 1 − F_e | d = 2 | d = 3 | d = 5 |
|---|---|---|---|---|
| calibrated ladder, strength *s* | — | 0.75 s | 1.46 s | 2.82 s |
| depolarizing, strength *p* | p(1 − 1/d²) | 0.75 p | 0.89 p | 0.96 p |

A ququint takes **~4× a qubit's damage per event** on the ladder — and
almost exactly the same damage per event under depolarizing. That
contrast explains most of the difference between the two channels'
verdicts throughout the paper.

Deriving the depolarizing entry: for E(ρ) = (1−p)ρ + p 𝟙/d, the identity
part contributes (1−p)·d² to tr S and the fully depolarizing part
contributes p·1, so F_e = (1−p) + p/d² and 1 − F_e = p(1 − 1/d²). ∎

### 14.4 The collapse test — and what it does *not* prove

Re-plot everything with damage-weighted exposure on the abscissa.
Grover's three bases then collapse onto a single exponential: per-family
decay rates **0.44 / 0.49 / 0.43** (a 1.1× spread, against 3.6× in event
units), each family log-linear with R² ≥ 0.996.

Pooling *both* algorithms, all bases and sizes:

| ordinate | abscissa | ladder R² | depol. R² |
|---|---|---|---|
| signal | exposure × strength | 0.67 | 0.79 |
| signal | exposure × damage | 0.81 | 0.79 |
| **fidelity** | **exposure × damage** | **0.97** | **0.99** |

**Now the honest reading, and this is important.** For a product of
near-identity incoherent channels, log-fidelity is **additive** in the
per-application entanglement infidelity to first order. So a single
exponential with fitted amplitude ≈ 1 is the **null expectation**, not a
discovery. The paper says so explicitly, and bounds the claim two ways:

- Rescored in **log** fidelity — the metric that weights the deep tail —
  the same fit gives R² = 0.76 in both channels (0.85–0.91 if refit
  there). See `logfid_rescore.py`.
- The law holds within a factor of two down to fidelity 1.5 × 10⁻² on
  the ladder and, excepting one floor-pinned Grover point, to
  2.7 × 10⁻⁴ under depolarizing. Every departure is a Grover point
  approaching its 1/dim ℋ fidelity floor.

**The law's failure mode is error that does not compose incoherently.**
Correlated or coherent noise breaks the additivity — and that is
precisely what the deep hardware circuit exhibits (§21.5). This is why
the law is stated for Markovian incoherent channels only.

### 14.5 The residual *is* the decoder

What no channel-level argument predicts is the residual. With units
fixed, a nested fit gives one shared amplitude with a
**per-algorithm** decay rate at R² = 0.93/0.94. The split is stark:

- **Grover** is a textbook exponential in damage. Its fidelity equals
  its signal to within 0.006 (ladder) / 0.025 (depolarizing) at every
  point — because its decoder is the identity.
- **Shor at d = 3** holds a flat signal of ≈ 0.73 while its exposure
  triples and it loses two thirds of its fidelity (0.55 → 0.18).
- At **d = 2, m = 12** under depolarizing, continued fractions decode a
  signal of 0.131 ± 0.018 from a state with fidelity **3 × 10⁻⁴** to the
  ideal.

So the mechanism claim, in the form the data support:

> **Accumulated channel damage is the law for the quantum state; the
> residual algorithm dependence of decoded success sits in the
> decoder** — for which §12 gives an exact, base-independent account.

---

## 15. The calibrated ladder channel

### 15.1 What a transmon is, in one paragraph

A transmon is a weakly anharmonic oscillator: a Josephson junction
shunted by a large capacitor, with level spacings E_{k+1} − E_k
decreasing by the anharmonicity α ≈ −200 to −300 MHz. The lowest two
levels are the qubit; levels 2, 3, … are the qudit. Because it is nearly
harmonic, higher levels relax and dephase **faster** — the "ladder"
structure. Full background in `docs/TRANSMON.md`.

### 15.2 The textbook model is wrong — in both exponents

Naive expectations, from a harmonic oscillator and from flux-noise
arguments:

    relaxation   Γ_k ∝ k          (bosonic enhancement)
    dephasing    Γ_φ(j,k) ∝ (k − j)²   (frequency-difference squared)

Both are contradicted by measurement, and — this is the point —
**both in the direction of over-penalizing qudits**:

| quantity | textbook | measured |
|---|---|---|
| Γ₂/Γ₁ | 2.0 | **≈ 1.7** |
| Γ_φ^{01} : Γ_φ^{12} : Γ_φ^{02} | 1 : 1 : 4 | **1 : 2.0 : 2.3** |

The measured dephasing ratios are flatly incompatible with a
(Δlevel)² law: the 0↔2 pair should be 4× the 0↔1 pair and is only 2.3×,
while the 1↔2 pair should equal the 0↔1 pair and is twice it. The
physical reason is charge dispersion — the charge dispersion of |2⟩
exceeds that of |1⟩ by an **order of magnitude**, so dephasing tracks
the *higher* level involved, not the gap.

### 15.3 The calibrated replacement

Fits to published per-level coherence data spanning **nine devices and
d = 3 to 12**:

    relaxation:  Γ_k ∝ k^{0.7}
    dephasing:   Γ_φ(j, k) ∝ max(j, k)^{1.1}      ← a max-level law

Our channel reproduces the measured ratios as **1.62** and
**1 : 2.14 : 2.14**.

**Normalization matters.** Rates are set so the 0↔1 subspace is
bit-for-bit identical to the qubit channel. *Every* difference between
bases is therefore purely a higher-level effect — there is no hidden
overall-rate advantage handed to either side.

### 15.4 The dephasing knob

A single scale factor on the dephasing term interpolates from free
evolution to perfect echo. It does double duty:

- it models the **high-E_J/E_C regime** demonstrated at d = 12, where
  echo coherence approaches the T₁ limit;
- it models **refocused (dynamically decoupled) operation**, which is
  how any real transmon runs a long circuit.

The knob is consequential. Under linear-in-*d* gate cost the ququint
**loses** Shor without echo (−0.026) and **wins** with it (+0.191); QPE
moves from exact parity to +0.196. Mechanistically this is expected:
dynamical decoupling suppresses dephasing — the part of the ladder
scaling worst with *d*, via the max-level law — and leaves the gentler
k^{0.7} relaxation. Refocusing buys **roughly one cost model of
headroom**, which is why the paper's condition is stated "at the
device's operating dephasing level."

### 15.5 The four named regimes

Appearing in every figure:

1. **idealized ladder** — Γ_k ∝ k, (Δlevel)² dephasing. The textbook
   model, used **only as a bound**.
2. **calibrated ladder** — §15.3. The honest transmon model.
3. **low-charge-dispersion** — the knob set to the high-E_J/E_C regime.
4. **per-particle depolarizing** — §17.

---

## 16. Realizing a dephasing matrix exactly: Euclidean embedding

A pretty result, and the reason the max-level law can be modelled at all.

**Problem.** Given a target *d* × *d* matrix of pairwise dephasing rates
Γ_φ(j,k), find diagonal jump operators realizing it exactly.

**Setup.** With diagonal jumps {J^{(1)}, …, J^{(L)}}, collect the *j*-th
diagonal entries across jumps into a vector

    v_j = ( J^{(1)}_{jj}, …, J^{(L)}_{jj} ) ∈ ℝ^L.

The Lindblad equation then gives the coherence ρ_{jk} the decay rate

    Γ_φ(j, k) = ½ ‖ v_j − v_k ‖².

**Recognition.** This is a **Euclidean embedding problem**: find points
v_j in ℝ^L whose pairwise squared distances match 2Γ_φ. That is exactly
what **classical multidimensional scaling** solves — double-centre the
squared-distance matrix, eigendecompose, take the positive spectrum.

**Result.** The measured max-level law is realized *exactly*, with
residual ≤ 3 × 10⁻¹⁷ for d = 2…7. No linear-frequency-ladder model can
do this: a frequency ladder forces v_j = (f_j) collinear in ℝ¹, which
can only produce Γ_φ ∝ (f_j − f_k)² — a (Δlevel)²-type law, precisely
the one the data reject.

---

## 17. Depolarizing, and the Zeeman failure mode

### 17.1 The per-particle depolarizing convention

    ρ ⟶ (1 − p) ρ + p 𝟙/d       per carrier, per layer

Same *p* for every *d*. This is the trapped-ion-like channel, and the
convention rests on measured structure, not convenience:

- every qudit level in the encoding is ground-state or metastable
  (τ₁ ~ 1.1 s, orders of magnitude beyond gate times);
- allowed-transition magnetic sensitivities span only ~5×;
- single-qudit per-pulse error is **nearly flat in d**: 2.0 × 10⁻⁴ at
  d = 3 and 3.2 × 10⁻⁴ at d = 5;
- qudit control is demonstrated to 13 levels.

Note from §14.3 that this channel's damage is nearly flat in *d*
(0.75p → 0.96p), which is why it is the qudit-friendly channel.

### 17.2 The sharpest failure mode found

The per-particle convention **flattens pair structure the ion encoding
really has.** So the paper tests the worst case: magnetic-field
dephasing carrying the collective-*B* sensitivity structure of the
⁴⁰Ca⁺ S_{1/2}/D_{5/2} level indexing, realized exactly by a single
diagonal jump ∝ diag(g_j m_j) with g_S = 2, g_D = 6/5, normalized so the
optical-qubit pair 0↔1 matches the qubit channel.

Pair rates then span **1–25×** the reference at d = 3 and **1–49×** at
d = 5.

**The encoding is no strawman.** Over all C(8, d) level subsets of the
manifold, the chosen levels *exactly minimize* the worst pair rate at
d = 5 and d = 7; only d = 3 admits a gentler choice (9×, via
{S_{−1/2}, D_{−3/2}, D_{−1/2}}).

**The verdict reverses outright:**

| dephasing structure | d = 2 | d = 3 | d = 5 |
|---|---|---|---|
| per-carrier Zeeman | **0.72** | 0.24 | 0.23 |
| common-mode Zeeman | **0.87** | 0.45 | 0.34 |

The qubit wins at every strength under **both** cost models. Nor is the
missing correlation structure doing the work: genuinely common-mode
dephasing (one global jump coupling to the total Zeeman shift, exact as
an elementwise mask on ρ) preserves the reversal — its
decoherence-free pairs soften every base, the qubit most.

**Unmitigated Zeeman-structured dephasing on a sensitivity-ordered
encoding is a regime with no qudit advantage at all.** The condition's
"operating dephasing level" clause must be read to include it.

### 17.3 The price of mitigation

Measured devices are engineered away from this regime (shielding gives
~100 ms coherence across transitions), and the device's randomized
benchmarking — per-pulse error rising only 1.6× from d = 3 to d = 5
where the raw sensitivity ratio is 25–49 — is consistent with a
near-flat residual. But a few-microsecond pulse cannot resolve slow
dephasing; the direct evidence needed is *d*-resolved Ramsey or echo
coherence across the encoding's transitions.

Pending that, the paper prices the failure. Composing the Zeeman
component with the depolarizing operating point (the two channels
commute, so the product is exact) and sweeping the suppression factor ε
applied to the unmitigated reference, the qudit ordering returns at

    ε* = 0.58–0.79   under native-gate (`uniform`) cost
    ε* = 0.09–0.15   under 2(d−1) Mølmer–Sørensen (`ion`) cost

In hardware units: a 0↔1-pair coherence of **≳ 400–600 layer times** for
native-gate cost and **≳ 2200–3800** for MS cost. At ~100 μs layers, a
100 ms shielded coherence meets the native-gate bar with a factor-two
margin but **falls short of the MS-cost bar by 2–4×.**

This is the single most consequential caveat in the paper, and it is why
§21.6 recommends the transmon route as the *robust* one even though ions
offer the larger headline gains.

---

## 18. Quantum trajectories

Exact density-matrix evolution costs O(d^{2n}) and dies around
dim ℋ ≈ 3000. To reach 5.3 × 10⁵ we use the **Monte Carlo wavefunction**
(quantum trajectory) method.

**The method.** Evolve a pure state |ψ⟩. After each gate, each carrier
independently passes through the per-layer channel raised to the gate's
cost; one Kraus operator K_i is sampled with probability
tr(K_i† K_i ρ_q) from that carrier's *reduced* state, applied, and
renormalized. Averaging |ψ⟩⟨ψ| over trajectories reproduces the channel
**exactly** — this is a theorem, not an approximation.

**Why the statistics are better than they look.** Each trajectory
contributes its **full outcome distribution**, not a single sampled
shot. Statistical error is therefore well below the Bernoulli rate you
would guess from the trajectory count.

**Fidelity estimation.** End-state fidelity is estimated as the
trajectory average of |⟨ψ_ideal|ψ⟩|², an unbiased estimator of
⟨ψ_ideal|ρ|ψ_ideal⟩, cross-checked against exact density matrices.

**Statistics actually used.** 1000 trajectories per Shor and QPE scaling
point; 400 for the N = 29 instance-robustness sweep (200 at the three
deepest configurations); 400 for grid-alignment and within-modulus
studies; 1000 for the eigenstate-interpolation study and the d = 7 demo
grid; 200 for the fidelity-collapse Shor points (100 at d = 2, m = 12).
Demo-size cost, SPAM, and refocusing results use exact density matrices
throughout.

---
---

# Part V — The accounting, and the result

## 19. Exposure, cost models, and break-even

### 19.1 The exposure convention

Stated once, precisely, because every number in the paper depends on it:

> One layer of noise is applied to **every** carrier for **every** layer
> of the serial schedule. A gate spanning *k* carriers occupies its
> decomposition depth in layers, so **idling carriers decohere while
> gates execute.**

    exposure = carriers × layers
    damage-weighted exposure = exposure × (1 − F_e)

The schedule is **serial** — every carrier idles during every gate —
matching single-addressed ion strings. Platforms that execute gates
concurrently would cut idle exposure most for the *widest* register,
i.e. for d = 2, softening the qudit advantage. This is disclosed as a
limitation.

### 19.2 The break-even criterion

Janković *et al.* derive, by linear response over Haar-random gates
under pure dephasing, the critical **gate-efficiency ratio** a qudit
register must clear to beat a qubit register:

    ratio* = (d² − 1) / (3 log₂ d)

Evaluated: **1.68** (d = 3), **3.45** (d = 5), **5.70** (d = 7). Compare
the folklore value O(d²/log₂ d) = 5.7, 10.8, 17.5 — the true bar is
**three times lower** than commonly assumed.

Reading this repo's layer-count ratios as gate-efficiency ratios, the
gate-level criterion predicts the algorithm-level winner in **seven of
nine** cost/dimension cases on the ladder channel, including the tight
one (d = 5 `uniform` clears 3.45 at 3.80, and wins). Both misses (d = 3
`ion`; d = 7 `uniform`) are in the **conservative direction** their
pure-dephasing assumption predicts — our calibrated relaxation is
gentler (k^{0.7}).

**Independent validation.** The three central equations of that paper —
qudit and multi-qubit process infidelities and the critical curve — are
reproduced from this repo's superoperator code with no analytics of our
own, to a worst relative error of **4.1 × 10⁻⁴** over d = 2…64. The
residual is identified as their first-order truncation (it tracks the
infidelity itself). See `jankovic_check.py`.

### 19.3 The noise-inflation threshold

The channels charge every base the same per-layer strength. If higher-*d*
gates are *additionally* noisier per layer, the condition acquires a
threshold. Inflating the qudit's strength alone, s_d = f · s₂, and
locating the crossing f* where the qudit's signal falls to the qubit's:

| cost model | channel | f* |
|---|---|---|
| `uniform` | calibrated ladder | 2.0–2.5 |
| `uniform` | depolarizing | 2.6 (d=3) – 4.5 (d=5) |
| `ion` | calibrated ladder | 1.2 (d=3); ququint cell already lost at f = 1 |
| `ion` | depolarizing | 1.6 (d=3, 5) |

**Read as hardware guidance:** a platform keeps the qudit advantage
while its measured qudit-to-qubit per-gate noise ratio stays below f*
**after** the layer-count multiplier is charged — roughly 1.6× for
today's trapped-ion pairing and 2.0–2.5× for a native-entangler
transmon.

---

## 20. The success metric

### 20.1 Why raw success probability is not usable

Continued fractions "succeed" on a substantial share of **uniformly
random** outcomes. The random floor is 0.12–0.13 on the *N* = 21
benchmark at demo size, 0.20–0.26 on *N* = 29, and up to **0.59** on
small-order instances — at r = 2 it reaches 0.72–0.80, *meeting or
exceeding the noiseless baseline*.

### 20.2 The floor-corrected signal

    signal = (success − floor) / (success_noiseless − floor)

= 1 for perfect interference, 0 for random guessing, **negative** when
noise actively biases outcomes away from the answer. Floors and
noiseless baselines are recomputed for every base, size, and
readout-error setting.

### 20.3 The span rule

Small orders compress the metric's dynamic range, so any instance used
for a quantitative comparison must have

    floor-to-baseline span > 0.15.

The paper discloses one grandfathered exception (the r = 3 aligned
instance, span 0.07–0.12), retained because no other instance represents
its alignment class — and quotes **no signal magnitudes** from it, only
winner margins.

This rule has teeth: it is why *every* base-2-aligned order class at
N = 21, 33, 55 is unscorable, and why the converse alignment control of
§10.4 cannot be built.

### 20.4 Readout error, and a structural cancellation

A *d*-level readout must resolve *d* pointer states, the higher ones
worst. Charging a readout channel with misread rate of |k⟩ growing as
(1 + k) on every control carrier leaves the qudit advantage untouched —
the ququint's lead drifts by < ±0.03 over ε = 0…0.04.

The reason is arithmetic, not luck. Mean misread rate over levels is
ε(d+1)/2, and total readout exposure is m × ε(d+1)/2. At matched
precision m ≈ log D / log d, giving at D ≈ 64:

    d = 2:  6 × 1.5ε = 9ε
    d = 3:  4 × 2.0ε = 8ε
    d = 5:  3 × 3.0ε = 9ε

**Per-level readout degradation with *d* is almost exactly cancelled by
the reduced carrier count.** Near-neutral by construction.

*Scope:* this is for **simultaneous** *d*-level discrimination (the
transmon case). Ion-qudit readout is sequential shelving with *d*−1
detection rounds, so misreads compound and readout *time* grows with
*d* — adding idle decoherence the cancellation does not include.

---

## 21. Assembling the paper's condition

Everything above converges on one statement.

### 21.1 The condition

> **Qudits outperform qubits in bare, uncorrected circuits only with a
> native two-qudit entangling gate whose cost grows no faster than
> linearly in *d*** — and whether linear cost *suffices* is set by the
> level and structure of the operating dephasing.
>
> Quantitatively: the break-even is the qudit's layer-count ratio
> clearing (d² − 1)/(3 log₂ d) at the operating dephasing level.

### 21.2 The table it comes from

Floor-corrected signal, unbiased instance (N = 21, r = 6), common
strength 0.005:

| noise | cost | d = 2 | d = 3 | d = 5 | layers |
|---|---|---|---|---|---|
| depol. | `uniform` | 0.331 | 0.667 | **0.782** | 57/26/15 |
| | `ion` | 0.331 | 0.497 | **0.502** | 57/44/42 |
| | `pavlidis` | 0.331 | **0.394** | 0.215 | 57/58.5/93.8 |
| ladder | `uniform` | 0.282 | 0.578 | **0.631** | 57/26/15 |
| | `ion` | 0.282 | **0.374** | 0.256 | 57/44/42 |
| | `pavlidis` | **0.282** | 0.255 | 0.039 | 57/58.5/93.8 |

**The winner is decided by the cost model, not the noise model.** Read
the columns:

- **`pavlidis` (d² decomposition)** forfeits the advantage in every
  algorithm, dimension and channel — with **one instructive exception**:
  Shor at d = 3 under per-particle noise (0.394 vs 0.331; replicated at
  1000-trajectory statistics in the d = 7 grid, 0.378 vs 0.312). This
  exception *isolates the width component*: at d = 3 the depth surcharge
  almost exactly cancels the depth compression (58.5 vs 57 layers) while
  width compression survives (7 vs 11 carriers), and per-particle damage
  is nearly flat in *d*. Width alone carries the residual — which the
  ladder channel, whose per-event damage doubles at d = 3, erases.
- **`uniform` (native entangler)** — compression untouched, qudits win
  on both hardware classes.
- **`ion` (linear)** — the interesting cell. On per-particle hardware
  the ququint advantage survives (0.502 vs 0.331). At free-evolution
  ladder dephasing the verdict **splits**: the qutrit still wins Shor,
  the ququint loses, QPE is a dead heat, and Grover passes to the qubit
  for both qudits. **Refocusing repairs this entire column** (§15.4).

**Matched pairings.** Cost and noise are not independent — each pairing
describes a platform. Both physically matched pairings favour ququints:
trapped-ion qudits (`ion` + per-particle) and native-cross-Kerr
transmons (`uniform` + calibrated ladder). The pessimistic cells are
mostly *mismatched* combinations. The genuine failure mode is the
absence of a native entangler.

### 21.3 Scaling, and the plateau

Sweeping precision 6 → 14.3 bits (control dimensions 64 → 19683; the
largest register is the qutrit's sixth size, m = 9, at dim ℋ =
5.3 × 10⁵):

- Both qudits stay above the qubit at every precision in all four
  regimes.
- The qubit decays roughly **2× faster per precision bit**:
  −0.045 ± 0.003/bit (d = 2, R² = 0.99, n = 4) against
  −0.021 ± 0.005/bit (d = 3, R² = 0.80, n = 6) under the calibrated
  ladder; the ququint decays comparably to the qubit
  (−0.040 ± 0.004/bit, R² = 0.99, n = 3) **from a higher starting
  point**.
- **The qutrit is shallowest in every regime but flat in none.** The
  family holds a **plateau then falls**: under the calibrated ladder the
  first three sizes agree to χ²/dof = 0.01 (0.738–0.742 from 6.3 to 9.5
  bits) and the whole decline is carried by the last three, with the
  14.3-bit point 4.1σ below the 9.5-bit one. A single slope is a
  *summary*, not a model.
- The plateau is later and gentler under depolarizing — the ordering
  §14.3 predicts, since its per-event damage is flatter in *d*.
- **This is the decoder law made visible.** Acceptance grows linearly in
  D (exponentially in *m*) while noise broadening grows polynomially in
  *m*, so decoder tolerance **postpones** the decay of decoded success —
  it does not repeal it. The reprieve ends when accepted outcomes stop
  carrying amplitude.

> **Honest reporting note.** Five sizes would have read as a *flat*
> depolarizing family; it is the **sixth** that resolves the shape. The
> paper reports the plateau as an observation with a mechanism, not as a
> law. An earlier version of this project claimed flatness and has
> retracted it.

**Instance robustness.** The identical sweep on *N* = 29 replicates the
ordering, the qubit's fastest decay, and the qutrit's slope (0.6σ under
the calibrated ladder, 1.4σ under depolarizing) — but stops at four
qutrit sizes, so it corroborates the slope without reaching the fall.

**Eigenstate QPE** is the cleanest practical result: the advantage is
decisive and **grows** with size — at 11.6 bits the ququint retains 2.8×
the qubit's signal (+0.44 ± 0.02), reaching +0.50 ± 0.02 in the
high-E_J/E_C regime. Since eigenstate QPE is the quantum-chemistry
workhorse, this is the result with the clearest consequence.

### 21.4 The controls

| control | question | answer |
|---|---|---|
| d = 7 demo grid | does the condition extend one prime higher? | Yes, and the window **narrows**. `pavlidis` at/below the floor (−0.05…+0.04); `uniform` still wins both channels (0.53 vs 0.27 ladder; 0.80 vs 0.31 depol.) but the ladder optimum moves to **d = 5**; `ion` fails cleanly on the ladder |
| matched control dimension | is the qudit lead just a bigger acceptance set? | No — equalizing D **helps the qudits**. At d = 2, m = 7 (D = 128) the qubit scores 0.47/0.30 vs 0.51/0.33 at D = 64: extra decoder tolerance is outweighed by the deeper circuit's exposure |
| d = 4 (prime power) | does primality matter? | Lands in the qudit band (0.83/0.75) — but GF(4) exists and its D = 64 shares the qubit's misalignment bit for bit, so it cannot settle it alone |
| **d = 6 (composite, non-prime-power)** | the decisive primality control | Family reads 0.45/0.64/0.77/0.70/0.77 (ladder) and 0.29/0.53/0.72/0.71/0.84 (depol.) for d = 2/3/4/5/6 — **both composites inside the qudit band, d = 6 at its top under depolarizing.** The bare dynamics carries no trace of primality |
| readout error | does *d*-level readout kill it? | Structurally near-neutral (§20.4) |
| noise inflation | how much extra qudit noise is tolerable? | f* = 1.2–4.5 depending on pairing (§19.3) |
| Zeeman dephasing | worst realistic case? | **Reverses the verdict outright** (§17.2) |

### 21.5 The hardware anchor

The qubit branch of the predictions compiles at face-value gate counts,
and was run on AWS Braket in August 2026:

| device | circuit | predicted | measured | \|w⟩ |
|---|---|---|---|---|
| IonQ Forte-1 | m = 5 (15 gates) | 0.60–0.70 | **0.617 ± 0.007** | 0.99 |
| IonQ Forte-1 | m = 7 (28 gates) | 0.42–0.54 | 0.011 ± 0.001 | 0.99 |
| IonQ Forte-1 | m = 7 AQFT (25) | 0.44–0.57 | 0.066 ± 0.005 | 0.99 |
| IQM Garnet | m = 5 (15 gates) | — | 0.080 ± 0.004 | 0.81 |
| IQM Garnet | m = 7 (28 gates) | — | 0.032 ± 0.003 | 0.66 |

Three findings, each mapping onto the framework:

1. **The shallow ion circuit lands inside its predicted band.** And
   debiasing is not doing the work: the raw 1000-shot pilot scored
   0.608 ± 0.015, within 0.009 of the debiased value and inside the same
   band. Because the success-vs-strength map is steep, this single
   number **pins the device's effective per-gate depolarizing strength
   at 0.007–0.009**, bracketing the vendor's measured 0.7% two-qubit
   infidelity. That is a quantitative validation of the depolarizing
   convention on the hardware class it models.
2. **The deep ion circuit fails coherently, not by decoherence.** The
   peak is destroyed (0.011, below the 0.031 random floor) while the
   work qubit stays at 0.99. No relabeling recovers it — the best over
   **10,080 reinterpretations** (every ordering of control bits in both
   polarities) reaches only 0.15, not significant over so large a
   hypothesis set. A 500-shot raw m = 4 probe caught the mechanism
   directly and unmitigated: a nearly pure output state (71% of shots on
   one outcome) whose phase is **wrong by one least-significant digit**.
   AQFT recovers only ~6×. This is accumulated coherent angle
   systematics — precisely the error class §14.4 says breaks the
   damage law.
3. **The superconducting lattice fails by plain decoherence** — both
   circuits at the random floor with the work qubit visibly decayed
   (0.81/0.66), the signature of SWAP-routing an all-to-all kickback
   pattern through fixed connectivity. This is **compilation overhead
   deciding the outcome before noise structure enters** — the hardware
   face of the `pavlidis` lesson.

**The caution generalizes:** past a depth threshold, a decoded-success
benchmark on NISQ hardware measures coherent calibration error, not the
decoherence it nominally probes.

### 21.6 The proposed experiment

The cheapest decisive test: **eigenstate QPE at d = 5, m = 2–3 on a
Ringbauer-class trapped-ion processor.** Six native entangling gates at
m = 3 (~8–12 two-qudit gates after reduction, i.e. 64–96 MS pulses at
2(d−1) per gate). No multi-qudit algorithm requiring entangling gates
has yet been run above d = 3 on that platform.

| register | b | gates (MS layers) | noiseless | s = 0.001 | 0.005 | 0.01 | 0.02 |
|---|---|---|---|---|---|---|---|
| d = 5, m = 2 | 4 | 3 (20) | 0.816 | 0.785 | 0.674 | 0.562 | 0.401 |
| d = 2, m = 5 | 4 | 15 (30) | 0.917 | 0.807 | 0.500 | 0.299 | 0.142 |
| d = 5, m = 3 | 5 | 6 (36) | 0.948 | **0.855** | 0.575 | 0.364 | 0.168 |
| d = 2, m = 7 | 5 | 28 (49) | 0.989 | 0.778 | 0.328 | 0.140 | 0.053 |

Key point: **the proposal does not wait on projected gate fidelities.**
Demonstrated two-qudit gates sit an order of magnitude above the
single-qudit figure, and in that band the separation *widens* — 0.575 vs
0.328 at s = 5 × 10⁻³. The m = 2 pair is subtler (the coarse D = 25 grid
depresses the ququint's noiseless ceiling, so its advantage shows in
floor-corrected signal while raw success crosses only near
s = 2 × 10⁻³), so **m = 3 is the decisive pair** — and the deep-circuit
coherent failure above counsels entering at m = 2 first.

**Which platform.** Both matched pairings favour ququints, but their
robustness to residual structured dephasing differs sharply (§17.3): the
native-entangler route tolerates ε ≈ 0.6–0.8, the linear-MS route only
0.09–0.15. **The transmon route is the robust one**; the ion route
offers larger headline gains, conditional on collective-*B* suppression
beyond plain shielding.

### 21.7 Reconciling with the code-level literature

Keppens *et al.* find slightly **worse** qudit logical error rates for
the five-qudit code under the same noise convention. The results are
compatible, and the reconciliation is one sentence:

> A code is five carriers and a fixed gate list at every *q* — **there
> is no problem instance to compress** — so raising *q* charges every
> carrier more while buying no width or depth. An algorithm compresses;
> that compression is the entire source of the advantage measured here.

A qudit advantage must therefore be argued at the level of a
**compressible workload**, and does not transfer automatically to the
error-correction layer, where the dimension dependence can carry the
opposite sign. Relatedly, Bocharov *et al.* show emulated-binary
arithmetic can beat native ternary — **encoding density alone is not a
mechanism** — consistent with attributing the advantage to
width-and-depth compression, and with its disappearance when compilation
buys the compression back.

### 21.8 Recommendations to the field

Each rule was learned by stepping on the corresponding rake.

1. **Randomize or report grid alignment.** An irrational target phase
   does it for QPE; for order finding, choose *r* dividing no dᵐ and
   report residual misalignment.
2. **Match problem size by interpolation**, not by comparing raw dⁿ
   points.
3. **Charge multi-qudit gates their decomposition depth.**
4. **Report the floor-to-baseline span** of the metric (> 0.15).
5. **Report end-state fidelity alongside decoded signal** (§12.8).

---

## 22. What is *not* settled

A textbook that only lists results teaches the wrong lesson. The paper's
Limitations, restated as open problems:

- **Coherent errors are not modelled.** Cross-Kerr shifts (0.1–0.7 MHz)
  and drive-induced shifts are excluded, as is leakage during gates.
  Cross-Kerr is known to be fast on unprotected qutrits, and the number
  of level pairs it can act on **grows with d** — so its omission
  plausibly favours qudits. *The sign of this bias runs against the
  paper's conclusion, not for it.*
- **Gate cost and gate error are treated as proportional.** A model
  where longer gates achieve better per-operation fidelity would soften
  the ion penalty.
- **The schedule is serial.** Concurrent execution would cut idle
  exposure most for d = 2.
- **The plateau's onset is unfitted.** Six sizes locate the fall in the
  last three but cannot fit its onset; the N = 29 sweep stops before
  reaching it. Behaviour beyond 14.3 bits is unmeasured.
- **d > 7 is untested**, and d = 7 only at demo size on one instance —
  where the break-even window has visibly narrowed.
- **Modular arithmetic is applied as an exact unitary.** Compiled
  arithmetic (depth 4d²q per adder under two-level decomposition) has a
  *d*-dependence of its own: at face value the compiled qudit-to-qubit
  depth ratio spans ≈ 0.9–2.7 across d = 3, 5, extending beyond the
  `pavlidis` row's 1.0–1.65. **Compiled arithmetic can be harsher than
  any cost model charged here** — so the decomposition verdict is, if
  anything, conservative. The penalty is confined to **depth**: the
  follow-up multiplier construction is in-place and ancilla-free (width
  exactly *n*, nearest-neighbour interactions only), so compiled
  arithmetic inflates the *layers* term of the carriers × layers
  exposure budget but not the carrier count — and maps onto a linear ion
  chain without routing overhead.
- **Fault-tolerant overhead is out of scope**, and its dimension
  dependence may differ in sign.
- **d = 5 entangling gates exist today only on trapped ions** — the deep
  register results are one to two hardware generations ahead of
  experiment.
- **The Zeeman convention needs direct evidence:** *d*-resolved Ramsey
  or echo coherence across the encoding's transitions. Until then, the
  per-particle convention is a statement about *mitigated* hardware.

---
---

# Part VI — Exercises

Each is checkable against a script in this repo. Difficulty: ★ (pen and
paper) to ★★★ (write code).

**§1–4 · Qudits and registers**

1. ★ Verify ZX = ωXZ directly on basis states, and deduce X^a Z^b =
   ω^{−ab} Z^b X^a.
2. ★ Show tr((X^a Z^b)† X^{a′} Z^{b′}) = d δ_{aa′} δ_{bb′}. Conclude the
   d² generalized Paulis are an operator basis.
3. ★ Show F_d† X F_d = Z.
4. ★ For N = 21, compute *w* = ⌈log_d N⌉ and *m* for D ≥ 64 at
   d = 2, 3, 5. Reproduce the 11 / 7 / 5 carrier counts.
5. ★★ Reproduce the 57 / 26 / 15 uniform layer counts, then apply the
   `pavlidis` d²/4 multiplier to get 57 / 58.5 / 93.8.

**§5–9 · Algorithms**

6. ★★ Derive the Fejér kernel P(y) from the geometric sum, and verify
   P(y₀) = 1 when φ = y₀/D.
7. ★★ Prove the worst-case bound P(nearest) ≥ 4/π².
8. ★ Verify U_a|u_s⟩ = e^{2πis/r}|u_s⟩ and (1/√r)Σ_s |u_s⟩ = |1⟩.
9. ★ Show (Z/15)* ≅ Z₂ × Z₄ and conclude every order divides 4.
   *This is the whole N = 15 pathology in one line.*
10. ★★ Compute the continued fraction of 0.6180339887…. Explain in one
    sentence why this makes eigenstate QPE immune to §10.
11. ★★★ Implement Grover in base *d* and confirm the iteration count
    ⌊(π/4)√M⌉ maximizes marked-state probability. Compare with
    `grover.py`.

**§10–12 · Number theory** *(the core)*

12. ★★ Compute residual misalignment for (N = 21, r = 6) at d = 2, 3, 5.
    Reproduce 0.267 / 0.300 / 0.300. Then do (N = 29, r = 7) and get
    0.2857 for all three.
13. ★★ Prove D = dᵐ mod r is eventually periodic in *m*, and conclude
    alignment cannot drift with register size (§10.5). Check against
    `misalignment_scaling.py`.
14. ★★ Prove the acceptance lemma of §11 in both directions. Where
    exactly is "*r* is the **order**" (not merely *some* exponent) used?
15. ★★★ Enumerate A for (N = 21, r = 6) at D = 64, 256, 1024 and
    reproduce |A| = 8, 36, 148. Check against `decoder_formula.py`.
16. ★★ Verify the totient sum for (N = 21, r = 6): admissible
    denominators are 6, 12, 18. Compute
    2 ln 2 · [φ(6)/36 + φ(12)/144 + φ(18)/324] and compare with 0.141.
17. ★★ Show why the naive (r−1)/r² envelope is accidentally right at
    r = 6, N = 21 — identify the two compensating errors of §12.6.
18. ★★★ For (N = 33, r = 5) vs (r = 10), compute totient-sum ratios and
    reproduce 9.7 / 9.3 against measured 9.6 / 8.9. Note that 1/r²
    predicts 4.0.
19. ★★ Show Σ_{q≤Q} μ(q) → (12 ln 2/π²) ln Q using Σ φ(q)/q² ≈
    (6/π²) ln Q. Why does this *validate* the measure rather than the
    law?

**§13–18 · Open systems**

20. ★★ Show F_e = Σ_i |tr K_i|²/d² for a Kraus decomposition.
21. ★★ Derive 1 − F_e = p(1 − 1/d²) for depolarizing; evaluate at
    d = 2, 3, 5 and reproduce 0.75p / 0.89p / 0.96p.
22. ★★ Show a linear frequency ladder can only produce a (Δlevel)²
    dephasing law, and hence **cannot** realize the measured max-level
    law. (This is why §16 exists.)
23. ★★★ Implement classical MDS on a target Γ_φ matrix and confirm
    residual ≤ 10⁻¹⁶ for d = 3, 5.
24. ★★ Explain why log-fidelity additivity makes the R² = 0.97–0.99
    collapse a **null expectation**. Then explain what in
    Table §14.4 is *not* null.
25. ★★★ Reproduce the trajectory-vs-exact agreement test for a small
    register.

**§19–21 · Accounting**

26. ★ Evaluate (d²−1)/(3 log₂ d) at d = 3, 5, 7 → 1.68 / 3.45 / 5.70.
    Compare with folklore d²/log₂ d → 5.7 / 10.8 / 17.5.
27. ★★ Reproduce the readout cancellation 9ε / 8ε / 9ε at D ≈ 64.
28. ★★ For a random outcome at (N = 21, D = 64, r = 6), compute the
    continued-fraction floor and check it against 0.12–0.13.
29. ★★★ Show why r = 4 has floor > baseline at every modulus except
    N = 15 — i.e. why the converse alignment control of §10.4 cannot
    exist.

---
---

# Appendix

## A.1 Notation

| symbol | meaning |
|---|---|
| *d* | qudit dimension (levels per carrier) |
| ω, ω_D | e^{2πi/d}, e^{2πi/D} |
| X, Z | generalized Pauli shift and clock |
| F_d | Fourier (generalized Hadamard) gate |
| *m*, *D* | control carriers, control dimension D = dᵐ |
| *w* | work carriers, w = ⌈log_d N⌉ |
| *N*, *a*, *r* | modulus, base, multiplicative order r = ord_N(a) |
| φ, φ* | phase; golden-ratio conjugate ≈ 0.6180 |
| *A* | decoder acceptance set {y : decode(y) = r} |
| φ(·) | Euler totient (context distinguishes it from phase) |
| S | one-layer superoperator, natural representation |
| F_e | entanglement fidelity tr S / d²; **damage** = 1 − F_e |
| Γ_k, Γ_φ(j,k) | relaxation rate of level *k*; dephasing rate of pair (j,k) |
| *s*, *p* | per-carrier-layer noise strength (ladder, depolarizing) |
| f* | noise-inflation crossing factor |
| ε* | Zeeman suppression factor at which qudit ordering returns |

⚠ **φ is overloaded** — Euler's totient in §12, a phase everywhere else.
The paper does the same; context always disambiguates.

## A.2 Reading path

If you are starting cold, in order:

| step | read | for |
|---|---|---|
| 1 | This document, Parts I–II | the algorithms in base *d* |
| 2 | `docs/THEORY.md` | physical platforms, literature pointers |
| 3 | `docs/TRANSMON.md` | what a transmon is, and why "ladder" |
| 4 | `docs/CALIBRATION.md` | how the ladder channel was fitted |
| 5 | This document, Parts III–IV | the two original derivations |
| 6 | `docs/GRID_ALIGNMENT.md`, `docs/MECHANISM.md` | how the confound was found (the audit trail) |
| 7 | `docs/COST_SENSITIVITY.md`, `docs/ROBUSTNESS.md` | the objections, tested |
| 8 | `docs/GROVER.md` | the falsification test and the damage-unit fits |
| 9 | `docs/HARDWARE.md` | the Braket campaign |
| 10 | `paper/main.pdf` | the finished argument |
| 11 | `docs/SOTA.md`, `papers/INDEX.md` | the 51-paper library |

`docs/PAPER.md` maps every paper section to its document and script.

## A.3 Script map

Where each derivation in this textbook is executed:

| § | topic | script | result |
|---|---|---|---|
| 3, 19 | cost models | `cost_fair.py`, `cost_sensitivity.py` | `cost_fair.json` |
| 3 | d = 7 grid | `d7_demo.py` | `d7_demo.json` |
| 6–7 | QPE, order finding | `qudit_shor.py`, `qpe_generic.py` | — |
| 7.4 | eigenstate interpolation | `interpolation_experiment.py` | `interpolation.json` |
| 9 | Grover | `grover.py`, `grover_study.py`, `grover_cost.py` | `grover*.json` |
| 10 | alignment classes | `grid_alignment.py` | `grid_alignment.json` |
| 10.3 | within-modulus control | `same_n_control.py` | `same_n_control.json` |
| 10.3 | ensembles over (Z/N)* | `ensemble_a.py`, `ensemble_a_traj.py` | `ensemble_a*.json` |
| 10.5 | misalignment vs size | `misalignment_scaling.py` | `misalignment_scaling.json` |
| 11 | acceptance lemma | `decoder_formula.py` | `decoder_formula.json` |
| 12 | acceptance law | `decoder_scaling.py` | `decoder_scaling.json` |
| 14 | damage units | `exposure_collapse.py` | `exposure_collapse.json` |
| 14.4 | fidelity collapse | `fidelity_collapse.py`, `logfid_rescore.py` | `fidelity_collapse.json`, `logfid_rescore.json` |
| 15–16 | calibrated ladder | `qudit_shor.py` (channel construction) | — |
| 17 | Zeeman dephasing | `collective_zeeman.py`, `ion_zeeman_demo.py`, `ion_zeeman_echo.py` | `collective_zeeman.json`, `ion_zeeman_{demo,echo}.json` |
| 19.2 | Janković reproduction | `jankovic_check.py` | `jankovic.json` |
| 19.3 | noise inflation | `noise_inflation.py` | `noise_inflation.json` |
| 20.4 | readout error | `spam_study.py` | `spam.json` |
| 15.4 | refocusing | `dd_study.py` | `dd.json` |
| 21.3 | scaling | `scaling_fair.py`, `scaling_fair_m8.py`, `scaling_fair_n29.py`, `scaling_fair_point.py` | `scaling_fair*.json` |
| 21.4 | matched D | `matched_D.py` | `matched_D.json` |
| 21.4 | composite d | `d4_control.py`, `composite_control.py` | `d4_control.json`, `composite_control.json` |
| 21.5 | hardware | `braket_qpe_anchor.py`, `braket_raw_analysis.py` | `braket_*.json` |
| 21.6 | ion predictions | `ion_qpe_prediction.py` | `ion_qpe_prediction.json` |
| — | correctness suite | `test_qudit_shor.py` | 20 tests |

---

*Companion to `paper/main.tex`. Corrections welcome — every number here
is reproducible from the scripts above.*
