"""
Qudit Shor order-finding with decoherence.

Simulates quantum phase estimation for order finding (the quantum core of
Shor's algorithm) on registers of d-level qudits for prime d in {2, 3, 5},
evolving the full density matrix under per-gate noise channels.

The point of the experiment: for a fixed factoring problem (N = 15, a = 7),
compare how the success probability of the algorithm degrades with noise
when the same computation is carried by qubits (d=2), qutrits (d=3) or
ququints (d=5), under two physically motivated noise models:

* "transmon"      - amplitude-damping ladder (level k decays at rate k*gamma)
                    plus number-operator dephasing (coherence between levels
                    j,k decays as exp(-gamma_phi (j-k)^2 t / 2)). This is the
                    noise structure of an anharmonic-oscillator qudit
                    (transmon higher levels, cavity modes): higher levels are
                    strictly worse.
* "depolarizing"  - uniform depolarizing channel with the same per-qudit rate
                    regardless of d. This models platforms whose levels are
                    all comparably good (trapped-ion hyperfine/optical
                    qudits, nuclear/electron spin manifolds): noise is paid
                    per particle and per time step, not per level.

Conventions
-----------
* A register is described by a list of qudit dimensions ``dims``. The density
  matrix is stored as an ndarray of shape dims + dims (row indices first).
* Integer <-> digit encoding is big-endian: qudit 0 holds the most
  significant digit.
* vec() is row-major: vec(rho)[r*d + c] = rho[r, c]. A single-qudit channel
  is a (d^2 x d^2) superoperator E with vec(rho') = E @ vec(rho), and
  vec(A X B) = kron(A, B.T) vec(X).
"""

from __future__ import annotations

from math import gcd

import numpy as np
from scipy.linalg import expm

# ---------------------------------------------------------------------------
# Elementary gates
# ---------------------------------------------------------------------------


def fourier(d: int) -> np.ndarray:
    """Single-qudit Fourier gate F_d (the generalized Hadamard)."""
    j, k = np.indices((d, d))
    return np.exp(2j * np.pi * j * k / d) / np.sqrt(d)


def qft_matrix(D: int) -> np.ndarray:
    """Dense QFT over Z_D (reference for tests)."""
    j, k = np.indices((D, D))
    return np.exp(2j * np.pi * j * k / D) / np.sqrt(D)


def cphase(d: int, denom_power: int) -> np.ndarray:
    """Two-qudit diagonal gate  |c1,c2> -> exp(2*pi*i c1 c2 / d**denom_power)."""
    U = np.zeros((d * d, d * d), complex)
    for c1 in range(d):
        for c2 in range(d):
            idx = c1 * d + c2
            U[idx, idx] = np.exp(2j * np.pi * c1 * c2 / d ** denom_power)
    return U


def cmult_unitary(d: int, w: int, mult: int, N: int) -> np.ndarray:
    """Controlled modular multiplier on (1 control qudit) x (w work qudits).

    For control digit c, maps work state |x> -> |mult^c * x mod N> for x < N,
    and acts as identity on the unused states x >= N. Requires gcd(mult, N)=1
    so the map is a permutation.
    """
    if gcd(mult, N) != 1:
        raise ValueError("mult must be a unit mod N")
    Dw = d ** w
    if Dw < N:
        raise ValueError("work register too small")
    U = np.zeros((d * Dw, d * Dw))
    for c in range(d):
        f = pow(mult, c, N)
        for x in range(Dw):
            y = (f * x) % N if x < N else x
            U[c * Dw + y, c * Dw + x] = 1.0
    return U


# ---------------------------------------------------------------------------
# Digit bookkeeping
# ---------------------------------------------------------------------------


