PKG ?= ./oop_es
VENV := .venv
ACTIVATE := $(PKG)/$(VENV)/bin/activate
PYPROJECT := $(PKG)/pyproject.toml
BUILD := ".[test]"
PYTHON := "python3"

.PHONY: all
all: $(ACTIVATE)

$(ACTIVATE): $(PYPROJECT)
	cd $(PKG) && test -d $(VENV) || uv venv
	. $(ACTIVATE) && cd $(PKG) && uv pip install -e $(BUILD) ../oop_es
	touch $(ACTIVATE)

.PHONY: test
test: $(ACTIVATE)
	. $(ACTIVATE) && cd $(PKG) && pytest tests --ignore=tests/integration

.PHONY: testint
testint: $(ACTIVATE) # to run integration tests for oop_es_pg
	. $(ACTIVATE) && cd $(PKG)/tests/integration && ./test.sh

.PHONY: cs
cs: $(ACTIVATE)
	. $(ACTIVATE) && cd $(PKG) && ruff check src tests
	. $(ACTIVATE) && cd $(PKG) && ty check src tests

.PHONY: build
build:
	cd $(PKG) && $(PYTHON) -m build

.PHONY: run
run: $(ACTIVATE) # to run example with `make run PKG=./example`
	. $(ACTIVATE) && cd $(PKG) && cd src/example && $(PYTHON) run.py

