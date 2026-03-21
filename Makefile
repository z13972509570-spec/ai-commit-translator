.PHONY: install test lint clean build publish

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src

lint:
	ruff check src/ cli/ tests/
	black --check src/ cli/ tests/

format:
	black src/ cli/ tests/
	ruff check --fix src/ cli/ tests/

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:
	python -m build

publish: build
	python -m twine upload dist/*

run:
	ai-commit translate "新增用户登录功能"