def digits_of(x: int, d: int, n: int) -> list[int]:
    """Big-endian base-d digits of x, length n."""
    return [(x // d ** (n - 1 - i)) % d for i in range(n)]


def reverse_digits(x: int, d: int, n: int) -> int:
    """Integer whose base-d digit string is the reverse of x's."""
    ds = digits_of(x, d, n)
    return sum(v * d ** i for i, v in enumerate(ds))


# ---------------------------------------------------------------------------
# Tensor-network style application of gates / channels to a density matrix
# ---------------------------------------------------------------------------


def apply_unitary(rho: np.ndarray, U: np.ndarray, sites: tuple[int, ...],
                  dims: list[int]) -> np.ndarray:
    """rho -> U rho U^dag with U acting on ``sites`` (ascending order)."""
    n = len(dims)
    k = len(sites)
    assert list(sites) == sorted(sites), "sites must be ascending"
    ds = [dims[s] for s in sites]
    Ut = U.reshape(ds + ds)
    # Row side: contract U's input legs with rho's row legs.
    rho = np.tensordot(Ut, rho, axes=(list(range(k, 2 * k)), list(sites)))
    rho = np.moveaxis(rho, list(range(k)), list(sites))
    # Column side: contract rho's column legs with conj(U)'s input legs.
    col_sites = [n + s for s in sites]
    rho = np.tensordot(rho, np.conj(Ut), axes=(col_sites, list(range(k, 2 * k))))
    rho = np.moveaxis(rho, list(range(2 * n - k, 2 * n)), col_sites)
    return rho


def apply_unitary_vec(t: np.ndarray, U: np.ndarray, sites: tuple[int, ...],
                      dims: list[int]) -> np.ndarray:
    """psi -> U psi on a state tensor of shape dims (sites ascending).

    Extra trailing axes (e.g. a batch axis) are allowed and untouched.
    """
    k = len(sites)
    ds = [dims[s] for s in sites]
    Ut = U.reshape(ds + ds)
    t = np.tensordot(Ut, t, axes=(list(range(k, 2 * k)), list(sites)))
    return np.moveaxis(t, list(range(k)), list(sites))


def kraus_from_superop(E: np.ndarray) -> list[np.ndarray]:
    """Kraus operators of a channel given as a superoperator (row-major vec).

    Via the Choi matrix C[(r,i),(c,j)] = E(|i><j|)[r,c]; eigenvectors with
    positive eigenvalues, reshaped, are the Kraus operators.
    """
    d = int(round(np.sqrt(E.shape[0])))
    C = np.zeros((d * d, d * d), complex)
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d))
            eij[i, j] = 1.0
            out = (E @ eij.reshape(-1)).reshape(d, d)
            # place out[r,c] at C[(r,i),(c,j)]
            for r in range(d):
                for c in range(d):
                    C[r * d + i, c * d + j] += out[r, c]
    C = (C + C.conj().T) / 2
    evals, evecs = np.linalg.eigh(C)
    kraus = []
    for lam, v in zip(evals, evecs.T):
        if lam > 1e-12:
            kraus.append(np.sqrt(lam) * v.reshape(d, d))
    return kraus


def apply_channel(rho: np.ndarray, E: np.ndarray, site: int,
                  dims: list[int]) -> np.ndarray:
    """Apply a single-qudit superoperator E (d^2 x d^2, row-major vec)."""
    n = len(dims)
    d = dims[site]
    t = np.moveaxis(rho, [site, n + site], [0, 1])
    shape = t.shape
    t = E @ t.reshape(d * d, -1)
    t = t.reshape(shape)
    return np.moveaxis(t, [0, 1], [site, n + site])


# ---------------------------------------------------------------------------
# Noise channels
# ---------------------------------------------------------------------------


def _dissipator(J: np.ndarray) -> np.ndarray:
    """Lindblad dissipator superoperator for jump operator J (row-major vec)."""
    d = J.shape[0]
    I = np.eye(d)
    JdJ = J.conj().T @ J
    return (np.kron(J, J.conj())
            - 0.5 * np.kron(JdJ, I)
            - 0.5 * np.kron(I, JdJ.T))


