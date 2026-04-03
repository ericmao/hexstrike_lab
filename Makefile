.PHONY: install test lint run assess-dry pipeline-dry clean

PYTHON ?= python3
PIP ?= pip

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	@echo "Add ruff/flake8 when ready"; true

run:
	$(PYTHON) -m hexstrike_lab run --target 127.0.0.1

assess-dry:
	$(PYTHON) -m hexstrike_lab assess --target 192.0.2.1 --profile quick --pretty

pipeline-dry:
	$(PYTHON) -m hexstrike_lab pipeline --target 192.0.2.1 --profile quick --output-base output

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	find . -type f -name "*.pyc" -delete 2>/dev/null; true
