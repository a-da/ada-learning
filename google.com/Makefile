# see https://makefiletutorial.com/

SHELL := /bin/bash -eu -o pipefail
PYTHON_3 ?= python3
PYTHON_D ?= /opt/python.d

VENV_PATH_DEV := $(PYTHON_D)/dev/github.com/ada-learning/google.com
VENV_PATH := $(PYTHON_D)/github.com/ada-learning/google.com

CMD = ./src/quickstart.py
SOURCE_PATHS=src


setup_dev: $(VENV_PATH_DEV)

$(VENV_PATH_DEV):
	$(PYTHON_3) -m venv $(VENV_PATH_DEV)
	"$(VENV_PATH_DEV)/bin/pip" install -U pip wheel
	"$(VENV_PATH_DEV)/bin/pip" install -r ./requirements/dev.txt
	# "$(VENV_PATH_DEV)/bin/pip" install -e .

setup_prod: $(VENV_PATH)

$(VENV_PATH):
	$(PYTHON_3) -m venv $(VENV_PATH)
	"$(VENV_PATH)/bin/pip" install -U pip wheel
	"$(VENV_PATH)/bin/pip" install -r ./requirements/prod.txt
	#"$(VENV_PATH)/bin/pip" install .

isort:
	"$(VENV_PATH_DEV)/bin/isort" $(SOURCE_PATHS) tests

pylint:
	"$(VENV_PATH_DEV)/bin/pylint" $(SOURCE_PATHS) tests

coverage_run:
	PYTHONPATH=src "$(VENV_PATH_DEV)/bin/coverage" run -m pytest -m 'not integration'

coverage_report:
	"$(VENV_PATH_DEV)/bin/coverage" report

mypy:
	"$(VENV_PATH_DEV)/bin/mypy" $(SOURCE_PATHS)

code_check: \
	setup_dev \
	isort \
	pylint \
	coverage_run coverage_report \
	mypy

run: setup_prod
	: $${BITBUCKET_ORG_REPOS}
	source "$(VENV_PATH)/bin/activate" && $(CMD)

clean_dev:
	rm -rfv "$(VENV_PATH_DEV)"

clean_prod: $(VENV_PATH)
	rm -rfv "$(VENV_PATH)"

activate_env_prod:
	@echo "activate \"$(VENV_PATH)/bin/activate\""