def _relaxation_dissipator(amps: np.ndarray, relaxation: str) -> np.ndarray:
    """Ladder relaxation with per-transition amplitudes amps[k-1] on |k-1><k|.

    "secular": one independent jump operator per transition, sum_k
    D[amps_k |k-1><k|]. For an anharmonic ladder the Bohr frequencies
    w_{k,k-1} are split by the anharmonicity (hundreds of MHz) while the
    decay rates are kHz-MHz, so the secular Born-Markov limit applies and
    cross-transition coherence-transfer terms rho_{j,k} -> rho_{j-1,k-1}
    (j != k) are rotated away. This is the physical form for a transmon.

    "collective": the single jump a = sum_k amps_k |k-1><k| (harmonic-
    oscillator form, exact only for degenerate Bohr frequencies). Retains
    the coherence-transfer terms; kept for auditing pre-revision results.

    Populations evolve identically under both; at d=2 the two coincide.
    """
    d = amps.shape[0] + 1
    if relaxation == "collective":
        return _dissipator(np.diag(amps, 1))
    if relaxation != "secular":
        raise ValueError(f"unknown relaxation form: {relaxation!r}")
    L = np.zeros((d * d, d * d))
    for k in range(1, d):
        Lk = np.zeros((d, d))
        Lk[k - 1, k] = amps[k - 1]
        L += _dissipator(Lk)
    return L


def transmon_superop(d: int, gamma_tau: float,
                     dephase_ratio: float = 1.0,
                     relaxation: str = "secular") -> np.ndarray:
    """One time-layer of anharmonic-ladder noise.

    Jump operators: sqrt(k)|k-1><k| per transition (rate gamma; see
    `_relaxation_dissipator` for the secular/collective distinction), and
    the number operator n_hat (rate dephase_ratio * gamma). gamma_tau is
    the dimensionless product (rate x layer duration).
    """
    amps = np.sqrt(np.arange(1.0, d))
    n_op = np.diag(np.arange(d, dtype=float))
    L = (gamma_tau * _relaxation_dissipator(amps, relaxation)
         + gamma_tau * dephase_ratio * _dissipator(n_op))
    return expm(L)


def depolarizing_superop(d: int, p: float) -> np.ndarray:
    """One time-layer of uniform depolarizing: rho -> (1-p) rho + p I/d."""
    vec_i = np.eye(d).reshape(-1)
    return (1 - p) * np.eye(d * d) + (p / d) * np.outer(vec_i, vec_i)


# --- Calibrated transmon noise ---------------------------------------------
# The idealized `transmon_superop` above assumes textbook scalings: level-k
# decay rate exactly k*gamma (bosonic enhancement) and dephasing exactly
# (j-k)^2 (a frequency ladder linear in level index). Published per-level
# coherence measurements say both are wrong, in opposite directions:
#
#   Relaxation. Measured Gamma_12/Gamma_01 = 1.7 mean over 9 transmons
#   (Goss 2022, Blok 2020) and T1 = 53/33.7/24.3 us for levels 1/2/3
#   (Tripathi 2024) -> Gamma_k ~ k^0.68, i.e. SUBLINEAR. Peterer 2015
#   confirms decay is sequential |k> -> |k-1> up to the 4th level.
#
#   Dephasing. Pure-dephasing rates extracted from echo data (T1
#   contribution subtracted) give median ratios
#       Gamma_phi(0,1) : Gamma_phi(1,2) : Gamma_phi(0,2) = 1 : 2.0 : 2.3,
#   whereas (Delta level)^2 predicts 1 : 1 : 4. The measured pattern is a
#   "max level" law -- any coherence touching level 2 costs ~2x -- because
#   the charge dispersion of |2> is >=10x that of |1> (Blok: 12 kHz vs
#   261 Hz), an independent noise channel rather than a steeper ladder.
#
# Both corrections make the idealized model too harsh on qudits, so the
# calibrated channel is the honest test of the "qubits win Shor on
# transmon-like hardware" claim.
#
# `dephase_scale` interpolates toward the high-E_J/E_C regime of Wang et
# al. 2024 (12 levels on one transmon, T2-echo approaching the T1 limit):
# scale 1.0 = devices as measured, scale 0.0 = charge noise engineered
# away, leaving only the relaxation ladder.

