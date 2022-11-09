install:
	poetry install

update:
	poetry update

start:
	export PYTHONPATH=${PWD}/tracklift:${PYTHONPATH} && python tracklift/interfaces/cli.py

test:
	pytest tests/unit -v --cov-config pyproject.toml --cov
	coverage xml --fail-under 75

check-all: check-poetry check-lint check-mypy check-bandit check-private-keys check-format

check-poetry:
	poetry check

check-lint:
	poetry run flake8 .
	poetry run isort .

check-mypy:
	poetry run mypy --config-file pyproject.toml .

check-bandit:
	poetry run bandit -r -q . --exclude /tests,/venv

check-private-keys:
	poetry run detect-private-key

check-format:
	poetry run isort --check-only --diff .
	poetry run black --check --diff .

format:
	poetry run isort .
	poetry run black .
	poetry run end-of-file-fixer
	poetry run trailing-whitespace-fixer