# Glossary, diagrams, tests & benchmarks

Companion reference for the ai-qutrits simulator. Everything here refers to
concrete objects in `qudit_shor.py`; the benchmark numbers are measured from
`results/results.json` on the machine listed in §5.

---

## 1. Glossary

### Information carriers

**Qubit** — a 2-level quantum system, states |0⟩, |1⟩. The standard unit of
quantum information; 1 qubit = 1 bit of quantum information capacity.

**Qutrit** — a 3-level system, |0⟩, |1⟩, |2⟩. Carries log₂ 3 ≈ 1.585
qubits' worth of information. d = 3 is prime, so the full field-based
machinery (stabilizers, MUBs, discrete Wigner functions) applies.

**Ququint** — a 5-level system, |0⟩ … |4⟩. Carries log₂ 5 ≈ 2.322
qubits' worth. The largest base simulated in this repo.

**Qudit** — the generic term: a d-level system for any d ≥ 2.

**Prime dimension** — a qudit whose d is prime. Then ℤ_d is a finite field
𝔽_d, which is what makes the stabilizer formalism, maximal sets of mutually
unbiased bases, and clean qudit error correction work. Composite d (4, 6, …)
breaks this: ℤ_6 has zero divisors.

**Register** — a row of qudits read as one big-endian base-d integer. In
`qudit_shor.py`: qudit 0 holds the most significant digit
(`digits_of`, `reverse_digits`).

**Control / work register** — phase estimation uses two registers: the
*control* (m qudits, dimension D = d^m) that ends up holding the phase
estimate, and the *work* register (w qudits, d^w ≥ N) that carries the
modular arithmetic.

**Leakage states** — work-register basis states with index ≥ N that encode
no number mod N (e.g. states 15–26 of the 27-dimensional qutrit work
register). Unitaries leave them alone, but noise scatters population into
them, where it is lost to the computation.

### Algorithm terms

**Shor's algorithm** — factors N by reducing factoring to *order finding*,
which a quantum computer does in polynomial time via phase estimation.

**Order finding** — given coprime a, N, find the smallest r ≥ 1 with
a^r ≡ 1 (mod N). This repo's instance: a = 7, N = 15, r = 4.

**Phase estimation** — the circuit pattern: put the control register in a
uniform superposition, apply controlled powers of a unitary U, undo the
superposition with an inverse QFT, measure. Outcomes concentrate near
y ≈ s·D/r.

**QFT (quantum Fourier transform)** — the unitary F|x⟩ = D^(−1/2) Σ_y
ω^{xy}|y⟩ over ℤ_D, ω = e^{2πi/D}. Implemented as a circuit of
single-qudit Fourier gates and two-qudit controlled phases
(`build_qft_gates`, verified against the dense matrix `qft_matrix`).

**Generalized Hadamard / Fourier gate F_d** — the single-qudit QFT,
(F_d)_{jk} = ω_d^{jk}/√d. For d = 2 it *is* the Hadamard (`fourier`).

**Controlled phase gate** — diagonal two-qudit gate
|c₁,c₂⟩ → exp(2πi c₁c₂ / d^t)|c₁,c₂⟩ (`cphase`); the glue of the QFT
circuit.

**Controlled modular multiplier** — |c⟩|x⟩ → |c⟩|a^c·x mod N⟩; one per
control qudit, with a raised to the d^i power for control qudit i
(`cmult_unitary`). This is where the work register gets entangled with the
control phases.

**No-swap QFT** — the standard QFT circuit emits digits in reversed order;
instead of physical swap gates, this repo wires control qudit i to exponent
d^i (little-endian) so the inverse-QFT output comes out in natural order.

**Continued fractions** — the classical post-processing that turns a
measurement y into the order: expand y/D into convergents p/q and accept a
denominator q ≤ N with a^q ≡ 1 (`convergents`, `recovered_order`).