DAMPING_EXPONENT = 0.7    # Gamma_k ~ k^0.7  (measured ~0.68)
DEPHASE_EXPONENT = 1.1    # max(j,k)^1.1 -> 2.15x at level 2 (measured 2.0-2.3)


def _mds_dephasing_jumps(gphi: np.ndarray) -> list[np.ndarray]:
    """Diagonal jump operators realizing a target pure-dephasing matrix.

    With diagonal jumps L_m = diag(c_m), the coherence (j,k) decays at
    Gamma_phi(j,k) = 0.5 * sum_m (c_m(j) - c_m(k))^2 -- i.e. half the squared
    Euclidean distance between the level vectors v_j = (c_1(j), c_2(j), ...).
    So realizing a target matrix is exactly a Euclidean embedding problem:
    classical multidimensional scaling on D^2 = 2*Gamma_phi returns the
    coordinates, whose columns are the jump operators. Any target that is a
    valid squared-distance matrix (sqrt obeys the triangle inequality) is
    realizable; the caller should check `dephasing_residual`.
    """
    d = gphi.shape[0]
    D2 = 2.0 * gphi
    J = np.eye(d) - np.ones((d, d)) / d
    B = -0.5 * J @ D2 @ J
    B = (B + B.T) / 2
    evals, evecs = np.linalg.eigh(B)
    return [np.diag(np.sqrt(lam) * v)
            for lam, v in zip(evals, evecs.T) if lam > 1e-12]


def dephasing_matrix(d: int, gamma_tau: float, dephase_ratio: float = 1.0,
                     dephase_exponent: float = DEPHASE_EXPONENT,
                     dephase_scale: float = 1.0) -> np.ndarray:
    """Target pure-dephasing rate matrix under the measured max-level law.

    Normalized so the 0<->1 coherence decays at exactly the same rate as in
    the idealized model -- hence d=2 results are bit-for-bit unchanged and
    any difference between the two models is purely a higher-level effect.
    """
    idx = np.arange(d)
    mx = np.maximum.outer(idx, idx).astype(float)
    gphi = (0.5 * gamma_tau * dephase_ratio * dephase_scale
            * mx ** dephase_exponent)
    np.fill_diagonal(gphi, 0.0)
    return gphi


def dephasing_residual(gphi: np.ndarray) -> float:
    """Max deviation between a target dephasing matrix and what the MDS jump
    operators actually realize (0 if exactly embeddable)."""
    jumps = _mds_dephasing_jumps(gphi)
    got = np.zeros_like(gphi)
    for L in jumps:
        c = np.real(np.diag(L))
        got += 0.5 * (c[:, None] - c[None, :]) ** 2
    return float(np.abs(got - gphi).max())


def transmon_calibrated_superop(d: int, gamma_tau: float,
                                dephase_ratio: float = 1.0,
                                damping_exponent: float = DAMPING_EXPONENT,
                                dephase_exponent: float = DEPHASE_EXPONENT,
                                dephase_scale: float = 1.0,
                                relaxation: str = "secular") -> np.ndarray:
    """One time-layer of transmon noise calibrated to measured per-level data.

    Relaxation uses one jump operator per transition (secular form; see
    `_relaxation_dissipator`) -- the sequential population decay of
    Peterer 2015 fixes the rates but not the form, and the anharmonicity
    makes the secular choice the physical one. The pre-revision collective
    form is available as relaxation="collective".
    """
    amps = np.sqrt(np.arange(1.0, d) ** damping_exponent)
    L = gamma_tau * _relaxation_dissipator(amps, relaxation)
    if dephase_ratio > 0 and dephase_scale > 0:
        gphi = dephasing_matrix(d, gamma_tau, dephase_ratio,
                                dephase_exponent, dephase_scale)
        for Ld in _mds_dephasing_jumps(gphi):
            L = L + _dissipator(Ld)
    return expm(L)


