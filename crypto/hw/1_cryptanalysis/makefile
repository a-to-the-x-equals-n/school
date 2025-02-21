# vars
PY = python3
JP = jupyter
VE = venv
BINARY = $(VE)/bin/python

# setup virtual env 
start:
	$(PY) -m venv $(VE)

# dependencies from requirements.txt
reqs: start
	$(BINARY) -m pip install -r requirements.txt

# open in notebook if you choose
notebook: reqs
	$(BINARY) -m $(JP) notebook

# clean up
end:
	rm -rf $(VE) __pycache__ .pytest_cache .ipynb_checkpoints
