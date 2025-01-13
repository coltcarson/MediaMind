.PHONY: install test lint clean

install:
	python -m pip install -e .
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt
	pre-commit install

test:
	./venv/bin/pytest tests/ --cov=mediamind --cov-report=term-missing

lint:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".tox" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find ./transcripts -type f -name "test*.md" -delete

update-deps:
	pip-compile requirements.in
	pip-compile requirements-dev.in
