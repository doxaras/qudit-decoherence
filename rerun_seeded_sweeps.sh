#!/bin/sh
# Re-run every trajectory sweep whose seeds were process-salted.
#
# Until now these scripts seeded with hash((label, d, m)); Python salts
# str.__hash__ per process, so the seeds behind the published numbers
# could not be regenerated. They now seed with zlib.crc32 of the same
# tuple, matching scaling_fair_point.py. That makes the runs reproducible
# but also changes them: every point moves by roughly its own standard
# error, so every derived slope, R^2 and sigma has to be recomputed.
#
# The pre-change results are copied to results_prehash/ first, so the
# shift can be measured rather than assumed (see compare_prehash.py).
#
# Ordered cheapest-informative first, so a problem shows up early, and
# run strictly one at a time: each script already parallelises across
# 4-6 workers internally.
#
# Run: sh rerun_seeded_sweeps.sh   (expect ~5 h wall clock)
set -e
cd "$(dirname "$0")"

if [ ! -d results_prehash ]; then
  cp -R results results_prehash
  echo "backed up results/ -> results_prehash/"
fi

run() {
  echo ""
  echo "=== $* ==="
  date "+started %H:%M:%S"
  PYTHONUNBUFFERED=1 python3 "$@" 2>&1 | tail -25
  date "+finished %H:%M:%S"
}

run grid_alignment.py
run same_n_control.py
run composite_control.py
run interpolation_experiment.py
run d7_demo.py
run scaling_calibrated.py
run scaling_experiment.py
run qpe_scaling_experiment.py
run scaling_fair.py 400
run scaling_fair_m8.py 1000
run scaling_fair.py 1000
run qpe_hires.py 1000
run scaling_fair_n29.py 400
run ladder_exponent_sensitivity.py
run ladder_exponent_sensitivity.py traj

# derived from scaling_fair_1000, so it must follow it
run fidelity_collapse.py

echo ""
echo "=== all sweeps re-run; regenerating figures ==="
for p in plots.py plots_calibrated.py plots_fair.py plots_scaling.py \
         plots_scaling_fair.py plots_grid.py plots_mechanism.py; do
  [ -f "$p" ] && run "$p"
done
date "+ALL DONE %Y-%m-%d %H:%M:%S"
