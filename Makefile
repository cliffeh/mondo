PIP=venv/bin/pip
PYTHON=venv/bin/python3
FLASK=venv/bin/flask

# linters
BLACK=venv/bin/black
ISORT=venv/bin/isort
MYPY=venv/bin/mypy

default: help

venv $(FLASK):  ## create a virtual environment and install dependencies
	@python3 -mvenv --upgrade-deps --prompt mondo venv
	@$(PIP) install -e .[dev]
.PHONY: venv

lint:  ## run all linters (black, isort, mypy)
	@$(BLACK) src
	@$(ISORT) src
	@$(MYPY) src
.PHONY: lint

serve: $(FLASK)  ## run a hot-reloading development server
	@$(FLASK) --app mondo run --host :: --port 2505 --reload --debug
.PHONY: serve

instance-clean: ## clean up the instance directory
	@rm -rf instance
.PHONY: instance-clean

build-clean:  ## clean up build directories
	@rm -rf build src/mondo.egg-info src/mondo/__pycache__
.PHONY: build-clean

venv-clean:  ## delete the virtual environment
	@rm -rf venv
.PHONY: venv-clean

realclean: build-clean instance-clean venv-clean ## clean up All the Things
.PHONY: realclean

help: ## show this help
	@echo "\nSpecify a command. The choices are:\n"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
