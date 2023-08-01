VENV := venv
PYTHON := ./$(VENV)/Scripts/python
PIP := ./$(VENV)/Scripts/pip

$(VENV)/Scripts/activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

venv: $(VENV)/Scripts/activate

.PHONY: venv