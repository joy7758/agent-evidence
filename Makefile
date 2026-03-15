PYTHON ?= ./.venv/bin/python
PIP ?= ./.venv/bin/pip
PRE_COMMIT ?= ./.venv/bin/pre-commit
PYTEST ?= ./.venv/bin/pytest
RUFF ?= ./.venv/bin/ruff

.PHONY: install test lint format hooks pre-commit clean

install:
	$(PIP) install -e ".[dev,langchain,sql]"

test:
	$(PYTEST)

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
