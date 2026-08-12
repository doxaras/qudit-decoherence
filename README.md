# ai-qutrits — prime-base quantum information vs. decoherence

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21901534.svg)](https://doi.org/10.5281/zenodo.21901534)

Can storing quantum information in a **prime base** — qutrits (d = 3),
ququints (d = 5) — instead of qubits buy you resilience against
decoherence? This repo answers the question quantitatively across three
algorithms — **Shor order finding**, **eigenstate phase estimation** and
**Grover search** — under two hardware-grounded noise models, three gate
cost models, and register sizes up to 17 qubits.

> **Current headline**, after calibrating the noise to measured hardware
> data (`docs/CALIBRATION.md`), charging realistic gate costs
> (`docs/COST_SENSITIVITY.md`), removing a number-theoretic confound
> (`docs/MECHANISM.md`) and re-running every Shor study on unbiased
> instances (`docs/GRID_ALIGNMENT.md`):
>
> Prime-dimensional qudits help **all three** algorithms under one
> condition: the two-qudit entangling gate must be **native** at the
> device's operating dephasing level — its cost must grow no faster than
> linearly in d. The advantage survives ions' 2(d−1) Mølmer–Sørensen cost
> but not a d² decomposition, and refocusing (`docs/ROBUSTNESS.md`) buys
> roughly one cost model's worth of headroom.
>
> The advantage **decomposes**: Grover compresses register width but not
> oracle count, and delivers 0.29–0.49 of Shor's advantage
> (`docs/GROVER.md`). Width alone is sufficient; depth is the larger
> contribution. Counted in *damage units* (per-event channel infidelity
> rather than event count), noise exposure acts as a genuine law for
> state decay — Grover's bases collapse onto one exponential — and the
> residual cross-algorithm structure is the decoder, not the noise:
> Shor's continued-fraction recovery grows more error-tolerant with
> register size (`docs/GROVER.md` §5).
>
> An earlier version of this README reported that qudits *lose* at Shor.
> That was an artifact of the instance, not physics: N = 15 admits only
> power-of-two orders, so the qubit register always lands exactly on the
> interference peaks while qutrits and ququints never do. **Grid
> alignment predicts the winner in all 6 biased runs** (3 instances × 2
> noise models), and a
> within-modulus control (same registers, only the order changed) prices
> it at ≈ 0.2 signal. On unbiased instances (N = 21, r = 6; N = 29,
> r = 7) the ordering reverses to d = 5 > d = 3 > d = 2 — under every
> noise model, at every strength and every register size.
>
> ![grid alignment](results/grid_alignment.png)
>
> ![unbiased demo sweep](results/fair_demo.png)
>
> ![unbiased cost sensitivity](results/cost_fair.png)

The sections below record how that conclusion was reached, starting from
the idealized noise models.

> ⚠️ **Everything from here down uses the confounded N = 15 instance** and
> is kept as the project's audit trail, not as current results. Any claim
> below about qubits leading in Shor is superseded by
> `docs/GRID_ALIGNMENT.md`. The QPE results are unaffected throughout —
> their golden-ratio target phase was base-fair by construction.

**First-pass result: the hardware's *noise structure* decides the question —
the same circuits under two noise models give opposite orderings.**

- On **ladder platforms** (transmon higher levels, cavity Fock states),
  the qubit advantage is **real but confined to Shor at small scale**.
  Under noise calibrated to published per-level coherence data
  (`docs/CALIBRATION.md`) the ququint's Shor deficit shrinks from 1.3σ
  at 7 bits of precision to **0.1σ — a dead heat — by 11.6 bits**, and
  eigenstate phase estimation is a ququint win at **12–17σ** that
  *widens* with problem size. The textbook ∝k damping and (Δlevel)²
  dephasing exponents overstated the qudit penalty substantially.
- On platforms where noise is paid **per particle per unit time**
  (trapped-ion qudits, NV spin-1, time-bin photonics — modeled as uniform
  depolarizing), qudits break even at demo size with a slight ququint
  edge — and you still pocket the structural savings for free: d = 5 uses
  half the particles (5 vs 10) and a 3.4× shorter serial schedule (15 vs
  51 time-layers).
- **The advantage compounds with problem size.** A register-size scaling
  study (quantum trajectories, precision 6 → ~11.6 bits, registers up to
  16 qubits) shows the ququint signal decaying at ≈ 0.022 per precision
  bit vs ≈ 0.053/bit for qubits under per-particle noise: d = 5 overtakes
  d = 2 at ~7–8 bits and leads decisively by 12. Under ladder noise the
  qubit lead *widens* with size instead — no crossover is coming.
- **Beyond Shor, the qudit case gets stronger.** Rerunning the scaling
  study as *generic* phase estimation (arbitrary unitary, eigenstate
  input, base-fair golden-ratio target phase — the quantum-chemistry
  setting) gives d = 5 > d = 3 > d = 2 at every size under *both* noise
  models. The ladder-noise qubit win turns out to be Shor-specific: it
  requires the algorithm to entangle the phase register with a work
  register living on high, fast-decaying levels, which modular
  arithmetic does maximally and eigenstate QPE not at all. See
  `docs/THEORY.md` for the full argument.

![scaling](results/scaling.png)

![qpe scaling](results/qpe_scaling.png)

Under **hardware-calibrated** transmon noise (the honest test — see
`docs/CALIBRATION.md`), with a second regime modelling the high-E_J/E_C
devices that carry 12 levels on one transmon:

![calibrated scaling](results/scaling_calibrated.png)

See `docs/THEORY.md` for the physics (candidate physical systems, why
*prime* d is mathematically special, resource scaling of Shor in base d)
and `results/` for the measured curves.

![success vs noise](results/success_vs_noise.png)

![resources](results/resources.png)

## What is simulated

Full density-matrix evolution of the order-finding circuit
(phase estimation over Z_D):

- registers of d-level qudits, d ∈ {2, 3, 5}: control dim ≥ 64
  (m = 6/4/3 qudits), work dim ≥ N (w = 5/3/2 qudits at the headline
  instance N = 21);
- generalized Fourier gates F_d, two-qudit controlled phases, controlled
  modular multipliers |x⟩ → |aᶜ x mod N⟩, and a gate-decomposed no-swap
  inverse QFT over Z_{d^m} (verified against the dense QFT matrix);
- after every gate, **every** qudit idles through the gate's time-layers
  under a single-qudit noise channel (exact Lindblad exponential):
  - `transmon`: jump operators a (√k ladder, rate γ) and n̂ (rate γ_φ = γ);
  - `depolarizing`: ρ → (1−p)ρ + p·I/d per layer, same p for every d;
- classical post-processing by continued fractions; **success = probability
  that the exact order r is recovered** from the measured outcome.

Continued fractions also "succeed" on a substantial share of *uniformly
random* outcomes (~28–30% at N = 15, ~12–13% at N = 21), so the plots show
the floor-corrected signal (success − random floor)/(noiseless − random
floor): 1 = perfect run, 0 = fully decohered register. This isolates the
decoherence effect from finite-register artifacts.

**Choosing the instance matters as much as choosing the noise model.** An
order r that divides D = dᵐ puts the target phases exactly on grid points
and sharpens that base's interference peaks enormously — worth ≈ 0.2
signal, more than most of the decoherence effects being measured. Current
results therefore use orders that divide no power of 2, 3 or 5, and report
the residual misalignment of each. See `docs/GRID_ALIGNMENT.md`.

## Files

| file | contents |
|------|----------|
| `qudit_shor.py` | qudit density-matrix simulator + circuit construction |
| `trajectories.py` | quantum-trajectory (Monte Carlo wavefunction) engine for large registers |
| `test_qudit_shor.py` | 20 correctness tests (QFT vs dense matrix, CPTP checks, exact baselines, trajectory-vs-exact agreement, fidelity-estimator cross-check, grid-alignment predicates, unbiased-instance ordering, Grover correctness and cost accounting) |
| `experiments.py` | noise sweep → `results/results.json` |
| `scaling_experiment.py` | register-size scaling study → `results/scaling.json` |
| `qpe_generic.py` | generic phase estimation (arbitrary unitary — beyond Shor) |
| `qpe_scaling_experiment.py` | QPE scaling study → `results/qpe_scaling.json` |
| `scaling_calibrated.py` | hardware-calibrated noise study → `results/scaling_calibrated.json` |
| `cost_sensitivity.py` | gate-cost sensitivity grid → `results/cost_sensitivity.json` |
| `docs/CALIBRATION.md` | the calibrated transmon channel: fit, verification, results |
| `docs/COST_SENSITIVITY.md` | do the results survive realistic gate costs? |
| `interpolation_experiment.py` | entanglement interpolation → `results/interpolation.json` |
| `order_confound.py`, `fair_shor.py` | the grid-alignment confound → `results/order_confound.json`, `results/fair_shor.json` |
| `docs/MECHANISM.md` | falsified mechanism + the confound that overturned the Shor result |
| `grid_alignment.py` | one instance per alignment class, r = 3…7 → `results/grid_alignment.json` |
| `same_n_control.py` | alignment isolated at fixed register size → `results/same_n_control.json` |
| `fair_demo.py` | unbiased-instance noise sweep (N = 21, r = 6) → `results/fair_demo.json` |
| `scaling_fair.py` | unbiased-instance scaling study → `results/scaling_fair.json` |
| `cost_fair.py` | unbiased-instance gate-cost grid → `results/cost_fair.json` |
| `docs/GRID_ALIGNMENT.md` | **the unbiased re-run of every Shor result** |
| `jankovic_check.py` | cross-validation vs arXiv:2302.04543 → `results/jankovic.json` |
| `spam_study.py` | d-dependent readout error → `results/spam.json` |
| `dd_study.py` | dynamical decoupling sweep → `results/dd.json` |
| `qpe_hires.py` | QPE scaling at publication statistics → `results/qpe_hires_1000.json` |
| `docs/ROBUSTNESS.md` | independent validation, SPAM, and echo |
| `grover.py` | Grover search on qudit registers (exact + trajectories) |
| `grover_study.py`, `grover_cost.py` | Grover scaling and cost grid → `results/grover{,_cost}.json` |
| `docs/GROVER.md` | **the mechanism falsification test: width vs depth** |
| `exposure_collapse.py` | cross-algorithm collapse re-fit in damage units → `results/exposure_collapse.json` |
| `fidelity_collapse.py` | end-state fidelity vs decoded signal: the decoder check → `results/fidelity_collapse.json` |
| `plots.py`, `plots_scaling.py` | figures from the JSONs |
| `docs/THEORY.md` | physics background & literature pointers |
| `docs/GLOSSARY.md` | glossary of terms, ASCII diagrams, tests & benchmark tables |
| `papers/INDEX.md` | annotated index of the 42 reference papers, with verified arXiv IDs (PDFs not redistributed here — fetch via the links) |

## Run it

```bash
python3 test_qudit_shor.py   # ~3.5 min, 17 tests
python3 fair_demo.py         # ~4 min  -> results/fair_demo.json
python3 grid_alignment.py    # ~8 min  -> results/grid_alignment.json
python3 same_n_control.py    # ~7 min  -> results/same_n_control.json
python3 cost_fair.py         # ~12 min -> results/cost_fair.json
python3 scaling_fair.py      # ~1 h    -> results/scaling_fair.json
python3 plots_fair.py; python3 plots_grid.py
python3 plots_cost_fair.py; python3 plots_scaling_fair.py
```

The superseded N = 15 studies (`experiments.py`, `scaling_experiment.py`,
`scaling_calibrated.py`, `cost_sensitivity.py`, `plots.py`) still run and
are kept for the audit trail.

Requires numpy, scipy, matplotlib.

## Modeling assumptions (honest list)

- Serial gate execution; every single- or two-qudit gate is one time-layer,
  a controlled modular multiplier costs w layers (control must touch each
  work qudit). Real schedules parallelize some gates; this uniformly favors
  no particular base.
- Same per-layer noise strength across bases — i.e. gate *speed* is assumed
  d-independent. On real transmons, qutrit gates are somewhat slower
  (smaller anharmonicity); on ions, qudit gates run at qubit-like speeds.
- State preparation and measurement are noiseless.
- The demo instances (control dim 64–125, below the textbook D ≥ N²
  guarantee for continued fractions) are small enough that a random outcome
  sometimes "recovers" the order; this is handled by the floor correction,
  and all bases use the same rule. It does constrain instance choice: at
  D ≥ 64 the order r = 4 has a random floor *above* its noiseless baseline
  for every modulus except N = 15, which is why no base-2-aligned control
  instance exists (`docs/GRID_ALIGNMENT.md` §3).
- Results are reported per instance, never averaged over instances. The
  arithmetic of a single instance moves the answer by more than the noise
  model does.
