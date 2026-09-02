# Reproduction pipeline for the paper, top to bottom.
# docs/PAPER.md §5 is the annotated version of this sequence.
# Long targets are marked; `make core` skips them.

PY ?= python3
R := results

.PHONY: all core tests figures paper \
        alignment cost scaling decoder robustness hardware anchors

all: tests core scaling_long paper

core: tests alignment cost scaling decoder robustness anchors figures

tests:
	$(PY) test_qudit_shor.py            # 20 tests, ~3.5 min

# --- Sec. III: grid alignment --------------------------------------
alignment: $(R)/grid_alignment.json $(R)/same_n_control.json \
           $(R)/ensemble_a_n33.json $(R)/misalignment_scaling.json \
           $(R)/fair_demo.json

$(R)/grid_alignment.json:        ; $(PY) grid_alignment.py      # ~8 min
$(R)/same_n_control.json:        ; $(PY) same_n_control.py      # ~7 min
$(R)/ensemble_a_n33.json:        ; $(PY) ensemble_a_traj.py 33  # also: 21, 55
$(R)/misalignment_scaling.json:  ; $(PY) misalignment_scaling.py
$(R)/fair_demo.json:             ; $(PY) fair_demo.py           # ~4 min

# --- Sec. IV: the cost condition ------------------------------------
cost: $(R)/cost_fair.json $(R)/d7_demo.json $(R)/matched_D.json \
      $(R)/d11_demo.json $(R)/d7_matched_D.json

$(R)/cost_fair.json:     ; $(PY) cost_fair.py       # ~12 min
$(R)/d7_demo.json:       ; $(PY) d7_demo.py
$(R)/d11_demo.json:      ; $(PY) d11_demo.py
$(R)/matched_D.json:     ; $(PY) matched_D.py
$(R)/d7_matched_D.json:  ; $(PY) d7_matched_D.py

# --- Sec. V: scaling (long) ------------------------------------------
scaling: $(R)/scaling_fair.json $(R)/scaling_fair_n29.json

scaling_long: scaling $(R)/scaling_fair_d3_m9.json $(R)/qpe_hires_1000.json

$(R)/scaling_fair.json:          ; $(PY) scaling_fair.py        # ~1 h
$(R)/scaling_fair_d3_m9.json:    ; $(PY) scaling_fair_point.py  # deep points
$(R)/scaling_fair_n29.json:      ; $(PY) scaling_fair_n29.py
$(R)/qpe_hires_1000.json:        ; $(PY) qpe_hires.py

# --- Sec. VI-VII: Grover, mechanism, decoder --------------------------
decoder: $(R)/grover.json $(R)/grover_cost.json \
         $(R)/exposure_collapse.json $(R)/fidelity_collapse.json \
         $(R)/logfid_rescore.json $(R)/decoder_formula.json \
         $(R)/decoder_scaling.json $(R)/collapse_tail_deep.json \
         $(R)/favg_rescore.json $(R)/interpolation_slopes.json \
         $(R)/crossing_bootstrap.json

$(R)/grover.json:             ; $(PY) grover_study.py
$(R)/grover_cost.json:        ; $(PY) grover_cost.py
$(R)/exposure_collapse.json:  ; $(PY) exposure_collapse.py
$(R)/fidelity_collapse.json:  ; $(PY) fidelity_collapse.py
$(R)/logfid_rescore.json:     ; $(PY) logfid_rescore.py
$(R)/decoder_formula.json:    ; $(PY) decoder_formula.py   # seconds
$(R)/decoder_scaling.json:    ; $(PY) decoder_scaling.py   # seconds
$(R)/crossing_bootstrap.json: ; $(PY) crossing_bootstrap.py # seconds
$(R)/collapse_tail_deep.json: ; $(PY) collapse_tail_deep.py
$(R)/favg_rescore.json:       ; $(PY) favg_rescore.py
$(R)/interpolation_slopes.json: ; $(PY) interpolation_slopes.py

# --- Sec. VIII: robustness ---------------------------------------------
robustness: $(R)/spam.json $(R)/dd.json $(R)/noise_inflation.json \
            $(R)/collective_zeeman.json $(R)/ion_zeeman_echo.json \
            $(R)/d4_control.json $(R)/composite_control.json \
            $(R)/jankovic.json $(R)/hrmo_reanalysis.json \
            $(R)/transmon_rebuild.json $(R)/ion_2d_fstar.json \
            $(R)/hrmo_d4.json $(R)/dephase_ratio_sweep.json \
            $(R)/ladder_quasistatic.json $(R)/ladder_thermal.json \
            $(R)/ion_zeeman_quasistatic.json

$(R)/spam.json:               ; $(PY) spam_study.py
$(R)/dd.json:                 ; $(PY) dd_study.py
$(R)/noise_inflation.json:    ; $(PY) noise_inflation.py
$(R)/collective_zeeman.json:  ; $(PY) collective_zeeman.py
$(R)/ion_zeeman_echo.json:    ; $(PY) ion_zeeman_echo.py
$(R)/ion_zeeman_quasistatic.json: ; $(PY) ion_zeeman_quasistatic.py
$(R)/d4_control.json:         ; $(PY) d4_control.py
$(R)/composite_control.json:  ; $(PY) composite_control.py
$(R)/jankovic.json:           ; $(PY) jankovic_check.py
$(R)/hrmo_reanalysis.json:    ; $(PY) hrmo_reanalysis.py
$(R)/transmon_rebuild.json:   ; $(PY) transmon_rebuild.py
$(R)/ion_2d_fstar.json:       ; $(PY) ion_2d_fstar.py
$(R)/hrmo_d4.json:            ; $(PY) hrmo_d4.py
$(R)/dephase_ratio_sweep.json: ; $(PY) dephase_ratio_sweep.py
$(R)/ladder_quasistatic.json: ; $(PY) ladder_quasistatic.py
$(R)/ladder_thermal.json:     ; $(PY) ladder_thermal.py

# --- Sec. IX-X: hardware analysis + predictions (free; re-submission
#     to AWS Braket costs money and is NOT a target) -------------------
anchors: $(R)/braket_raw_analysis.json $(R)/qpe_measured_strengths.json \
         $(R)/qpe_d3_measured.json $(R)/garnet_routed.json

$(R)/braket_raw_analysis.json:  ; $(PY) braket_raw_analysis.py   # free
$(R)/qpe_measured_strengths.json: ; $(PY) qpe_measured_strengths.py
$(R)/qpe_d3_measured.json:      ; $(PY) qpe_d3_measured.py
$(R)/garnet_routed.json:        ; $(PY) garnet_routed.py

hardware:
	@echo "braket_qpe_anchor.py re-submits to AWS and costs money; \
	       the committed results/braket_raw_counts.json lets 'make anchors' \
	       reproduce every hardware number for free."

# --- figures + paper ---------------------------------------------------
figures: alignment cost scaling decoder
	$(PY) plots_grid.py && $(PY) plots_fair.py && \
	$(PY) plots_scaling_fair.py && $(PY) plots_grover.py && \
	$(PY) plots_mechanism.py

paper:
	cd paper && latexmk -pdf main.tex
