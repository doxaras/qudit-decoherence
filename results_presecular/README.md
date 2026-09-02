# Retired pre-secular artifacts

`scaling_fair_1000.json` (Aug 15) — a higher-statistics variant of the
main scaling sweep, written by `trajectory_variance.py`. It predates the
secular relaxation change and, because `_scaling_fair_path()` in
`exposure_collapse.py` prefers it over `scaling_fair.json` when present,
it silently shadowed the regenerated sweep in eight consumer scripts.
Moved here on 2026-08-31 so the fallback picks up the fresh file.

To regenerate it under the secular channel, re-run
`trajectory_variance.py` (expensive: 24 replicas per point) and move the
output back; until then the consumers use `results/scaling_fair.json`
(1000 trajectories, secular).
