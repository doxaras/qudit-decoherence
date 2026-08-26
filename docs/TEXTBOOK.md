# Qudits under decoherence: a first-principles textbook

*From bachelor mathematics to the paper's result, with nothing assumed
in between.*

This document is the self-contained course behind `paper/main.tex` —
**"Native gates are necessary but not sufficient: the conditions for a
qudit advantage in uncorrected quantum algorithms under decoherence."**
Its ambition is the one Nielsen and Chuang set for quantum computation
as a whole: start from mathematics a third-year undergraduate already
owns — linear algebra, calculus, elementary probability — and *derive*
everything else. Qudits, the Fourier transform over Z_D, phase
estimation, continued fractions, completely positive maps, the Lindblad
equation, entanglement fidelity, quantum trajectories, and the paper's
own two original derivations (the decoder acceptance law and the
damage-unit accounting) are all built here from definitions, with
proofs.

**Rules of the game.**

1. Every object gets a *Definition* before it is used.
2. Every claim that is not a definition gets a *Proof*, a *Proof
   sketch* with the gap stated, or an explicit citation to where the
   proof lives.
3. Every number gets a script: each quantitative statement in this book
   is reproducible from a committed script in this repository, named
   where the number appears and indexed in Appendix A.3.
4. *Exercises* are interleaved where the muscle should be built, in the
   Nielsen–Chuang style: doing them is part of reading. Starred
   exercises (★★★) require writing code; the repository is the answer
   key.

**How to read it.** Part 0 is the mathematical toolkit; skim it if you
have had a linear algebra course with inner product spaces and a first
number theory course, but do the exercises you cannot do on sight —
they are diagnostic. Parts I–II are standard quantum computation
rebuilt in base *d* instead of base 2. Parts III–IV contain the two
derivations original to this work. Part V assembles the paper's central
condition and its robustness program. Part VI collects the project-size
exercises.

The other documents in `docs/` are *lab notebooks*: they record what
was run, in the order it was run, including the things that turned out
to be wrong. This book is the opposite: the shortest correct path from
first principles to the result, with the wrong turns removed — except
where a wrong turn *is* the lesson (§7.4, §10.2), in which case it is
kept and labelled.

**Conventions.** *d* is the qudit dimension (levels per carrier), *m*
the number of control carriers, *D = dᵐ* the control dimension, *w* the
number of work carriers, *N* the modulus, *r* the multiplicative order,
ω = e^{2πi/d}, ω_D = e^{2πi/D}. "Carrier" means one physical *d*-level
system; "layer" means one time step of the serial schedule. Logarithms
are base 2 unless written ln. ℕ, ℤ, ℝ, ℂ are the naturals, integers,
reals, complexes; 𝟙 is the identity operator. Proof ends are marked ∎.

---

## Contents

**Part 0 — The mathematical toolkit**
- 0.1 Complex inner product spaces and Dirac notation
- 0.2 Operators: adjoints, unitaries, and the spectral theorem
- 0.3 Tensor products
- 0.4 Probability for quantum measurement
- 0.5 Arithmetic: gcd, modular arithmetic, and the group (Z/N)*
- 0.6 Fields, and why Z_p is one
- 0.7 The matrix exponential

**Part I — The qudit**
1. Hilbert space, basis, and the generalized Pauli group
2. Why *prime* d is special — and where it is irrelevant
3. Gates, and what a two-qudit gate costs
4. Registers: width, depth, and qubit-equivalents

**Part II — The algorithms**
5. The Fourier transform over Z_D
6. Phase estimation, derived
7. Order finding: why Shor *is* phase estimation
8. Continued fractions, with proofs
9. Grover search in base d

**Part III — The number theory**
10. Grid alignment
11. The decoder acceptance lemma
12. The decoder acceptance law

**Part IV — Open quantum systems**
13. Density matrices, channels, and the Choi theorem
14. The Lindblad equation, derived
15. Damage units: entanglement fidelity as the currency
16. The calibrated ladder channel
17. Realizing a dephasing matrix exactly: Euclidean embedding
18. Depolarizing, structured dephasing, and what measurement did to both
19. Quantum trajectories, with the unravelling theorem

**Part V — The accounting, and the result**
20. Exposure, cost models, and break-even
21. The success metric
22. Assembling the paper's condition
23. The robustness program: every objection, priced
24. What is *not* settled

**Part VI — Projects**

**Appendix — A.1 Notation · A.2 Reading path · A.3 Script map**

---
---

# Part 0 — The mathematical toolkit

Nothing in this part is about quantum mechanics. It is the mathematics
a bachelor's degree supplies, restated in the notation the rest of the
book uses, with the proofs the rest of the book leans on. If a section
is familiar, do its last exercise and move on.

## 0.1 Complex inner product spaces and Dirac notation

**Definition 0.1 (Complex vector space).** A set *V* with addition and
scalar multiplication by complex numbers satisfying the usual axioms
(associativity, commutativity of +, distributivity, a zero vector, and
1·v = v). Every space in this book is ℂ^n for some finite *n*: column
vectors of *n* complex numbers.

**Definition 0.2 (Inner product).** A map ⟨·,·⟩ : V × V → ℂ that is
(i) linear in the *second* argument, (ii) conjugate-symmetric,
⟨u, v⟩ = ⟨v, u⟩*, and (iii) positive definite: ⟨v, v⟩ > 0 for v ≠ 0.
On ℂ^n the standard inner product is ⟨u, v⟩ = Σ_i u_i* v_i. The
**norm** is ‖v‖ = √⟨v, v⟩.

The physics convention (linearity in the second slot) is opposite to
most linear algebra texts; it is what makes Dirac notation compose
without conjugation surprises.

**Dirac notation, as a dictionary.** A **ket** |ψ⟩ is a column vector.
A **bra** ⟨ψ| is its conjugate transpose — a row vector, i.e. the
linear functional v ↦ ⟨ψ, v⟩. Then:

- ⟨φ|ψ⟩ is the inner product (a number),
- |φ⟩⟨ψ| is the outer product (a rank-one matrix),
- ⟨φ|A|ψ⟩ is the number ⟨φ, Aψ⟩ for a matrix A.

Nothing about the notation is deep; its value is that composition of
symbols matches composition of maps.

**Theorem 0.1 (Cauchy–Schwarz).** |⟨u, v⟩| ≤ ‖u‖ ‖v‖, with equality
iff u, v are linearly dependent.

*Proof.* If v = 0 both sides vanish. Otherwise let λ = ⟨v, u⟩ / ⟨v, v⟩
and w = u − λv, the component of u orthogonal to v (check:
⟨v, w⟩ = ⟨v, u⟩ − λ⟨v, v⟩ = 0). Then

    ‖u‖² = ⟨λv + w, λv + w⟩ = |λ|²‖v‖² + ‖w‖² ≥ |λ|²‖v‖²
         = |⟨u, v⟩|² / ‖v‖²,

which rearranges to the claim; equality forces w = 0, i.e. u ∝ v. ∎

**Definition 0.3 (Orthonormal basis).** A set {|e_1⟩, …, |e_n⟩} with
⟨e_i|e_j⟩ = δ_ij that spans *V*. Every finite-dimensional inner product
space has one (Gram–Schmidt), and every vector expands uniquely as
|v⟩ = Σ_i ⟨e_i|v⟩ |e_i⟩. The **completeness relation**
Σ_i |e_i⟩⟨e_i| = 𝟙 is this expansion written as an operator identity,
and it is used silently on almost every page below: inserting it
converts abstract equalities into component computations.

**Exercise 0.1.** Prove the completeness relation from the unique
expansion, and use it to show ⟨φ|ψ⟩ = Σ_i ⟨φ|e_i⟩⟨e_i|ψ⟩ (the
resolution of the inner product every "insert a complete set of states"
argument uses).

**Exercise 0.2.** Show that the *n*-th roots of unity sum to zero for
n > 1: Σ_{k=0}^{n−1} e^{2πi jk/n} = n δ_{j ≡ 0 (mod n)}. (Geometric
series. This one identity is the engine of every Fourier argument in
Part II; we will call it **root-of-unity orthogonality**.)

## 0.2 Operators: adjoints, unitaries, and the spectral theorem

**Definition 0.4 (Adjoint).** For a linear map A on *V*, the adjoint
A† is the unique map with ⟨A†u, v⟩ = ⟨u, Av⟩ for all u, v. In any
orthonormal basis, A† is the conjugate transpose. Key algebra:
(AB)† = B†A†, (A†)† = A.

**Definition 0.5.** A is **Hermitian** if A = A†; **unitary** if
A†A = 𝟙 (equivalently: A preserves inner products, hence norms);
**normal** if AA† = A†A. Hermitian and unitary operators are both
normal.

**Definition 0.6 (Projector).** P is an (orthogonal) projector if
P = P† = P². For a unit vector, |e⟩⟨e| is the projector onto its line.

**Theorem 0.2 (Spectral theorem, finite dimension).** A is normal iff
there is an orthonormal basis {|e_i⟩} of eigenvectors:
A = Σ_i λ_i |e_i⟩⟨e_i| with λ_i ∈ ℂ. If A is Hermitian the λ_i are
real; if unitary, |λ_i| = 1.

*Proof.* (⇐) is a computation. (⇒) by induction on dim V. Over ℂ the
characteristic polynomial has a root λ with unit eigenvector |e⟩. The
step that needs normality: the orthogonal complement W = {v : ⟨e|v⟩=0}
is invariant under A. First, A†|e⟩ = λ*|e⟩: normality gives
‖(A − λ)v‖ = ‖(A† − λ*)v‖ for every v (expand both sides and use
AA† = A†A), and applying this at v = |e⟩ makes the right side vanish.
Then for v ∈ W: ⟨e|Av⟩ = ⟨A†e|v⟩ = λ⟨e|v⟩ = 0, so Av ∈ W. Restrict A
to W — still normal — and induct. The eigenvalue claims: if A = A†,
λ = ⟨e|Ae⟩ = ⟨Ae|e⟩ = λ*; if A†A = 𝟙, |λ|² ⟨e|e⟩ = ⟨Ae|Ae⟩ = ⟨e|e⟩. ∎

**Definition 0.7 (Function of an operator).** For normal
A = Σ λ_i |e_i⟩⟨e_i| and f defined on the spectrum,
f(A) := Σ f(λ_i)|e_i⟩⟨e_i|. This is how √ρ, log ρ, and e^{iθZ} are
meant everywhere below, and the spectral theorem is what makes the
definition basis-independent.

**Definition 0.8 (Trace; Hilbert–Schmidt inner product).**
tr A = Σ_i ⟨e_i|A|e_i⟩, independent of the orthonormal basis (proof:
insert completeness twice), with the cyclic property tr(AB) = tr(BA).
The space of operators is itself an inner product space under
⟨A, B⟩_HS = tr(A†B); "orthogonal operators" below always means
orthogonal in this sense.

**Definition 0.9 (Positive semidefinite).** A ⪰ 0 iff ⟨v|A|v⟩ ≥ 0 for
all v. Equivalent (via the spectral theorem): A Hermitian with all
eigenvalues ≥ 0. Equivalent again: A = B†B for some B.

**Exercise 0.3.** Prove the three characterizations of A ⪰ 0
equivalent. (For Hermiticity from ⟨v|A|v⟩ ∈ ℝ ∀v: polarize — apply the
hypothesis at v, w, v + w, v + iw.)

**Exercise 0.4.** Show that the eigenvalues of a projector are 0 and
1, and that tr P = rank P.

**Exercise 0.5 (Operator basis warm-up).** Show dim of the operator
space on ℂ^d is d², and that any d² operators that are HS-orthogonal
and nonzero form a basis. Part I builds precisely such a basis from two
matrices.

## 0.3 Tensor products

Composite systems are described by tensor products; every register in
this book is one. We give the concrete construction; its
basis-independence is Exercise 0.6.

**Definition 0.10 (Tensor product of spaces).** For V = ℂ^a, W = ℂ^b
with bases {|i⟩}, {|j⟩}, the space V ⊗ W is ℂ^{ab} with basis the
formal symbols |i⟩⊗|j⟩ (written |i⟩|j⟩ or |ij⟩), and
(Σ_i α_i|i⟩) ⊗ (Σ_j β_j|j⟩) := Σ_{ij} α_i β_j |ij⟩. The inner product
is ⟨i j|i′j′⟩ = δ_{ii′}δ_{jj′}, extended conjugate-bilinearly.

Two consequences worth internalizing early:

- **Dimensions multiply.** *n* carriers of dimension *d* give dⁿ, not
  nd. This exponential is the resource the whole field mines.
- **Not every vector is a product.** |00⟩ + |11⟩ (unnormalized) cannot
  be written (α|0⟩+β|1⟩)⊗(γ|0⟩+δ|1⟩): matching coefficients forces
  αδ = βγ = 0 while αγ = βδ = 1, a contradiction. Such vectors are
  **entangled**.

**Definition 0.11 (Tensor product of operators).**
(A ⊗ B)(|v⟩⊗|w⟩) = A|v⟩ ⊗ B|w⟩, extended linearly. In components,
the Kronecker product. Algebra used constantly:
(A⊗B)(C⊗D) = AC ⊗ BD, (A⊗B)† = A†⊗B†, tr(A⊗B) = tr A · tr B.

**Definition 0.12 (Partial trace).** The unique linear map
tr_W : Op(V⊗W) → Op(V) satisfying tr_W(A ⊗ B) = A · tr B. Concretely,
(tr_W M)_{ii′} = Σ_j M_{ij, i′j}. Physically: the description of
subsystem V alone, when M describes the joint system — the proof that
this is the *right* notion is Exercise 0.8, and the object it produces
(the reduced density matrix) is the workhorse of §13 and §19.

**Exercise 0.6.** Show that Definition 0.10 built from a different
pair of bases gives a canonically isomorphic space. (Map basis symbols
via the change-of-basis matrices; check inner products.)

**Exercise 0.7.** Prove tr(A⊗B) = tr A tr B from Definition 0.12's
component form.

**Exercise 0.8.** Let M ⪰ 0 with tr M = 1 on V ⊗ W, and let O be an
observable on V. Show tr((O ⊗ 𝟙)M) = tr(O · tr_W M). (This says: for
every measurement made on V alone, tr_W M predicts what M predicts —
which is the defining property of the reduced state.)

## 0.4 Probability for quantum measurement

Finite probability only; nothing measure-theoretic is needed.

**Definition 0.13.** A finite probability distribution is p : Ω → [0,1]
with Σ p(x) = 1. A random variable is f : Ω → ℝ, with expectation
E[f] = Σ p(x)f(x) and variance Var f = E[f²] − E[f]².

**The Born rule (statement, not theorem).** Measuring a system in
state |ψ⟩ in the orthonormal basis {|e_i⟩} yields outcome *i* with
probability p_i = |⟨e_i|ψ⟩|². Completeness (Exercise 0.1) is what makes
these sum to one. In this book the rule is an axiom; everything else
about measurement is derived from it plus linear algebra.

**Theorem 0.3 (Monte Carlo error bar).** If X₁,…,X_n are independent,
identically distributed with mean μ and variance σ², the sample mean
X̄ has E[X̄] = μ and Var X̄ = σ²/n. Hence the **standard error**
σ/√n, estimated in practice by the sample standard deviation over √n.

*Proof.* Linearity of E gives E[X̄] = μ. For the variance, expand
Var(ΣX_i) = Σ Var X_i (cross terms vanish by independence) = nσ², and
Var(X̄) = Var(ΣX_i)/n². ∎

Every "± value" attached to a trajectory number in this repository is
exactly this estimator, and §19 explains why the trajectory samples
have *smaller* variance than the Bernoulli p(1−p)/n a naive reading
would assign — each trajectory reports a full distribution, not one
sampled outcome. The claim that these bars are *calibrated* is itself
measured, on 24 × 1000 independent replicas (`trajectory_variance.py`:
empirical-to-quoted ratio 0.995).

**Exercise 0.9.** An estimator averages n i.i.d. values of a quantity
bounded in [0,1]. Show its standard error is at most 1/(2√n), and
compute the n needed for a ±0.01 bar in the worst case.

## 0.5 Arithmetic: gcd, modular arithmetic, and the group (Z/N)*