# --- Zeeman-structured ion dephasing (Ringbauer 40Ca+ encoding) ------------
# Level indexing of Ringbauer et al. 2022, Fig. 1 (ordered by magnetic
# sensitivity): S(-1/2), D(-1/2), S(+1/2), D(+1/2), D(-3/2), D(+3/2),
# D(-5/2). Magnetic-field noise shifts level j by g_j m_j mu_B B, so a
# single diagonal jump ~ diag(g_j m_j) dephases pair (j, k) at a rate
# ~ (g_j m_j - g_k m_k)^2; the allowed-transition sensitivities span the
# "factor of 5" quoted in the paper. NOTE: applied per carrier by
# run_circuit, this is LOCAL (uncorrelated) field noise carrying the
# collective-B sensitivity structure -- the uncorrelated worst case.
# Genuinely common-mode dephasing (one field for the whole string, with
# its decoherence-free pairs) is implemented in collective_zeeman.py.
# Coefficients g_j m_j follow from g_S = 2, g_D = 6/5 (derived; the
# paper tabulates no per-pair numbers). Relaxation is omitted: every
# level is ground-state or metastable (tau_1 ~ 1.1 s).

ZEEMAN_COEFF = (-1.0, -0.6, 1.0, 0.6, -1.8, 1.8, -3.0)


def ion_zeeman_superop(d: int, gamma_tau: float) -> np.ndarray:
    """One time-layer of collective-B dephasing on the 40Ca+ encoding.

    Normalized so the optical-qubit pair 0<->1 dephases at exactly
    gamma_tau: the d=2 block is identical for every d (the calibrated
    ladder's convention), so every cross-base difference is purely a
    higher-level effect. Pair (j,k) dephases at
    gamma_tau * ((c_j - c_k) / (c_0 - c_1))^2, up to 49x for the
    S(+1/2)-D(-3/2) pair at d = 5.
    """
    if d > len(ZEEMAN_COEFF):
        raise ValueError(f"Zeeman encoding defined up to d={len(ZEEMAN_COEFF)}")
    c = np.asarray(ZEEMAN_COEFF[:d], dtype=float)
    J = np.sqrt(2.0 * gamma_tau) / abs(c[0] - c[1]) * np.diag(c)
    return expm(_dissipator(J))


NOISE_MODELS = ("transmon", "transmon_cal", "depolarizing", "ion_zeeman",
                "ion_mix")


def noise_superop(d: int, model: str, strength: float,
                  dephase_ratio: float = 1.0, **kw) -> np.ndarray:
    """Single-qudit noise channel for one time-layer, by model name."""
    if model == "transmon":
        return transmon_superop(d, strength, dephase_ratio)
    if model == "transmon_cal":
        return transmon_calibrated_superop(d, strength, dephase_ratio, **kw)
    if model == "depolarizing":
        return depolarizing_superop(d, strength)
    if model == "ion_zeeman":
        return ion_zeeman_superop(d, strength)
    if model == "ion_mix":
        # Flat depolarizing residual (strength) plus collective-B Zeeman
        # dephasing (zeeman_tau, i.e. the unmitigated rate times whatever
        # echo suppression the caller applies). The two commute (the
        # Zeeman channel is unital and diagonal), so the order is moot.
        return (depolarizing_superop(d, strength)
                @ ion_zeeman_superop(d, kw.get("zeeman_tau", 0.0)))
    raise ValueError(f"unknown noise model {model!r}")


def noise_superop_pow(d: int, model: str, strength: float, power: float = 1.0,
                      dephase_ratio: float = 1.0, **kw) -> np.ndarray:
    """The channel composed with itself `power` times, exactly, for real power.

    Both families form one-parameter semigroups, so fractional gate costs are
    exact rather than approximated:
      * Lindblad models (transmon, transmon_cal): E^t = exp(tL), i.e. simply
        scale the dimensionless rate by t;
      * depolarizing: E_p composed t times is E_q with 1-q = (1-p)^t.
    """
    if power == 1.0:
        return noise_superop(d, model, strength, dephase_ratio, **kw)
    if model == "depolarizing":
        return depolarizing_superop(d, 1.0 - (1.0 - strength) ** power)
    if model == "ion_mix":
        return (depolarizing_superop(d, 1.0 - (1.0 - strength) ** power)
                @ ion_zeeman_superop(d, kw.get("zeeman_tau", 0.0) * power))
    return noise_superop(d, model, strength * power, dephase_ratio, **kw)


