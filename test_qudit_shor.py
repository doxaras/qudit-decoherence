"""Self-contained correctness tests for qudit_shor. Run: python3 test_qudit_shor.py"""

import numpy as np

from qudit_shor import (
    build_qft_gates, build_shor_gates, cmult_unitary, dephasing_matrix,
    dephasing_residual, depolarizing_superop, kraus_from_superop,
    multiplicative_order, noise_superop, qft_matrix, recovered_order,
    reverse_digits, shor_config, shor_run, transmon_calibrated_superop,
    transmon_superop,
)


def _channel_rates(E, d, g):
    """Population decay rates and pure-dephasing rates realized by E."""
    pop = {}
    for k in range(1, d):
        rho = np.zeros((d, d), complex)
        rho[k, k] = 1.0
        pop[k] = -np.log(np.real((E @ rho.reshape(-1)).reshape(d, d)[k, k])) / g
    deph = {}
    for j in range(d):
        for k in range(j + 1, d):
            rho = np.zeros((d, d), complex)
            rho[j, k] = 1.0
            tot = -np.log(abs((E @ rho.reshape(-1)).reshape(d, d)[j, k])) / g
            deph[(j, k)] = tot - 0.5 * (pop.get(j, 0.0) + pop.get(k, 0.0))
    return pop, deph


def compose(gates, dims):
    """Dense unitary of a gate sequence (test helper)."""
    Dtot = int(np.prod(dims))
    t = np.eye(Dtot).reshape(dims + [Dtot])
    for sites, U, _ in gates:
        k = len(sites)
        ds = [dims[s] for s in sites]
        Ut = U.reshape(ds + ds)
        t = np.tensordot(Ut, t, axes=(list(range(k, 2 * k)), list(sites)))
        t = np.moveaxis(t, list(range(k)), list(sites))
    return t.reshape(Dtot, Dtot)


def test_qft_circuit():
    """No-swap QFT circuit equals digit-reversal x dense QFT."""
    for d, m in [(2, 3), (3, 3), (5, 2)]:
        D = d ** m
        Uc = compose(build_qft_gates(d, m), [d] * m)
        P = np.zeros((D, D))
        for x in range(D):
            P[reverse_digits(x, d, m), x] = 1.0
        assert np.allclose(Uc, P @ qft_matrix(D), atol=1e-10), (d, m)


def test_cmult_unitary():
    for d, w in [(2, 4), (3, 3), (5, 2)]:
        U = cmult_unitary(d, w, 7, 15)
        assert np.allclose(U @ U.T, np.eye(U.shape[0])), (d, w)


def test_channels_cptp():
    rng = np.random.default_rng(0)
    for d in (2, 3, 5):
        for E in (transmon_superop(d, 0.03), depolarizing_superop(d, 0.05)):
            # trace preservation on a random state
            A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            rho = A @ A.conj().T
            rho /= np.trace(rho)
            out = (E @ rho.reshape(-1)).reshape(d, d)
            assert abs(np.trace(out) - 1) < 1e-10, d
            # complete positivity via the Choi matrix
            choi = np.zeros((d * d, d * d), complex)
            for i in range(d):
                for j in range(d):
                    eij = np.zeros((d, d))
                    eij[i, j] = 1.0
                    out_ij = (E @ eij.reshape(-1)).reshape(d, d)
                    choi += np.kron(out_ij, eij)
            evals = np.linalg.eigvalsh((choi + choi.conj().T) / 2)
            assert evals.min() > -1e-10, d


def test_depolarizing_fixed_point():
    for d in (2, 3, 5):
        E = depolarizing_superop(d, 0.3)
        mm = np.eye(d).reshape(-1) / d
        assert np.allclose(E @ mm, mm)


def test_postprocessing():
    assert multiplicative_order(7, 15) == 4
    assert recovered_order(0, 64, 7, 15) is None
    assert recovered_order(16, 64, 7, 15) == 4   # 16/64 = 1/4
    assert recovered_order(48, 64, 7, 15) == 4   # 48/64 = 3/4
    assert recovered_order(32, 64, 7, 15) is None  # 1/2 -> q=2, but 7^2 = 4 != 1
    assert recovered_order(31, 125, 7, 15) == 4  # 31/125 ~ 1/4