This section is the complete number-theoretic toolkit for Parts II–III.
Proofs are short and are given because Part III's derivations stand on
them.

**Definition 0.14.** For integers a, b not both zero, gcd(a, b) is the
largest positive integer dividing both. Integers with gcd 1 are
**coprime**.

**Theorem 0.4 (Euclidean algorithm and Bézout).** gcd(a, b) is
computed by repeated division with remainder (gcd(a, b) =
gcd(b, a mod b), terminating at gcd(g, 0) = g), and there exist
integers x, y with ax + by = gcd(a, b).

*Proof.* If a = qb + r then any common divisor of (a, b) divides
(b, r) and conversely, so the gcd is preserved and the recursion
terminates (remainders strictly decrease). Bézout by reverse
substitution through the division steps, or: the set
{ax + by > 0} has a least element g; division with remainder shows g
divides both a and b (else a smaller positive combination exists), and
any common divisor divides g. ∎

**Definition 0.15 (Z_N and (Z/N)*).** Z_N = {0, 1, …, N−1} with
addition and multiplication mod N — a commutative ring. Its
**unit group** (Z/N)* is the subset of elements coprime to N, under
multiplication.

**Theorem 0.5.** a ∈ Z_N has a multiplicative inverse iff
gcd(a, N) = 1, and (Z/N)* is a group of order φ(N), where φ is Euler's
totient (the count of 1 ≤ k ≤ N coprime to N).

*Proof.* If ax ≡ 1 then ax − 1 = kN, so any common divisor of a, N
divides 1. Conversely Bézout gives ax + Ny = 1, i.e. ax ≡ 1 (mod N).
Closure: a product of units has the product of inverses. ∎

**Definition 0.16 (Order).** For a ∈ (Z/N)*, ord_N(a) = min{k > 0 :
a^k ≡ 1 (mod N)} — finite because powers of *a* repeat in a finite
set, and a repeat a^i = a^j (i < j) cancels (a is a unit!) to
a^{j−i} = 1.

**Theorem 0.6 (The order divides every annihilator).** a^k ≡ 1 (mod N)
iff ord_N(a) | k. In particular (Lagrange, via the cyclic subgroup
⟨a⟩): ord_N(a) divides φ(N), which is Fermat–Euler.

*Proof.* Let r = ord_N(a), k = qr + s with 0 ≤ s < r. Then
1 ≡ a^k = (a^r)^q a^s ≡ a^s, and minimality of r forces s = 0. The
converse is trivial. For the divisibility of φ(N): the cosets of the
subgroup {1, a, …, a^{r−1}} partition (Z/N)* into equal-size classes
(the standard Lagrange argument), so r | φ(N). ∎

Theorem 0.6 is quoted verbatim in the decoder acceptance lemma (§11):
*"a^q ≡ 1 iff r | q" is the only number theory the lemma needs.*

**Theorem 0.7 (Chinese Remainder Theorem).** If N = N₁N₂ with
gcd(N₁, N₂) = 1, then Z_N ≅ Z_{N₁} × Z_{N₂} as rings, via
x ↦ (x mod N₁, x mod N₂); the unit groups factor accordingly, and φ is
multiplicative on coprime factors.

*Proof.* The map is a ring homomorphism; it is injective because
x ≡ 0 mod both factors implies N | x (coprimality); surjective by
counting (both sides have N elements) — or explicitly, by Bézout write
1 = N₁u + N₂v and check x = a·N₂v + b·N₁u hits (a, b). ∎

**Worked example (the N = 15 pathology, previewed).**
(Z/15)* ≅ (Z/3)* × (Z/5)* ≅ Z₂ × Z₄ by CRT. Every element of Z₂ × Z₄
has order dividing lcm(2,4) = 4, so **every order mod 15 is 1, 2, or
4 — a power of two**. Section 10.2 shows how this innocent-looking fact
silently rigged an entire generation of qudit-Shor benchmarks,
including the first version of this project.