# --- Gate cost models ------------------------------------------------------
# How many time-layers a gate occupies, as a function of the qudit dimension.
# The default ("uniform") charges every gate one layer regardless of d, which
# is the assumption most favourable to qudits. Two published cost structures
# charge more:
#
#   ion       Ringbauer 2022: a fully entangling two-qudit gate (Cinc) costs
#             2(d-1) Molmer-Sorensen gates on trapped ions -- linear in d.
#             Normalized to 1 layer at d=2, this is (d-1). Single-qudit laser
#             pulses stay cheap.
#   pavlidis  Pavlidis & Floratos 2017: QFT-domain arithmetic on qudits has
#             two-qudit-gate depth carrying an explicit d^2 factor (QFT depth
#             8 d^2 q, MAC depth 4 d^2 q). Normalized to 1 at d=2: d^2/4,
#             applied to two-qudit gates only -- the d^2 is the two-level
#             decomposition cost of the *controlled* rotations, so
#             single-qudit gates stay at one layer. The harshest of the
#             three.
#
# Transmon hardware sits nearer "uniform": Goss 2022's cross-Kerr CZ is a
# single fully entangling two-qutrit gate whose count does not grow with d.

GATE_COST_MODELS = {
    "uniform": (lambda d: 1.0, lambda d: 1.0),
    "ion": (lambda d: 1.0, lambda d: float(d - 1)),
    "pavlidis": (lambda d: 1.0, lambda d: d * d / 4.0),
}


def apply_cost_model(gates, d: int, cost_model: str = "uniform"):
    """Rescale each gate's time-layer cost according to a cost model."""
    if cost_model not in GATE_COST_MODELS:
        raise ValueError(f"unknown cost model {cost_model!r}")
    mult_1q, mult_2q = GATE_COST_MODELS[cost_model]
    m1, m2 = mult_1q(d), mult_2q(d)
    return [(sites, U, cost * (m1 if len(sites) == 1 else m2))
            for sites, U, cost in gates]


# ---------------------------------------------------------------------------
# Circuit construction
# ---------------------------------------------------------------------------
# A gate is a tuple (sites, U, cost) where cost is the number of serial
# time-layers the gate occupies in the toy scheduling model. Single-qudit and
# two-qudit gates cost 1 layer; a controlled modular multiplier costs w
# layers (the control must interact with each work qudit at least once).


def build_qft_gates(d: int, m: int):
    """No-swap QFT circuit on m qudits (output digit-reversed)."""
    gates = []
    for i in range(m):
        gates.append(((i,), fourier(d), 1))
        for j in range(i + 1, m):
            gates.append(((i, j), cphase(d, j - i + 1), 1))
    return gates


def shor_config(d: int, N: int = 15):
    """Register sizes for base d: control dim >= 64, work dim >= N."""
    m = 1
    while d ** m < 64:
        m += 1
    w = 1
    while d ** w < N:
        w += 1
    return m, w


def build_shor_gates(d: int, m: int, w: int, a: int, N: int):
    """Phase-estimation order-finding circuit on m control + w work qudits.

    Control qudit i is wired to the exponent d**i (little-endian on the
    controls) so that the no-swap inverse QFT returns outcomes in natural
    big-endian order without physical swaps.
    """
    gates = []
    for i in range(m):
        gates.append(((i,), fourier(d), 1))
    for i in range(m):
        mult = pow(a, d ** i, N)
        sites = (i,) + tuple(range(m, m + w))
        gates.append((sites, cmult_unitary(d, w, mult, N), w))
    for sites, U, cost in reversed(build_qft_gates(d, m)):
        gates.append((sites, U.conj().T, cost))
    return gates