def test_noiseless_baselines():
    for d, lo in [(2, 0.499999), (3, 0.45), (5, 0.45)]:
        res = shor_run(d)
        assert abs(res["trace"] - 1) < 1e-8, d
        assert res["success"] > lo, (d, res["success"])
    assert abs(shor_run(2)["success"] - 0.5) < 1e-9


def test_noise_degrades():
    for d in (2, 3):
        base = shor_run(d)["success"]
        for model in ("transmon", "depolarizing"):
            noisy = shor_run(d, model, 0.02)
            assert abs(noisy["trace"] - 1) < 1e-6
            assert noisy["success"] < base, (d, model)


def test_register_sizing():
    assert shor_config(2) == (6, 4)
    assert shor_config(3) == (4, 3)
    assert shor_config(5) == (3, 2)


def test_kraus_from_superop():
    """Kraus decomposition is complete and reproduces the channel."""
    rng = np.random.default_rng(3)
    for d in (2, 3, 5):
        for E in (transmon_superop(d, 0.02), depolarizing_superop(d, 0.03)):
            ks = kraus_from_superop(E)
            comp = sum(K.conj().T @ K for K in ks)
            assert np.allclose(comp, np.eye(d), atol=1e-9), d
            A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            rho = A @ A.conj().T
            rho /= np.trace(rho)
            exact = (E @ rho.reshape(-1)).reshape(d, d)
            via = sum(K @ rho @ K.conj().T for K in ks)
            assert np.allclose(exact, via, atol=1e-9), d


def test_trajectories_match_exact():
    """Monte Carlo engine agrees with the density-matrix simulator."""
    from trajectories import shor_trajectories

    # noiseless: single pure-state run must be exact
    assert abs(shor_trajectories(3, 4)["success"]
               - shor_run(3)["success"]) < 1e-9
    # noisy: statistical agreement (stderr ~ 0.01 at 150 trajectories)
    exact = shor_run(3, "depolarizing", 0.01)["success"]
    mc = shor_trajectories(3, 4, "depolarizing", 0.01, n_traj=150, seed=0)
    assert abs(mc["success"] - exact) < max(4 * mc["stderr"], 0.04), (
        mc["success"], exact)


def test_calibrated_transmon_channel():
    """Calibrated channel is realizable, CPTP, and matches measured ratios."""
    g = 0.01
    # the max-level dephasing law must be an exact Euclidean embedding
    for d in (2, 3, 4, 5, 7):
        assert dephasing_residual(dephasing_matrix(d, g)) < 1e-12, d
    # d=2 must be bit-for-bit identical to the idealized model, so that any
    # difference between the two models is purely a higher-level effect
    assert np.allclose(transmon_calibrated_superop(2, g),
                       transmon_superop(2, g), atol=1e-14)
    # measured targets: T1 ladder ratio ~1.7, dephasing 1 : 2.0 : 2.3
    pop, deph = _channel_rates(transmon_calibrated_superop(3, g), 3, g)
    assert 1.5 < pop[2] / pop[1] < 1.9, pop[2] / pop[1]
    base = deph[(0, 1)]
    assert 1.8 < deph[(1, 2)] / base < 2.4, deph[(1, 2)] / base
    assert 1.8 < deph[(0, 2)] / base < 2.5, deph[(0, 2)] / base
    # the idealized model, for contrast, gives 2.0 and 1 : 1 : 4
    pop_i, deph_i = _channel_rates(transmon_superop(3, g), 3, g)
    assert abs(pop_i[2] / pop_i[1] - 2.0) < 0.05
    assert abs(deph_i[(0, 2)] / deph_i[(0, 1)] - 4.0) < 0.05
    # dephase_ratio=0 leaves the relaxation ladder untouched (high-E_J/E_C)
    pop0, deph0 = _channel_rates(
        transmon_calibrated_superop(5, g, dephase_ratio=0.0), 5, g)
    assert max(abs(v) for v in deph0.values()) < 1e-9
    assert abs(pop0[4] - 4 ** 0.7) < 0.05
    # CPTP
    rng = np.random.default_rng(5)
    for d in (2, 3, 5):
        E = noise_superop(d, "transmon_cal", 0.03)
        A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        rho = A @ A.conj().T
        rho /= np.trace(rho)
        assert abs(np.trace((E @ rho.reshape(-1)).reshape(d, d)) - 1) < 1e-10
        choi = np.zeros((d * d, d * d), complex)
        for i in range(d):
            for j in range(d):
                eij = np.zeros((d, d))
                eij[i, j] = 1.0
                choi += np.kron((E @ eij.reshape(-1)).reshape(d, d), eij)
        assert np.linalg.eigvalsh((choi + choi.conj().T) / 2).min() > -1e-10, d


