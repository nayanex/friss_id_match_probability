ENV_NAME=friss-env
BIN=$(ENV_NAME)/bin/
PYTHON=$(BIN)/python
BASE_REQUIREMENTS=requirements/requirements-base.in
DEV_REQUIREMENTS=requirements/requirements-dev.in

create_environment:
	make clean
	$(PYTHON) -m venv $(ENV_NAME)

clean:
	rm -rf $(ENV_NAME)
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf flask_session/
	rm -f .coverage
	rm -rf tests/.pytest_cache
	rm -rf htmlcov

install_requirements:
	$(BIN)pip install -r $(BASE_REQUIREMENTS)

install_dev_requirements: install_requirements
	$(BIN)pip install -r $(BASE_REQUIREMENTS)
	$(BIN)pip install -r $(DEV_REQUIREMENTS)

# Run unittests and generate html coverage report
test:
	coverage run -m pytest tests
	coverage html

# Run linters check only
lint:
	$(BIN)isort . --skip $(ENV_NAME) --check
	$(BIN)black . --exclude=$(ENV_NAME) --check

# Run linters and try to fix the errors
format:
	$(BIN)isort . --skip $(ENV_NAME)
	$(BIN)black . --exclude=$(ENV_NAME)

# Update all libraries required to run this application
requirements_txt:
	sort -u $(BASE_REQUIREMENTS) -o $(BASE_REQUIREMENTS)
	pip-compile --output-file=requirements.txt $(BASE_REQUIREMENTS)

requirements_dev_txt:
	sort -u $(DEV_REQUIREMENTS) -o $(DEV_REQUIREMENTS)
	sort -u $(BASE_REQUIREMENTS) -o $(BASE_REQUIREMENTS)
	pip-compile --output-file=requirements.txt $(BASE_REQUIREMENTS) $(DEV_REQUIREMENTS)

# Re/install the virtual environment with all requirements
install:
	make install_requirements

# Re/install the virtual environment for DEV usage
dev_install:
	make install_dev_requirements

# Do all checks.
build:
	make dev_install
	make lint
	make test