**Exercise 0.10.** Compute φ(21), list the orders of all elements of
(Z/21)*, and verify ord₂₁(2) = 6. (The paper's benchmark instance.)

**Exercise 0.11.** Prove φ is multiplicative on coprime arguments
directly from CRT, and evaluate the formula
φ(p^k) = p^k − p^{k−1}.

**Exercise 0.12.** Show that (Z/N)* is *not* always cyclic (N = 15
suffices), so "order of the group" and "maximal element order" can
differ — the gap the N = 15 pathology lives in.

## 0.6 Fields, and why Z_p is one

**Definition 0.17 (Field).** A commutative ring in which every nonzero
element has a multiplicative inverse.

**Theorem 0.8.** Z_d is a field iff d is prime.

*Proof.* If d = ab nontrivially, then ab ≡ 0 with a, b ≢ 0 — zero
divisors, so no inverse for a. If d = p prime, every a ∈ {1,…,p−1} is
coprime to p, so Theorem 0.5 supplies the inverse. ∎

Over a field, linear algebra works verbatim (unique solutions, ranks,
no zero divisors). That single fact powers everything "special" about
prime dimension in §2 — mutually unbiased bases, the stabilizer
formalism, discrete phase space, and the invertible-multiplier
arithmetic of the QFT constructions. Where the *ring* structure
suffices — and §2.1 shows the paper's dynamics only ever uses the ring
— primality buys nothing, a distinction the composite-d controls
measure directly.

**Exercise 0.13.** Solve 3x ≡ 5 in Z₇ and show 3x ≡ 5 has no solution
in Z₆. Which step of Gaussian elimination fails in Z₆?

## 0.7 The matrix exponential

Continuous-time noise (Part IV) is generated: channels appear as
exp(𝓛t). We need the exponential of a (possibly non-Hermitian) matrix
and three of its properties.

**Definition 0.18.** e^A = Σ_{k≥0} A^k / k!. The series converges
absolutely for every square matrix (bound ‖A^k‖ ≤ ‖A‖^k by
submultiplicativity; compare with the scalar series).

**Theorem 0.9.** (i) If AB = BA then e^{A+B} = e^A e^B.
(ii) d/dt e^{tA} = A e^{tA}.
(iii) det e^A = e^{tr A}; in particular e^A is always invertible.

*Proof.* (i) Expand e^A e^B by the Cauchy product and regroup with the
binomial theorem — the regrouping needs commutativity. (ii)
Differentiate the series term by term (uniform convergence on compact
t-intervals justifies it). (iii) For diagonalizable A it is the
product of eigenvalue exponentials; diagonalizable matrices are dense
and both sides are continuous. ∎

The *failure* of (i) for noncommuting A, B is not a nuisance here —
the repository never Trotterizes. Each noise layer is exp(𝓛 · t)
evaluated *exactly*, and fractional gate costs use the semigroup
property exp(𝓛t₁)exp(𝓛t₂) = exp(𝓛(t₁+t₂)) — which *is* case (i),
A and B being multiples of the same generator.

**Exercise 0.14.** Compute e^{iθZ} for Z = diag(1, ω, ω², …) via
Definition 0.7, and check it against the series definition. (They
agree on normal matrices — why?)

**Exercise 0.15.** Find 2×2 matrices with e^{A+B} ≠ e^Ae^B.

---
---

# Part I — The qudit

## 1. Hilbert space, basis, and the generalized Pauli group

**Definition 1.1 (Qudit).** A qudit of dimension *d* is a quantum
system with state space ℋ_d ≅ ℂ^d and a distinguished orthonormal
*computational basis* {|0⟩, |1⟩, …, |d−1⟩}. At d = 2 this is a qubit;
d = 3 a **qutrit**; d = 5 a **ququint**.

The labels are elements of Z_d, and that is the point: the basis
carries the arithmetic of the ring Z_d (§0.5), and every gate below is
defined by what it does to those labels.

### 1.1 The two generators

**Definition 1.2 (Shift and clock).** With ω = e^{2πi/d} a primitive
d-th root of unity,

    X|j⟩ = |j + 1 mod d⟩          Z|j⟩ = ω^j |j⟩.

**Theorem 1.1 (Basic algebra of X and Z).**
(i) X and Z are unitary, of order d: X^d = Z^d = 𝟙.
(ii) Neither is Hermitian for d > 2; at d = 2 they are the Pauli
matrices σ_x, σ_z.
(iii) **Weyl relation:** ZX = ω XZ, and more generally
X^a Z^b = ω^{−ab} Z^b X^a.

*Proof.* (i) X permutes an orthonormal basis and Z rephases it — both
manifestly norm-preserving, hence unitary (Definition 0.5); the d-th
power returns every label and every phase to the start
(ω^d = 1). (ii) X† shifts down, ≠ X unless d = 2; Z† has entries
ω^{−j} ≠ ω^j unless ω is real. (iii) Evaluate both sides on |j⟩:
ZX|j⟩ = Z|j+1⟩ = ω^{j+1}|j+1⟩ while XZ|j⟩ = ω^j|j+1⟩. The general form
follows by induction, moving one Z past one X at a time and counting
the ω's: ab of them. ∎

**Theorem 1.2 (The generalized Pauli basis).** The d² operators
{X^a Z^b : a, b ∈ Z_d} are orthogonal in the Hilbert–Schmidt inner
product (Definition 0.8):

    tr( (X^a Z^b)† X^{a′} Z^{b′} ) = d · δ_{aa′} δ_{bb′},

and therefore form a basis of the operator space (Exercise 0.5).

*Proof.* Compute the trace in the computational basis. (X^a Z^b)†
X^{a′}Z^{b′} = Z^{−b}X^{a′−a}Z^{b′} up to a phase (Weyl relation), and
⟨j| Z^{−b} X^{a′−a} Z^{b′} |j⟩ = ω^{j(b′−b)} ⟨j|j + a′−a⟩. The matrix
element vanishes unless a′ = a; then the trace is
Σ_j ω^{j(b′−b)} = d δ_{bb′} by root-of-unity orthogonality
(Exercise 0.2). ∎

Consequently *any* operator on ℋ_d — and in particular any noise
process — expands in generalized Paulis. That expansion is how the
depolarizing channel of §18 is built, and why "Pauli twirling"
survives the trip to qudits.

### 1.2 Why "generalized Pauli" and not "Pauli"

For d > 2 the group generated by X and Z contains phases ω^k, so it is
not a group of Hermitian observables — one genuinely loses the
"unitary *and* Hermitian" coincidence of the qubit. The physically
meaningful object is the group modulo phases, of order d². Its
normalizer in the unitary group is the **Clifford group** — the qudit
generalization of {H, S, CNOT} — and the structure of that group is
what makes prime d special, next.

**Exercise 1.1.** Verify ZX = ωXZ on d = 3 explicitly as 3×3
matrices, and write out X² Z² in matrix form.

**Exercise 1.2.** Show that the eigenvalues of X are the d-th roots of
unity, and find its eigenvectors. (You are one Fourier transform away
from §5; compare after reading it.)

---

## 2. Why *prime* d is special — and where it is irrelevant

All the reasons reduce to one algebraic fact, proved as Theorem 0.8:
**Z_d is a field iff d is prime.**

**Consequence 1 — Mutually unbiased bases.** Two orthonormal bases
{|a_i⟩}, {|b_j⟩} are *mutually unbiased* if |⟨a_i|b_j⟩|² = 1/d for all
i, j. For prime d there exist exactly **d + 1** of them — the maximum
any dimension allows — constructed from the eigenbases of
{Z, X, XZ, XZ², …, XZ^{d−1}}; the proof that these are pairwise
unbiased is a Gauss-sum evaluation that needs every nonzero multiplier
invertible, i.e. the field property. For composite d the maximal
number is open (unknown already at d = 6). MUBs are the measurement
backbone of tomography and of many error-correction constructions.

**Consequence 2 — Stabilizer codes close.** A stabilizer code is an
abelian subgroup of the generalized Pauli group. Over a field the
subgroup ↔ subspace correspondence is clean and the qubit machinery —
symplectic representation, CSS constructions, Gottesman–Knill —
transfers verbatim; Gottesman's 1998 higher-dimensional fault
tolerance is stated for prime d for exactly this reason
(`papers/gottesman-1998-*.pdf`). At d = 4 one recovers structure via
the field GF(4); at d = 6 there is no field and the machinery
genuinely breaks.

**Consequence 3 — Clean discrete phase space.** For odd prime d the
discrete Wigner function is non-negative exactly on stabilizer states,
giving a sharp resource-theoretic notion of "magic"
(`papers/gross-2006-*.pdf`). At d = 2 state-independent contextuality
intervenes; at composite d the phase space does not factor.

**Consequence 4 — QFT arithmetic assumes it.** The in-place
multipliers, quadratic-phase operators and fractional Fourier
transforms of Floratos–Pavlidis assume odd prime d, where every
nonzero multiplier is invertible — the field property again. This is
the same construction that supplies the `pavlidis` cost model (§3.3),
so primality enters this book twice: once through fault tolerance,
once through the arithmetic whose compilation cost decides the
verdict.

### 2.1 …and why primality plays **no role** in this paper's dynamics

Stated loudly, because it is a result of the work and a frequent
misreading. The circuits simulated here — Fourier gates, controlled
phases, controlled modular multipliers, Grover diffusers — use only
the *ring* Z_d. Nothing in the noise channels uses primality either.
So the bare, uncorrected dynamics should not care whether d is prime,
and the paper's composite controls confirm it: d = 4 and d = 6 both
land inside the qudit band (§23).

Primality is inherited from the **fault-tolerance and QFT-arithmetic
motivations** — the reasons anyone wants prime-dimensional hardware —
not from the algorithm-level physics measured here. Keep the two
separate.

**Exercise 2.1.** Construct the d + 1 = 3 mutually unbiased bases for
the qubit (eigenbases of Z, X, XZ = −iY) and verify unbiasedness by
hand.

**Exercise 2.2.** Where exactly does the MUB construction for the
eigenbases of XZ^k use invertibility mod d? Try to run it at d = 6
and watch which step fails.

---

## 3. Gates, and what a two-qudit gate costs

### 3.1 Single-qudit gates

**Definition 3.1 (Fourier gate).**

    F_d |j⟩ = (1/√d) Σ_{k=0}^{d−1} ω^{jk} |k⟩.

**Theorem 3.1.** F_d is unitary, and F_d† X F_d = Z.

*Proof.* Unitarity: the columns of F_d have inner products
(1/d)Σ_k ω^{(j′−j)k} = δ_{jj′} by root-of-unity orthogonality.
Diagonalization: evaluate on |j⟩. XF_d|j⟩ = (1/√d)Σ_k ω^{jk}|k+1⟩ =
(1/√d)Σ_k ω^{j(k−1)}|k⟩ = ω^{−j} F_d|j⟩. So F_d maps |j⟩ to an
eigenvector of X with eigenvalue ω^{−j}; equivalently
F_d† X F_d |j⟩ = ω^{−j}|j⟩. This is Z up to relabeling
(Z† = Z^{d−1} conventions differ by a harmless inverse; the repository
fixes F_d† X F_d = Z with the sign conventions of `qudit_shor.py`, and
Exercise 3.1 asks you to chase them). ∎

At d = 2, F₂ = H. Applying F_d to |0⟩ gives the uniform superposition
— the initialization of every algorithm here. Also used: diagonal
**phase gates** diag(1, e^{iθ₁}, …, e^{iθ_{d−1}}), which supply the
controlled rotations of the QFT.

### 3.2 Two-qudit gates

**Definition 3.2.** The entangling primitive is the **controlled
phase** CP(θ)|j⟩|k⟩ = e^{iθjk}|j⟩|k⟩, and, for order finding, the
**controlled modular multiplier** |c⟩|x⟩ ↦ |c⟩|a^c x mod N⟩.

In this repository the multiplier is applied as an *exact unitary* —
it is not compiled into elementary gates — but it is *charged* the
cost of the carriers it spans. That accounting distinction is the
subject of the next subsection and, ultimately, of the paper's whole
result.

### 3.3 The cost question, stated early

Here is the crux, and it is a hardware question, not a mathematical
one. A base-d register needs fewer carriers and fewer time-layers than
a base-2 register at the same problem size (§4) — a **rebate**. But a
two-qudit entangling gate on real hardware may cost more than a
two-qubit gate, by a factor growing with d — a **surcharge**. Whether
the qudit wins is whether the rebate exceeds the surcharge.

Three published cost structures bracket the possibilities, charged as
multipliers on the layer count:

| model | charge per **two-qudit** gate | single-qudit gate | physical realization |
|---|---|---|---|
| `uniform` | 1 layer, any d | 1 layer | native entangler — cross-Kerr CZ on transmons |
| `ion` | d − 1 layers | 1 layer | Ringbauer's 2(d−1) Mølmer–Sørensen pulse construction, normalized to 1 at d = 2 |
| `pavlidis` | d²/4 layers | 1 layer | two-level (Givens-style) decomposition of the QFT-arithmetic controlled rotations |

Note the scope of the `pavlidis` charge: **d²/4 applies to the
two-qudit controlled rotations only.** The d² count in
Pavlidis–Floratos is the two-level decomposition cost of a
*controlled* rotation; a single-qudit rotation decomposes into O(d)
two-level gates, not O(d²), so single-qudit gates stay at one layer
and their measured cost is priced separately (§23, the single-qudit
charge). An earlier version of the repository charged all gates the
multiplier; the corrected accounting re-scored every `pavlidis` cell
in the current paper.

The d²/4 is still deliberately generous to the qudit: the actual
decomposition costs 4(d−1)² elementary two-level gates per controlled
rotation — (d−1)² after the d = 2 normalization, i.e. 4 at d = 3 and
16 at d = 5, against the 2.25 and 6.25 charged. **Verdicts against
decomposed gates are therefore conservative.** A 2024 follow-up by the
same authors reports the same d² scaling in *depth* (not merely count)
for a full QFT-based in-place modular multiplier under 1D-local
connectivity, which is what licenses treating `pavlidis` as a uniform
layer multiplier on the entangling gates.

On the benchmark instance (N = 21) the three models swing the ququint
circuit from **3.8× shorter** than the qubit's to **1.1× longer**:

    layers (d = 2 / 3 / 5)
    uniform    57 / 26   / 15
    ion        57 / 44   / 42
    pavlidis   57 / 48.5 / 62.2

That swing — a factor of four in ququint depth — is larger than
anything the noise model does. Hold this table in mind; §22 is
essentially its consequence.

**Exercise 3.1 (★).** Chase the Fourier conventions: with
Definition 3.1, is F_d† X F_d equal to Z or Z†? Reconcile with
`qudit_shor.py`.

**Exercise 3.2 (★).** Reproduce the layer counts: 57/26/15 under
`uniform`, then apply d − 1 to the entangling gates for `ion`
(57/44/42) and d²/4 for `pavlidis` (57/48.5/62.2). You will need the
circuit structure of §5–7; return to this exercise after them.

---

## 4. Registers: width, depth, and qubit-equivalents

### 4.1 Width

To hold an integer < N you need w = ⌈log_d N⌉ carriers. For N = 21:
w = 5 (d = 2), 3 (d = 3), 2 (d = 5). A control register of dimension D
needs m = log_d D carriers. **Width compression is exactly a factor
log₂ d**: a base-d register uses 1/log₂ d as many carriers as a qubit
register at the same Hilbert-space dimension.

### 4.2 Depth

The controlled-U^{d^i} chain has m gates rather than the qubit's
log₂ D, and the inverse QFT has m(m−1)/2 controlled rotations rather
than the qubit's larger triangle. Both shrink with d. **Depth
compression is roughly (log₂ d)²** before cost models are applied,
because the number of control digits *and* the QFT triangle both
shrink.

### 4.3 Qubit-equivalents

Cross-base comparisons index everything by

    qubit-equivalents = log₂ dim ℋ = log₂ (D · d^w).

The deepest register in the paper is d = 3, m = 9, w = 3:
dim ℋ = 3¹² = 5.3 × 10⁵ ≈ **19.0 qubit-equivalents**. The widest
*qubit* register run is 17 carriers. Different numbers describing the
same axis; conflating them is a standard reporting error.

### 4.4 The exposure width and depth buy

Total noise exposure (defined precisely in §20) is
carriers × time-layers. At matched problem size, going d = 2 → 5
compresses Shor's exposure by **10.9×** and Grover's by only **5.7×**
— a contrast the paper uses as an experimental knob (§9.2).

**Exercise 4.1 (★).** Reproduce the 11/7/5 total carrier counts for
N = 21 at D ≥ 64, and the 10.9×/5.7× exposure compressions.

---
---

# Part II — The algorithms

## 5. The Fourier transform over Z_D

### 5.1 Definition and unitarity

**Definition 5.1.** For a control register of m base-d carriers, label
the computational basis by Z_D, D = dᵐ, via the positional expansion

    |y⟩ = |y_{m−1}⟩ ⊗ ⋯ ⊗ |y_0⟩,     y = Σ_i y_i d^i.

The **quantum Fourier transform over Z_D** is

    QFT_D |x⟩ = (1/√D) Σ_{y=0}^{D−1} ω_D^{xy} |y⟩,   ω_D = e^{2πi/D}.

Unitarity is the same computation as Theorem 3.1: columns are
orthonormal by root-of-unity orthogonality with D in place of d.

### 5.2 The factorized (circuit) form, derived

The single fact that makes QFT_D a *circuit* — a polynomial number of
one- and two-carrier gates — is that the phase ω_D^{xy} factorizes
across the digits of y.

**Theorem 5.1 (QFT factorization).** Writing y = Σ_i y_i d^i,

    QFT_D |x⟩ = ⨂_{i=m−1}^{0} [ (1/√d) Σ_{y_i=0}^{d−1}
                  exp( 2πi · x · y_i / d^{m−i} ) |y_i⟩ ],

and each single-digit factor depends only on the last m − i digits of
x. Consequently QFT_D is implemented by m Fourier gates F_d and
m(m−1)/2 two-carrier controlled phases CP(2π/d^k), k = 2…m, with the
output digits emerging in reversed order.

*Proof.* Substitute the digit expansion of y into ω_D^{xy}:

    ω_D^{xy} = exp(2πi x Σ_i y_i d^i / dᵐ) = Π_i exp(2πi x y_i / d^{m−i}).

The double sum over y = (y_{m−1},…,y_0) of a product of single-digit
phases factorizes into a product of single-digit sums, which is the
tensor-product form. For the digit dependence: in the i-th factor the
phase is x y_i / d^{m−i} (mod 1), and writing x = Σ_j x_j d^j, the
terms with j ≥ m − i contribute integer multiples of y_i — no phase.
So the factor sees only x_0, …, x_{m−i−1}: the digit x_{m−i−1}
contributes through F_d (angle 2π x_{m−i−1} y_i / d), and each lower
digit x_j through a controlled phase between carriers j and i with
angle 2π/d^{m−i−j} — a gate controlled on a *different* carrier's
value, which is exactly CP. Counting: one F_d per output digit and one
CP per ordered pair, m(m−1)/2 in all. ∎

This derivation is worth doing once by hand at d = 2, m = 3 —
Exercise 5.1 — after which the base-d case holds no surprises: the
qudit QFT is not a generalization that needs new ideas, just the same
positional arithmetic in a different base. What changes is the *count*:
the triangle m(m−1)/2 shrinks quadratically as d grows at fixed D.

### 5.3 The no-swap convention

Textbook presentations append m/2 SWAPs to undo the digit reversal of
Theorem 5.1. This repository does **not**: the reversal is absorbed
into the classical reading of the outcome. Two reasons, one principled
and one earned on hardware:

- SWAPs are three entangling gates each and would be charged as such,
  penalizing whichever base has more carriers — i.e. d = 2. Dropping
  them is the *conservative* choice for the qudit claim.
- Different devices reverse in different directions. IonQ Forte-1
  returns the control register digit-reversed relative to the Braket
  local simulator; the m = 5 hardware peak sits exactly on the
  bit-reversed ideal outcome. Getting this wrong looks exactly like a
  failed experiment (§23.5).

### 5.4 Approximate QFT

The controlled rotation between digits i and j has angle
2π/d^{j−i+1}, decaying geometrically with digit separation. Dropping
all rotations beyond separation k (the **AQFT**) costs little fidelity
and saves many gates — a base-2 result of Barenco et al. and Nam–Kim
that Pavlidis and Floratos conjectured extends to qudits. The paper
tests it on hardware once (dropping the three smallest angles at
m = 7, 25 entangling gates instead of 28) and finds it recovers a
factor ~6 but cannot repair a *coherent* failure — a datum adjacent to
that conjecture, not a test of it (§23.5).

**Exercise 5.1 (★).** Derive Theorem 5.1 explicitly for d = 2, m = 3,
drawing the circuit, and identify which controlled phase carries which
angle.

**Exercise 5.2 (★★).** Bound the error of the AQFT: show the operator
norm of the difference between QFT and its separation-k truncation is
at most Σ over dropped gates of their angles (each dropped CP(θ)
differs from 𝟙 by at most |θ| in operator norm). Evaluate for d = 2,
m = 7, k = 4.

---

## 6. Phase estimation, derived

### 6.1 The problem

Given a unitary U, an eigenstate |u⟩ with U|u⟩ = e^{2πiφ}|u⟩, and the
ability to apply controlled-U^k, estimate φ ∈ [0, 1).

### 6.2 The circuit and its output distribution

**The circuit.** Prepare m control carriers in |0⟩^{⊗m}, apply
F_d^{⊗m} to reach the uniform superposition, apply controlled-U^{d^i}
from control carrier i (so control value x applies U^x in total), then
QFT_D†, then measure the control register.

**Theorem 6.1 (Output distribution: the Fejér kernel).** With
δ_y = φ − y/D, the probability of outcome y is

    P(y) = (1/D²) · sin²(π D δ_y) / sin²(π δ_y),

with the limiting value P(y) = 1 when δ_y = 0.

*Proof.* Track the state. After the Fourier layer:
(1/√D) Σ_x |x⟩|u⟩. The controlled powers put U^x on the work register:
since |u⟩ is an eigenstate, this is a pure phase,

    (1/√D) Σ_x e^{2πiφx} |x⟩ |u⟩

— note the work register is *unchanged and unentangled*; the phase has
"kicked back" onto the control. Apply QFT_D† (the inverse of
Definition 5.1) and read off the amplitude of |y⟩:

    A(y) = (1/D) Σ_{x=0}^{D−1} e^{2πix(φ − y/D)} .

This is a geometric series with ratio e^{2πiδ_y}: summing,
|A(y)|² = (1/D²) |1 − e^{2πiDδ_y}|² / |1 − e^{2πiδ_y}|², and
|1 − e^{iθ}|² = 4 sin²(θ/2) gives the kernel. ∎

Three properties of the kernel do all the work in this book:

**Corollary 6.2 (Exact hit).** If φ = y₀/D exactly, P(y₀) = 1: the
distribution is a delta function. (All D terms of the series align.)

**Corollary 6.3 (Worst case).** For any φ, the nearest grid point y*
(|δ_{y*}| ≤ 1/2D) has P(y*) ≥ 4/π², and the two nearest together
carry ≥ 8/π².

*Proof.* On |δ| ≤ 1/2D the numerator sin²(πDδ) ≥ (2Dδ)² · (π/2)²
… the clean route: use sin θ ≥ 2θ/π on [0, π/2] for the numerator's
argument πD|δ| ≤ π/2, and sin θ ≤ θ for the denominator:

    P ≥ (1/D²) · (2Dδ)² / (πδ)² = 4/π².

For the pair statement apply the same bound to the two grid points
flanking φ, whose offsets sum to 1/D. ∎

**Corollary 6.4 (Tails).** For |δ_y| ≫ 1/D, P(y) ≤ 1/(D sin πδ_y)² ≈
1/(πDδ_y)²: the peak is **~1 outcome wide no matter how large D
grows**. Hold that thought — §12 contrasts it with a decoder
acceptance set that grows *linearly* in D, and the tension between
those two growth rates is the mechanism behind the paper's scaling
plateau.

### 6.3 The eigenstate benchmark

The paper's QPE benchmark takes U diagonal with target phase the
golden-ratio conjugate φ* = (√5 − 1)/2 ≈ 0.6180339887 — the "most
irrational" number, whose continued fraction is [0; 1, 1, 1, …]
(Exercise 8.2), hence badly approximable by small-denominator
fractions in *any* base. That makes eigenstate QPE **structurally
immune to the grid-alignment confound of §10**, which is exactly why
it is in the paper: it is the control against which the Shor results
are checked. Success criterion: the estimate lands within 2^{−(b+1)}
of φ*, at b = 5 bits.

**Exercise 6.1.** Fill in the sin-bound details of Corollary 6.3, and
show the constant 4/π² is attained in the limit D → ∞ with φ exactly
between grid points.

**Exercise 6.2 (★★).** Show that measuring the control register of the
QPE circuit *without* the inverse QFT yields a uniform distribution,
independent of φ. (Moral: the QFT is where the information becomes
readable; the kickback only stores it.)

---

## 7. Order finding: why Shor *is* phase estimation

### 7.1 The problem

Given N and a coprime to N, find r = ord_N(a) (Definition 0.16). This
is the quantum core of Shor's factoring algorithm; the reduction from
factoring to order finding is classical and not simulated here.

### 7.2 The eigenstates of the multiplier

**Theorem 7.1.** Let U_a|x⟩ = |ax mod N⟩ act on work-register states
labelled by Z_N. For s ∈ {0, …, r−1} define

    |u_s⟩ = (1/√r) Σ_{k=0}^{r−1} e^{−2πisk/r} |a^k mod N⟩.

Then (i) U_a|u_s⟩ = e^{2πis/r}|u_s⟩, and
(ii) (1/√r) Σ_{s=0}^{r−1} |u_s⟩ = |1⟩.

*Proof.* (i) U_a maps |a^k⟩ ↦ |a^{k+1}⟩, so it shifts the sum's index:

    U_a|u_s⟩ = (1/√r) Σ_k e^{−2πisk/r} |a^{k+1}⟩
             = e^{2πis/r} (1/√r) Σ_k e^{−2πis(k+1)/r} |a^{k+1}⟩,

and the relabelled sum k+1 → k runs over the same r states because
a^r ≡ 1 closes the cycle. (ii) Sum over s first:
Σ_s e^{−2πisk/r} = r δ_{k0} by root-of-unity orthogonality, leaving
only the k = 0 term, |a^0⟩ = |1⟩. ∎

So |u_s⟩ is an eigenstate with phase s/r, and phase estimation on it
returns an approximation to s/r — from which r is recovered by §8.

### 7.3 The trick: |1⟩ is all of them at once

We cannot prepare |u_s⟩ — that would require knowing r. But
Theorem 7.1(ii) says the trivially preparable |1⟩ *is* the equal
superposition of all r eigenstates. Running phase estimation on
|x = 1⟩ therefore runs it on all r phases simultaneously, and the
measurement statistics are an equal mixture: the output distribution
is the Fejér kernel of Theorem 6.1 **centred on each of the r phases
s/r, with weight 1/r each**. (Why an incoherent mixture and not an
interference pattern: distinct |u_s⟩ are orthogonal and remain
distinguishable in the work register, so the cross terms vanish at
readout — Exercise 7.1.)

This is the sense in which *Shor is phase estimation*, and it is an
exact statement about the same circuit with a different input — not an
analogy.

### 7.4 The interpolation experiment (a falsified hypothesis)

Because |1⟩ is a K = r-fold eigenstate superposition and a true
eigenstate is K = 1, one can interpolate between eigenstate QPE and
Shor by preparing a K-fold subset superposition, with circuit, metric,
noise, and cost all held fixed. The control–work entanglement entropy
is then exactly log₂ K bits.

The early hypothesis of this project was that the Shor/QPE performance
difference was *caused* by which-path dephasing through that
entanglement. The interpolation experiment
(`interpolation_experiment.py`, slopes in `interpolation_slopes.py`)
measures the effect at ≈ −0.025 signal per bit — real, reproducible in
all four noise/cost conditions, and an **order of magnitude too
small** to explain the ≈ 0.5 gap it was invented for. Hypothesis
falsified. The study covers 2.0 of the demo instance's 2.6 entropy
bits, so it is an interpolation, not a full extrapolation — stated in
the paper with exactly that scope.

It stays in this book because chasing the falsification is what
exposed grid alignment (§10), which overturned the study's original
conclusion. That is what a control is *for*.

### 7.5 Benchmark instances

| N | a | r | why |
|---|---|---|---|
| 15 | any | 1, 2, 4 | **pathological — do not use** (§0.5 worked example; §10.2) |
| 21 | 2 | 6 | unbiased; mild residual tilt *toward* the qubit (0.267 vs 0.300) |
| 29 | 16 | 7 | exactly alignment-neutral across d = 2, 3, 5 (0.2857 each) — the recommended benchmark |
| 33, 55 | various | 5, 10 | within-modulus alignment controls (§10.3) |

**Exercise 7.1.** Complete the mixture argument of §7.3: show that for
orthogonal eigenstates the control-register outcome distribution is
the weighted sum of per-eigenstate distributions, with no cross terms.

**Exercise 7.2.** Show (Z/15)* ≅ Z₂ × Z₄ via CRT (Theorem 0.7) and
conclude every order divides 4. *The whole N = 15 pathology in one
line.*

---

## 8. Continued fractions, with proofs

Order finding hands us y/D near some s/r; recovering the rational s/r
from its noisy neighbour is the entire classical half of Shor. That
recovery runs on three theorems, proved here in full because Part III
stands on them.

### 8.1 The algorithm and the recurrences

**Definition 8.1.** For x ∈ (0, 1), the continued fraction expansion
x = [0; a₁, a₂, …] is produced by

    x₀ = x;   a_k = ⌊1/x_{k−1}⌋,  x_k = 1/x_{k−1} − a_k,

stopping when x_k = 0 (which happens iff x is rational — the a_k
recursion is the Euclidean algorithm of Theorem 0.4 applied to
numerator and denominator, and Euclid terminates). The truncations
p_k/q_k = [0; a₁, …, a_k] are the **convergents**.

**Theorem 8.1 (Convergent recurrences).** With p_{−1} = 1, q_{−1} = 0,
p₀ = 0, q₀ = 1:

    p_k = a_k p_{k−1} + p_{k−2},    q_k = a_k q_{k−1} + q_{k−2},

and the determinant identity p_k q_{k−1} − p_{k−1} q_k = (−1)^{k−1}
holds; in particular gcd(p_k, q_k) = 1 — convergents are automatically
in lowest terms.

*Proof.* Induction on k, on the stronger statement that for any real
t > 0, [0; a₁,…,a_{k−1}, t] = (t p_{k−1} + p_{k−2}) /
(t q_{k−1} + q_{k−2}). Base cases check directly. Inductive step:
[0; a₁,…,a_k, t] = [0; a₁,…, a_k + 1/t], and substituting a_k + 1/t
for t in the inductive hypothesis and clearing 1/t reproduces the same
form one level deeper. Setting t = a_k gives the recurrences. The
determinant identity follows by induction: the recurrence step
multiplies the 2×2 matrix (p_k p_{k−1}; q_k q_{k−1}) on the right by
(a_k 1; 1 0), whose determinant is −1. A common divisor of p_k, q_k
would divide the determinant ±1. ∎

**Theorem 8.2 (Best approximation).** Convergents alternate around x
and satisfy

    | x − p_k/q_k | < 1 / (q_k q_{k+1}) ≤ 1 / q_k².

*Proof.* By the t-form above with the exact tail t = 1/x_k:
x = (t p_k + p_{k−1})/(t q_k + q_{k−1}), so

    x − p_k/q_k = [ (t p_k + p_{k−1}) q_k − p_k (t q_k + q_{k−1}) ]
                  / [ q_k (t q_k + q_{k−1}) ]
                = (−1)^k / [ q_k (t q_k + q_{k−1}) ],

using the determinant identity. Since t > a_{k+1} ≥ 1, the denominator
exceeds q_k(a_{k+1} q_k + q_{k−1}) = q_k q_{k+1}. The sign (−1)^k gives
the alternation. ∎

### 8.2 Legendre's theorem — the converse Shor uses

**Theorem 8.3 (Legendre).** If gcd(p, q) = 1 and

    | x − p/q | < 1/(2q²),

then p/q is a convergent of x.

*Proof.* Write x − p/q = εθ/q² with ε = ±1 and 0 < θ < 1/2 (the case
x = p/q is trivial: a rational is its own last convergent). Expand p/q
as a *finite* continued fraction [0; a₁, …, a_k] — and here is the one
degree of freedom the proof needs: the expansion can be chosen with k
of either parity, because [0; …, a_k] = [0; …, a_k − 1, 1] when
a_k ≥ 2 (and [0; …, a_{k−1}, 1] = [0; …, a_{k−1}+1] in the other
direction). Choose the parity so that (−1)^k = ε, matching the side on
which x sits.

Now define t from x = (t p_k + p_{k−1}) / (t q_k + q_{k−1}) — solving,

    t = ( p_{k−1} − x q_{k−1} ) / ( x q_k − p_k ).

Substituting x = p_k/q_k + εθ/q_k² and using the determinant identity
to simplify the numerator:

    t = q_k/(θ q_k) − q_{k−1}/q_k · (…) — carried through, 
    t = 1/θ − q_{k−1}/q_k.

Since θ < 1/2 and q_{k−1} ≤ q_k, we get t > 2 − 1 = 1. A number with
x = (t p_k + p_{k−1})/(t q_k + q_{k−1}) and t > 1 has continued
fraction [0; a₁, …, a_k, b₁, b₂, …] where [b₁; b₂, …] is the expansion
of t — i.e. the expansion of x *begins* with a₁ … a_k, so p/q = p_k/q_k
is a convergent of x. ∎

The parity trick is the entire subtlety; everything else is the
determinant identity used twice. Exercise 8.1 asks for the two
algebra steps compressed above.

### 8.3 Applying it to order finding

Phase estimation returns y with y/D within 1/2D of some s/r
(Corollary 6.3 gives this with probability ≥ 8/π² per phase). For
Legendre's theorem to certify s/r as a convergent of y/D we need

    1/(2D) < 1/(2r²)   ⟺   D > r².

Since r < N, taking D ≥ N² is sufficient — the textbook requirement.
The demo registers in this repository (D = 64–125 against N = 21) are
deliberately **below** that bar. This is not sloppiness: it is what
makes the random-outcome floor non-negligible and forces the honest
floor-corrected metric of §21; all bases are held to the same rule,
and the scaling sweeps run far above N².

### 8.4 Divisor recovery vs returning r itself

Legendre certifies the **reduced** fraction (s/g)/(r/g), g = gcd(s,r):
its denominator is a *divisor* of r, not r. Standard analyses (Shor's
4/π² bound, Gerjuoy, Bourdon–Williams, Ekerå, Magdon-Ismail–Dong)
certify divisor recovery and then lift to r by classical search over
multiples.

This repository's decoder does something different, and the difference
is the subject of Part III:

> **The decoder.** On outcome y ∈ [1, D), scan the convergents p/q of
> y/D in order of increasing denominator. At the **first** q ≤ N with
> a^q ≡ 1 (mod N), return the least r′ dividing q with a^{r′} ≡ 1
> (mod N). If no convergent denominator q ≤ N passes, **reject**
> (y = 0 always rejects).

It performs no lift. It succeeds precisely on convergent denominators
that are *already* multiples of r — including the deep ones 2r, 3r,
…, ⌊N/r⌋r that lie outside any sufficient-condition window. That is
why its acceptance set has an exact closed form, and why that form is
a **totient sum** rather than a window count (§12).

**Exercise 8.1.** Complete the two compressed algebra steps in the
proof of Theorem 8.3 (the simplification of t, and the claim that
t > 1 implies the expansion of x extends that of p/q).

**Exercise 8.2.** Show the golden-ratio conjugate satisfies
x = 1/(1+x), conclude its continued fraction is [0; 1, 1, 1, …], and
compute its first six convergents (ratios of Fibonacci numbers). Why
does q_{k+1} ≤ 2q_k for this x make it the *worst* case for
rational approximation?

**Exercise 8.3 (★★).** Implement the decoder in twenty lines and
verify on (N = 21, a = 2): which y ∈ [0, 64) are accepted? Check
|A| = 8 against `decoder_formula.py`.

---

## 9. Grover search in base d

### 9.1 The algorithm, and the rotation proof

Over M = dⁿ items with marked item |t⟩, alternate

    oracle    O = 𝟙 − 2|t⟩⟨t|
    diffuser  Dif = 2|ψ⟩⟨ψ| − 𝟙,   |ψ⟩ = (1/√M) Σ_x |x⟩.

**Theorem 9.1.** The two-dimensional subspace spanned by |t⟩ and |ψ⟩
is invariant under Dif·O, which acts on it as a rotation by
θ = 2 arcsin(1/√M); starting from |ψ⟩, the marked amplitude after k
iterations is sin((2k+1)·θ/2), maximized at k = ⌊(π/4)√M⌉.

*Proof.* Write |ψ⟩ = sin(θ/2)|t⟩ + cos(θ/2)|t̄⟩ with
|t̄⟩ ∝ |ψ⟩ − ⟨t|ψ⟩|t⟩ and sin(θ/2) = ⟨t|ψ⟩ = 1/√M. In the ordered
basis (|t⟩, |t̄⟩): O = diag(−1, 1) is reflection about |t̄⟩, and Dif
is reflection about |ψ⟩. The product of two reflections is a rotation
by twice the angle between the mirror lines, which is θ. The iterate
angle and optimum follow by reading off the component. ∎

Everything here is base-independent: **the iteration count √M does not
care about d.**

### 9.2 Why Grover is in this paper

Grover is the **falsification test** for the paper's mechanism, chosen
with the prediction registered in the source *before* the runs:
*qudits win, by less than in phase estimation.*

The logic: since the oracle count is fixed across bases (Theorem 9.1),
Grover's only compression is width and the narrower multi-qudit
decompositions — roughly half of Shor's exposure compression (5.7× vs
10.9×, §4.4). If the qudit advantage were an artifact of the
continued-fraction metric, Grover — which has no decoder at all —
would not show it. If the advantage were pure depth, Grover would show
none of it. Measured: Grover's advantage is **0.33–0.50 of Shor's**.
Compression is the mechanism, and the response is at least
proportional.