def test_calibrated_is_gentler_on_qudits():
    """Calibration must relax the qudit penalty relative to the ideal model."""
    for d in (3, 5):
        ideal = shor_run(d, "transmon", 0.01)["success"]
        cal = shor_run(d, "transmon_cal", 0.01)["success"]
        assert cal > ideal, (d, cal, ideal)
    # ...and leave the qubit case untouched
    assert abs(shor_run(2, "transmon_cal", 0.01)["success"]
               - shor_run(2, "transmon", 0.01)["success"]) < 1e-12


def test_noise_superop_pow_exact():
    """Fractional/integer channel powers compose exactly (semigroup property)."""
    from qudit_shor import noise_superop, noise_superop_pow
    for model in ("transmon", "transmon_cal", "depolarizing"):
        for d in (2, 3, 5):
            E = noise_superop(d, model, 0.01)
            for n in (2, 3, 4):
                assert np.allclose(noise_superop_pow(d, model, 0.01, float(n)),
                                   np.linalg.matrix_power(E, n), atol=1e-12), (
                    model, d, n)
            # a half-step composed with itself reproduces one full step
            half = noise_superop_pow(d, model, 0.01, 0.5)
            assert np.allclose(half @ half, E, atol=1e-12), (model, d)


def test_gate_cost_models():
    """Cost models scale circuit depth as published, and hurt bigger d more."""
    from qudit_shor import (apply_cost_model, build_shor_gates, layer_count,
                            shor_config)
    layers = {}
    for cm in ("uniform", "ion", "pavlidis"):
        for d in (2, 3, 5):
            m, w = shor_config(d)
            g = apply_cost_model(build_shor_gates(d, m, w, 7, 15), d, cm)
            layers[(cm, d)] = layer_count(g)
    # d=2 is the normalization point: every model agrees there
    assert layers[("uniform", 2)] == layers[("ion", 2)] == layers[("pavlidis", 2)]
    # uniform: qudits compress; pavlidis: qudits cost more than qubits
    assert layers[("uniform", 5)] < layers[("uniform", 2)]
    assert layers[("pavlidis", 5)] > layers[("pavlidis", 2)]
    # monotone in cost model for every d > 2
    for d in (3, 5):
        assert (layers[("uniform", d)] < layers[("ion", d)]
                < layers[("pavlidis", d)]), d
    # more layers must mean less signal
    prev = 1.0
    for cm in ("uniform", "ion", "pavlidis"):
        s = shor_run(5, "transmon_cal", 0.005, cost_model=cm)["success"]
        assert s < prev, cm
        prev = s


def test_qpe_generic():
    """Generic phase estimation: correct phase, sane floors, MC agreement."""
    from qpe_generic import (PHI_TARGET, qpe_run_exact, qpe_trajectories)

    for d, m in [(2, 6), (3, 4), (5, 3)]:
        r = qpe_run_exact(d, m)
        D = d ** m
        # the peak outcome must be the grid point nearest the target phase
        peak = int(np.argmax(r["probs"]))
        dist = abs(peak / D - PHI_TARGET)
        assert min(dist, 1 - dist) <= 1.0 / D, (d, m, peak)
        assert r["success"] > 0.8, (d, m, r["success"])
        assert 0.02 < r["floor"] < 0.05, (d, m, r["floor"])
        # noiseless trajectory run is the same pure-state simulation
        assert abs(qpe_trajectories(d, m)["success"] - r["success"]) < 1e-9
    # noisy: statistical agreement with the exact simulator
    exact = qpe_run_exact(3, 4, "depolarizing", 0.01)["success"]
    mc = qpe_trajectories(3, 4, "depolarizing", 0.01, n_traj=150, seed=0)
    assert abs(mc["success"] - exact) < max(4 * mc["stderr"], 0.04), (
        mc["success"], exact)