**Success probability** — Σ p(y) over outcomes y from which post-processing
recovers the *exact* order r = 4 (`shor_run`'s `success` field).

**Random floor** — the success probability of a *uniformly random* outcome.
At this demo size it is large (≈ 0.28–0.30, see §5) because continued
fractions is forgiving; all comparisons use the floor-corrected signal
(success − floor)/(noiseless − floor).

### Noise & decoherence

**Decoherence** — loss of quantum phase relationships to the environment;
the thing that turns interference patterns into random noise.

**T₁ (relaxation)** — timescale for energy decay |1⟩ → |0⟩. In a ladder
system level |k⟩ decays at ≈ k/T₁.

**T₂ (dephasing)** — timescale for losing the *phase* between levels
without losing energy. Frequency noise dephases levels j, k at a rate
growing like (j−k)².

**Amplitude damping ladder** — the relaxation model of an anharmonic
oscillator: jump operator a = Σ_k √k |k−1⟩⟨k| (see the diagram in §2).
Used in the `transmon` noise model (`transmon_superop`).

**Depolarizing channel** — ρ → (1−p)ρ + p·I/d: with probability p the
qudit is replaced by the maximally mixed state. Level-independent —
the model of "per-particle" noise platforms (`depolarizing_superop`).

**Lindblad equation / dissipator** — the generator of Markovian open-system
dynamics, dρ/dt = Σ γ_i (J ρ J† − ½{J†J, ρ}). The simulator exponentiates
it exactly per time-layer (`_dissipator`, `scipy.linalg.expm`).

**Superoperator** — a linear map on density matrices, stored as a d²×d²
matrix acting on vec(ρ) (row-major). Applied locally to one qudit of the
register tensor (`apply_channel`).

**Kraus / CPTP** — a physical channel must be Completely Positive and
Trace-Preserving; equivalent to having a Kraus decomposition, and to its
Choi matrix being positive semidefinite (checked in `test_channels_cptp`).

**Density matrix** — the state ρ of a possibly-mixed quantum system;
pure states are ρ = |ψ⟩⟨ψ|. Stored here as a tensor of shape dims + dims.

**Quantum trajectory (Monte Carlo wavefunction)** — instead of evolving ρ
(memory ∝ dim²), evolve a pure state (memory ∝ dim) and apply one randomly
chosen Kraus operator of the noise channel per qudit per layer, drawn with
probability Tr(K†K ρ_q); averaging over trajectories reproduces the exact
channel. This is what lets `trajectories.py` reach Hilbert dimensions
(~78 000) that the exact simulator cannot (ρ would need ~68 GB at
dim 65 536). Statistical error shrinks as 1/√n_trajectories.

**Reduced density matrix (RDM)** — the d×d state of one qudit obtained by
tracing out the rest of the register; used to compute per-qudit jump
probabilities cheaply during a trajectory (`_reduced_dm`).

**Choi matrix** — a d²×d² matrix representation of a channel whose positive
semidefiniteness certifies complete positivity; its eigenvectors give the
Kraus operators (`kraus_from_superop`).

**Time-layer** — the scheduling unit of the toy noise model: every gate
occupies an integer number of layers (single/two-qudit gates: 1;
controlled multiplier: w), and *every* qudit decoheres during every layer.

### Math machinery

**Generalized Paulis** — X|j⟩ = |j+1 mod d⟩ and Z|j⟩ = ω^j|j⟩; the qudit
analogue of the Pauli group.

**Stabilizer formalism** — description of a large class of states/circuits
by their symmetry group; over prime d it inherits the symplectic structure
of 𝔽_d² (Gottesman 1999).

**MUB (mutually unbiased bases)** — bases where every state of one has
equal overlap 1/√d with every state of the other; d + 1 of them exist
exactly for prime-power d.

**Discrete Wigner function** — quasi-probability picture of qudit states;
for odd prime d its *negativity* is the resource that powers quantum
speedup (Gross 2006).

**Magic states** — states that promote stabilizer circuits to universality;
qutrit magic-state distillation has exceptionally clean constructions.

### Transmon & hardware terms

**Transmon** — a superconducting anharmonic oscillator: an LC circuit whose
inductor is a Josephson junction. Levels are unequally spaced, so |0⟩,|1⟩
can be addressed as a qubit and |2⟩,|3⟩,… come for free as qudit levels.
Full explainer in `TRANSMON.md`.

**Josephson junction** — two superconductors separated by ~1 nm of oxide;
Cooper pairs tunnel coherently through it, giving a *nonlinear* inductance.
The source of the anharmonicity that makes a transmon addressable.

**Anharmonicity (α)** — the amount by which each successive transition
frequency drops, α ≈ −200 to −340 MHz. Small anharmonicity is what limits
how fast a pulse can drive one transition without disturbing its neighbours.

**E_J/E_C** — ratio of Josephson to charging energy (≈ 50–100 in the
"transmon regime", up to 325 in the d = 12 device of Wang et al.). Raising
it exponentially suppresses charge noise; it is the **design parameter**
that sets how badly higher levels dephase.

**Charge dispersion** — residual sensitivity of a level's frequency to
stray charge. It grows steeply with level index (|2⟩ is ≥10× worse than
|1⟩), which is why real transmon dephasing follows a max-level rather than
a (Δlevel)² law.

**Bosonic enhancement** — because the transmon is nearly harmonic, its
coupling to the environment carries the ladder-operator matrix element √k,
so level k relaxes ≈ k times faster. Measured exponent ≈ 0.7, not 1.

**Max-level dephasing law** — the empirical rule replacing (Δlevel)²: any
coherence *touching* level 2 dephases ~2× faster, essentially regardless of
its partner. Measured ratios Γφ 01 : 12 : 02 = 1 : 2.0 : 2.3.

**Cross-Kerr coupling** — an always-on conditional phase shift between
neighbouring qudits (0.1–0.7 MHz). A *coherent* error our Markovian models
omit; it can destroy an unprotected two-qutrit Bell state in ~1 µs.

**Dispersive readout** — measuring a qudit by the state-dependent frequency
shift it induces on a coupled resonator, probed with a weak microwave tone.

**Mølmer–Sørensen (MS) gate** — the standard trapped-ion entangling gate,
mediated by a shared motional mode. Ringbauer's fully entangling qudit gate
costs 2(d−1) of them — the basis of our `ion` cost model.

**Cex / Cinc** — trapped-ion two-qudit entanglers: Cex acts on a *subspace*
(cost independent of d), Cinc entangles the full space (cost 2(d−1)).

**Dynamical decoupling (DD)** — pulse sequences that refocus dephasing.
Qudit DD helps *more* at higher d, but its pulse cost grows as 2(d−1) and it
cannot touch amplitude damping.

**ODMR (optically detected magnetic resonance)** — the standard NV-center
readout: spin state is inferred from fluorescence intensity. The basis of
the benchtop experiment E2 in `EXPERIMENTS.md`.

**Randomized benchmarking (RB) / SPAM** — RB extracts an average error per
Clifford from random gate sequences; SPAM is state-preparation-and-
measurement error, which our simulations idealize away.

### Cost & compilation terms

**Gate cost model** — how many time-layers a gate occupies as a function of
d. Three are implemented (`uniform`, `ion`, `pavlidis`); see §3.3 and
`COST_SENSITIVITY.md`. This is the single most consequential modelling
choice in the project.

**Native qudit gate** — an entangling gate acting on the full d²-dimensional
two-qudit space in one physical operation (e.g. Goss's cross-Kerr CZ), as
opposed to one **decomposed** into many two-level rotations. Our central
finding is that the qudit advantage exists *iff* the gate is native.

**Emulated-binary encoding** — running a qubit algorithm inside two levels
of a qudit. Bocharov 2016 found this can *beat* native ternary arithmetic,
which is why qudit advantages must not be attributed to encoding density.

**Semigroup / fractional channel power** — both our noise families satisfy
E^s ∘ E^t = E^(s+t), so a non-integer gate cost is applied *exactly*:
Lindblad models scale the rate, depolarizing uses 1 − (1−p)^t.

### Mechanism terms

**Control–work entanglement** — correlation between the phase-carrying
control register and the arithmetic work register. Shor's modular
multiplication creates it maximally; eigenstate QPE creates none.

**Which-path information** — when the work register's state reveals which
control-register branch was taken, noise on the work register dephases the
control *even if the control itself is untouched*. Our proposed explanation
for why Shor and eigenstate QPE order oppositely.

**Entanglement entropy** — von Neumann entropy of the control register's
reduced state, S = −Σ p log₂ p, measured in bits across the control:work
cut. Zero for eigenstate QPE; log₂ K for a K-fold eigenstate superposition;
**2 bits for Shor** (r = 4). The x-axis of the interpolation experiment.

**Eigenstate superposition (K-fold)** — a work-register input
Σ_{j<K}|u_j⟩/√K. Since Shor's |x = 1⟩ is exactly an equal superposition of
the r eigenstates of the modular multiplier, sweeping K interpolates
continuously between eigenstate QPE (K = 1) and Shor (K = r = 4).

**Noise exposure** — carriers × time-layers: how many (qudit, layer)
noise events a run pays. The compression of exposure at matched problem
size is the mechanism candidate tested across algorithms; Shor compresses
it ~11× from d = 2 to d = 5, Grover ~6× (width only).

**Per-event damage (1 − F_e)** — the entanglement infidelity of one
carrier-layer of the actual channel, 1 − tr(S)/d² for superoperator S.
Exposure × strength counts *events*; exposure × (1 − F_e) counts *damage*,
and the two differ by a d-dependent factor: 0.75s / 1.46s / 2.82s for
d = 2/3/5 under the calibrated ladder, p(1 − 1/d²) under depolarizing.
Damage units are what make Grover's bases collapse onto one exponential
(`exposure_collapse.py`, `docs/GROVER.md` §5).

**Exposure collapse** — the test of whether floor-corrected signal is a
function of accumulated noise alone, fitted as A·exp(−k·x) across both
algorithms, all bases and sizes. In damage units the collapse holds per
algorithm (shared amplitude, per-algorithm rate: R² = 0.93–0.94); what it cannot absorb is the decoder transfer (next entry).

**Decoder transfer function** — the map from end-state fidelity to
measured signal. Grover's is the identity (signal *is* marked-state
survival); Shor's continued-fraction order recovery is error-tolerant
with tolerance growing with register size, which flattens signal against
exposure (d = 3 sits at ~0.72 signal while exposure triples). Measured
directly in `fidelity_collapse.py`: end-state *fidelity* obeys a single
damage-unit exponential across both algorithms (R² = 0.97 / 0.99,
amplitude ≈ 1) where decoded *signal* does not — the residual structure
in the signal collapse is entirely the decoder.

### Metric terms

**Golden-ratio conjugate (φ* ≈ 0.6180)** — the QPE target phase, chosen
because it is far from every fraction with a small base-2/3/5 denominator,
so no base is accidentally favoured by the phase being exactly
representable on its grid.

**Phase window / bits of precision** — QPE success is defined as the
measured estimate landing within 2^−(b+1) of the target, i.e. the phase is
correct to b = 5 bits. Its random floor (≈ 2^−b) is far cleaner than
Shor's continued-fraction floor.

**Floor-corrected signal** — (success − random floor)/(noiseless − random
floor): 1 = perfect interference, 0 = indistinguishable from guessing,
negative = actively biased away from the answer. Every comparison in this
project uses it, because raw success probabilities have base-dependent
floors and would flatter some bases over others.

---

## 2. ASCII diagrams

### 2.1 Level ladders and why "transmon" noise punishes big d

Decay rate of level |k⟩ is k·γ; dephasing between |j⟩,|k⟩ goes as (j−k)².

```
   qubit (d=2)        qutrit (d=3)          ququint (d=5)

                                            |4⟩ ──╮ Γ = 4γ
                                            |3⟩ ◀─╯──╮ Γ = 3γ
                      |2⟩ ──╮ Γ = 2γ        |2⟩ ◀────╯──╮ Γ = 2γ
   |1⟩ ──╮ Γ = γ      |1⟩ ◀─╯──╮ Γ = γ      |1⟩ ◀───────╯──╮ Γ = γ
   |0⟩ ◀─╯            |0⟩ ◀────╯            |0⟩ ◀──────────╯

   capacity:          capacity:             capacity:
   1.00 qubit         1.585 qubits          2.322 qubits
```

More capacity per particle, but on ladder hardware the top levels decay
faster than the capacity grows — the core of the tradeoff.

### 2.2 The order-finding circuit (shown for d = 5, m = 3, w = 2)

```
 control ┌─────┐                                  ┌───────┐
 |0⟩ ────┤ F₅  ├────●─────────────────────────────┤       ├──▦  y₀ (MSD)
         ├─────┤    │                             │       │
 |0⟩ ────┤ F₅  ├────┼─────────●───────────────────┤ QFT†  ├──▦  y₁
         ├─────┤    │         │                   │ (Z₁₂₅)│
 |0⟩ ────┤ F₅  ├────┼─────────┼─────────●─────────┤       ├──▦  y₂
         └─────┘    │         │         │         └───────┘
 work           ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
 |x=1⟩ ═════════╡ ×7^(5⁰)╞═╡ ×7^(5¹)╞═╡ ×7^(5²)╞═   (mod 15)
                └───────┘ └───────┘ └───────┘

 measure y ∈ {0..124};  peaks near y ≈ s·125/4
```

The QFT† box is itself decomposed into F₅† gates and controlled phases
(m single-qudit + m(m−1)/2 two-qudit gates) — noise is applied per gate,
not per box.

### 2.3 The noise schedule (serial execution, everyone idles)

```
 time ──▶   layer 1     layer 2     ...     layer L
           ┌────────┐  ┌────────┐          ┌────────┐
 qudit 0   │ gate?  │  │  idle  │          │  idle  │
 qudit 1   │  idle  │  │ gate?  │   ...    │  idle  │
 qudit 2   │  idle  │  │ gate?  │          │ gate?  │
   ⋮       │   ⋮    │  │   ⋮    │          │   ⋮    │
           └────────┘  └────────┘          └────────┘
              ▼▼▼         ▼▼▼                 ▼▼▼
           noise on    noise on            noise on
           ALL qudits  ALL qudits          ALL qudits

 L = 51 layers (d=2)   26 (d=3)   15 (d=5)
```

Fewer layers × fewer qudits = less noise exposure — the qudit advantage.
Bigger qudits = bigger loss per noise event — the qudit penalty.

### 2.4 From measurement to factors (classical post-processing)

```
            y            y/D          convergents        check
 measure ─────▶ fraction ─────▶ p₁/q₁, p₂/q₂, ... ─────▶ a^q ≡ 1 mod N ?
   ▦                                                        │
                                              yes: r = minimal such q
                                                            │
                       r even and a^(r/2) ≢ −1?  ──▶  gcd(a^(r/2) ± 1, N)
                                                      = factors of N
 e.g.  y=31, D=125:  31/125 ≈ 1/4  ──▶  q=4,  7⁴ ≡ 1 ✓ ──▶ r=4
       gcd(7² − 1, 15) = 3,  gcd(7² + 1, 15) = 5   ──▶  15 = 3 × 5
```

### 2.5 Register sizing across bases (same problem, N = 15)

```
 d = 2   [c][c][c][c][c][c] [w][w][w][w]     10 qudits, D = 64,  work 16
 d = 3   [c][c][c][c] [w][w][w]               7 qudits, D = 81,  work 27
 d = 5   [c][c][c] [w][w]                     5 qudits, D = 125, work 25
                                              (control dim ≥ 64, work ≥ 15)
```

---

## 3. How we emulate the physical system

This section is the bridge between the physics and the code: what a
"qudit register" *is* inside the simulator, how the hardware's cost is
charged against it, and how each experiment's initial state is prepared.

### 3.1 Representing the register

A register of n qudits of dimension d lives in a Hilbert space of
dimension dⁿ. Two representations are used, chosen by size:

| | state stored as | memory | reachable size | used for |
|---|---|---|---|---|
| **Exact** | density matrix ρ, shape `dims + dims` (2n tensor axes) | dim² | ~3 000 dim | demo-size runs, ground truth |
| **Trajectory** | pure state ψ, shape `dims` (n axes) | dim | ~78 000 dim | scaling studies |

The density matrix is the honest object — it represents *mixed* states, so
decoherence is applied deterministically and the answer is exact. Its cost
is quadratic, which is what caps it near dimension 3 000 (a 16-qubit
register would need ~68 GB). The trajectory engine trades exactness for
reach: it propagates a pure state and applies **one randomly chosen Kraus
operator per qudit per layer**, drawn with probability Tr(K†K ρ_q) from the
qudit's reduced density matrix. Averaging many trajectories reproduces the
exact channel; statistical error falls as 1/√n. The two agree within 1σ on
every configuration where both can run (`test_trajectories_match_exact`).

Indices are **big-endian**: qudit 0 holds the most significant digit, so a
register state ↔ an integer in base d. Gates are applied by tensor
contraction on just the axes they touch (`apply_unitary`,
`apply_unitary_vec`), never by building a dⁿ × dⁿ matrix — this is what
makes 16-qudit registers tractable at all.

### 3.2 Emulating the hardware's gates

Every circuit is a list of `(sites, U, cost)` triples. The unitaries are
exact matrices, built from the qudit generalizations of familiar gates:

- **F_d** — the single-qudit Fourier gate, (F_d)_{jk} = ω^{jk}/√d. At
  d = 2 it is literally the Hadamard.
- **controlled phase** — |c₁,c₂⟩ → exp(2πi c₁c₂/d^t)|c₁,c₂⟩, the two-qudit
  glue of the QFT.
- **controlled modular multiplier** — |c⟩|x⟩ → |c⟩|aᶜx mod N⟩, a
  permutation matrix; the identity on the leakage states x ≥ N.
- **controlled-U^(dⁱ)** — for generic QPE, block-diagonal over the control
  digit, built from a random unitary with pinned eigenphases.

Two deliberate simplifications: gates are treated as **instantaneous and
perfect** (their error is charged separately, as idle decoherence during
the layers they occupy), and the compiled circuit is assumed to run
**serially**. Real hardware parallelizes some gates and has coherent gate
errors; both are listed as limitations in `SOTA.md` §5.

### 3.3 Charging the hardware's cost

Noise enters *only* through time: after each gate, **every qudit in the
register** — not just the ones the gate touched — idles through that gate's
`cost` in time-layers and is hit with the noise channel raised to that
power. Idle qudits decohere exactly like active ones, which is what makes
circuit *width* as expensive as circuit *depth*.

The cost assigned to a gate is where hardware reality enters:

| cost model | single-qudit | entangling | represents |
|---|---|---|---|
| `uniform` | 1 | 1 | a **native** qudit gate (transmon cross-Kerr CZ) |
| `ion` | 1 | d−1 | trapped ions (Cinc = 2(d−1) MS gates, normalized) |
| `pavlidis` | d²/4 | d²/4 | **no** native entangler — everything decomposed |

A controlled modular multiplier additionally costs w layers (its control
must interact with each of the w work qudits). All models are normalized so
**d = 2 costs exactly one layer**, which makes the qubit baseline identical
across models and every difference attributable to the higher dimensions.

Because both noise families are one-parameter semigroups, a *fractional*
cost is applied exactly rather than approximated: Lindblad models scale the
dimensionless rate (E^t = exp(tL)), and the depolarizing channel composes
as 1 − (1−p)^t. Verified against integer matrix powers to 10⁻¹⁶.

This charging scheme is the project's central modelling choice, and §5.3
shows it decides the answer: the same circuits give opposite orderings
under `uniform` and `pavlidis`.

### 3.4 Preparing the states

Each experiment prepares a different work-register input; the control
register always starts in |0…0⟩ and is put into uniform superposition by
the opening layer of F_d gates.

**Shor order finding.** Work register starts in the computational state
|x = 1⟩. Physically this is the multiplicative identity mod N; quantum
mechanically it is an equal superposition of the r eigenstates of the
modular-multiplication operator — which is precisely why order finding
works, and why it carries r-fold control–work entanglement.

**Eigenstate QPE.** Work register starts in a single eigenvector |u₀⟩ of
the target unitary (column 0 of the random eigenbasis V). The controlled-U
stage then only multiplies it by a phase, so the control and work registers
stay in a **product state** — no which-path information exists.

**Interpolating QPE.** Work register starts in Σ_{j<K}|u_j⟩/√K, an equal
superposition of K eigenstates. The controlled-U stage entangles it with
the control, producing exactly **log₂ K bits** of control–work entanglement
entropy (verified numerically: 0.000, 1.000, 1.585, 2.000 bits for
K = 1,2,3,4 in all three bases). Since Shor's r = 4 gives 2 bits, K sweeps
continuously from eigenstate QPE to the Shor regime with everything else —
circuit, metric, noise, cost — held fixed. The K target eigenphases are
pinned to mutually well-separated irrational values so their success
windows never overlap and none is exactly representable in any base.

**Leakage states.** When d^w > N (or > 16 for QPE), the surplus work-register
states carry no data. Unitaries act as the identity on them, but noise
scatters population into them, where it is lost — a real, d-dependent
penalty the simulator captures automatically.

### 3.5 Measuring and scoring

The control register is measured in the computational basis: the work
register is traced out and the diagonal of the control block gives the
outcome distribution (`control_probs`). Measurement itself is idealized as
perfect — a limitation, since real qudit readout degrades with level index
(|2⟩ reads out 3–7% worse than |0⟩).

Scoring differs by algorithm — Shor uses continued fractions to recover the
order, QPE uses a 5-bit phase window — but both are then **floor-corrected**
to (success − random floor)/(noiseless − random floor) so that bases with
different register dimensions, and therefore different random-guessing
baselines, can be compared on one axis.

## 4. Tests

`test_qudit_shor.py` — 10 tests, plain Python, no framework needed:

```bash
python3 test_qudit_shor.py     # ~30 s, prints "10 tests passed"
```

| test | what it guards |
|------|----------------|
| `test_qft_circuit` | the gate-decomposed QFT equals digit-reversal × dense QFT matrix, for (d,m) = (2,3), (3,3), (5,2) |
| `test_cmult_unitary` | controlled modular multipliers are permutation unitaries (U Uᵀ = I) |
| `test_channels_cptp` | both noise channels preserve trace on random states **and** are completely positive (Choi matrix ⪰ 0) for d = 2, 3, 5 |
| `test_depolarizing_fixed_point` | the maximally mixed state is exactly stationary under depolarizing |
| `test_postprocessing` | continued fractions: y = 16, 48 → r = 4; y = 32 correctly rejected (7² ≡ 4 ≠ 1); y = 0 → None |
| `test_noiseless_baselines` | trace ≈ 1 to 1e-8; d = 2 success is *exactly* 1/2 (analytic value); d = 3, 5 above 0.45 |
| `test_noise_degrades` | with noise on, trace still ≈ 1 and success strictly drops |
| `test_register_sizing` | (m, w) = (6,4) / (4,3) / (3,2) for d = 2 / 3 / 5 |
| `test_kraus_from_superop` | Choi-derived Kraus sets are complete (Σ K†K = I) and reproduce both channels exactly |
| `test_trajectories_match_exact` | the Monte Carlo engine is exact when noiseless and agrees with the density-matrix simulator within 4σ when noisy |

The most load-bearing test is `test_qft_circuit`: it pins the digit-order
convention that the whole no-swap phase-estimation construction relies on.

---

## 5. Benchmarks

Machine: Apple M4 Pro, Python 3.14, NumPy 2.5. Full density-matrix
simulation (no trajectory sampling). Reproduce with:

```bash
python3 experiments.py    # 36 runs → results/results.json  (~4 min total)
python3 plots.py          # → results/*.png
```

### 5.1 Simulation cost

| base | qudits | total Hilbert dim | ρ size (complex128) | noiseless run | noisy run (avg) |
|------|--------|-------------------|---------------------|---------------|-----------------|
| d = 2 | 10 | 1 024 | 16 MB | 0.6 s | 2.6 s |
| d = 3 | 7 | 2 187 | 76 MB | 2.0 s | 7.0 s |
| d = 5 | 5 | 3 125 | 156 MB | 2.2 s | 8.0 s |

Cost scales with (Hilbert dim)² × gate count; noise dominates because every
gate triggers a channel application on every qudit.

### 5.2 Algorithm quality — floor-corrected success signal

1 = noiseless interference fully intact, 0 = indistinguishable from random
guessing. Noiseless absolute baselines: 0.500 / 0.491 / 0.493; random
floors: 0.281 / 0.296 / 0.288 (d = 2 / 3 / 5).

**Transmon-ladder noise** (level-dependent — qubits win):

| strength/layer | d = 2 | d = 3 | d = 5 |
|---------------:|------:|------:|------:|
| 0.002 | 0.92 | 0.84 | 0.74 |
| 0.005 | 0.82 | 0.63 | 0.45 |
| 0.01  | 0.68 | 0.36 | 0.17 |
| 0.02  | 0.52 | 0.04 | −0.07 |
| 0.035 | 0.42 | −0.17 | −0.15 |
| 0.05  | 0.37 | −0.27 | −0.15 |

**Uniform depolarizing** (per-particle — slight ququint edge, qutrit lags):

| strength/layer | d = 2 | d = 3 | d = 5 |
|---------------:|------:|------:|------:|
| 0.002 | 0.93 | 0.87 | 0.91 |
| 0.005 | 0.81 | 0.69 | 0.79 |
| 0.01  | 0.61 | 0.45 | 0.61 |
| 0.02  | 0.33 | 0.16 | 0.37 |
| 0.035 | 0.12 | −0.01 | 0.16 |
| 0.05  | 0.05 | −0.05 | 0.06 |

Negative values are physical, not numerical error: amplitude damping drags
the control register toward |0…0⟩, which biases outcomes *away* from the
good set — worse than guessing.

### 5.3 Register-size scaling (quantum trajectories)

Floor-corrected signal vs phase-estimation precision, 400 trajectories per
point (200 for d = 2, m = 12), statistical error ±0.02–0.09. Reproduce with
`python3 scaling_experiment.py` (~25 min wall on 6 workers) and
`python3 plots_scaling.py`.

**Uniform depolarizing, 0.005/layer** (per-particle noise):

| precision (bits) | d = 2 | d = 3 | d = 5 |
|-----------------:|------:|------:|------:|
| ~6–7   | 0.80 (m=6) | 0.62 (m=4) | 0.74 (m=3) |
| ~8     | 0.67 (m=8) | 0.59 (m=5) | — |
| ~9–10  | 0.61 (m=10) | 0.52 (m=6) | 0.67 (m=4) |
| ~11–12 | 0.48 (m=12) | 0.44 (m=7) | 0.64 (m=5) |

Slopes: ≈ −0.053/bit (d = 2), −0.037/bit (d = 3), −0.022/bit (d = 5).
**Crossover: d = 5 passes d = 2 at ~7–8 bits and leads by ~0.16 at 12.**

**Transmon ladder, 0.003/layer** (level-dependent noise):

| precision (bits) | d = 2 | d = 3 | d = 5 |
|-----------------:|------:|------:|------:|
| ~6–7   | 0.92 (m=6) | 0.74 (m=4) | 0.65 (m=3) |
| ~8     | 0.85 (m=8) | 0.65 (m=5) | — |
| ~9–10  | 0.73 (m=10) | 0.56 (m=6) | 0.53 (m=4) |
| ~11–12 | 0.74 (m=12) | 0.60 (m=7) | 0.37 (m=5) |

Ordering monotone in d at every size; the qubit lead widens — no
crossover is coming.

Trajectory-engine cost (Apple M4 Pro): the largest configs are
d = 2, m = 12 (16 qubits, Hilbert dim 65 536, ~3.8 s/trajectory),
d = 3, m = 7 (dim 59 049, ~0.8 s), d = 5, m = 5 (dim 78 125,
~0.4 s) — sizes where the exact density matrix would need up to ~68 GB.

### 5.4 Generic phase estimation (beyond Shor)

Same grid and noise settings as §5.3, but the controlled unitaries are
powers of an arbitrary 16-dim unitary with the target eigenphase pinned to
the golden-ratio conjugate, and success = phase correct to 5 bits (random
floor ≈ 0.03). Reproduce: `python3 qpe_scaling_experiment.py` then
`python3 plots_scaling.py results/qpe_scaling.json results/qpe_scaling.png`.

Floor-corrected signal at ~7 / ~9.5 / ~11.6 precision bits:

| noise | d = 2 | d = 3 | d = 5 |
|-------|-------|-------|-------|
| depolarizing 0.005 | 0.40 / 0.22 / 0.15 | 0.66 / 0.51 / 0.45 | 0.82 / 0.76 / 0.65 |
| transmon 0.003 | 0.56 / 0.30 / 0.26 | 0.70 / 0.54 / 0.51 | 0.74 / 0.67 / 0.60 |

**d = 5 > d = 3 > d = 2 at every size under both noise models.** The
ladder-noise qubit advantage seen for Shor does not transfer: it requires
control–work entanglement with high-level work states (which-path
dephasing), which eigenstate QPE does not have. See THEORY.md §"Beyond
Shor".

### 5.5 Reading the two demo-size tables together

```
                 ladder noise            per-particle noise
 d = 2         ████████████ best       ███████ ~tie
 d = 3         █████                   █████   worst
 d = 5         ███          worst      ████████ ~tie (slight edge)
```

Same circuits, opposite orderings — the hardware's noise structure, not
the algorithm, decides whether prime-base encoding helps.