### 9.3 Grover as a methodological control

- **Grid alignment is structurally impossible** for it (no orders, no
  fractions). Its agreement with the Shor ordering rules out the
  continued-fraction metric as the source of the effect.
- **Its "decoder" is the identity** — the signal *is* marked-state
  survival. That makes it the clean baseline of §15: Grover's fidelity
  equals its signal to within 0.006 (ladder) / 0.025 (depolarizing) at
  every measured point, while Shor's emphatically does not.

### 9.4 The size-matching trap

M = dⁿ never matches across bases (8, 9, 25, …), and comparing raw
demo-size points **reverses orderings**. All cross-base comparisons
interpolate onto a common log₂-size axis. This is the second of the
paper's two fairness traps; alignment is the first.

The multi-qudit oracle and reflection are applied as exact unitaries
but **charged their (n−1)-layer decomposition depth**; charging them
one layer would hand the largest free ride to the base packing the
most carriers into one gate — which is d = 2.

**Exercise 9.1.** Prove that the product of reflections about two
lines at angle α is a rotation by 2α (the plane-geometry input to
Theorem 9.1).

**Exercise 9.2 (★★★).** Implement base-d Grover, confirm the optimal
iteration count, and reproduce the 5.7× exposure compression. Compare
`grover.py`.

---
---

# Part III — The number theory

This part and Part IV contain the derivations original to this work.
The mathematics is elementary — everything rests on Part 0.5 and the
three theorems of §8 — but the *questions* are ones the literature had
not asked, because they only arise when you compare decoders across
bases.

## 10. Grid alignment

### 10.1 The observation

Phase estimation concentrates probability on the phases s/r
(Theorem 6.1 applied per §7.3). Two regimes:

- **If r | D** (= dᵐ), every s/r is exactly a grid point y/D, and by
  Corollary 6.2 the peaks are delta functions — maximally robust to
  noise.
- **If r ∤ D**, the peaks smear over neighbouring outcomes according
  to the Fejér kernel, and smeared peaks degrade far faster under
  decoherence.

**Which base receives the sharp peaks is decided by arithmetic, not
physics.** Because prior qudit studies work at fixed d — where
alignment is a constant — the confound is invisible in the literature.

### 10.2 The N = 15 pathology

By Exercise 7.2, every order mod 15 is a power of two. A base-2
control register (D = 2ᵐ) is then *always* exactly aligned, and bases
3 and 5 never are. Any cross-dimension comparison on N = 15 —
including the first version of this study — hands base 2 a structural
gift that has nothing to do with decoherence. This is what produced,
and then destroyed, the original "qubits win Shor on transmons"
finding.

### 10.3 Quantifying it

**Definition 10.1 (Residual misalignment).** For base d on instance
(N, r) at control dimension D = dᵐ:

    misalign(d) = mean over s = 1…r−1 of dist(D·s/r mod 1, 0),

the mean distance of the target phases to the nearest grid point, in
grid units; 0 = aligned, 0.5 = worst case.

Three measurements price the confound (`grid_alignment.py`,
`same_n_control.py`, `ensemble_a.py`):

| test | isolates | result |
|---|---|---|
| one instance per alignment class, r = 3…7 | does alignment predict the winner? | 5 of 6 biased cells predicted (the N = 15 depolarizing cell misses by 1.4σ) |
| within-modulus control (N = 33, 55: r = 5 vs 10 on identical registers) | alignment at fixed width, depth, exposure | costs the ququint 0.14–0.22 signal; residual physical lead 0.38–0.57 |
| full multiplicative-group ensembles (all a ≠ 1 at N = 21, 33, 55) | what a real Shor user samples | qudit ordering preserved; aligned-over-unaligned excess +0.18 to +0.19 |

So alignment is worth ≈ 0.2 signal to whoever receives it, and the
remaining qudit lead is physical. Both effects are real; separating
them is the point.

### 10.4 The converse control does not exist

One would like the mirror test: a base-2-aligned instance with a
usable metric. It cannot be built. At every modulus large enough to
carry both r = 4 and a non-power-of-two order, the r = 4
continued-fraction **random floor exceeds its noiseless baseline**,
collapsing the metric (§21.3). N = 15 is the only qubit-aligned
instance with usable dynamic range — itself worth knowing. The paper
states the consequence honestly: the ≈ 0.2 price is measured only in
the ququint-aligned direction.

### 10.5 Alignment cannot drift with register size

**Theorem 10.1.** The multiset of grid offsets
{D·s/r mod 1 : s = 1…r−1} depends only on D mod r, and D = dᵐ mod r is
eventually periodic in m. Hence residual misalignment is (eventually)
periodic — it cannot drift monotonically with register size.

*Proof.* The offsets are determined by D mod r termwise. The sequence
dᵐ mod r lives in the finite set Z_r, so it repeats; once a value
recurs the recursion dᵐ⁺¹ = d·dᵐ makes it periodic from there
(immediately periodic with period ord_r(d) when gcd(d, r) = 1, by
Theorem 0.6). ∎

Measured (`misalignment_scaling.py`): misalignment is *exactly
constant* across the entire sweep for all three bases on both
instances — 0.267 (d=2) and 0.300 (d=3, 5) at N = 21, 0.2857 for
every base at N = 29 — to a spread < 10⁻¹¹, i.e. floating-point noise
on equal values. Alignment can therefore explain neither a
size-dependent nor a size-independent component of the scaling signal.

**Exercise 10.1 (★★).** Compute residual misalignment for
(N = 21, r = 6) at d = 2, 3, 5 and reproduce 0.267/0.300/0.300; then
(N = 29, r = 7), reproducing 0.2857 for all three.

**Exercise 10.2.** Where does the proof of Theorem 10.1 need
"eventually"? Give a (d, r) with gcd ≠ 1 whose offset sequence has a
pre-periodic head.

---

## 11. The decoder acceptance lemma

Everything in §12 rests on reducing the decoder (§8.4) to a purely
number-theoretic predicate.

**Lemma 11.1 (Acceptance lemma).** The decoder returns the order r of
a mod N **iff** some convergent denominator q of y/D satisfies q ≤ N
and r | q. On every other outcome it rejects. In particular it never
returns a wrong order.

