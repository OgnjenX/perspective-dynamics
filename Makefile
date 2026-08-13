.PHONY: test baseline analyze exp002 analyze-exp002 exp003 analyze-exp003 reproduce

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

reproduce: test baseline analyze exp002 analyze-exp002 exp003 analyze-exp003
