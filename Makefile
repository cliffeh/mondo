PIP=venv/bin/pip
PYTHON=venv/bin/python3
FLASK=venv/bin/flask

# linters
BLACK=venv/bin/black
ISORT=venv/bin/isort
MYPY=venv/bin/mypy

default: help

venv:  ## create a virtual environment and install dependencies
	@python3 -mvenv --upgrade-deps --prompt mondo venv
	@$(PIP) install -e .[dev]
.PHONY: venv

lint:  ## run all linters (black, isort, mypy)
	$(BLACK) mondo
	$(ISORT) mondo
	$(MYPY) mondo
.PHONY: lint

serve:  ## run a hot-reloading development server
	$(FLASK) --app mondo run --reload --debug
.PHONY: serve

build-clean:  ## clean up build directories
	@rm -rf build mondo.egg-info
.PHONY: build-clean

venv-clean:  ## delete the virtual environment
	@rm -rf venv
.PHONY: venv-clean

realclean: build-clean venv-clean ## clean up All the Things
.PHONY: realclean

help: ## show this help
	@echo "\nSpecify a command. The choices are:\n"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