def test_grover():
    """Grover on qudit registers: correctness and fair cost accounting."""
    from grover import (grover_gates, grover_run, optimal_iterations,
                        _marked_sample)

    # the textbook iteration count, and near-certain noiseless success
    assert optimal_iterations(64) == 6, optimal_iterations(64)
    for d, n in ((2, 6), (3, 4), (5, 3)):
        r = grover_run(d, n, n_marked=3)
        assert r["success"] > 0.97, (d, n, r["success"])
        assert abs(r["floor"] - 1.0 / d ** n) < 1e-15, (d, n)
        # noise can only hurt
        noisy = grover_run(d, n, "depolarizing", 0.01, n_marked=3)
        assert noisy["success"] < r["success"], (d, n)

    # the all-zero state is never used as a marked item (it is the
    # diffuser's reflection axis and the bottom of the damping ladder)
    assert 0 not in _marked_sample(64, 8, 7)

    # multi-qudit gates are charged their decomposition depth, not 1 layer.
    # Otherwise the base with the MOST carriers gets the biggest free ride.
    for d, n in ((2, 6), (5, 3)):
        gates = grover_gates(d, n, marked=1, iterations=1)
        multi = [g for g in gates if len(g[0]) > 1]
        assert len(multi) == 2, (d, n)            # oracle + reflection
        for sites, U, cost in multi:
            assert cost == n - 1, (d, n, cost)
            assert U.shape == (d ** n, d ** n)
            assert np.allclose(U.conj().T @ U, np.eye(d ** n)), (d, n)

    # a qudit register must be cheaper in total exposure than a qubit one
    # at comparable problem size -- this is the effect under study
    e2 = 6 * grover_run(2, 6, n_marked=1)["n_layers"]
    e5 = 3 * grover_run(5, 3, n_marked=1)["n_layers"]
    assert e5 < e2 / 2, (e2, e5)


def test_fidelity_estimator():
    """Trajectory fidelity estimate agrees with the exact density matrix.

    fidelity_collapse.py estimates end-state fidelity <psi|rho|psi> by
    averaging |<psi_ideal|psi_traj>|^2 over Monte Carlo trajectories.
    That estimator is unbiased because averaging |psi><psi| over
    trajectories reproduces rho exactly -- verified here against a full
    density-matrix evolution of the same small Shor instance.
    """
    from fidelity_collapse import shor_fidelity
    from qudit_shor import (apply_channel, apply_unitary, apply_unitary_vec,
                            build_shor_gates, channels_by_cost, shor_config)

    d, m, model, s = 3, 3, "transmon_cal", 0.01
    _, w = shor_config(d, 21)
    dims = [d] * (m + w)
    D = d ** (m + w)
    gates = build_shor_gates(d, m, w, 2, 21)     # uniform cost, as the study
    E = channels_by_cost(d, gates, model, s, 1.0)

    psi = np.zeros(D, complex)
    psi[1] = 1.0                                 # control |0..0>, work |x=1>
    psi = psi.reshape(dims)
    rho = np.zeros((D, D), complex)
    rho[1, 1] = 1.0
    rho = rho.reshape(dims + dims)
    for sites, U, cost in gates:
        psi = apply_unitary_vec(psi, U, sites, dims)
        rho = apply_unitary(rho, U, sites, dims)
        for q in range(len(dims)):
            rho = apply_channel(rho, E[cost], q, dims)
    v = psi.reshape(-1)
    f_exact = float(np.real(v.conj() @ rho.reshape(D, D) @ v))

    r = shor_fidelity(d, m, model, s, n_traj=300, seed=11)
    err = abs(r["fidelity"] - f_exact)
    tol = max(4 * r["stderr"], 0.01)
    assert err < tol, (r["fidelity"], f_exact, r["stderr"])
    # and the fidelity is in a regime where the test has teeth
    assert 0.05 < f_exact < 0.95, f_exact


