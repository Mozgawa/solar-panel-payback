.DEFAULT_GOAL := help

.SILENT: clean-build clean-pyc clean-test

PYTHON=python310
PACKAGE_NAME=pysolar

help: @$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-inf' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
	rm -fr .ipynb_checkpoints
	rm -fr *.log
	rm -fr *.log.*
	rm -f test_result.xml

lint:
	pylint --exit-zero $(PACKAGE_NAME)
	radon cc $(PACKAGE_NAME) -a -nc
	radon cc tests -a -nc
	radon mi $(PACKAGE_NAME) -nc
	radon mi tests -nc
	mypy $(PACKAGE_NAME) --strict
	bandit $(PACKAGE_NAME)
	bandit tests

tests:
	pytest tests

cov:
	coverage run --source $(PACKAGE_NAME) -m pytest tests
	coverage report -m
	coverage html

pre-commit:
	pre-commit run --all-files

format:
	black $(PACKAGE_NAME)
	black tests
	isort --profile black $(PACKAGE_NAME)
	isort --profile black tests
	docformatter -r -i --wrap-summaries 100 --wrap-descriptions 90 $(PACKAGE_NAME)
	docformatter -r -i --wrap-summaries 100 --wrap-descriptions 90 tests
