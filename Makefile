.PHONY: help setup docs docs-serve check test

help:
	@echo "setup       install documentation tooling"
	@echo "docs        build the documentation site"
	@echo "docs-serve  serve docs locally at :8000"
	@echo "check       validate doc links and ADR index coverage"
	@echo "test        run unit tests (placeholder until the kinematics library lands)"

setup:
	python3 -m pip install --upgrade mkdocs mkdocs-material

docs:
	mkdocs build --strict

docs-serve:
	mkdocs serve

check:
	python3 scripts/check_docs.py

test:
	@echo "No unit tests yet. KIN-001 lands with the kinematics library."