# ---------------------------------------------------------------------------
# Classical post-processing (continued fractions)
# ---------------------------------------------------------------------------


def convergents(num: int, den: int):
    """Continued-fraction convergents (p, q) of num/den."""
    out = []
    a, b = num, den
    quots = []
    while b:
        quots.append(a // b)
        a, b = b, a - (a // b) * b
    p1, p0 = 1, 0
    q1, q0 = 0, 1
    for q in quots:
        p1, p0 = q * p1 + p0, p1
        q1, q0 = q * q1 + q0, q1
        out.append((p1, q1))
    return out


def multiplicative_order(a: int, N: int) -> int:
    r = 1
    x = a % N
    while x != 1:
        x = (x * a) % N
        r += 1
    return r


def recovered_order(y: int, D: int, a: int, N: int):
    """Order candidate extracted from measurement outcome y (or None)."""
    if y == 0:
        return None
    for _, q in convergents(y, D):
        if q > N:
            break
        if q >= 1 and pow(a, q, N) == 1:
            # minimize: the true order divides q
            for r in range(1, q + 1):
                if q % r == 0 and pow(a, r, N) == 1:
                    return r
    return None


# ---------------------------------------------------------------------------
# Simulation driver
# ---------------------------------------------------------------------------


def initial_state(dims: list[int], m: int, d: int, w: int) -> np.ndarray:
    """|0...0>_control (x) |x=1>_work as a density-matrix tensor."""
    Dtot = int(np.prod(dims))
    Dw = d ** w
    idx = 0 * Dw + 1  # control = 0, work = 1
    psi = np.zeros(Dtot)
    psi[idx] = 1.0
    rho = np.outer(psi, psi).astype(complex)
    return rho.reshape(dims + dims)


def run_circuit(dims: list[int], gates, rho: np.ndarray,
                E_by_cost: dict | None = None,
                E_gate_by_cost: dict | None = None) -> np.ndarray:
    """Apply gates in series; after each gate every qudit idles through the
    gate's time-layers under the matching noise superoperator.

    `E_by_cost` maps a gate's layer cost to the channel already raised to
    that power (see `channels_by_cost`). If `E_gate_by_cost` is given, the
    *participants* of a multi-qudit gate take that channel through the
    gate's layers instead -- gate-only noise inflation -- while spectators
    and single-qudit-gate layers keep `E_by_cost`.
    """
    for sites, U, cost in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if E_by_cost is not None:
            Ec = E_by_cost[cost]
            if E_gate_by_cost is not None and len(sites) >= 2:
                Eg = E_gate_by_cost[cost]
                for q in range(len(dims)):
                    rho = apply_channel(rho, Eg if q in sites else Ec, q,
                                        dims)
            else:
                for q in range(len(dims)):
                    rho = apply_channel(rho, Ec, q, dims)
    return rho


def channels_by_cost(d: int, gates, model: str, strength: float,
                     dephase_ratio: float = 1.0, **kw) -> dict:
    """Pre-raise the noise channel to every distinct gate cost in a circuit."""
    return {c: noise_superop_pow(d, model, strength, c, dephase_ratio, **kw)
            for c in {cost for _, _, cost in gates}}


def control_probs(rho: np.ndarray, d: int, m: int, w: int) -> np.ndarray:
    """Probability of each control-register outcome y in [0, d^m)."""
    Dc, Dw = d ** m, d ** w
    flat = rho.reshape(Dc * Dw, Dc * Dw)
    diag = np.real(np.diag(flat)).reshape(Dc, Dw)
    return diag.sum(axis=1)


READOUT_EXPONENT = 1.0    # misread rate of |k> grows as (1+k)^exponent
READOUT_DOWN = 0.7        # share of readout error that lands one level DOWN


def readout_confusion(d: int, eps: float, exponent: float = READOUT_EXPONENT,
                      down: float = READOUT_DOWN) -> np.ndarray:
    """Column-stochastic P(read k | prepared j) for one qudit.

    Dispersive readout gets harder for higher levels on every ladder
    platform we model: the pointer states crowd together as the
    transmon's anharmonicity compresses the spectrum, and a level has
    more time to decay during the measurement window the higher it sits.
    Both effects grow with k, so the misread rate of |j> is taken as
    eps * (1+j)^exponent -- roughly 1 : 2 : 3 for a qutrit at exponent 1,
    matching the ~1% / 2% / 4% readout errors reported for transmon
    qutrits (Blok 2021, Goss 2022).

    Errors go to adjacent levels only (a readout rarely mistakes |0> for
    |3>), split `down` / 1-`down` between k = j-1 and k = j+1 because
    decay during the window dominates. Edge levels send everything to
    their one neighbour.
    """
    C = np.zeros((d, d))
    for j in range(d):
        err = min(eps * (1.0 + j) ** exponent, 1.0)
        lo, hi = j - 1 >= 0, j + 1 < d
        if lo and hi:
            C[j - 1, j], C[j + 1, j] = err * down, err * (1.0 - down)
        elif lo:
            C[j - 1, j] = err
        elif hi:
            C[j + 1, j] = err
        else:
            err = 0.0          # d = 1 has nowhere to go
        C[j, j] = 1.0 - err
    return C


def apply_readout(probs: np.ndarray, d: int, m: int,
                  C: np.ndarray) -> np.ndarray:
    """Push an outcome distribution over Z_{d^m} through per-qudit readout.

    The joint confusion matrix is C^{\\otimes m}; applying it factor by
    factor costs O(m d^{m+1}) instead of building a d^m x d^m matrix.
    """
    out = probs.reshape((d,) * m)
    for axis in range(m):
        out = np.tensordot(C, out, axes=([1], [axis]))
        out = np.moveaxis(out, 0, axis)
    return out.reshape(-1)


def layer_count(gates) -> float:
    return sum(cost for _, _, cost in gates)


def shor_run(d: int, noise_model: str | None = None, strength: float = 0.0,
             a: int = 7, N: int = 15, dephase_ratio: float = 1.0,
             cost_model: str = "uniform", readout_eps: float = 0.0,
             gate_strength: float | None = None,
             **noise_kw) -> dict:
    """Run the full order-finding circuit and score it.

    Returns a dict with outcome probabilities, success probability (the
    probability that continued-fraction post-processing recovers the exact
    multiplicative order of a mod N), and resource counts.

    `gate_strength`, if given, is the strength the participants of a
    multi-qudit gate take through that gate's layers (gate-only noise
    inflation); everything else stays at `strength`.
    """
    m, w = shor_config(d, N)
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, a, N), d, cost_model)
    rho = initial_state(dims, m, d, w)

    E = Eg = None
    if noise_model and strength > 0:
        E = channels_by_cost(d, gates, noise_model, strength, dephase_ratio,
                             **noise_kw)
        if gate_strength is not None:
            Eg = channels_by_cost(d, gates, noise_model, gate_strength,
                                  dephase_ratio, **noise_kw)

    rho = run_circuit(dims, gates, rho, E, Eg)
    probs = control_probs(rho, d, m, w)
    if readout_eps > 0:
        probs = apply_readout(probs, d, m, readout_confusion(d, readout_eps))

    D = d ** m
    r_true = multiplicative_order(a, N)
    success = 0.0
    for y in range(D):
        if recovered_order(y, D, a, N) == r_true:
            success += probs[y]

    return {
        "d": d,
        "m": m,
        "w": w,
        "D": D,
        "n_qudits": m + w,
        "n_gates": len(gates),
        "n_layers": layer_count(gates),
        "cost_model": cost_model,
        "noise_model": noise_model,
        "strength": strength,
        "readout_eps": readout_eps,
        "probs": probs,
        "trace": float(np.real(np.trace(rho.reshape(D * d ** w, D * d ** w)))),
        "success": float(success),
        "r_true": r_true,
    }
