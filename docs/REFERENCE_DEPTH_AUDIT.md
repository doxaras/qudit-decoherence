# Reference Depth Audit — ai-qutrits paper/main.tex

Full-text (not abstract-level) audit of all 54 references cited in `paper/main.tex`.
For each reference: the exact claim(s) main.tex attributes to it (with section), what the
source paper actually says based on a full read of its PDF, and verification questions for
an LLM judge to check main.tex's characterization against the source.

Notes on sourcing:
- All 54 cited keys match `paper/refs.bib` exactly (no missing/orphaned citations).
- 48 references had PDFs already in `papers/`; 6 more (`shor1997`, `grover1996`,
  `kitaev1995`, `hrmo2023`, `meth2025`, `sutherland2023`) were freshly downloaded from
  arXiv for this audit.
- 4 references (`dalibard1992`, `molmer1993`, `hardy2008`, `khinchin1964`) are pre-arXiv
  papers or standard textbooks with no downloadable full text; those sections are marked as
  based on bibliographic metadata / well-established textbook content rather than a direct PDF read.

## Table of contents

- [`agrawal2025`](#agrawal2025)
- [`barenco1996`](#barenco1996)
- [`barzen2022`](#barzen2022)
- [`blok2021`](#blok2021)
- [`bocharov2017`](#bocharov2017)
- [`bourdon2007`](#bourdon2007)
- [`campbell2012`](#campbell2012)
- [`campbell2014`](#campbell2014)
- [`chappell2011`](#chappell2011)
- [`chiesa2024`](#chiesa2024)
- [`dalibard1992`](#dalibard1992)
- [`ekera2024`](#ekera2024)
- [`floratos2024`](#floratos2024)
- [`gardill2020`](#gardill2020)
- [`gerjuoy2005`](#gerjuoy2005)
- [`gokhale2019`](#gokhale2019)
- [`goss2022`](#goss2022)
- [`goss2024`](#goss2024)
- [`gottesman1999`](#gottesman1999)
- [`gross2006`](#gross2006)
- [`grover1996`](#grover1996)
- [`gustafson2022`](#gustafson2022)
- [`gustafson2025synthesis`](#gustafson2025synthesis)
- [`hardy2008`](#hardy2008)
- [`hrmo2023`](#hrmo2023)
- [`jankovic2024`](#jankovic2024)
- [`keppens2025`](#keppens2025)
- [`khinchin1964`](#khinchin1964)
- [`kiktenko2025`](#kiktenko2025)
- [`kitaev1995`](#kitaev1995)
- [`low2023`](#low2023)
- [`lu2020`](#lu2020)
- [`magdon2025`](#magdon2025)
- [`marks2017`](#marks2017)
- [`meth2025`](#meth2025)
- [`molmer1993`](#molmer1993)
- [`nam2012`](#nam2012)
- [`nikolaeva2024`](#nikolaeva2024)
- [`parasa2011`](#parasa2011)
- [`pavlidis2021`](#pavlidis2021)
- [`peterer2015`](#peterer2015)
- [`ringbauer2022`](#ringbauer2022)
- [`robert2026`](#robert2026)
- [`roy2022`](#roy2022)
- [`rubinosanz2025`](#rubinosanz2025)
- [`shi2025`](#shi2025)
- [`shor1997`](#shor1997)
- [`sutherland2023`](#sutherland2023)
- [`tripathi2025`](#tripathi2025)
- [`venturelli2025`](#venturelli2025)
- [`wang2020`](#wang2020)
- [`wang2025`](#wang2025)
- [`weng2024`](#weng2024)
- [`yurtalan2020`](#yurtalan2020)

---

## `agrawal2025` — Tradeoff between noise and banding in a quantum adder with qudits (Agrawal, Konar, Lakkaraju, Sen(De), 2025)

**Full citation:** G. Agrawal, T. K. Konar, L. G. C. Lakkaraju, A. Sen(De), "Tradeoff between noise and banding in a quantum adder with qudits," Phys. Rev. A **111**, 032408 (2025); arXiv:2310.11514.
**Source:** arXiv:2310.11514v3 (8 Apr 2025), Phys. Rev. A 111, 032408, PDF: `agrawal-2023-noise-banding-qudit-adder.pdf`

**Cited in main.tex:**
- *Introduction*: "The closest cross-dimension noisy study is a QFT-based adder under local noise across arbitrary $d$; it compares a single arithmetic primitive rather than a full algorithm with its decoder."
- *Introduction* (related-work list): "Agrawal et al. = one primitive, no decoder, no calibrated channel."

**What the paper actually shows (full-text, not abstract-level):**
- **Scope is exactly one arithmetic primitive.** The circuit studied is the Draper-style QFT adder in base $d$: QFT encoding → SUM block of controlled rotations $R_d^{\tilde q}$ → IQFT decoding (Sec. II, Fig. 1). No modular exponentiation, no order finding, no Shor, no Grover, no phase estimation. The word "algorithm" in the paper refers to "the quantum addition algorithm."
- **No decoder / no classical post-processing.** The figure of merit throughout is the Uhlmann fidelity $f=\langle\Psi^\alpha|\rho^\alpha_{er}|\Psi^\alpha\rangle$ between the ideal output state and the banded/noisy output state (Sec. II B), plus the normalized $\ell_1$-norm of coherence $C^N_{\ell_1}=\sum_{i\neq j}|\rho_{ij}|/(D-1)$ (Eq. 5). There is no success-probability metric that runs measurement outcomes through a classical acceptance rule.
- **Noise model is a uniform single-parameter local channel, not calibrated to per-level hardware coherence.** Kraus operators are level-independent: PDC $M_0=\sum_i\sqrt{1-p}|i\rangle\langle i|$, $M_{i+1}=\sqrt p |i\rangle\langle i|$; ADC $M_0=\sum_k\sqrt{1-kp}|k\rangle\langle k|$, $M_i=\sum_k\sqrt p|k\rangle\langle k+i|$; DPC $\rho\to p\,I_d/d+(1-p)\rho$; plus a correlated/uncorrelated Pauli mixture (Sec. III B, Sec. IV "Correlated Noise"). $p$ is a free knob (values used: 0.002–0.05, up to 0.4 in the map plots), never fitted to measured $T_1$/$T_2$ of any device. The noise acts after each controlled rotation on both control and target qudit.
- **Analytic banding bound (Proposition 1):** $q \ge \tfrac12\log_d\!\big[(n-1)(d^2-1)\pi^2/(3\epsilon)\big]$; the authors note it "decreases with the increase of $d$, thereby establishing an advantage of dimensions in terms of the circuit depth."
- **Dimensions actually studied:** $d=2,3,4$ for coherence (Fig. 3), $d=2,3$ for banding fidelity (Figs. 4, 8, 10), $d=2,3,4$ for the $f_{\max}/q_{\text{best}}$ map plots (Fig. 11), and a single sweep $d=2\ldots10$ at fixed $\max(a,b)=500$, $p=0.1$ (Fig. 7). No prime-dimension framing; $d=4$ (non-prime) is treated on the same footing.
- **Dimensional-gain claim is conditional.** Verbatim: "It seems that $f_{\max}$ decreases as the dimension increases although $q_{\text{best}}$ improves (see Fig. 8). To manifest the dimensional gain, we fix the total number of qudits depending on the input." Matched Hilbert-space comparison used: 22 qubits ($2^{22}$), 14 qutrits ($3^{14}$), 11 ququarts ($4^{11}$).
- **Headline result:** non-monotonic fidelity vs banding order $q$; an optimal $q_{\text{best}}$ exists, it saturates with $n$ for fixed $p$, giving $O(1)$ SUM-circuit depth (e.g. $q=5$–$6$ suffices at $p=0.1$–$0.2$ even for 90 qubits). Banding the SUM circuit works; banding the QFT/IQFT (AQFT) does not reproduce the advantage and is input-dependent (Fig. 13).
- **Gate-cost models:** none. There is no entangling-gate cost model, no native-gate vs decomposed-gate comparison, no Mølmer–Sørensen counting. Depth is counted in controlled-rotation orders only.
- **Hardware:** no experiment. A proposed spin-chain/Ising analogue implementation (Sec. V) is qubit-level ($\sigma_x,\sigma_z$ Hamiltonians, Eqs. 28–29), simulated for adding 7+7 on 4 qubits.

**Judge verification questions:**
- Main.tex calls this "a QFT-based adder under local noise across arbitrary $d$." The paper's analytic results (Prop. 1, Eqs. 8–9, 25–26) are indeed for general $d$, but every numerical figure uses $d\le 4$ except one sweep to $d=10$. Is "arbitrary $d$" a fair description, or does it overstate the numerical coverage?
- Main.tex says the study has "no decoder." Is there anywhere in Agrawal et al. a classical post-processing / acceptance step, as opposed to state fidelity and $\ell_1$ coherence? (Answer should be: no.)
- Main.tex says "no calibrated channel." Do Agrawal et al. anywhere tie their $p$, or the level-dependence of their Kraus operators, to measured per-level $T_1$/$T_2$ data? (Answer should be: no — $p$ is a free parameter and the PDC/DPC operators are level-symmetric; only the ADC has a $\sqrt{1-kp}$ level dependence.)
- Main.tex positions this as "the closest cross-dimension noisy study." Is that defensible given the paper does compare $d=2$ vs $d=3$ vs $d=4$ under a common noise strength at matched Hilbert-space dimension (Sec. IV, "Dimensional gain")?

---

---

## `barenco1996` — Approximate Quantum Fourier Transform and Decoherence (Barenco, Ekert, Suominen, Törmä, 1996)

**Full citation:** A. Barenco, A. Ekert, K.-A. Suominen, P. Törmä, "Approximate quantum Fourier transform and decoherence," Phys. Rev. A **54**, 139–146 (1996); arXiv:quant-ph/9601018.
**Source:** arXiv:quant-ph/9601018v1, Phys. Rev. A 54, 139, PDF: `barenco-1996-approximate-qft-decoherence.pdf`

**Cited in main.tex:**
- *Introduction*: "Qubit evidence that order finding tolerates truncation of small QFT rotations" — cited alongside `nam2012` as the empirical basis Pavlidis & Floratos invoke when conjecturing "a similar robustness" for qudits.

**What the paper actually shows (full-text, not abstract-level):**
- **Truncation is exactly what is studied.** The AQFT of degree $m$ drops every two-qubit gate $B_{jk}$ whose phase satisfies $\theta_{jk}=\pi/2^{k-j}<\pi/2^m$. Gate count falls from $L$ A-gates $+\,L(L-1)/2$ B-gates to $L$ A-gates $+\,(2L-m)(m-1)/2$ B-gates; execution time $\sim Lm$ instead of $\sim L^2$ (Sec. 3).
- **Noiseless truncation bound (Appendix, Eq. 41):** $\mathrm{Prob}_A \ge \tfrac{8}{\pi^2}\sin^2\!\big(\tfrac{\pi m}{4L}\big)$, reducing to Shor's $4/\pi^2$ at $m=L$. Repetition overhead: $k'/k < C\,(L/m)^3$ — "the AQFT is not less efficient than the ordinary QFT, i.e., the ratio $k'/k$ scales only polynomially with $L/m$" (Sec. 4, Eq. 15).
- **There is a hard floor on how far you may truncate:** $\Delta_{\max}=\tfrac{2\pi}{2^m}(L-m-1+2^{m-L})$ must satisfy $\Delta_{\max}<\pi/2$, which for large $L$ gives $m > \log_2 L + 2$ (Eqs. 37–38, 21). Below this the Argand-diagram vectors scramble and "the probability $\mathrm{Prob}_A(\bar c)$ can become vanishingly small and the AQFT of order $m$ is inefficient" (Fig. 10 caption).
- **The "less is more" decoherence result.** Quality factor $Q$ = probability of measuring the integer nearest a multiple of $2^L/r$. For $\delta>0$ (nonzero decoherence), "the maximum of $Q$ is obtained for $m<L$. Thus in the presence of decoherence one should use the AQFT rather than the QFT" (Sec. 6). At $\delta=0$, $Q$ is almost flat for all $m$ above the $m>\log_2 L+2$ bound; when $\delta>0$ the optimum $m$ sits *near* that lower bound.
- **Decoherence model is deliberately narrow:** a random Gaussian phase kick of width $\delta$ applied only when a qubit is touched by a **B (two-qubit) gate**. "In our model we have not attached any decoherence effects to gate A" and none to wires/idling; the authors state that including them "would not affect our results much, only the time scale for decoherence would change" (Sec. 6). Simulation ensembles: "typically one to two thousands individual realisations."
- **Purely qubit, purely $s=2^L$.** Register sizes shown: $L=9$, $L=12$, $L=16$; $\delta\in\{0.01,0.02,0.03,\dots,0.5\}$. Example state $f(a)=\delta_{9,\,a\bmod 10}$, i.e. $r=10$, $l=9$.
- **Important scope limit:** the object transformed is an idealized *already-periodic* register state $|\Psi\rangle=\frac{1}{\sqrt N}\sum_a \delta_{l,a\bmod r}|a\rangle$ (Eqs. 11–12, 22–23). The modular-exponentiation stage of Shor is not simulated, and the classical continued-fraction decoder is not modelled — the metric stops at "did we measure an integer near a multiple of $2^L/r$."

**Judge verification questions:**
- Main.tex attributes to `barenco1996` the claim that "order finding tolerates truncation of small QFT rotations." Barenco et al.'s tolerance is bounded: it fails for $m \le \log_2 L + 2$. Does main.tex's sentence carry (or need) that qualification, given it is being used only as the antecedent for someone else's conjecture?
- Barenco et al. simulate the QFT applied to a pre-prepared periodic state, not full order finding with modular exponentiation and a continued-fraction decoder. Is main.tex's phrase "order finding tolerates truncation" an accurate summary of a periodicity-estimation-only result?
- Barenco et al.'s decoherence is a phase kick attached *only* to two-qubit gates, with no idle/relaxation channel. If main.tex anywhere leans on this reference for a claim about idle decoherence or about relaxation, is that outside the paper's model?
- Does main.tex correctly present this as qubit ($d=2$) evidence only? (The paper never treats $d>2$.)

---

---

## `barzen2022` — Continued Fractions and Probability Estimations in Shor's Algorithm: A Detailed and Self-Contained Treatise (Barzen & Leymann, 2022)

**Full citation:** J. Barzen, F. Leymann, "Continued fractions and probability estimations in Shor's algorithm: A detailed and self-contained treatise," AppliedMath **2**(3), 393–432 (2022); arXiv:2205.01925 [math.HO].
**Source:** arXiv:2205.01925, AppliedMath 2(3), 393–432, PDF: `barzen-2022-continued-fractions-shor-treatise.pdf`

**Cited in main.tex:**
- *Why the decoder gains tolerance with size*: listed among the "exact literature [that] bounds the success of continued-fraction post-processing on **base-2 registers**," specifically as "the self-contained treatise of Barzen and Leymann." Main.tex then characterizes the whole group: "These analyses score outcomes inside a tolerance window of the peaks via the convergent guarantee — a sufficient condition — and typically certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$."

**What the paper actually shows (full-text, not abstract-level):**
- **It is a pedagogical/expository treatise, not a new bound.** Conclusion, Sec. 11: "the contribution at hand is very detailed on the probability estimation of being able to use the Legendre theorem in Shor's algorithm. The authors are not aware of any other publication providing these low-level details." It reproduces Preskill's lecture-note argument with full proofs; no sharper constant than $4/\pi^2$ is claimed.
- **Base-2 register, explicitly.** Section 8 bullet list: "$N$: a power of 2 (e.g. $N=2^m$) with $n^2 < N < 2n^2$," where $n$ is the integer to factor and $p$ the period. This matches main.tex's "base-2 registers."
- **Tolerance-window structure, exactly as main.tex describes.** Lemma 57: the probability that the measured $y$ lies in the window $\big[k\tfrac{N}{p}-\tfrac12,\;k\tfrac{N}{p}+\tfrac12\big]$ for some $k\in\{0,\dots,p-1\}$ is $\approx 4/\pi^2$ (assuming $q=e^{i2\pi yp/N}\neq 1$).
- **Convergent guarantee as the sufficient condition.** Theorem 59: with probability $\approx 4/\pi^2$ there is $k$ with $\big|\tfrac{y}{N}-\tfrac{k}{p}\big|<\tfrac{1}{2p^2}$, using $p<n$ and $n^2<N$ so $\tfrac{1}{2N}<\tfrac{1}{2p^2}$. Theorem 60 then applies Legendre's convergent criterion (their Theorem 35): "With probability $\approx 4/\pi^2$, $k/p$ is a convergent of $y/N$."
- **The decoder they specify (Sec. 10.1):** compute $y/N$, its continued fraction $[a_0;a_1,\dots,a_m]$, the convergents $g_u/h_u$; take $h_\omega$ = largest denominator with $h_\omega<n$; "$h_\omega\approx p$ is a candidate for the period"; then **"Check whether $p$ is in fact the period."** The $q=1$ branch (Sec. 10.2) is explicitly non-guaranteeing: "This may yield the period $p$ but does not guarantee it."
- **Nuance relevant to main.tex's "divisor $r/\gcd(s,r)$" wording:** Barzen & Leymann's Theorem 60 states that $k/p$ (their $k$ = main.tex's $s$, their $p$ = main.tex's $r$) is a convergent of $y/N$. They do *not* separately treat the case $\gcd(k,p)>1$, in which the convergent's denominator is $p/\gcd(k,p)$ — a proper divisor — rather than $p$. Their algorithm papers over this with the closing "check whether $p$ is in fact the period" step. So main.tex's blanket "certify recovery of a divisor $r/\gcd(s,r)$" is the mathematically correct reading of what a convergent gives, but it is *not* the phrasing Barzen & Leymann themselves use — they speak of determining "the period."
- **No noise, no qudits, no cross-dimension content whatsoever.** The paper contains no decoherence model, no $d>2$ register, no hardware.

**Judge verification questions:**
- Main.tex groups `barzen2022` under "exact literature [that] bounds the success of continued-fraction post-processing." Barzen & Leymann state their probability only as $\approx 4/\pi^2$ (an approximation, not a proven inequality) and describe their own contribution as expository detail rather than a new bound. Is "exact literature bounds" an overstatement for this particular entry?
- Main.tex says these analyses "score outcomes inside a tolerance window of the peaks." Does Barzen & Leymann's Lemma 57 window $\big[kN/p-1/2,\;kN/p+1/2\big]$ match that description? (It does.)
- Main.tex says these analyses "typically certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$." Barzen & Leymann's Theorem 60/Sec. 10.1 present the convergent denominator directly as the period candidate and close with a verification step, not a divisor-lifting search. Is main.tex's characterization accurate for this reference, or only for `bourdon2007`/`gerjuoy2005`?
- Main.tex asserts all these analyses are on **base-2** registers. Does Barzen & Leymann's "$N$ a power of 2 with $n^2<N<2n^2$" confirm it? (Yes, Sec. 8.)

---

---

## `blok2021` — Quantum Information Scrambling on a Superconducting Qutrit Processor (Blok, Ramasesh, Schuster, et al., 2021)

**Full citation:** M. S. Blok, V. V. Ramasesh, T. Schuster, K. O'Brien, J. M. Kreikebaum, D. Dahlen, A. Morvan, B. Yoshida, N. Y. Yao, I. Siddiqi, "Quantum information scrambling on a superconducting qutrit processor," Phys. Rev. X **11**, 021010 (2021); arXiv:2003.03307.
**Source:** arXiv:2003.03307v2 (10 Feb 2021), Phys. Rev. X 11, 021010, PDF: `blok-2020-scrambling-superconducting-qutrit.pdf`

**Cited in main.tex:**
- *Introduction*: "Processors that exploit more than two usable levels as qudits now exist or are proposed on several platforms" (grouped with `ringbauer2022`, `goss2022`, `low2023`, `gardill2020`, `chiesa2024`, `robert2026`).
- *Introduction*: source of "published per-level transmon coherence measurements" used to calibrate the anharmonic-ladder channel (with `peterer2015`, `goss2022`, `tripathi2025`, `wang2025`).
- *Noise channels*: "the relaxation ratio $\Gamma_2/\Gamma_1$ is measured at ${\approx}1.7$" across nine devices, $d=3$–$12$ (with `goss2022`, `tripathi2025`, `peterer2015`, `yurtalan2020`, `wang2025`).
- *Noise channels*: "the dephasing ratios $\Gamma_\phi^{01}:\Gamma_\phi^{12}:\Gamma_\phi^{02}$ are measured at $1:2.0:2.3$ — incompatible with the textbook $(\Delta\text{level})^2$ law (which predicts $1:1:4$) because **the charge dispersion of $|2\rangle$ exceeds that of $|1\rangle$ by an order of magnitude**" — this last clause is attributed to `blok2021` alone.
- *Robustness*: "few-percent, higher-is-worse readout errors reported for transmon qutrits" motivating the $(1+k)$ misread model (with `goss2022`).
- *Robustness*: "transmon qutrit assignment fidelities of $97$–$99\%$ for $|0\rangle$ and $92$–$96\%$ for $|2\rangle$" (with `goss2022`).
- *Robustness*: "the charge dispersion of $|2\rangle$ that drives idle dephasing is the same mechanism that limits the cross-Kerr entangler, so idle and gate error should co-scale" (with `goss2022`).

**What the paper actually shows (full-text, not abstract-level):**
- **Platform:** five fixed-frequency transmon qutrits ($Q_1$–$Q_5$) on an eight-transmon ring chip, $d=3$ only. Nb on intrinsic Si, Al/AlO$_x$ Manhattan junctions. $E_J/E_C\approx73$.
- **Readout fidelities — Table II (per qutrit $Q_1$–$Q_5$):**
  - $|0\rangle$: **0.99, 0.99, 0.97, 0.98, 0.99** → range **97–99%**, exactly matching main.tex.
  - $|1\rangle$: 0.97, 0.95, 0.94, 0.95, 0.96.
  - $|2\rangle$: **0.95, 0.94, 0.92, 0.95, 0.96** → range **92–96%**, exactly matching main.tex.
  - Main text: "Averaged over all qutrits, our readout fidelity is $F_{avg}=0.96\pm0.02$"; single-shot readout "generally achievable with fidelities above 0.95… largely limited by decay during readout." Higher levels are read worst — consistent with the $(1+k)$ misread model's direction.
- **Relaxation — Table II and main text:** $T_1^{1\to0}$ per qutrit = 70, 49, 43, 55, 63 µs (average $56.0\pm10$ µs); $T_1^{2\to1}$ = 38, 29, 39, 32, 36 µs (average $34.8\pm4$ µs). Ratio of averages $\Gamma_2/\Gamma_1 = 56.0/34.8 = \mathbf{1.61}$; per-device ratios 1.84, 1.69, 1.10, 1.72, 1.75. The paper's *prose* asserts the textbook expectation, not the measurement: "Due to bosonic enhancement… the time constant associated with $|2\rangle\to|1\rangle$ decay is roughly half that of the $|1\rangle\to|0\rangle$ transition" and (Appendix B2) "proceeds roughly twice as fast." **The measured numbers (1.61) sit well below the "roughly 2" the authors state in words** — which is precisely the direction main.tex's $1.7$-vs-$2.0$ argument needs, but it means main.tex is relying on Blok's *table*, not Blok's *sentence*.
- **Dephasing — Table II:** $T_2^*$ $|1\rangle/|0\rangle$ = 73, 13, 41, 48, 20 µs (avg $39\pm21$); $T_2^*$ $|2\rangle/|1\rangle$ = 13, 10, 16, 23, 10 µs (avg $14\pm5$); $T_2^*$ $|2\rangle/|0\rangle$ = 16, 6, 15, 26, 11 µs (avg ≈14.8). Echo: $T_2^{\rm echo}$ $|1\rangle/|0\rangle$ = 71, 51, 46, 64, 74 (avg $61.2\pm11$); $|2\rangle/|1\rangle$ = 29, 22, 22, 35, 32 (avg $28\pm5$); $|2\rangle/|0\rangle$ = 39, 26, 34, 45, 39 (avg ≈36.6). Rate ratios from the echo averages: $1 : 2.19 : 1.67$ for $01:12:02$; from $T_2^*$: $1 : 2.79 : 2.64$. **In both cases the $0$–$2$ coherence is comparable to or better than the $1$–$2$ coherence, i.e. nowhere near the $4\times$ that a $(\Delta\text{level})^2$ law predicts.** This directly supports main.tex's "incompatible with the textbook $(\Delta\text{level})^2$ law."
- **Charge dispersion — the clause main.tex attributes solely to Blok:** main text Sec. II A(ii): "the charge dispersion of the $|2\rangle$ state is at least an order of magnitude greater than that of the $|1\rangle$ state, resulting in a charge-limited dephasing time ten times lower than that of the qubit subspace." Appendix B2 gives the numbers: at $E_J/E_C\approx50$, dispersions were **102 kHz ($|2\rangle$) vs <10 kHz ($|1\rangle$)**; after moving to $E_J/E_C\approx73$, **12 kHz ($|2\rangle$) vs 261 Hz ($|1\rangle$)** — a factor of ~46, i.e. more than an order of magnitude. At $E_J/E_C\approx50$ "charge-parity fluctuations dephase the coherence between the $|2\rangle$ and $|1\rangle$ states within 5 µs, making high-fidelity gates impossible."
- **Cross-Kerr entangler.** Always-on dispersive cross-Kerr $H_{cK}/\hbar=\alpha_{11}|11\rangle\langle11|+\alpha_{12}|12\rangle\langle12|+\alpha_{21}|21\rangle\langle21|+\alpha_{22}|22\rangle\langle22|$; measured $\alpha_{ij}$ (Table I, kHz): $Q_1/Q_2$ = −279/160/−528/−743; $Q_2/Q_3$ = −138/158/−335/−342; $Q_3/Q_4$ = −276/−631/243/−748; $Q_4/Q_5$ = −262/−495/−528/−708. Underlying exchange coupling $g\approx3$ MHz. Controlled-phase/controlled-SUM built from four segments of cross-Kerr evolution interleaved with $\pi^{12}$ swap pulses, total time **$\sim1.5$ µs**. **Measured cSUM process fidelity 0.889, "primarily limited by decoherence occurring throughout the cross-Kerr time evolution."** The scrambling unitary (two cSUM gates) has process fidelity **0.875**, "with two dominant error mechanisms: (i) dephasing and (ii) amplitude-damping during the cross-Kerr evolution." The first (simpler) cross-Kerr construction is described as "prone to local dephasing."
- **Other measured numbers:** single-qutrit gates in 30 ns; RB fidelities $f_{01}=0.9997\pm0.0001$, $f_{12}=0.9994\pm0.0001$ (per-Clifford errors in Table II: $3.6/3.9/5.5/2.7/3.6\times10^{-4}$ for $|1\rangle/|0\rangle$ and $6.0/5.0/7.5\times10^{-4}$ for $|2\rangle/|1\rangle$). Cross-resonance conditional-$\pi$ gate: $t_g=125$ ns, $\omega_0-\omega_1=4$ MHz, EPR state fidelity $F_{\rm EPR}=0.98\pm0.002$ "mostly limited by decoherence." Teleportation $F_{avg}=0.568\pm0.001$, OTOC upper bound $0.618\pm0.004$; classical qutrit limit 0.5, random-guess 1/3.
- **Caveats the authors themselves state:** the cross-resonance qutrit Hamiltonian model "is only approximate… further study is needed"; RB was done as *qubit* RB in two subspaces and "is not sensitive to certain sources of errors, including phase errors in the idle state and multi-qutrit errors" — "a full characterization of qutrit operations will require the development of genuine qutrit randomized benchmarking protocols."
- **What the paper does NOT contain:** no algorithm benchmark, no $d>3$, no error-mitigation demonstration (that is later work by the same group), no explicit statement that the charge dispersion of $|2\rangle$ *is* the mechanism limiting the cross-Kerr gate. Blok attributes the cSUM/scrambler infidelity to "decoherence"/"dephasing and amplitude damping during the cross-Kerr evolution," and separately attributes qutrit dephasing to charge dispersion of $|2\rangle$ — main.tex's joining of these two into one shared mechanism is an *inference*, not a quoted claim.

**Judge verification questions:**
- Main.tex states transmon qutrit assignment fidelities of "$97$–$99\%$ for $|0\rangle$ and $92$–$96\%$ for $|2\rangle$." Blok Table II gives $|0\rangle$: 0.99/0.99/0.97/0.98/0.99 and $|2\rangle$: 0.95/0.94/0.92/0.95/0.96. Do the ranges match exactly? (They do — but confirm main.tex is not implying these ranges also come from `goss2022` with the same numbers.)
- Main.tex says the relaxation ratio $\Gamma_2/\Gamma_1$ is "measured at ${\approx}1.7$… against $2.0$ for the textbook $\Gamma_k\propto k$ ladder." Blok's own *prose* says $|2\rangle\to|1\rangle$ decay "proceeds roughly twice as fast," while Blok's Table II gives $56.0/34.8=1.61$. Is main.tex's use of the table over the prose legitimate, and is $1.61$ consistent with a pooled ${\approx}1.7$?
- Main.tex says the dephasing ratios are "measured at $1:2.0:2.3$" and are "incompatible with the textbook $(\Delta\text{level})^2$ law (which predicts $1:1:4$)." From Blok's Table II, echo-based rate ratios are $1:2.19:1.67$ and $T_2^*$-based $1:2.79:2.64$. Does Blok's $02$ coherence support a $02$ rate near $2.3\times$ the $01$ rate rather than $4\times$? Does main.tex's pooled $1:2.0:2.3$ remain defensible with Blok included?
- Main.tex attributes to `blok2021` that "the charge dispersion of $|2\rangle$ exceeds that of $|1\rangle$ by an order of magnitude." Blok says "at least an order of magnitude" (main text) and gives 12 kHz vs 261 Hz (~46×) and 102 kHz vs <10 kHz (~10×) in Appendix B2. Accurate?
- Main.tex claims "the charge dispersion of $|2\rangle$ that drives idle dephasing is **the same mechanism that limits the cross-Kerr entangler**." Blok attributes cSUM infidelity (0.889) to "decoherence occurring throughout the cross-Kerr time evolution" and the scrambler (0.875) to "dephasing and amplitude-damping during the cross-Kerr evolution," without naming charge dispersion as the gate limiter. Is main.tex's causal identification an inference beyond what Blok states, and is main.tex flagged as such ("the physics leans to the harsher reading")?
- Main.tex's Robustness passage says "the operative target is $98.2\%$, $0.9$ points above the measured gate," implying a measured two-qutrit gate fidelity of $97.3\%$. Blok's measured two-qutrit numbers are cSUM 0.889 and conditional-$\pi$-derived EPR 0.98. Does the $97.3\%$ figure come from `goss2022` rather than `blok2021`, and does main.tex's sentence make that attribution clear?

---

---

## `bocharov2017` — Factoring with Qutrits: Shor's Algorithm on Ternary and Metaplectic Quantum Architectures (Bocharov, Roetteler, Svore, 2017)

**Full citation:** A. Bocharov, M. Roetteler, K. M. Svore, "Factoring with qutrits: Shor's algorithm on ternary and metaplectic quantum architectures," Phys. Rev. A **96**, 012306 (2017); arXiv:1605.02756.
**Source:** arXiv:1605.02756v4 (8 Apr 2017), Phys. Rev. A 96, 012306, PDF: `bocharov-2016-factoring-with-qutrits-shor.pdf`

**Cited in main.tex:**
- *Introduction*: listed as one of the indirect ways cross-dimension comparisons "still treat noise": "analytic coherent-error bounds."
- *Discussion*: "Bocharov et al. show emulated-binary arithmetic can beat native ternary — encoding density alone is not a mechanism — which is consistent with our attribution of the advantage to width-and-depth compression under a per-carrier noise budget, and with its disappearance when compilation buys the compression back."

**What the paper actually shows (full-text, not abstract-level):**
- **It is a fault-tolerant resource count, not a noise simulation.** Costs are non-Clifford magic-state counts ($P_9$ for the generic ternary Clifford+$P_9$ platform, $R_{|2\rangle}$ for the metaplectic MTQC platform, $T$ for the Clifford+$T$ binary backdrop) and non-Clifford depth/width. There is no density-matrix simulation, no decoherence channel, no $T_1$/$T_2$.
- **The "analytic coherent-error bounds" are Appendix B, and they are purely unitary.** Proposition 16: if $|v\rangle$ is at Hilbert distance $\varepsilon$ from $\mathrm{QFT}|u\rangle$, the useful-measurement probability exceeds $p_{\rm useful}-2\sqrt{p_{\rm useful}}\,\varepsilon$. Corollary 17: if $\varepsilon<\gamma\sqrt{p_{\rm useful}}$ with $0<\gamma<1/2$, success $>(1-2\gamma)p_{\rm useful}$; at $\varepsilon<\sqrt{p_{\rm useful}}/4$ you are "at least half as likely" to succeed. Proposition 18: for $d$ imperfect *unitary* gates with $\|U_k-V_k\|\le\delta$, $\|U-V\|\le d\delta$ — linear coherent-error accumulation. Threshold: useful precision $\varepsilon \in O\!\big(1/\sqrt{\log\log N}\big)$, hence per-gate tolerance $\varepsilon/d$, i.e. $o\!\big(1/(d\sqrt{\log\log N})\big)$ (Sec. II E). **All of this is coherent/approximation error; nothing about incoherent noise.**
- **Emulated binary vs native ternary — Table III (ripple-carry additive shift, $\#P_9$):** simple shift **12n (emulated binary) vs 19n (ternary)**; controlled shift **18n vs >21n**; doubly-controlled shift **24n vs >33n**. Emulated binary wins on all three.
- **Table IV (low-width modular exponentiation):** emulated binary via $P_9$: width $n+4$, depth $48n^3$; ternary via $P_9$: width $2m-\omega_1(m)$ with $m=\lceil\log_3(2)n\rceil$, depth $\approx76.35n^3$. Emulated binary wins on **both** width and depth. Binary Clifford+$T$ backdrop (Häner et al./Takahashi): $2n+6$ qubits, $160n^3$.
- **The mechanism of the ternary width loss, in the authors' own words:** the true-ternary additive shift needs an ancilla qutrit for the carry in the $a_i\in\{0,2\}$ cases, giving "an average width of the additive shift circuit of roughly $5/3\,m$ **which eliminates the space savings afforded by denser ternary encoding** ($5/3\log_3 2\approx1.05$)." This is exactly the "encoding density alone is not a mechanism" point.
- **Conclusion, verbatim:** "An interesting feature of our ternary arithmetic circuits is the fact that the denser and more compact ternary encoding of integers does not necessarily lead to more resource-efficient period finding solutions compared to binary encoding. As a rule of a thumb: if low-width circuits are desired, then binary encoding of integers combined with ternary arithmetic gates appears more efficient both in terms of width and depth than a pure ternary solution."
- **CRITICAL CAVEAT — the result reverses with better compilation.** Same sentence continues: "**However, even a moderate ancilla-assisted depth compression, such as provided by carry lookahead additive shifts, tips the balance in favor of ternary encoding and ternary arithmetic gates.**" Sec. III C: with carry-lookahead, non-Clifford depths are $4\log_2 n$ vs $4\log_2 m$ — "there is no substantial difference in non-Clifford depths" — while "the purely ternary solution has roughly $m/n\approx\log_3(2)$ smaller width." Table V confirms: ternary width $4m-\omega_1(m)$ vs binary $4n-\omega_1(n)$. The one exception is inline-metaplectic MTQC compilation, where "the use of emulated binary encoding is practically better," because metaplectic circuits are reflection-oriented and best suited to two-level reflections (Toffoli), whereas $C_f(\mathrm{INC})$/Horner gates must first be decomposed.
- **Other notable results:** qutrit-based computers are argued space-optimal among qudits, $d_{ee}=3$ (citing ref. [22]). MTQC needs magic-state preparation width linear in $\log(n)$ vs $O(\log^3 n)$ for a generic ternary computer; MTQC factors an $n$-bit number with $n+7$ logical qutrits at a $O(\log)$ depth cost. Emulated CNOT on binary data costs 2 $C_2(\mathrm{INC})$; emulated Toffoli 12 $P_9$; binary-controlled Toffoli 18 $P_9$.

**Judge verification questions:**
- Main.tex calls this reference an instance of treating noise via "analytic coherent-error bounds." Is Appendix B (Props. 16–18, $\|U-V\|\le d\delta$, threshold $\varepsilon\in O(1/\sqrt{\log\log N})$) purely a *coherent/unitary* approximation-error analysis with no incoherent channel? (It is.) Does main.tex avoid implying Bocharov et al. simulated decoherence?
- Main.tex says Bocharov et al. "show emulated-binary arithmetic **can** beat native ternary." Table III (12n/18n/24n vs 19n/>21n/>33n) and Table IV (width $n+4$, depth $48n^3$ vs $2m-\omega_1(m)$, $\approx76.35n^3$) support this for **ripple-carry / low-width** circuits. Does main.tex's hedged "can beat" adequately cover the authors' explicit reversal under carry-lookahead adders, where ternary regains a $\log_3 2$ width advantage at insignificant depth cost?
- Main.tex reads the Bocharov result as showing "encoding density alone is not a mechanism." Does the paper's own explanation — the carry ancilla inflating true-ternary width to $\approx\tfrac53 m$, "which eliminates the space savings afforded by denser ternary encoding" — support that reading? (It does, and it is arguably the strongest single sentence to cite.)
- Main.tex ties this to "its disappearance when compilation buys the compression back." Is that consistent with Bocharov et al.'s carry-lookahead reversal, or is main.tex using the reference in the opposite direction from the authors' own final recommendation (which favors ternary once depth compression is available)?

---

---

## `bourdon2007` — Sharp probability estimates for Shor's order-finding algorithm (Bourdon & Williams, 2007)

**Full citation:** P. S. Bourdon, H. T. Williams, "Sharp probability estimates for Shor's order-finding algorithm," Quantum Inf. Comput. **7**(5–6), 522–550 (2007); doi:10.26421/QIC7.5-6-7; arXiv:quant-ph/0607148.
**Source:** arXiv:quant-ph/0607148v3 (4 Sep 2006), QIC 7(5–6), 522–550, PDF: `bourdon-2006-sharp-probability-estimates-shor.pdf`

**Cited in main.tex:**
- *Why the decoder gains tolerance with size*: "the sharp divisor-recovery bounds of Gerjuoy and of Bourdon and Williams," within the group of analyses of "continued-fraction post-processing on base-2 registers" that "score outcomes inside a tolerance window of the peaks via the convergent guarantee — a sufficient condition — and typically certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$."

**What the paper actually shows (full-text, not abstract-level):**
- **Base-2 register of exactly Shor's original size.** Input register has $n$ qubits with $N^2\le 2^n<2N^2$; output register $n_0$ qubits with $N\le 2^{n_0}$ (so $n=2n_0$ or $2n_0-1$). Everything is qubits and powers of 2. The generalization $QC(q)$ adds $q$ more **qubits**.
- **Exact probability formula (Eq. 12):** $p(y_s)=\dfrac{1}{2^n m}\cdot\dfrac{\sin^2(\pi m r\delta_s/2^n)}{\sin^2(\pi r\delta_s/2^n)}$ with $\delta_s=y_s-s2^n/r$, $y_s=\mathrm{nint}(s2^n/r)$, $m=\lceil 2^n/r - x_0/r\rceil$; $P=\sum_{s=1}^{r-1}p(y_s)$.
- **The tolerance window is explicit and narrow.** $S=\{\mathrm{nint}(s2^n/r): s=1,\dots,r-1\}$, i.e. $|y-s2^n/r|\le 1/2$. In Sec. 5 (following Gerjuoy) the wider $\tilde S=\{y: |y-s2^n/r|\le 2\}$ is used. **Only $r-1$ outcomes are scored; the higher-denominator convergents main.tex says "window bounds do not count" are indeed uncounted here.**
- **Sufficient-condition structure exactly as main.tex describes.** They invoke the classical convergent theorem: if $|y/2^n - s/r|\le 1/(2r^2)$ then the continued-fraction expansion of $y/2^n$ yields $\tilde s/\tilde r$ in lowest terms equal to $s/r$; "hence $r=\tfrac{s}{\tilde s}\tilde r$ and $\tilde r$ is a divisor of $r$." From $y\in S$: $|y/2^n-s/r|\le \tfrac{1}{2\cdot 2^n}\le \tfrac{1}{2N^2}<\tfrac{1}{2r^2}$.
- **Divisor, not $r$ itself — stated outright.** "If $s$ happens to be relatively prime to $r$, then the order $r$ is determined." And: "**The probability of finding $r$ itself, as the least common-multiple of divisors found, rises quickly to 1 with the number of different divisors known.**" This is precisely main.tex's "certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$."
- **Numerical results.** (i) With Shor's original register size: $P>0.70$ whenever $N\ge 2^{11}$ (more precisely $N\cdot 2^{11}\le 2^n$) and $r\ge 40$; crude asymptotic $1-\pi^2/36\approx 0.726$; sharp asymptotic lower bound $\tfrac{2}{\pi^2}(-2+\pi\,\mathrm{Si}(\pi))\approx \mathbf{0.7737}$ (abstract says .7736). $F$ exceeds 0.75 at $N=2^{11}, r'=75, \tilde k=0$; the 0.77 threshold at e.g. $N=2^{15}, r'=447$. (ii) $N$ not a power of a prime (Gerjuoy's lemma $r<N/2$, window $\tilde S$): asymptotic lower bound $2\,\mathrm{Si}(4\pi)/\pi\approx \mathbf{0.9499}$; exceeds 0.90 at $N=2^{16}, r'=59, \tilde k=0$. (iii) With $q$ extra qubits: asymptotic lower bound $2\,\mathrm{Si}(2^{q+2}\pi)/\pi$; at $q=3$ this "exceeds 0.993," and explicit conditions give >99% at $N=2^{20}, r'=819, \tilde k=0$. They note phase-estimation analysis (Nielsen–Chuang) reaches 99% at $q=5$ ($N$ not a prime power) or $q=7$ (arbitrary $N$).
- **Baseline they are improving on:** "Lower bounds for this probability… are typically given at around 40 percent along with $4/\pi^2$ as an asymptotic lower bound."
- **No noise anywhere.** The analysis is of the ideal noiseless circuit; the only "error" is the finite-register broadening $\delta_s$. No qudits, no $d>2$.
- **Structural point relevant to main.tex's contrast:** their success criterion is *recovering a divisor of $r$*, and the probability is over the $r-1$ nearest-integer peaks only. There is no accounting of outcomes outside the window whose continued fraction happens to return $r$ via a larger admissible denominator.

**Judge verification questions:**
- Main.tex calls these "sharp divisor-recovery bounds." Bourdon & Williams' title is "Sharp probability estimates," their asymptotic bounds are $0.7737$ (general) and $0.9499$ ($N$ not a prime power), and their success event is "obtaining a (nontrivial) divisor of $r$." Is main.tex's label accurate?
- Main.tex says these analyses "score outcomes inside a tolerance window of the peaks." Bourdon & Williams score exactly $y\in S$ with $|y-s2^n/r|\le 1/2$ (Sec. 4) or $\tilde S$ with $\le 2$ (Sec. 5). Confirmed?
- Main.tex says they "typically certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$." Bourdon & Williams state "$\tilde r$ is a divisor of $r$" and that $r$ is recovered "as the least common-multiple of divisors found," which "rises quickly to 1 with the number of different divisors known." Is main.tex's characterization an accurate paraphrase, including the multi-run lifting?
- Main.tex contrasts its own law as counting "the admissible denominators $2r,\dots,\lfloor N/r\rfloor r$ that window bounds do not count." Does Bourdon & Williams' $P=\sum_{s=1}^{r-1}p(y_s)$ in fact omit all outcomes outside the $r-1$ nearest-integer peaks? (It does — verify no other outcomes are summed.)
- Main.tex says the literature it is contrasting with is on **base-2 registers**. Does Bourdon & Williams' setup ($N^2\le2^n<2N^2$ qubits, $QC(q)$ with $q$ extra qubits) confirm this exclusively? (It does — no qudit or base-$d$ generalization appears anywhere.)

---

## `campbell2012` — Magic-state distillation in all prime dimensions using quantum Reed–Muller codes (Campbell, Anwar & Browne, 2012)

**Full citation:** E. T. Campbell, H. Anwar and D. E. Browne, "Magic-state distillation in all prime dimensions using quantum Reed–Muller codes," *Phys. Rev. X* **2**, 041021 (2012); arXiv:1205.3104.
**Source:** arXiv:1205.3104v2 [quant-ph], Phys. Rev. X 2, 041021, PDF: `campbell-2012-magic-state-distillation-prime-dims.pdf` (18 pp., read in full text form)

**Cited in main.tex:**
- *Introduction* (l. 86–87): "magic-state distillation protocols exist in every prime dimension~\cite{campbell2012}" — an existence claim across all prime $d$, used as part of the structural case for qudits. (Note the *rate of improvement with $d$* in the same sentence is attributed to `campbell2014`, not to this reference.)
- *Robustness* (l. 2247–2249): "the prime restriction elsewhere in this paper is inherited from the fault-tolerance and QFT-arithmetic motivations~\cite{gottesman1999,campbell2012,floratos2024}" — i.e. this reference is offered as a fault-tolerance reason why $d$ must be prime.

**What the paper actually shows (full-text, not abstract-level):**
- Scope statement, Sec. I: "We are interested in $d$-dimensional quantum systems, or qudits, where $d$ is an **odd prime**... $\mathbb{F}_d$ denotes the finite field of $d$ elements." The whole construction (Reed–Muller polynomial codes over $\mathbb{F}_d$, invertibility of multiplication, $\lambda$-functions) requires $d$ prime so that $\mathbb{F}_d$ is a field. This is exactly the "fault-tolerance motivation for prime $d$" the Robustness section invokes.
- Theorem 2 (p. 4): for **any odd prime $d$** and any $m\ge 2$ (or $d\ge5$ and $m\ge1$) there exists a stabilizer operation that iteratively distils $|M_0\rangle$, with $\epsilon' \le K\epsilon^2$ and hence a nonzero threshold $\epsilon^*>0$. Theorem 4: $\mathcal{QRM}_d(m)$ codes are $\mathcal{M}^m_d$-distillation codes of **distance $D=2$** for all odd prime $d$, all $m$.
- Coverage of $d=2$: the title says "all prime dimensions," and the authors state (p. 10, after Eq. 65) that "Our analysis also describes the Bravyi–Kitaev protocol, the only difference being that in the qubit case we need $m\ge4$, and so the above formula also holds for qubits." The qubit code $\mathcal{QRM}_2(4)$ (15 qubits) appears in Tables I and II. So "exist in every prime dimension" is defensible: the *new* protocols are for odd prime $d$; $d=2$ is the pre-existing Bravyi–Kitaev case subsumed by the same analysis.
- **Performance does NOT improve monotonically with $d$ in this paper** — the opposite. Table II ($\epsilon^*_{\rm dep}$, depolarizing threshold): $d=2$ ($m=4$) 0.14148; $d=3$ ($m=2$) 0.211001; $d=5$ ($m=1$) 0.3631226; $d=7$ 0.2322599; $d=11$ 0.1341066; $d=13$ 0.1106148; $d=17$ 0.0818753; $d=19$ 0.072453. The authors write: "The threshold gets weaker for both increasing $d$ and increasing $m$." Yield parameter $\gamma^*=\log_2(d^m-1)$ (Table I) likewise grows (worsens) with $d$: 2 at $d=5,m=1$; 2.58 at $d=7$; 3.32 at $d=11$; 4.17 at $d=19$. This is the exact "performance declines for $d>5$" that Campbell 2014 later reverses — so main.tex is correct to attribute the "keeps improving with $d$" clause to `campbell2014` and only the existence claim to `campbell2012`.
- Headline numbers of this paper: $\mathcal{QRM}_5(1)$ (4 ququints, $n=d^m-1=4$) has $\epsilon^*_{\rm dep}=0.363122$ and $\epsilon^*=0.31195$ for general noise; $\mathcal{QRM}_3(2)$ (8 qutrits) has $\epsilon^*_{\rm dep}=0.211001$, $\epsilon^*=0.20015$, $K=5.03$. Error suppression is **quadratic** ($\epsilon'\approx \frac{(d^m-1)(d-2)}{2(d-1)}\epsilon^2$), weaker than the cubic suppression of the 15-qubit Bravyi–Kitaev code, but with better thresholds and yields for $d=3,5$.
- Caveat the authors themselves state: gains are attributed to $d=5$ being the smallest dimension admitting a period-$d$ diagonal non-Clifford gate ($m=1$), i.e. a *small-code* effect, not a monotone dimension effect: "research to date indicates that smaller codes lend themselves to better thresholds."

**Judge verification questions:**
1. Does main.tex attribute *only* existence-across-primes to `campbell2012`, and the "thresholds and efficiencies keep improving with $d$" claim exclusively to `campbell2014`? (If the improvement claim were read as also resting on `campbell2012`, it would directly contradict this paper's Table II, where thresholds fall monotonically for $d\ge7$.)
2. Is "every prime dimension" acceptable given that the paper's own new protocols are stated for **odd** prime $d$, with $d=2$ covered only as the pre-existing Bravyi–Kitaev case subsumed by the same formulae?
3. Does the paper actually support "prime restriction inherited from fault-tolerance motivations"? (Yes — the code construction is over the finite field $\mathbb{F}_d$, which requires prime $d$; check main.tex is not claiming anything stronger, e.g. that primality is *necessary* for distillation in general.)

---

---

## `campbell2014` — Enhanced fault-tolerant quantum computing in $d$-level systems (Campbell, 2014)

**Full citation:** E. T. Campbell, "Enhanced fault-tolerant quantum computing in $d$-level systems," *Phys. Rev. Lett.* **113**, 230501 (2014); arXiv:1406.3055.
**Source:** arXiv:1406.3055v2 [quant-ph] (9 Oct 2015), PRL 113, 230501, PDF: `campbell-2014-enhanced-ft-d-level-systems.pdf` (6 pp., read in full)

**Cited in main.tex:**
- *Introduction* (l. 87–89): magic-state distillation "with thresholds and efficiencies that keep improving with $d$ **(within congruence classes mod 3, for primes up to 17)**~\cite{campbell2014}".
- *Introduction* (l. 97–99): direct quotation — Campbell noted that "in physical systems one may also see noise rise with $d$. Such features depend subtly on the details of the underlying physics".

**What the paper actually shows (full-text, not abstract-level):**
- Abstract and conclusion: "Unlike prior work, we find performance is always enhanced by increasing $d$." Codes use $n=d-1$ qudits, detect up to $\sim d/3$ errors, best codes have distance $D=\lfloor(d+1)/3\rfloor$; efficiency $\gamma=\log_D(d-1)$ (i.e. $\log(n)/\log(D)$) decreases toward 1 as $d\to\infty$.
- **The mod-3 congruence-class qualifier is verbatim in the paper** (p. 4): "For prime $d\le 17$, we have numerically found $\epsilon^*$ shown in Fig. (1c), and observed increasing improvements with $d$. There is a **monotonic improvement in both threshold and $\gamma$ within the two classes of odd numbers, $d=1\ (\mathrm{mod}\ 3)$ versus $d=2\ (\mathrm{mod}\ 3)$**. Jumps occur because the code distance only increases when $d$ increases by 3 or more." So both main.tex qualifiers ("within congruence classes mod 3", "for primes up to 17") match the paper exactly — the $\epsilon^*$ numerics are stated for prime $d\le17$; the $\gamma$ efficiency plot (Fig. 1a) extends further, to $d=19,23$, and Fig. 1b to $d\sim10^9$ on a log scale.
- Threshold comparisons: "we exceed $\epsilon^*_{\rm dep}=0.5$ even with $d=11$ while toric codes only approach 0.5 in the large-$d$ limit"; "Compared to qudit toric code thresholds, these distillation thresholds are consistently higher." Qubit comparison: 15-qubit code $\gamma=2.465$; qubit block codes reach $\gamma\to1.585$ (Bravyi–Haah limit); multi-level distillation numerically $\gamma\to1$ but with heavy caveats.
- **Scope limits the citing paper does not repeat:** (i) "For technical reasons, we consider only **prime dimensions of five and above**" (p. 2) — $d=3$ is excluded from the improved construction, because $3\mu \equiv 0 \pmod 3$ kills the non-Cliffordness argument (App. A). (ii) The efficiency gain is asymptotic and slow: "Though very large $d$ is needed for our protocols to get $\gamma$ close to unity (see Fig. 1), modest $d$ is sufficient to outperform qubit protocols." (iii) $\epsilon^*$ is a *depolarizing-noise* threshold, defined by mixing $M_\mu|+\rangle$ with the identity.
- **Quote verification (Conclusions, p. 4, verbatim):** "We must remark that coherent control of high $d$ qudits is challenging, and **in physical systems one may also see noise rise with $d$. Such features depend subtly on the details of the underlying physics.**" The main.tex quotation is word-for-word correct, and the surrounding context supports main.tex's framing (a flagged-but-unanswered question). The very next sentences, which main.tex omits, are more optimistic: "Whilst many systems may not be well suited to qudit approaches, many atomic systems come equipped with large Hilbert spaces for which control of many levels need not be substantially more difficult than control of just 2 levels. For instance, experiments in trapped cesium have performed gates between 16 levels at 99% fidelity [49]."

**Judge verification questions:**
1. Is the direct quotation in main.tex (l. 97–99) verbatim and in-context, and does omitting the following two sentences (trapped-cesium 16-level gates at 99% fidelity, "many atomic systems... need not be substantially more difficult") change the impression of Campbell's stance in a way that matters for the citing paper's thesis?
2. Are the qualifiers "within congruence classes mod 3" and "for primes up to 17" faithful to p. 4 of the paper? (Both appear verbatim; check whether "primes up to 17" is correctly attached to the *threshold* numerics rather than to the $\gamma$ efficiency data, which Fig. 1a extends to $d=23$.)
3. Does main.tex anywhere imply the improvement holds for $d=3$? The paper explicitly restricts its improved codes to prime $d\ge5$ (and App. A explains why $d=3$ fails), so a blanket "keeps improving with $d$" including $d=3$ would overstate it.
4. Is "thresholds **and efficiencies**" accurate? (Yes: the paper claims monotone improvement in both $\epsilon^*$ and $\gamma$ within each mod-3 class, and specifically flags the efficiency gain as the more surprising result absent in toric codes.)

---

---

## `chappell2011` — A precise error bound for quantum phase estimation (Chappell, Lohe, von Smekal, Iqbal & Abbott, 2011)

**Full citation:** J. M. Chappell, M. A. Lohe, L. von Smekal, A. Iqbal and D. Abbott, "A precise error bound for quantum phase estimation," *PLoS ONE* **6**(5), e19663 (2011); arXiv:1102.0108.
**Source:** arXiv:1102.0108v2 [quant-ph], PLoS ONE 6(5):e19663, PDF: `chappell-2011-precise-error-bound-qpe.pdf` (6 pp., read in full)

**Cited in main.tex:**
- *subsection "Why the decoder gains tolerance with size"* (l. 1524–1528): listed at the end of a survey of order-finding success-probability analyses — "and, for eigenstate phase estimation, Chappell \emph{et al.}~\cite{chappell2011}. **These analyses** score outcomes inside a tolerance window of the peaks via the convergent guarantee---a sufficient condition---and typically certify recovery of a divisor $r/\gcd(s,r)$ that a classical search then lifts to $r$."

**What the paper actually shows (full-text, not abstract-level):**
- Setting: **pure eigenstate** phase estimation. Given $U|u\rangle = e^{2\pi i\phi}|u\rangle$, estimate $\phi\in[0,1)$ with a $t$-qubit measurement register, $t=s+p$ ($s$ = desired bits of accuracy, $p$ = extra qubits). The main.tex qualifier "for eigenstate phase estimation" is exactly right — there is **no** order $r$, no periodic $r$-peak structure, and no Shor/order-finding content in this paper beyond a one-line mention of Shor's algorithm in the Introduction.
- **No continued fractions anywhere.** The paper contains no continued-fraction expansion, no "convergent guarantee," no divisor $r/\gcd(s,r)$, and no classical lifting step. Its post-processing is simply: read the register, accept if the outcome $m$ is within tolerance of $\phi$.
- The tolerance-window part *does* match: they define success as $|2\pi m/2^t - \phi| \le \tfrac12\cdot 2\pi/2^s$ (Eq. 12), i.e. a symmetric window about the true $\phi$, and sum $|x_{b+\ell}|^2$ over the window (Eqs. 7, 13). So Chappell et al. genuinely are a "score outcomes inside a tolerance window of the peaks" analysis — but of a **single** peak at $\phi$, not $r$ peaks at $s/r$.
- Concrete results: Eq. (20), the exact worst-case failure probability $\epsilon(s,p) = 1 - \frac{1}{2^{2(p+s)-2}}\sum_{\ell=1}^{2^{p-1}} \left[1-\cos\frac{\pi(2\ell-1)}{2^{(p+s)}}\right]^{-1}$; Eq. (22) the $t\to\infty$ trigamma form $\epsilon \le \frac{2}{\pi^2}\psi'\!\left(\frac{1+2^p}{2}\right)$; Eq. (23) the large-$p$ asymptote $\epsilon = \frac{4}{\pi^2}2^{-p}$; Eq. (24) $p_\infty = \lceil\log_2(2\sqrt2/(\pi^2\epsilon))\rceil$.
- Their improvement over prior work is a *symmetrization* of the error definition (dropping the outermost lower state, so the sum runs $\ell=-2^{p-1}+1$ to $2^{p-1}$), plus avoiding the $\cos x \ge 1-x^2/2$ approximation. They prove the bound is attained at $a=2^t\delta=1/2$ (midway between states) by a Taylor argument showing $c_1=0$.
- Verification: "We have checked the new error formula through simulations, by running the phase estimation algorithm on a **2-dimensional rotation matrix**, and undertaking a numerical search for the rotation angle that maximizes the error $\epsilon$, which has confirmed Eq. (20) to six decimal places." Also a footnote correcting Nielsen & Chuang (2^p−1 vs 2^{p−1} preceding Eq. 5.35).
- Explicit purpose stated by the authors: the exact formula "avoids overestimating the number of qubits actually required" relative to the Cleve et al. bound $p_C = \lceil\log_2(1/(2\epsilon)+1/2)\rceil$, and is "useful in confirming the operation of classical simulators of the phase estimation procedure."

**Judge verification questions:**
1. Does the sentence "**These analyses** score outcomes inside a tolerance window of the peaks **via the convergent guarantee** ... and typically certify recovery of a divisor $r/\gcd(s,r)$" grammatically sweep Chappell et al. into a group characterized by continued-fraction convergents and divisor recovery — neither of which appears anywhere in Chappell et al.? Does the hedge "typically" plus the "for eigenstate phase estimation" apposition sufficiently exempt it?
2. Is the "tolerance window" half of the characterization accurate for Chappell? (Yes — Eqs. 7/12/13 sum probability over a window; but the window is around a single phase $\phi$, not around $r$ peaks $s/r$.)
3. Is Chappell et al. correctly grouped as a *base-2 register* analysis ("An exact literature bounds the success of continued-fraction post-processing on base-2 registers")? Chappell is base-2 but has no continued-fraction post-processing — check whether the umbrella clause misdescribes it.
4. Does main.tex make any numerical claim traceable to this paper (e.g. $4/\pi^2$)? Note Chappell's asymptote is $\epsilon = (4/\pi^2)2^{-p}$ — a *failure*-probability asymptote for phase estimation, numerically coincident-looking with Shor's $4/\pi^2$ *success* constant but conceptually unrelated; check main.tex does not conflate them.

---

---

## `chiesa2024` — Quantum information processing with molecular nanomagnets: an introduction (Chiesa, Macaluso & Carretta, 2024)

**Full citation:** A. Chiesa, E. Macaluso and S. Carretta, "Quantum information processing with molecular nanomagnets: an introduction," *Contemp. Phys.* (2024), doi:10.1080/00107514.2024.2381952; arXiv:2405.21000.
**Source:** arXiv:2405.21000v2 [quant-ph] (22 Aug 2024), Contemp. Phys., PDF: `chiesa-2024-molecular-nanomagnets-intro.pdf` (27 pp., read in full text form)

**Cited in main.tex:**
- *Introduction* (l. 70–75): one of seven platform citations for "Transmons, trapped ions, nitrogen-vacancy centers, **molecular spins**, and Rydberg-blockaded atom arrays all expose more than two usable levels, and processors that exploit them as qudits **now exist or are proposed** on several platforms." I.e. `chiesa2024` is the molecular-spin entry, supporting multi-level availability + qudit processors existing or proposed.

**What the paper actually shows (full-text, not abstract-level):**
- It is a **pedagogical review / "introduction"** in *Contemporary Physics*, not a device demonstration. This matters for how much weight "processors ... now exist" can carry from this citation alone; the citing sentence's "or are proposed" hedge is doing the work here.
- Multi-level availability is directly and repeatedly supported: MNMs "naturally provide two or more discrete energy levels"; "their spin Hamiltonian naturally provides many (more than two) low-energy levels which can be manipulated coherently by electromagnetic pulses"; Sec. VII: "MNMs are natural multi-level spin systems to encode qudits."
- Concrete qudit hardware described: nuclear spin qudits with $I\ge3/2$ hyperfine-coupled to an electronic doublet (Eq. 36, $H_{mnq}=I\cdot A\cdot s + pI_z^2 + \mu_B s\cdot g\cdot B$); a 6-level qudit ($^{173}$Yb(trensal), $I=5/2$) coupled to an $s=1/2$ electronic ancilla for an amplitude-shift QEC code (Fig. 7a); a 4-level $S=3/2$ qudit code against pure dephasing; multi-spin clusters (Cr$_7$Ni ring, Ni$_7$-like 7-ion cluster).
- **Experimental qudit algorithm actually run:** Grover's search implemented on a nuclear spin qudit in a TbPc$_2$ single-molecule transistor (Godfrin et al., PRL 119, 187702 (2017)), via a three-frequency pulse creating an equal-weight superposition of three nuclear states and then amplifying the searched state (Fig. 9). Also cited: two-qubit gate demonstration, first proof-of-concept quantum simulator, single-molecule transistor readout.
- Coherence numbers: Cr$_7$Ni $T_2 \sim 1$–10 µs, improved by structural simplification; single-ion Cu$^{2+}$/V complexes reach $T_2$ up to 70 µs and "even close to ms," in some cases at room temperature. $T_1$ upper-bounds $T_2$ by $2T_1$; at low $T$, pure dephasing from the ligand nuclear-spin bath dominates.
- **Directly relevant tension with the citing paper's central premise** (Sec. VII, p. 22): "We stress that, **at difference from other quantum systems which are also characterised by several energy levels, in MNMs coherence is in general not suppressed by increasing the number of states embedded in the qudit** [83]." Sec. IV.B gives the mechanism: with competing (rather than ferromagnetic) exchange, the variation of $\langle\mu|s_{zj}|\mu\rangle$ across eigenstates is small, so "a superposition of all the qudit states is much more protected from decoherence if the hierarchy of interactions in the molecule is chosen properly." This is a cited-author claim that on *this* platform, the citing paper's premise ("higher levels of a real device decay and dephase faster than lower ones") need not hold.
- Authors' own stated challenges: MNMs "have still been little explored at the experimental level"; "the most important challenge to win is represented by reading out the state of a single molecular spin"; scaling is hoped for via strong spin–photon coupling in superconducting resonators.

**Judge verification questions:**
1. Does main.tex's sentence claim more for molecular spins than a review supports? (The claim is only "expose more than two usable levels" and "processors ... now exist **or are proposed**" — check whether the disjunction is present and whether main.tex elsewhere upgrades molecular spins to an existing processor.)
2. Chiesa et al. explicitly assert that in MNMs coherence is *not* generally suppressed by increasing the number of qudit levels. Does main.tex anywhere cite `chiesa2024` in support of the opposite (level-dependent decay), or otherwise imply the cited authors endorse its noise premise? (In the given contexts it does not — but a judge should confirm no other use, and consider whether the paper's scope statement should acknowledge this platform as a stated exception.)
3. Is "molecular spins" an accurate one-word rendering of "molecular nanomagnets / molecular spin qudits" as used in the source?

---

---

## `dalibard1992` — Wave-function approach to dissipative processes in quantum optics (Dalibard, Castin & Mølmer, 1992)

**Full citation:** J. Dalibard, Y. Castin and K. Mølmer, "Wave-function approach to dissipative processes in quantum optics," *Phys. Rev. Lett.* **68**, 580 (1992).
**Source:** Phys. Rev. Lett. 68, 580 (1992); doi:10.1103/PhysRevLett.68.580. PDF: **not available** — no full text in `papers/`, and this is a pre-arXiv 1992 PRL. **The bullets below rest on bibliographic and domain knowledge of this well-known paper, not on a full-text read of this specific PDF, and should be treated as lower-confidence than the other five entries in this batch.** Specific equation numbers and the paper's illustrative physical example were NOT verified.

**Cited in main.tex:**
- *Methods* (l. 2675–2683): "beyond that, Monte Carlo wavefunction trajectories~\cite{dalibard1992,molmer1993}: after each gate, each carrier independently passes through the per-layer channel raised to the gate's cost, sampled via one Kraus operator drawn with probability $\mathrm{tr}(K^\dagger K\rho_q)$ from the carrier's reduced state. Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly." Used as the *methodological provenance* for the stochastic-wavefunction simulator that replaces exact density-matrix evolution above Hilbert dimension ~3000.

**What the paper actually shows (to the best of domain knowledge; unverified against the PDF):**
- It introduces the Monte Carlo wave-function (MCWF) / quantum-jump method: instead of integrating the master equation for $\rho$ ($N^2$ complex entries), one propagates single wavefunctions ($N$ amplitudes) and averages, which is the exact motivation main.tex gives for switching methods above a Hilbert-dimension threshold.
- The algorithm as originally posed is **continuous-time**: over a small step $\delta t$, evolve with a non-Hermitian effective Hamiltonian $H_{\rm eff} = H - \tfrac{i\hbar}{2}\sum_m C_m^\dagger C_m$; compute the total jump probability $\delta p = \delta t\sum_m \langle\psi|C_m^\dagger C_m|\psi\rangle$; with probability $1-\delta p$ keep the renormalized non-Hermitian evolution, otherwise apply a jump $|\psi\rangle \to C_m|\psi\rangle/\||C_m|\psi\rangle\|$ with $m$ chosen with probability $\delta p_m/\delta p$.
- The central theorem is the equivalence claim: the ensemble average $\overline{|\psi\rangle\langle\psi|}$ over trajectories reproduces the master-equation density matrix (to first order in $\delta t$). This is the statement main.tex leans on ("Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly").
- **Scope mismatch worth flagging:** the 1992 PRL formulates the unravelling for a **Lindblad master equation in continuous time** with jump operators $C_m$, applied to a quantum-optics dissipation problem. main.tex uses a **discrete-time, per-gate Kraus-operator sampling** of a CPTP channel ($K$ drawn with probability $\mathrm{tr}(K^\dagger K\rho_q)$), applied per carrier per layer. The discrete Kraus unravelling is the standard generalization and the "average reproduces the channel" identity is exact and elementary in the discrete case (it does not even need the $O(\delta t)$ argument), but it is a *generalization* of, not literally the content of, Dalibard–Castin–Mølmer. Citing DCM (+ Mølmer–Castin–Dalibard 1993) as the provenance of "Monte Carlo wavefunction trajectories" is standard practice in the literature.
- The companion reference `molmer1993` (K. Mølmer, Y. Castin, J. Dalibard, JOSA B 10, 524 (1993)) is the long-form treatment and is the one that contains the detailed statistical-error analysis ($\propto 1/\sqrt{N_{\rm traj}}$) and the discussion of when MCWF beats density-matrix integration. main.tex's variance claims (variance ratio 7.7–26.6 vs Bernoulli; $0.51\sigma$ agreement with an exact density matrix at $d=3$, $m=4$) are presented as *its own* measurements, not attributed to either reference — check this holds.

**Judge verification questions:**
1. Does main.tex attribute to `dalibard1992` anything beyond "the Monte Carlo wavefunction trajectory method"? Specifically, does it claim the *discrete per-gate Kraus-sampling* scheme (with $K$ drawn at probability $\mathrm{tr}(K^\dagger K\rho_q)$) comes from this reference, or only the general trajectory idea?
2. Is "Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly" a fair statement? (In the discrete Kraus setting it is exact; in DCM's original continuous-time setting the equivalence is to first order in the time step $\delta t$. Check whether main.tex's word "exactly" is claimed for its own discrete scheme — which is correct — or is being attributed to the cited paper.)
3. Are the quantitative simulator-quality numbers in Methods (variance ratios, $0.51\sigma$ unbiasedness check) presented as this paper's own measurements rather than as results from `dalibard1992` / `molmer1993`?
4. **Sourcing flag for the judge:** no full text of `dalibard1992` was available in the repository; if the verification hinges on a fine point of the original algorithm, obtain the PRL.

---

---

## `ekera2024` — On the success probability of quantum order finding (Ekerå, 2024)

**Full citation:** M. Ekerå, "On the success probability of quantum order finding," *ACM Trans. Quantum Comput.* **5**(2), art. 11 (2024); doi:10.1145/3655026; arXiv:2201.07791.
**Source:** arXiv:2201.07791v2 [quant-ph] (28 Nov 2022) — note the local PDF is the **arXiv preprint version**, filename `ekera-2022-success-probability-order-finding.pdf` (42 pp., read in full text form); the bib entry cites the 2024 ACM TQC published version.

**Cited in main.tex:**
- *subsection "Why the decoder gains tolerance with size"* (l. 1520–1521): "Eker{\aa}'s proof that a single run recovers $r$ with probability approaching one~\cite{ekera2024}", listed among exact analyses of continued-fraction post-processing on base-2 registers.
- *The decoder acceptance lemma* (l. 2843–2846): "for $y$ within $1/(2\tilde r^2)$ of a peak $s/r$, the convergent guarantee~\cite{hardy2008} yields the reduced fraction $(s/g)/(r/g)$ with $g=\gcd(s,r)$, whose denominator $\tilde r = r/g$ **divides** $r$~\cite{shor1997,ekera2024}."
- *The decoder acceptance lemma* (l. 2847–2849): "those analyses lift $\tilde r$ to $r$ by classical search over multiples (**or over gcd-smoothness classes**~\cite{ekera2024})."

**What the paper actually shows (full-text, not abstract-level):**
- Main result, **Thm. 3** (p. ~19): the quantum algorithm plus continued-fraction- or lattice-based post-processing recovers $r$ in a single run with probability at least
 $\left[\left(1-\frac{1}{\pi^2}\left(\frac{2}{B}+\frac{1}{B^2}+\frac{1}{3B^3}\right)\right) - \frac{\pi^2 r(2B+1)}{2^{m+\ell}}\right]\left(1-\frac{1}{c\log cm}\right)$, for $2^m>r$, $2^{m+\ell}>r^2$, $c\ge1$, $B\in[1,B_{\max})\cap\mathbb{Z}$.
- **Cor. 3.2:** "In the limit as $r$ tends to infinity, the probability of the quantum algorithm in combination with the classical post-processing succeeding in recovering $r$ **in a single run tends to one**. All algorithms involved may be parameterized so as to achieve this limit whilst executing in polynomial time." Proof takes $c=1$, $B=m$, $m=O(\mathrm{poly}(\log r))$. This is exactly main.tex's "single run recovers $r$ with probability approaching one" — **accurate**, with the standing conditions that (i) the two limited classical searches are performed, (ii) $m$ with $2^m>r$ is known, (iii) group arithmetic is efficient.
- **Non-asymptotic numbers** (Tab. 1, $m=\ell=128$, bound tabulated in $B$ and $c$): 0.85714 (weakest tabulated corner) up to 0.99993; abstract and conclusion state "Already for moderate $r$, a high success probability exceeding e.g. $1-10^{-4}$ can be guaranteed." Authors stress it is a worst-case bound: "In practice, the success probability is usually higher than the bound indicates, as our bound stems from a worst case analysis that holds for any $r$ given only an upper bound $m$ on the bit length of $r$."
- **The two searches** (Sect. 1.6.1): (a) a search over frequency offsets — solve not only the observed $j$ but $j\pm1,\dots,j\pm B$ for $z/r$, so that $j_0(z)$ is hit with the Thm. 2 probability, with $z$ uniform on $[0,r)$; (b) a search to lift $\tilde r$ to $r$. Alternatively lattice-based post-processing with $\ell=m-\Delta$ and enumeration of at most $6\sqrt3\cdot2^\Delta$ lattice vectors (Lem. 8, Cor. 3.1).
- **Divisor structure — supports main.tex l. 2843–2846:** Sect. 4: picking $\ell$ with $2^{m+\ell}>r^2$ and expanding $j_0(z)/2^{m+\ell}$ as a continued fraction yields $z/r$, "and hence $\tilde r = r/d$ where $d=\gcd(r,z)$." So the denominator recovered is $r/\gcd(r,z)$, a **divisor** of $r$ — matching main.tex's $\tilde r = r/g$, $g=\gcd(s,r)$ (main.tex writes the peak index as $s$, Ekerå writes it as $z$).
- **gcd-smoothness — supports main.tex l. 2847–2849, precisely:** Sect. 4.1.1 defines an integer to be **$cm$-smooth** iff it is positive and not divisible by any prime power greater than $cm$. **Lem. 9:** for $z$ uniform on $[0,r)$, $\Pr[d=\gcd(r,z)\ \text{is}\ cm\text{-smooth}] \ge 1 - \frac{1}{c\log cm}$ (proof: at most $\log r/\log cm$ prime powers $q^e>cm$ divide $r$, each divides $z$ with probability $1/q^e<1/(cm)$; union bound). Alg. 1 recovers a positive integer **multiple** $r'$ of $r$ from $\tilde r$; Alg. 2 and Alg. 3 recover $r$ itself from $\tilde r$ when $d$ is $cm$-smooth; Alg. 4 filters candidates for $\tilde r$. So main.tex's parenthetical "(or over gcd-smoothness classes~\cite{ekera2024})" is a correct and specific description: the lift is not a naive search over all multiples but exploits that $\gcd(r,z)$ is $cm$-smooth with high probability.
- Shor attribution context (Sect. 1.4): Ekerå records that Shor lower-bounds $\Pr[\text{observe }j_0(z)]$ by $4/(r\pi^2)$ hence $4/\pi^2$ over all $z$ [35, p. 1500], that at least a fraction $\varphi(r)/r = \Omega(1/\log\log r)$ of $z$ are coprime to $r$, and that Odlyzko (credited by Shor, p. 1501) suggested recovering $r/d$ then searching over $d$ — "This improves the expected number of runs from $O(\log\log r)$ without searching to $O(1)$ provided one exhausts on the order of $(\log r)^{1+\epsilon}$ values of $d$." So main.tex's phrase "those analyses lift $\tilde r$ to $r$ by classical search over multiples" is historically correct and attributable to Shor/Odlyzko as well.
- Exponent length: this work uses $m+\ell$ bits with $2^m>r$, $2^{m+\ell}>r^2$ — "on par with or slightly shorter than the exponent in Shor's original work"; lattice post-processing can shave a few more bits. So "without re-running the quantum part or increasing the exponent length."
- Scope note: the analysis is for **base-2 registers** ($2^{m+\ell}$-dimensional control register), consistent with main.tex's framing "on base-2 registers." It is also generic order finding in any efficiently-implementable finite cyclic group, not only $\mathbb{Z}_N^*$; corollaries 3.3–3.5 extend to complete factorization of $N$ in a single run.

**Judge verification questions:**
1. Does main.tex's "single run recovers $r$ with probability approaching one" preserve the essential conditions — asymptotic in $r\to\infty$, with two limited classical searches ($B$ frequency offsets, $cm$-smooth lift) and a known bound $m$? Or does it read as an unconditional single-run guarantee?
2. Is the divisor claim exact? Ekerå obtains $\tilde r = r/\gcd(r,z)$ with peak index $z$; main.tex writes $\tilde r = r/\gcd(s,r)$ with peak index $s$. Confirm these are the same object under relabelling and that $\tilde r \mid r$ is asserted, not $\tilde r = r$.
3. Is "gcd-smoothness classes" a faithful compression of Ekerå's $cm$-smoothness of $d=\gcd(r,z)$ (Sect. 4.1.1, Lem. 9, Alg. 2–3)? Does main.tex overstate by implying the search is *over* smoothness classes rather than being *enabled by* the smoothness of $d$?
4. Is the claim that these analyses "typically certify recovery of a divisor ... that a classical search then lifts to $r$" consistent with Ekerå's Thm. 3, whose bound is on recovering $r$ **itself** (search included in the bound), not merely a divisor?
5. Bibliographic: the bib entry gives *ACM Trans. Quantum Comput.* 5(2):11 (2024), doi:10.1145/3655026, eprint 2201.07791 — the local PDF is arXiv v2 (2022). Confirm no page/theorem number cited in main.tex is version-specific.

---

## `floratos2024` — A Novel Finite Fractional Fourier Transform and its Quantum Circuit Implementation on Qudits (Floratos & Pavlidis, 2024)

**Full citation:** E. Floratos and A. Pavlidis, "A Novel Finite Fractional Fourier Transform and its Quantum Circuit Implementation on Qudits," arXiv:2409.05759 [quant-ph] (2024).
**Source:** arXiv:2409.05759, PDF: `floratos-pavlidis-2024-fractional-qft-qudits.pdf` (28 pp.)

**Cited in main.tex:**
- *Introduction*: "the quantum arithmetic fractional Fourier transform of Ref. [floratos2024] exists for odd prime $p$, where the discrete rotation group $SO_2[\mathbb{Z}_{p^n}]$ is cyclic (the in-place constant multipliers and quadratic-phase diagonals of the same construction carry over to any dimension, including $p=2$, whenever the multiplication constant is a unit)" — used as one of the structural motivations for restricting to prime dimension.
- *Gate-cost models*: "the follow-up construction of Ref. [floratos2024] retains it [the $d^2$ factor in depth] ($16p^2n$ for the in-place constant multiplier)."
- *Robustness*: listed with `gottesman1999, campbell2012` as the "QFT-arithmetic motivation" from which the paper's prime restriction is inherited (the bare-circuit dynamics itself carries no trace of primality).
- *Discussion*: "the follow-up construction of Ref. [floratos2024] gives an in-place, ancilla-free multiplier of width exactly $n$ with nearest-neighbor interactions---but for multiplication by a *constant* modulo the register size $p^n$ (unit constants only), not the mod-$N$ modular multiplication Shor's controlled-$U^{d^i}$ requires, which in general needs comparison-and-correction machinery with ancillas."

**What the paper actually shows (full-text, not abstract-level):**
- Sec. 2, Eq. (2.8)–(2.9) and the sentence following Eq. (2.10): $SO_2(\mathbb{Z}_N)=\{(a,-b;b,a): a^2+b^2=1 \bmod N\}$; for $N=p^n$ the group order is $g=p^{n-1}(p+1)$ if $p\equiv3\ (4)$ and $p^{n-1}(p-1)$ if $p\equiv1\ (4)$. **Verbatim: "They are cyclic for every prime $p\neq 2$ and $n$ and therefore they possess generator..."** So the cyclicity — and hence the existence of a generator whose $m$-th power is the $90^\circ$ Fourier element $\epsilon$ — is stated *only* for odd prime $p$. This directly supports main.tex's "exists for odd prime $p$, where … is cyclic."
- Additional nuance the authors state (p. 5, after Eq. 2.13): for $p\equiv1\ (4)$ the generator can be determined analytically; for $p\equiv3\ (4)$ **only by trial and error**. Main.tex does not use this, but it is a practicality caveat on "exists."
- Sec. 5 ("QFT-based in-place constant Multiplier on multilevel qudits"): the multiplier realizes $\mathrm{MODMULC}_\lambda|l\rangle = |\lambda l \bmod p^n\rangle$. Verbatim: **"It is an 'in-place' multiplier in the sense that it doesn't use any ancilla qudits. This multiplier by constant $\lambda$ performs the multiplication modulo $p^n$, where $n$ is the qudits number… Unitarity of the multiplier poses the restriction $\gcd(\lambda,p^n)=1$."** This is exactly main.tex's Discussion characterization: constant multiplier, modulus = register size $p^n$, unit constants only, ancilla-free, width $n$. The paper nowhere claims a mod-$N$ (arbitrary modulus) modular multiplier.
- Intro summary (p. 3–4): "In section 5 we propose an in-place (without any ancilla) modulo $p^n$ multiplier of **linear depth, quadratic quantum cost and local interactions between the qudits**." The quadratic-phase diagonal circuits are described identically ("ancilla-free, linear depth, quadratic quantum cost and local interactions like the modulo multiplier"). Conclusions: "The whole quantum fractional Fourier transform circuit uses local interactions only… suitable for 1D-LNN architectures." → supports "nearest-neighbor interactions."
- **Table 1 (p. 23), "Quantum cost, depth and width of the proposed arithmetic circuits":**
  | Circuit | Cost | Depth | Width |
  |---|---|---|---|
  | QAFrFT | $6p^2n^2$ | $16p^2n$ | $n$ |
  | mQFT | $2p^2n^2$ | $8p^2n$ | $n$ |
  | MODMULC | $4p^2n^2$ | $16p^2n$ | $n$ |
  | Diagonal | $2p^2n^2$ | $8p^2n$ | $n$ |
  So $16p^2n$ is indeed the **depth** of MODMULC (and of the full QAFrFT). Main.tex's "$16p^2n$ for the in-place constant multiplier" matches Table 1 exactly.
- Origin of the $p^2$ (Conclusions, p. 23): "The decomposition of an $R_k^p$ requires about $4p^2$ elementary gates, while $P_\mu^d$ … requires $p$ elementary gates (for $p\neq2$)." I.e. the $p^2$ factor is precisely the two-level decomposition cost of a controlled rotation — the same mechanism main.tex attributes to it in the Gate-cost-models paragraph.
- Before that decomposition, at the level of the composite gates $H^{(p)}, P_\mu^p, R_k^p$, the authors report the QAFrFT costs only $4n$ depth vs $2n$ for the QFT and $1.5n^2$ vs $0.5n^2$ cost on 1D-LNN (Conclusions, p. 23). So the $16p^2n$ number applies *only after* elementary-two-level decomposition — consistent with main.tex's framing of it as the $O(d^2)$ decomposition model.
- Conclusions, p. 23: **"the multipliers and diagonal circuits presented herein, can be adapted to operate on two dimensional qubits. Further work is in progress for the execution of the QAFrFT on existing quantum platforms for qubits."** This supports main.tex's parenthetical that the multipliers and quadratic-phase diagonals carry over to $p=2$ while the AFrFT proper does not.
- Scope: the paper is purely a construction/complexity paper — no hardware, no noise, no fidelity numbers, and no comparison with Shor's modular exponentiation.

**Judge verification questions:**
- Does main.tex's phrase "exists for odd prime $p$, where … $SO_2[\mathbb{Z}_{p^n}]$ is cyclic" match the paper's own statement "They are cyclic for every prime $p\neq2$", and does the paper ever claim the AFrFT exists for $p=2$?
- Is $16p^2n$ correctly identified in main.tex as the *depth* (not cost) of the MODMULC circuit, per Table 1 on p. 23?
- Does the paper anywhere provide a modular multiplier with a modulus other than the register size $p^n$, or accept a non-unit multiplication constant? (Main.tex asserts it does not.)
- Does the paper support the parenthetical that the multipliers/diagonals "carry over to any dimension, including $p=2$" — and if so, is the qualifier "whenever the multiplication constant is a unit" faithful to $\gcd(\lambda,p^n)=1$?

---

---

## `gardill2020` — Fast relaxation on qutrit transitions of nitrogen-vacancy centers in nanodiamonds (Gardill, Cambria & Kolkowitz, 2020)

**Full citation:** A. Gardill, M. C. Cambria and S. Kolkowitz, "Fast relaxation on qutrit transitions of nitrogen-vacancy centers in nanodiamonds," Phys. Rev. Appl. **13**, 034010 (2020); arXiv:1910.10813.
**Source:** arXiv:1910.10813v4, Phys. Rev. Appl. 13, 034010, PDF: `gardill-2019-nv-qutrit-fast-relaxation.pdf` (13 pp.)

**Cited in main.tex:**
- *Introduction* (single citation): grouped with `ringbauer2022, blok2021, goss2022, low2023, chiesa2024, robert2026` to support "Transmons, trapped ions, **nitrogen-vacancy centers**, molecular spins, and Rydberg-blockaded atom arrays all expose more than two usable levels, and processors that exploit them as qudits now exist or are proposed on several platforms."

**What the paper actually shows (full-text, not abstract-level):**
- Platform/scope: **5 single NV centers** in commercial (Adámas Nano) **~40-nm nanodiamonds**, spin-coated on a glass coverslip, measured on a room-temperature confocal microscope **under ambient conditions**. The 5 usable NVs were selected from a starting set of **110 nanodiamonds** (most emitters showed low or no ODMR contrast). This is a sensing/decoherence-spectroscopy study, **not a processor, not a gate demonstration, and not a computing proposal**.
- The paper does establish that the NV$^-$ ground state is a spin-1 triplet with three addressable levels $|H;0\rangle,|H;\pm1\rangle$, and it explicitly names $|H;-1\rangle\leftrightarrow|H;+1\rangle$ **"the qutrit transition"** (a generalization of the $\Delta m_s=2$ double-quantum transition), with $|H;0\rangle\leftrightarrow|H;\pm1\rangle$ called "the qubit transitions." Preparation and readout of *any* of the three states is achieved via 532-nm optical polarization plus state-selective resonant microwave $\pi$-pulses, giving "a total of nine measurement combinations." → three levels are demonstrably *addressable*.
- **The paper's actual result is a negative/cautionary one for qutrit use of NVs.** Abstract and Sec. III: at low axial field ($B_z<10$ G) the qutrit relaxation rate $\gamma$ **can exceed 100 kHz, more than two orders of magnitude faster** than the qubit-transition rate $\Omega$, "limiting the maximum theoretically achievable coherence times of NVs in this regime to tens of microseconds."
- **Table I (measured, 5 NVs):** max $\gamma$ = 117(8), 124(6), 110(20), 35(3), 240(50) kHz at splittings $\Delta_\pm$ = 19.8, 15.3, 17.1, 23.4, 10.9 MHz, giving $T_{2,\max}$ = 16.6(11), 16.0(8), 18(3), 57(4), 8.3(17) **µs**. $\Omega_{\rm avg}$ = 0.32–1.1 kHz. So $\gamma/\Omega$ is $\sim10^2$.
- Representative fit (Fig. 1e / Fig. 2c): $\Omega=1.0$ kHz, $\gamma=56$ kHz. A standard $|H;0\rangle$-based $T_1$ measurement gives a single exponential with $\sim330$ µs, but the authors note it "is blind to the population leakage between $|H;+1\rangle$ and $|H;-1\rangle$, and would therefore drastically overestimate the achievable coherence time $T_2$ for this NV." Population prepared in $|H;+1\rangle$ "has mostly depolarized after just ~20 microseconds."
- Attribution: fast $\gamma$ is attributed to **surface electric-field noise** (not magnetic noise — two independent tests rule magnetic noise out), scaling as $\gamma(\Delta_\pm)=A_0/\Delta_\pm^2+\gamma_\infty$ (consistent with $1/f^2$ noise PSD), with $E_\perp^{\rm RMS}\approx10^7$ V/m. $\gamma$ also **fluctuates on hour-to-day timescales** (Fig. 4, 140 consecutive hours).
- Practical recommendation the authors give: "whenever possible, measurements with NVs in nanodiamonds should be performed at moderate axial magnetic fields ($>60$ G)" — i.e. the qutrit-transition problem is mitigated by splitting the $\pm1$ levels, which is precisely what would be done to use the NV as a *qubit*.
- The comparison baseline (Myers et al., ref. [24] of the paper): in shallow NVs ~7 nm below the surface in *bulk* diamond, electric-field noise drives $\Delta m_s=2$ transitions at rates up to ~2 kHz, ">20× the rate between $m_s=0$ and $m_s=\pm1$."

**Judge verification questions:**
- Main.tex's sentence has two conjuncts: (a) NV centers "expose more than two usable levels" and (b) "processors that exploit them as qudits now exist or are proposed on several platforms." Which conjunct does gardill2020 support, and does the paper describe or propose any *processor*?
- Does citing this paper as evidence *for* qudit viability, without noting that its central result is that NV qutrit transitions relax at $10^2\times$ the qubit rate and cap $T_2$ at 8–57 µs, risk misrepresenting the source's thrust?
- Are the numbers in Table I ($\gamma$ up to 240 kHz, $T_{2,\max}$ down to 8.3 µs, 5 NVs from 110 nanodiamonds, ambient conditions, ~40-nm commercial nanodiamonds) compatible with any quantitative use main.tex makes of this reference elsewhere? (It appears exactly once, with no numbers attached.)

---

---

## `gerjuoy2005` — Shor's factoring algorithm and modern cryptography. An illustration of the capabilities inherent in quantum computers (Gerjuoy, 2005)

**Full citation:** E. Gerjuoy, "Shor's Factoring Algorithm and Modern Cryptography. An Illustration of the Capabilities Inherent in Quantum Computers," Am. J. Phys. **73**, 521–540 (2005); arXiv:quant-ph/0411184.
**Source:** arXiv:quant-ph/0411184v1, Am. J. Phys. 73, 521, PDF: `gerjuoy-2004-shor-factoring-modern-cryptography.pdf` (29 pp.)

**Cited in main.tex:**
- *Why the decoder gains tolerance with size* (single citation): listed inside a survey of exact success-probability results for continued-fraction post-processing on **base-2** registers — "Shor's original $4/\pi^2$ asymptotics [shor1997], **the sharp divisor-recovery bounds of Gerjuoy [gerjuoy2005]** and of Bourdon and Williams [bourdon2007], Ekerå's proof … [ekera2024], the tight two-sided window bounds of Magdon-Ismail and Dong [magdon2025], the self-contained treatise of Barzen and Leymann [barzen2022], …"

**What the paper actually shows (full-text, not abstract-level):**
- Genre: this is an **American Journal of Physics pedagogical article** ("This paper endeavors to explain, in a fashion comprehensible to the non-expert readers of this journal…"), self-contained, aimed at non-specialists. It is not a research paper on probability bounds per se, though it contains an original quantitative improvement.
- **Its one original quantitative claim, stated in the abstract:** "The careful analysis herein reveals, however, that **the probability of achieving a successful factorization on a single run is about twice as large as commonly quoted in the literature.**"
- The "commonly quoted" baseline, Eq. (51) (§III.C.6): $P_c\ge r^{-1}\sin^2(\pi\varepsilon)/(\pi\varepsilon)^2\ge r^{-1}(\pi/2)^{-2}=4/(r\pi^2)$, hence total $P=rP_c\ge 4/\pi^2\cong0.4$ for measuring a $c$ satisfying the strict window Eq. (48), $|c/2^y - d/r|\le 2^{-y-1}$. Gerjuoy explicitly attributes this $0.4$ to **Ekert and Josza**, noting "it is larger than the value of $P$ originally quoted by Shor." (Relevant if main.tex attributes $4/\pi^2$ to Shor in the adjacent clause.)
- Gerjuoy's improvement (Eq. 56–57, §III.C.7): a **widened window** $|c/2^y-d/r|\le 2\cdot2^{-y}$ still guarantees $d/r$ appears as a continued-fraction convergent of $c/2^y$; summing the four adjacent $P_c$ gives
  $P_c'\ \ge\ \frac{\sin^2\pi\varepsilon}{\pi^2 r}\left[\frac{1}{(1+\varepsilon)^2}+\frac{1}{\varepsilon^2}+\frac{1}{(1-\varepsilon)^2}+\frac{1}{(2-\varepsilon)^2}\right],\quad 0\le\varepsilon\le\tfrac12.$
  **At $\varepsilon=1/2$: $P_c'=80/(9\pi^2 r)=0.90/r$, i.e. total $P'\ge0.90$. Using the average $\varepsilon=1/4$: $P_c'=0.935/r$, i.e. $\approx0.935$.** This is the "about twice as large as commonly quoted" claim ($0.90$ vs $0.40$).
- He also notes (§III.C.6) that even within the strict window, replacing $|\varepsilon|$ by its *average* $1/4$ rather than its maximum $1/2$ gives $P_c\ge8/(r\pi^2)$, i.e. $P\ge0.81$.
- Everything is derived for a **base-2 register of $y$ qubits with $2^y>N^2$** (he shows explicitly that $2^y<N^2/4$ would break both the convergent guarantee and the uniqueness of $d/r$). There is no qudit / base-$d$ generalization anywhere.
- Uniqueness result (Eqs. 52–53): for a given $c$ satisfying Eq. (48) there is **exactly one** permissible fraction $d/r$ with $0<d<r<N/2$ — proved by showing $|d_1/r_1-d_2/r_2|>4/N^2$ while two solutions would force $\le2^{-y}<1/N^2$.
- **Caveats the author himself flags, which bound how "sharp" the result is:**
  - $P'\approx0.90$ is the probability of recovering *some* convergent $d/r$, **not** of factoring $N$. §III.C.8: "the probability that $r$ will meet the necessary requirements for being able to factor $N$, namely that $r$ is even and satisfies Eq. (14), is only about 1/2," so on average at least two full runs are needed.
  - Additional repetitions are needed when $\gcd(d,r)\ne1$: with $P''=P'\phi(r)/r$ and $\phi(r)/r\ge0.56/\ln\ln r\cong1.17/\log_2\log_2 r$ (Eq. 58, quoted from Ekert & Josza), the repetition count "might need to be increased by a factor of about $\log_2\log_2 r$" — though he argues this is "probably an overestimate."
  - He works a full concrete example throughout ($N=55$, $n=37$, $r=20$, $y=12$, $2^{12}=4096>N^2=3025$), verifying that 2251/4096, 2252/4096, 2253/4096, 2254/4096 all yield 11/20 as a convergent.

**Judge verification questions:**
- Main.tex calls these "**divisor**-recovery bounds." Gerjuoy's $0.90$/$0.935$ bounds are on recovering the **order $r$** (via a continued-fraction convergent $d/r$), and he separately notes only $\approx1/2$ of orders are usable for factoring. Is "divisor-recovery" an accurate label, or does it conflate order-finding success with factor-recovery success?
- Is "**sharp**" defensible? Gerjuoy's results are explicitly *lower bounds* ($P_c'\ge\cdots$), and he characterizes the earlier $4/\pi^2$ as one that "considerably underestimates" the true $P$ — so his own bound is tighter, not proven tight.
- Does main.tex's adjacent attribution of the $4/\pi^2$ figure to "Shor's original … asymptotics [shor1997]" conflict with Gerjuoy's statement that $4/\pi^2\cong0.4$ is due to **Ekert and Josza** and "is larger than the value of $P$ originally quoted by Shor"?
- Is main.tex's framing "on **base-2** registers" accurate for this reference? (Yes — check that the paper contains no base-$d$/qudit analysis, only $2^y$ registers.)

---

---

## `gokhale2019` — Asymptotic improvements to quantum circuits via qutrits (Gokhale et al., ISCA 2019)

**Full citation:** P. Gokhale, J. M. Baker, C. Duckering, N. C. Brown, K. R. Brown and F. T. Chong, "Asymptotic improvements to quantum circuits via qutrits," in *Proc. 46th Int. Symp. on Computer Architecture (ISCA '19)*, p. 554 (2019); arXiv:1905.10481.
**Source:** arXiv:1905.10481v1, ISCA '19 pp. 554–566, PDF: `gokhale-2019-asymptotic-improvements-via-qutrits.pdf` (13 pp.)

**Cited in main.tex:**
- *Introduction*: "Noisy qutrit circuit simulations exist [gokhale2019, gustafson2022], but **always at $d=3$ against a qubit baseline**; the closest cross-dimension noisy study … [agrawal2025] compares a single arithmetic primitive rather than a full algorithm with its decoder."
- *Introduction*: "qutrit advantages obtained with **native third levels---as ancillas** [gokhale2019] or as encoding capacity [gustafson2022]---versus 35–69% more non-Clifford gates for single-qutrit synthesis from a fault-tolerant gate set [gustafson2025synthesis]."
- *Introduction* (related-work differentiation): "the qutrit circuit studies of Gokhale *et al.* [gokhale2019] and Gustafson [gustafson2022] (**$d=3$ only; no comparison across multiple prime dimensions, no per-level-calibrated channel**)."

**What the paper actually shows (full-text, not abstract-level):**
- **Dimension studied: $d=3$ only.** Sec. 2: "Here, we focus on $d=3$ with which we achieve the desired improvements to the Generalized Toffoli gate." The only mention of larger $d$ is as *future work* in the Discussion: "there may be other circuits that are optimized by qudit information carriers for larger $d$." No simulation, cost model, or result at any $d>3$. → directly confirms main.tex's "$d=3$ only."
- **Third level used as an ancilla substitute.** Sec. 1: "our approach utilizes qutrits in a novel fashion, essentially **using the third state as temporary storage**"; Sec. 3.2: "instead of storing temporary results with a linear number of ancilla qubits, our circuit temporarily stores information directly in the qutrit $|2\rangle$ state of the controls. **Thus, no ancilla are needed.**" Inputs and outputs remain qubits; $|2\rangle$ is occupied only intermediately. → confirms main.tex's "native third levels—as ancillas."
- Headline circuit results (Generalized Toffoli, $N$ controls, ancilla-free): depth $633N \to 38\log_2 N$; two-qudit gate count $397N \to 6N$ (a **70×** reduction in the linearity constant vs. the ancilla-free Gidney qubit circuit, 8× vs. the borrowed-ancilla version at $76N$ depth / $48N$ gates). All three constructions are linear in *total* gate count; only depth is asymptotically improved.
- **Noise model — this is the key point for main.tex's "no per-level-calibrated channel":**
  - Gate errors: **symmetric depolarizing** in the generalized-Pauli basis, "assumes equal probabilities between each error channel." No-error probability drops from $1-3p_1\to1-8p_1$ (single) and $1-15p_2\to1-80p_2$ (two-operand) going from qubits to qutrits. Sec. 7.1.1: "The scaling of gate errors for a $d$-level qudit can be roughly summarized as increasing as $d^4$ for two-qudit gates and $d^2$ for single-qudit gates." So the model *charges qutrits more per gate*, uniformly — it is not calibrated to measured per-level fidelities.
  - Idle errors: amplitude damping only, with **Eq. (9): $\lambda_m = 1-e^{-m\Delta t/T_1}$** — a single device $T_1$ and a strictly *linear-in-level* damping law. There is no per-level $T_1^{(k)}$, no per-level-pair dephasing, and no dephasing channel at all in the superconducting models. → main.tex's "no per-level-calibrated channel" is accurate; note also that this is the **textbook $\Gamma_k\propto k$ ladder** that main.tex elsewhere contrasts against its own fitted $k^{0.7}$ law.
  - Qutrit amplitude damping is modeled as $|1\rangle\to|0\rangle$ (rate $\lambda_1$) and $|2\rangle\to|0\rangle$ (rate $\lambda_2$) — i.e. a direct $2\to0$ channel, not the sequential $2\to1\to0$ cascade.
  - Explicitly **not** modeled: initialization/readout errors ("we do not consider initialization errors and readout errors, because our circuit constructions maintain binary input and output"), crosstalk, and leakage.
- Noise parameters (Table 2, superconducting): SC baseline $3p_1=10^{-4}$, $15p_2=10^{-3}$, $T_1=1$ ms — i.e. **10× better gate errors and 10× longer $T_1$ than the then-current IBM hardware**; the other three models add a further 10× to gates, $T_1$, or both. Table 3 (trapped ion $^{171}$Yb$^+$): TI_QUBIT $p_1=6.4\times10^{-4}$, $p_2=1.3\times10^{-4}$; BARE_QUTRIT $2.2\times10^{-4}/4.3\times10^{-4}$; DRESSED_QUTRIT $1.5\times10^{-4}/3.1\times10^{-4}$; gate times 1 µs / 200 µs.
- Simulation results (Fig. 11, 14-input Generalized Toffoli, 1000+ trials/bar, $2\sigma<0.1\%$): abstract says "over 90% mean reliability (fidelity) for our circuit construction, versus under 30% for the qubit-only baseline"; Sec. 8 text says the qutrit circuit reaches **57–83%** under SC/SC+T1/SC+GATES with the ancilla-free qubit circuit at "almost 0%," and near-100% under SC+T1+GATES where QUBIT reaches 26%. Trapped ion: DRESSED_QUTRIT **96.1%**, BARE_QUTRIT **94.9%**, TI_QUBIT **44.7%**. Stated reliability advantage: "**2x for trapped ion noise models up to more than 10,000x for superconducting noise models**."
- Everything is benchmarked against a **qubit baseline** (Gidney ancilla-free, plus QUBIT+ANCILLA) — never against another qudit dimension.
- Author-stated caveats bearing on main.tex's differentiation: all-to-all connectivity is assumed (Sec. 4); on a nearest-neighbor 2D superconducting array the qutrit depth would degrade from $\log N$ to $\sqrt{N}$; simulations only up to 14 qutrits wide; the Section-5 algorithm applications (quantum neuron, Grover, incrementer, Shor's modular exponentiation) were **not explicitly simulated** ("we also expect to see an advantage for the circuits in Section 5 that rely on the Generalized Toffoli, although we did not explicitly simulate these circuits"). Sec. 5.4 is explicit that "a shallower Incrementer circuit alone is not sufficient to reduce the asymptotic cost of modular exponentiation (and therefore Shor's algorithm), it does reduce constants." → supports main.tex's implicit claim that this is not a full-algorithm-with-decoder study.

**Judge verification questions:**
- Does the paper contain any simulation, cost model, or comparison at $d>3$, or any comparison between two qudit dimensions? (Main.tex asserts "$d=3$ only; no comparison across multiple prime dimensions.")
- Is the noise model "per-level calibrated"? Check Eq. (9) $\lambda_m=1-e^{-m\Delta t/T_1}$ (single $T_1$, linear-in-$m$) and the symmetric-depolarizing gate channel against main.tex's "no per-level-calibrated channel."
- Is "as ancillas" a fair description of how Gokhale et al. use the third level? (Sec. 3.2/4.1: $|2\rangle$ as temporary storage replacing ancilla qubits, with qubit-only inputs/outputs.)
- Does the paper actually simulate Shor's algorithm or any full algorithm with a classical decoder, or only the Generalized Toffoli primitive at width 14?

---

---

## `goss2022` — High-fidelity qutrit entangling gates for superconducting circuits (Goss et al., 2022)

**Full citation:** N. Goss, A. Morvan, B. Marinelli, B. K. Mitchell, L. B. Nguyen, R. K. Naik, L. Chen, C. Jünger, J. M. Kreikebaum, D. I. Santiago, J. J. Wallman and I. Siddiqi, "High-fidelity qutrit entangling gates for superconducting circuits," Nat. Commun. **13**, 7481 (2022); arXiv:2206.07216.
**Source:** arXiv:2206.07216v3, Nat. Commun. 13, 7481, PDF: `goss-2022-high-fidelity-qutrit-entangling-gates.pdf` (28 pp. incl. supplement)

**Cited in main.tex (10 distinct contexts; merged):**
- *Introduction*: platform-existence list ("processors that exploit them as qudits now exist").
- *Introduction*: one of the sources for the anharmonic-ladder channel "calibrated to published per-level transmon coherence measurements."
- *Introduction*: "The native-gate cost requirement is met … by **native cross-Kerr transmon entanglers** [goss2022]."
- *Noise channels*: "the relaxation ratio $\Gamma_2/\Gamma_1$ is measured at $\approx1.7$ [goss2022, blok2021, tripathi2025, peterer2015, yurtalan2020, wang2025] against 2.0 for the textbook $\Gamma_k\propto k$ ladder, and the dephasing ratios $\Gamma_\phi^{01}:\Gamma_\phi^{12}:\Gamma_\phi^{02}$ are measured at $1:2.0:2.3$."
- *Noise channels*: "Measured per-gate infidelities place transmon two-qutrit gates at $2.7\times10^{-2}$–$4.8\times10^{-2}$ (CZ$^\dagger$/CZ process infidelity [goss2022])."
- *Gate-cost models*: `uniform` model = "native qudit entangler, one layer regardless of $d$—e.g. **the cross-Kerr CZ of Ref. [goss2022]**."
- *Robustness (readout)*: "a linear reading of the few-percent, higher-is-worse readout errors reported for transmon qutrits [blok2021, goss2022]"; and "**transmon qutrit assignment fidelities of 97–99% for $|0\rangle$ and 92–96% for $|2\rangle$** [blok2021, goss2022] correspond to $\varepsilon\approx0.01$–$0.03$."
- *Robustness (transmon test)*: "The measured cross-Kerr two-qutrit gates of Ref. [goss2022]—**CZ$^\dagger$ process fidelity $97.3(1)\%$, CZ $95.2(3)\%$**—face the matched calibrated-ladder/`uniform` pairing. Goss *et al.* report **no qubit-subspace entangler on the same footing**."
- *Robustness*: "the charge dispersion of $|2\rangle$ that drives idle dephasing is the same mechanism that limits the cross-Kerr entangler [blok2021, goss2022], so idle and gate error should co-scale."
- *Robustness*: "the $d\ge5$ verdicts only worsen here, **no transmon entangler beyond $d=3$ having been demonstrated at all** [goss2022]."
- *Discussion (limitations)*: "at the measured **$\alpha\approx0.1$–$0.7$ MHz** a residual always-on coupling dephases an unprotected two-qutrit coherence on the microsecond scale, i.e. within a few **580-ns** gate durations [goss2022]."

**What the paper actually shows (full-text, not abstract-level):**
- **Gate fidelities (Results/Benchmarking, p. 4–5, and Fig. 4c):** cycle benchmarking gives Weyl (generalized-Pauli) error rates of **2.7(1)% for CZ$^\dagger$ and 4.8(3)% for CZ**; the CB histogram fidelities are 0.936(1) (dressed CZ$^\dagger$) and 0.966(1) (reference cycle), "**yielding an estimated process fidelity of 97.3(1)%**." Abstract states "estimated process fidelities of 97.3(1)% and 95.2(3)%." So main.tex's "$2.7\times10^{-2}$–$4.8\times10^{-2}$ CZ$^\dagger$/CZ process infidelity" and "$97.3(1)\%$ / $95.2(3)\%$" both match.
  - Corroborating/qualifying numbers the paper reports: XEB depolarized fidelity **0.933(3)**; speckle-purity limit **0.961(3)**; CB purity-limited fidelity 0.973(9) dressed / **0.986(9) isolated CZ$^\dagger$**; worst-case error "less than 8%"; direct **process tomography gives $F_{\rm PTM}=93.2\%$** (Supp. Note 9, disfavored because SPAM-contaminated). Note the CB estimate (97.3(9)%) *exceeds* the speckle-purity limit (96.1(3)%), which the authors attribute to single-qutrit phase errors fluctuating between batches and to noise drift between the XEB and CB runs performed "in separate batches."
  - CB "reveals that the noise is dominated by single-qutrit phase errors."
- **Gate times (Fig. 3 caption + Supp. Tables 1–2):** "the CZ$^\dagger$ (CZ) is compiled with a total gate time of **580(783) ns**." → main.tex's 580 ns is the CZ$^\dagger$ time and is correct.
- **Coherence data — Supplementary Tables 1 and 2 (the only per-level numbers in the paper):**
  - CZ pair (Q3/Q4): $T_1^{01}$ = 125(37), 78(16) µs; $T_1^{12}$ = 63(9), 47(5) µs; $T_{2e}^{01}$ = 190(28), 138(25); $T_{2e}^{12}$ = 61(13), 45(7); $T_{2e}^{02}$ = 75(19), 62(6); $T_{2r}^{01}$ = 114(47), 99(24); $T_{2r}^{12}$ = 17(8), 17(9); $T_{2r}^{02}$ = 20(16), 21(9). Anharmonicities $-260.20$, $-262.94$ MHz.
  - CZ$^\dagger$ pair (Q5/Q6): $T_1^{01}$ = 45(7), 58(7); $T_1^{12}$ = 33(3), 28(3); $T_{2e}^{01}$ = 63(7), 84(6); $T_{2e}^{12}$ = 28(3), 30(3); $T_{2e}^{02}$ = 37(3), 35(3); $T_{2r}^{01}$ = 36(9), 76(8); $T_{2r}^{12}$ = 10(6), 18(6); $T_{2r}^{02}$ = 11(6), 21(8).
  - **Relaxation ratio check** ($\Gamma_2/\Gamma_1 = T_1^{01}/T_1^{12}$): 125/63 = 1.98; 78/47 = 1.66; 45/33 = 1.36; 58/28 = 2.07 → mean $\approx1.77$. **Consistent with main.tex's $\approx1.7$** and below the textbook 2.0.
  - **Dephasing ratio check** ($\Gamma_\phi=1/T_2-1/(2T_1)$, echo values): Q3 gives $\Gamma_\phi^{01}=1.26\times10^{-3}$, $\Gamma_\phi^{12}=8.46\times10^{-3}$ µs$^{-1}$ → ratio **6.7**; Q4 → **13.9**; Q5 → **4.3**; Q6 → **4.7**. Using $T_{2r}$ instead gives even larger ratios. These are all well above main.tex's stated measured $\Gamma_\phi^{01}:\Gamma_\phi^{12}=1:2.0$. (Main.tex describes 1:2.0:2.3 as a fit "spanning nine devices and $d=3$ to 12", so Goss 2022 is only one input — but a judge should confirm the aggregate is not dominated in the opposite direction by this source.)
- **Cross-Kerr magnitudes ($\alpha$): the paper reports NO numerical $\alpha_{ij}$ values in its text.** $\alpha_{ij}$ appear only as fitted slopes in Fig. 2b and as perturbative formulas (Supp. Eqs. S5–S12). The only numeric MHz quantities in the text are drive amplitudes $\Omega\approx11$/13 MHz, coupling $J=2.7$ MHz, anharmonicities $\eta_c=272$, $\eta_t=270$ MHz, and (Supp. Note 8) simulation-filtering thresholds: linear-fit uncertainty $<300$ kHz and "we also omitted points where the magnitude of the **simulated** cross-Kerr was larger than 3 MHz." **The tabulated measured values $\alpha_{11}=0.10/0.16$, $\alpha_{12}=0.60/0.41$, $\alpha_{21}=-0.44/-0.16$, $\alpha_{22}=0.36/0.49$ MHz are in `goss2024` (Table A1), not in `goss2022`.** Their range is $|\alpha|=0.10$–$0.60$ MHz, not 0.1–0.7.
- **Readout: the paper reports NO assignment/readout fidelities.** "readout" appears exactly three times, all in the Introduction as background citations ("dispersive readout can be used for high-fidelity single shot qutrit readout [27]"; "improved qubit readout [38]"). There is no confusion matrix, no $P(k|k)$, no per-level readout error anywhere in the main text or supplement. **The numbers $P(0|0)=0.994/0.991/0.986$ and $P(2|2)=0.974/0.943/0.951$ are in `goss2024` Table A1** — which bracket main.tex's quoted "97–99% for $|0\rangle$" (98.6–99.4%) and "92–96% for $|2\rangle$" (94.3–97.4%) fairly well.
- **Dimension: $d=3$ exclusively.** All gates are two-qutrit; no $d>3$ transmon result is presented. The paper's framing supports the difficulty claim: "generating high-fidelity, maximally entangling two-qudit gates remains a major challenge in superconducting circuits," and the previous best transmon two-qutrit gate had error 11.1% (Blok et al.). But the paper makes **no explicit statement that no transmon entangler beyond $d=3$ has been demonstrated.**
- **No qubit-subspace entangler is benchmarked.** Confirmed — the paper benchmarks only the qutrit CZ/CZ$^\dagger$, and its own Discussion asks the community to develop "metrics and benchmarks … to reasonably compare qudit vs. qubit gates," implicitly conceding no matched comparison exists. → supports main.tex's "Goss *et al.* report no qubit-subspace entangler on the same footing."
- **Single-application / one-layer character** (relevant to the `uniform` cost model): "unique amongst these gates, the CZ/CZ$^\dagger$ can generate maximally entangled two qutrit states **with a single iteration of the gate**" (Bell state $\frac{1}{\sqrt3}(|00\rangle+|11\rangle+|22\rangle)$ reconstructed at $F=0.952$). Note the gate itself is compiled from **two rounds of cross-Kerr driving with interleaved $X_\pi^{12}$ echo pulses** (Fig. 3), so "one layer" is a logical-layer statement, not a single physical pulse. Also: the gate is Clifford and maximally entangling; all 1000 Haar-random two-qutrit unitaries synthesize at depth 6 in CZ/CZ$^\dagger$ vs. 7 for $C_{\rm inc}$ and 9 for $C_{\rm ex}$ (the trapped-ion subspace gates of Ringbauer et al.), and Cliffords at depth 3 vs. 6/9.
- **Leakage:** the authors state only "To ensure adiabaticity and **limit leakage**, we perform the Stark drive via flat-top cosine pulses with ramp up and down features." **They never quantify a leakage fraction**, so main.tex's leakage-fraction sweep is a hypothetical over an unmeasured quantity, not a use of a reported number.
- **Charge dispersion of $|2\rangle$:** not discussed in Goss 2022 (the mechanism analysis there is the perturbative cross-Kerr in terms of $J$, $\eta$, $\Delta$, $\Omega$). The charge-dispersion argument main.tex attributes to `blok2021, goss2022` is, on the Goss 2022 side, at best inferable from the $|2\rangle$ coherence being ~3× worse than $|1\rangle$ in Supp. Tables 1–2.

**Judge verification questions:**
- **Readout attribution:** main.tex cites `goss2022` for "transmon qutrit assignment fidelities of 97–99% for $|0\rangle$ and 92–96% for $|2\rangle$." Does Goss 2022 report *any* readout/assignment fidelity? (It does not; the corresponding table is `goss2024` Table A1, with $P(0|0)$ 98.6–99.4% and $P(2|2)$ 94.3–97.4%.) Should the citation be `goss2024`?
- **Cross-Kerr magnitude attribution:** main.tex cites `goss2022` for "the measured $\alpha\approx0.1$–$0.7$ MHz." Does Goss 2022 tabulate numerical $\alpha_{ij}$ anywhere? (The tabulated values are in `goss2024`: $|\alpha|$ = 0.10–0.60 MHz.) Is the upper bound "0.7" supported by any reported number?
- **Dephasing ratio:** do Supp. Tables 1–2 of Goss 2022 support $\Gamma_\phi^{01}:\Gamma_\phi^{12}\approx1:2.0$? Computing $\Gamma_\phi=1/T_{2e}-1/(2T_1)$ per qutrit gives ratios of 4.3–13.9, not 2.0. Is main.tex's nine-device aggregate still defensible given this source, and is the direction of the discrepancy (model *under*-penalizing high-level dephasing) acknowledged?
- **Relaxation ratio:** does $T_1^{01}/T_1^{12}$ from Supp. Tables 1–2 (1.36, 1.66, 1.98, 2.07; mean 1.77) support "$\Gamma_2/\Gamma_1$ measured at $\approx1.7$ … against 2.0 for the textbook ladder"?
- **Fidelity/gate-time numbers:** are $97.3(1)\%$, $95.2(3)\%$, $2.7$–$4.8\times10^{-2}$ and $580$ ns each reproduced exactly from the paper, and is main.tex's label "process infidelity" consistent with the paper's own distinction between the CB *Weyl error rate* (2.7%/4.8%) and the *estimated process fidelity* (97.3%/95.2%)?
- **Absence claims:** does Goss 2022 assert that "no transmon entangler beyond $d=3$ has been demonstrated at all," or is main.tex attributing an absence-of-evidence claim to a paper that merely happens to work at $d=3$?
- **`uniform` cost model:** does citing the Goss CZ as "one layer regardless of $d$" over-generalize a gate that exists only at $d=3$ and is itself compiled from two cross-Kerr rounds plus echo pulses?
- **Leakage:** does the paper quantify the leaked fraction $\lambda$ that main.tex's leakage sweep parameterizes, or only state that flat-top cosine pulses "limit leakage"?

---

---

## `goss2024` — Extending the computational reach of a superconducting qutrit processor (Goss et al., 2024)

**Full citation:** N. Goss, S. Ferracin, A. Hashim, A. Carignan-Dugas, J. M. Kreikebaum, R. K. Naik, D. I. Santiago and I. Siddiqi, "Extending the computational reach of a superconducting qutrit processor," npj Quantum Inf. **10**, 101 (2024); arXiv:2305.16507.
**Source:** arXiv:2305.16507v1, npj Quantum Inf. 10, 101, PDF: `goss-2023-extending-reach-qutrit-processor.pdf` (14 pp.)

**Cited in main.tex:**
- *Robustness* (single citation): "Nor is the measured number a ceiling: **the same group has since demonstrated the first qutrit error-mitigation protocols---noise tailoring with up to $3\times$ improvement in effective error on a transmon qutrit processor** [goss2024]---so the 0.9-point gap is within reach of demonstrated mitigation, with the caveat that mitigation overhead is itself exposure this paper's accounting would charge."

**What the paper actually shows (full-text, not abstract-level):**
- **Priority claim is explicit and matches "first":** abstract — "To the best of our knowledge, this constitutes the **first ever error mitigation experiment performed on qutrits**." Conclusions repeat: "Our work is the first to experimentally demonstrate that error-mitigation can be effectively implemented on qutrit platforms."
- **"Up to 3×" is the paper's own headline:** abstract — "benchmark their effectiveness for multipartite qutrit entanglement and random circuit sampling, **obtaining up to 3x improvement in our results**"; Sec. I — "achieving up to a 3 times improvement in fidelity."
- **Where the 3× comes from, precisely (Sec. III.A):** three-qutrit GHZ state $\frac{1}{\sqrt3}(|000\rangle+|111\rangle+|222\rangle)$ on a $D=27$ Hilbert space, full three-qutrit tomography (729 circuits). Bare state fidelity **$F=0.818$**; with RC+NOX (43,740 = 729×20×3 circuits) **$F=0.951$**, "resulting in a **greater than 3x reduction in infidelity** compared to the unmitigated case." Purifying the RC-only reconstructed state improved fidelity from 0.912 to 0.998.
  - **Scope caveat for main.tex's phrase "effective error":** the 3× is a reduction in *three-qutrit GHZ state infidelity*, **not** a measured reduction in two-qutrit gate error or process infidelity. The paper reports no post-mitigation CZ$^\dagger$ gate fidelity.
- Second experiment (Sec. III.B, random circuit sampling, 2 and 3 qutrits, 20 instances/depth, variation distance metric): "when employing RC+NOX in both the two and three-qutrit RCS experiments, the variation distances at depth 6 were comparable to the unmitigated case at depth 2, and **at all depths we found at least a 30% fractional improvement**." Best mitigated results used 3 identity insertions.
- **Methods = noise *tailoring* + *mitigation*, and the overhead main.tex flags is real and explicit:**
  - Randomized Compiling (RC) twirls Markovian noise into stochastic Weyl channels; the twirled circuit has the **same depth** as the input (extra Weyl gates are recompiled into the native single-qutrit cycles). Fig. 2d numerically shows coherent-error suppression is **independent of $d$** for $d\in\{2,3,5\}$: "for an equal suppression of coherent errors, RC does not require additional twirls in higher dimensions" (Hoeffding bound Eq. 6 is dimension-independent).
  - Noiseless Output Extrapolation (NOX) requires running amplified copies via **unitary folding** ($WH \to (WH)^{\alpha+1}$), i.e. it *deepens* the circuit — this is the "mitigation overhead is itself exposure" point. The 3× GHZ result cost 43,740 circuits vs. 729 (a **60× sampling overhead**).
  - RCAL (readout calibration) inverts single-qutrit confusion matrices to remove assignment error.
- **Device parameters, Appendix A / Table A1 (3 fixed-frequency transmons on an 8-qutrit ring; the same platform family as `goss2022`, gate mechanism referenced to `goss2022`):**
  - Qubit freq. 5.299/5.362/5.523 GHz; anharm. $-272/-275/-271$ MHz.
  - $T_1^{01}$ = 60(13), 64(20), 47(14) µs; $T_1^{12}$ = 36(4), 33(4), 34(5) µs → $T_1^{01}/T_1^{12}$ = 1.67, 1.94, 1.38.
  - $T_{2e}^{01}$ = 69(7), 82(12), 61(14) µs; $T_{2e}^{12}$ = 32(5), 33(4), 32(6) µs.
  - **Readout: $F_{\rm RO}\ P(0|0)$ = 0.994, 0.991, 0.986; $P(1|1)$ = 0.979, 0.953, 0.943; $P(2|2)$ = 0.974, 0.943, 0.951.** (This is the table that actually contains the assignment fidelities main.tex attributes to `goss2022`.)
  - Single-qutrit RB: $F_{\rm RB,Iso}$ = 0.991/0.992/0.989; $F_{\rm RB,Sim}$ = 0.975/0.969/0.972.
  - **Cross-Kerr rates: $\alpha_{11}$ = 0.10/0.16, $\alpha_{12}$ = 0.60/0.41, $\alpha_{21}$ = $-0.44$/$-0.16$, $\alpha_{22}$ = 0.36/0.49 MHz** (two gate pairs). Range $|\alpha|$ = 0.10–0.60 MHz. (This is the table that actually contains the $\alpha$ values main.tex attributes to `goss2022`.)
- Author-acknowledged limitation relevant to main.tex's overhead caveat: Appendix E area — mitigation "overhead with large system sizes, we do not consider" (the sampling cost of NOX is not carried to scale). The paper also notes a "sizable portion of our error budget can be caused by **coherent calibration errors** in the two-qutrit gate," which is exactly what RC targets — so the 3× is largely recovery of *calibration* error, not of decoherence.
- Dimension: **$d=3$ only** experimentally (the $d\in\{2,3,5\}$ appearance in Fig. 2d is a numerical PTM study of RC twirling, not hardware).

**Judge verification questions:**
- Is "up to $3\times$ improvement in **effective error**" a faithful rendering of the paper's "greater than 3x reduction in **infidelity**" of a *three-qutrit GHZ state fidelity* (0.818 → 0.951)? Does the paper report any 3× improvement in a *gate* error, which is the quantity main.tex's 0.9-point gap is measured in?
- Does the paper support "first qutrit error-mitigation protocols"? (Check the explicit "first ever error mitigation experiment performed on qutrits.")
- Is main.tex's caveat that "mitigation overhead is itself exposure" consistent with what the paper reports — specifically NOX's unitary folding (circuit deepening) and the 729 → 43,740 circuit count?
- Given that main.tex elsewhere attributes assignment fidelities and cross-Kerr $\alpha$ values to `goss2022`, but Table A1 of `goss2024` is where those numbers actually appear, are the citations in the Robustness (readout) and Discussion (limitations) paragraphs pointing at the right paper?

---

## `gottesman1999` — Fault-Tolerant Quantum Computation with Higher-Dimensional Systems (Gottesman, 1998/1999)

**Full citation:** D. Gottesman, "Fault-tolerant quantum computation with higher-dimensional systems," *Chaos, Solitons & Fractals* **10**, 1749 (1999); arXiv:quant-ph/9802007.
**Source:** arXiv quant-ph/9802007 (v1, 2 Feb 1998; LANL preprint LA-UR 98-270), PDF: `gottesman-1998-ft-higher-dimensional-systems.pdf` (12 pp., read in full via text extraction)

**Cited in main.tex:**
- *Introduction*: "fault-tolerant stabilizer constructions close cleanly in prime dimension" — i.e. the prime-dimension restriction adopted throughout the paper is justified by fault-tolerance theory.
- *Robustness*: co-cited with `campbell2012` and `floratos2024` for the statement that "the bare-circuit dynamics carries no trace of primality; the prime restriction elsewhere in this paper is inherited from the fault-tolerance and QFT-arithmetic motivations." I.e. Gottesman is credited only as a *motivation* for restricting to prime $d$, not as a claim about noisy dynamics.

**What the paper actually shows (full-text, not abstract-level):**
- Abstract and Sec. 1: "I prove that universal fault-tolerant computation is possible with any higher-dimensional stabilizer code for prime $d$." The prime hypothesis is stated up front and repeated: "Assume that $d$ is prime unless it is otherwise specified" (Sec. 1, end).
- Generalized Pauli group: $X_d|j\rangle = |j+1\rangle$, $Z_d|j\rangle = \omega^j|j\rangle$, $X_dZ_d = \omega^{-1}Z_dX_d$, elements $\omega^a X_d^r Z_d^s$ (Sec. 2, Eqs. 4–5).
- **The specific place primality is load-bearing** (Sec. 2): "If the stabilizer on $n$ qudits has $n-k$ generators, then $S$ will have $d^{n-k}$ elements and the coding space will consist of $k$ qudits. Note that this last fact need no longer be true when $d$ is not prime, and this is the main source of complications in that case. It is unclear exactly how to deal with a code that does not encode an integral number of qudits." This is the sharpest support for "close cleanly in prime dimension."
- Second place: the Clifford-group generation argument. $R$ (Fourier), $P$ (phase $|j\rangle\to\omega^{j(j-1)/2}|j\rangle$), SUM, plus the $S$ gate $|j\rangle\to|aj\rangle$ with $ab\equiv 1 \bmod d$; "a single pair $(a,b)$ is sufficient, as long as $a$ generates the multiplicative group $\mathbb{Z}_d^*$." Gottesman then states: "The structure is somewhat more complicated when $d$ is not prime, and I have not verified that these gates are sufficient for the nonprime case."
- Third place, in the measurement/stabilizer-update argument (Sec. 3): after $MA = \omega AM$, "note that when $d$ is prime, this will always be true for some power of $M$."
- Footnote 3 additionally distinguishes **odd** from even $d$: "This is true for odd $d$. For even $d$, $XZ$ has order $2d$, so extra factors of $i$ will be necessary, as in the $d=2$ case. This aspect is actually simpler for odd $d$ than for $d=2$." Sec. 2 likewise notes "when $d$ is even, this actually imposes an additional constraint on the overall phase of elements of $S$." So the paper's cleanliness argument splits along *two* axes (prime, and odd), not one.
- Partial rescue for non-prime $d$: "If we stick to codes for which all the generators of the stabilizer have order $d$, the rest of the proof will hold, modulo a question about gates necessary to generate the Clifford group." So the prime restriction is a sufficient-condition/technical-convenience statement, not a proven impossibility for composite $d$.
- Constructive content: Secs. 4–6 build $P$, $R$, $S$ from SUM + Pauli measurement; Sec. 5 builds SUM between *any* pair of encoded qudits (same or different blocks, different codes, different block sizes) using a single logical ancilla qudit; Sec. 6 completes universality with the qudit Toffoli $|a\rangle|b\rangle|c\rangle\to|a\rangle|b\rangle|c+ab\rangle$ via a Shor-style magic ancilla $|A\rangle = \sum_{a,b}|a\rangle|b\rangle|ab\rangle$ and CAT-state measurement of $M_3$.
- **Scope limits relevant to a citing paper:** this is a pure fault-tolerance/algebraic-structure result. There are no noise models, no error rates, no thresholds, no numerical simulations, no claim about decoherence, and no claim that prime-dimension qudits are *physically* advantageous. Nothing in it bears on bare (unencoded) noisy circuit dynamics.

**Judge verification questions:**
1. Does main.tex claim only that prime $d$ makes the *stabilizer/fault-tolerance construction* close cleanly — or does it (incorrectly) upgrade Gottesman into a claim about noise, thresholds, or physical advantage of prime qudits? (Gottesman contains none of the latter.)
2. Gottesman's own qualification is that composite $d$ is "complicated"/"unclear," and he explicitly leaves a partial route open (codes whose stabilizer generators all have order $d$). Does main.tex overstate this as an impossibility or a hard requirement?
3. The Robustness sentence says the prime restriction is "inherited from the fault-tolerance ... motivations." Is that an accurate description of Gottesman's role in the argument (a motivation, not a derived constraint on the simulated dynamics)? Does main.tex anywhere let this citation imply the *simulated* results depend on primality?
4. Gottesman's paper number/year: the arXiv preprint is 1998 (quant-ph/9802007), published in *Chaos, Solitons & Fractals* 10, 1749 (1999). Does the bib entry's year/volume/page match the published version?

---

---

## `gross2006` — Hudson's Theorem for finite-dimensional quantum systems (Gross, 2006)

**Full citation:** D. Gross, "Hudson's theorem for finite-dimensional quantum systems," *J. Math. Phys.* **47**, 122107 (2006); arXiv:quant-ph/0602001.
**Source:** arXiv quant-ph/0602001v3 (1 Feb 2007), PDF: `gross-2006-hudson-theorem-wigner-functions.pdf` (17 pp.; read intro, phase-space formalism, Wigner definition, uniqueness theorem, prime-power section)

**Cited in main.tex:**
- *Introduction*: "the discrete phase-space structure is cleanest in odd dimension" — a structural motivation, cited alongside `gottesman1999` (prime-dimension fault tolerance) and `floratos2024` (odd-prime QFrFT).

**What the paper actually shows (full-text, not abstract-level):**
- Main result, Theorem 2 (Discrete Hudson's Theorem), stated with an explicit odd hypothesis: "**Let $d$ be odd** and $\psi \in L^2(\mathbb{Z}_d^n)$ be a state vector. The Wigner function of $\psi$ is non-negative if and only if $\psi$ is a stabilizer state." Explicit form: $\psi(q) \propto e^{\frac{2\pi}{d}i(q\theta q + xq)}$ with $\theta$ symmetric over $\mathbb{Z}_d$ — the exact discrete analogue of the continuous Gaussian $e^{2\pi i(q\theta q + xq)}$.
- **The specific technical reason odd $d$ is needed:** the Wigner function is defined using $2^{-1} = (d+1)/2$, the multiplicative inverse of 2 modulo $d$, which exists only for odd $d$. It appears in the Wigner function itself, $W_\psi(p,q) = d^{-1}\sum_{\xi\in\mathbb{Z}_d} e^{-\frac{2\pi}{d}i\xi p}\bar\psi(q-2^{-1}\xi)\psi(q+2^{-1}\xi)$, in the Weyl operator phase convention $w(p,q)=\chi(-2^{-1}pq)\hat z(p)\hat x(q)$ (Eq. 3), and in the composition law (Eq. 4). Sec. II A opens "We start by considering a $d$-dimensional quantum system, **$d$ odd**." Definition 5 (Wigner function) likewise begins "Let $d$ be odd."
- Gross argues the odd-$d$ definition is canonical from two independent directions: it is the discrete symplectic Fourier transform of the characteristic function (in complete analogy to the continuous case), *and* it satisfies the Gibbons–Hoffman–Wootters axioms. Introduction: "We will argue that, for odd dimensions $d$, [the above] is the most sensible analogue of Eq. (1), judged in terms of either of these approaches."
- Uniqueness (Theorem 23): "**Let $d$ be an odd prime.**" Under (1) phase space linearity, (2) Clifford covariance, one gets $W' = \lambda_1 W + \lambda_2$; adding (3) correct marginals forces $W' = W$. So the *uniqueness* statement is stated for odd **prime** $d$, stronger than merely odd.
- Contrast with the axiomatic (GHW) approach: "for a $d$-dimensional Hilbert space, there exist $d^{d+1}$ distinct generalized Wigner functions" — i.e. the GHW axioms alone do *not* pin down a unique object; Gross's construction does (Theorem 23). Also, the GHW line-based construction "has been described only for the case where $d=p^n$ is the power of a prime, because only then the notion of a line in phase space has a well-defined meaning."
- Properties valid in the odd-$d$ setting (Theorem 6): phase-space point operators are an orthonormal Hermitian basis; $d^{-n}\mathrm{tr}(\rho\sigma) = \sum_v W_\rho(v)W_\sigma(v)$; correct normalization; multi-particle factorization $A(p_1..p_n,q_1..q_n)=\bigotimes_i A^{(i)}(p_i,q_i)$; $A(0)|q\rangle = |-q\rangle$ (phase-space point operator at origin = parity operator); Groenewold/Moyal $\star$-product for operator products.
- **Explicit limitation the authors state:** "our main theorem does not address qubits or mixed states, which Galvão et al. do." And Sec. V refutes the natural mixed-state conjecture by counter-example: non-negative-Wigner mixed states are *not* all convex combinations of stabilizer states.
- Primality (as distinct from oddness) matters separately: "For prime values of $d$, $\mathbb{Z}_d$ has the structure of a finite algebraic field, $\mathbb{Z}_d^n$ is a finite vector space and most of the intuitions we have about vector spaces continue to be true." Non-prime subspaces misbehave (worked counterexample $\{0,3,6\}\subset\mathbb{Z}_9$ is closed but not of the form $\mathbb{Z}_9^{n'}$). Gross notes "the Clifford covariance of the Wigner function in non-prime dimensions, seem to be new," and Sec. VII treats prime-power dimensions separately.

**Judge verification questions:**
1. main.tex says the phase-space structure is "cleanest in **odd** dimension." Gross's *main theorem* is odd-$d$; his *uniqueness* theorem is odd-**prime**-$d$. Does main.tex conflate odd with odd-prime, or use `gross2006` to support a prime-specific claim it does not make?
2. Is the sentence structured so that `gross2006` supports only the odd/phase-space clause and `gottesman1999` only the prime/fault-tolerance clause? (Both are structural-motivation claims; neither paper supports the other's clause.)
3. Does main.tex anywhere imply Gross shows an *operational* or noise-related advantage for odd $d$? The paper is a mathematical characterization of non-negative Wigner functions with no noise, hardware, or performance content, and it explicitly excludes qubits and mixed states.
4. Is the "cleanest in odd dimension" phrasing supported by the concrete mechanism (the need for $2^{-1} \bmod d$, which fails at even $d$), and does main.tex avoid implying that even-$d$ discrete Wigner functions do not exist at all (they do — they are just not covered by this construction)?

---

---

## `grover1996` — A fast quantum mechanical algorithm for database search (Grover, 1996)

**Full citation:** L. K. Grover, "A fast quantum mechanical algorithm for database search," in *Proc. 28th ACM Symp. on Theory of Computing (STOC)*, 212–219 (1996); arXiv:quant-ph/9605043.
**Source:** arXiv quant-ph/9605043 (updated version of the STOC 1996 paper, pp. 212–219), PDF: `grover-1996-fast-quantum-database-search.pdf` (8 pp., read in full)

**Cited in main.tex:**
- *Introduction*: "We simulate Shor order finding~\cite{shor1997}, eigenstate quantum phase estimation (QPE)~\cite{kitaev1995}, and Grover search~\cite{grover1996} on qubit ($d=2$), qutrit ($d=3$), and ququint ($d=5$) registers, under two decoherence channels..." — i.e. `grover1996` is cited as the definition/source of the third simulated algorithm.
- (Elsewhere in main.tex, Sec. "Grover search: decomposing the mechanism" and Sec. Methods define the simulated instance: Grover over $M=d^n$ items with $\lfloor(\pi/4)\sqrt{M}\rceil$ iterations; success = probability of measuring the marked item, averaged over marked items excluding $|0\cdots0\rangle$.)

**What the paper actually shows (full-text, not abstract-level):**
- Problem: unsorted database of $N$ items, **exactly one** item $S_\nu$ satisfies $C(S_\nu)=1$; $C(S)$ evaluable in unit time; no exploitable structure. Classical cost: average $N/2$ examinations.
- Algorithm (Sec. 3): (i) uniform superposition over $N$ states, obtainable in $O(\log N)$ steps; (ii) repeat $O(\sqrt N)$ times: (a) rotate the phase of the marked state by $\pi$; (b) apply the diffusion transform $D$ with $D_{ij} = 2/N$ ($i\ne j$), $D_{ii} = -1 + 2/N$; (iii) sample — the final state is the marked one "with a probability of at least $1/2$."
- $N = 2^n$ throughout; states are $n$-bit strings; $W_{ij} = 2^{-n/2}(-1)^{i\cdot j}$ is the **Walsh–Hadamard** transform on bits. **The paper is entirely qubit-based; it defines no qudit generalization.** The remark "or a closely related operation called the Fourier Transformation" (Sec. 1.2) is the only gesture in that direction.
- $D = WRW$ with $R_{ii}=1$ for $i=0$, $R_{ii}=-1$ for $i\ne 0$ (Theorem 1); $D = -I + 2P$ with $P_{ij}=1/N$, so $D$ is "inversion about average" and $D^2 = I$ (unitary).
- Theorem 3: with marked amplitude $k$, unmarked $l$, $0<k<1/2$, $l>0$, one iteration gives $\Delta k > 1/(2\sqrt N)$. Consequence stated in the text: "there exists a number $M$ **less than $\sqrt{2N}$**" iterations after which $k$ exceeds $1/\sqrt2$, i.e. success probability $k^2 \ge 1/2$.
- **The $\pi/4$ constant is NOT in this paper.** Grover gives $O(\sqrt N)$ and the bound $M < \sqrt{2N}$, and defers the exact iteration count to Boyer–Brassard–Høyer–Tapp: "the precise number of repetitions is important as discussed in [BBHT96]" (Sec. 3(ii)), and "[BBHT96] gives a direct proof of this result along with tight bounds showing the algorithm of this paper is within a few percent of the fastest possible quantum mechanical algorithm" (Sec. 6). The optimal $\approx(\pi/4)\sqrt N$ count is due to BBHT, not Grover 1996.
- Optimality: matching $\Omega(\sqrt N)$ lower bound quoted from Bennett–Bernstein–Brassard–Vazirani (Sec. 6); Grover's algorithm is "within a small constant factor of the fastest possible."
- Multiple marked items: Sec. 8, remark 3 — the unique-solution assumption "can be easily modified" via (i) BBHT-style degeneracy range search or (ii) MVV random perturbation. Not analysed quantitatively here.
- Implementation notes (Sec. 7): the phase-inversion step "does not involve a classical measurement" and must leave "no trace of the state," so interfering paths stay indistinguishable.
- **Scope limits relevant to a citing paper: there is no noise model, no decoherence analysis, no error rate, no fidelity, and no qudit ($d>2$) content anywhere in the paper.**

**Judge verification questions:**
1. main.tex simulates Grover on $d=3$ and $d=5$ registers. Does the text attribute the *qudit generalization* (base-$d$ diffuser / QFT$_d$-style reflection, $M=d^n$) to `grover1996`, which contains no such generalization, or does it present the generalization as its own construction with `grover1996` cited only for the base algorithm?
2. main.tex uses $\lfloor(\pi/4)\sqrt{M}\rceil$ iterations. Is that iteration count attributed to `grover1996`? Grover states only $O(\sqrt N)$ and $M<\sqrt{2N}$ and explicitly defers the tight count to BBHT96 — so citing `grover1996` alone for $\pi/4$ would be a misattribution.
3. Grover 1996 assumes exactly **one** marked item. Does main.tex's Grover instance (single marked item, averaged over marked items excluding $|0\cdots0\rangle$) stay inside that assumption, and does it flag the exclusion of $|0\cdots0\rangle$ as its own choice rather than something in the source?
4. Does main.tex ever cite `grover1996` for a noise, fidelity, or acceptance-set property? The paper has zero noise content; its "acceptance set is the single marked item at every size" (main.tex, Sec. mechanism) is a consequence of the algorithm's definition, which is fair, but any noise-related attribution would not be.

---

---

## `gustafson2022` — Noise Improvements in Quantum Simulations of sQED using Qutrits (Gustafson, 2022)

**Full citation:** E. J. Gustafson, "Noise improvements in quantum simulations of sQED using qutrits," arXiv:2201.04546 (2022); FERMILAB-PUB-22-002-SQMS-T.
**Source:** arXiv:2201.04546v1 (12 Jan 2022), PDF: `gustafson-2022-noise-improvements-sqed-qutrits.pdf` (15 pp., read in full through the conclusions)

**Cited in main.tex:**
- *Introduction* (related work): "Noisy qutrit circuit simulations exist~\cite{gokhale2019,gustafson2022}, but always at $d=3$ against a qubit baseline."
- *Introduction* (verdict split): "qutrit advantages obtained with native third levels---as ancillas~\cite{gokhale2019} or as **encoding capacity**~\cite{gustafson2022}---versus 35--69\% more non-Clifford gates for single-qutrit synthesis from a fault-tolerant gate set~\cite{gustafson2025synthesis}."
- *Introduction* (differentiation from prior work): "the qutrit circuit studies of Gokhale \emph{et al.}~\cite{gokhale2019} and Gustafson~\cite{gustafson2022} (**$d=3$ only; no comparison across multiple prime dimensions, no per-level-calibrated channel**)."

**What the paper actually shows (full-text, not abstract-level):**
- Model and system: (1+1)d scalar QED (sQED) rotor Hamiltonian, **three-state truncation** of the link Hilbert space ($|{-}1\rangle,|0\rangle,|{+}1\rangle$), on **four sites**, with $a_s=1$, $g^2a_s=5$. Observable: the mass gap, extracted from the FFT peak of a real-time out-of-time/temporal correlator (Eqs. 10–11, 17).
- **Encoding-capacity argument (this is exactly what main.tex attributes):** "The structure of the operators in this model are naturally truncated to an odd-dimensional local Hilbert space... For this reason the simplest mapping for this model would require 3 states." Mapping onto two qubits leaves "an added difficulty that an unused fourth state $|11\rangle_2$ remains. Including this state results in the un-physical portions of the Hilbert space being reached when gate noise is present." So the advantage is the native match of a 3-dimensional local Hilbert space to one qutrit, plus the absence of a leakage-prone unphysical state — i.e. encoding capacity, not ancilla use.
- Gate-count evidence (Table II, per operator, qubit-1q/qubit-2q vs qutrit-1q/qutrit-2q): $V_g$ 3/2 vs 2/0; $CU_g$ **54/54 vs 5/2**; $e^{-i\theta(L^z)^2}$ 1/0 vs 2/0; $e^{-i\theta U^x}$ 6/2 vs 5/0; $e^{-i\theta L^zL^z}$ 4/26 vs 4/3. Text: the qubit $CU_g$ encoding "is sixteen times longer in terms of entangling gate depth"; all-to-all connectivity needs 15 CNOTs, linear connectivity rises to 51 CNOTs (36 of them inside SWAPs), with 48 CNOTs during which other qubits idle. For $e^{-i\theta L^zL^z}$: 8 entangling + 6 SWAP (18 CNOT) gates for qubits vs 3 CSUM for qutrits.
- **Noise models (both generic, both $d=3$ vs $d=2$ only):**
  - Generalized Pauli/depolarizing channel, single- and two-particle versions (Eqs. 30–34), applied **only after the CSUM/CNOT gate**. Quoted current hardware value: "values of $p_2$ for qutrits are approximately 0.13."
  - Amplitude damping (Eqs. 35–38), applied after all $R^x,R^y$ rotations (qutrits) / all logic ops (qubits). Qutrit Kraus operators use $e^{-t/T_1}$ for $|1\rangle$ and $e^{-2t/T_1}$ for $|2\rangle$ — i.e. **the $|2\rangle\to|0\rangle$ rate is fixed at twice the $|1\rangle\to|0\rangle$ rate by fiat**: "While the $T_1$ time for the $|1\rangle\to|0\rangle$ decay does not have to be one half the $T_1$ time for the $|2\rangle\to|0\rangle$ decay this is chosen to simplify the parameter space search." This is the crux of main.tex's "no per-level-calibrated channel" claim: the channel *has* per-level structure but that structure is a stipulated 2:1 ratio, not calibrated to measurements. (The paper does separately note, citing transmon refs, that "higher energy states decay faster by 25 to 50%" — a number it does not then use in the channel.)
- **Headline results:** for the same mass-determination error, "the qutrit simulations can tolerate **10 to 100x larger gate noise** than a qubit simulations." Under Pauli decoherence alone, $\delta E_{fft}/m \propto p_2$ with proportionality constant $\sim 200$ for qubits and $\sim 4$ for qutrits; required $p_2$ values are $O(10^2)$ larger for qutrits (Table IV: 20%/10%/5% accuracy needs $p_{2,2} = 4/2/1 \times10^{-4}$ vs $p_{2,3} = 8/4/1\times10^{-2}$). Under amplitude damping alone, CNOT times must be $<10^{-3}T_1$ but CSUM times only $<10^{-1}T_1$; "the qutrits $T_1$ can be 100 times greater than the qubit $T_1$ and the same precision can be achieved."
- Conclusion: 20% accuracy on the mass gap is plausible for near-future qutrits (entangling fidelity $\approx 0.99$) but "infeasible using qubits" (would need $>0.9995$ fidelity and gate times $\sim 1000\times$ shorter than $T_1$). 5% and 10% are "beyond the ability of current qutrit machines."
- **Caveats the author himself states:** single-qubit/qutrit gates are assumed noiseless and $O(1)$ in time — "there is a caveat on this scaling argument presented here; single qudit gates for qudits with a large number of states may not necessarily be noiseless or be functionally instantaneous" (flagged for $d\gtrsim20$, since rotation count scales $O(d^2)$). Cross-talk and spectator errors are excluded ("these noise requirements will be even more stringent" if included). Trotter step fixed at $\delta t=0.235$; $N_{Trotter}\in\{40,80,200\}$ mapping to 20%/10%/5% FFT resolution. Qubit sims via QISKit density-matrix simulator; qutrit sims via a bespoke numpy density-matrix implementation.
- **Dimension scope:** qutrits only. The only forward-looking statement is "While the work that follows uses qutrits, the same methodology can be applied to higher dimensional operators as well" — a methodological remark, not a study of $d>3$. No $d=5$, no prime-dimension comparison anywhere.

**Judge verification questions:**
1. Is main.tex's "$d=3$ only" characterization accurate given that Gustafson notes the methodology extends to higher $d$ but never runs it? (The paper's every number is $d=3$ vs $d=2$.)
2. Is "encoding capacity" the right one-word summary of Gustafson's qutrit advantage, as opposed to Gokhale's ancilla advantage? Check that main.tex does not attribute an *ancilla*-based mechanism to Gustafson — his advantage is the native 3-state local Hilbert space plus avoidance of the unphysical $|11\rangle_2$ state and of SWAP-heavy compilation.
3. Is "no per-level-calibrated channel" fair? Gustafson's amplitude-damping channel *does* distinguish $|1\rangle$ and $|2\rangle$ (rates $e^{-t/T_1}$ vs $e^{-2t/T_1}$), but the 2:1 ratio is explicitly stipulated "to simplify the parameter space search," not calibrated to measured per-level $T_1$. Does main.tex's phrasing draw that distinction, or could a reader take it to mean the channel is level-blind?
4. Does main.tex anywhere quote Gustafson's magnitude (10–100× noise tolerance, or the $\sim200$ vs $\sim4$ proportionality constants, or the 20% feasibility verdict)? If so, are the numbers and their conditions (single-qudit gates assumed noiseless, no cross-talk, 4 sites, 3-state truncation, mass gap only) reproduced accurately?
5. Gustafson's comparison is against a *2-qubit* encoding of one qutrit ($D=4$ vs $D=3$), not a matched-Hilbert-space comparison. Does main.tex's use of this reference respect its own "matched control dimension" fairness standard, or at least avoid implying Gustafson controlled for it?

---

---

## `gustafson2025synthesis` — Synthesis of single qutrit circuits from Clifford+R (Gustafson, Lamm, Liu, Murairi, Zhu, 2025)

**Full citation:** E. J. Gustafson, H. Lamm, D. Liu, E. M. Murairi, S. Zhu, "Synthesis of single qutrit circuits from Clifford+R," *Phys. Rev. A* **112**, 062414 (2025), doi:10.1103/98q1-3yv8; arXiv:2503.20203.
**Source:** arXiv:2503.20203v1 (26 Mar 2025), FERMILAB-PUB-25-0002-SQMS-T, PDF: `gustafson-2025-single-qutrit-clifford-r-synthesis.pdf` (12 pp., read in full through Sec. VII)

**Cited in main.tex:**
- *Introduction*: "...violated whenever qudit gates are compiled by two-level decomposition~\cite{pavlidis2021,gustafson2025synthesis}" — i.e. cited as an instance of the regime where the native-gate-cost requirement fails.
- *Introduction*: "versus **35--69\% more non-Clifford gates** for single-qutrit synthesis from a fault-tolerant gate set~\cite{gustafson2025synthesis}."
- *The cost condition*: "the genuine failure mode remains the absence of a native entangler (\texttt{pavlidis})... which is precisely the regime of synthesis-based compilation~\cite{gustafson2025synthesis,venturelli2025}."

**What the paper actually shows (full-text, not abstract-level):**
- Two deterministic algorithms approximating **diagonal single-qutrit** rotations $R^Z_{(0,1)}(\theta)=\mathrm{Diag}(e^{-i\theta/2},e^{i\theta/2},1)$ over the metaplectic set $(C+R)_3$, generated by qutrit Hadamard $H$, $S=\mathrm{Diag}(1,\omega,1)$, and $R=\mathrm{Diag}(1,1,-1)$. Cost metric: $N_R$, the R-gate (non-Clifford) count. Frobenius norm throughout.
- **Measured scalings (Sec. VI, the source of the 35%/69%):**
  - Exhaustive search: $N_R^E(\varepsilon) = 2.193(11) + 8.621(7)\log_{10}(1/\varepsilon) = 2.193(11)+4.113(3)\log_3(1/\varepsilon)$; classical time complexity $O(\varepsilon^{-4.4})$; fit from 100 random angles in $(-\pi/2,\pi/2)$ at 10 precisions $\varepsilon\in\{1,0.5,0.25,0.1,\dots,10^{-3}\}$.
  - Householder search: $N_R^H(\varepsilon) = 3.20(13) + 10.77(3)\log_{10}(1/\varepsilon) = 3.20(13)+5.139(14)\log_3(1/\varepsilon)$; complexity $O(\varepsilon^{-0.42})$; 100 angles at 10 precisions $\varepsilon\in\{1,10^{-1},\dots,10^{-9}\}$ plus 36 angles at $10^{-10}$; contraction factor $c=0.35$.
- **The 35%/69% comparison and its exact baseline** (Sec. VI, final paragraph): the qutrit costs are compared "to that of implementing the same unitary on **two qubits**." Construction: for general two-qubit $SU(4)$ circuits 15 single-qubit rotations are required; "Restricting to the single-qutrit subspace of $SU(3)$, dimensional analysis bounds the cost as at least **10** $R^\alpha(\theta)$." Using the Ross–Selinger/repeat-until-success average $N_R^{RUS} = 9.2 + 3.817\log_{10}(1/\varepsilon)$ per $R_Z$, the two-qubit estimate is $10\,N^{RUS}$. Comparing gives "an overhead factor as $\varepsilon\to0$ of **1.35 and 1.69** respectively."
- **Critical qualifications on 35%/69% that a citing paper can misrepresent by omission:**
  - They are **asymptotic** ($\varepsilon\to0$) ratios of the *leading log coefficients*. At a fiducial $\varepsilon=10^{-10}$ the paper states "these factors **reduce to 1.12 and 1.40**" — i.e. 12% and 40%, not 35% and 69%, at a realistic finite precision.
  - 1.35 corresponds to the exhaustive algorithm, 1.69 to the Householder algorithm; they are two different algorithms, not a range from one.
  - Both figures are for **diagonal** rotations. For an arbitrary single-qutrit $SU(3)$ gate "these results should be multiplied by 6."
  - The two-qubit baseline is an *estimate* built from a dimensional-analysis lower bound (≥10 rotations), not a measured or optimal two-qubit synthesis.
  - The measured prefactor 10.77 is "close to the lower bound of 10.27" from Eq. (6) ($N_G = 10.27\log_{10}(1/\varepsilon)-2.16$ for $d=3$); the corresponding $d=2$ bound is $N_G = 9.97\log_{10}(1/\varepsilon)-5.65$ (Eq. 5). So even at the information-theoretic lower-bound level, the qutrit/qubit ratio is only $\approx 10.27/9.97 \approx 1.03$ — the 1.35/1.69 gap is largely algorithmic, not fundamental.
- **The authors' own framing is positive toward qutrits**, not negative: abstract — "Such initial results are encouraging for using the R gate as the non-transversal gate for qutrit-based computation"; conclusion — "These results open up the feasibility of using fault-tolerant qutrits for quantum simulations," with several stated routes to improvement (repeat-until-success, broader subclasses of efficiently synthesizable gates, other groups $(C+D)_3$ or $(C+T)_3$, larger transversal groups).
- **Scope:** single-qutrit gates only. No two-qutrit/entangling-gate synthesis, no noise model, no algorithm-level simulation, no hardware. Note $(C+R)_3$ is "strictly a subset of $(C+T)_3$."
- Relevance to the "no native entangler / two-level decomposition" claim: the paper is about fault-tolerant *synthesis* of single-qutrit rotations from a discrete gate set — it is an example of compilation overhead in a fault-tolerant setting, but it is **not** literally a two-level (qubit-pair) decomposition of a qudit gate in the Pavlidis sense, and it does not compile an entangler. main.tex's Cost-condition sentence pairs it with `pavlidis2021` and `venturelli2025` under "synthesis-based compilation."

**Judge verification questions:**
1. Does main.tex's "35--69\% more non-Clifford gates" reproduce the paper's numbers correctly *and* state (or at least not contradict) that these are **asymptotic $\varepsilon\to0$** figures for **diagonal** single-qutrit gates, which fall to **12% and 40%** at $\varepsilon=10^{-10}$?
2. Does main.tex present 35–69% as a *range* (which reads like an interval over conditions) when the paper reports two point values from two different algorithms (1.35 exhaustive, 1.69 Householder)?
3. Is the baseline correctly identified as "the same unitary on two qubits" using an estimated $10\times$ Ross–Selinger RUS cost — and does main.tex avoid implying it is a measured optimal two-qubit synthesis or an entangling-gate comparison?
4. main.tex cites this alongside `pavlidis2021` for "qudit gates compiled by two-level decomposition" and "the absence of a native entangler." Is that an accurate placement, given that Gustafson et al. synthesize **single-qutrit** gates from a fault-tolerant discrete set and never treat an entangler? Does main.tex's sentence structure make clear which reference supports which failure mode?
5. The paper's own conclusion is encouraging for fault-tolerant qutrits. Does main.tex's use of it as evidence on the "versus" side of a split verdict fairly represent the authors' framing, or does it read as if the authors concluded against qutrits?

---

---

## `hardy2008` — An Introduction to the Theory of Numbers, 6th ed. (Hardy & Wright, 2008)

**Full citation:** G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed. (Oxford University Press, 2008), revised by D. R. Heath-Brown and J. H. Silverman.
**Source:** Textbook; no arXiv/DOI. PDF: **not available** — no full text was consulted. The assessment below rests on standard, well-established content of this textbook; **specific theorem numbers could not be verified and are flagged as such.**

**Cited in main.tex:**
- *subsection "Why the decoder gains tolerance with size"* (claim A): "Continued-fraction recovery succeeds for any outcome $y$ whose phase $y/D$ lies within $1/(2r^2)$ of some $s/r$---**the classical convergent guarantee**~\cite{hardy2008,shor1997}."
- *subsection "Why the decoder gains tolerance with size"* (claim B): "for a reduced fraction $p/q$, the phases with $p/q$ among their convergents form the open interval between the **Stern--Brocot mediants** $(p+p')/(q+q')$ and $(2p-p')/(2q-q')$, where $p'/q'$ is the penultimate convergent of $p/q$---**a classical fact of continued-fraction theory**~\cite{khinchin1964,hardy2008}."
- *section "The decoder acceptance lemma"* (claim C): "for $y$ within $1/(2\tilde r^{2})$ of a peak $s/r$, the convergent guarantee~\cite{hardy2008} yields the reduced fraction $(s/g)/(r/g)$ with $g=\gcd(s,r)$, whose denominator $\tilde r=r/g$ \emph{divides} $r$~\cite{shor1997,ekera2024}."

**What the source actually contains (bibliographic/domain knowledge; no full text read):**
- **Claim A/C — the convergent guarantee (Legendre's theorem).** This is genuinely in Hardy & Wright, Chapter X ("Continued fractions"), in the section on Legendre's theorem: *if $p/q$ is in lowest terms with $q\ge1$ and $|x - p/q| < 1/(2q^2)$, then $p/q$ is a convergent of the continued-fraction expansion of $x$.* I am confident of the mathematical content and of its presence in Ch. X; I could **not** verify the theorem number (commonly cited as Theorem 184, §10.10, but unverified here). Standard supporting results in the same chapter: convergents $p_n/q_n$ are in lowest terms; $|x - p_n/q_n| < 1/(q_nq_{n+1}) \le 1/q_n^2$; the best-approximation property.
- **Important precision point for claim A:** the theorem's hypothesis is on the **reduced** fraction. If $\gcd(s,r)=g>1$, then $|y/D - s/r| < 1/(2r^2)$ implies the same bound with the *smaller* denominator $\tilde r = r/g$ (since $1/(2r^2) < 1/(2\tilde r^2)$), so the theorem returns $(s/g)/(r/g)$ — denominator $\tilde r$, **not** $r$. main.tex's claim C states exactly this, so claims A and C are consistent with each other only if "succeeds" in claim A is read as "the reduced fraction is recovered as a convergent," not "the order $r$ is recovered." The gcd lift is a separate classical step, which main.tex attributes to `shor1997`/`ekera2024`.
- **Claim B — the mediant interval.** Farey series and the mediant $(p+p')/(q+q')$ are standard Hardy & Wright material, but in **Chapter III (Farey series and a theorem of Minkowski)**, not the continued-fraction chapter. The *specific* statement main.tex makes — that the set of $x$ having a given reduced $p/q$ among its convergents is the open interval between $(p+p')/(q+q')$ and $(2p-p')/(2q-q')$, with $p'/q'$ the penultimate convergent — is **not, to my knowledge, a numbered theorem in Hardy & Wright**. It is a derivable classical consequence of the CF machinery (the interval of reals whose CF expansion begins with a given finite prefix, expressed via the last two convergents), and main.tex's own wording ("a classical fact of continued-fraction theory") frames it as folklore attributed jointly to `khinchin1964` and `hardy2008` rather than as a literal quotation. Khinchin's *Continued Fractions* is the closer of the two sources for prefix-interval statements. **This should be treated as a general-reference citation, not a pinpoint citation, and flagged as such.**
- **A real mathematical subtlety in claim B that the textbook citation does not resolve:** every rational $p/q$ has **two** continued-fraction expansions ($[a_0;\dots,a_n]$ with $a_n\ge2$, and $[a_0;\dots,a_n-1,1]$), which give **two different** penultimate convergents $p'/q'$. The interval endpoints $(p+p')/(q+q')$ and $(2p-p')/(2q-q')$ therefore depend on a convention that must be fixed. main.tex's surrounding text does gesture at a convention ("...recovery of the standard analyses"), so the judge should check that the convention is stated explicitly and that the asserted endpoints match it. Also note the asymmetry of the two endpoint formulas — one is a mediant with $p'/q'$, the other is a mediant-like combination $(2p-p')/(2q-q')$ (equivalently the mediant of $p/q$ with the reflection of $p'/q'$); a reader should confirm which side each bounds.
- **What the textbook does not contain, at all:** anything about quantum computing, Shor's algorithm, order finding, register dimension $D$, acceptance sets, or decoder tolerance. Any claim in main.tex about *acceptance-set size*, *scaling in $D=d^m$*, or the number of admissible convergent denominators (e.g. "at $N{=}55$, $r{=}5$ the chain $5,10,25$ is realizable, $25=2\cdot10+5$") is main.tex's own work and must not be attributed to `hardy2008`.
- Bibliographic check: the 6th edition was published by OUP in 2008 (paperback ISBN 978-0-19-921986-5), revised by Heath-Brown and Silverman with a foreword by Andrew Wiles. The bib entry (author, title, edition, publisher, year) is correct as given; no page/theorem locator is provided, which is a weakness for the pinpoint claims A and C.

**Judge verification questions:**
1. Does main.tex's claim A sentence ("Continued-fraction recovery **succeeds** for any outcome $y$ whose phase lies within $1/(2r^2)$ of some $s/r$") overstate the classical theorem? The theorem guarantees only that the **reduced** fraction is a convergent; when $\gcd(s,r)>1$ the recovered denominator is $r/g$, and recovering $r$ itself needs the extra gcd/multiple search that main.tex describes later. Are the two passages mutually consistent, and is the sufficient-condition framing preserved (the criterion is sufficient, not necessary)?
2. Is claim B — the Stern–Brocot mediant interval $\big((p+p')/(q+q'),\,(2p-p')/(2q-q')\big)$ with $p'/q'$ the penultimate convergent — actually stated in Hardy & Wright, or is it folklore that main.tex is citing loosely? If the latter, does main.tex's hedge ("a classical fact of continued-fraction theory") make that clear, and is `khinchin1964` the load-bearing citation?
3. Does main.tex fix a convention for the (non-unique) penultimate convergent $p'/q'$ of a rational $p/q$? Without it, claim B's endpoints are ambiguous.
4. Does main.tex confine `hardy2008` to the pure number-theoretic facts (Legendre's criterion, mediants) and keep its own quantum-specific results — acceptance-set size $\sim D/r^2$, growth linear in $D=d^m$, the 42 (instance, $D$) bit-identical verification, the $N=55$ chain $5,10,25$ — clearly attributed to itself and to `shor1997`/`ekera2024`?
5. Given that no page or theorem number is supplied for a 600+ page textbook cited three times for two distinct pinpoint facts, should the citation carry a locator (e.g. Ch. X / §10.10 for Legendre's criterion, Ch. III for Farey mediants)?

---

**Batch note:** 5 of 6 references were audited against the full extracted text of the PDF in `papers/`. `hardy2008` has no PDF in the repository (`pdf_file: null`); its section rests on bibliographic and domain knowledge only, with theorem numbers explicitly unverified — flagged inline above.

---

## `hrmo2023` — Native qudit entanglement in a trapped ion quantum processor (Hrmo, Wilhelm, Gerster, van Mourik, Huber, Blatt, Schindler, Monz, Ringbauer, 2023)

**Full citation:** P. Hrmo, B. Wilhelm, L. Gerster, M. W. van Mourik, M. Huber, R. Blatt, P. Schindler, T. Monz, M. Ringbauer, "Native qudit entanglement in a trapped ion quantum processor," *Nat. Commun.* **14**, 2242 (2023); arXiv:2206.04104.
**Source:** arXiv:2206.04104, Nat. Commun. 14, 2242 (2023), PDF: `hrmo-2023-native-qudit-entanglement-trapped-ion.pdf` (9 pp incl. appendix; read in full)

**Cited in main.tex:**
- *Introduction*: "The native-gate cost requirement (one entangling layer regardless of $d$) is met by current trapped-ion qudit gates — the single-application light-shift entangler of Hrmo et al. realizes it **up to $d=5$**"; and "the ion gate's error grows **$16\times$ from $d=2$** [to $d=5$]".
- *Noise channels*: "ion two-qudit entangling gates at **$1.3\times10^{-2}$–$6.3\times10^{-2}$ for $d=3$–$5$** (native light-shift)"; and ion entangler durations are orders of magnitude longer than the transmon CZ$^\dagger$'s 580 ns.
- *Gate-cost models*: Hrmo's "single-application light-shift gate" is one of the two published exemplars justifying the `uniform` cost model — "native qudit entangler, **one layer regardless of $d$**".
- *The cost condition*: "measured qudit entangling gates **stop at $d=5$**~\cite{hrmo2023}", so all $d=7$ cost models are extrapolations beyond measurement.
- *Robustness*: "The **only** native two-qudit entangling gate characterized across $d=2,3,5$ **on one apparatus** — the single-application light-shift gate of Hrmo et al., **fidelity $99.6(1)/98.7(2)/93.7(3)\%$ at $d=2/3/5$**"; a table row set is evaluated "at the measured native qudit gate of Ref.~\cite{hrmo2023}", with "$d=4$ rows from `results/hrmo_d4.json`".
- *Discussion*: strength band "$5\times10^{-3}$–$2\times10^{-2}$" is said to be what "demonstrated two-qudit entangling gates imply", glossed as "native gate fidelities of **$93.7$–$98.7\%$ at $d=3$–$5$**"; and "$d=5$ entangling gates **exist today only on trapped ions**".

**What the paper actually shows (full-text, not abstract-level):**
- **The headline fidelities (p. 5, main text, first sentence):** "We apply this procedure for $d = 2, 3, 4, 5$ and obtain fidelities of **99.6(1)%, 98.7(2)%, 97.0(2)%, 93.7(3)%** respectively." These are the numbers main.tex quotes; the $d=4$ value (97.0(2)%, infidelity $3.0\times10^{-2}$) is measured and reported, so a `hrmo_d4` row is grounded in the paper.
- **Implied infidelities:** $d=2$: $4.0\times10^{-3}$; $d=3$: $1.3\times10^{-2}$; $d=4$: $3.0\times10^{-2}$; $d=5$: $6.3\times10^{-2}$. Ratio $d=5$ to $d=2$ = $6.3\times10^{-2}/4.0\times10^{-3} = 15.75$, i.e. "$16\times$" to two significant figures.
- **Independent confirmation from the error model (Table A1, p. 8):** simulated total infidelity from independently measured noise parameters is $4.2\times10^{-3}$ ($d=2$), $1.3\times10^{-2}$ ($d=3$), $2.7\times10^{-2}$ ($d=4$), $6.2\times10^{-2}$ ($d=5$) — consistent with the measured values.
- **What "single application" actually means (p. 2–3):** the qudit gate is $G = (X_d U_{\rm LS}(t_{\rm g}))^d$ — i.e. **$d$ interleaved light-shift pulses plus $d$ cyclic-permutation local gates**. It is one *gate/entangling operation* in the circuit sense (and the "calibration overhead ... is independent of the dimension"), but its pulse content and duration grow with $d$. A single LS pulse has $t_{\rm g} \sim 35\,\mu$s (p. 3), so a $d=5$ gate involves $\sim5\times35\,\mu$s of LS pulses plus local operations — three orders of magnitude longer than a 580 ns transmon CZ$^\dagger$.
- **The authors explicitly attribute the error growth to the local-pulse count (p. 5):** "the measured gate performance degrades **quadratically** with dimension ... the total gate error is dominated by the errors of the local pulses, since their number **increases quadratically** with qudit dimension, whereas the number of entangling pulses increases linearly." So the paper's own mechanism says per-gate error is *not* $d$-independent even though the layer count is.
- **Maximal-entanglement caveat (abstract + p. 4):** "direct application of the gate can generate **maximal qudit entanglement up to dimension 4**". At $d=5$ a single application yields the *non-maximally* entangled $|\Psi_5\rangle = (3|00\rangle + 2\sum_{j=1}^{4}|jj\rangle)/5$; "For higher-dimensional qudits, **multiple applications of the gate are required to achieve maximal entanglement**." The $d=5$ target state in Table A2 is correspondingly $|\psi_T\rangle = 0.6|00\rangle + 0.4(|11\rangle+|22\rangle+|33\rangle+|44\rangle)$, not the maximally entangled state.
- **Fidelity extraction method and its caveats (p. 4):** fidelities are SPAM-corrected, obtained by inserting up to 9 applications of $G(\theta)$ between preparation and its conjugate and fitting an **exponential decay**; error bars are one standard deviation in the fit parameters. The authors warn: "Such repeated gate applications, however, are also sensitive to the presence of **non-Markovian** noise in our system that leads to deviations from purely exponential decay. The extracted fidelities should thus be interpreted as an estimate for the **SPAM corrected average gate performance over a sequence of length $n$**." This is neither randomized benchmarking nor a process-fidelity measurement.
- **Table A2 (p. 9) reports separate single-gate *state* fidelities:** 0.989±0.005, 0.978±0.012, 0.947±0.012, 0.884±0.012 for $d=2,3,4,5$. These are lower than the extracted gate fidelities and are a different quantity — a citing paper must not mix the two.
- **Platform/scale:** two $^{40}$Ca$^+$ ions in a segmented surface Paul trap at $\sim$35 K; qudit encoded in $S_{1/2,m_j=-1/2}$ plus $D_{5/2}$ Zeeman sub-levels; $d\le 5$ only. No $d=7$ data of any kind.
- **Dominant error source shifts with $d$ (p. 5):** at $d=2$ the gate fidelity is limited by motional coherence; "for $d = 4, 5$ the dominant error source becomes **slow frequency noise that causes dephasing of the local operations**" — Table A1 shows "Local operation frequency noise" at $3.3\times10^{-2}$ for $d=5$, over half the total $6.2\times10^{-2}$. The authors state this is technical and "can be significantly improved if technical noise sources such as magnetic field noise ... or Rabi frequency fluctuations can be suppressed."
- **Concurrence (p. 5, Fig. 5):** concurrence exceeds the max qubit value for all $d>2$, but "for the ququart ($d=4$) and ququint ($d=5$) we **do not exceed the maximum possible concurrence for qutrits**".

**Judge verification questions:**
- Does main.tex's "$1.3\times10^{-2}$–$6.3\times10^{-2}$ for $d=3$–$5$" and "$99.6(1)/98.7(2)/93.7(3)\%$ at $d=2/3/5$" match Hrmo p. 5 exactly (it should: 99.6/98.7/97.0/93.7% for $d=2/3/4/5$), and is the "$16\times$" growth from $d=2$ to $d=5$ correctly $15.75\times$?
- main.tex uses Hrmo as an exemplar of a `uniform` cost model — "one layer regardless of $d$". Does main.tex anywhere acknowledge that (a) the gate is internally $d$ LS pulses + $d$ local permutations, so its **duration and error grow with $d$** (quadratically, per Hrmo p. 5), and (b) a **single application generates maximal entanglement only up to $d=4$**, with $d=5$ requiring multiple applications? Omitting (b) while writing "realizes it up to $d=5$" would overstate the reference.
- Does main.tex represent these as *gate* fidelities (correct) rather than the *state* fidelities of Table A2 (0.989/0.978/0.947/0.884)? And does it note that they are exponential-decay fits the authors themselves flag as non-Markovian-sensitive rather than RB/process fidelities?
- main.tex's Discussion band "$5\times10^{-3}$–$2\times10^{-2}$" is attributed to "demonstrated two-qudit entangling gates ... native gate fidelities of $93.7$–$98.7\%$ at $d=3$–$5$". The raw infidelities are $1.3\times10^{-2}$ and $6.3\times10^{-2}$, both outside that band — does main.tex state and correctly apply a conversion (e.g. dividing by the $\Delta(d)=1-1/d^2$ damage factor and/or by carrier count) that maps them into $5\times10^{-3}$–$2\times10^{-2}$?
- Is "measured qudit entangling gates stop at $d=5$" and "$d=5$ entangling gates exist today only on trapped ions" consistent with the reference (which caps at $d=5$ and is trapped-ion)? Note the paper itself makes no cross-platform exclusivity claim — that is main.tex's own assertion.

---

---

## `jankovic2024` — Noisy qudit vs multiple qubits: conditions on gate efficiency for enhancing fidelity (Janković, Hartmann, Ruben, Hervieux, 2024)

**Full citation:** D. Janković, J.-G. Hartmann, M. Ruben, P.-A. Hervieux, "Noisy qudit vs multiple qubits: conditions on gate efficiency for enhancing fidelity," *npj Quantum Inf.* **10**, 59 (2024); arXiv:2302.04543.
**Source:** arXiv:2302.04543v4 (27 May 2025), npj QI 10, 59 (2024), PDF: `jankovic-2023-noisy-qudit-vs-multiple-qubits.pdf` (13 pp incl. appendices; read in full via text extraction)

**Cited in main.tex:**
- *Introduction*: "An independent analytic gate-level criterion~\cite{jankovic2024}, which we reproduce numerically to $4\times10^{-4}$ and apply to our circuits under the identification of layer-count ratios with gate-efficiency ratios ... is consistent with our algorithm-level outcomes in four of six cost-model/dimension cases".
- *Introduction*: prior work is differentiated as "the gate-level criterion of Janković et al. (**no algorithms, no scaling**)".
- *The cost condition*: "Janković et al. derive, **by linear response over Haar-random gates under pure dephasing**, the critical gate-efficiency ratio $(d^2-1)/(3\log_2 d)$ a single qudit must clear to beat a multi-qubit register **at matched Hilbert dimension** — **$1.68$ at $d=3$, $3.45$ at $d=5$, and $5.70$ at $d=7$**. Their criterion is stated for ratios of gate *times* in units of the dec[oherence time]".
- *Robustness*: "we reproduce **the three central equations** of Ref.~\cite{jankovic2024} — qudit and multi-qubit **process infidelities** and the critical curve $(d^2-1)/(3\log_2 d)$ — from our superoperator code with no analytics of our own, to a **worst relative error of $4.1\times10^{-4}$ over $d=2$–$64$**, with the residual identified as their **first-order truncation** (it tracks the infidelity itself)."
- *Methods*: "The external reproduction of Ref.~\cite{jankovic2024} (Sec. Robustness) runs **separately from the test suite**."

**What the paper actually shows (full-text, not abstract-level):**
- **The critical curve is Eq. (22), stated exactly as main.tex quotes it:** $\dfrac{t_{b,n}/T_{2,b}}{t_d/T_{2,d}} > \dfrac{c_d}{c_{b,n}} = \dfrac{d^2-1}{3\log_2 d} = \dfrac{4^n-1}{3n}$. Numeric evaluation: $d=3 \to 8/(3\log_2 3)=1.6825$; $d=5 \to 24/(3\log_2 5)=3.4454$; $d=7 \to 48/(3\log_2 7)=5.6994$. main.tex's 1.68 / 3.45 / 5.70 are exact to the digits shown.
- **The figure of merit is explicitly gate time in units of decoherence time:** "the figure of merit $\tau_k = t_k/T_{2,k} = \gamma_k t_k/2$" (Fig. 8 discussion). main.tex's "ratios of gate *times* in units of the decoherence time" is a faithful restatement.
- **Where the Haar average actually lives.** The AGI is Nielsen's average gate fidelity, averaged over **input states** under the Fubini–Study/Haar measure on pure states (Eq. (8), and App. A 4 which does the Weingarten integral over $\int d\rho$). The analytic result is **gate-independent** — derived once and valid for arbitrary $U$; there is no averaging over gates in the derivation. **Haar-random gates (5000 drawn from the CUE via the Bristol package, with GRAPE-optimized pulses) appear only in the numerical gate-dependence check** of Fig. 5. So "linear response over Haar-random gates" conflates the state-average with the numerical gate ensemble.
- **The three equations main.tex claims to reproduce all exist:** qudit AGI Eq. (14) $\mathcal{E}_d(E_z)=\frac{\gamma t}{12}d(d-1)$; $n$-qubit AGI Eq. (20) $\mathcal{E}_{b,n}(E_z)=\frac{\gamma t}{4}\frac{n2^n}{2^n+1}=\frac{\gamma t\log_2(d)\,d}{4(d+1)}$; and the **process/entanglement** infidelity forms Eq. (30) $\mathcal{E}^{(p)}_d(E_z)=\frac{\gamma t}{12}(d^2-1)$ and Eq. (31) $\mathcal{E}^{(p)}_{b,n}(E_z)=\frac{\gamma t}{4}n$, related by $D\mathcal{E}^{(p)}=(D+1)\mathcal{E}$. main.tex's phrase "qudit and multi-qubit **process** infidelities" maps onto Eqs. (30)–(31); the ratio of those two *is* the critical curve.
- **Scope limit 1 — pure dephasing only.** The critical curve is derived for the single collapse operator $L=J_z$ (qudit) / $S_z$ on each qubit (register). Other channels are computed (Fig. 6: bit-flip $\frac{1}{12}d(d-1)$·... , amplitude damping $\frac16 d(d-1)$, depolarizing $\frac14 d(d-1)$ — 2× and 3× the dephasing gradient) but **no critical curve is derived for them**.
- **Scope limit 2 — first order in $\gamma t$ only.** Validity range stated by the authors: "the AGI can only be considered gate-independent when $\gamma t \ll 1$ and $\gamma t \ll 1/\|H\|t$"; and for linearity, "$\gamma t \ll 1$ and $\ll 1/d^2$" (the $O((\gamma t)^2)$ prefactor scales as $d^4$). "the range of $\gamma t$ values for which the AGI can be treated linearly **diminishes with increasing qudit dimension**." This directly supports main.tex's "residual identified as their first-order truncation".
- **Scope limit 3 — the matched register is $d=2^n$, i.e. $d$ a power of two.** Eq. (22) sets $n=\log_2 d$; Table I tabulates only $d=2,4,8,64$ (critical $\tau_b/\tau_d$ = 1, 2.5, 7, 227.5 — all reproduced exactly by the formula). **Evaluating the curve at $d=3,5,7$ means $n=\log_2 d$ is not an integer, so there is no literal $n$-qubit register of matched Hilbert dimension.** The paper never evaluates it at odd/prime $d$. main.tex's 1.68/3.45/5.70 are therefore off-lattice extrapolations of the formula, correct arithmetically but outside the setting the authors constructed.
- **"No algorithms, no scaling" — mostly accurate, with one qualification.** There is no algorithm, no circuit, no depth: the object of study is a *single* gate of duration $t$. However, the paper *does* generalize to $N$ qudits (Eq. (23) $\mathcal{E}_{d,N}=\frac{\gamma t}{12}\frac{Nd^N}{d^N+1}(d^2-1)$, Eq. (24) the same critical ratio for $N$ qudits vs $N\log_2 d$ qubits, Eq. (26) for per-qudit noise parameters) and briefly discusses how the advantage persists under scaling. So "no scaling" is true of *circuit-depth/algorithmic* scaling but not literally of system-size generalization.
- **Best-case-for-qubits framing:** "Considering any additional coupling mechanism to the environment arising from inter-qubit interactions would only further disadvantage the multi-qubit implementation. Our considerations then provide a **best-case scenario for comparable qubits**." A qudit-favourable conclusion drawn from this criterion is therefore conservative — relevant to main.tex's claim that "all misses [are] in the conservative direction".
- **Numerics:** QuTiP 4.7; single qudits $d\in[2,22]$ even, $\gamma t \in [0,10^{-4}]$, fit quality $1-R^2 < 10^{-5}$; $n$-qubit ensembles $n\in[1,7]$, $1-R^2<10^{-7}$; qudits modelled as ladder systems with one pulse per adjacent transition.
- **Platform table (Table II) caveat:** the paper's own hardware application uses $\gamma t\approx10^{-3}$ (trapped ions), $\approx10^{-2}$ (superconducting), $\approx10^{-4}$ (molecular nuclear spins); it concludes molecular-spin qudits up to $d\lesssim40$ could be advantageous. These are single-gate statements, not algorithm-level ones.

**Judge verification questions:**
- main.tex says the criterion is derived "by linear response **over Haar-random gates**". In the paper the analytic derivation is **gate-independent** with the Haar/Fubini–Study average taken over **input states**; Haar-random gates are only a numerical robustness check (Fig. 5, 5000 CUE gates). Is main.tex's phrasing a material mischaracterization of the derivation?
- Eq. (22) is constructed for a qudit of dimension $d$ vs $n=\log_2 d$ qubits, and the paper only tabulates $d=2,4,8,64$. Does main.tex flag that its quoted values at $d=3,5,7$ evaluate the formula where $\log_2 d$ is non-integral and no matched-dimension qubit register exists?
- Do the reproduced quantities match the paper's Eqs. (30), (31) and (22) — i.e. does main.tex correctly call Eqs. (30)/(31) *process* (entanglement) infidelities rather than average gate infidelities (Eqs. (14)/(20))? And is "$d=2$–$64$" within the paper's own simulated range ($d\in[2,22]$ for single qudits, $d=2^n$ up to $n=7$ i.e. 128 for registers)?
- Does main.tex acknowledge that the critical curve is derived **only for pure dephasing**, while main.tex's own channels include depolarizing and a calibrated anharmonic ladder — for which Fig. 6 shows gradients 2–3× larger and no critical curve is derived?
- Is main.tex's "first-order truncation ... tracks the infidelity itself" consistent with the paper's stated validity conditions $\gamma t \ll 1$ and $\gamma t \ll 1/d^2$?

---

---

## `keppens2025` — Qudit vs. qubit: Simulated performance of error correction codes in higher dimensions (Keppens, Eggerickx, Levajac, Simion, Sorée, 2025)

**Full citation:** J. Keppens, Q. Eggerickx, V. Levajac, G. Simion, B. Sorée, "Qudit vs. qubit: Simulated performance of error correction codes in higher dimensions," arXiv:2502.05992 (2025).
**Source:** arXiv:2502.05992v2 (5 Sep 2025), PDF: `keppens-2025-qudit-vs-qubit-error-correction.pdf` (14 pp; read in full via text extraction)

**Cited in main.tex:**
- *Introduction*: the paper's bare-circuit condition "does not transfer automatically to the error-correction layer, where a code has no problem instance to compress and **the dimension dependence can carry the opposite sign**~\cite{keppens2025}".
- *Introduction*: prior work differentiated as "the **code-level comparison** of Keppens et al., whose **opposite ordering** we reconcile explicitly: a code has no problem instance to compress, so it pays the per-carrier cost of dimension without the width-and-depth rebate".
- *Discussion*: "Keppens et al. find **slightly *worse* qudit logical error rates for the five-qudit code under the same noise convention we use**, and the two results are compatible: a code is five carriers and a fixed gate list at every $q$ — no problem instance to compress — so raising $q$ buys no width or depth while charging every carrier more."
- *Discussion*: "Fault-tolerant overhead is out of scope, and per Ref.~\cite{keppens2025} its **dimension-dependence may differ in sign**."

**What the paper actually shows (full-text, not abstract-level):**
- **Object of study:** the $[[5,1,3]]_q$ "perfect" five-qudit code — 5 data qudits + 4 ancillas (+1 optional flag qudit) — with a general encoding circuit valid for all prime $q$, simulated in Cirq with custom qudit gates. Dimensions $q = 2, 3, 5$ throughout, plus a **single** $q=7$ data point under depolarizing noise only.
- **The headline result main.tex leans on — Table I (circuit-level noise, BM decoder, level-by-level concatenation threshold estimate):**

  | $q$ | flag | $a$ | $b$ | threshold |
  |---|---|---|---|---|
  | 2 (qubit) | no | 36.7 | 1.264 | $1.21\times10^{-6}$ |
  | 2 (qubit) | yes | 766 | 1.873 | $4.95\times10^{-4}$ |
  | 3 (qutrit) | no | 58.7 | 1.288 | $7.22\times10^{-7}$ |
  | 3 (qutrit) | yes | 1116 | 1.870 | $3.24\times10^{-4}$ |
  | 5 (ququint) | no | 35.3 | 1.149 | $4.36\times10^{-11}$ |
  | 5 (ququint) | yes | 792 | 1.798 | $2.32\times10^{-4}$ |

  So **with the flag qudit, thresholds are monotonically worse with dimension**: $4.95\times10^{-4}$ (qubit) $>3.24\times10^{-4}$ (qutrit) $>2.32\times10^{-4}$ (ququint). Without the flag, the ququint is catastrophically worse ($4.36\times10^{-11}$). This supports main.tex's "slightly worse qudit logical error rates" — but "slightly" applies **only to the flag-qudit case**; without a flag the gap is five orders of magnitude.
- **The authors' own statement of the ordering (Sec. 5.3):** "The fact that the logical error rates for higher-dimensional qudits are **slightly worse than those for qubits is expected due to the nature of the noise models**." And the conclusion: "the thresholds for qutrits and ququints were **comparable** to those of qubits ... qudits remain a **viable and promising** platform." The paper's own framing is "comparable, order $10^{-4}$" (abstract), not "qudits lose".
- **The noise convention is the key checkable claim.** Eq. (13): $\rho \to \left(1 - p\frac{q^2-1}{q^2}\right)\rho + \frac{p}{q^2}\sum_{i=1}^{q^2-1}P_i\rho P_i^\dagger$. The probability of *no* error is $1-p(q^2-1)/q^2 = 1 - p(1-1/q^2)$ — i.e. the damage per carrier is $p\cdot(1-1/q^2)$, exactly the $\Delta(d)=1-1/d^2$ identity main.tex uses elsewhere. Two-qudit version Eq. (14) uses $q^4$ normalization over $(q^2-1)^2 + 2(q^2-1)$ Pauli terms. Measurement error Eq. (15) is a bit-flip $X_q$ with probability $p_m$. The authors explicitly note "the noise channel (13) is **inherently dependent on the system's dimensionality**" and, in the conclusion, "despite being subject to an **error model that scales with dimension**".
- **A counter-signal main.tex does not cite:** under the *standard depolarization* model with the **MWPM** decoder (Fig. 7), "the decoder initially shows **lower** logical error rates for higher-dimensional codes than for the qubit version", because hyperedge errors in higher dimensions decompose into fewer equally weighted paths (qubit graph: 3 configurations; qutrit graph: 2). So the qudit-is-worse ordering is a property of the **BM decoder under circuit-level noise**, not a universal finding of the paper.
- **Threshold-estimation caveat (Sec. 5.4):** the five-qudit code "does not exhibit a natural pathway for scalability"; distance is increased only by concatenation. "The computational cost of such large simulations with qudits is far beyond what is currently computationally feasible." Thresholds are therefore obtained by **fitting a power law $P_L(p_s) = a p_s^b$ to level-1 data and recursively extrapolating** to $l=2,3$, then intersecting the curves — **not** by simulating distance-5 and distance-7 codes. The exponent $b$ is a free fit parameter (fitted values 1.15–1.87), not fixed at the theoretical 2.
- **Statistics:** depolarizing model, $q=2,3,5$: 400,000 samples per point; $q=7$: **only 5000 samples**, "solely used to provide some confirmation of expected trends". Circuit-level: 50 independent simulations of $A/p_s$ samples each, with $A=20$ (qubits), 5 (qutrits), 2 or 1 (ququints) — i.e. **an order of magnitude fewer samples for ququints than qubits**.
- **Internal inconsistency worth noting:** Table I lists the qutrit-with-flag threshold as $3.24\times10^{-4}$, while the Fig. 11 caption/legend reads "Threshold: $p_s = 3.29\times10^{-4}$". Body text uses $3.24\times10^{-4}\pm6.5\times10^{-6}$.
- **Mechanism the authors give for the qudit penalty:** twofold — (i) the depolarizing channel is intrinsically dimension-dependent, and (ii) "as the dimension of the qudit increases, the likelihood that errors **cancel each other out** diminishes"; plus higher-dimensional qudits "are **more susceptible to hook errors**" (the flag qudit narrows the qubit–qudit gap).

**Judge verification questions:**
- Does main.tex's depolarizing channel definition match Keppens Eq. (13) — specifically the $(1-1/d^2)$ no-error weighting — so that "under the same noise convention we use" is literally true? If main.tex uses a different normalization (e.g. uniform-over-$d^2$ or a per-level ladder), the claim of a shared convention fails.
- main.tex says Keppens finds "slightly worse qudit logical error rates". Does main.tex disclose that this holds for the **flag-qudit / circuit-level-noise / BM-decoder** configuration, and that (a) **without** a flag the ququint is $\sim5$ orders of magnitude worse, and (b) under standard depolarizing noise with the **MWPM** decoder qudits were *better* than qubits?
- Does main.tex characterize the thresholds as **simulated** or as **extrapolated**? The paper obtains them by power-law fit plus recursive concatenation projection, never simulating $l=2,3$ directly.
- Is main.tex's "dimension dependence can carry the **opposite sign**" a fair summary given the paper's own conclusion is "**comparable** error thresholds of the order of $10^{-4}$ ... qudits remain a viable and promising platform"? The signs do differ (qubit threshold highest), but the paper does not present this as a verdict against qudits.
- Does main.tex's reconciliation argument ("a code has no problem instance to compress ... raising $q$ buys no width or depth") correctly describe the Keppens setup — 5 data qudits and a fixed stabilizer/gate list at every prime $q$? (It does: the encoding circuit of Fig. 1 and syndrome circuit of Fig. 2 are the *same* circuits at every $q$.)

---

---

## `khinchin1964` — Continued Fractions (Khinchin, 1964)

**Full citation:** A. Ya. Khinchin, *Continued Fractions*, University of Chicago Press, Chicago, 1964.
**Source:** Book (English translation of the 3rd Russian edition), PDF: **not available**

> **No full text was consulted for this entry.** The assessment below rests on the standard, well-established content of Khinchin's *Continued Fractions* and on independent mathematical verification of the two claims; a judge should treat page/theorem-number pointers as indicative rather than checked against the physical book.

**Cited in main.tex:**
- *Why the decoder gains tolerance with size*: "for a reduced fraction $p/q$, the phases with $p/q$ among their convergents form the **open interval between the Stern–Brocot mediants $(p+p')/(q+q')$ and $(2p-p')/(2q-q')$**, where $p'/q'$ is the penultimate convergent of $p/q$ — **a classical fact of continued-fraction theory**~\cite{khinchin1964,hardy2008}."
- *Why the decoder gains tolerance with size*: "summed over **all** denominators $q\le Q$ the weight $\mu$ reproduces the **almost-everywhere count $(12\ln 2/\pi^2)\ln Q$ of convergent denominators below $Q$**~\cite{khinchin1964}, so the measure itself is classical".

**What the source actually shows (from established content of the book; no PDF consulted):**
- **Claim 2 is Lévy's theorem, and it is a centerpiece of Khinchin's book (Part III, the metric theory of continued fractions).** The theorem states that for almost all $x$, $\lim_{n\to\infty}\frac{1}{n}\ln q_n = \frac{\pi^2}{12\ln 2}$ (equivalently $q_n^{1/n}\to e^{\pi^2/(12\ln 2)}\approx 3.2758$, Lévy's constant). Inverting: the number of convergent denominators $q_n \le Q$ is asymptotically $n \approx \frac{12\ln 2}{\pi^2}\ln Q \approx 0.8428\ln Q$ for almost every $x$. **main.tex's constant is exactly right.** Attribution note: the result is due to P. Lévy (1936); Khinchin's book is the standard reference that presents and proves it, so citing Khinchin 1964 is conventional and defensible, but the theorem is not originally Khinchin's (Khinchin's own constant is the *geometric mean of partial quotients*, $K_0\approx2.6854$ — a different theorem, and **not** what main.tex uses).
- **Consistency check of main.tex's own weight.** main.tex's measure is $\mu(q) = 2\ln 2\,\varphi(q)/q^2$. Summing over all $q\le Q$: $\sum_{q\le Q}\varphi(q)/q^2 \sim \frac{6}{\pi^2}\ln Q$, so $2\ln 2 \cdot \frac{6}{\pi^2}\ln Q = \frac{12\ln 2}{\pi^2}\ln Q$. **The identity main.tex asserts is exactly correct** and independently verifiable without the book.
- **Claim 1 is true and classical, but is a corollary rather than a displayed theorem in Khinchin.** The set of $x$ having $p/q$ (reduced) among its convergents is an interval bounded by the two Stern–Brocot mediants. Derivation, one line from Khinchin's standard convergent identity $x = \dfrac{p_n\alpha_{n+1} + p_{n-1}}{q_n\alpha_{n+1} + q_{n-1}}$ with complete quotient $\alpha_{n+1}\ge 1$: taking $\alpha_{n+1}\to 1$ gives the mediant $(p+p')/(q+q')$ and $\alpha_{n+1}\to\infty$ gives $p/q$ itself; the *other* continued-fraction representation of $p/q$ (with penultimate convergent $p''=p-p'$, $q''=q-q'$) supplies the mirror endpoint $(p+p'')/(q+q'') = (2p-p')/(2q-q')$. Union of the two half-cylinders = the open interval main.tex describes. **The stated endpoints are correct.**
- **Scope caveat inherent to Claim 2:** the $(12\ln 2/\pi^2)\ln Q$ count is an **almost-everywhere / measure-theoretic asymptotic**, not a bound valid for every $x$ or for finite $Q$. main.tex's own text acknowledges this ("almost-everywhere count", and "The residual of Eq. (eq:decoderlaw) is dominated by the **asymptote substitution**, not by finite-size discreteness"), which is the honest framing.
- Khinchin's book also contains the machinery main.tex implicitly relies on elsewhere: the convergent recurrences $p_n = a_np_{n-1}+p_{n-2}$, $q_n = a_nq_{n-1}+q_{n-2}$; $p_nq_{n-1}-p_{n-1}q_n = (-1)^{n-1}$; and the best-approximation theorems (convergents are exactly the best approximations of the second kind), which is what licenses "reduces $A$ to pure number theory".

**Judge verification questions:**
- Is main.tex's constant $12\ln2/\pi^2$ (≈0.8428) the correct almost-everywhere growth rate for the count of convergent denominators below $Q$? (It is — Lévy's theorem, $\lim\frac1n\ln q_n = \pi^2/(12\ln2)$.) And does main.tex correctly present it as an **almost-everywhere asymptotic** rather than an exact or universal count?
- Are the two mediant endpoints $(p+p')/(q+q')$ and $(2p-p')/(2q-q')$ stated correctly, with $p'/q'$ the **penultimate** convergent? (They are; the second endpoint arises from the alternative CF representation with penultimate convergent $p-p'$ over $q-q'$.)
- main.tex calls this "a classical fact of continued-fraction theory~\cite{khinchin1964,hardy2008}" — a general rather than pinpoint citation. Given that the mediant-interval characterization is a one-line corollary of Khinchin's convergent identity rather than a displayed theorem in the book, is the level of attribution ("a classical fact") appropriately hedged, or does main.tex imply the book states it verbatim?
- Does main.tex anywhere conflate **Lévy's constant** ($e^{\pi^2/(12\ln2)}$, the denominator growth rate — the one it actually uses) with **Khinchin's constant** ($K_0\approx2.6854$, the geometric mean of partial quotients — a different result)? The cited claim is Lévy's, presented in Khinchin's book.

---

---

## `kiktenko2025` — Colloquium: Qudits for decomposing multiqubit gates and realizing quantum algorithms (Kiktenko, Nikolaeva, Fedorov, 2025)

**Full citation:** E. O. Kiktenko, A. S. Nikolaeva, A. K. Fedorov, "Colloquium: Qudits for decomposing multiqubit gates and realizing quantum algorithms," *Rev. Mod. Phys.* **97**, 021003 (2025); arXiv:2311.12003.
**Source:** arXiv:2311.12003v2 (3 Jun 2025), Rev. Mod. Phys. 97, 021003 (2025), PDF: `kiktenko-2023-qudits-decomposing-gates-algorithms.pdf` (30 pp; read in full via text extraction, with targeted section reads)

**Cited in main.tex:**
- *Introduction*: "the recent qudit review of Kiktenko et al. lists **''the investigation of the impact of noise within the discussed schemes''** as an **open problem**~\cite{kiktenko2025}."
- *Introduction*: "Comparisons *across* dimensions still treat noise indirectly: **entangling-gate counts as a noise proxy**~\cite{nikolaeva2024,kiktenko2025}".

**What the paper actually shows (full-text, not abstract-level):**
- **The quoted open problem is verbatim.** Sec. VI (Discussion and Conclusion), in the list of "open issues and research directions": "The second significant topic is **the investigation of the impact of noise within the discussed schemes**. In particular, there is an interesting challenge in developing error-correction methods for the case of multiple qubits embedded in a single qudit. Note that local errors in a single qudit can result in entangling errors between qubits contained within that qudit." main.tex's quotation and its characterization as an open problem are both exact. (The abstract likewise says the Colloquium "concludes by summarizing a set of **open problems**".)
- **The gate-count-as-noise-proxy claim is directly supported by an explicit sentence.** Sec. IV.A: "Since **entangling gates commonly are the main source of decoherence**, the qudit-based implementation can be advantageous, especially in the NISQ era." The review's quantitative figure of merit is uniformly the **entangling-gate count**: Fig. 18 plots the number of $\mathrm{CPh}^\bullet$ (qudit) vs CZ/CX (qubit) gates required for $C^{N-1}Z$; Sec. VI's summary is stated in gate counts ("$2N-3$ entangling gates ... for comparison, the best known qubit-based decompositions require $6N+\mathrm{const}$ entangling gates (Maslov, 2016) with clean ancillas or $4N+\mathrm{const}$ with measurement-based feedforward"); the concluding open problems name "a specified **cost function, such as the number of entangling gates or the circuit depth**."
- **The review contains no noise model, no decoherence simulation, and no error-rate calculation.** A full-text search for "noise model", "depolariz", "decoherence" returns only two substantive hits in 6061 lines: the sentence quoted above (Sec. IV.A) and a bibliography entry. There is no Lindblad/Kraus simulation, no fidelity-vs-noise-strength curve, and no cross-dimension noisy comparison anywhere in the review. This **strongly corroborates** main.tex's framing that cross-dimension comparisons in the literature "treat noise **indirectly**".
- **Scope of the review, for context on "cross-dimension comparison":** the Colloquium is about running **qubit** circuits on qudit hardware — (i) qudit-assisted decomposition of multiqubit gates using higher levels as an ancillary buffer, and (ii) compressing $b=\lfloor\log_2 d\rfloor$ qubits into one qudit. It is *not* a study of native qudit algorithms at prime $d$.
- **The review's own headline verdict is explicitly two-sided, not pro-qudit:** Sec. VI: "qudit-based implementations may offer both **substantial advantages and disadvantages** compared to conventional qubit-based solutions", depending on how the $N$ affected qubits are distributed across qudits. Best case for $C^{N-1}Z$: $N=Kb$ qubits grouped into $K$ qudits gives $2K-3$ $\mathrm{CPh}^{i|j}$ gates. Worst case: $N$ qubits on $N$ distinct qudits with no free ancillary levels forces a $2^{2b-2}$-fold **increase** in entangling gates.
- **Scalability limit the authors state:** "we expect a limitation on the scalability of this approach up to the values $b = 2$ and $3$", i.e. $d\le 8$, "Taking into account apparent experimental challenges that appear when control is operated over each new level."
- **Experimental fidelities the review surveys (Sec. V), for calibration against main.tex's own hardware numbers:** photonic two-ququart processor (Chi et al. 2022) — single-ququart Pauli/Fourier gate mean fidelities 98.8(1.3)% and 96.7(1.9)%, two-ququart controlled-unitary **process** fidelity 95.2%; integrated-optics maximally entangled state fidelities 96%/87%/81% at $d=4/8/12$ (Wang et al. 2018); a $d=32$ time-bin photonic qudit used to factor 15 by Shor (Weng and Chuu 2024). The review's summary judgement: "the fidelity of operations with qudits **becomes comparable to** that for standard qubit-based architectures."

**Judge verification questions:**
- Is main.tex's quoted string "the investigation of the impact of noise within the discussed schemes" verbatim from the review, and is it genuinely presented there as an **open problem** (Sec. VI open-issues list)? (Both: yes.)
- Does main.tex's "entangling-gate counts as a noise proxy" fairly describe the review? Check against Sec. IV.A's explicit "entangling gates commonly are the main source of decoherence" and the fact that Fig. 18 and the entire Sec. VI summary are stated in entangling-gate counts with no noise model anywhere in the 30-page review.
- Does main.tex avoid attributing to Kiktenko et al. any *quantitative* noise result or cross-dimension noisy comparison? (It should — the review contains none.)
- If main.tex characterizes the review as a qudit-favourable source, does that square with the review's own two-sided verdict ("both substantial advantages and disadvantages", worst-case $2^{2b-2}$-fold gate increase) and its expectation that the compression approach scales only to $b=2$–$3$ ($d\le8$)?

---

---

## `kitaev1995` — Quantum measurements and the Abelian stabilizer problem (Kitaev, 1995)

**Full citation:** A. Yu. Kitaev, "Quantum measurements and the Abelian stabilizer problem," arXiv:quant-ph/9511026 (1995).
**Source:** arXiv:quant-ph/9511026 (20 Nov 1995), PDF: `kitaev-1995-abelian-stabilizer-problem.pdf` (22 pp; read in full via text extraction, with targeted section reads)

**Cited in main.tex:**
- *Introduction*: "We simulate Shor order finding~\cite{shor1997}, **eigenstate quantum phase estimation (QPE)**~\cite{kitaev1995}, and Grover search~\cite{grover1996} on qubit ($d=2$), qutrit ($d=3$), and ququint ($d=5$) registers, under two decoherence channels..." — i.e. Kitaev 1995 is the origin citation for the QPE algorithm main.tex simulates.

**What the paper actually shows (full-text, not abstract-level):**
- **This is the paper that introduces eigenvalue estimation of a unitary, i.e. quantum phase estimation.** Abstract: "Our method is based on a **procedure for measuring an eigenvalue of a unitary operator**." The attribution in main.tex is the standard and correct one.
- **The precision ladder (Lemma 10, p. 17):** define $U^{[0,r]}|a,\xi\rangle = |a\rangle\otimes U^a|\xi\rangle$ with $r=2^l-1$. Then "the value of the observable $\varphi$ can be measured with precision $2^{-l-2}$ and error probability $\le\epsilon$ by an operation sequence of length $O(l\log(l/\epsilon)) + \mathrm{poly}(l)$", with $U^{[0,r]}$ used at most $O(l\log(l/\epsilon))$ times. This is the $b$-bits-of-phase / controlled-$U^{2^j}$ structure main.tex's QPE circuits implement.
- **Kitaev's readout is *not* the textbook inverse-QFT register.** The procedure (Lemma 9 → Lemma 10) is a **Hadamard-test / repeated-measurement** scheme: each $2^j\varphi \pmod 1$ is localized into one of 8 intervals $[\frac{s-1}{8},\frac{s+1}{8}]$ with error probability $\le\epsilon/l$ by $O(\log(l/\epsilon))$ repetitions (measuring $P = \frac12(1-\cos 2\pi\varphi)$, and $-\sin 2\pi\varphi$ by substituting $iU$), then **classical** post-processing recovers $\varphi$. The QFT-based single-shot readout register is due to Cleve–Ekert–Macchiavello–Mosca (1998) / the Nielsen–Chuang presentation, not to this paper. If main.tex's simulated "eigenstate QPE" uses an inverse-QFT readout register, the algorithm is the *descendant* of Kitaev's, not literally his circuit.
- **The "eigenstate" qualifier is exactly right.** The whole construction assumes an eigenvector: Eq. (21) constructs the Fourier basis $|\psi_h\rangle$ of eigenvectors of the permutation operators $U\in E$, with eigenvalues $\lambda_h(U) = \exp(-2\pi i(h,U))$. main.tex's phrase "**eigenstate** quantum phase estimation" correctly distinguishes this from the superposition-input variant used inside Shor's order finding.
- **Continued-fraction post-processing is in this paper too (Theorem 1, p. 18).** For $U$ a permutation on $N\subseteq B^n$, eigenvalues are $\exp(2\pi i p/q)$ with $q$ = cycle length $\le 2^n$; minimal separation of such rationals is $[2^n(2^n-1)]^{-1}$, so measuring $\varphi$ to precision $2^{-2n-1}$ determines it exactly, and "the transition from the measured value to the exact one can be performed in polynomial time, **using continuous fractions**." Kitaev gives the explicit Euclid-algorithm argument: applying Euclid to $(q',p')$ yields $k'_j=k_j$ for $j\le s-1$ and $k'_s\in\{k_s,k_s-1\}$, so $p/q = \mathrm{CF}(0,k'_1,\dots,k'_s)$ or $\mathrm{CF}(0,k'_1,\dots,k'_{s+1})$. **This is the same decoder structure main.tex analyses in its Stern–Brocot/convergent section** (cited there to `khinchin1964`/`hardy2008`) — a judge may want to check whether main.tex credits Kitaev for the CF decoder as well as for QPE.
- **The result the paper is actually *for*:** a polynomial quantum algorithm for the Abelian Stabilizer Problem (Sec. 4), which subsumes factoring and discrete log, thereby reproducing Shor's results by a different method; plus a polynomial QFT algorithm for an arbitrary finite Abelian group (Sec. 5).
- **The paper is entirely noiseless/complexity-theoretic.** There is **no noise model, no decoherence, and no error-channel analysis**. Its only precision discussion is the *gate-precision* requirement (Introduction): "every step of the computation must be done with precision $c\,(\text{number of steps})^{-1}$", i.e. a logarithmic number of precision bits per gate — a coherent-control statement, not a decoherence statement. All "error probability $\le\epsilon$" quantities in Lemmas 9–10 and Theorem 1 are the algorithm's **intrinsic sampling failure probability at fixed precision**, not hardware error.
- Kitaev explicitly names decoherence-resilience as unresolved: "Precision still remains the most important problem in the field of quantum computation", and asks "is it possible to organize computation so that a moderate perturbation would not affect the result?" — i.e. the reference itself frames noise-robustness as *open*, which is consistent with main.tex's motivating framing.

**Judge verification questions:**
- Does main.tex attribute to Kitaev only the **algorithm** (eigenstate phase estimation) and not any noise-robustness result or intrinsic-failure-probability claim? The paper contains no noise analysis whatsoever; its $\epsilon$'s are sampling failure probabilities at fixed precision.
- main.tex's sentence adjacent to this citation ("concerns the noiseless algorithm; we are not aware of it having been tested against a noise model") — is the noiseless claim being attributed to Kitaev, or to the separately cited robustness/truncation folklore? If Kitaev is being credited with a truncation-robustness statement, that is not in this paper.
- Is "eigenstate QPE" the right label for what Kitaev does? (Yes — Eq. (21) supplies eigenvectors $|\psi_h\rangle$ explicitly, and Lemmas 9–10 estimate the phase of a supplied eigenstate.)
- Does main.tex's simulated QPE circuit use Kitaev's iterative Hadamard-test readout or the later inverse-QFT readout register? If the latter, is the attribution to `kitaev1995` alone (without Cleve et al. 1998) potentially misleading about the circuit actually simulated?
- Does main.tex credit the continued-fraction decoder anywhere to Kitaev (Theorem 1 gives it explicitly, with the $2^{-2n-1}$ precision requirement and the Euclid-algorithm recovery), or only to `khinchin1964`/`hardy2008`?

---

## `low2023` — Control and Readout of a 13-level Trapped Ion Qudit (Low, White & Senko, 2023/2025)

**Full citation:** P. J. Low, B. White, and C. Senko, "Control and readout of a 13-level trapped ion qudit," *npj Quantum Inf.* **11**, 85 (2025); arXiv:2306.03340.
**Source:** arXiv:2306.03340v1 (6 Jun 2023); DOI 10.1038/s41534-025-01031-y. PDF: `low-2023-13-level-trapped-ion-qudit.pdf` (23 pp incl. Extended Data + Supplementary; arXiv v1 text read in full)

**Cited in main.tex:**
- *Introduction* (l. 75): listed among platforms where "processors that exploit them as qudits now exist or are proposed" — grouped with ringbauer2022, blok2021, goss2022, gardill2020, chiesa2024, robert2026.
- *Introduction* (l. 139): co-cited with ringbauer2022 as the basis for "a per-particle depolarizing channel **representative of trapped-ion qudits**" — i.e. low2023 is offered as empirical warrant that trapped-ion qudit noise is well modelled as dimension-flat per-particle depolarizing.
- *Noise channels* (l. 481): "with qudit control demonstrated to **13 levels**~\cite{low2023}" — appended to a sentence whose numbers (per-pulse $2.0\times10^{-4}$ at $d=3$, $3.2\times10^{-4}$ at $d=5$; per-Clifford $2\times10^{-3}\to1.0\times10^{-2}$) all come from ringbauer2022.
- *Noise channels* (l. 492): "only single-qudit pulses reach the $10^{-3}$–$10^{-4}$ scale~\cite{ringbauer2022,low2023}" — low2023 is co-cited as evidence for the $10^{-3}$–$10^{-4}$ single-qudit error scale.

**What the paper actually shows (full-text, not abstract-level):**
- Scope is **SPAM only** — state preparation and single-shot readout of a 13-level qudit in $^{137}$Ba$^+$. **No single-qudit gate benchmarking, no randomized benchmarking, no entangling gate, no algorithm** is performed. The abstract and Main are explicit: "universal quantum computation requires other quantum logic primitives such as entangling gates. These primitives have been demonstrated for lower qudit dimensions" (i.e. by Ringbauer *et al.* at $d=5$ in $^{40}$Ca$^+$) "and can be directly generalized." Conclusion repeats: "To build a functioning quantum computer, the ability to perform single qudit gates and entangling gates are required. Such procedures have been demonstrated in Ref.1 for a qudit dimension of 5."
- Headline numbers (Main, "SPAM Experimental Results"): average **raw SPAM error 13.1 ± 0.3 %**, average **post-selected SPAM error 8.3 ± 0.3 %** (post-selected fidelity 91.7 ± 0.3 %) for $d=13$. Sample size **1000 shots per prepared state**. These are **percent-level**, three to four orders of magnitude above $10^{-4}$.
- Encoding: $|0\rangle=|6S_{1/2},F{=}2,m_F{=}2\rangle$ plus 12 metastable $5D_{5/2}$ states reachable by 1762 nm quadrupole $\pi$-pulses; states with $\pi$-pulse transition fidelity $\le 75\%$ are **excluded**. Protocol extends in principle to **25 levels** (7 of 32 stable/metastable states must be left unencoded for full single-shot distinguishability).
- **Dominant error is magnetic-field noise, and it is explicitly state-dependent, not depolarizing.** Eq. (4): $\chi \propto \kappa^2\tau_\pi^2$, where $\kappa$ is the *transition-specific* magnetic-field sensitivity and $\tau_\pi$ the $\pi$-pulse time. Fig. 4a shows $\varepsilon_\mathrm{SPAM}$ rising linearly in $\kappa^2\tau_\pi^2$ across prepared states, from ~0.04 (intercept) to ~0.3. Per-state post-selected fidelities in Fig. 3c / Table S2 range from ~0.70 ($|6\rangle$) and 0.775 ($|9\rangle$) to 0.97 ($|3\rangle$) — a factor >10 spread in error across levels of the *same* qudit.
- Vertical intercept $\varepsilon_\mathrm{SPAM}=0.04\pm0.01$ attributed to other technical sources: ~1.5 ± 2 % from calibration drift, remainder speculated to be imperfect optical-pumping polarization. Spontaneous decay from $5D_{5/2}$ ($\tau=35$ s), off-resonant transitions, and bright/dark discrimination together contribute **< 0.5 %**.
- Fig. 4b: SPAM fidelity vs $d$ for "optimal choice" vs "worst choice" of encoded states. With optimal choice, average fidelity **improves** slightly with $d$ (~0.93→0.95 region); with worst choice it degrades to ~0.83. Authors' interpretation: "the errors improve with higher dimension indicate that our results are **not limited by any effects that intrinsically depend on the qudit dimension**."
- Authors' own caveat: "we have not made any efforts to mitigate magnetic field noise in this work"; passive/active mitigation is known, so B-noise "is not a fundamental limiting factor."
- Timing: total measurement time ~**100 ms**, described as an artificial limitation of their waveform generation and 614 nm laser; ~1 ms should be achievable. Supplementary §VI, step 3: the 1762 nm probe is left on for "a time that is longer than the coherence time in our system. We set it to **3 ms**" — i.e. the system coherence time is **below 3 ms**.
- Apparatus: 4-rod linear Paul trap, $B_e = 8.35$ G (deliberately in the regime where the linear Zeeman approximation fails and $|F,m_F\rangle$ is not a good basis), NA = 0.26 imaging, PMT detection.
- Table S1/S2 (Supplementary §VIII) give an alternative, stricter reading of the same data (any second bright event counts as failure); overall raw fidelity is lower, post-selected fidelities essentially unchanged.

**Judge verification questions:**
1. main.tex l. 492 states "only single-qudit pulses reach the $10^{-3}$–$10^{-4}$ scale~\cite{ringbauer2022,low2023}." Does low2023 report *any* single-qudit error at the $10^{-3}$–$10^{-4}$ scale? (Its only quoted errors are SPAM at 8.3 % / 13.1 %, and per-state errors of 3–30 %.) Is the co-citation defensible, or does it attribute a Ringbauer number to a paper whose own numbers are two orders of magnitude worse?
2. main.tex l. 139 offers low2023 as warrant for a **per-particle depolarizing** channel "representative of trapped-ion qudits." Low *et al.* find their dominant error is $\kappa^2\tau_\pi^2$-scaled **magnetic-field dephasing** that varies by >10× between levels of the same qudit (Fig. 3c, Fig. 4a). Does main.tex's surrounding text adequately signal this (it does immediately note a "Zeeman-structured dephasing variant... tested in Sec. robustness"), or does the depolarizing claim overstate what low2023 supports?
3. Is "qudit control demonstrated to 13 levels" (l. 481) accurate given that low2023 demonstrates **SPAM only** and no gates? Does main.tex anywhere imply gate-level control at $d=13$?
4. main.tex l. 75 counts low2023 among platforms where qudit "processors... now exist." Given the paper performs no two-qudit gate and no algorithm, is that grouping fair as written (the sentence hedges with "exist or are proposed")?

---

---

## `lu2020` — Quantum Phase Estimation with Time-Frequency Qudits in a Single Photon (Lu, Hu, Alshaykh *et al.*, 2020)

**Full citation:** H.-H. Lu, Z. Hu, M. S. Alshaykh, A. J. Moore, Y. Wang, P. Imany, A. M. Weiner, and S. Kais, "Quantum phase estimation with time-frequency qudits in a single photon," *Adv. Quantum Technol.* **3**, 1900074 (2020); arXiv:1906.11401.
**Source:** arXiv:1906.11401v1 (27 Jun 2019). PDF: `lu-2019-qpe-time-frequency-qudits.pdf` (7 pp, read in full)

**Cited in main.tex:**
- *Discussion* (l. 2416–2417): "single-qudit demonstrations reach $d=8$ on a trapped ion~\cite{shi2025} and, on photonic platforms, **$d=32$ Shor and qudit QPE**~\cite{weng2024,lu2020}." As written, "$d=32$" is the only dimension supplied for the photonic clause; lu2020 is the citation carrying "qudit QPE."

**What the paper actually shows (full-text, not abstract-level):**
- The demonstration is at **$d=3$, not $d=32$**. Explicitly: "As a proof-of-concept implementation, here we limit our dimension to $d=3$ (qutrit) for **both the control and target registers**, capable of retrieving the eigenphase of a given three-dimensional unitary with $2\pi/3$ precision." Abstract: "successfully retrieves any arbitrary phase with **one ternary digit** of precision."
- Encoding: one photon carries two qutrits — **frequency** bins (control, 54 GHz spacing after pulse shaping) and **time** bins (target, 6 ns spacing, ~0.2 ns FWHM). The multi-value-controlled gate is realized as a single-photon operation (phase modulator between two chirped fiber Bragg gratings, ±2 ns/nm), circumventing probabilistic photon–photon interaction.
- Results: for $\hat U_1 = \mathrm{diag}(1, e^{2\pi i/3}, e^{4\pi i/3})$ — eigenphases exactly representable in one ternary digit — measurement fidelity (correct-projection counts / total counts) is **98 ± 1 %**; per-eigenstate diagonal counts 0.9948, 0.9805, 0.9758 (Table I). Phase errors 1.4 %, 2.7 %, 3.0 %.
- For $\hat U_2 = \mathrm{diag}(1, e^{i0.351\pi}, e^{i1.045\pi})$ — not representable in one ternary digit — counts spread across projections; phases are recovered by **least-squares fitting the measured photon statistics** to the theoretical distribution $C(n,\varphi)$ (Eq. 8), giving max error **7.1 %**, <3 % otherwise.
- Explicit self-imposed scope limits stated by the authors: (i) only **diagonal** unitaries were implemented ("Although limited to a proof-of-principle model with arbitrary-phase diagonal unitaries"); (ii) the statistical/fitting approach **requires an eigenstate input** and "should not be viewed as a standalone method for determining an unknown phase"; (iii) the inverse DFT was implemented in a **probabilistic**, multi-shot fashion using a single phase modulator (footnote [41]: a single PM necessarily scatters photons out of the computational space), not the near-deterministic quantum frequency processor; (iv) **coherent states, not true single photons**, were used as input, which they note is permissible because the controlled gate is a one-photon operation.
- The only appearance of "32" in the paper is a *different, non-QPE* result cited from their own group: "our group has recently demonstrated a two-photon four-party GHZ state by encoding **two 32-dimensional qudits in each photon**" (ref. [31], Imany *et al.*, arXiv:1805.04410). This is entanglement generation, not phase estimation.
- Stated next steps confirm the ceiling: "The next steps for our qudit-based PEA are (i) implementing arbitrary unitaries (i.e. non-diagonal) in addition to **increasing the qudit dimension ($d>3$)**."
- Scaling caveat the authors flag: for a target unitary of dimension $M$, the number of target qudits must be $m \ge \log_d M$, so $\hat U$ becomes a multi-photon gate once $\log_d M > 1$; their ability to implement high-dimensional $\hat U$ "scales polynomially with the qudit dimension $d$ and exponentially with the number of target qudits $m$."

**Judge verification questions:**
1. Does main.tex's sentence read as attributing **$d=32$** to lu2020's QPE demonstration? If so, this is a factual error by a factor of ~10 in dimension: lu2020 is $d=3$ with one ternary digit of precision. If the intended parse is "$d=32$ Shor [weng2024] and qudit QPE [lu2020]," is that parse recoverable from the sentence as printed?
2. Does main.tex anywhere state or imply that lu2020's QPE is at a dimension higher than 3, or that it handled non-diagonal unitaries / non-eigenstate inputs?
3. lu2020 is a **single-photon, two-degree-of-freedom** demonstration with a probabilistic inverse DFT and coherent-state input. Is main.tex's framing ("single-qudit demonstrations... on photonic platforms") consistent with a demonstration that actually uses two qutrit registers within one photon?
4. Does the citation support the *comparative* rhetorical purpose (that photonic platforms have gone to higher $d$ than ion traps for algorithm demonstrations)? For QPE specifically, lu2020's $d=3$ is **not** higher than the $d=3$/$d=5$ ion work cited alongside it.

---

---

## `magdon2025` — Tight Success Probabilities for Quantum Period Finding and Phase Estimation (Magdon-Ismail & Dong, 2025)

**Full citation:** M. Magdon-Ismail and K. Dong, "Tight success probabilities for quantum period finding and phase estimation," arXiv:2506.20527 (2025).
**Source:** arXiv:2506.20527v3 (28 Dec 2025). PDF: `magdon-2025-tight-success-probabilities-period-finding.pdf` (20 pp, main text + appendices read)

**Cited in main.tex:**
- *Why the decoder gains tolerance with size* (l. 1522–1523): listed as "the **tight two-sided window bounds** of Magdon-Ismail and Dong" within an inventory of "exact literature [that] bounds the success of continued-fraction post-processing on **base-2 registers**." The surrounding sentence characterizes all listed analyses as scoring "outcomes inside a **tolerance window** of the peaks via the convergent guarantee — **a sufficient condition** — and typically certify recovery of a **divisor $r/\gcd(s,r)$** that a classical search then lifts to $r$," in contrast with main.tex's own exact outcome-for-outcome law.

**What the paper actually shows (full-text, not abstract-level):**
- **Two-sided is correct and is the paper's distinguishing claim.** Theorem 1 (lower bound) and Theorem 2 (upper bound) both bound $P(M) = \mathbb{P}[\min_{k\in\{1,\dots,r-1\}} |\hat\ell - k2^n/r| \le M]$. Theorem 1: $P(M) \ge 1 - \frac1r - \frac{(M-\frac12)}{\pi^2 M(M-1)} + \underline E$ with $|\underline E| \in O(r2^{-n}\log_2 M) \subseteq O(2^{-(m+q+1)}\log_2 M)$. Theorem 2: same leading form with $\kappa \le 1+(M-\frac14)/M(M-1)$ in the denominator and $\overline E - \underline E \in O(r2^{-n})$. Bullet (v) of the intro: "We are not aware of any upper bounds on the probability $P(M)$" — the upper bound is new.
- **Tolerance-window / sufficient-condition framing is exactly right.** Success is *defined* as $\hat\ell$ landing within $M$ of a positive integer multiple of $2^n/r$ (Eq. 2, Eq. 17). §5.4 derives that standard continued-fraction post-processing succeeds whenever $|\hat\ell/2^n - k/r| \le 2^{-(2m+1)}$, i.e. $M = 2^q$ with $n = 2m+q+1$. The analysis is *agnostic to post-processing details apart from $M$*, and $M$ is tunable by extra classical work (lattice methods, brute-force search around $\hat\ell$ à la Proos–Zalka: $M = 2^q + B$).
- **Divisor recovery, not $r$ itself.** "the final output, in the case of period finding, a **divisor of the period $r$**" (abstract); "The algorithm succeeds if $\hat r$ is a **non-trivial divisor of $r$**" (§1); Algorithm 1 line 4: "if $1 < q_k < 2^m$ and $q_k$ **is a divisor of $r$** then return $q_k$, reporting success." This matches main.tex's characterization ("certify recovery of a divisor... that a classical search then lifts to $r$"), though the paper writes it as "a non-trivial divisor," not literally $r/\gcd(s,r)$.
- **Base-2 only.** The circuit (Fig. 2) is an $n$-qubit upper register and $m$-qubit lower register, $n = 2m+q+1$, $\hat\ell \in [0,2^n-1]$, $\mathcal F_n$ the size-$2^n$ DFT. No qudit / base-$d$ generalization anywhere.
- **Peaks excluded at $\ell=0$.** Their $k$ ranges over $\{1,\dots,r-1\}$; they deliberately exclude the $\ell=0$ peak ("we are not aware of any post-processing that extracts non-trivial information from this peak"), and remove it from Ekerå's bound in Table 1 for a fair comparison. main.tex's contrast — that its own law counts "admissible denominators $2r,\dots,\lfloor N/r\rfloor r$ that window bounds do not count" — should be checked against this: Magdon-Ismail & Dong's window is centered on multiples of $2^n/r$ and its success predicate is divisibility of $r$, so denominators that are *multiples* of $r$ are indeed outside their success set.
- **Convergence to 1 and Ekerå comparison.** Leading asymptotic is $1 - 1/r$; with $M \ge 2^q$ convergence is exponential in the $q$ extra top-register qubits. Table 1 ($m=8$, $q=5$): exact 0.664/0.930/0.981/0.993 for $r = 3/15/63/255$ at $M=2^q$; Monte Carlo (50,000 iterations) 0.664/0.932/0.982/0.994; their bounds bracket these to 3 decimals. Ekerå's adapted bound gives 0.662/0.925/0.968/**0.951** — it *decreases* with $M$ and $r$ because its error term is linear in $M$; theirs is logarithmic.
- **Phase estimation is a warm-up, not the main result.** §4 reproduces $\mathbb{P}[|\hat\varphi-\varphi| \le (B+1)/2^t] \ge 1 - \frac{4}{\pi^2(2B-1)}$ (Eq. 15) and states this "seemlessly reproduce[s] the lower bound derived by Chappell in [3]" while **plugging a gap in Chappell's proof** — Chappell showed $x=1/2$ is a critical point but assumed without proof it is a global minimum; Theorem 3 here proves $H_L(x;M)$ is non-increasing on $[0,\tfrac12]$ for $1 \le M \le \lceil L/2\rceil$. Note the authors caution that $H_L(x;M)$ can be *increasing* for large $M$, and that for perturbed $H_L(x;M,\epsilon)$ the critical point at $x=1/2$ may be non-unique or a global maximum (Fig. 1b).
- Stated regime of validity: $m \ge 4$ (so $|\epsilon| \le 1/32$), $2 \le M \le M_* \approx 2^{n-1}/r$, and $M \le L/2(1+|\epsilon|)$. Also assumes one classically tests small periods up to $r_0$ (e.g. $10^6$), so the quantum step need only succeed for $r > r_0$.

**Judge verification questions:**
1. Is "tight **two-sided** window bounds" accurate? (Yes on the face of Theorems 1 and 2 — verify main.tex does not additionally claim more, e.g. exactness rather than tightness up to $\kappa = 1+O(1/M)$.)
2. Does main.tex's blanket characterization "score outcomes inside a tolerance window of the peaks via the convergent guarantee — a **sufficient condition**" fairly describe magdon2025? Verify against Eq. (2)/(17) and §5.4, where success is *defined* as the window condition and continued fractions is shown to imply $M = 2^q$.
3. main.tex says these analyses "typically certify recovery of a divisor $r/\gcd(s,r)$." magdon2025 says "a **non-trivial divisor** of $r$." Is the more specific $r/\gcd(s,r)$ form attributable to magdon2025, or is it a generic claim about the listed group (Gerjuoy, Bourdon–Williams, etc.) that this reference does not itself state?
4. Is "on **base-2 registers**" correct for magdon2025? (Verify: circuit is explicitly $n$-qubit / $2^n$-dimensional throughout; no base-$d$ result exists in the paper, so main.tex's claim of novelty for the base-$d$ setting is not undercut by this reference.)
5. Does main.tex's claim that window bounds "do not count" the admissible denominators $2r,\dots,\lfloor N/r\rfloor r$ hold against magdon2025's success predicate ($\hat r$ a non-trivial divisor of $r$, with $k \in \{1,\dots,r-1\}$ and $\ell=0$ excluded)?

---

---

## `marks2017` — Comparison of Memory Thresholds for Planar Qudit Geometries (Marks, Jochym-O'Connor & Gheorghiu, 2017)

**Full citation:** J. Marks, T. Jochym-O'Connor, and V. Gheorghiu, "Comparison of memory thresholds for planar qudit geometries," *New J. Phys.* **19**, 113022 (2017); arXiv:1701.02335.
**Source:** arXiv:1701.02335v2 (16 Nov 2017). PDF: `marks-2017-memory-thresholds-planar-qudit.pdf` (15 pp, read in full)

**Cited in main.tex:**
- *Introduction* (l. 90): "and qudit **memory thresholds rise under abstract noise models**~\cite{marks2017}" — final item in the list of structural arguments for higher $d$.
- *Introduction* (l. 100–104): "Marks *et al.* point to the ``**increased degrees of freedom that can be coupled to the environment**'' and call whether such noise can be kept sufficiently small ``**an interesting question for experimental implementations**''~\cite{marks2017}" — used as literature evidence that the physical-decoherence question has been flagged and left unanswered.

**What the paper actually shows (full-text, not abstract-level):**
- **Both quoted phrases are verbatim from the Conclusion (§VI).** Full sentence: "One would expect any experimental implementation of qudit codes to be hampered by the increased dimensionality of the system size in terms of potential error leakage, as there are **increased degrees of freedom that can be coupled to the environment**. Whether such noise can be reduced to sufficiently small levels in order to take advantage of the properties that qudit codes provide remains **an interesting question for experimental implementations**." main.tex's rendering ("call whether such noise can be kept sufficiently small...") is a faithful paraphrase of "reduced to sufficiently small levels."
- **The noise model is indeed abstract and dimension-agnostic**, exactly as main.tex says. §V: memory (code-capacity) noise only — noisy data qudits with **perfect syndrome extraction and correction**. Qubit model $\mathcal E(\rho)=(1-p)\rho + pX\rho X$; qudit generalization $\mathcal E(\rho)=(1-p)\rho + \frac{p}{D-1}\sum_{j=1}^{D-1} X^j\rho X^{-j}$ (Eq. 3) — i.e. **generalized bit-flip only** (justified because the code is CSS, so $X$ and $Z$ errors decode independently). Each data point = 30,000 trials.
- **Thresholds do rise with $D$** (Table I and Figs. 11–19):
  - Surface code, MWPM (qubit): $p_\mathrm{th} = 0.103$ (crossing of $d=13$ and $d=15$; only 5,000 trials/point here).
  - Surface code, hard-decision renormalization group (HDRG) clustering: **0.093 at $D=2$**, 0.1255 at $D=5$, 0.1545 at $D=100$, plateau **0.155** as $D\to\infty$.
  - 6-6-6 color code, Delfosse surface projection (qubit): **0.080** (their implementation; Delfosse's own result is 0.087).
  - 6-6-6 color code, new GCC (General Color Clustering) decoder: **0.056 at $D=2$**, 0.084 at $D=3$, 0.115 at $D=25$, 0.1207 at $D=1001$, plateau **0.119** (abstract: "increases by up to **112 %**").
  - Threshold curves fitted to $T(D) = T_\mathrm{plateau} - \alpha\beta^{-D}$.
- **The authors' own strong caveat directly qualifies the "thresholds rise" headline** (§VI): "while the threshold value for qudit codes exceed that of the qubit base, **a direct comparison may be misleading**. Namely, while the probability of introducing an error is the same, the probability of a given error type is **reduced** in the qudit case since there are an increased number of possible errors due to the growth in system size." They also caution (§V B) against directly comparing surface-code and 6-6-6 color-code threshold values because the geometries differ.
- Further caveats stated by the authors: memory/code-capacity thresholds are "a first estimate"; good performance here "will typically translate into good performance under gate noise... **although the threshold will typically decrease by at least an order of magnitude**." The clustering (renormalization) decoders are approximate and *underperform* the optimal qubit decoders at $D=2$ — the qudit gain is measured against a decoder that is itself suboptimal at $D=2$. Simulations were limited to code distance $\le 13$; the $d=7$ color-code curve is excluded from the threshold fit due to small-size boundary effects.
- **Dimensions studied are not restricted to primes** ($D = 2, 3, 5, 25, 100, 1001$). The paper's qudit generalized Paulis are $\mathbb{Z}_D$ Heisenberg–Weyl operators; nothing here supports a prime-dimension-specific claim.
- Software contribution: QTop, an open-source framework for topological codes of arbitrary distance and qudit dimension.

**Judge verification questions:**
1. Are both quoted strings in main.tex l. 100–104 verbatim/faithful to §VI of marks2017? (Verify "increased degrees of freedom that can be coupled to the environment" — exact; and that "kept sufficiently small" is a fair rendering of "reduced to sufficiently small levels.")
2. Is "qudit memory thresholds rise **under abstract noise models**" accurate, and does the qualifier "abstract" adequately convey that the model is code-capacity generalized-bit-flip with **perfect measurement**? Does main.tex anywhere over-generalize this to circuit-level or physical noise?
3. Does main.tex omit the authors' own countervailing caveat that "a direct comparison may be misleading" because per-error-type probability falls as $D$ grows? Given that main.tex's whole argument is that structural qudit advantages may not survive physical noise, does omitting this *strengthen* or *weaken* the framing it builds?
4. Does main.tex draw any prime-dimension implication from marks2017? (The paper studies $D=25,100,1001$ — composite — so no prime-specific claim is supportable from it.)

---

---

## `meth2025` — Simulating Two-Dimensional Lattice Gauge Theories on a Qudit Quantum Computer (Meth *et al.*, 2025)

**Full citation:** M. Meth, J. Zhang, J. F. Haase, C. Edmunds, L. Postler, A. J. Jena, A. Steiner, L. Dellantonio, R. Blatt, P. Zoller, T. Monz, P. Schindler, C. Muschik, and M. Ringbauer, "Simulating two-dimensional lattice gauge theories on a qudit quantum computer," *Nat. Phys.* **21**, 570 (2025); arXiv:2310.12110.
**Source:** arXiv:2310.12110v3 (24 Oct 2024). PDF: `meth-2025-2d-lattice-gauge-qudit-quantum-computer.pdf` (23 pp incl. appendices A–K, read)

**Cited in main.tex:**
- *Discussion* (l. 2411–2413): "on a Ringbauer-class ion processor~\cite{ringbauer2022}, where multi-qudit entangling algorithms have been demonstrated at $d=3$ and $d=5$ (**a qutrit–ququint lattice-gauge simulation**~\cite{meth2025})."
- *Discussion* (l. 2473–2474): systematics budget item (iv) *Motional heating*: "**$2.7(2)$ phonons/s with $27.4(4)$ ms motional coherence**~\cite{meth2025} against a ${\sim}10$ ms schedule — percent-level at most."

**What the paper actually shows (full-text, not abstract-level):**
- **Both numbers are verbatim from Appendix A**: "We measure a heating rate of **2.7(2) phonons per second** and a motional coherence time $\tau$ of **27.4(4) ms**." Same paragraph gives the supporting apparatus context: $^{40}$Ca$^+$, axial trap frequency $\omega_z = 0.77$ MHz, beam at $22.5^\circ$ to the trap axis, Lamb–Dicke factor $\eta = 0.041$.
- Adjacent coherence figures a judge may want for the "~100 ms coherence" statement elsewhere in the same main.tex paragraph: $D_{5/2}$ lifetime $T_1 \approx 1.1$ s; the narrow-band addressing laser has coherence time **$T_2 = 92(9)$ ms** (Fig. 4 caption).
- **The qutrit–ququint characterization is accurate but has two distinct experiments that main.tex compresses into one clause:**
  1. *2D-QED with matter, open boundary conditions*: a **hybrid qubit–qudit** register — one **qutrit** ($d=3$) for the single surviving gauge field after Gauss's-law elimination, plus **four qubits** for the matter vertices. VQE ground-state search; plaquette expectation $\langle\hat\Box\rangle$ measured vs $g^{-2}$ at $\Omega=5$, $m=0.1$. This experiment is $d=3$ only.
  2. *Pure-gauge 2D-QED, periodic boundary conditions*: the gauge-field truncation is refined from **qutrits ($d=3$) to ququints ($d=5$)**, $(L,l) = (2,1)$ and $(3,2)$ respectively, in the electric and magnetic representations. This is where $d=5$ appears. Authors' finding: at small $g^{-2}$ a qutrit truncation suffices; at larger $g^{-2}$ truncation errors matter and the ququint representation "becomes advantageous."
- **Entangling mechanism**: mixed-dimensional controlled rotations (C-ROTs) via Cirac–Zoller-style coupling to a single axial COM phonon mode, using an anti-Jaynes–Cummings interaction $\hat H_j = i\eta\Omega_j(\hat a^\dagger\hat\sigma_j^+ + \hat a\hat\sigma_j^-)^{|g\rangle\leftrightarrow|k\rangle}$, with $S_{1/2}$ ground states as auxiliary levels $|g\rangle$ and the qudit encoded entirely in the $D_{5/2}$ Zeeman manifold for $d>2$.
- **Directly relevant to main.tex's item (iii) on AC-Stark cross-talk**: Appendix A states each blue-sideband pulse $B(\theta,\phi)$ "will thus introduce unwanted AC Stark shifts $\Delta_\mathrm{AC}$ on the order of a few kHz [11], which must be carefully taken into account for achieving high-fidelity C-ROT gates," compensated two-fold — actively on the driven BSB and passively in software via frame updates on subsequent operations; $\Delta_\mathrm{AC}$ measured per state by Ramsey, of order $2\pi\cdot 4$ kHz. This supports main.tex's characterization of the shifts as **coherent and calibratable**.
- **Important countervailing methodological point (Appendix J, "Noise Model"):** "While systems consisting of qubits only can often be accurately described by generic noise models such as **simple depolarising noise, we found that for our qudit systems this is too reductive**." Their heuristic model instead uses (a) Gaussian amplitude fluctuations on gate angles, variance $\sigma_a^2$ for entangling gates and $\sigma_a^2/10$ for single-qudit gates, and (b) a Gaussian AC-Stark **phase error** $\Phi \sim \mathcal N(0,\sigma_p^2)$ applied level-dependently (Eqs. J3–J5; the qutrit target picks up $e^{i3\Phi}, e^{i2\Phi}, e^{i3\Phi}$ on $|-1\rangle,|0\rangle,|+1\rangle$). Fitted values $\sigma_a^2 = 0.047$, $\sigma_p^2 = 0.073$; "good qualitative agreement" with experiment.
- Gate-count context (Table I, Appendix): register sizes 5/5/5 (qubit-equivalent circuits) vs 7/9/11 for $d = 3/5/7$ comparisons, with tabulated CNOT fidelities of 99 % and 99.5 % used for hardware-agnostic circuit-complexity comparison — these are *assumed* fidelities for a complexity estimate, not measured gate fidelities of this device.
- The paper does **not** report a total circuit wall-clock duration for the VQE circuits, so main.tex's "against a ${\sim}10$ ms schedule" comparison is main.tex's own schedule estimate, not a meth2025 number.

**Judge verification questions:**
1. Are "$2.7(2)$ phonons/s" and "$27.4(4)$ ms motional coherence" quoted exactly and attributed to the right device? (Verify: Appendix A of meth2025, $^{40}$Ca$^+$, $\omega_z=0.77$ MHz — and confirm main.tex is not conflating the 27.4 ms **motional** coherence with the 92(9) ms laser $T_2$ or the ~100 ms figure used two sentences earlier.)
2. Is "a qutrit–ququint lattice-gauge simulation" a fair one-clause summary? Verify that the $d=5$ ququint appears only in the **pure-gauge, periodic-boundary** experiment, while the matter-including 2D-QED experiment is a hybrid **qubit–qutrit** register (one qutrit + four qubits) — i.e. that main.tex is not implying a single $d=5$ multi-qudit algorithm with matter fields.
3. main.tex's item (iii) treats residual cross-talk as "largely coherent (state-dependent AC-Stark shifts on occupied higher levels)... in principle calibratable." Does meth2025's Appendix A/J support "calibratable" (they compensate actively + in software) while simultaneously showing a **residual** stochastic phase error $\sigma_p^2 = 0.073$ that they must model to reproduce the data? Is "calibration requirement rather than a decoherence rate" defensible against that residual?
4. main.tex's core noise model is a **per-particle depolarizing** channel for ion qudits. meth2025 explicitly finds "simple depolarising noise... too reductive" for their qudit system and substitutes a level-dependent coherent-phase model. Does main.tex acknowledge this tension anywhere it cites meth2025, or in its Limitations?
5. Is the "${\sim}10$ ms schedule" figure sourced from meth2025 or supplied by main.tex? (meth2025 reports no VQE circuit duration; verify main.tex does not imply otherwise.)

---

---

## `molmer1993` — Monte Carlo Wave-Function Method in Quantum Optics (Mølmer, Castin & Dalibard, 1993)

**Full citation:** K. Mølmer, Y. Castin, and J. Dalibard, "Monte Carlo wave-function method in quantum optics," *J. Opt. Soc. Am. B* **10**, 524 (1993).
**Source:** JOSA B 10(3), 524–538 (1993); DOI 10.1364/JOSAB.10.000524. PDF: **not available** — no arXiv preprint exists (paper predates quant-ph), and no local copy is in `papers/`. **The account below is from bibliographic/domain knowledge of this classic paper, not from the full text, and should be treated as lower-confidence than the other five entries in this batch.** A judge who needs line-level verification should obtain the JOSA B PDF.

**Cited in main.tex:**
- *Methods* (l. 2676–2678): co-cited with `dalibard1992` as the provenance of the "**Monte Carlo wavefunction trajectories**" simulator used beyond Hilbert dimension ~3000. main.tex's own described procedure: "after each gate, each carrier independently passes through the per-layer channel raised to the gate's cost, sampled via one Kraus operator drawn with probability $\mathrm{tr}(K^\dagger K\rho_q)$ from the carrier's reduced state. Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly."

**What the paper actually shows (from domain knowledge — full text not consulted):**
- This is the canonical long-form exposition of the Monte Carlo wave-function (MCWF) / quantum-jump method, expanding the short letter of Dalibard, Castin & Mølmer, *Phys. Rev. Lett.* **68**, 580 (1992) (= `dalibard1992`). The pairing of the two citations in main.tex is the standard convention.
- Core algorithm as presented there: a single stochastic wave function $|\psi(t)\rangle$ is evolved over a small step $\delta t$ under the **non-Hermitian effective Hamiltonian** $H_\mathrm{eff} = H - \tfrac{i\hbar}{2}\sum_m C_m^\dagger C_m$; with probability $\delta p = \sum_m \delta p_m$, $\delta p_m = \delta t\,\langle\psi|C_m^\dagger C_m|\psi\rangle$, a **quantum jump** $|\psi\rangle \to C_m|\psi\rangle/\lVert C_m|\psi\rangle\rVert$ is applied, the jump channel $m$ being drawn with relative probability $\delta p_m/\delta p$; otherwise the state is renormalized after the deterministic non-Hermitian evolution.
- Central theorem: the trajectory-averaged projector $\overline{|\psi\rangle\langle\psi|}$ **reproduces the Lindblad master-equation density matrix** $\sigma(t)$, to first order in $\delta t$ and exactly in the limit of infinitely many trajectories. This is the result main.tex leans on ("Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly").
- Computational-cost argument (the paper's main practical selling point): storing a wave function costs $O(N)$ versus $O(N^2)$ for a density matrix in an $N$-dimensional Hilbert space, so MCWF wins once $N$ is large enough that the number of trajectories required for the desired statistical precision is $\ll N$. Statistical error on a trajectory-averaged observable falls as $1/\sqrt{N_\mathrm{traj}}$. This is exactly the tradeoff main.tex invokes by switching methods above Hilbert dimension ~3000.
- Scope of the original: continuous-time dissipative **quantum optics** problems — spontaneous emission from multilevel atoms in laser fields, and in particular laser-cooling simulations (Sisyphus / lin$\perp$lin cooling in 1D and higher dimensions) that were intractable by direct density-matrix integration. The paper also discusses the relation to other unravelings (Carmichael's quantum trajectories; Dum, Zoller & Ritsch) and stresses that **different unravelings give the same density matrix but different individual trajectories**, so single trajectories should not be over-interpreted physically without a measurement scheme attached.

**Caveats a judge should weigh (methodological gap between cited method and main.tex's use):**
- Mølmer–Castin–Dalibard describe a **continuous-time** unraveling with infinitesimal $\delta t$, an effective non-Hermitian Hamiltonian, and jump operators. main.tex describes a **discrete-time Kraus-operator sampling** applied once per gate per carrier, with the Kraus index drawn with probability $\mathrm{tr}(K^\dagger K\rho_q)$ from the carrier's **reduced** state. That discrete Kraus unraveling is mathematically the same idea (and is exact — for a global pure state, the probability of outcome $K$ acting on carrier $q$ is indeed $\mathrm{tr}(K^\dagger K\rho_q)$), but it is a *generalization/descendant* of the 1993 scheme rather than the literal algorithm in that paper.
- The per-carrier, reduced-state variant used in main.tex is not, to my knowledge, in the 1993 paper; nor is the "channel raised to the gate's cost" construction. If main.tex frames the citation as "we use the method of [dalibard1992, molmer1993]," that is a fair lineage citation; if it frames it as "as prescribed in [molmer1993]," that would over-attribute.
- The unbiasedness and variance-ratio numbers main.tex reports ($8000$ trajectories giving $0.24294\pm0.00092$ vs exact $0.242474$, a $0.51\sigma$ agreement; variance ratios $7.7$–$26.6$) are main.tex's own validation, not results from molmer1993.

**Judge verification questions:**
1. Does main.tex present molmer1993 as the source of the **general MCWF method** (fair) or as the source of the **specific per-gate, per-carrier Kraus-sampling procedure with $\mathrm{tr}(K^\dagger K\rho_q)$** (over-attribution — that discrete-channel formulation is not the 1993 continuous-time jump algorithm)?
2. Is "Averaging $|\psi\rangle\langle\psi|$ over trajectories reproduces the channel exactly" a correct statement of the MCWF equivalence theorem? (Yes for the ensemble limit; check whether main.tex's word "exactly" is qualified anywhere as an infinite-trajectory statement, since at finite $N_\mathrm{traj}$ there is $1/\sqrt{N_\mathrm{traj}}$ statistical error — which main.tex does then quantify.)
3. Does main.tex attribute any *numerical* result to molmer1993? (It should not — all reported trajectory statistics are main.tex's own.)
4. **Availability flag for the audit chain:** no PDF of this reference is held in `papers/`. Given the project convention of archiving cited PDFs, should this one be obtained (JOSA B, DOI 10.1364/JOSAB.10.000524) so the citation can be verified at full-text level rather than from memory?

---

## `nam2012` — Performance scaling of Shor's algorithm with a banded quantum Fourier transform (Nam & Blümel, 2012)

**Full citation:** Y. S. Nam and R. Blümel, "Performance scaling of Shor's algorithm with a banded quantum Fourier transform," Phys. Rev. A **86**, 044303 (2012).
**Source:** Phys. Rev. A 86, 044303 (2012). PDF: `nam-2013-scaling-laws-banded-qft.pdf`

> **PDF/BIB MISMATCH (flag to judge).** The PDF in `papers/` is **not** the cited 2012 paper. It is arXiv:1302.5844v1 (23 Feb 2013), *"Scaling laws for Shor's algorithm with a banded quantum Fourier transform"* by the same two authors — the longer companion/successor. That PDF **cites** the 2012 PRA 86, 044303 paper as its own Ref. [16] (bibliography line: "[16] Y. S. Nam and R. Blümel, Phys. Rev. A 86, 044303 (2012)"), and attributes its small-$n$ non-exponential performance formula $P_<(n,b)$ [Eq. (67)/(69)] to that reference. So the cited 2012 paper is the *source of the small-$n$ regime result*, while the PDF on hand supplies the large-$n$ exponential scaling and the RSA-2048 illustration. The two papers are the same research program; the specific numbers quoted below come from the 2013 PDF unless noted.

**Cited in main.tex:**
- *Introduction*: cited jointly with `barenco1996` as the "qubit evidence that order finding tolerates truncation of small QFT rotations" — i.e. as the empirical qubit-side basis for Pavlidis & Floratos's conjecture that qudit QFT-based arithmetic would show "a similar robustness." No number from this reference is quoted in main.tex; it is used purely as a pointer to the qubit truncation-robustness literature.

**What the paper actually shows (full-text, not abstract-level):**
- Subject: Shor order-finding with the **banded QFT** — the semiclassical (measurement-based, single-qubit) QFT of Griffiths–Niu with each qubit retaining conditional rotations only from its $b$ nearest neighbours (Coppersmith's approximate QFT), Figs. 1(a)/(b). Bandwidth $b=n-1$ is the full QFT.
- Performance measure $P(n,b)$ = ratio of success rates of banded vs full-bandwidth QFT, based on the single $|l_j\rangle$ state closest to each Fourier peak centre (Sec. IV, Eq. (22)); the authors justify the single-state proxy by the numerical observation that peak *width* is unchanged by banding while peak *height* drops, so all states under a peak respond in unison (Sec. VIII, p. 34).
- **Numerics**: proper $\omega$-averaged simulations of factoring *actual semiprimes* $N$, $n = 9$ to $33$ qubits, up to 7 semiprimes per $n$, $b = 1\ldots8$ (Figs. 4, 5) and $b = 10, 15, 20$ (Fig. 6).
- **Large-$n$ (exponential) regime**: $P_>(n,b) = 2^{-\xi_b(n-8)}$ with $\xi_b = 1.1\times2^{-2b}$ (Eq. 66). Analytically $\xi_b^{(a)} \approx \tfrac{1}{2}\pi\ln(2)\times2^{-2b} \approx 1.19\times2^{-2b}$ — prefactor reproduced to within 10%.
- **Small-$n$ (non-exponential) regime**: $P_<(n,b) \approx \exp[-\varphi_{\max}^2(n,b)/100]$ numerically (Eq. 67/69, *taken from Ref. [16] = the cited 2012 paper*), $\exp[-\varphi_{\max}^2/64]$ analytically, with $\varphi_{\max}(n,b)=2\pi[2^{-b-1}(n-b-2)+2^{-n}]$.
- **Transition point**: $n_t(b) \approx b + 5.9 + \sqrt{7.7(b+2)-47}$ for $b \gtrsim 8$ (Eq. 75).
- **Headline robustness claim (Sec. VIII, pp. 35–36)**: for RSA-2048 ($n = 4096$ qubits), $b = 8$ gives $P = 0.954$ — i.e. "a quantum computer with a bandwidth of only $b=8$ can factor RSA-2048 with a performance of better than 95%"; $b=9$ raises it to 98%. Sec. V: "relatively small $b \lesssim 10$ are already sufficient for excellent quantum computer performance."
- **Scope limits the authors state**: (i) $P=0.954$ at $n=4096$ is an **extrapolation** — numerics only reach $n\approx33$; the authors argue validity via $\hat\sigma^2 < 1 \Rightarrow n < 12\times2^{2b}/\pi^2 = 79682$ for $b=8$. (ii) The performance measure is a *single-$l$ proxy*, not the full set of post-processable states. (iii) The exponent shift by 8 in $n-8$ is an empirical artefact tied to $N=15$. (iv) This is **noiseless**: banding is a *coherent* circuit truncation, not decoherence. The only decoherence-aware member of this literature that the paper discusses is Barenco *et al.* [32], whose analytic estimates the authors note require $b > \log_2(n)+2$ and are therefore **not applicable** in the small-$b$, large-$n$ regime.

**Judge verification questions:**
- Does main.tex's phrase "qubit evidence that order finding tolerates truncation of small QFT rotations" accurately describe this work, given the result is $P \geq 95\%$ at $b=8$ for $n=4096$ **for the noiseless banded circuit**, and does main.tex anywhere imply this reference tested truncation against *noise* (which it did not)?
- The PDF on file is the 2013 "Scaling laws" companion, not the 2012 PRA 86, 044303 "Performance scaling" paper actually cited. Is the bib entry (title/volume/page/year) correct for what main.tex intends, and does anything main.tex says depend on which of the two papers is meant?
- Does main.tex correctly place this reference as *cited by Pavlidis & Floratos* (Pavlidis's Ref. [52] is exactly Nam & Blümel, PRA 86, 044303 (2012)) rather than claiming Nam & Blümel themselves studied qudits? (The paper is entirely $d=2$.)

---

---

## `nikolaeva2024` — Efficient realization of quantum algorithms with qudits (Nikolaeva, Kiktenko & Fedorov, 2024)

**Full citation:** A. S. Nikolaeva, E. O. Kiktenko and A. K. Fedorov, "Efficient realization of quantum algorithms with qudits," EPJ Quantum Technol. **11**, 43 (2024); arXiv:2111.04384.
**Source:** arXiv:2111.04384v3 (1 Jul 2024) / EPJ Quantum Technol. 11, 43. PDF assigned in batch: `nikolaeva-2024-trapped-ion-qutrit-toffoli.pdf` — **wrong file**; correct file in `papers/` is `nikolaeva-2021-efficient-algorithms-with-qudits.pdf`.

> **PDF/BIB MISMATCH (flag to judge).** `nikolaeva-2024-trapped-ion-qutrit-toffoli.pdf` is arXiv:2407.07758v2, *"Scalable improvement of the generalized Toffoli gate realization using trapped-ion-based qutrits"* by Nikolaeva, Zalivako, Borisenko, Semenin, Galstyan, Korolkov, Kiktenko, Khabarova, Semerikov, Fedorov & Kolachevsky — a **different, experimental** paper with a different author list and arXiv id. The bib entry (title, authors, arXiv id, journal) matches `nikolaeva-2021-efficient-algorithms-with-qudits.pdf`, which I read in full and use below. Findings from the mis-assigned experimental paper are given at the end because they bear on the same claim.

**Cited in main.tex:**
- *Introduction*: cited with `kiktenko2025` as an example that "Comparisons *across* dimensions still treat noise indirectly: entangling-gate counts as a noise proxy." I.e. main.tex attributes to this reference the methodological choice of using two-qudit gate *counts* as a stand-in for noise, rather than simulating noise.

**What the paper actually shows (full-text, not abstract-level):**
- It is a **qudit transpiler** paper: a scheme mapping a standard qubit circuit onto a qudit register ($m$ qudits of $d$ levels) via an optimized qubit-to-qudit mapping $\phi_{\rm opt}: \{0,1\}^n \to \{0,\ldots,d-1\}^m$, then compiling to a universal set of single-qudit + two-qudit gates. Two techniques: (a) embed several qubits per qudit ($d \geq 2^{m'}$); (b) use upper levels $|a\rangle$, $a\geq2$, as ancillas in multi-qubit-gate decompositions.
- **The figure of merit is explicitly the two-qudit gate count, and the noise-proxy justification is stated verbatim** (Sec. II): *"we use the number of two-qudit interactions as the main figure of merit for quantifying the performance of the transpilation… The reason for this is that usually, two-body gates are the main source of errors during the process of executing quantum circuits. Nevertheless, alternative metrics, such as circuit depth or resulting fidelity estimation, can be used."* This is a direct, near-literal match to how main.tex characterizes it.
- **The authors themselves flag the limitation** (Discussion, Sec. VI): *"we note that one can consider a refinement of the optimized qudit circuit criterion. It can be defined not only by the number of two-particle operations but also as a total qudit circuit fidelity (or its estimation), which takes into account both single-qudit and two-qudit gates fidelities… this metric allows one to more accurately take into account the effects of decoherence arising from the usage of upper levels."* — i.e. the paper concedes it does **not** model decoherence from higher levels.
- **No noise simulation anywhere.** No noise channel, no decoherence rate, no per-level coherence data. All results are gate counts.
- Concrete result: a 6-qubit example circuit transpiled onto **four 4-level qudits** needs only $N^{qd}_{2\text{-body}} = 6$ two-qudit gates versus the straightforward qubit implementation, with advantage in both circuit width and depth (Fig. 9).
- Guarantee: if $m \geq n$, the qudit two-qudit gate count never exceeds the qubit two-qubit count (trivial one-qubit-per-qudit mapping). Warning: the first (embedding) technique "is not universal in the sense that the total number of operations strongly depends on the mapping."
- Cites as motivating evidence (Sec. VI) a "thousandfold reduction in entangling gate number starting from eight qubits… with ququints ($d=5$)" for Grover, from their Ref. [83] — a *gate-count* claim, again with no noise model.
- The paper notes qudit gate fidelities are "comparable with qubit gates' fidelities" but presents no measurements of its own; it is purely theoretical/compilation work.

**What the mis-assigned PDF (arXiv:2407.07758) shows, for completeness:** experimental $^{171}$Yb$^+$ omg-qutrit register of 10 ions; $N$-qubit Toffoli in $2N-3$ two-qutrit MS gates vs $O(N^2)$ for the ancilla-free qubit decomposition; XX($\pi/4$) SPAM-corrected Bell fidelity 96.3(2)%; single-qudit RB fidelities 0.99946(6) ($R^{01}$) and 0.9994(1) ($R^{02}$); qutrit-Toffoli truth-table fidelity beats qubit decomposition for all $N=3..6$ (qubit $F_{tt}$ falls to 4.2(1)% at $N=6$); leakage $1-A p^{2N-3}$ with $p=0.92(1)$; post-selected 3-qubit Grover error 12.9(5)% vs 22.8(5)% qubit (1.7× reduction). Note this paper *does* measure fidelity directly rather than using gate count as a proxy — so if the citation were resolved against this PDF, main.tex's "entangling-gate counts as a noise proxy" characterization would be a **poorer** fit.

**Judge verification questions:**
- Does main.tex's sentence "entangling-gate counts as a noise proxy~\cite{nikolaeva2024,kiktenko2025}" fairly describe arXiv:2111.04384 / EPJQT 11:43, given that paper's own words "we use the number of two-qudit interactions as the main figure of merit… two-body gates are the main source of errors"? (Answer should be yes.)
- Does main.tex anywhere attribute a *noise simulation*, a *fidelity measurement*, or a *cross-dimension noise comparison* to `nikolaeva2024`? (The cited paper has none.)
- Is the bibliography entry pointing at the intended paper, and does the repo's PDF↔bibkey mapping need correcting (`nikolaeva-2021-efficient-algorithms-with-qudits.pdf`, not `nikolaeva-2024-trapped-ion-qutrit-toffoli.pdf`)?

---

---

## `parasa2011` — Quantum phase estimation using multiple-valued logic (Parasa & Perkowski, 2011)

**Full citation:** V. Parasa and M. Perkowski, "Quantum phase estimation using multiple-valued logic," in Proc. 41st IEEE Int. Symp. on Multiple-Valued Logic (ISMVL), p. 224 (2011). DOI 10.1109/ISMVL.2011.47.
**Source:** ISMVL 2011, 23–25 May 2011, Tuusula, Finland. PDF: `parasa-2011-qpe-multivalued-logic-SLIDES.pdf` (53-slide conference deck, not the proceedings paper).

**Cited in main.tex:**
- *Introduction*: main.tex says a claim that "qudit phase-estimation error decreases exponentially with $d$" is attributed by the Wang *et al.* review (`wang2020`) to this conference contribution, "whose available slides state it for the algorithm's intrinsic failure probability at fixed precision," and that the claim "concerns the noiseless algorithm; we are not aware of it having been tested against a noise model."

**What the paper actually shows (full-text, not abstract-level):**
- The deck generalizes textbook QPE from qubits to base-$d$ qudits: Chrestenson gate in place of Hadamard, base-$d$ inverse QFT, $d$-valued quantum multiplexers for controlled $U^{j}$ (explicit $d=3$ multiplexer shown).
- **Binary baseline** (slide, "QPE Performance"): when the phase is not an exact fraction, QPE succeeds with minimum probability $8/\pi^2 = 81.5\%$; derived from $|\alpha_l|^2 \geq 4/\pi^2$ per state.
- **Definition of failure probability** (slide "Failure probability"): with $t$ dits used and $n$ dits of required precision, error $e = d^{t-n}-1$, and
  $\varepsilon = p(|l - \tilde\varphi_u| > e) = \sum_{l \notin [\tilde\varphi_u - e,\ \tilde\varphi_u + e]} |\alpha_l|^2 \le \dfrac{1}{2(e-1)}$, so $p(\mathrm{Success}) > 1 - \dfrac{1}{2(e-1)}$ with $e = d^{t-n}-1$.
- **Resource formula** (slide "Success probability: REQUIREMENTS"): $t = n + p = n + \log_d\!\left(2 + \tfrac{1}{2\varepsilon}\right)$.
- **The quantitative "exponential in $d$" datum** (slide "How MVL HELPS"): bar chart of failure probability $\varepsilon$ as a percentage at *fixed* $p = 3$ extra dits, versus $d$: $d=2 \to 8.35\%$, $d=3 \to \approx2.0\%$, $d=4 \to \approx0.8\%$, $d=5 \to \approx0.4\%$, $d=6 \to \approx0.25\%$, $d=7\ldots10 \to \approx0.15\%$ down to $\approx0.05\%$. Slide title/bullet: *"Failure probability decreases exponentially with increase in radix d of the logic used."*
- **Register-size table** ("More RESULTS", NUMBER OF QUDITS REQUIRED FOR QPE ALGORITHM): e.g. 5 decimal digits @ 99.5% needs $t = 24 / 15 / 12 / 11 / 10$ for $d = 2/3/4/5/6$; 4 digits @ 98% needs $19/12/10/9/8$; 2 digits @ 90% needs $11/7/6/5/5$. A companion chart gives 5 decimal digits @ 98% success: $t = 22$ ($d{=}2$) down to $7$ ($d{=}10$).
- **Nature of the claim, and its scope limits**: The quantity that falls is the *intrinsic algorithmic* failure probability of QPE at a fixed number $p = t-n$ of extra dits — i.e. the probability that the measured $l$ falls outside the requested precision window. From $\varepsilon \le 1/(2(d^{p}-2))$ the decay is strictly *geometric in $p$* and *power-law $d^{-p}$ in $d$* at fixed $p$; the "exponentially with $d$" phrasing is **the slides' own wording**, arguably loose. Nothing on any slide involves decoherence, gate error, noise channels, or hardware fidelity — the words "noise," "decoherence," "error rate," and "fidelity" never appear. The concluding slides identify the *open* problem as synthesis/decomposition of the high powers $U^k$ ("We cannot design these matrices as powers. This would be extremely wasteful… This research problem has been not solved in literature even in case of binary unitary matrices $U$") — i.e. the deck explicitly does **not** cost the controlled-$U^{d^i}$ compilation.
- Note: the artefact is a **slide deck**, not the ISMVL proceedings paper; several derivation slides are images and some intermediate algebra is not reproducible from text extraction.

**Judge verification questions:**
- Does main.tex correctly restrict the "exponential decrease with $d$" claim to the **intrinsic failure probability at fixed precision** (not to a noise-induced error), matching the slides' $\varepsilon \le 1/(2(d^{t-n}-2))$ and the $p=3$ bar chart?
- Is main.tex's statement "we are not aware of it having been tested against a noise model" defensible — i.e. do the slides contain any noise/decoherence content at all? (They do not.)
- Does main.tex attribute the claim to *Wang et al.'s review citing* Parasa & Perkowski, rather than asserting it as Parasa & Perkowski's own published, peer-reviewed result — and is the hedge "whose available slides state it" appropriate given the artefact is a deck, not the proceedings paper?
- Would a stricter reading ("power-law $d^{-p}$ in $d$ at fixed $p$; exponential in $p$") contradict main.tex? main.tex reports the claim as-attributed rather than endorsing it, so this is a scope check, not necessarily an error.

---

---

## `pavlidis2021` — Quantum-Fourier-transform-based quantum arithmetic with qudits (Pavlidis & Floratos, 2021)

**Full citation:** A. Pavlidis and E. Floratos, "Quantum-Fourier-transform-based quantum arithmetic with qudits," Phys. Rev. A **103**, 032417 (2021); preprint arXiv:1707.08834, "Arithmetic circuits for multilevel qudits based on quantum Fourier transform."
**Source:** arXiv:1707.08834v2 (13 Sep 2017), QIC-style preprint. PDF: `pavlidis-2017-qudit-arithmetic-circuits-qft.pdf`

> Note: the PDF is the **2017 preprint version** (different title, QIC formatting). Table and equation numbers below are the preprint's; the PRA 103, 032417 version may renumber them. main.tex's bib entry already carries a `note` acknowledging the title change.

**Cited in main.tex:**
- *Introduction*: "Pavlidis and Floratos, citing qubit evidence that order finding tolerates truncation of small QFT rotations~\cite{barenco1996,nam2012}, conjecture 'a similar robustness' for qudits but leave its investigation open."
- *Introduction*: listed as the source of the "$O(d^2)$ two-level decomposition" entangling-gate cost model.
- *Introduction*: the native-gate cost requirement is "violated whenever qudit gates are compiled by two-level decomposition~\cite{pavlidis2021,gustafson2025synthesis}."
- *Gate-cost models*: `pavlidis` model = $d^2/4$ on two-qudit gates; justified because "the *controlled* rotations of the QFT-arithmetic circuits of Ref.~\cite{pavlidis2021} decompose into $4(d-1)^2$ elementary two-level gates, i.e. $(d-1)^2$ per gate after the same $d=2$ normalization, and our $d^2/4$ charge rounds that cost *down* — $2.25$ against $4$ at $d=3$, $6.25$ against $16$ at $d=5$; the same reference's Table 1 carries the $d^2$ factor in circuit *depth* as well ($8d^2q$ for the QFT, $4d^2q$ per adder)."
- *Hardware anchor*: a base-2 hardware datum described as "adjacent to the truncation-robustness conjecture for qudits~\cite{pavlidis2021}---which it cannot test directly."
- *Discussion*: "compiled modular arithmetic---depth $4d^2q$ per adder under two-level decomposition~\cite{pavlidis2021}."
- *Methods*: notes that an earlier version of the code wrongly applied the $d^2/4$ `pavlidis` multiplier to single-qudit gates, "that both the text and Ref.~\cite{pavlidis2021}'s construction reserve for controlled rotations."

**What the paper actually shows (full-text, not abstract-level):**
- **The $4(d-1)^2$ figure is exact and is for a *controlled* rotation.** Sec. 3.5.2 defines the two-qudit controlled-diagonal gate $CD_m(\phi_1,\ldots,\phi_{d-1})$ (block-diagonal $d^2\times d^2$, $D$ applied to the target iff control is in $|m\rangle$), and states: *"A construction of a $CD'_m(a_1,\ldots,a_{d-1})$ gate using $4(d-1)$ elementary $GCX^{(jk)}_{(m)}$ and $R_z^{(jk)}(\theta)$ gates is shown in Figure 2."* Then, Eq. (18) builds the QFT controlled rotation $R_k^{(d)}$ from $d-1$ such $CD^{(m)}$ gates, concluding: *"an $R_k^{(d)}$ gate requires $4(d-1)^2$ elementary gates."* At $d=2$ this is 4, so the $d{=}2$-normalized cost is $(d-1)^2$ → 4 at $d=3$, 16 at $d=5$, exactly as main.tex states.
- **Caveat on what "elementary" means:** the $4(d-1)$ per $CD$ is a *mixture* — from Fig. 2 the pattern per level $j$ is $R_z(a_j/2)$, $X^{(0j)}$, $R_z(-a_j/2)$, $X^{(0j)}$, so only **half** ($2(d-1)$ per $CD$, hence $2(d-1)^2$ per $R_k$) are the two-qudit $GCX$ entanglers; the rest are single-qudit $R_z$. main.tex charges the full $4(d-1)^2$-derived figure to two-qudit gates but then rounds it *down* to $d^2/4$, so the direction of the approximation is conservative — but a judge should confirm main.tex's phrase "elementary two-level gates" (which is the paper's own phrase) is not read as "elementary two-*qudit* gates."
- **Table 1 (p. 25), "Quantum cost, depth and width of the proposed arithmetic circuits":**

  | Circuit | Cost | Depth | Width |
  |---|---|---|---|
  | QFT | $4d^2q^2$ | $8d^2q$ | $q$ |
  | ADD | $4d^2q^2$ | $4d^2q$ | $2q$ |
  | MAC | $4d^2q^2$ | $4d^2q$ | $2q$ |
  | MULC | $24d^2q^2$ | $32d^2q$ | $2q$ |
  | MMAC | $7d^3q^3$ | $21d^3q^2$ | $3q$ |
  | SMAC | $14d^3q^3$ | $42d^3q^2$ | $4q$ |
  | $\Delta_q\gamma$ | $14d^3q^3$ | $42d^3q^2$ | $4q$ |

  Confirms main.tex's "$8d^2q$ for the QFT, $4d^2q$ per adder" exactly. Note the *quadratic-form* circuits (MMAC/SMAC/$\Delta_q\gamma$) carry $d^3$, not $d^2$ — a harsher $d$-dependence main.tex does not quote.
- **Authors' own caveats on the cost model (important):** immediately under Table 1 — *"The analysis assumes that single and two qudits gates are equivalent in terms of costs and execution time. Exact costs and depths depend on the particular implementations."* And in the conclusion (p. 27): *"because the exact cost depends on the exact technology used, which for qudits is at an early stage, the complexity analysis of section 7 is to be considered as a crude indicator of performance."*
- **The truncation-robustness conjecture (p. 26), verbatim:** *"Another advantage that has been observed in designs adopting the QFT method is their robustness to various kinds of deviations from the ideal operation. E.g. approximate QFT [50] or QFT banding is the design procedure of eliminating small angle rotation gates. Studies of the Shor's algorithm which uses the QFT showed that the algorithm still works sufficiently even when a large proportion of the QFT rotation gates are eliminated [22, 51, 52]. … The above results suggest that a similar robustness is expected in the multidimensional qudits case and further investigation to be carried."* — main.tex's quotation "a similar robustness" and "leave its investigation open" is verbatim-accurate.
- **The cited qubit evidence is exactly main.tex's `barenco1996` + `nam2012`:** Pavlidis's Ref. [22] = A. Barenco, A. Ekert, K.-A. Suominen, P. Törmä, *"Approximate quantum Fourier transform and decoherence,"* Phys. Rev. A **54**, 139 (1996); Ref. [52] = Y. S. Nam and R. Blümel, *"Performance scaling of Shor's algorithm with a banded quantum Fourier transform,"* Phys. Rev. A **86**, 044303 (2012). (Also [51] Fowler & Hollenberg 2004, [23] Nam & Blümel PRA 92, 042301 (2015), [53]/[54] Nam & Blümel PRA 88, 062310 and PRA 87, 060304.) main.tex's attribution chain is therefore exactly right.
- **Companion caveat the authors raise right after the conjecture:** truncation trades against "the requirement of reliable implementing high accuracy small angles rotation gates," and those gates must be fault-tolerant; approximation is possible "albeit with a cost" (Appendix B).
- The paper is **purely a circuit-synthesis/complexity paper**: no noise model, no simulation, no decoherence channel, no hardware fidelities. All arithmetic blocks (ADD, MAC, MULC, MMAC, SMAC, $\Delta_q\gamma$) are QFT-basis constructions; depths $O(q)$ or $O(q^2)$ in the register length via commuting-rotation reordering.
- Supporting count for the QFT block (p. 25 text): the QFT circuit needs $q$ Hadamards, $(q^2-q/2)(d-1)(2d-1)$ $GCX^{(jk)}_m$ gates and $(q^2-q/2)(d-1)2d$ $R_z^{(jk)}(\theta)$ gates.

**Judge verification questions:**
- Is main.tex's $4(d-1)^2$ figure quoted for the **controlled** rotation $R_k^{(d)}$ (correct), and does main.tex's "$(d-1)^2$ per gate after the same $d=2$ normalization → 4 at $d=3$, 16 at $d=5$" arithmetic check out against Pavlidis Sec. 3.5.2?
- Does main.tex's Table-1 quotation ($8d^2q$ QFT depth, $4d^2q$ adder depth) match Pavlidis Table 1 exactly, and does main.tex avoid implying the $d^2$ scaling extends to the quadratic-form blocks (which are $d^3$)?
- Does main.tex reproduce the "a similar robustness" conjecture and the "leave its investigation open" framing without overstating it into a *claim* by Pavlidis & Floratos?
- Does main.tex anywhere present the `pavlidis` cost model as a *measured* or *hardware-validated* cost, when the authors themselves call their complexity analysis "a crude indicator of performance" that assumes single- and two-qudit gates cost the same?
- Half the $4(d-1)$ elementary gates per $CD$ are single-qudit $R_z$, not entanglers. Does main.tex's charging of the whole figure to two-qudit gates (before rounding down to $d^2/4$) get flagged as conservative, or does it read as an overcharge?

---

---

## `peterer2015` — Coherence and decay of higher energy levels of a superconducting transmon qubit (Peterer *et al.*, 2015)

**Full citation:** M. J. Peterer, S. J. Bader, X. Jin, F. Yan, A. Kamal, T. Gudmundsen, P. J. Leek, T. P. Orlando, W. D. Oliver and S. Gustavsson, "Coherence and decay of higher energy levels of a superconducting transmon qubit," Phys. Rev. Lett. **114**, 010501 (2015); arXiv:1409.6031.
**Source:** PRL 114, 010501 (2015). PDF: `peterer-2014-higher-levels-transmon-coherence.pdf`

**Cited in main.tex:**
- *Introduction*: one of five refs for "an anharmonic-ladder channel calibrated to published per-level transmon coherence measurements."
- *Noise channels*: one of six refs supporting "the relaxation ratio $\Gamma_2/\Gamma_1$ is measured at $\approx1.7$ … against $2.0$ for the textbook $\Gamma_k\propto k$ ladder"; also in the group underpinning the dephasing ratios $\Gamma_\phi^{01}:\Gamma_\phi^{12}:\Gamma_\phi^{02} = 1:2.0:2.3$ and the charge-dispersion explanation ("the charge dispersion of $|2\rangle$ exceeds that of $|1\rangle$ by an order of magnitude").
- *Robustness*: singled out as a **dissenting** measurement — "Peterer *et al.*, who measured the sequential ladder to the fourth level, disagree in both places: their $T_1$ series gives $\Gamma_{21}/\Gamma_{10}=2.05$ (i.e. $k^{1.0}$, not $k^{0.7}$), and their $T_2$ series gives pair rates $1:2.25:6.0:{>}36$ against $1:2.14:3.35:4.59$ under the max-level law. No power law fits that escalation…"

**What the paper actually shows (full-text, not abstract-level):**
- **Device**: a single 3D-cavity transmon, $E_J = 14.07$ GHz, $E_C = 243$ MHz, $E_J/E_C = 58$; $f_{01}=4.9692$ GHz, $f_{12}=4.6944$, $f_{23}=4.3855$, $f_{34}=4.0280$ GHz; anharmonicities $\alpha_{12}=274.8$, $\alpha_{23}=583.7$, $\alpha_{34}=941.2$ MHz. Levels $|0\rangle$–$|4\rangle$ prepared and characterized ($d$ up to 5 levels). **$n=1$ device.**
- **Table I, sequential relaxation times $\Gamma_{ij}^{-1}$:** $\Gamma_{10}^{-1}=84\pm0.24\,\mu$s, $\Gamma_{21}^{-1}=41\pm0.21$, $\Gamma_{32}^{-1}=30\pm0.21$, $\Gamma_{43}^{-1}=22\pm2\,\mu$s.
  → **$\Gamma_{21}/\Gamma_{10}=84/41=2.05$** — main.tex's number is exact. Full rate series normalized: $1 : 2.05 : 2.80 : 3.82$ (vs $1:2:3:4$ for $k^{1.0}$, vs $1:1.62:2.16:2.64$ for $k^{0.7}$). So $k^{1.0}$ is the closer fit at $k=2$ but the series *sub*-scales at $k=3,4$.
- Authors' own statement: *"For the sequential rates, we find that the rates scale linearly with state $i$"* (Fig. 2(d)), consistent with electric-field-fluctuation (Purcell/dielectric) processes for which lifetimes go as $|\langle i|\hat n|j\rangle|^{-2}$, and with quasiparticle tunnelling giving $\Gamma_{i,i-1}\simeq i\,\Gamma_{10}$. They note the weak anharmonicity makes the decay rates scale like harmonic-oscillator Fock states.
- **Non-sequential rates are strongly suppressed** (~2 orders of magnitude): $\Gamma_{20}^{-1}=1812\pm223$, $\Gamma_{31}^{-1}=1314\pm359$, $\Gamma_{30}^{-1}=2631\pm694\,\mu$s — parity selection rules suppress $\Gamma_{20},\Gamma_{31}$; $|\langle3|\hat n|0\rangle|^2$ is ~100× smaller than $|\langle1|\hat n|0\rangle|^2$.
- **Table I, dephasing times $T_2(ij)$ (accurate to $\pm20\%$):** $T_2(01)=72$, $T_2(12)=32$, $T_2(23)=12$, $T_2(34)<2\,\mu$s.
  → normalized pair *rates*: $1 : 72/32 = 2.25 : 72/12 = 6.0 : >72/2 = 36$. **main.tex's "$1:2.25:6.0:{>}36$" is exact.**
  → max-level law $\max(j,k)^{1.1}$ predicts $1^{1.1}:2^{1.1}:3^{1.1}:4^{1.1} = 1:2.14:3.35:4.59$ — **main.tex's comparison numbers are exact.**
- **Important methodological caveat on those $T_2$ values:** they are **Ramsey ($T_2^\ast$)** values fit to an *exponentially* damped double sine, $A = e^{-t/T_2}[\cos(2\pi f_A t) + \cos(2\pi(f_A+\Delta f)t)]$ (SM Eq. 7), with $[f_A,\Delta f] = [379\,\text{kHz}, 0]_{(01)}$, $[504, 93]_{(12)}$, $[1.1\,\text{MHz}, 2.5\,\text{MHz}]_{(23)}$. The charge-dispersion splitting is fit as the **beat frequency $\Delta f$**, not as the decay envelope. For $|4\rangle$ the Ramsey PSD shows "a number of frequencies" (unresolved multi-component dispersion), which is why $T_2(34)$ is only bounded ($<2\,\mu$s) — so the "$>36$" leg of the escalation may partly reflect unresolved beating rather than pure dephasing.
- **The authors explicitly note the dominant noise is refocusable:** *"for quantum information purposes, the noise causing the beating in the Ramsey fringes can be refocused with an echo sequence by adding a temporally short $\pi$-pulse … to the center of the Ramsey sequence."* Supplement: in a different cooldown the same transmon gave $T_2^\ast = 90\text{–}115\,\mu$s and echo $T_{2E} = 154\,\mu$s — i.e. $T_2(01)=72\,\mu$s in Table I is not a stable device constant and echo more than doubles it.
- **Charge dispersion (mechanism for the non-textbook dephasing law), Table I:** measured splittings $\epsilon_{ij}$: $|1\rangle$ **unresolved**, $|2\rangle$ = 0.09 MHz, $|3\rangle$ = 2.53 MHz, $|4\rangle$ = 5–10 MHz. Simulated maxima $\epsilon^{(\max)}_{ij}$: $|1\rangle$ = 0.0025, $|2\rangle$ = 0.091, $|3\rangle$ = 1.89, $|4\rangle$ = 26.8 MHz. → **simulated $|2\rangle/|1\rangle \approx 36\times$**, i.e. *more* than the "order of magnitude" main.tex claims; the measured $|1\rangle$ value is only an upper bound because it is unresolved. Authors: "the charge dispersion approximately grows in an exponentially way with increasing level number."
- Abstract-level headline the paper itself emphasizes: relaxation and coherence times "in excess of 20 $\mu$s for all transitions" up to $|4\rangle$.
- **Not measured by this paper:** $T_2(02)$ (so no direct $\Gamma_\phi^{02}$ datum), any $d>5$ level, any two-qudit gate, any echo-based per-level $T_2$, and any second device.

**Judge verification questions:**
- Do main.tex's four quoted Peterer numbers reproduce Table I exactly: $\Gamma_{21}/\Gamma_{10} = 84/41 = 2.05$, and the $T_2$-derived pair rates $1:2.25:6.0:{>}36$ from $T_2 = 72/32/12/{<}2\,\mu$s? (Both check out.)
- main.tex's *Noise channels* section puts `peterer2015` in the list supporting "$\Gamma_2/\Gamma_1 \approx 1.7$," while its *Robustness* section says Peterer gives $2.05$ and "disagrees." Is the Noise-channels citation list presented as an **aggregate fit across nine devices** (so an outlier member is fine), or does it read as claiming Peterer measured 1.7? Only the aggregate reading is defensible.
- Does main.tex flag that the Peterer $T_2$ values are Ramsey $T_2^\ast$ with the charge-dispersion splitting fit as a *beat frequency* (exponential envelope, not Gaussian), and that $T_2(34)$ is only an upper bound? main.tex's Robustness argument turns on whether pair ratios were "extracted from Ramsey decay in a quasi-static-dominated regime" — Peterer's fit form is exponential, which cuts against that framing for this dataset.
- Is "the charge dispersion of $|2\rangle$ exceeds that of $|1\rangle$ by an order of magnitude" supported? Simulation gives $\approx36\times$ ($0.091$ vs $0.0025$ MHz) and $|1\rangle$ is experimentally unresolved — so the claim is true but understated, and rests on simulated rather than measured $|1\rangle$ dispersion.
- Does main.tex acknowledge this is a **single device** with $T_2^\ast$ varying 72 → 90–115 $\mu$s between cooldowns and echo $T_{2E}=154\,\mu$s, when using it as a per-level coherence calibration anchor?

---

---

## `ringbauer2022` — A universal qudit quantum processor with trapped ions (Ringbauer *et al.*, 2022)

**Full citation:** M. Ringbauer, M. Meth, L. Postler, R. Stricker, R. Blatt, P. Schindler and T. Monz, "A universal qudit quantum processor with trapped ions," Nat. Phys. **18**, 1053 (2022); arXiv:2109.06903.
**Source:** Nat. Phys. 18, 1053 (2022). PDF: `ringbauer-2021-universal-qudit-ion-processor.pdf` (arXiv:2109.06903v1, 14 Sep 2021 — preprint; main text + Supplementary Information)

**Cited in main.tex (17 contexts, kept distinct):**
1. *Introduction*: among platforms where "processors that exploit them as qudits now exist or are proposed."
2. *Introduction*: source for "a per-particle depolarizing channel representative of trapped-ion qudits" (with `low2023`).
3. *Introduction*: source of "the measured trapped-ion $2(d{-}1)$ Mølmer–Sørensen cost" underlying the `ion` cost model.
4. *Noise channels*: "the single-qudit *per-pulse* error is nearly flat in $d$ ($2.0\times10^{-4}$ at $d=3$, $3.2\times10^{-4}$ at $d=5$; the per-*Clifford* error rises $5\times$, $2\times10^{-3}$ to $1.0\times10^{-2}$, because a $d=5$ Clifford takes ${\sim}3\times$ the pulses)."
5. *Noise channels*: "ion two-qudit entangling gates at … $2.5\times10^{-2}$–$6.2\times10^{-2}$ at $d=3$ (decomposed)."
6. *Noise channels*: "only single-qudit pulses reach the $10^{-3}$–$10^{-4}$ scale" (with `low2023`).
7. *Gate-cost models*: "the supplement of Ref.~[ringbauer2022] decomposes a $d$-dimensional controlled-increment into $2(d{-}1)$ pairwise fully entangling gates, which we normalize to $1$ at $d=2$ … the same reference's main text quotes $2d$ MS gates for the Cinc and a $d$-*independent* two-gate cost for the controlled-exchange."
8. *Gate-cost models*: "All three models charge a *single*-qudit gate one layer at every $d$, which matches the per-pulse benchmarking of Ref.~[ringbauer2022] but not its per-Clifford figures."
9. *The cost condition*: "measured qudit entangling gates stop at $d=5$~[hrmo2023] (Ringbauer's are characterized at $d=3$)."
10. *Robustness*: "Per laser pulse that matches Ref.~[ringbauer2022]; per *operation* it does not, since the same device's randomized benchmarking gives a per-Clifford error rising $5\times$ from $d=3$ to $d=5$ on ${\sim}3\times$ the pulses."
11. *Robustness*: Zeeman-structured dephasing "carrying the collective-$B$ sensitivity structure of the $^{40}$Ca$^{+}$ level indexing of Ref.~[ringbauer2022] … $\propto\mathrm{diag}(g_j m_j)$ ($g_S=2$, $g_D=6/5$)."
12. *Robustness*: "shielding makes coherence times of order $100$ ms achievable across all transitions."
13. *Robustness*: "The device's randomized benchmarking---per-pulse error rising only $1.6\times$ from $d=3$ to $d=5$ ($2.0\times10^{-4}$ to $3.2\times10^{-4}$) where the raw sensitivity ratio is $25$–$49$."
14. *Discussion*: "eigenstate QPE at $m=2$–$3$ on a Ringbauer-class ion processor, where multi-qudit entangling algorithms have been demonstrated at $d=3$ and $d=5$" (the $d=5$ demo attributed to `meth2025`).
15. *Discussion (i)*: "at the measured per-Clifford error ($2\times10^{-3}$ at $d{=}3$)."
16. *Discussion (ii)*: "Readout: $d{-}1=2$ sequential shelving rounds at ${\sim}3\times10^{-3}$ worst-case misassignment each, plus ${\sim}3$ ms of detection and re-cooling idle per round."
17. *Discussion (iii)* and *Table `tab:prediction`* caption: "Cross-talk: residual ${\sim}2\times10^{-3}$ per gate, largely coherent (state-dependent AC-Stark shifts on occupied higher levels)"; and "sequential-shelving readout adds up to $d-1$ detection rounds at ${\sim}3\times10^{-3}$ worst-case qudit error."

**What the paper actually shows (full-text, not abstract-level):**
- **Platform/encoding**: string of $^{40}$Ca$^+$ ions in a linear Paul trap; information in $S_{1/2}$ (Zeeman $m=\pm1/2$) and metastable $D_{5/2}$ ($m=\pm5/2,\pm3/2,\pm1/2$), $\tau_1\sim1.1$ s; ~4 G field; 10 allowed $S\!\leftrightarrow\!D$ quadrupole transitions ($\Delta m = 0,\pm1,\pm2$) all driven by one 729 nm laser. **8 levels natively; qudit dimension demonstrated up to $d=7$** (one level must remain unoccupied for the sequential readout).
- **Magnetic sensitivity (bears on citation 11/13):** *"These transitions differ in their sensitivity to magnetic field fluctuations by up to a factor of 5, such that optical qubits are typically encoded in the least sensitive states $|0\rangle = S_{1/2,-1/2}$, $|1\rangle = D_{5/2,-1/2}$."* — the paper gives the level scheme and the **factor-5 sensitivity spread**, but it does **not** print $g_S=2$ or $g_D=6/5$ anywhere; those are standard $^{40}$Ca$^+$ Landé values supplied by main.tex. main.tex's "$1$–$25\times$ at $d=3$ and $1$–$49\times$ at $d=5$" rate spreads are main.tex's own derivation ($25 = 5^2$ is consistent with the paper's factor-5 sensitivity via rate $\propto$ sensitivity$^2$; $49 = 7^2$ exceeds the paper's stated factor-5 bound and comes from main.tex's $g_j m_j$ construction, not from Ringbauer).
- **Coherence (citation 12):** *"with magnetic shielding, spin coherence times on the order of 100 ms, which is at least 3 orders of magnitude larger than typical gate times, can be achieved for all transitions."* Note this is stated as *achievable with shielding*, not as a measurement on the device reported here. Separately, "All operations can be performed with error rates below 1% and at least 3 orders of magnitude faster than the coherence time."
- **Single-qudit randomized benchmarking (citations 4, 8, 10, 13, 15), Fig. 2:**
  - qutrit ($d=3$): average error **$2(2)\cdot10^{-3}$ per Clifford**, corresponding to **$2.0^{+0.8}_{-0.5}\cdot10^{-4}$ per laser pulse**.
  - ququint ($d=5$): average error **$1.0(2)\cdot10^{-2}$ per Clifford**, corresponding to **$3.2^{+0.8}_{-0.7}\cdot10^{-4}$ per laser pulse**.
  - Derived: per-Clifford ratio $= 5.0\times$; per-pulse ratio $= 1.6\times$; implied pulses per Clifford $= 10$ ($d{=}3$) vs $31.25$ ($d{=}5$), i.e. $\approx3.1\times$. **Every one of main.tex's numbers in citations 4/10/13/15 is exact.**
  - Uncertainties are large: $2(2)\cdot10^{-3}$ is a 100% relative error bar on the qutrit Clifford figure; at least 20 random sequences per length, median-fit with 99% CIs.
  - Single-qudit gates need "at most $O(d^2)$ two-level rotations" via Givens decomposition (SM).
- **Two-qudit entangling gates (citations 5, 7, 9), Fig. 3:**
  - **Cex** (controlled-exchange, Cnot embedded in a qudit space): SPAM-free fidelity **$F = 97.5(2)\%$** → infidelity $2.5\times10^{-2}$.
  - **Cinc** (controlled-increment): **$F = 93.8(2)\%$** → infidelity $6.2\times10^{-2}$.
  - **Both characterized in a *qutrit* Hilbert space** (Fig. 3 caption: "Fidelity decays for a Cex gate in a qutrit Hilbert space, and a qutrit Cinc gate"). **No two-qudit gate is characterized at $d=5$ or above in this paper.** main.tex's caveat "Ringbauer's are characterized at $d=3$" is correct.
  - **Main text gate counts:** *"for the Cex gate we find a decomposition into 2 two-level MS gates independent of qudit dimension, and for the Cinc gate we require $2d$ MS gates."*
  - **Supplement gate count** (SI, "Decomposition of the CINC gate"): *"This decomposition achieves a $d$-dimensional Cinc gate, using $2(d-1)$ pairwise fully entangling gates, see Fig. S8."* — **main.tex's $2(d-1)$ is verbatim from the SM, and main.tex correctly flags the main-text/SM discrepancy ($2d$ vs $2(d-1)$).** Note a further internal tension: the fully-compiled qutrit circuit drawn in Fig. S8(b) shows only **two** MS gates ($\mathrm{MS}_{01}$, $\mathrm{MS}_{12}$), whereas $2(d-1)=4$ at $d=3$ — a judge may want to note this is an ambiguity in the source, not in main.tex.
  - The authors explicitly note the alternative: *"one could directly generalize the MS gate to a native qudit gate by driving multiple transitions simultaneously. This reduces the gate count, however, only at the cost of increased complexity of the classical control system and more challenging experimental calibration [ref to Low et al.]."* — i.e. Ringbauer's construction is the *decomposed* route, not the native-entangler route, which is exactly how main.tex uses it (the `ion` model, not `uniform`).
  - Addressed MS-gate fidelity in the qubit subspace (SI Fig. S3): **0.993 ± 0.002 in a 3-ion string, 0.983 ± 0.002 in a 10-ion string.**
- **Readout (citation 16, 17b), Fig. 4:** sequential electron-shelving scheme — shelve $|2\rangle$ to $D$, fluorescence-read (projects onto $\{|0\rangle\langle0|, 1-|0\rangle\langle0|\}$), reordering pulse, read again; repeat until all ions have been bright. *"leading to a qutrit readout error of $\sim99.7\%$ for $500\,\mu$s detection time and $2500\,\mu$s re-cooling time"* (sic — fidelity 99.7%, i.e. error $3\times10^{-3}$; Fig. 4(c) caption confirms "an optimum of $3\cdot10^{-3}$ for $\sim500\,\mu$s detection time"). $500 + 2500\,\mu$s $= 3$ ms per round — **main.tex's "$\sim3$ ms of detection and re-cooling idle per round" is exact.** The authors state *"this is a worst-case error, since those states measured earlier will experience lower spontaneous decay errors than those measured later"* — matching main.tex's "worst-case misassignment." Readout time "increases only linearly in qudit dimension"; the qutrit case uses 2 detections (Fig. 4(c) dotted line), consistent with main.tex's $d-1$ rounds. The authors add that readout error "can be reduced by an order of magnitude using improved collection optics and fast re-cooling techniques."
- **Cross-talk (citation 17a), SI "Off-resonant operations":** composite pulse sequence $R(\theta,\phi) = Z(\pi)-R(-\theta/2,\phi)-Z(\pi)-R(\theta/2,\phi)$ *"suppresses cross-talk to $\sim2\cdot10^{-3}$ (from $\sim4\%$ for a resonant operation), which is on the same order of magnitude as the benchmarked gate error rate from Fig. 2. This could be further reduced by several orders of magnitude with improved addressing optics."* The mechanism is AC-Stark: *"when more than two states are occupied, the effect of off-resonant laser interaction is more complex, as each state acquires a different AC-Stark shift due to varying detunings and coupling strengths"* (SI Eq. S2), and *"for a system with $d$ occupied levels, a multi-chromatic off-resonant light field with $(d-1)$ tones can, in principle, exactly compensate all level shifts, but one … each such beam contains $2\cdot(d-2)$ coupled parameters, which can make their experimental calibration challenging."* — **fully supports main.tex's "largely coherent (state-dependent AC-Stark shifts on occupied higher levels) … in principle calibratable, so it enters as a calibration requirement rather than a decoherence rate."**
- **What the paper does NOT contain (relevant to citations 2, 14):** no depolarizing-channel model, no per-level $T_1$/$T_2$ measurement, no $d$-resolved Ramsey/echo coherence data, no noise simulation, no algorithm run (no QPE, Grover, or order finding), and **no multi-qudit entangling demonstration at $d=5$** — the highest-$d$ entangling result here is $d=3$. The paper's own listed open problems: "low cross-talk errors due to the large number of local operations required, and fast re-cooling and readout capabilities to reduce SPAM errors," a larger magnetic field for spectral separation, "compiling quantum algorithms into the qudit framework," and complementing "the embedded two-level entangling gates we presented with a suite of genuine qudit entangling gates."

**Judge verification questions:**
- Do main.tex's RB numbers match Fig. 2 exactly — $2(2)\cdot10^{-3}$ / $2.0\cdot10^{-4}$ ($d{=}3$) and $1.0(2)\cdot10^{-2}$ / $3.2\cdot10^{-4}$ ($d{=}5$), giving $5\times$ per-Clifford, $1.6\times$ per-pulse, $\approx3\times$ pulses-per-Clifford? Does main.tex anywhere quote these without the paper's very large uncertainty on the qutrit Clifford figure ($\pm100\%$)?
- Is main.tex's `ion` cost model correctly sourced to the **Supplement**'s $2(d-1)$ rather than the main text's $2d$, and does main.tex explicitly note the discrepancy? Does main.tex's $d{=}2$ normalization ("the $d{=}2$ MS gate being itself the two-pulse unit") follow from $2(d-1)|_{d=2}=2$?
- Are the two-qudit infidelities $2.5\times10^{-2}$ (Cex) and $6.2\times10^{-2}$ (Cinc) correctly labelled by main.tex as **$d=3$-only, decomposed** gates — and does main.tex avoid implying Ringbauer measured any two-qudit gate at $d\geq5$?
- Does main.tex's Zeeman-dephasing construction ($g_S=2$, $g_D=6/5$, rate spreads $1$–$25\times$ at $d{=}3$ and $1$–$49\times$ at $d{=}5$) claim more from Ringbauer than the paper supplies? The paper gives the level *indexing* and a "**up to a factor of 5**" sensitivity spread; it prints no $g$-factors and no $d$-resolved rate spread. Is main.tex's phrasing ("carrying the collective-$B$ sensitivity structure of the $^{40}$Ca$^{+}$ level indexing of Ref.~[ringbauer2022]") narrow enough, and is the $49\times$ (implying a sensitivity ratio of 7) reconcilable with the paper's factor-5 statement?
- Is "shielding makes coherence times of order $100$ ms achievable across all transitions" quoted with the paper's conditional framing ("with magnetic shielding … can be achieved"), rather than as a measured coherence time on the device reported?
- Are the readout figures right: $\sim3\times10^{-3}$ **worst-case** qutrit misassignment, $500\,\mu$s detection $+\ 2500\,\mu$s PGC re-cooling $= 3$ ms per round, $d-1$ rounds, readout time linear in $d$? Does main.tex carry the paper's own note that this is improvable by an order of magnitude with better optics?
- Is the cross-talk figure right ($\sim2\times10^{-3}$ residual after composite pulses, down from $\sim4\%$ resonant), and is main.tex's "largely coherent … in principle calibratable" supported by SI Eq. (S2) and the $(d-1)$-tone compensation discussion?
- In the Discussion, does main.tex avoid attributing the $d=5$ multi-qudit entangling demonstration to `ringbauer2022`? (Ringbauer's highest-$d$ entangling result is $d=3$; the $d=5$ claim is carried by `meth2025`.) Does "Ringbauer-class ion processor" read as a hardware-class statement rather than a claim about this paper's own demonstrations?
- Does main.tex justify calling a **per-particle depolarizing channel** "representative of trapped-ion qudits~\cite{ringbauer2022,low2023}" when Ringbauer reports no noise model, no per-level coherence, and no depolarizing characterization — only RB error rates and gate fidelities?

---

## `robert2026` — Qudit encoding in Rydberg blockaded arrays of atoms (Robert & Bienaimé, 2026)

**Full citation:** A. Robert and T. Bienaimé, "Qudit encoding in Rydberg blockaded arrays of atoms," Phys. Rev. A **113**, 062614 (2026).
**Source:** arXiv:2502.06465 (v3, 17 Jun 2026); Phys. Rev. A 113, 062614. PDF: `robert-2025-qudit-encoding-rydberg-blockaded-arrays.pdf`

**Cited in main.tex:**
- *Introduction* (line 75): listed among platforms that "expose more than two usable levels, and processors that exploit them as qudits now exist **or are proposed**" — Rydberg-blockaded atom arrays.
- *Robustness* (line ~2041): "an independent Rydberg-superatom qudit encoding derives its generalized Fourier gate at $\sim(d/2)^2$ laser pulses — $\alpha=2$ by construction, **before any entangling gate exists on that platform**." Used as independent corroboration that a single-qudit gate cost exponent $\alpha=2$ is not an ion-specific artifact.

**What the paper actually shows (full-text, not abstract-level):**
- **It is a theory/proposal paper, not an experiment.** All fidelities are from numerical simulation of the pulse sequences (matrix exponentiation of the exact Hamiltonian $\hat H_0+\hat H_c$). No hardware was run. The Introduction's citation "exist **or are proposed**" therefore covers it correctly; a claim that Rydberg qudit *processors exist* would not.
- **Qudit dimension is $d = 2N$**, where $N$ = number of blockaded three-level atoms. Hilbert space $\mathcal{H}'$ = dressed states $\{|\pm,q\rangle\}_{q=1..N}$, dimension $2N$; the full space $\mathcal{H}$ including $|g,0\rangle$ has $2N+1$ levels (Sec. III).
- **Pulse-count scaling (the load-bearing fact for the $\alpha=2$ claim), Sec. VI:** "Any nontrivial target phase gate requires $\sim N$ pulses while the Hadamard gate and more complex gates need the sequential application of $2N$ phase gates leading to a **total number of pulses $\sim N^2$**." Substituting $N=d/2$ gives exactly $\sim(d/2)^2$ — main.tex's number is a correct and direct restatement.
- **The gate main.tex calls the "generalized Fourier gate" is the paper's "generalized Hadamard gate"** (Sec. V B), defined as $\hat U_{\rm Had}: |q_j\rangle \mapsto \frac{1}{\sqrt{2N}}\sum_{p=1}^{2N} e^{i\frac{\pi}{N}(j-1)(p-1)}|q_p\rangle$. Since $e^{i\pi(j-1)(p-1)/N} = e^{2\pi i (j-1)(p-1)/(2N)} = e^{2\pi i (j-1)(p-1)/d}$, this matrix **is literally the $d$-dimensional DFT/QFT**. Calling it a generalized Fourier gate is accurate, though the paper never uses that phrase.
- **No entangling gate exists in this work.** Conclusion (Sec. VIII): "Possible extensions of this work include the development of **entangling two qudit gates** [40, 41] which would enable universal quantum computation with this platform." The protocol is single-(super)qudit only. main.tex's "before any entangling gate exists on that platform" is correct.
- **Infidelity scaling** (Sec. VI): per-pulse error $\sim N\Omega_{01}^2/\Omega_{1r}^2$; total $\sim N^2\Omega_{01}^2/\Omega_{1r}^2$ for the generalized phase gate and $\sim N^3\Omega_{01}^2/\Omega_{1r}^2$ for the Hadamard. Note the *infidelity* exponent (3 in $N$) differs from the *pulse-count* exponent (2 in $N$); main.tex charges pulses, matching the $N^2$ figure.
- **Concrete simulated numbers:** gate infidelity $9\times10^{-5}$ for $\Omega_{01}/\Omega_{1r}=10^{-3}$ at $N=7$ (14-level qudit), Fig. 3; infidelity $3\times10^{-2}$ at $\Omega_{01}/\Omega_{1r}=0.004$, $N=7$ (Fig. 4b, parameters deliberately chosen to make imperfections visible).
- **Rydberg-decay ceiling on $d$** (Sec. VII), with $\Gamma_r^{-1}=100\,\mu$s and $\Omega_{1r}/2\pi = 25$ MHz: complex gates (Hadamard) feasible up to a **14-level qudit ($N=7$)**; generalized phase gates up to **24 levels (12 atoms)**; arbitrary state preparation up to **340 levels (170 atoms)**. Total sequence durations scale $T_{\rm tot}\sim N/\Omega_{01}$ (state prep), $N^2/\Omega_{01}$ (phase gate), $N^3/\Omega_{01}$ (Hadamard).
- **Authors' own caveats:** the protocol is *approximate* (built from an effective Hamiltonian $\hat H_{\rm eff}$, so nonresonant terms cause the gate errors); works best only in the regime $\Omega_{01}/\Omega_{1r}\ll 1$; requires a well-controlled atom number (tweezer arrays, not thermal ensembles/Mott insulators, because collective parameters $K_N^q, Q_N^q$ depend on $N$); laser phase noise, Doppler shifts, and intermediate-state spontaneous emission are explicitly **not** included and are flagged as needing future study.

**Judge verification questions:**
- Does main.tex's "$\sim(d/2)^2$ laser pulses" match the paper's "$\sim N^2$ pulses" under the paper's own $d=2N$ encoding? (It does — confirm main.tex has not conflated $d=N$ with $d=2N$, which would change the constant.)
- Does main.tex anywhere imply this is an *experimental* pulse-count measurement rather than a theoretical construction ("by construction" suggests it does not — verify)?
- Is "before any entangling gate exists on that platform" supported? Check that main.tex does not elsewhere cite `robert2026` for two-qudit or entangling capability.
- Does the Introduction's list wording ("exist **or are proposed**") preserve the proposal-only status of this reference, or does main.tex imply a Rydberg qudit processor has been built?
- Does main.tex conflate the pulse-count exponent ($N^2$) with the infidelity exponent ($N^3$)? The paper gives both; only the former supports $\alpha=2$.

---

---

## `roy2022` — Realization of two-qutrit quantum algorithms on a programmable superconducting processor (Roy, Li, Kapit & Schuster, 2022)

**Full citation:** T. Roy, Z. Li, E. Kapit, and D. I. Schuster, "Realization of two-qutrit quantum algorithms on a programmable superconducting processor," arXiv:2211.06523 (2022).
**Source:** arXiv:2211.06523v1 (12 Nov 2022). PDF: `roy-2022-two-qutrit-algorithms-superconducting.pdf`

**Cited in main.tex:**
- *Discussion* (line ~2414): grouped as evidence that "multi-qudit entangling algorithms have been demonstrated at $d=3$ and $d=5$ … earlier $d=3$ circuit work in Refs.~\cite{roy2022,shi2025}."

**What the paper actually shows (full-text, not abstract-level):**
- **Fully programmable two-qutrit ($d=3$, 9-dimensional Hilbert space) superconducting processor** built from the lowest three levels of two transmons (Q1, Q2), coupled by a SQUID-based parametric coupler. This is genuinely **multi-qudit and entangling** — exactly what main.tex's clause asserts.
- **Algorithms demonstrated, all ancilla-free:** Deutsch–Jozsa, Bernstein–Vazirani, and Grover's search. The authors claim "to our knowledge, ours is the **first successful demonstration of a qutrit-based Grover's search** across any quantum computing platform."
- **Measured success probabilities (measurement-error corrected, 20,000 repetitions per oracle):**
  - Deutsch–Jozsa: 75.5(3)% constant oracles (per-output: 72.8(3)%, 76.5(3)%, 77.2(3)%), 98.5(1)% balanced oracles; classical baseline 50%.
  - Bernstein–Vazirani: 78.3(3)% average over 9 strings; classical 33.3%.
  - Grover (N=9): **44.4(3)% after round 1, 49.6(3)% after round 2**, versus classical 11.1% and 22.2%. Theoretical ideal is 72.6% and 98.4% — so the experiment lands well below ideal, though above classical.
- **Native entangling gates:** $C_p(\pi,|22\rangle)$ via a 94 ns $2\pi$-pulse on the $|22\rangle\!\leftrightarrow\!|31\rangle$ red sideband; $C_p(\pi,|21\rangle)$ via a 56 ns $2\pi$-pulse on $|21\rangle\!\leftrightarrow\!|30\rangle$. A native $C_p(\pi,|12\rangle)$ exists but is avoided for lower fidelity. Bosonic enhancement makes $C_p(\pi,|22\rangle)$ twice as fast as $C_p(\pi,|11\rangle)$.
- **Qudit-vs-qubit gate-count argument:** "During a similar search using three qubits ($N=8$), each oracle (and amplification) step requires eight CNOT gates (for a linear chain), resulting in an **eight-fold rise in entangling operations** compared to our efficient two-qutrit implementation."
- **Single-qutrit gate costs (Appendix A):** $H$ needs 3 physical pulses, $X$ needs 2, $Z$ needs 0 (virtual, ~100% fidelity). $H$ process fidelities 98.96% (Q1) / 97.06% (Q2); $Z$ 97.48% / 96.76% (SPAM-limited). Gate durations: $\pi_{01}\approx95$ ns, $\pi_{12}\approx79$–84 ns, $H\approx142$–148 ns.
- **Coherence (Table II) — the key caveat, and directly relevant to a decoherence paper:** Q1: $T_1^{01}=47.9\,\mu$s, $T_1^{12}=21.7\,\mu$s, $T_{2R}^{01}=4.5\,\mu$s, $T_{2R}^{12}=2.0\,\mu$s. Q2: $T_1^{01}=35.1\,\mu$s, $T_1^{12}=3.9\,\mu$s, $T_{2R}^{01}=3.2\,\mu$s, $T_{2R}^{12}=2.4\,\mu$s. The authors state performance is **"dephasing limited"** and matches a master-equation simulation. Note the strong **level-dependent degradation** ($T_1^{12}\ll T_1^{01}$, especially Q2) — this is exactly the "anharmonic ladder / max-level" structure main.tex models elsewhere, so this reference is corroborative on that point too.
- **Authors' own caveats:** degradation for target states closer to $|00\rangle$ is due to less-efficient oracle decompositions (more single-qutrit rotations); $|02\rangle$ and $|12\rangle$ did not improve after round 2, attributed to the shorter lifetime of Q2's $|2\rangle$ level.

**Judge verification questions:**
- Is `roy2022` correctly characterized as **multi-qudit entangling** $d=3$ circuit work? (Yes — two transmon qutrits with native two-qutrit CPhase gates; confirm main.tex's clause does not imply single-qudit.)
- Is "earlier" accurate relative to `meth2025` and `ringbauer2022`? (roy2022 is Nov 2022; check the chronology main.tex asserts.)
- Does main.tex claim any specific numeric success probability from `roy2022`? If so, does it match 44.4(3)% / 49.6(3)% (Grover) or 75.5/98.5% (DJ) or 78.3% (BV) — and does it note these are measurement-error-corrected?
- This is a superconducting (transmon) platform, not a trapped ion. Does main.tex's sentence — which sets the scene on "a Ringbauer-class ion processor" — risk implying `roy2022` was done on an ion processor?

---

---

## `rubinosanz2025` — Implementation of the Quantum Fourier Transform on a molecular qudit with full refocusing and state tomography (Rubín-Osanz et al., 2025)

**Full citation:** M. Rubín-Osanz, L. Bersani, S. Chicco, G. Allodi, R. De Renzi, A. Mavromagoulos, M. D. Roy, S. Piligkos, E. Garlatti, and S. Carretta, "Implementation of the Quantum Fourier Transform on a molecular qudit with full refocusing and state tomography," arXiv:2512.15611 (2025).
**Source:** arXiv:2512.15611v1 (17 Dec 2025). PDF: `rubinosanz-2025-qft-molecular-qudit.pdf`

**Cited in main.tex:**
- *Robustness* (line ~1596): "dynamical decoupling suppresses dephasing — the part of the ladder channel scaling worst with $d$ (the max-level law) — and leaves the gentler $k^{0.7}$ relaxation, **in agreement with** qudit DD experiments~\cite{tripathi2025} and with the **refocused molecular-qudit QFT** of Ref.~\cite{rubinosanz2025}." Supports the conclusion that "refocusing buys roughly one cost model of headroom, and benchmarks of qudit algorithms should be run on refocused devices."

**What the paper actually shows (full-text, not abstract-level):**
- **Platform:** isotopically enriched $^{173}$Yb(trensal) single crystal, magnetically diluted to 0.05% in diamagnetic Lu(trensal). Effective electronic $S=1/2$ coupled to nuclear $I=5/2$ → **12 total energy levels available**. Hyperfine constants $A_\parallel=-883$ MHz, $A_\perp=-628$ MHz, quadrupolar $p=-66$ MHz.
- **CRITICAL SCOPE LIMIT: the QFT was implemented on a $d=3$ (qutrit) subspace only**, not on the full $d=12$ manifold. States $|0\rangle=|+\tfrac12,+\tfrac12\rangle$, $|1\rangle=|+\tfrac12,-\tfrac12\rangle$, $|2\rangle=|+\tfrac12,-\tfrac32\rangle$, with $f_{01}=333.0$ MHz, $f_{12}=359.9$ MHz — chosen because they were the only transitions inside the 320–370 MHz probe bandwidth. **The paper therefore contains no $d$-scaling data whatsoever**; generalization to $d>3$ is stated as future work ("can be generalized to qudits with $d>3$").
- **The decoherence being refocused is *inhomogeneous broadening* ($T_2^*$), not homogeneous/Markovian dephasing.** $T_2 > 0.1$ ms (long, Gaussian decay, dipolar-dominated), but $T_2^* \sim 500$ ns for both transitions — comparable to a single pulse duration (360 ns for a $\pi$ rotation) and far shorter than the 9-pulse bare QFT sequence. This is a **quasi-static ensemble dephasing** mechanism, since the sample is an *ensemble* of molecules with a statistical distribution of hyperfine couplings (simulations identify **strain in the hyperfine couplings** as the dominant mechanism).
- **Refocusing construction and its cost:** each refocusing block applies **five $\pi$-pulses** alternating between the two addressable transitions, cycling each amplitude through all basis states so every spin collects the same global phase $2\phi_0+2\phi_1+2\phi_2$; the block also leaves a swap of two states. The bare QFT is 9 planar rotations; the **refocused sequence is 19 pulses**, refocusing every 6 pulses. So refocusing here roughly doubles circuit depth — relevant if main.tex treats refocusing as free.
- **Headline measured gains (Fig. 4), the numbers that bear on main.tex's claim:**
  - Refocused QFT: $\mathcal{F}=0.98\pm0.02$ (initial $|0\rangle$), $0.96\pm0.01$ ($|2\rangle$), $0.98\pm0.02$ ($\tfrac{1}{\sqrt2}(|0\rangle-i|1\rangle)$) — i.e. $\mathcal{F}\ge0.96$.
  - Non-refocused QFT: $\mathcal{F}=0.85\pm0.01$ ($|0\rangle$), $0.90\pm0.01$ ($|2\rangle$) — i.e. $\mathcal{F}\le0.90$.
  - Mechanism, stated explicitly: without refocusing "the **populations** of the qutrit's final state are accurately reproduced, whereas the **coherences — particularly the two-quanta ones — are substantially attenuated**." This is a clean dephasing (not relaxation) signature, supporting main.tex's "DD suppresses dephasing and leaves relaxation."
  - Single-gate benchmark: a $\pi/2$ pulse yields $\mathcal{F}=0.97\pm0.02$ by full tomography.
- **Reported fidelities are QFT-sequence-only.** $\mathcal{F}$ is computed against $\rho_{\rm ideal} = U_d \rho_0 U_d^\dagger$ where $\rho_0$ is the *experimentally tomographed* initial state — so state-preparation error is deliberately divided out. Also, measurements use a **pseudo-pure state** (1.4 K is too warm for thermal initialization to a pure state), so results are equivalent to pure-state results only up to a normalization factor.
- **A selection effect the authors flag themselves:** "the relatively long pulses used in the detection sequence act as a filter, suppressing contributions from spins exhibiting the strongest dephasing … the measurement predominantly probes spins located near the centre of the distribution, **for which the refocusing procedure is most effective**." The reported refocused fidelity is therefore somewhat favorably biased.
- The authors note the ensemble inhomogeneity is largely an ensemble artifact: "a more resilient behaviour is expected when going to the single molecule limit."

**Judge verification questions:**
- main.tex says DD suppresses "the part of the ladder channel scaling **worst with $d$** (the max-level law)." This paper studies **only $d=3$** and reports no $d$-dependence. Does main.tex's phrasing ("in agreement with … the refocused molecular-qudit QFT") overstate this reference as evidence for a *$d$-scaling* claim, or is it cited only for the weaker claim that refocusing restores coherences?
- The refocused mechanism here is **inhomogeneous ($T_2^*$, quasi-static ensemble) broadening**, not Markovian dephasing. Does main.tex's channel model — and its "at the device's operating dephasing level" condition — distinguish these? Note main.tex elsewhere in the same section explicitly contrasts "quasi-static versus Markovian field noise," so check for consistency.
- Does main.tex acknowledge that refocusing here roughly doubles the pulse count (9 → 19 pulses, five $\pi$-pulses per block)? "Refocusing buys roughly one cost model of headroom" is a net claim — is the overhead netted out?
- Does main.tex attribute any numeric fidelity to this reference? If so, does it match $\mathcal{F}\ge0.96$ refocused vs $\le0.90$ non-refocused, and does it note these exclude state-prep error and are ensemble/pseudo-pure measurements?

---

---

## `shi2025` — Efficient implementation of a quantum algorithm with a trapped ion qudit (Shi, Sinanan-Singh, Burke, Chiaverini & Chuang, 2026)

**Full citation:** X. Shi, J. Sinanan-Singh, T. J. Burke, J. Chiaverini, and I. L. Chuang, "Efficient implementation of a quantum algorithm with a trapped ion qudit," Nat. Commun. **17**, 1911 (2026), doi:10.1038/s41467-026-68746-0.
**Source:** arXiv:2506.09371v1 (11 Jun 2025). PDF: `shi-2025-grover-trapped-ion-qudit.pdf`

**Cited in main.tex (both in *Discussion*, line ~2414–2416, one sentence, two distinct uses):**
- (a) "multi-qudit entangling algorithms have been demonstrated at $d=3$ and $d=5$ … **earlier $d=3$ circuit work** in Refs.~\cite{roy2022,shi2025}"
- (b) "**single-qudit demonstrations reach $d=8$ on a trapped ion**~\cite{shi2025}"

**What the paper actually shows (full-text, not abstract-level):**
- **Platform:** a **single** $^{137}$Ba$^+$ ion in a surface-electrode trap (ion 50 $\mu$m above the surface), qudit encoded in the metastable $5D_{5/2}$ manifold (24 available sublevels), $|B_0|\approx7.2$ G. Multi-tone RF control via up to **seven** phase-coherent DDS tones through two trap RF electrodes.
- **Dimensions actually studied: $d=5$ and $d=8$. There is no $d=3$ work in this paper.** The only $d=3$ content is a description of *prior* work by others: Godfrin et al. (ref. [26], a Tb$^{3+}$ nuclear spin $I=3/2$), where "due to the lack of a pulse sequence capable of generating an equal superposition of four states with equal phases, the algorithm was implemented only on a $d=3$ subspace and an algorithm success probability of $\sim80\%$ was achieved." **⚠️ This is the sharpest flag in this batch:** citing `shi2025` for "earlier $d=3$ circuit work" appears to be a miscitation.
- **⚠️ Second flag: this paper contains no entangling gates at all, and involves only one ion.** Abstract: "the sequence requires only $O(d)$ single qudit gates and **no entangling gates**." Discussion: "In our case, **no entangling gate is needed** to implement Grover's search algorithm for this database size." Conclusion: "This control scheme allows for the implementation of Grover's search algorithm **without entangling gates**." So placing `shi2025` inside the clause "multi-qudit entangling algorithms have been demonstrated" is doubly wrong — it is neither multi-qudit nor entangling.
- **Use (b) is correct:** Grover's search implemented on a single trapped-ion qudit of **dimension 8** (and 5). Measured results:
  - $d=5$: algorithm success probability (ASP) **96.8(3)%** for $N=1$ iteration (highest achievable ~96.7% from $p(N)=\sin^2[(2N+1)\sin^{-1}(1/\sqrt d)]$); average SSO **99.9(1)%** (max 100%). Per-iteration fidelity **99.28(2)%** from a linear fit over multiple oracle–reflection rounds.
  - $d=8$: ASP **69(6)%** vs. theoretical max **78%**; SSO **97.1(3)%**. Pulse counts: Hadamard 3, oracle 2, reflection 8 displacement pulses.
  - $d=5$ pulse counts: equal superposition 2 pulses, oracle 2 pulses, reflection 4 pulses.
- **Comparison to qubit baselines** (relevant if main.tex uses this for a qudit-advantage claim): for a size-8 Grover search with a phase oracle and one iteration, prior qubit experiments achieved ASP 43.7(2)%, 51(6)%, 49.2(4)% — "approximately 20% lower than our implementation with a single qudit."
- **Scaling claim:** an unstructured (multi-tone) gate set achieves $O(d)$ pulses for an arbitrary unitary, versus $O(d^2)$ for structured/Givens-rotation gate sets. **Note this cuts against a generic $\alpha=2$ single-qudit pulse charge** — main.tex charges $\mu_1(d)=(d/2)^\alpha$ with $\alpha\approx2$, whereas this paper's central efficiency claim is $O(d)$, i.e. $\alpha=1$, on this platform. Worth checking whether main.tex's robustness argument acknowledges an $O(d)$ counterexample.
- **Decoherence numbers (main error source):** "A major source of error that limits the algorithm's fidelity is decoherence." Main text: measured coherence times **3(1) ms and 9(1) ms** for $d=5$ and $d=8$; average pulse lengths 33 and 30 $\mu$s → ~0.4% and ~1% error per pulse. ⚠️ **Note an internal inconsistency in the paper:** the Supplementary (Fig. 7) reports coherence times of **12(2) ms ($d=5$) and 4.9(5) ms ($d=8$)** — the reverse ordering, and consistent with the SI's own explanation that "the shorter coherence time is expected … for the $d=8$ qudit" due to higher magnetic-field sensitivity. The main-text pairing (3 ms for $d=5$, 9 ms for $d=8$) looks transposed. Do not rely on the main-text values without checking the published version.
- Dephasing is modeled as magnetic-field-sensitivity-driven (a diagonal dephasing operator whose elements are per-level $B$-sensitivities), confirmed against a master-equation simulation — i.e. **level-dependent dephasing**, structurally similar to main.tex's ladder channel.
- Off-resonant coupling to non-qudit states contributes only $\sim3\times10^{-5}$ ($d=5$) and $\sim2\times10^{-4}$ ($d=8$).
- Randomized benchmarking (SU(2) subgroup) gives pulse fidelities 99.94(1)% ($d=5$) and 99.7(1)% ($d=8$) — but the authors caution the RB-measured pulse fidelity is "approximately three times lower than the error rate we'd expect" from the Grover experiments, and that "a better benchmarking method should be used."
- Native two-qudit entangling gates on trapped ions are cited as existing **elsewhere** (Hrmo et al., 93.7(3)% fidelity), not demonstrated here.

**Judge verification questions:**
- **Does `shi2025` support "earlier $d=3$ circuit work"?** The paper studies $d=5$ and $d=8$ only; its sole $d=3$ mention is a *different group's* prior Tb$^{3+}$ experiment. Is this citation misplaced (should it be `roy2022` alone, or should it point to Godfrin et al.)?
- **Does `shi2025` support "multi-qudit entangling algorithms have been demonstrated"?** The paper is a single ion with explicitly zero entangling gates. Does the sentence's grammar attach `shi2025` to that clause?
- Is "single-qudit demonstrations reach $d=8$ on a trapped ion" accurate? (Yes — verify main.tex does not inflate to the 24 available $5D_{5/2}$ sublevels or the 13-level SPAM demonstration cited as ref. [39].)
- Does main.tex's Sec.-Robustness $\alpha\approx2$ single-qudit pulse charge conflict with this paper's headline $O(d)$ ($\alpha=1$) pulse scaling for multi-tone control? If main.tex cites `robert2026` as independent support for $\alpha=2$, does it also owe a rebuttal to the $O(d)$ result in a reference it cites elsewhere?
- If main.tex quotes coherence times or per-pulse errors from this reference, does it use the main-text (3/9 ms) or Supplementary (12/4.9 ms) values, and is the discrepancy material?

---

---

## `shor1997` — Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer (Shor, 1997)

**Full citation:** P. W. Shor, "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer," SIAM J. Comput. **26**, 1484 (1997).
**Source:** arXiv:quant-ph/9508027 (v2, 25 Jan 1996); SIAM J. Comput. 26, 1484. PDF: `shor-1997-polynomial-time-factoring-discrete-log.pdf` (28 pp.)

**Cited in main.tex (four places):**
- *Introduction* (line 131): "We simulate Shor order finding~\cite{shor1997}" — attribution of the algorithm being simulated.
- *Why the decoder gains tolerance with size* (line 1376): "Continued-fraction recovery succeeds for any outcome $y$ whose phase $y/D$ lies within $1/(2r^2)$ of some $s/r$ — the classical convergent guarantee~\cite{hardy2008,shor1997}."
- *Why the decoder gains tolerance with size* (line 1518): "An exact literature bounds the success of continued-fraction post-processing on base-2 registers: **Shor's original $4/\pi^2$ asymptotics**~\cite{shor1997}, the sharp divisor-recovery bounds of Gerjuoy … "
- *The decoder acceptance lemma* (line 2846): "the convergent guarantee~\cite{hardy2008} yields the reduced fraction $(s/g)/(r/g)$ with $g=\gcd(s,r)$, whose denominator $\tilde r=r/g$ **divides** $r$~\cite{shor1997,ekera2024}. A divisor with $g>1$ fails the test $a^{\tilde r}\equiv1$, so those analyses **lift $\tilde r$ to $r$ by classical search over multiples**."

**What the paper actually shows (full-text, not abstract-level):**
- **Order-finding construction (§5):** choose $q$ = the **power of 2 with $n^2 \le q < 2n^2$**. Prepare $q^{-1/2}\sum_{a=0}^{q-1}|a\rangle|0\rangle$, compute $x^a \bmod n$ in the second register, apply the Fourier transform $A_q$ ($|a\rangle \mapsto q^{-1/2}\sum_c e^{2\pi i ac/q}|c\rangle$), then observe. This is a **base-2 (power-of-two) register**, matching main.tex's "on base-2 registers" framing.
- **⚠️ Shor's own stated acceptance window is $1/(2q)$, not $1/(2r^2)$.** Eq. (5.13): the probability of seeing state $|c, x^k\rangle$ is at least $1/3r^2$ if $\left|\frac{c}{q}-\frac{d}{r}\right| \le \frac{1}{2q}$. Shor then argues: "Because $q > n^2$, there is **at most one** fraction $d/r$ with $r<n$ that satisfies the above inequality. Thus, we can obtain the fraction $d/r$ in lowest terms by rounding $c/q$ to the nearest fraction having a denominator smaller than $n$." The $1/(2r^2)$ form is the **Legendre/best-approximation theorem from Hardy & Wright** (Shor cites "[Hardy and Wright 1979, Chapter X]" for continued fractions finding all best approximations). So the joint cite `\cite{hardy2008,shor1997}` is defensible — Shor invokes exactly that theorem — but the specific inequality $1/(2r^2)$ is Hardy & Wright's, and Shor's stricter $1/(2q)$ (with $q>n^2>r^2$) admits **~1 outcome per peak**, not the $\sim D/r^2$ outcomes main.tex's window argument needs. main.tex's wider-window arithmetic ($1/r^2$ in phase, $\sim D/r^2$ outcomes) follows from Hardy & Wright, not from Shor's §5.
- **⚠️ What "$4/\pi^2$" actually is.** From §5: "Letting $\{rc\}_q/r$ vary between $-\tfrac12$ and $\tfrac12$, the absolute magnitude of the integral (5.10) is easily seen to be minimized when $\{rc\}_q/r=\pm\tfrac12$, in which case the absolute value of expression (5.10) is $2/(\pi r)$. The square of this quantity is a lower bound on the probability that we see any particular state $|c, x^k \bmod n\rangle$ with $\{rc\}_q \le r/2$; **this probability is thus asymptotically bounded below by $4/(\pi^2 r^2)$**, and so is at least $1/3r^2$ for sufficiently large $n$." So $4/\pi^2$ is the coefficient in a **per-outcome amplitude lower bound** $4/(\pi^2 r^2)$ — it is *not* an end-to-end success probability for continued-fraction post-processing. Describing it as bounding "the success of continued-fraction post-processing" is loose.
- **Shor's actual end-to-end success bound:** there are $\varphi(r)$ values of $d$ coprime to $r$, one $c$ per such $d$, and $r$ values of $x^k$, giving $r\varphi(r)$ good states each of probability $\ge 1/3r^2$, hence **success probability $\ge \varphi(r)/3r$**. Using $\varphi(r)/r > \delta/\log\log r$ [Hardy & Wright, Thm. 328], "we find $r$ at least a $\delta/\log\log r$ fraction of the time, so by repeating this experiment only $O(\log\log r)$ times, we are assured of a high probability of success." A judge should check whether main.tex's "$4/\pi^2$ asymptotics" is presented as the per-peak constant (correct) or as the algorithm's success probability (incorrect — that is $\varphi(r)/3r \sim 1/\log\log r$).
- **✓ The divisor/lift claim at line 2846 is very well supported.** Shor: "If we have the fraction $d/r$ in lowest terms, and if $d$ happens to be **relatively prime to $r$**, this will give us $r$" — i.e. the $g=1$ case, which is exactly why only $\varphi(r)$ of the $r$ numerators count. And explicitly on the lift: "if the observed value of $c/q$ is rounded off to $d'/r'$ in lowest terms, for a candidate $r$ one should consider **not only $r'$ but also its small multiples $2r', 3r', \ldots$**, to see if these are the actual order of $x$." This is precisely main.tex's "those analyses lift $\tilde r$ to $r$ by classical search over multiples." Shor further credits Odlyzko [1995] that considering the first $(\log n)^{1+\epsilon}$ multiples reduces the expected trials for the hardest $n$ from $O(\log\log n)$ to $O(1)$, and Knill [1995] for the lcm$(r_1,r_2)$ variant. Both are classical post-processing lifts, exactly as main.tex characterizes.
- **Peak structure (supports main.tex's "peak stays ~1 outcome wide"):** Fig. 5.1 plots the exact probabilities of Eq. (5.7) for $q=256$, $r=10$ — Shor notes "with high probability the observed value of $c$ is near an integral multiple of $q/r = 256/10$." He explicitly remarks this example "could occur when factoring 33 if $x$ were chosen to be 5" — note main.tex's decoder section uses $N=33,55$ instances, so this is a nice concordance.
- **Factoring reduction (§5, preamble):** find the order $r$ of a random $x \bmod n$, compute $\gcd(x^{r/2}-1, n)$; this fails to give a nontrivial divisor only if $r$ is odd or $x^{r/2}\equiv-1 \pmod n$. Works for $n$ odd and not a prime power. Failure probability at most $1/2^{k-1}$ for $k$ distinct odd prime factors.
- **Complexity:** modular exponentiation asymptotically $O(l^2 \log l \log\log l)$ time and $O(l\log l\log\log l)$ space using Schönhage–Strassen; $O(l^3)$ with schoolbook multiplication. The paper covers **both** factoring and discrete logarithms (§6 is the discrete-log algorithm, with its own bounds, e.g. "at least $.054/q^2 > 1/(20q^2)$").
- The paper is entirely **noiseless/idealized** — there is no noise model, no decoherence analysis, and no error-tolerance claim anywhere in §5. This is consistent with main.tex's Introduction framing that the size-scaling question "concerns the noiseless algorithm; we are not aware of it having been tested against a noise model."

**Judge verification questions:**
- At line 1376, main.tex attributes the $1/(2r^2)$ window to `\cite{hardy2008,shor1997}`. Shor's own stated condition is $1/(2q)$ with $q>n^2$. Is the joint citation acceptable (Shor invokes Hardy & Wright's best-approximation theorem), or does main.tex specifically attribute the $1/(2r^2)$ inequality to Shor in a way the paper does not state?
- At line 1518, is "$4/\pi^2$ asymptotics" presented as the **per-outcome** probability constant $4/(\pi^2 r^2)$ (correct) or as an end-to-end post-processing success probability (incorrect — Shor's is $\varphi(r)/3r \ge \delta/\log\log r$)?
- At line 2846, does Shor really support "denominator $\tilde r = r/g$ divides $r$" and "lift $\tilde r$ to $r$ by classical search over multiples"? (Yes on both — verify main.tex's wording matches Shor's "consider not only $r'$ but also its small multiples $2r', 3r', \ldots$" and the $\varphi(r)$/coprimality argument.)
- Does main.tex correctly treat `shor1997` as a **noiseless** analysis with no error model, given its Introduction claims the size-scaling question has not been tested against noise?
- main.tex's decoder argument needs a window holding $\sim D/r^2$ outcomes. Shor's construction ($q>n^2$, unique rounding) yields ~1 outcome per peak. Does main.tex cite Shor for a window width his own analysis does not use?

---

---

## `sutherland2023` — Passive dynamical decoupling of trapped-ion qubits and qudits (Sutherland & Erickson, 2024)

**Full citation:** R. T. Sutherland and S. D. Erickson, "Passive dynamical decoupling of trapped-ion qubits and qudits," Phys. Rev. A **109**, 022620 (2024), doi:10.1103/PhysRevA.109.022620.
**Source:** arXiv:2312.09399v1 (14 Dec 2023). PDF: `sutherland-2024-passive-dynamical-decoupling-qudits.pdf`
*(Note the bibtex key says 2023 — the arXiv year — while the bib fields correctly give the 2024 PRA publication. Not a factual error, just a key/year mismatch.)*

**Cited in main.tex (both in *Robustness*):**
- (line ~2136): the refocusing mitigation "is therefore free for the qubit and costs $d$ pulses for the qudit, which is the opposite of the **$d$-independence the constant-overhead passive-decoupling construction**~\cite{sutherland2023} would supply, and the reason that construction is the right thing to reach for here."
- (line ~2227): "On linear-cost hardware the Zeeman component must be suppressed below the plain shielding level — deeper echo sequences, **passive decoupling of the full manifold**~\cite{sutherland2023}, or magnetically insensitive encodings — before the qudit ordering returns."

**What the paper actually shows (full-text, not abstract-level):**
- **✓ The "constant overhead in $d$" claim is stated verbatim and repeatedly by the authors.** Abstract: "Fundamentally, PDD drives the transition $m_F \to -m_F$ for every magnetic quantum number $m_F$ in the system — **with only one operation** — indicating it applies to **qudits with constant overhead in the dimensionality of the qudit**." Body (Sec. I): "The fact that PDD acts on an entire ion, rather than a qubit subspace of that ion, extends dynamical decoupling to **qudit systems with constant overhead in the dimensionality of the qudit**." Sec. III: "the control sequences we describe would similarly dynamically decouple **qudit systems with constant overhead**." main.tex's characterization is exact.
- **✓ The "full manifold" claim is also exact.** The whole point of PDD is that it "dynamically decouple[s] the **entire ion**, rather than a qubit subspace," inverting the linear Zeeman sensitivity of *every* $m_F \ne 0$ sublevel simultaneously. Sec. III: "there is **no requirement whatsoever** on the ability to directly drive transitions between a system's information carrying states, **or even how many information carrying states there are**." This is precisely the $d$-independence main.tex contrasts against its own $d$-pulse permutation cost.
- **Mechanism:** trap-integrated circuits generate a local field $\vec B_c$; the total quantization field $\vec B_t = \vec B_0 + \vec B_c$ is **adiabatically rotated** until anti-parallel to its original direction, inverting every sublevel's $B$-field susceptibility. Formally $\tilde H = \mu_B B_t g_J \hat J_z + \hbar\dot\phi(t)\hat J_y$ (Eq. 5); in the adiabatic limit $\dot\phi\to0$. Two variants: **pulsed PDD** (a "passive spin echo") and **continuous PDD** (rotating $\hat B_t$ in a circle at $\omega_r$, rendering noise at $\omega_e \ll \omega_r$ off-resonant).
- **⚠️ CRITICAL SCOPE LIMIT #1: this is a proposal, not an experiment.** All results are analytic + numerical (filter-function and Magnus-expansion analysis, simulated on $^{137}$Ba$^+$). No hardware demonstration. main.tex's "would supply" (subjunctive) at line 2136 correctly signals this; check line 2227's "passive decoupling of the full manifold" does not read as an available technique.
- **⚠️ CRITICAL SCOPE LIMIT #2: PDD targets *magnetic-field* noise / the *linear* Zeeman sensitivity only.** It "does **not** dynamically decouple the quadratic shift due to $B_0$ mixing the two hyperfine manifolds; this means, for example, that pulsed PDD **could not** be used to increase the memory time of the $\{|F^+,0\rangle, |F^-,0\rangle\}$ 'clock' qubit." It is not a general dephasing remedy. Since main.tex invokes it specifically for the **Zeeman/common-mode field** component, this is a good match — but a judge should confirm main.tex does not generalize it to the full ladder dephasing channel.
- **Quantitative performance:** filter-function analysis (Fig. 3, $^{137}$Ba$^+$, $t_f=100\,\mu$s, $B_t=10$ G, $\tau=10\,\mu$s) shows $S(\omega_e)\to0$ as $\omega_e\to0$ for the echoed sequence (vs. maximal for no PDD), and continuous PDD "suppresses magnetic field noise by **several orders-of-magnitude** relative to a spin-echo sequence." Since magnetic-field noise spectral densities are largest at low frequencies, PDD "should lead to significantly longer qubit **and qudit** memory times."
- **Error budget and the pulsed-vs-continuous tradeoff (relevant to main.tex's cost accounting):** with $\delta\vec B_c\cdot\hat B_t$ uncertainty of $10^{-4}$ and $B_c\simeq2.5$ G, infidelity $\mathcal{I}\simeq1\times10^{-5}$ for **pulsed** PDD ($t_r\simeq3\,\mu$s) but $\mathcal{I}\simeq2\times10^{-2}$ for **continuous** PDD ($t_r\simeq100\,\mu$s) — "continuous PDD is significantly more sensitive to control field uncertainties because $t_r$ is larger, making **pulsed PDD more appealing as a near-term tool**." State leakage from diabaticity scales $\propto(\phi_0/\varepsilon_0)^2$ and is suppressed below $10^{-4}$ at $B_t\sim1$ G (pulsed) / $\sim2.5$ G (continuous) (Fig. 4).
- **Hardware requirements:** $B_0 \lesssim 10$ G (as in current commercial ion processors); a wire carrying 0.25 A produces 10 G at 50 $\mu$m; a 0.1 A current gives 4 G at 50 $\mu$m, with "resistive heat loads $\sim$100 times lower than the $\sim$1 A currents used in Ref. [4]." So the overhead is in *trap fabrication* (integrated circuits), not in pulse count — consistent with main.tex's framing of $d$-independence.
- **Bonus result not used by main.tex:** Sec. III C proposes a PDD-assisted **laser-free two-qubit gate** by tuning $\omega_r$ near a motional-mode frequency in a static $B$-field gradient (Eq. 14 reduces to a $\hat\sigma_z\otimes\hat\sigma_z$ entangling Hamiltonian). Note this gate section is framed for **qubits**, not qudits.
- Crosstalk is explicitly **not** analyzed in detail ("this will likely be device specific"), though idle ions far from $\vec B_c$ are argued to see only small, trackable phase shifts.

**Judge verification questions:**
- Does main.tex's "constant-overhead passive-decoupling construction" and "$d$-independence" faithfully reflect the paper? (It does — the phrase "constant overhead in the dimensionality of the qudit" is the authors' own, stated three times.)
- Does main.tex make clear this is a **theoretical proposal** with no experimental demonstration? Line 2136's "would supply" suggests yes; check line 2227, where it is listed alongside "deeper echo sequences" and "magnetically insensitive encodings" as if it were an available remedy.
- PDD suppresses only the **linear Zeeman** sensitivity and explicitly **fails** on the quadratic shift (clock qubits). Does main.tex confine its use to the Zeeman/common-mode field component (it appears to — "the Zeeman component must be suppressed"), or does it imply broader dephasing suppression?
- main.tex contrasts a mitigation that "costs $d$ pulses for the qudit" against this construction. Is the comparison apples-to-apples, given that PDD's constant pulse overhead is bought with **trap-integrated-circuit hardware** and carries its own control-field-uncertainty infidelity ($10^{-5}$ pulsed, $2\times10^{-2}$ continuous)?
- Does main.tex cite this for a trapped-ion context only? (The construction is specific to trapped-ion hyperfine $m_F$ manifolds and integrated trap circuits; it does not transfer to transmons.)

---

## `tripathi2025` — Qudit Dynamical Decoupling on a Superconducting Quantum Processor (Tripathi, Goss, Vezvaee, Nguyen, Siddiqi & Lidar, 2025)

**Full citation:** V. Tripathi, N. Goss, A. Vezvaee, L. B. Nguyen, I. Siddiqi, D. A. Lidar, "Qudit dynamical decoupling on a superconducting quantum processor," Phys. Rev. Lett. **134**, 050601 (2025); arXiv:2407.04893.
**Source:** arXiv:2407.04893 (v1, 5 Jul 2024) / PRL 134, 050601, PDF: `tripathi-2024-qudit-dynamical-decoupling.pdf`

**Cited in main.tex:**
- *Introduction*: listed among the "published per-level transmon coherence measurements" (with peterer2015, goss2022, blok2021, wang2025) to which the anharmonic-ladder decoherence channel is calibrated.
- *Noise channels*: cited as one of six sources supporting "the relaxation ratio $\Gamma_2/\Gamma_1$ is measured at $\approx 1.7$ ... against $2.0$ for the textbook $\Gamma_k \propto k$ ladder", and (by grouping) the dephasing ratios $\Gamma_\phi^{01}:\Gamma_\phi^{12}:\Gamma_\phi^{02} = 1:2.0:2.3$. Also implicitly part of the "nine devices, $d=3$ to $12$" fit set.
- *Robustness*: "dynamical decoupling suppresses dephasing — the part of the ladder channel scaling worst with $d$ (the max-level law) — and leaves the gentler $k^{0.7}$ relaxation, **in agreement with qudit DD experiments**~\cite{tripathi2025}". Used to support the claim that refocusing "buys roughly one cost model of headroom" and that the ququint's Shor advantage flips from $-0.026$ (no echo) to $+0.191$ (echo).

**What the paper actually shows (full-text, not abstract-level):**
- **Platform and dimensions.** 8 fixed-frequency transmon qudits coupled by CPW resonators in a ring; experiments use a 3-qudit line (Q1, Q2, Q3). Qudit dimensions studied are **$d=3$ (qutrit) and $d=4$ (ququart) only**. There is **no $d=5$ (ququint) data anywhere in the paper**.
- **Per-level coherence (SM, Table I)** — the only per-level numbers the paper contributes, in µs, "two-level subspace mean $T_1$ and $T_2$ echo times ... from 100 repetitions":
  | | Q1 | Q2 | Q3 |
  |---|---|---|---|
  | $T_1^{01}$ | 50(4) | 49(4) | 60(5) |
  | $T_1^{12}$ | 35(2) | 35(4) | 31(8) |
  | $T_1^{23}$ | 24(4) | 26(3) | 23(4) |
  | $T_{2e}^{01}$ | 78(5) | 85(9) | 90(6) |
  | $T_{2e}^{12}$ | 57(4) | 57(4) | 56(9) |
  | $T_{2e}^{23}$ | 26(2) | 27(2) | 24(3) |
- **Implied relaxation ratio.** $\Gamma_2/\Gamma_1 = T_1^{01}/T_1^{12}$ = **1.43 (Q1), 1.40 (Q2), 1.94 (Q3)**; mean ≈ **1.59**. Implied $\Gamma_3/\Gamma_1 = T_1^{01}/T_1^{23}$ = 2.08 / 1.88 / 2.61, mean ≈ 2.19 (a $k^{0.7}$ law predicts $3^{0.7}=2.16$). So this device *does* support a sub-linear ladder, but its own $\Gamma_2/\Gamma_1$ centres closer to ~1.6 than to 1.7 and one qudit (Q3) reads 1.94, i.e. essentially the textbook 2.0.
- **Implied dephasing ratios (must be derived; not reported by the authors).** Using $\Gamma_\phi = 1/T_{2e} - 1/(2T_1)$, the ratio $\Gamma_\phi^{12}/\Gamma_\phi^{01}$ is **2.09 (Q2), 1.15 (Q1), 0.62 (Q3)** — i.e. the "1 : 2.0" figure is attainable on one of three qudits and is *inverted* on another. **The paper reports no $0\!\leftrightarrow\!2$ coherence at all**, so it cannot bear on the $\Gamma_\phi^{02}$ ($=2.3$) element of the cited ratio. Also note these are **Hahn-echo** $T_2$, not Ramsey $T_2^*$, so the extracted $\Gamma_\phi$ are already partly refocused.
- **DD mechanism claim.** The authors state explicitly: "The dominant decoherence mechanism in transmon qutrits and ququarts is dephasing due to $1/f$ noise [58], which has been connected to charge fluctuations and higher level charge sensitivity," and later "The superior performance of the $3X_3$ sequences also confirms that the dominant source of noise is dephasing." This directly supports main.tex's mechanistic statement that DD in transmon qudits mainly attacks dephasing.
- **DD works, but not monotonically.** Fig. 2(a): *all* DD curves beat free evolution for $d=3$. However, "Our results exhibit the opposite of both expectations": the single repetition $1\times 3X_3$ (longest pulse interval) gives the **highest** fidelity and universal (full order-9 HWG) DD gives the **lowest** DD fidelity, because coherent pulse errors accumulate. $X_3$ needs four native $\sqrt{\sigma^x_s}$ gates while the remaining HW pulses need six, so $\tau_{\min}=180$ ns for universal DD vs 120 ns for $3X_3$.
- **DD cost grows with $d$.** "The underlying cycle operator $X_d$ is compiled using $2(d-1)$ native $\sqrt{\sigma^x_s}$ subspace rotations." The $dX_d$ sequence is $d\tau$ long; CKDD is $d^2\tau$ long. So refocusing overhead scales with $d$ — a cost main.tex's "one cost model of headroom" framing does not itself charge.
- **Ququarts benefit *more* than qutrits, qualitatively.** "Since ququarts are more susceptible to charge noise due to the involvement of the third excited state, the free evolution fidelity is significantly lower than in the qutrit case, and the improvement with DD is even more pronounced." This is the closest support for main.tex's "the ququint's lead grows monotonically" under refocusing — but it is a $d=4$ observation, extrapolated.
- **Countervailing detail for higher $d$.** For ququart CKDD: "In the presence of large cross-Kerr interactions, driving the two-level subspaces is prone to large detuning errors. This results in somewhat lower CKDD fidelities for the ququart experiments compared to qutrits." So higher $d$ is not uniformly better under DD in this device.
- **Cross-Kerr (CKDD) results.** Measured qutrit cross-Kerr rates $\alpha_{ij}/2\pi$ = 0.112–0.623 MHz (Q1–Q2) and $-0.162$ to 0.615 MHz (Q2–Q3); ququart rates up to 0.730 MHz. Qutrit Bell state $(|00\rangle+|11\rangle+|22\rangle)/\sqrt3$: without DD fidelity "drops to near zero in $\sim 1$ µs" then oscillates about the 1/9 mixed-state baseline; with CKDD, fidelity "remains $>50\%$ even after 10 µs."
- **Theory contribution.** HWG-based universal qudit DD; proves first-order decoupling for **arbitrary $d$** (not just prime powers); numerically verified $O(\tau^4)$ infidelity scaling for $2\le d\le 10$ (Fig. 5) — but this is *simulation with a classical randomized bath*, not experiment.
- The authors call the work "a proof-of-concept demonstration"; no algorithm-level or Shor/QPE benchmark appears.

**Judge verification questions:**
- Does main.tex claim that tripathi2025 supports $\Gamma_2/\Gamma_1 \approx 1.7$? The paper's own Table I gives 1.43 / 1.40 / 1.94 (mean 1.59) across its three qudits — is 1.7 a fair representation of this device once averaged with the other five references, and does main.tex say "$\approx$" rather than asserting agreement?
- Does main.tex attribute the *dephasing* ratio $1:2.0:2.3$ (including the $0\!\leftrightarrow\!2$ element) to tripathi2025? The paper measures **no 0–2 coherence**, and its derived $\Gamma_\phi^{12}/\Gamma_\phi^{01}$ ranges 0.62–2.09 across three qudits. Is the citation grouped loosely enough that this is defensible?
- Main.tex says the echo result is "in agreement with qudit DD experiments~\cite{tripathi2025}" while discussing a **ququint ($d=5$)** Shor/QPE flip. Tripathi studied only $d=3$ and $d=4$. Does main.tex's sentence claim agreement about the *mechanism* (DD suppresses dephasing) — which the paper does support — or about $d=5$ behaviour, which it does not?
- Does main.tex anywhere charge the DD overhead that Tripathi documents ($2(d-1)$ native rotations per $X_d$; pulse-error accumulation that made *shorter* intervals and universal DD *worse*)? If the "perfect echo" end of main.tex's dephasing-scale sweep assumes error-free refocusing, does main.tex flag that Tripathi's experiment could not reach the theoretical DD optimum?

---

---

## `venturelli2025` — Near-term Application Engineering Challenges in Emerging Superconducting Qudit Processors (Venturelli, Gustafson, Kurkcuoglu & Zorzetti, 2025)

**Full citation:** D. Venturelli, E. Gustafson, D. Kurkcuoglu, S. Zorzetti, "Near-term application engineering challenges in emerging superconducting qudit processors," arXiv:2506.05608 (2025).
**Source:** arXiv:2506.05608v1 (5 Jun 2025), PDF: `venturelli-2025-superconducting-qudit-processors.pdf`

**Cited in main.tex:**
- *The cost condition*: "the genuine failure mode remains the absence of a native entangler (`pavlidis`) — fatal at $d\ge5$ on the ladder and under any realistic accounting at $d=3$ there, survivable only by the per-particle qutrit — which is precisely the regime of **synthesis-based compilation**~\cite{gustafson2025synthesis,venturelli2025}."

**What the paper actually shows (full-text, not abstract-level):**
- **Genre.** A 4-page IEEE-style review/position paper (SQMS / NASA QuAIL / Fermilab). **No new experiments, no new numerics, no measured fidelities of its own.** It surveys three near-term application targets (sQED lattice-gauge simulation, graph-colouring QAOA, quantum reservoir computing) and names the engineering blockers.
- **Platform scope.** Its qudits are predominantly **bosonic/cavity qudits** — Fock-state encodings in 3D SRF cavities coupled to a transmon ancilla (SNAP + displacement control), not transmon energy-ladder qudits. Forecast: "$\simeq$10 linearly connected cavities, each contributing $\simeq$4 modes ... occupied by $d\simeq10$ photons with millisecond $T_1$ ... within the next 5 years"; bare SRF cavities have shown $T_1\sim 2$ s.
- **The synthesis/entangler claim main.tex leans on — supported, and repeatedly:**
  - "a key challenge is the engineering [of] the CSUM gate, crucial to implement nearest-neighbor interactions. ... This gate is the Clifford extension of CNOT to qudit states, and efficiently implementing it is key for both near and far-term applications. The timescale of execution of this gate at high fidelity will ultimately determine the viability and scale of the simulation. There has been work on the subject [13], [14], but **it typically requires advanced pulse and hardware-specific tuning**. As this gate forms the basis for entangling operations in the Clifford-basis ... [it] **represents a missing engineering component**."
  - "Similar advances as the ones required for the CSUM gate are required to perform a clear resource estimate for this application as well ... The **numerical studies to synthesize two-qudit gates don't consider decoherence and employ numerical methods that can't scale with increasing Hilbert space. Constructive algorithms for synthesis are the likely solution, yet to be demonstrated in context** [14]."
  - Table I ("Main challenge" column) lists "Synthesis CSUM between co-located and adjacent qumodes [24]" and "CSUM and generalize QRACs to qudits [22]".
- **Ref. [14]** in this paper is Mato, Ringbauer, Hillmich & Wille, "Compilation of entangling gates for high-dimensional quantum systems" (ASP-DAC 2023) — i.e. the paper does explicitly point at *decomposition/synthesis* compilation as the operative regime when no native entangler exists.
- **Related numbers the paper cites (not its own):** Ozgüler & Venturelli [20] numerically synthesized bosonic-qudit QAOA circuits with single-qudit control over **up to eight energy levels** and two-qutrit phase-separation operations, "achieving gate fidelities exceeding 99% **in a noiseless setting**." Gustafson [11] found the "most native qutrit encodings tolerated gate errors **10–100 times higher** than qubit encodings" for sQED.
- **Scope limits the paper states about itself:** the table's implementation estimates "refer to objectives that are difficult (due to noise) but *in principle* mappable and executable in NISQ hardware"; "conclusive near-term quantum advantage remains elusive"; the first multi-oscillator demonstration "remains to be achieved."
- **What it does NOT contain:** no $O(d^2)$ or $2(d-1)$ entangling-gate cost model, no claim that synthesis compilation is "fatal at $d\ge5$", no $d=3/5$ comparison, and no decoherence-channel calibration. It is a directional citation only.

**Judge verification questions:**
- Is main.tex citing venturelli2025 only to characterise the *regime* ("synthesis-based compilation" when a native entangler is absent), rather than for any quantitative cost figure? If main.tex attributes any number (e.g. an $O(d^2)$ multiplier, or a "fatal at $d\ge5$" threshold) to venturelli2025, that number is not in the paper.
- The paper's qudits are bosonic cavity modes with $d\simeq10$ and SNAP/displacement control; main.tex's cost-condition discussion concerns $d=3$ and $d=5$ registers under ladder or per-particle noise. Does main.tex's sentence implicitly transfer a cavity-qudit compilation problem to a transmon/ion register without flagging the platform difference?
- The paper explicitly notes that existing two-qudit synthesis studies "don't consider decoherence" and "can't scale with increasing Hilbert space." Does main.tex's use of this citation remain consistent with that caveat (i.e. it is a statement of an open engineering gap, not of a measured penalty)?

---

---

## `wang2020` — Qudits and High-Dimensional Quantum Computing (Wang, Hu, Sanders & Kais, 2020)

**Full citation:** Y. Wang, Z. Hu, B. C. Sanders, S. Kais, "Qudits and high-dimensional quantum computing," Front. Phys. **8**, 589504 (2020); arXiv:2008.00959.
**Source:** arXiv:2008.00959 / Front. Phys. 8:589504, PDF: `wang-2020-qudits-high-dimensional-qc-review.pdf`

**Cited in main.tex:**
- *Introduction*: listed among indirect cross-dimension noise treatments — specifically "the qualitative argument that fewer carriers means less local noise~\cite{wang2020}".
- *Introduction*: "A claim that qudit phase-estimation error decreases exponentially with $d$ — attributed by the review of Wang *et al.*~\cite{wang2020} to a conference contribution of Parasa and Perkowski~\cite{parasa2011}, whose available slides state it for the algorithm's intrinsic failure probability at fixed precision — concerns the noiseless algorithm; we are not aware of it having been tested against a noise model."

**What the paper actually shows (full-text, not abstract-level):**
- **Genre.** A ~55-page pedagogical review (qudit gates, geometric gate-count bounds, qudit QFT/PEA/Deutsch–Jozsa/Bernstein–Vazirani, and physical platforms: photonics, superconducting circuits, trapped ions, molecular magnets, NMR). **No original experiments or simulations.**
- **The PEA-error claim, verbatim (§3.2.2, p. 28):** "The PEA in qudit system provides a significant improvement in the number of the required qudits and **the error rate decreases exponentially as the qudit dimension increases [87]**." Reference **[87] is exactly** "V. Parasa and M. Perkowski, 'Quantum phase estimation using multi-valued logic,' in *2011 41st IEEE International Symposium on Multiple-Valued Logic*, pp. 224–229, May 2011" — a conference contribution, confirming main.tex's attribution.
  - The sentence appears in a purely algebraic derivation of the qudit PEA (Eqs. 100–105, phase kick-back, inverse QFT $F^{-1}(d,d^t)|\text{Register 1}\rangle = |R\rangle$). **There is no noise model, no decoherence channel, no density-matrix evolution, and no "error rate" definition anywhere in the surrounding text.** The claim is stated once and not derived, quantified, or bounded in the review.
  - A closely related but distinct claim appears earlier for the **QFT** (p. 26): "Qudit QFT offers superior approximations where the magnitude of the error decreases exponentially with $d$ and the smaller error bounds are smaller [84], which outperforms the binary case [85]" — again approximation/truncation error, not noise.
- **The "fewer carriers means less local noise" argument, verbatim (§6.1, p. 41):** "This higher noise resilience of qudits is more advantageous if the qudits are entangled. The entanglement becomes more robust by increasing the dimension of the qudits while fixing their numbers. In other words, **as the noise sources act locally on every system, increasing the dimension $d$ will reduce the number of systems and thus reduce the effect of noise resulting in the robustness increase [160]**." Reference [160] = Z. Liu & H. Fan, "Decay of multiqudit entanglement," Phys. Rev. A **79**, 064305 (2009).
  - **Scope of that passage:** it sits in a paragraph about **quantum communication / QKD**, not computation — "the qudit also has advantages in quantum communication as it possesses a higher noise resilience than the qubit [158]," higher QBER tolerance, secret-key rate increasing with Hilbert-space dimension at fixed noise level [159], and a photonic OAM entanglement-distribution demonstration [161] (Ecker *et al.*, PRX 9, 041042). It is an entanglement-decay/communication argument, **not** an algorithm-level circuit-noise result.
  - The review itself hedges: "in practical situation, the qudit system performed on each particular physical apparatus has varied amount of advantages than the qubit."
- **Decoherence is treated only as a gate-budget constraint** (§2.3): "each qudit can remain coherent for a limited amount of time ... The decoherence time of a qudit state limits the number of quantum gates in the circuit. Therefore, we need to design more efficient algorithms and circuits." The review then pivots to Riemannian-geometry gate-count lower bounds ($O(n^6 d(I,U)^3)$ for qubits vs $O(n^k d(I,U)^3)$, $k<6$, for qutrits) — i.e. **gate count as the noise proxy**, exactly the pattern main.tex describes.
- **Acknowledged challenges (§6.2):** "these advantages can come with challenges such as possibly harder-to-implement universal gates, benchmarking, characterization of qudit gate and error correction connected with the complexity of the Clifford hierarchy for qudits."

**Judge verification questions:**
- Does main.tex's sentence accurately say the exponential-error-with-$d$ PEA claim is *attributed by the review* to Parasa & Perkowski (rather than proven by Wang *et al.*)? The review states it in one sentence with citation [87] and no derivation — is main.tex's framing ("attributed by the review ... to a conference contribution") exact?
- Main.tex says the claim "concerns the noiseless algorithm." Is that correct given that the review's PEA section contains no noise model at all, and that its own $\Gamma$/decoherence discussion is confined to gate-count budgeting?
- Main.tex characterises wang2020 as offering "the qualitative argument that fewer carriers means less local noise." Does main.tex disclose that this argument appears in the review's **quantum-communication / entanglement-decay** paragraph (sourced to Liu & Fan 2009 on multiqudit entanglement decay), not as a computation-level result? Is the paraphrase still fair as a characterisation of the literature?
- Does main.tex avoid implying that wang2020 itself performed any noise simulation? (It did not — it is a review with no original numerics.)

---

---

## `wang2025` — Systematic Study of High $E_J/E_C$ Transmon Qudits up to $d=12$ (Wang, Parker, Champion & Blok, 2025)

**Full citation:** Z. Wang, R. W. Parker, E. Champion, M. S. Blok, "Systematic study of high $E_J/E_C$ transmon qudits up to $d=12$," Phys. Rev. Applied **23**, 034046 (2025), doi:10.1103/PhysRevApplied.23.034046; arXiv:2407.17407.
**Source:** arXiv:2407.17407v1 (24 Jul 2024) / PRApplied 23, 034046, PDF: `wang-2024-high-ej-ec-transmon-qudits-d12.pdf`

**Cited in main.tex:**
- *Introduction*: among the "published per-level transmon coherence measurements" the anharmonic-ladder channel is calibrated to.
- *Noise channels* (×3): (a) one of six sources for "$\Gamma_2/\Gamma_1$ measured at $\approx 1.7$" and the "nine devices, $d=3$ to $12$" fit set; (b) "A dephasing-scale knob interpolates to the high-$E_J/E_C$ regime demonstrated at $d=12$~\cite{wang2025}, **where echo coherence approaches the $T_1$ limit**"; (c) the "*low-charge-dispersion* variant (the dephasing knob set to the high-$E_J/E_C$ regime of Ref.~\cite{wang2025})" is one of four named noise regimes in the figures.
- *Robustness* (×2): (a) "Wang's ten-state single-shot readout at **93.8%**~\cite{wang2025} sits at [the] upper end" of $\varepsilon\approx0.01$–$0.03$ in the $(1{+}k)$ readout-error model; (b) "Sweeping the dephasing scale from free evolution to perfect echo (**the same knob that models the high-$E_J/E_C$ regime**~\cite{wang2025})".

**What the paper actually shows (full-text, not abstract-level):**
- **Devices.** Six fixed-frequency Xmon transmons (Q0–Q5) across three chips, $E_J/E_C$ = **88, 139, 144, 204, 266, 325** (Table I), all $f_{01}\approx 5$ GHz; first anharmonicities $\alpha_1$ = $-209$ to $-104$ MHz. **12 levels ($d=12$) observed on Q5**; coherence characterised on **Q5 only**, up to $|9\rangle$; multi-tone readout of **10 states**.
- **Per-level coherence, Q5 (Appendix Table III, µs):**
  | Transition | $T_1$ | $T_{2R}$ | $T_{2E}$ |
  |---|---|---|---|
  | $|1\rangle\!\leftrightarrow\!|0\rangle$ | 64(15) | 85(31) | 93(27) |
  | $|2\rangle\!\leftrightarrow\!|1\rangle$ | 34(8) | 51(19) | 53(14) |
  | $|3\rangle\!\leftrightarrow\!|2\rangle$ | 24(5) | 44(12) | 45(10) |
  | $|4\rangle\!\leftrightarrow\!|3\rangle$ | 21(4) | 39(11) | 39(8) |
  | $|5\rangle\!\leftrightarrow\!|4\rangle$ | 17(3) | 27(8) | 32(7) |
  | $|6\rangle\!\leftrightarrow\!|5\rangle$ | 14(3) | 25(7) | 26(6) |
  | $|7\rangle\!\leftrightarrow\!|6\rangle$ | 13(3) | 22(8) | 24(6) |
  | $|8\rangle\!\leftrightarrow\!|7\rangle$ | 14(3) | 21(7) | 24(6) |
  | $|9\rangle\!\leftrightarrow\!|8\rangle$ | 13(2) | 16(5) | 22(5) |
  (Measurements interleaved over **>3 days** to average temporal fluctuations.)
- **Implied relaxation exponent — strongly supportive of $k^{0.7}$ *globally*, less so at $k=2$.** $\Gamma_9/\Gamma_1 = 64/13 = 4.92$; a $k^p$ fit through the endpoints gives $p = \ln 4.92/\ln 9 = \mathbf{0.73}$ (main.tex uses 0.7; textbook linear would give 9). **But $\Gamma_2/\Gamma_1 = 64/34 = 1.88$**, not 1.7 — the local exponent over the first step is $\ln 1.88/\ln 2 = 0.91$, near-linear. The sub-linearity comes from saturation at $k\ge6$ (13–14 µs flat), which the authors note: "the experimental results show close values when initializing transmon at $|6\rangle$ to $|9\rangle$." Error bars are wide (64±15, 34±8), so 1.88 is statistically compatible with both 1.7 and 2.0.
- **Echo approaches the $T_1$ limit — main.tex's claim (b) is directly and verbatim supported:** "We find that our measured echo times $T_{2E}$ approach $2T_1$, especially for the higher transitions, suggesting that **there are no additional strong dephasing channels and that the coherence is mostly limited by $T_1$ decay**. The pure dephasing time $T_\phi$ ... we found to be around **300 µs in $\{|0\rangle,|1\rangle\}$ and 200 µs in $\{|8\rangle,|9\rangle\}$**." (The abstract likewise: "$T_{2E}$ for the higher levels is close to the limit of $T_1$ decay, primarily limited by bosonic enhancement.")
- **Consequence for the dephasing ratio.** Because dephasing is nearly unresolved here, the extracted $\Gamma_\phi = 1/T_{2E}-1/(2T_1)$ ratios are noisy and **non-monotonic**: $\Gamma_\phi^{12}/\Gamma_\phi^{01} \approx 1.4$, $\Gamma_\phi^{23}/\Gamma_\phi^{01}\approx 0.47$, $\Gamma_\phi^{34}/\Gamma_\phi^{01}\approx 0.62$. **This device therefore does not, on its own, support $\Gamma_\phi^{01}:\Gamma_\phi^{12}=1{:}2.0$** — which is consistent with main.tex using it as the *low-charge-dispersion* endpoint rather than the calibrated-ladder anchor. **No 0–2 coherence is measured** (all Ramsey/echo are adjacent-level subspaces), so wang2025 cannot support the $\Gamma_\phi^{02}=2.3$ element.
- **Charge dispersion.** Standard-transmon $\epsilon_m$ formula given as Eq. (4), $\epsilon_m \propto \frac{2^{4m+5}}{m!}(\ldots)$ — the source of the order-of-magnitude growth from $|1\rangle$ to $|2\rangle$ that main.tex invokes. Measured $\delta f = (|\epsilon_m|+|\epsilon_{m+1}|)/h$: **Q0 ($E_J/E_C=88$) $|3\rangle\!\leftrightarrow\!|4\rangle$: 901 kHz** vs **Q5 ($E_J/E_C=325$) $|9\rangle\!\leftrightarrow\!|10\rangle$: 292 kHz**. Lower transitions have $\delta f<20$ kHz, **below measurement resolution**. "This validates the idea that high values of $E_J/E_C$ effectively suppress charge dispersion in the highly excited states." Caveat the authors raise: the standard transmon model **underestimates** the measured $\delta f$; the Josephson-harmonics model ($M=2$) fits better, because $E_{J1}/E_C$ is overestimated (325 → 270–290 on Q5).
- **Readout — main.tex's 93.8% is exact.** 10-state single-shot assignment fidelity: **93.8% with a deep neural network on raw traces**, vs **85.8% with a Gaussian mixture model** on the same 8000-train/2000-test data (a 56% reduction in assignment error). Per-state DNN diagonal (Fig. 4b): $|0\rangle$ 99.8%, $|1\rangle$ 98.6, $|2\rangle$ 94.2, $|3\rangle$ 96.2, $|4\rangle$ 94.8, $|5\rangle$ 91.3, $|6\rangle$ 86.6, $|7\rangle$ 83.1, $|8\rangle$ 96.0, $|9\rangle$ 97.6 — i.e. **not monotone in level**, with the worst states $|6\rangle$/$|7\rangle$, and the $|9\rangle$ figure *higher* than $|5\rangle$–$|7\rangle$. Readout uses **three simultaneous tones on one resonator, 2.2 µs readout length**; the authors attribute the dominant errors $P(i-1|i)$ to "decay during readout ... estimate that the 2.2 µs spontaneous decay can induce up to **3% error for preparing $|1\rangle$ and up to 16% for preparing $|9\rangle$**."
- **Control fidelity.** Process infidelities $e_f < 3\times10^{-3}$ for qubit-like RB on **every** calibrated adjacent-level transition in the lowest 10 levels; minimal EPC $= 3.25(9)\times10^{-4}$ at 44 ns on $\{|0\rangle,|1\rangle\}$ (close to the coherence limit). Qudit state tomography of $(|0\rangle+|8\rangle)/\sqrt2$ on Q4: **state fidelity 98.2%** (limited by 8 sequential pulses + SPAM).
- **Relaxation mechanism (Appendix D).** $\Gamma_1 = \Gamma_{1,\rm QP}+\Gamma_{1,\rm Purcell}+\Gamma_{1,\rm diel}+\ldots$. Neither Purcell nor quasiparticle loss alone reproduces the measured scaling; **dielectric loss with $Q_{\rm diel,0}=2.2\times10^6$, $\epsilon=1.2$** best captures the trend. So the sub-linear ladder here is a *dielectric-loss* signature, not a universal transmon law.
- **Two-qudit ZZ.** Native $J = 1.59$ MHz (Q1–Q2); effective ZZ shift $\simeq 0.4$ MHz in the $\{|0\rangle,|1\rangle\}\otimes\{|0\rangle,|1\rangle\}$ encoding, growing to $\sim 4$ MHz for higher levels — "boosted by bosonic enhancement."

**Judge verification questions:**
- Main.tex says the relaxation ratio is "measured at $\approx1.7$" citing wang2025 among others. Wang's own Table III gives $\Gamma_2/\Gamma_1 = 64/34 = 1.88$. Does main.tex's "$\approx1.7$" (and its reported channel value of 1.62) stay within the honest envelope of this dataset, given $T_1$ uncertainties of ±15 and ±8 µs?
- Main.tex says the high-$E_J/E_C$ knob models the regime "where echo coherence approaches the $T_1$ limit." Is this a verbatim match to the paper's "$T_{2E}$ approach $2T_1$ ... coherence is mostly limited by $T_1$ decay"? (It appears to be.) Does main.tex correctly describe this as an *interpolation endpoint* rather than the calibrated operating point?
- Main.tex places "Wang's ten-state single-shot readout at 93.8%" at the *upper end* of $\varepsilon\approx0.01$–$0.03$ in a $(1{+}k)$ level-dependent readout-error model. Wang's per-state fidelities are **non-monotone in $k$** (worst at $|6\rangle$–$|7\rangle$, and $|8\rangle$/$|9\rangle$ recover to 96%/97.6%). Does main.tex's $(1{+}k)$ linear-in-level model misrepresent this device, and does main.tex flag that 93.8% is the **DNN** number while the simpler GMM classifier gives 85.8%?
- Does main.tex attribute the dephasing ratio $1:2.0:2.3$ to wang2025? This device measures **no 0–2 coherence** and its echo dephasing is non-monotone in level — is wang2025 used only for the low-charge-dispersion *variant*, as it should be?
- Wang's sub-linear $T_1$ scaling is attributed to **dielectric loss with fitted phenomenological parameters** ($Q_{\rm diel,0}=2.2\times10^6$, $\epsilon=1.2$), not to a device-independent law, and saturates at $|6\rangle$–$|9\rangle$. Does main.tex claim $k^{0.7}$ is a *universal* transmon ladder, or does it present it as an empirical fit to the aggregated data?

---

---

## `weng2024` — Implementation of Shor's Algorithm with a Single Photon in 32 Dimensions (Weng & Chuu, 2024)

**Full citation:** H.-C. Weng, C.-S. Chuu, "Implementation of Shor's algorithm with a single photon in 32 dimensions," Phys. Rev. Applied **22**, 034003 (2024), doi:10.1103/PhysRevApplied.22.034003; arXiv:2408.08138.
**Source:** arXiv:2408.08138v1 (15 Aug 2024) / PRApplied 22, 034003, PDF: `weng-2024-shor-single-photon-32-dimensions.pdf`

**Cited in main.tex:**
- *Discussion*: "single-qudit demonstrations reach $d=8$ on a trapped ion~\cite{shi2025} and, **on photonic platforms, $d=32$ Shor and qudit QPE**~\cite{weng2024,lu2020}" — i.e. weng2024 is the $d=32$ Shor half of that pair, offered as evidence of the experimental reach of *single-qudit* (as opposed to multi-qudit entangling) demonstrations.

**What the paper actually shows (full-text, not abstract-level):**
- **The $d=32$ claim is literal and correct in the encoding sense.** Information is encoded in **32 time-bin modes of a single heralded photon** — "the largest reported to date for a time-bin-encoded single photon." The 32 time bins carry the 5-"qubit" register $|f_1 f_0 x_2 x_1 x_0\rangle$, i.e. $2^5 = 32$ computational basis states realised as one 32-dimensional single-particle Hilbert space.
- **It is a *compiled* Shor, factoring $N=15$ with $a=2$.** Register initialisation prepares $(|10000\rangle+\cdots+|10111\rangle)/\sqrt8$; after modular exponentiation the state is $(|00100\rangle+|00101\rangle+|01110\rangle+|01111\rangle+|10000\rangle+|10001\rangle+|11010\rangle+|11011\rangle)/\sqrt8$.
- **Critical caveat: the inverse QFT is not run on hardware.** "Since $r = 4 = 2^m$ for natural numbers $m$, **the inverse QFT can be carried out by the classical processing** [28–30,35]." The measured output (Fig. 6) is the *classically post-processed* argument register, compared against a theory curve that "considers initial time-bin modes with even amplitudes."
- **Outcome interpretation.** Interference peaks at $x = c2^3/r = 0,2,4,6$ (i.e. bitstrings 000, 010, 100, 110). "The case $x=0$ is an inherent failure of Shor's algorithm while the case $x=4$ gives the trivial result of the factors 1 and 15. The cases $x=2$ and $x=6$ result in finding the order $r=4$ with the factors $\gcd(a^{r/2}\pm1,N)=3$ and 5." So **only 2 of the 4 peaks (≈50% of the non-failure outcomes) yield the nontrivial factorisation** — the standard compiled-Shor caveat.
- **Hardware.** Type-II PPKTP monolithic cavity, cw 775 nm pump, heralded 1550 nm single photons with a **148 ns $1/e^2$ coherence time / 2.7 MHz bandwidth**, pair generation $4.2\times10^5$ s$^{-1}$mW$^{-1}$. Fibre loop with electro-optic amplitude modulator (state prep in **one shot**), polarization-switch mode couplers, 200 ns optical delay. Detectors: **15% quantum efficiency, 150 ps timing resolution**; time digitizer 100 ps. Losses: EOM 2 dB, polarization switch 3.5 dB insertion loss.
- **Statistics.** "For the result in (d), a coincidence count rate of **10 counts/s** is observed and the statistics is accumulated for **30 minutes**." Amplitudes across time bins are **uneven** — "due to the double-exponential single-photon wave packet and the different losses experienced by different time-bin modes." No reported state or process fidelity for the full algorithm; only a CNOT$_{10}$ truth table and single-qubit rotation Bloch-sphere characterisation (Fig. 4), described qualitatively as "in good agreement."
- **No entanglement between particles, and no scaling.** This is explicitly single-photon: "the powerful information processing capacity of a single photon in high dimensions." The authors themselves note that scalability would require multi-photon interferometry: "The high-dimensional states may also be manipulated by the high-dimensional quantum gates with the single-qudit interferometry replaced by a **multi-qudit interferometry**, in which the use of **multiple photons provides the scalability**." Extrapolation: "encoding more than 5000 time-bin modes on temporally long single photons is possible" with 40 GHz EOMs.
- **Honest note on noise from the authors:** "The manipulation and noise with the high-dimensional states are usually more troublesome compared to the qubits."
- **No decoherence model, no per-level coherence data, no dimension sweep** — it is a single-point $d=32$ demonstration.

**Judge verification questions:**
- Main.tex groups weng2024 under "**single-qudit** demonstrations." Is that accurate? (Yes — one photon, one time-bin DOF, no inter-particle entanglement — and it matters because the sentence contrasts these with the multi-qudit entangling demonstrations at $d=3$/$d=5$.)
- Does main.tex say or imply that this is a *full* hardware Shor at $d=32$? The inverse QFT was **carried out classically** (justified because $r=4=2^m$), and the circuit is the standard compiled $N=15$, $a=2$ instance — does main.tex's phrasing "$d=32$ Shor" overstate what was executed on the device?
- Main.tex uses this citation immediately before Table~\ref{tab:prediction} ("predicted success probabilities at common per-base strengths, computed by exact density-matrix evolution"). Does main.tex avoid implying that weng2024 provides any *noise* or *fidelity* benchmark? (The paper reports none for the full algorithm — only 10 counts/s over 30 min with uneven, loss-dependent amplitudes and 15%-efficiency detectors.)
- Does main.tex correctly keep weng2024 out of any $d$-scaling or advantage claim, given that the paper is a single-point demonstration with no dimension comparison?

---

---

## `yurtalan2020` — Characterization of Multi-Level Dynamics and Decoherence in a High-Anharmonicity Capacitively Shunted Flux Circuit (Yurtalan, Shi, Flatt & Lupascu, 2020)

**Full citation:** M. A. Yurtalan, J. Shi, G. J. K. Flatt, A. Lupascu, "Characterization of multi-level dynamics and decoherence in a high-anharmonicity capacitively shunted flux circuit," arXiv:2008.00593 (v2, 24 Feb 2022).
**Source:** arXiv:2008.00593v2, PDF: `yurtalan-2020-multilevel-decoherence-flux-qutrit.pdf`

**Cited in main.tex:**
- *Noise channels*: one of six sources for "the relaxation ratio $\Gamma_2/\Gamma_1$ is measured at ${\approx}1.7$ ... against $2.0$ for the textbook $\Gamma_k\propto k$ ladder", and part of the claim that "Both exponents are fits to published per-level coherence data spanning **nine devices and $d=3$ to $12$**", including the dephasing ratios $\Gamma_\phi^{01}:\Gamma_\phi^{12}:\Gamma_\phi^{02} = 1:2.0:2.3$ said to be "incompatible with the textbook $(\Delta\mathrm{level})^2$ law ... because the **charge dispersion of $|2\rangle$ exceeds that of $|1\rangle$ by an order** [of magnitude]".

**What the paper actually shows (full-text, not abstract-level):**
- **This is NOT a transmon.** It is a **three-Josephson-junction capacitively shunted flux circuit** with three shunt pads, $\alpha=0.61$, $E_J/E_C = 6.9$ for the small junction ($E_J/h = 50.9$ GHz), operated at/near the flux symmetry point $\Phi=0.5\Phi_0$. **Anharmonicity $2\pi\times3.69$ GHz** (vs ~100–200 MHz for the transmons in wang2025). One device; qutrit space = lowest three levels ($d=3$ only).
- **Transition frequencies at the symmetry point:** $\omega_{01}=2\pi\times1.708$ GHz, $\omega_{12}=2\pi\times5.398$ GHz, $\omega_{02}=2\pi\times7.107$ GHz. The 0–2 transition is **forbidden by selection rules at the symmetry point** (visible only off-symmetry).
- **Multi-level relaxation/excitation rates (Table II) — the numbers bearing on $\Gamma_2/\Gamma_1$:**
  | Rate | at $0.5\,\Phi_0$ | at $0.501\,\Phi_0$ |
  |---|---|---|
  | $\Gamma_{01}$ | 1.4 kHz | 1.2 kHz |
  | $\Gamma_{10}$ | **29.5 kHz** | **63.4 kHz** |
  | $\Gamma_{12}$ | 8.8 Hz | 0.4 Hz |
  | $\Gamma_{21}$ | **124.3 kHz** | **78.1 Hz** *(printed as Hz; almost certainly a units typo for kHz)* |
  | $\Gamma_{02}$ | 0.1 Hz | 0.01 Hz |
  | $\Gamma_{20}$ | 27.8 kHz | 61.1 kHz |
  - **$\Gamma_2/\Gamma_1 = \Gamma_{21}/\Gamma_{10} = 124.3/29.5 = 4.21$ at the symmetry point** — i.e. **more than double** the textbook 2.0 and 2.5× main.tex's "$\approx1.7$". Off-symmetry, taking the printed 78.1 as kHz gives 1.23; taking it literally as Hz gives 0.0012 (implausible). **Either way this device is a strong outlier against the $\approx1.7$ figure.**
  - The authors explain it physically: "The decay rate for the 1-2 transition is higher than the 0-1 level, **consistent with the larger transition strength**." They also note a substantial $\Gamma_{20}=27.8$ kHz **despite the 0–2 transition being selection-rule forbidden** at the symmetry point, tentatively attributed to quasiparticle-induced relaxation.
- **Multi-level dephasing — contradicts the max-level law on this device.**
  - At the symmetry point (Fig. 5 caption): Ramsey coherence times **4.7 µs (0–1), 3.4 µs (1–2), 5.4 µs (0–2)** → rate ratios $1 : 1.38 : 0.87$. **The 0–2 coherence is the LONGEST of the three**, i.e. $\Gamma^{02} < \Gamma^{01}$, the opposite of main.tex's $1{:}2.0{:}2.3$ ordering and of the textbook $1{:}1{:}4$.
  - Off-symmetry at $\Phi = 0.501\Phi_0$: "leading to **dephasing rates of 2.7 MHz and 0.9 MHz**" for 0–1 and 0–2 respectively → $\Gamma_\phi^{02}/\Gamma_\phi^{01} = \mathbf{0.33}$. The authors explain: "The Ramsey dephasing rates for 0-1 and 0-2 coherences at $\Phi=0.501\Phi_0$ are **in a ratio proportional to the flux sensitivity coefficients**, suggesting that **flux noise is the dominant dephasing source for higher levels as well**."
- **The dominant dephasing mechanism is FLUX noise, not charge dispersion.** "dephasing away from the symmetry point is dominated by flux noise ... PSD of the form $A/|\omega|^\delta$"; extracted $A = 1.8\times10^{-14}\,(\mathrm{rad/s})^{\delta-1}\Phi_0^2$, $\delta = 0.68$ over 3–46 MHz. Charge noise is explicitly ruled out: "We performed numerical simulations of the charge dispersion, yielding a charge modulation over one period of the island charges of $2\pi\times$**133 Hz, 626 Hz, and 493 Hz** for the transitions 0-1, 1-2 and 0-2, respectively. The contribution of this source to the dephasing rate ... is therefore a **negligible contribution** to the measured rate."
  - Note the *shape* of that simulated charge dispersion, $1 : 4.7 : 3.7$, is qualitatively **max-level-like** ($\Gamma^{12}\approx\Gamma^{02} > \Gamma^{01}$) and inconsistent with the textbook $1{:}1{:}4$ — but it is a *simulation of an effect the authors say is negligible on this device*, not a measured dephasing ratio.
- **Two-level (qubit) baseline numbers.** $T_1$ mostly 35–45 µs, reaching 47.1±2.0 µs; Ramsey 4.7 µs (exponential fit) / 7.3 µs (Gaussian); **spin-echo $T_{2E}=9.4$ µs**; CPMG $T=26.5$ µs at $N=100$, scaling as $N^{0.42}$. Average single-qubit gate fidelity **99.92±0.003%** by RB with 1.62 ns ($\pi/2$) and 2.64 ns ($\pi$) pulses. Effective qubit temperature 27–32 mK vs 27 mK cryostat.
- **Other decoherence sources the authors considered and largely excluded:** cavity photon noise (a 250 mK photon temperature would be needed to explain the Ramsey rate — "unreasonably high"; spin-locking bounds the cavity at 67 mK, 4.68 kHz), flux noise at the symmetry point (predicted times "significantly longer than experimentally measured"), quasiparticles ($T_1^{qp}=37.6$ µs, $T_1^R=47.6$ µs, mean 0.23±0.20 QPs), and TLFs (Ramsey $T_\phi$ rose to 10 µs in a later cooldown at unchanged energy gap). Their own summing-up: "this analysis is **not conclusive** in terms of identifying the dominant dephasing mechanisms."

**Judge verification questions:**
- Main.tex cites yurtalan2020 in support of "$\Gamma_2/\Gamma_1$ measured at ${\approx}1.7$". This device's Table II gives $\Gamma_{21}/\Gamma_{10} = 124.3/29.5 = \mathbf{4.21}$ at the symmetry point. Is this reference actually consistent with the cited ratio, or does its inclusion in the six-source list overstate the agreement of the underlying data?
- Main.tex attributes the departure from the textbook $(\Delta\mathrm{level})^2$ law to "the charge dispersion of $|2\rangle$ exceed[ing] that of $|1\rangle$ by an order [of magnitude]". In Yurtalan's device the simulated charge dispersion ratio is $1:4.7:3.7$ (a factor ~5, not 10) **and charge noise is explicitly stated to be a negligible contributor**, with flux noise dominant. Does main.tex's mechanism apply to this reference at all?
- Yurtalan's measured dephasing gives $\Gamma_\phi^{02}/\Gamma_\phi^{01} = 0.33$ off-symmetry and $0.87$ at the symmetry point — the 0–2 coherence is *longer* than 0–1, the reverse of main.tex's $1{:}2.0{:}2.3$. If main.tex's grouped citation implies this device supports the max-level dephasing law, is that a misrepresentation, and does main.tex disclose that the ordering is inverted here?
- Main.tex says the exponents are "fits to published per-level coherence data **spanning nine devices and $d=3$ to $12$**." Yurtalan contributes **one** device at $d=3$, and it is a **capacitively shunted flux circuit with $E_J/E_C = 6.9$ and $2\pi\times3.69$ GHz anharmonicity**, not a transmon. Does main.tex's framing of the calibration set as "published per-level **transmon** coherence measurements" (Introduction) accurately include this reference?