def test_readout_channel():
    """d-dependent SPAM: confusion matrix and its action on outcomes."""
    from qudit_shor import apply_readout, readout_confusion

    for d in (2, 3, 5):
        C = readout_confusion(d, 0.01)
        # a probability distribution in, a probability distribution out
        assert np.allclose(C.sum(axis=0), 1.0), d
        assert (C >= 0).all(), d
        # misread rate of |k> grows as (1+k): 1%, 2%, ... k+1 %
        assert np.allclose(1.0 - np.diag(C),
                           0.01 * (1.0 + np.arange(d))), d
        # errors only reach adjacent levels
        for j in range(d):
            for k in range(d):
                if abs(j - k) > 1:
                    assert C[k, j] == 0.0, (d, j, k)
        # eps = 0 is the identity, and total probability is conserved
        assert np.allclose(readout_confusion(d, 0.0), np.eye(d)), d
        m = 2
        p = np.abs(np.random.default_rng(0).normal(size=d ** m))
        p /= p.sum()
        q = apply_readout(p, d, m, C)
        assert abs(q.sum() - 1.0) < 1e-12, d
        assert np.allclose(apply_readout(p, d, m, np.eye(d)), p), d

    # readout error can only hurt: success must not increase with eps
    prev = None
    for eps in (0.0, 0.01, 0.03):
        s = shor_run(3, "depolarizing", 0.005, a=2, N=21,
                     readout_eps=eps)["success"]
        if prev is not None:
            assert s <= prev + 1e-12, (eps, s, prev)
        prev = s


def test_grid_alignment():
    """Pin the confound that overturned the Shor result (docs/GRID_ALIGNMENT.md).

    Exact grid alignment means r | D = d^m; residual misalignment is the mean
    distance of the r-1 target phases s/r from the nearest grid point.
    """
    def aligned(d, a, N):
        m, _ = shor_config(d, N)
        return (d ** m) % multiplicative_order(a, N) == 0

    def residual(d, a, N):
        m, _ = shor_config(d, N)
        D, r = d ** m, multiplicative_order(a, N)
        x = D * np.arange(1, r) / r
        return float(np.abs(x - np.round(x)).mean())

    # N = 15 admits only power-of-two orders -> base 2 is always aligned,
    # bases 3 and 5 never are. This is what biased the original study.
    for a in (2, 4, 7, 8, 11, 13, 14):
        assert aligned(2, a, 15), a
        assert not aligned(3, a, 15) and not aligned(5, a, 15), a

    # one instance per alignment class
    for a, N, base in [(4, 21, 3), (7, 15, 2), (4, 33, 5)]:
        for d in (2, 3, 5):
            assert aligned(d, a, N) == (d == base), (d, a, N)
            assert (residual(d, a, N) == 0.0) == (d == base), (d, a, N)

    # the two unbiased instances: nobody is aligned...
    for a, N in [(2, 21), (16, 29)]:
        assert not any(aligned(d, a, N) for d in (2, 3, 5)), (a, N)
    # ...and on N = 29 (r = 7) the residual is exactly tied across bases,
    # which is why it carries the headline.
    res29 = [residual(d, 16, 29) for d in (2, 3, 5)]
    assert max(res29) - min(res29) < 1e-12, res29
    # on N = 21 (r = 6) the residual mildly favours the QUBIT, so the
    # measured qudit win there cannot be a leftover alignment effect.
    assert residual(2, 2, 21) < min(residual(3, 2, 21), residual(5, 2, 21))


def test_unbiased_instance_ordering():
    """On the unbiased instance, qudits beat qubits under both noise models.

    Exact density matrices, the same demo point as docs/GRID_ALIGNMENT.md §4.
    """
    span = {}
    for d in (2, 3, 5):
        m, _ = shor_config(d, 21)
        D = d ** m
        floor = sum(recovered_order(y, D, 2, 21) == 6 for y in range(D)) / D
        span[d] = (floor, shor_run(d, a=2, N=21)["success"] - floor)

    def signal(d, model, s):
        floor, width = span[d]
        return (shor_run(d, model, s, a=2, N=21)["success"] - floor) / width

    for model in ("transmon_cal", "depolarizing"):
        sig = {d: signal(d, model, 0.005) for d in (2, 3, 5)}
        assert sig[5] > sig[3] > sig[2], (model, sig)
        assert sig[5] - sig[2] > 0.25, (model, sig)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