*Proof.* The only number theory needed is Theorem 0.6:
a^q ≡ 1 (mod N) iff r | q.

(⇐) Suppose some convergent denominator q ≤ N has r | q. The scan
stops at the *first* such q (any earlier stopping denominator would
itself satisfy the multiple condition). Every divisor r′ of q with
a^{r′} ≡ 1 is a multiple of r (Theorem 0.6 again); r itself divides q
and passes; hence the least passing divisor is exactly r.

(⇒) If no convergent denominator q ≤ N is a multiple of r, then the
test a^q ≡ 1 never fires and the decoder rejects. ∎

**Why this matters.** The lemma converts a question about a *program*
("what does this decoder accept?") into a question about the continued
fraction of y/D — classical number theory. It also establishes
*soundness*: no accepted outcome is a false positive, so the
acceptance set is exactly the success set.

**Verification.** `decoder_formula.py` enumerates the decoder over
every outcome and compares against the convergent predicate:
bit-identical acceptance sets on 42 (instance, D) combinations.

**Exercise 11.1.** In the (⇐) direction, point to the exact step that
uses "r is the *order*" rather than merely "a^r ≡ 1". Construct a
failure if r were only an annihilating exponent.

---

## 12. The decoder acceptance law

### 12.1 The question

Define the acceptance set A = {y ∈ [0, D) : decode(y) = r}. How large
is it, and how does it grow with D and r?

The naive estimate: the sufficient-condition window of width 1/r²
around each of the r − 1 nonzero phases holds ~D/r² outcomes, so
|A| ≈ (r−1)D/r². We will see this is wrong in *both* variables — and
right on the benchmark instance by an accident of cancellation.

### 12.2 Measure first

`decoder_scaling.py` enumerates A exactly (no simulation):

| d | m | D | \|A\| | per peak | naive D/r² | law (§12.5) |
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

Read the per-peak column: 1.6 accepted outcomes at D = 64 growing to
116 at D = 4096 — a 73× gain in decoder tolerance, against an
interference peak that, by Corollary 6.4, **never widens**. That
single contrast is the mechanism behind Shor's scaling plateau
(§23.3): acceptance grows linearly in D (exponentially in m) while
noise-induced broadening grows only polynomially in m.

### 12.3 The structure of A: mediant intervals

By Lemma 11.1, y ∈ A iff some convergent denominator of y/D is
**admissible** — a multiple of r that is ≤ N:

    admissible denominators:  r, 2r, 3r, …, ⌊N/r⌋·r.

The classical fact needed is *which reals have a given fraction among
their convergents*:

**Theorem 12.1 (Mediant interval).** Let p/q be reduced with
penultimate convergent p′/q′ (of its even-length expansion, say). The
set of x ∈ (0,1) whose convergents include p/q is the open interval
between the **Stern–Brocot mediants**

    (p + p′)/(q + q′)   and   (2p − p′)/(2q − q′).

