.PHONY: test baseline analyze reproduce

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

baseline:
	PYTHONPATH=src python3 experiments/EXP001_baseline_association/run.py

analyze:
	PYTHONPATH=src python3 experiments/EXP001_baseline_association/analysis.py

reproduce: test baseline analyze
