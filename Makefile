.PHONY: test baseline analyze exp002 analyze-exp002 exp003 analyze-exp003 exp004 analyze-exp004 exp005 analyze-exp005 exp006 analyze-exp006 exp007 analyze-exp007 reproduce

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

baseline:
	PYTHONPATH=src python3 experiments/EXP001_baseline_association/run.py

analyze:
	PYTHONPATH=src python3 experiments/EXP001_baseline_association/analysis.py

exp002:
	PYTHONPATH=src python3 experiments/EXP002_perspective_matrices/run.py

analyze-exp002:
	PYTHONPATH=src python3 experiments/EXP002_perspective_matrices/analysis.py

exp003:
	PYTHONPATH=src python3 experiments/EXP003_adaptive_switching/run.py

analyze-exp003:
	PYTHONPATH=src python3 experiments/EXP003_adaptive_switching/analysis.py

exp004:
	PYTHONPATH=src python3 experiments/EXP004_dwell_regime/run.py

analyze-exp004:
	PYTHONPATH=src python3 experiments/EXP004_dwell_regime/analysis.py

exp005:
	PYTHONPATH=src python3 experiments/EXP005_evidence_timescale/run.py

analyze-exp005:
	PYTHONPATH=src python3 experiments/EXP005_evidence_timescale/analysis.py

exp006:
	PYTHONPATH=src python3 experiments/EXP006_topology_propagation_falsification/run.py

analyze-exp006:
	PYTHONPATH=src python3 experiments/EXP006_topology_propagation_falsification/analysis.py

exp007:
	PYTHONPATH=src python3 experiments/EXP007_self_timed_controller/run.py

analyze-exp007:
	PYTHONPATH=src python3 experiments/EXP007_self_timed_controller/analysis.py

reproduce: test baseline analyze exp002 analyze-exp002 exp003 analyze-exp003 exp004 analyze-exp004 exp005 analyze-exp005 exp006 analyze-exp006 exp007 analyze-exp007
