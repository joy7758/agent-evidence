PYTHON ?= ./.venv/bin/python
PIP ?= ./.venv/bin/pip
PRE_COMMIT ?= ./.venv/bin/pre-commit
PYTEST ?= ./.venv/bin/pytest
RUFF ?= ./.venv/bin/ruff

.PHONY: install install-postgres test gate specimen test-postgres lint format hooks pre-commit clean

install:
	$(PIP) install -e ".[dev,langchain,sql]"

install-postgres:
	$(PIP) install -e ".[dev,postgres]"

test:
	$(PYTEST)

gate:
	$(PYTHON) scripts/run_profile_gate.py

specimen:
	$(PYTHON) scripts/run_specimen_gate.py

test-postgres:
	./scripts/run_postgres_integration.sh

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

hooks:
	$(PRE_COMMIT) install

pre-commit:
	$(PRE_COMMIT) run --all-files

clean:
	rm -rf .pytest_cache .ruff_cache build dist
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