*Proof sketch.* By the t-parametrization in the proof of Theorem 8.1,
the reals whose expansion begins [0; a₁,…,a_k] are exactly
x(t) = (t p_k + p_{k−1})/(t q_k + q_{k−1}) for t ∈ (1, ∞) — a
monotone Möbius image of (1, ∞), i.e. an interval with endpoints x(1)
= (p+p′)/(q+q′) and x(∞) = p/q. The two parity choices of the
expansion of p/q (Theorem 8.3's trick) give the two one-sided
intervals, whose union around p/q is the stated mediant interval: the
far endpoint of the opposite-parity side works out to
(p + (p − p′))/(q + (q − q′)) = (2p−p′)/(2q−q′), since the
opposite-parity penultimate convergent of p/q is p − p′ / q − q′.
Full details are Exercise 12.1 — every step is Theorem 8.1 algebra. ∎

To count |A| without double counting, partition outcomes by the
**first** admissible convergent of y/D. The partition is genuinely
disjoint by a gcd argument: the side denominator q − q′ is never a
multiple of r, because gcd(q, q′) = 1 forces gcd(q, q − q′) = 1 while
r | q and r > 1. Summing the interval counts over admissible
denominators reproduces the enumerated |A| **outcome for outcome, with
zero error**, on all 27 instance/size combinations tested.

### 12.4 From counts to measure

For reduced p/q the mediant interval has length

    μ(q) = (2/q) Σ_{u < q, gcd(u,q)=1} 1/(q + u)

summed over the φ(q) admissible numerators. Since coprime residues
equidistribute with density φ(q)/q, approximate the sum by the
integral:

    Σ_{u} 1/(q+u) ≈ (φ(q)/q) ∫_q^{2q} dt/t = (φ(q)/q) ln 2
    ⟹   μ(q) → 2 ln 2 · φ(q)/q².

**Sanity check against a classical theorem.** Summed over *all* q ≤ Q
with Σ_{q≤Q} φ(q)/q² ≈ (6/π²) ln Q, this gives
(12 ln 2/π²) ln Q — exactly Khinchin's almost-everywhere count of
convergent denominators below Q. The *measure* is classical; the
content of the law is its **restriction to the denominators the
decoder admits**.

### 12.5 The law

Restricting to admissible q = kr ≤ N:

    ┌─────────────────────────────────────────────────────┐
    │   |A| / D  ⟶  2 ln 2 · Σ_{k=1}^{⌊N/r⌋} φ(kr)/(kr)²  │
    └─────────────────────────────────────────────────────┘

— Eq. (5) of the paper. Accuracy: better than 1% on five of six
instances at D ≫ N²; 4.2% on the sixth (N = 55, r = 5, where eleven
admissible denominators make the first-admissible exclusions
largest). The exact finite-D form (interval *counts*) reproduces |A|
with zero error at every size.

### 12.6 What the law settles

**Scaling in D — exactly linear.** Measured |A| ∝ D^{1.03±0.01}
(R² = 0.999); the small excess over slope 1 is window discreteness.

**Scaling in r — the 1/r² envelope is wrong.** Comparing r = 5 vs 10
on identical registers, swept to D ≥ 5r²: measured per-peak ratios 9.6
(N = 33) and 8.9 (N = 55) where 1/r² predicts 4.0; the law's
totient-sum ratios are 9.7 and 9.3. The "9.5× mystery" was the totient
sum all along.

**Why the envelope looked fine on the benchmark.** At r = 6, N = 21
the naive (r−1)/r² = 0.139 sits within 2% of the law's 0.141 because
two errors cancel: the true q = r window measure
2 ln 2 · φ(6)/36 = 0.077 is only 0.55× the envelope's, and the
admissible multiples q = 12, 18 restore the difference. On the r = 5
instances, where the cancellation fails, the envelope is off by
2.5–3× while the law holds to 4.2%.

**The decoder decides scorability before noise enters.** At N = 55 the
modal order class is r = 20; for d = 2 at D = 64 its acceptance set is
*empty* — the noiseless baseline is exactly zero, and no amount of
coherence helps.

### 12.7 The consequence that matters

Eq. (5) depends only on r and N — **not on d**.

> At matched control dimension, the decoder's error tolerance is
> identical across bases. The entire cross-base difference in decoded
> success therefore sits in the **quantum state**.

That is what upgrades the paper's mechanism section from a plausible
story to a quantitative account: the classical half of the pipeline is
solved exactly and is base-blind, so what remains is physics.

### 12.8 A general lesson for benchmarking

Decoded success conflates (1) decay of the quantum state — universal,
described by damage-weighted exposure (§15) — with (2) the error
tolerance of classical post-processing, which is algorithm-specific
**and can grow with problem size**. Any "noise resilience" benchmark
scored on decoded success is partly measuring classical decoder
redundancy. Reporting end-state fidelity alongside decoded signal
separates the two at zero extra cost; the paper recommends it as
standard practice.

**Exercise 12.1 (★★).** Complete the proof of Theorem 12.1: verify the
opposite-parity penultimate convergent claim and both endpoint
computations.

**Exercise 12.2 (★★).** Verify the totient sum for (N = 21, r = 6):
admissible denominators 6, 12, 18; compute
2 ln 2 [φ(6)/36 + φ(12)/144 + φ(18)/324] and compare with 0.141.

**Exercise 12.3 (★★★).** Enumerate A for (N = 21, r = 6) at
D = 64, 256, 1024; reproduce |A| = 8, 36, 148; and check the
first-admissible partition is disjoint by explicit inspection at
D = 64.

**Exercise 12.4 (★★).** Reproduce Khinchin's constant from the measure
(§12.4), and explain in one sentence why this validates the *measure*
but not the *law*.

---
---

# Part IV — Open quantum systems

## 13. Density matrices, channels, and the Choi theorem

### 13.1 Mixed states

**Definition 13.1.** A **density matrix** is ρ with ρ = ρ†, ρ ⪰ 0,
tr ρ = 1. Pure states are the rank-one case ρ = |ψ⟩⟨ψ|; a
probabilistic mixture {p_i, |ψ_i⟩} is Σ p_i |ψ_i⟩⟨ψ_i|. The Born rule
extends linearly: outcome probabilities are ⟨e_j|ρ|e_j⟩.

Two distinct physical situations force the same object: classical
ignorance of which pure state was prepared, and *entanglement* — by
Exercise 0.8, the reduced state tr_W(|Ψ⟩⟨Ψ|) of an entangled pure
state is mixed, and it is the complete local description. For a
register of n carriers of dimension d, ρ has (dⁿ)² entries — the
memory wall that puts exact simulation out of reach around
dim ℋ ≈ 3000 and motivates §19.

### 13.2 Channels: three definitions that coincide

What is the most general physical evolution of a density matrix? Three
answers, from three directions:

1. **Axiomatic:** a linear map E that is trace-preserving and
   **completely positive** (CP): (E ⊗ 𝟙_k)(ρ) ⪰ 0 for every extension
   dimension k. (Positivity alone is not enough — the transpose map is
   positive but corrupts entangled inputs; complete positivity is
   positivity *in the presence of a spectator*.)
2. **Operational (Kraus):** E(ρ) = Σ_i K_i ρ K_i† with
   Σ K_i†K_i = 𝟙.
3. **Physical (Stinespring):** attach an environment in a fixed state,
   evolve jointly by a unitary, discard the environment:
   E(ρ) = tr_env[U(ρ ⊗ |0⟩⟨0|)U†].

**Theorem 13.1 (Choi–Jamiołkowski).** For a linear map E on d × d
matrices define the **Choi matrix**
J(E) = (E ⊗ 𝟙)(|Ω⟩⟨Ω|), where |Ω⟩ = Σ_{j} |j⟩|j⟩ (unnormalized
maximally entangled vector). Then E is CP iff J(E) ⪰ 0, and every CP
trace-preserving map has a Kraus decomposition (2), obtained from the
eigenvectors of J(E).

*Proof.* If E has Kraus form, J(E) = Σ_i (K_i ⊗ 𝟙)|Ω⟩⟨Ω|(K_i ⊗ 𝟙)† is
a sum of positive rank-ones, so J ⪰ 0 — and the same argument shows E
is CP (the spectator passes through). Conversely let J(E) ⪰ 0 with
spectral decomposition J = Σ_i |v_i⟩⟨v_i| (eigenvectors scaled by
√eigenvalue). Any vector |v⟩ ∈ ℂ^d ⊗ ℂ^d defines a matrix K_v by
⟨a|K_v|b⟩ = ⟨ab|v⟩ ("bending the wire"). A direct index computation
shows the map ρ ↦ Σ_i K_{v_i} ρ K_{v_i}† has Choi matrix exactly
Σ|v_i⟩⟨v_i| = J(E); and since a linear map on matrices is determined
by its Choi matrix (the entries ⟨ac|J|bd⟩ = ⟨a|E(|c⟩⟨d|)|b⟩ enumerate
E on a basis), E itself equals that Kraus map. Trace preservation
pins Σ K_i†K_i = 𝟙 by evaluating on a basis of matrix units. ∎

This proof is four lines of index gymnastics and one idea — a matrix
and a bipartite vector are the same data — and it is the single most
used structural fact in the repository: **CP is checkable.** Every
channel here is verified by computing Choi eigenvalues (one of the 20
tests in `test_qudit_shor.py`). Stinespring (3) follows from Kraus by
building U's first block-column out of the K_i — Exercise 13.2.

### 13.3 The superoperator representation

Vectorize: stack ρ's columns into vec(ρ) ∈ ℂ^{d²}. Every linear map on
matrices becomes a d² × d² matrix S — the **natural representation** —
with E(ρ) ↔ S vec(ρ), and for Kraus operators
S = Σ_i K̄_i ⊗ K_i. Composition of channels is matrix multiplication
of their S's. Two uses recur: tr S has direct physical meaning (§15),
and one-parameter families exponentiate (§14).

**Exercise 13.1.** Show the transpose map T(ρ) = ρᵀ is positive but
its Choi matrix is the SWAP operator, with eigenvalue −1 on
antisymmetric vectors — hence T is not CP.

**Exercise 13.2.** Construct the Stinespring dilation from a Kraus
decomposition: define U|ψ⟩|0⟩ = Σ_i (K_i|ψ⟩)|i⟩ and verify it extends
to a unitary (the Kraus normalization is exactly the isometry
condition).

**Exercise 13.3.** Verify S = Σ K̄_i ⊗ K_i against the convention
vec(AρB) = (Bᵀ ⊗ A)vec(ρ).

## 14. The Lindblad equation, derived

Noise in this book is *continuous*: a carrier decoheres per unit time,
and a gate of duration t exposes it to exp(𝓛t). Where does the
generator's form come from?

**Definition 14.1 (Quantum dynamical semigroup).** A family {E_t}_{t≥0}
of channels with E_0 = id, E_{t+s} = E_t E_s, continuous in t.

**Theorem 14.1 (Lindblad form; derivation at first order).** If
E_dt = id + 𝓛 dt + O(dt²) is a channel for all small dt, then

    𝓛(ρ) = −i[H, ρ] + Σ_k ( L_k ρ L_k† − ½{L_k†L_k, ρ} )

for some Hermitian H and **jump operators** L_k.

*Derivation.* Kraus-decompose E_dt (Theorem 13.1). To first order in
dt one Kraus operator is near the identity, K₀ = 𝟙 + (−iH + G)dt with
H Hermitian and G Hermitian (split of an arbitrary matrix into
anti-Hermitian and Hermitian parts), and the others are small,
K_k = L_k √dt. Trace preservation Σ K†K = 𝟙 at order dt forces
2G + Σ_k L_k†L_k = 0, i.e. G = −½Σ L_k†L_k. Substituting into
E_dt(ρ) = Σ KρK† and collecting the dt terms gives the stated form.
(The full theorem — that *every* norm-continuous semigroup of channels
has a generator of this form — is Gorini–Kossakowski–Sudarshan and
Lindblad, 1976; the derivation above is the direction this book needs:
the form is *sufficient* for E_t = e^{𝓛t} to be a channel at all t,
because it is a channel at first order and semigroups exponentiate.) ∎

In this repository H = 0 — the rotating frame puts all coherent
dynamics into the gates — so channels are pure dissipation, and one
layer of noise is exp(𝓛 · t_layer), **exponentiated exactly** (§0.7),
never Trotterized. Both channel families form one-parameter
semigroups, so a gate costing a *fractional* number of layers t is
exact: scale the Lindblad rates (ladder) or set 1 − q = (1−p)^t
(depolarizing).

**Worked example (amplitude damping, d = 2).** One jump
L = √γ |0⟩⟨1|. Then L†L = γ|1⟩⟨1| and the equation reads
ρ̇₁₁ = −γρ₁₁, ρ̇₀₁ = −(γ/2)ρ₀₁: population decays at γ, coherence at
γ/2 — the T₂ = 2T₁ limit. Every ladder-channel intuition in §16 is
this example with more levels and level-dependent rates.

**Exercise 14.1.** Add a dephasing jump L′ = √γ_φ |1⟩⟨1| to the
worked example and derive 1/T₂ = γ/2 + γ_φ. (This identity is used
verbatim in §23's T₂/T₁ sweep.)

**Exercise 14.2.** Show that for a single *diagonal* jump
L = diag(c₀, …, c_{d−1}), the Lindblad equation acts elementwise:
ρ_{jk}(t) = ρ_{jk}(0) exp(−½|c_j − c_k|² t). (The engine of §17 and
of every structured-dephasing model in the repository.)

## 15. Damage units: entanglement fidelity as the currency

### 15.1 The problem with counting events

"Exposure = carriers × layers" counts *events*. But one noise event
does d-dependent harm: a ququint sitting in a ladder channel for one
layer loses far more than a qubit does. Counting events compares
apples to oranges across bases.

### 15.2 The right currency

**Definition 15.1 (Entanglement fidelity).** For a channel with
one-layer superoperator S (natural representation),

    F_e = tr S / d².

**Theorem 15.1.** F_e = Σ_i |tr K_i|²/d² for any Kraus decomposition,
and F_e = ⟨Φ|(E ⊗ 𝟙)(|Φ⟩⟨Φ|)|Φ⟩ with |Φ⟩ = |Ω⟩/√d the maximally
entangled state — i.e. F_e is the survival fidelity of maximal
entanglement through the channel, which is what earns "damage" its
name.

*Proof.* From S = Σ K̄_i ⊗ K_i (Exercise 13.3),
tr S = Σ_i tr K̄_i · tr K_i = Σ_i |tr K_i|². For the second form,
expand ⟨Φ|(K_i ⊗ 𝟙)|Φ⟩ = tr K_i / d and sum the squares. ∎

**Definition 15.2.** The **damage** per carrier-layer is 1 − F_e, and

    damage-weighted exposure = (carriers × layers) × (1 − F_e).

### 15.3 The numbers

| channel | 1 − F_e | d = 2 | d = 3 | d = 5 |
|---|---|---|---|---|
| calibrated ladder, strength s | (numeric) | 0.750 s | 1.462 s | 2.833 s |
| depolarizing, strength p | p(1 − 1/d²) | 0.75 p | 0.89 p | 0.96 p |

*Derivation of the depolarizing row:* for E(ρ) = (1−p)ρ + p𝟙/d, the
identity part contributes (1−p)d² to tr S and the depolarizing part
p·1 (its superoperator is |vec 𝟙/d⟩⟨vec 𝟙| appropriately normalized;
check by Theorem 15.1 with the generalized-Pauli Kraus form:
uniform-over-nonidentity Paulis have traceless Kraus operators). So
F_e = (1−p) + p/d². ∎

A ququint takes ~4× a qubit's damage per event on the ladder, and
almost the same damage per event under depolarizing. That single
contrast explains most of the difference between the two channels'
verdicts throughout the paper.

**A convention caveat, priced.** 1 − F_e itself tends to 1 − 1/d² for
strong depolarizing — it grows with d by construction. The
d-normalized alternative, average gate infidelity
1 − F_avg = [d/(d+1)](1 − F_e), rescales each base's damage by
(d+1)/d. Rescoring the collapse below in F_avg units
(`favg_rescore.py`) leaves the pooled fidelity law unchanged to two
decimals while moving the per-family Grover rate spreads by ±25% *in
opposite directions* on the two channels (ladder 1.13×→1.29×,
depolarizing 1.52×→1.23×): neither unit is uniformly flattering, and
the paper flags the family-spread numbers as convention-dependent at
that level.

### 15.4 The collapse test — and what it does not prove

Re-plot every measured point with damage-weighted exposure on the
abscissa. Grover's three bases collapse onto one exponential:
per-family decay rates 0.44/0.49/0.43 on the ladder (1.13× spread,
against 3.6× in event units), each family log-linear with R² ≥ 0.996.
Pooling both algorithms, all bases and sizes:

| ordinate | abscissa | ladder R² | depol. R² |
|---|---|---|---|
| signal | exposure × strength | 0.67 | 0.77 |
| signal | exposure × damage | 0.84 | 0.77 |
| **fidelity** | **exposure × damage** | **0.97** | **0.99** |

**The honest reading.** For a product of near-identity incoherent
channels, log-fidelity is *additive* in per-application entanglement
infidelity to first order:

**Theorem 15.2 (Null expectation).** If a pure state passes through
channels E₁,…,E_n, each of the form E_i = (1−ε_i)·id + ε_i·(junk),
then the fidelity to the noiseless state satisfies
ln F ≈ −Σ_i ε_i c_i with c_i = O(1) state-dependent constants — i.e. a
single exponential in accumulated damage, amplitude ≈ 1, is the
*expected* behaviour, not a discovery.

*Proof sketch.* Write each channel's action on the current (nearly
pure) state as F_i = 1 − ε_i c_i + O(ε²); fidelities of composed
near-identity maps multiply to the same order because the state
remains within O(Σε) of pure. Take logs. The gap in the sketch — the
constants c_i drift as the state degrades — is exactly why the law
degrades in the deep tail, and why the paper *measures* the depth of
validity rather than asserting it. ∎

The paper bounds the claim in both directions:

- Rescored in **log** fidelity — the metric that weights the tail —
  the shared fit gives R² = 0.74–0.75 (0.87–0.93 if refit there);
  `logfid_rescore.py`, deep points at `collapse_tail_deep.py`.
- The deep endpoints are a *test*, not a resolution limit, after the
  1600-trajectory re-measurement: the law holds to a factor 1.12 down
  to fidelity 2.1(3)×10⁻² on the ladder and to a factor 1.5 at
  6.4(2.0)×10⁻⁴ under depolarizing. (The 100-trajectory first pass of
  the deepest point had read 2.7×10⁻⁴ at ±40% — the mean of a
  heavy-tailed estimator, skewed low. Measure twice.)

**The law's failure mode is error that does not compose incoherently**
— correlated or coherent noise breaks additivity, and that is
precisely what the deep hardware circuits exhibit (§23.5). Hence the
law is stated for Markovian incoherent channels only.

### 15.5 The residual *is* the decoder

What no channel-level argument predicts: with units fixed, a nested
fit needs a **per-algorithm** decay rate (R² = 0.953 ladder,
0.93–0.94 depolarizing). Grover's fidelity equals its signal
everywhere (its decoder is the identity); Shor's d = 3 family holds a
flat signal ≈ 0.73 while losing two-thirds of its fidelity; and at
d = 2, m = 12 under depolarizing, continued fractions decode a signal
of 0.131 ± 0.018 from a state with fidelity 6.4(2.0)×10⁻⁴. The
mechanism claim, in the form the data support:

> **Accumulated channel damage is the law for the quantum state; the
> residual algorithm dependence of decoded success sits in the
> decoder** — for which §12 gives an exact, base-independent account.

**Exercise 15.1.** Prove tr(A ⊗ B) = tr A tr B implies
F_e(E₁ ⊗ E₂) = F_e(E₁)F_e(E₂) for a product channel on two carriers.

**Exercise 15.2 (★★).** Compute 1 − F_e for the amplitude-damping
example of §14 at strength γt = s and compare with the ladder d = 2
value 0.75s (the remaining 0.5s is the dephasing jump's share —
decompose it).

## 16. The calibrated ladder channel

### 16.1 What a transmon is, in one paragraph

A transmon is a weakly anharmonic oscillator: a Josephson junction
shunted by a large capacitor, with level spacing decreasing by the
anharmonicity α ≈ −200 to −300 MHz. The lowest two levels are the
qubit; levels 2, 3, … are the qudit. Because it is nearly harmonic,
higher levels relax and dephase **faster** — the "ladder." Background:
`docs/TRANSMON.md`.

### 16.2 The textbook model is wrong — in both exponents

Naive expectations: bosonic relaxation Γ_k ∝ k; frequency-difference
dephasing Γ_φ(j,k) ∝ (k−j)². Both are contradicted by measurement,
both in the direction of over-penalizing qudits:

| quantity | textbook | measured |
|---|---|---|
| Γ₂/Γ₁ | 2.0 | ≈ 1.7 |
| Γ_φ^{01} : Γ_φ^{12} : Γ_φ^{02} | 1 : 1 : 4 | 1 : 2.0 : 2.3 |

The measured ratios are flatly incompatible with a (Δlevel)² law; the
physical driver is charge dispersion, which grows an order of
magnitude per level — so dephasing tracks the *higher* level of the
pair, not the gap.

### 16.3 The calibrated replacement

Fits to published per-level coherence data (nine devices, d = 3–12):

    relaxation  Γ_k ∝ k^0.7
    dephasing   Γ_φ(j,k) ∝ max(j,k)^1.1     (a max-level law)

realized in `qudit_shor.py` with the measured ratios reproduced as
1.62 and 1 : 2.14 : 2.14. **Normalization:** rates are set so the 0↔1
subspace is bit-for-bit identical to the qubit channel — every
cross-base difference is purely a higher-level effect.

Three calibration inputs and their error bars are *themselves* swept
as robustness axes in §23: the two exponents (Peterer's data admit
steeper dephasing, up to ≈ 2.6), the T₂/T₁ balance (hard-coded 1.0 in
the channel, swept 0.2–5), and the Ramsey-vs-Lindblad provenance of
the pair ratios (if Blok's ratios are quasi-static Ramsey rates, the
Lindblad realization should square them — priced by the exponent
sweep at ≈ 2.0).

### 16.4 The dephasing knob

A single scale on the dephasing term interpolates from free evolution
to perfect echo, modelling both the high-E_J/E_C regime (echo
coherence near the T₁ limit at d = 12) and refocused operation — how
any real transmon runs a long circuit. It is consequential: under
linear gate cost the ququint loses Shor without echo (−0.026) and wins
with it (+0.191). Mechanism: dynamical decoupling suppresses
dephasing, the part of the ladder scaling worst with d, and leaves the
gentler k^0.7 relaxation. Refocusing buys roughly one cost model of
headroom, which is why the paper's condition is stated "at the
operating dephasing level."

### 16.5 The four named regimes

1. **idealized ladder** — Γ_k ∝ k, (Δlevel)² dephasing; a bound only.
2. **calibrated ladder** — §16.3; the honest transmon model.
3. **low-charge-dispersion** — the knob at the high-E_J/E_C end.
4. **per-particle depolarizing** — §18.

## 17. Realizing a dephasing matrix exactly: Euclidean embedding

The max-level law cannot come from any single frequency ladder — and
proving that requires knowing exactly which dephasing matrices
diagonal jumps *can* realize.

**Theorem 17.1 (Dephasing realization = Euclidean embedding).** With
diagonal jumps L_1, …, L_M, collect v_j = (L_1(j,j), …, L_M(j,j)) ∈
ℝ^M. The Lindblad equation gives coherence (j,k) the decay rate
Γ_φ(j,k) = ½‖v_j − v_k‖² (Exercise 14.2, summed over jumps). A target
matrix Γ_φ is realizable iff 2Γ_φ is a Euclidean squared-distance
matrix, and the realizing jumps are recovered by **classical
multidimensional scaling**: with J = 𝟙 − (1/d)𝟙𝟙ᵀ the centering
projector and B = −½ J (2Γ_φ) J, the target is realizable iff B ⪰ 0,
in which case the eigendecomposition B = Σ λ_a u_a u_aᵀ yields jumps
L_a = diag(√λ_a u_a) realizing Γ_φ exactly.

*Proof.* Direction one is Exercise 14.2. For the reconstruction: if
v_j exist, center them (Σv_j = 0 costs nothing — a common shift of all
diagonal entries changes no difference v_j − v_k; physically it is a
global phase drift). Then B_{jk} := −½(D²_{jk} − row means − column
means + grand mean) = ⟨v_j, v_k⟩ by expanding
D²_{jk} = ‖v_j‖² + ‖v_k‖² − 2⟨v_j, v_k⟩ — the double-centering
identity. A Gram matrix is PSD; conversely any PSD B factors as
B = VVᵀ with rows v_j whose distances reproduce D² by the same
identity. Reading the columns of V (scaled eigenvectors) as diagonal
jumps finishes it. ∎

**Application.** The measured max-level law is realized exactly —
residual ≤ 3×10⁻¹⁷ for d = 2…7 (`dephasing_residual` in
`qudit_shor.py`). And no *linear frequency ladder* can do it: one
scalar sensitivity per level forces the v_j collinear in ℝ¹, giving
Γ_φ ∝ (f_j − f_k)² — a Δlevel-squared-type law, precisely the shape
the data reject. The embedding needs ≥ 2 dimensions; charge dispersion
supplies them physically.

The vectors v_j earn their keep twice over: §23's quasi-static control
reads them as *noise sensitivities* — a static Gaussian offset vector
ξ per shot, coupling as phase rate ξ·v_j, reproduces the calibrated
pair structure with quasi-static (depth²) accumulation. One
embedding, two noise models.

**Exercise 17.1 (★★★).** Implement classical MDS from Theorem 17.1,
verify the max-level law's residual ≤ 10⁻¹⁶ at d = 3, 5, and exhibit
a 3×3 dephasing matrix that is *not* realizable (B has a negative
eigenvalue). What triangle-like inequality does it violate?

## 18. Depolarizing, structured dephasing, and what measurement did to both

### 18.1 The per-particle depolarizing convention

ρ → (1−p)ρ + p𝟙/d per carrier per layer, same p at every d — the
trapped-ion-like channel. The convention rests on measured structure:
every level in the ion encoding is ground-state or metastable
(τ₁ ~ 1.1 s); allowed-transition magnetic sensitivities span only
~5×; single-qudit per-pulse error is nearly flat in d (2.0×10⁻⁴ at
d = 3, 3.2×10⁻⁴ at d = 5); control is demonstrated to 13 levels. By
§15.3 its damage is nearly flat in d — the qudit-friendly channel.

### 18.2 The sharpest failure mode: Zeeman-structured dephasing

The per-particle convention flattens pair structure the ion encoding
really has. The worst case: magnetic-field dephasing with the
collective-B sensitivity structure of the ⁴⁰Ca⁺ encoding, one
diagonal jump ∝ diag(g_j m_j), normalized so the optical-qubit pair
matches the qubit channel. Pair rates then span 1–25× at d = 3 and
1–49× at d = 5 — and the encoding is no strawman: over all C(8,d)
level subsets, the chosen levels exactly minimize the worst pair rate
at d = 5 and 7.

Under a **Markovian** realization of that structure the verdict
reverses outright — the qubit wins every cell. But field noise in the
laboratory is quasi-static on circuit timescales, and here the
Markovian stand-in is *not* a conservative simplification:

**The quasi-static control (`ion_zeeman_quasistatic.py`).** Draw the
field offset once per shot from a Gaussian, hold it through the
circuit, average by quadrature. Quasi-static damage accumulates as
depth² (Exercise 18.1), so the *shallower qudit schedules* shed
proportionally more of it. At matched qubit damage the unmitigated
`ion`-cost cell moves from a qubit win (0.275 vs 0.160) to a
statistical tie (0.296 vs 0.304). **The Markovian reversal was an
artifact of the stand-in, and the paper withdraws it as a claim about
laboratory field noise.**

Two structural results survive and sharpen the picture:

- **Refocusing is not d-independent.** One echo pulse refocuses the
  d = 2 encoding exactly; for d ≥ 3 *no* two-interval sequence
  refocuses (verified exhaustively over permutations), and exact
  refocusing needs L = d intervals — minimal over *all* permutation
  sequences. Charging those pulses as exposure puts d = 3 ahead of
  d = 5.
- **The mitigation bar is priced, not assumed.** Composing the Zeeman
  component with the depolarizing operating point and sweeping the
  suppression ε: the qudit ordering returns at ε* ≈ 0.6–0.8 under
  native-gate cost but only 0.09–0.15 under Mølmer–Sørensen cost — in
  hardware units, a 0↔1 coherence of ≳ 400–600 layer times
  (native) vs ≳ 2200–3800 (MS). A 100 ms shielded coherence at
  ~100 μs layers clears the first bar with margin and misses the
  second by 2–4×. This asymmetry is why the paper calls the transmon
  route the *robust* one even though ions offer larger headline gains.

**A worked quadrature warning.** The Gaussian average over the static
offset is an oscillatory integral ∫cos(ax)e^{−x²/2}dx with a up to
~24. Gauss–Hermite quadrature **fails outright** here (15 nodes return
0.98 where the truth is 6×10⁻⁵⁵, and raising the order gets worse
before better); the trapezoid rule, whose error on a Gaussian is pure
aliasing ~exp(−(2π/H − a)²/2), is exact to 10⁻¹² at spacing H = 0.2.
The repository learned this the expensive way; Exercise 18.2 makes you
learn it the cheap way.

### 18.3 The same discipline, applied to the ladder

Because the calibrated ladder's stated mechanism (charge dispersion)
is also 1/f and quasi-static, the identical substitution is run on
the transmon channel too (`ladder_quasistatic.py`, using the §17
vectors as sensitivities), along with a common-mode (spatially
correlated) variant. Result, previewed here and tabulated in §23:
every verdict survives all four temporal × spatial combinations —
quasi-static helps the qudits most (the Markovian convention is
conservative on the temporal axis), common-mode helps the qubit most
(mildly optimistic on the spatial axis), and neither moves a winner.

**Exercise 18.1.** For a static frequency offset δ held for a time T,
show the ensemble-averaged coherence is exp(−σ²c²T²/2) when
δ ~ N(0, σ²) with sensitivity c — versus exp(−ΓT) for Markovian
dephasing. Where does the T² come from, physically?

**Exercise 18.2 (★★).** Reproduce the Gauss–Hermite failure: integrate
cos(24x)e^{−x²/2} with 15-, 31-, and 61-node Gauss–Hermite and with
the trapezoid rule at H = 0.2, against the exact e^{−288}. Explain
the failure (where does Gauss–Hermite put its nodes, and what does the
integrand do between them?).

## 19. Quantum trajectories, with the unravelling theorem

Exact density-matrix evolution costs O(d^{2n}) and dies near
dim ℋ ≈ 3000. To reach 5.3×10⁵ the repository uses Monte Carlo
wavefunctions.

**The method.** Evolve a pure state. After each gate, each carrier q
independently passes through the per-layer channel raised to the
gate's cost: one Kraus operator K_i is sampled with probability
p_i = tr(K_i†K_i ρ_q) — ρ_q the carrier's *reduced* state
(Definition 0.12), cheap to extract from the state tensor — then
applied and the state renormalized.

**Theorem 19.1 (Unravelling).** Averaging |ψ⟩⟨ψ| over trajectories
reproduces the channel exactly:
E[|ψ′⟩⟨ψ′|] = Σ_i K_i|ψ⟩⟨ψ|K_i† = E(|ψ⟩⟨ψ|).

*Proof.* One sampling step maps |ψ⟩ to K_i|ψ⟩/‖K_i|ψ⟩‖ with
probability p_i = ‖K_i|ψ⟩‖² (check: tr(K_i†K_i|ψ⟩⟨ψ|) = ‖K_iψ‖², and
the p_i sum to 1 by the Kraus normalization). So

    E[|ψ′⟩⟨ψ′|] = Σ_i p_i · K_i|ψ⟩⟨ψ|K_i†/p_i = E(|ψ⟩⟨ψ|).

The normalization cancels against the sampling weight — that is the
whole theorem. Iterating over carriers and gates, and finally over a
convex mixture of initial states, extends it to the full circuit by
linearity. ∎

For a *carrier* inside a register the same computation runs with ρ_q
in place of |ψ⟩⟨ψ| — the sampling probability is defined by the
reduced state precisely so that the cancellation still works
(Exercise 19.1).

**Why the statistics beat Bernoulli.** Each trajectory contributes its
full outcome distribution (the Born probabilities of its final state),
not one sampled shot — so the variance is that of the *distribution
mean*, well below p(1−p)/n. Measured variance ratios on this
repository's points: 7.7–26.6× below Bernoulli. And the bars are
*calibrated*, not just estimated: 24 independent 1000-trajectory
replicas put the empirical-to-quoted standard-error ratio at 0.995
(`trajectory_variance.py`).

**Fidelity estimation.** End-state fidelity is the trajectory average
of |⟨ψ_ideal|ψ⟩|² — an unbiased estimator of ⟨ψ_ideal|ρ|ψ_ideal⟩ by
Theorem 19.1 — cross-checked against exact density matrices (8000
trajectories vs exact at d = 3, m = 4: 0.51σ agreement). One caution
the deep tail taught (§15.4): the estimator's distribution is heavy-
tailed at very low fidelity, and 100-trajectory means can sit
significantly low; the deepest points are measured at 1600.

**Exercise 19.1.** Write out the per-carrier sampling step for a
two-carrier register and verify the cancellation of Theorem 19.1 with
ρ_q = tr_other(|ψ⟩⟨ψ|).

**Exercise 19.2 (★★★).** Implement the method for a single qutrit
under the calibrated ladder, compare 10⁴ trajectories against the
exact exp(𝓛t), and watch the error scale as 1/√n.

---
---

# Part V — The accounting, and the result

## 20. Exposure, cost models, and break-even

### 20.1 The exposure convention

Stated once, precisely, because every number in the paper depends on
it:

> One layer of noise is applied to **every** carrier for **every**
> layer of the serial schedule. A gate spanning k carriers occupies
> its decomposition depth in layers, so idling carriers decohere while
> gates execute.

    exposure = carriers × layers
    damage-weighted exposure = exposure × (1 − F_e)

The serial convention is not neutral: concurrent execution shortens
the schedule most for the register with the most carriers, i.e.
d = 2, so the assumption runs *against* the conclusion it supports —
which is why §23 measures it instead of disclaiming it (the ASAP
scheduling control).

### 20.2 The break-even criterion

Janković et al. derive, by linear response over Haar-random gates
under pure dephasing, the critical gate-efficiency ratio a single
qudit must clear to beat a multi-qubit register at matched Hilbert
dimension:

    ratio* = (d² − 1) / (3 log₂ d)

= 1.68 (d = 3), 3.45 (d = 5), 5.70 (d = 7) — three times lower than
the folklore O(d²/log₂ d) = 5.7/10.8/17.5. Their criterion is stated
for ratios of gate *times* in units of the decoherence time; reading
this book's layer-count ratios as gate-efficiency ratios identifies
the two, an identification that holds when per-layer duration and
coherence co-scale across bases — an assumption the structured
channels of §23 can violate, and the paper says so.

Under that identification the gate-level criterion matches the
algorithm-level winner in four of six cost/dimension cases on the
ladder (including the tight one: d = 5 `uniform` clears 3.45 at 3.80
and wins); both misses are in the conservative direction their
pure-dephasing assumption predicts, our calibrated relaxation being
gentler. **Independent validation:** the three central equations of
their paper are reproduced from this repository's superoperator code
to worst relative error 4.1×10⁻⁴ over d = 2–64, the residual
identified as their own first-order truncation (`jankovic_check.py`).

### 20.3 The noise-inflation threshold f*

The channels charge every base the same per-layer strength. If
higher-d gates are *additionally* noisier, the condition acquires a
threshold: inflate the qudit's strength alone, s_d = f · s₂, and
locate the crossing f* where the qudit's signal falls to the qubit's.
Two charging *scopes* bracket the physics:

- **global** — every carrier-layer of the qudit circuit runs at f·s₂
  (idle error co-scales with gate error, as it does if both are driven
  by the same mechanism, e.g. charge dispersion);
- **gate-only** — only the entangling gate's participants pay f·s₂
  (idle decoherence stays at the ambient rate).

Representative thresholds at the demo operating points
(`noise_inflation.py`, `transmon_rebuild.json`): ladder/`uniform`
f* = 2.05 (d 3) and 2.46 (d 5) global; depolarizing/`uniform` 2.65 and
4.50; `ion` cost 1.21–1.62; the gate-only scope raises each (e.g.
3.63 for the transmon CZ† comparison of §23.4). Read as hardware
guidance: a platform keeps the qudit advantage while its measured
qudit-to-qubit per-gate noise ratio stays below f* *after* the
layer-count multiplier is charged. §23.4 feeds measured gate
fidelities through exactly this threshold — the paper's second
condition — and f* doubles as a **wall-clock tolerance**: a qudit
layer running f× longer at fixed rates is the same arithmetic, which
is how the 580-ns transmon gate and the ~250-ns critical comparator
time enter.

**Exercise 20.1.** Evaluate (d²−1)/(3 log₂ d) at d = 3, 5, 7 and the
folklore d²/log₂ d; reproduce both rows.

**Exercise 20.2.** Show that inflating strength by f at fixed layer
count is identical, to first order in damage, to inflating layer
*duration* by f at fixed strength — the observation that turns f*
into a duration tolerance.

## 21. The success metric

### 21.1 Why raw success probability is unusable

Continued fractions "succeed" on a substantial share of uniformly
random outcomes: the random floor is 0.12–0.13 on the N = 21
benchmark at demo size, 0.20–0.26 on N = 29, up to 0.59 on
small-order instances — and at r = 2 it meets or exceeds the
noiseless baseline. A metric that a random-number generator can score
on is not a metric.

### 21.2 The floor-corrected signal

    signal = (success − floor) / (success_noiseless − floor)

— 1 for perfect interference, 0 for random guessing, negative when
noise biases outcomes *away* from the answer. Floors and baselines
are recomputed for every base, size, and readout setting.

### 21.3 The span rule

Small orders compress the metric's dynamic range, so any instance
used quantitatively must have floor-to-baseline span > 0.15. The
paper discloses one grandfathered exception (the r = 3 aligned
instance, span 0.07–0.12; no signal magnitudes are quoted from it).
The rule has teeth: it is why every base-2-aligned order class at
N = 21, 33, 55 is unscorable and the converse alignment control of
§10.4 cannot be built.

### 21.4 Readout error, and a structural cancellation

Charging a readout channel with misread rate of |k⟩ growing as (1+k)
— a linear reading of measured transmon qutrit assignment errors — on
every control carrier leaves the qudit advantage untouched: the
ququint's lead drifts < ±0.03 over ε = 0–0.04. The reason is
arithmetic: mean misread over levels is ε(d+1)/2, total readout
exposure m·ε(d+1)/2, and at matched precision m ≈ log D/log d this is
9ε/8ε/9ε at D ≈ 64 for d = 2/3/5. Per-level degradation with d is
almost exactly cancelled by the reduced carrier count — near-neutral
*by construction*. Measured hardware sits mid-sweep (assignment
fidelities 97–99% for |0⟩, 92–96% for |2⟩ ⟹ ε ≈ 0.01–0.03), and at
ε = 0.02 every ordering of the central table is intact.

*Scope:* simultaneous d-level discrimination (the transmon case).
Ion readout is sequential shelving — d−1 detection rounds, compounding
misreads and adding readout *time* the cancellation does not cover.

**Exercise 21.1.** Reproduce the 9ε/8ε/9ε cancellation, and find the
D at which it is least exact.

**Exercise 21.2 (★★).** Compute the continued-fraction floor for
(N = 21, D = 64, r = 6) — i.e. |A|/D from §12 — and check 8/64 =
0.125 against the quoted 0.12–0.13 (the exact floor varies with the
outcome convention for y = 0).

## 22. Assembling the paper's condition

### 22.1 The two conditions

> **Condition 1 (structural).** A qudit advantage in bare, uncorrected
> circuits requires a native two-qudit entangling gate whose cost
> grows at most linearly in d. Two-level-decomposed gates forfeit it
> in every case tested but one — and that one (the depolarizing
> `pavlidis` qutrit cell, +0.13, with a thin ququint cell at +0.03)
> is width compression surviving on the channel whose damage is
> flattest in d.
>
> **Condition 2 (measured).** Given condition 1, the advantage
> survives only while the native gate's own infidelity growth with d
> stays below the critical inflation factor f* of §20.3 — a threshold
> decided by *measured* gate fidelities, charging scope, and
> wall-clock duration, not by asymptotics.

### 22.2 The central table

Floor-corrected signal, unbiased instance (N = 21, r = 6), both
channels at the common demo strength 0.005, exact density matrices
(`cost_fair.py`; the paper's Table III):

| noise | cost | d = 2 | d = 3 | d = 5 | layers |
|---|---|---|---|---|---|
| depol. | `uniform` | 0.331 | 0.667 | **0.782** | 57/26/15 |
| | `ion` | 0.331 | 0.497 | **0.502** | 57/44/42 |
| | `pavlidis` | 0.331 | **0.461** | 0.361 | 57/48.5/62.2 |
| ladder | `uniform` | 0.282 | 0.578 | **0.631** | 57/26/15 |
| | `ion` | 0.282 | **0.374** | 0.256 | 57/44/42 |
| | `pavlidis` | 0.282 | **0.333** | 0.132 | 57/48.5/62.2 |

Read the columns:

- **`pavlidis`** — the decomposition penalty. On the ladder it
  forfeits the ququint advantage outright (0.132) and leaves the
  qutrit a thin +0.051 that §23's single-qudit charge and concurrency
  control both eliminate; under depolarizing, width compression keeps
  both qudit cells above the qubit (the "one exception" of
  Condition 1), the qutrit clearly, the ququint by +0.030.
- **`uniform`** — native entangler: qudits win on both hardware
  classes.
- **`ion`** — the interesting column. Depolarizing: the d = 3 and
  d = 5 cells are a statistical tie (0.497/0.502) — the paper calls
  it a tie, and the concurrency control independently flips its best
  qudit to d = 3. Ladder: the qutrit wins, the ququint loses; the
  margin is thin enough that §23's controls (single-qudit charge,
  concurrency, T₂/T₁) each probe it.
- The winner is decided by the **cost model**, not the noise model —
  but the *margins* are decided by the noise structure, which is why
  §23 exists.

**Matched pairings.** Cost and noise are not independent; each pairing
describes a platform. Both physically matched pairings — trapped-ion
qudits (`ion` + depolarizing) and native-cross-Kerr transmons
(`uniform` + ladder) — favour qudits in the table. What the measured
inputs of §23.4 then decide is *which dimension*: d = 3 robustly;
d = 5 only under assumptions the data currently disfavour.

### 22.3 Scaling, and the plateau

Sweeping precision 6 → 14.3 bits (D = 64 to 19683; deepest register
3¹² = 5.3×10⁵), 1000 trajectories per point, weighted least-squares
fits with committed statistics (`scaling_claims.py`):

- Both qudits stay above the qubit at every precision in all four
  regimes (≥ 5σ where quoted).
- The qubit decays roughly 2× faster per precision bit: −0.045(3)/bit
  against the qutrit's −0.021(5) on the ladder; the ququint decays at
  qubit-like slope from a higher start.
- **The qutrit family holds a plateau, then falls**: first three sizes
  flat (χ²/dof = 0.15, lower-tail p = 0.14), the 14.3-bit point
  3.5σ below the 9.5-bit one. A single slope is a summary, not a
  model.
- Qutrit–ququint crossings, with Monte Carlo confidence intervals:
  8.6 [8.1–9.1] bits (ladder) and 12.5 [11.3–14.7] bits
  (depolarizing) — the second extrapolated past the ququint's last
  simulated size, and the first's lower end inside the simulated
  range.
- **This is the decoder law made visible** (§12.2): acceptance grows
  linearly in D while broadening grows polynomially in m, so decoder
  tolerance postpones the decay of decoded success. The reprieve ends
  when accepted outcomes stop carrying amplitude.

> **Honest-reporting note.** Five sizes would have read as a flat
> family; the sixth resolves the shape. An earlier version of this
> project claimed flatness and has retracted it. Instance robustness:
> the N = 29 sweep replicates the ordering and the qubit's fastest
> decay; the qutrit slope replicates under the ladder (1.7σ) but not
> depolarizing (3.7σ) — stated, not smoothed.

**Eigenstate QPE** is the cleanest practical result: decisive and
growing with size — at 11.6 bits the ququint retains 2.8× the qubit's
signal (+0.44 ± 0.02). Since eigenstate QPE is the quantum-chemistry
workhorse, this is the result with the clearest consequence.

**Exercise 22.1 (★★).** From `results/scaling_claims.json`, recompute
the weighted d = 2 ladder slope and its standard error; then compute
the unweighted slope and explain why the two disagree by more than
their bars (§ the weighting note in `scaling_claims.py`).

---

## 23. The robustness program: every objection, priced

The paper's method for objections is uniform: do not argue — build the
objection as a model, run it, and report which verdicts move. This
chapter is the catalogue. Each row names its script; each is a
self-contained exercise in reading the framework of §20–22 under one
altered assumption.

### 23.1 The catalogue

| control | question | answer |
|---|---|---|
| d = 7 grid (`d7_demo.py`) | does the condition extend a prime higher? | Yes, narrowing: `pavlidis` at/below the floor; `uniform` still beats the qubit on both channels but the ladder optimum moves to d = 5; `ion` fails on the ladder, keeps a 1.6σ edge under depolarizing |
| matched D (`matched_D.py`, `d7_matched_D.py`) | is the qudit lead just a bigger acceptance set (§12)? | No — equalizing D *helps* qudits: the D-matched qubit scores lower (0.33→0.27→0.22 depol. as D = 64→256→512), its decoder gift outweighed by added exposure; the d = 7 loss to d = 5 stands *despite* a 3× acceptance-set advantage |
| composite d (`d4_control.py`, `composite_control.py`) | does primality matter dynamically? | No: d = 4 and d = 6 land inside the qudit band (d = 6 at its top under depolarizing) — §2.1 measured |
| ladder exponents (`ladder_exponent_sensitivity.py`) | are the verdicts artifacts of the fitted 0.7/1.1? | Under native cost the qutrit survives every exponent Peterer admits; the ququint dies at the first steepening (1.6) and d = 7 falls hardest; under `ion` cost even the qutrit fails from exponent 2.0 |
| T₂/T₁ (`dephase_ratio_sweep.py`) | the channel hard-codes T₂ = T₁ | At fixed strength every verdict survives T₂/T₁ = 1.67→0.33; damage-matched to the qubit, the dephasing-dominated end inverts the `ion`-qutrit and the ququint's lead — only the native-gate qutrit is unconditional |
| quasi-static + correlated (`ladder_quasistatic.py`) | Markovian? uncorrelated? | All verdicts survive all four temporal × spatial structures; quasi-static helps qudits most (Markovian is conservative), common-mode helps the qubit most (+0.06 vs +0.006) without flipping anything (§18.3) |
| thermal + leakage (`ladder_thermal.py`) | no up-rate, confined top level — both favor qudits? | Per carrier yes; per register **no**: the qubit's 11×57 exposure loses more to thermal leakage than the qudits' √k growth costs them. Gaps *widen* monotonically (+0.21→+0.55 d3, +0.24→+0.65 d5 over n̄ = 0→0.4); no crossing anywhere, physical n̄ ≈ 0.01–0.05 moves qudit cells within error bars |
| single-qudit cost (`single_qudit_cost.py`) | 1-layer single-qudit gates at every d? | Charging (d/2)^α: the ladder/`ion` qutrit cell dies at α* = 2.14 — *exactly* the measured pulse-count charge; ladder/`pavlidis` at 1.44; the depolarizing cells survive measured charges; best qudit is d = 3 everywhere for α ≥ 1.5 |
| concurrency (`parallel_schedule.py`) | the serial schedule favors qudits | ASAP compresses d = 2 most (26.3% vs 20.0%); 5 of 6 verdicts hold, margins erode ≤ 4×, the thin ladder/`pavlidis` win flips — same cell the single-qudit charge kills |
| readout (`spam_study.py`) | d-level readout | structurally near-neutral (§21.4), verified at measured assignment fidelities |
| Zeeman (`collective_zeeman.py`, `ion_zeeman_*.py`) | worst structured dephasing | Markovian reversal withdrawn as quasi-static artifact; echo algebra (1 pulse for d = 2, L = d intervals for d ≥ 3) and the ε* mitigation bars remain (§18.2) |
| s-sweep (`cost_grid_ssweep.py`) | are the demo verdicts an artifact of s = 0.005? | Stable over every live window (down to 0.001–0.005 for ladder `ion`/`pavlidis` cells); depolarizing/`ion` is a d = 3 vs 5 tie |
| trajectory bars (`trajectory_variance.py`) | are the error bars real? | Empirical/quoted SE ratio 0.995 on 24×1000 replicas |

### 23.2 The wall-clock axis

The `uniform` model's "one layer at every d" assumes the native qudit
gate is as *fast* as the qubit gate. Restating f* (§20.3) as a
duration tolerance and re-scoring the demo instance in units of the
d = 2 two-qubit gate time: the qutrit advantage dies when its
entangler takes ρ* = 2.3× the qubit's two-qubit gate time — ~250 ns
against a Willow-class comparator. The measured 580-ns cross-Kerr
CZ† survives against IBM-class cross-resonance durations and dies
against 100-ns-class CZs. Wall-clock is not a footnote; it is a
second copy of Condition 2.

### 23.3 The measured-fidelity verdicts (Condition 2 executed)

Feeding the only published native two-qudit gate fidelities through
f*, with the conversion done through each channel's own damage
identity s = ε/[2L·Δ(d)] (an earlier draft used the depolarizing
identity for the ladder too, overstating ladder inflation by 1.6× at
d = 3 and 3.0× at d = 5 — the erratum is in the paper):

- **Ion (Hrmo et al.: 99.6/98.7/93.7% at d = 2/3/5).** The qutrit
  survives *both* charging scopes in 3 of 4 channel/cost pairings;
  the ququint fails 7 of 8 readings (the eighth a +0.04 near-tie).
  A d = 5 native gate at ≳ 96.7% would restore the 4-bit advantage —
  a falsifiable spec.
- **Transmon (Goss et al.: CZ† 97.3(1)%).** The channel-consistent
  inflation is f = 3.08 ± 0.11 against f*_gate = 3.63 (passes,
  robustly) and f*_global = 2.05 (fails): the verdict is decided by
  the *scope* question — whether idle dephasing co-scales with gate
  error, which charge-dispersion physics suggests it does. Inverted:
  the required two-qutrit fidelity is 96.8% (gate-only) to 98.2%
  (global) against a same-class qubit anchor, and the measured gate
  sits inside that bracket; mitigation demonstrated on the same
  processor family (3× effective-error reduction) spans the gap, at
  an exposure overhead the accounting would charge.

### 23.4 The hardware anchor

The qubit branch, compiled at face value and run on two commercial
devices (August 2026; every number reproducible from committed shot
histograms via `braket_raw_analysis.py`):

| device | circuit | predicted | measured | \|w⟩ |
|---|---|---|---|---|
| IonQ Forte-1 | m = 5 (15 gates) | 0.60–0.70 | 0.617 ± 0.007 | 0.99 |
| IonQ Forte-1 | m = 7 (28 gates) | 0.42–0.54 | 0.011 ± 0.001 | 0.99 |
| IonQ Forte-1 | m = 7 AQFT (25) | 0.44–0.57 | 0.066 ± 0.004 | 0.99 |
| IQM Garnet | m = 5 (47 routed) | 0.18–0.42 | 0.080 ± 0.004 | 0.81 |
| IQM Garnet | m = 7 (104 routed) | 0.04–0.15 | 0.032 ± 0.003 | 0.66 |

Three findings. (1) The shallow ion circuit lands inside its band and
pins the device's effective depolarizing strength at 0.007–0.009,
bracketing the vendor's 0.7% — quantitative validation of the
convention on the platform it models. (2) The deep ion circuit fails
*coherently*: peak destroyed below the random floor with the work
qubit at 0.99, no relabeling among 10,080 reinterpretations recovers
it, and a raw probe caught a nearly pure state with its phase wrong by
one digit — the error class that breaks Theorem 15.2, exhibited on
cue. (3) The superconducting lattice fails mostly-but-not-only by
routed decoherence: the routed programs (47/104 CZs, recovered from
task metadata, `garnet_routed.py`, parse validated to 10⁻⁶) predict
the work-qubit decay at s ≈ 0.004, but conditioned on that scale the
control register shows a 3–4× coherent excess at both depths — the
ion failure mode, at superconducting speed.

**The caution generalizes:** past a depth threshold, a decoded-success
benchmark on NISQ hardware measures coherent calibration error, not
the decoherence it nominally probes.

### 23.5 The proposed experiment

The revision moved the proposal to where the measured inputs say the
advantage is robust: **eigenstate QPE at d = 3** on a Ringbauer-class
processor, where the measured-strength prediction is 0.612 vs the
qubit's 0.533 on the same apparatus (`qpe_d3_measured.py`), with the
d = 5 version conditional on a ≳ 96.7% native gate (§23.3). The
deep-circuit coherent failure above counsels entering at m = 2 before
m = 3.

## 24. What is *not* settled

Restating the paper's Limitations as open problems:

- **Coherent errors are unmodeled** — cross-Kerr (0.1–0.7 MHz
  dephases unprotected two-qutrit coherence within a few gate times)
  and drive-induced shifts, plus leakage *during* gates (idle thermal
  leakage is now modeled and helps the qudits). The hardware anchor
  shows exactly this class deciding real devices at depth.
- **Gate cost and gate error are treated as proportional**; longer-
  but-better gates would soften the ion penalty, and f* bounds the
  tolerance in the opposite direction.
- **The plateau's onset is unfitted** — six sizes locate the fall but
  cannot fit its onset; beyond 14.3 bits is unmeasured.
- **d > 7 is untested**, and d = 7 only at demo size, where the
  break-even window has visibly narrowed.
- **Compiled arithmetic** is charged, not compiled: at face value the
  compiled qudit-to-qubit depth ratio spans ≈ 0.9–2.7 across
  d = 3–5, harsher than any cost model here — the decomposition
  verdicts are conservative. The penalty is confined to depth (the
  in-place constructions add no width).
- **Fault tolerance is out of scope**, and its d-dependence can carry
  the opposite sign (§23.1's Keppens reconciliation: a code has no
  problem instance to compress — compression, the entire mechanism
  here, is unavailable to it).
- **The d = 5 gates exist today only on trapped ions**; the deep
  ladder registers are one to two hardware generations ahead of
  experiment, and the paper's Table I marks those cells counterfactual.

---
---

# Part VI — Projects

Course-scale projects; each has a committed answer key.

1. **(Decoder.)** Implement the decoder, enumerate its acceptance
   sets, verify Lemma 11.1 on ten instances, then reproduce the
   totient-sum law and its two spectacular failures of the naive
   envelope (§12.6). Key: `decoder_formula.py`, `decoder_scaling.py`.
2. **(Channel builder.)** Build the calibrated ladder from
   Theorem 17.1: fit jumps, verify CPTP by Choi eigenvalues, compute
   damage constants 0.750/1.462/2.833. Key: `qudit_shor.py`,
   `test_qudit_shor.py`.
3. **(Trajectory engine.)** Implement Theorem 19.1 for a 3-carrier
   register, validate against exact evolution, and reproduce one demo
   cell of §22.2 to 2σ. Key: `trajectories.py`.
4. **(Alignment audit.)** Take any published cross-dimension Shor
   comparison and compute its residual misalignment per base. Was the
   comparison confounded? (For N = 15 you know the answer — §10.2.)
5. **(Cost-model referee.)** Re-derive the layer counts 57/26/15,
   apply all three cost models, and reproduce the central table's
   layer column. Then write the strongest objection to the `uniform`
   row you can, and check whether §23 already prices it. (It probably
   does; finding the row is the exercise.)
6. **(Deep-tail statistics.)** Estimate fidelity ≈ 10⁻⁴ by
   trajectories at n = 100 and watch the heavy-tailed estimator sit
   low; quantify the bias by bootstrap, then re-run at n = 1600.
   Key: `collapse_tail_deep.py` and the §15.4 erratum it produced.

---
---

# Appendix

## A.1 Notation

| symbol | meaning |
|---|---|
| d | qudit dimension (levels per carrier) |
| ω, ω_D | e^{2πi/d}, e^{2πi/D} |
| X, Z | generalized Pauli shift and clock (Definition 1.2) |
| F_d | Fourier gate (Definition 3.1) |
| m, D | control carriers, control dimension D = dᵐ |
| w | work carriers, w = ⌈log_d N⌉ |
| N, a, r | modulus, base, multiplicative order r = ord_N(a) |
| φ, φ* | phase; golden-ratio conjugate ≈ 0.6180 |
| A | decoder acceptance set {y : decode(y) = r} |
| φ(·) | Euler totient (context disambiguates from phase) |
| S | one-layer superoperator, natural representation (§13.3) |
| F_e | entanglement fidelity tr S/d²; damage = 1 − F_e |
| F_avg | average gate fidelity; 1−F_avg = [d/(d+1)](1−F_e) |
| Γ_k, Γ_φ(j,k) | relaxation rate of level k; dephasing rate of pair (j,k) |
| s, p | per-carrier-layer noise strength (ladder, depolarizing) |
| f*, ρ* | noise-inflation threshold; its wall-clock restatement |
| ε* | Zeeman suppression factor at which qudit ordering returns |
| n̄ | thermal occupation (up-jump rate ratio, §23.1) |

## A.2 Reading path

| step | read | for |
|---|---|---|
| 1 | this book, Parts 0–II | the mathematics and the algorithms in base d |
| 2 | `docs/THEORY.md`, `docs/TRANSMON.md` | platforms; why "ladder" |
| 3 | `docs/CALIBRATION.md` | how the channel was fitted |
| 4 | this book, Parts III–IV | the two original derivations |
| 5 | `docs/GRID_ALIGNMENT.md`, `docs/MECHANISM.md` | the audit trail of the confound |
| 6 | `docs/COST_SENSITIVITY.md`, `docs/ROBUSTNESS.md`, `docs/GROVER.md` | objections tested; the falsification run |
| 7 | `docs/HARDWARE.md` | the Braket campaign |
| 8 | `paper/main.pdf` | the finished argument |
| 9 | `docs/SOTA.md`, `papers/INDEX.md` | the literature library |

`docs/PAPER.md` maps every paper section to its documents and scripts.

## A.3 Script map

| § | topic | script → result |
|---|---|---|
| 3, 20 | cost models | `cost_fair.py` → `cost_fair.json`; `cost_sensitivity.py`; `cost_grid_ssweep.py` |
| 3 | d = 7 grid | `d7_demo.py`; matched-D extension `d7_matched_D.py` |
| 6–7 | QPE / order finding engines | `qudit_shor.py`, `qpe_generic.py`, `qpe_hires.py` |
| 7.4 | interpolation | `interpolation_experiment.py`, `interpolation_slopes.py` |
| 9 | Grover | `grover.py`, `grover_study.py`, `grover_cost.py` |
| 10 | alignment | `grid_alignment.py`, `same_n_control.py`, `ensemble_a.py`, `misalignment_scaling.py` |
| 11–12 | decoder lemma and law | `decoder_formula.py`, `decoder_scaling.py` |
| 15 | damage units and collapse | `exposure_collapse.py`, `fidelity_collapse.py`, `logfid_rescore.py`, `favg_rescore.py`, `collapse_tail_deep.py` |
| 16–17 | calibrated ladder, embedding | `qudit_shor.py` (channel construction) |
| 18 | Zeeman family | `collective_zeeman.py`, `ion_zeeman_demo.py`, `ion_zeeman_echo.py`, `ion_zeeman_quasistatic.py` |
| 18.3 | ladder temporal/spatial | `ladder_quasistatic.py` |
| 19 | trajectories, bars | `trajectories.py`, `trajectory_variance.py` |
| 20 | break-even, inflation | `jankovic_check.py`, `noise_inflation.py` |
| 21 | metric, readout | `spam_study.py`; floors via `plots.py` |
| 22.3 | scaling | `scaling_fair*.py`, `scaling_claims.py` |
| 23.1 | robustness catalogue | scripts named per row |
| 23.3 | measured fidelities | `hrmo_reanalysis.py`, `hrmo_gate_only.py`, `goss_transmon_test.py`, `transmon_rebuild.py`, `qpe_measured_strengths.py`, `qpe_d3_measured.py` |
| 23.1 | exponents, T₂/T₁, thermal | `ladder_exponent_sensitivity.py`, `dephase_ratio_sweep.py`, `ladder_thermal.py` |
| 23.1 | single-qudit, concurrency | `single_qudit_cost.py`, `parallel_schedule.py` |
| 23.4 | hardware | `braket_qpe_anchor.py`, `braket_raw_analysis.py`, `garnet_routed.py` |
| 23.5 | proposal | `ion_qpe_prediction.py`, `qpe_d3_measured.py` |
| — | correctness suite | `test_qudit_shor.py` (20 tests) |

---

*Companion to `paper/main.tex`. Every number in this book is
reproducible from the scripts above; corrections welcome.*
