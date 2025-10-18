# Makefile — project automation
# ATTENTION: Use TABS (not spaces) to indent recipe commands.

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.ONESHELL:
.DELETE_ON_ERROR:


version:


# ---- Configurable variables ----
PYTHON            ?= python3
PACKAGE           ?= PythonRuns
#INDEX_URL        ?= https://nexus.myrepo.net/repository/pypi-releases/simple # when using private repo (e.g., Nexus)
INDEX_URL         ?= https://pypi.org/simple
EXTRA_INDEX_URL   ?= https://pypi.org/simple
REPOSITORY_UPLOAD ?= https://nexus.myrepo.net/repository/pypi-releases/
UV_FLAGS          := --index-url $(INDEX_URL) --extra-index-url $(EXTRA_INDEX_URL)

# ---- Colors ----
C_CYAN  := \033[1;36m
C_GREEN := \033[1;32m
C_RST   := \033[0m

# ---- Logging helpers ----
define log_start
	@SECONDS=0; printf "\n$(C_CYAN)[%s] ▶ Starting %s$(C_RST)\n" "$$(date +'%F %T')" "$(1)"
endef
define log_done
	@printf "$(C_GREEN)✓ Done %s in %ss$(C_RST)\n" "$(1)" "$$SECONDS"
endef

.PHONY: sync install config update test test-coverage run pre-commit build deploy version help list clean \
        check-dist twine-check check-tools check-pytest check-precommit check-twine check-build check-uv \
        requirements requirements-clean

# ---- Guard checks ----
check-uv:
	@command -v uv >/dev/null || { echo "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

check-dist: ## Ensure ./dist exists and contains artifacts
	$(call log_start,$@)
	@test -d dist || { echo "No 'dist/' directory. Run 'make build' first."; exit 1; }
	@test -n "$$(ls -A dist 2>/dev/null)" || { echo "'dist/' is empty. Run 'make build' first."; exit 1; }
	$(call log_done,$@)

twine-check: check-dist check-twine ## Validate built artifacts (sdist/wheel) with Twine
	$(call log_start,$@)
	twine check dist/*
	$(call log_done,$@)

# ---- Target-specific tool checks ----
check-pytest:
	@command -v pytest >/dev/null || { echo "pytest not found. Run 'uv sync --all-groups' or 'make sync'"; exit 1; }
check-precommit:
	@command -v pre-commit >/dev/null || { echo "pre-commit not found. Run 'uv sync --all-groups'"; exit 1; }
check-twine:
	@command -v twine >/dev/null || { echo "twine not found. Run 'uv pip install --system twine'"; exit 1; }
check-build:
	@$(PYTHON) -c "import build" 2>/dev/null || { echo "build module not found. Run 'uv pip install --system build'"; exit 1; }

# Optional: quick all-in-one diagnostic
check-tools: ## Check common CLI tools are available
	$(call log_start,$@)
	command -v pip >/dev/null
	command -v $(PYTHON) >/dev/null
	command -v awk >/dev/null
	$(MAKE) check-pytest || true
	$(MAKE) check-precommit || true
	$(MAKE) check-twine || true
	$(MAKE) check-build || true
	$(call log_done,$@)

# ---- Targets ----
config: ## Configure pip indexes (optional, for legacy pip usage)
	$(call log_start,$@)
	pip config --user set global.index-url $(INDEX_URL)
	pip config --user set global.extra-index-url $(EXTRA_INDEX_URL)
	pip config --user list
	$(call log_done,$@)

clean: ## Remove build/test artifacts
	$(call log_start,$@)
	rm -rf dist build .pytest_cache .mypy_cache .coverage htmlcov report.html
	find . -type d -name "__pycache__" -exec rm -rf {} \;
	find . -type d -name "*.egg-info" -exec rm -rf {} \;
	$(call log_done,$@)

sync: check-uv ## Sync dependencies from uv.lock (recommended)
	$(call log_start,$@)
	uv sync
	$(call log_done,$@)

install: check-uv ## Install project with uv (creates venv and syncs dependencies)
	$(call log_start,$@)
	uv venv || true
	uv sync
	$(call log_done,$@)

update: check-uv ## Update dependencies and regenerate lockfile
	$(call log_start,$@)
	uv lock --upgrade
	uv sync
	$(call log_done,$@)

requirements: check-uv ## Export requirements.txt from pyproject.toml
	$(call log_start,$@)
	uv pip compile pyproject.toml -o requirements.txt $(UV_FLAGS)
	$(call log_done,$@)

requirements-clean: ## Delete requirements.txt
	$(call log_start,$@)
	rm -f requirements.txt
	@echo "requirements.txt deleted"
	$(call log_done,$@)

test: check-pytest ## Run tests (verbose)
	$(call log_start,$@)
	pytest --verbose
	$(call log_done,$@)

test-coverage: check-pytest ## Run tests with coverage; HTML at ./report.html
	$(call log_start,$@)
	pytest --cov=$(PACKAGE) --verbose --html=report.html --self-contained-html
	$(call log_done,$@)

run: ## Run the package as a module
	$(call log_start,$@)
	$(PYTHON) -m $(PACKAGE)
	$(call log_done,$@)

pre-commit: check-precommit ## Run all pre-commit hooks
	$(call log_start,$@)
	pre-commit run --all-files
	$(call log_done,$@)

build: check-build clean ## Build sdist and wheel into ./dist
	$(call log_start,$@)
	$(PYTHON) -m build
	$(call log_done,$@)

deploy: twine-check ## Upload ./dist to Nexus (uses TWINE_* env vars)
	$(call log_start,$@)
	twine upload --repository-url $(REPOSITORY_UPLOAD) dist/*
	$(call log_done,$@)

version: ## Show package version
	$(call log_start,$@)
	$(PACKAGE) -v
	$(call log_done,$@)

help: ## List available commands (default)
	@awk 'BEGIN {FS = ":.*## " } \
	/^[a-zA-Z0-9_.-]+:.*## / { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' \
	$(MAKEFILE_LIST)

list: help ## Alias for help

# ======================== HOW TO USE ========================
# List commands (with descriptions): make   OR   make help
# Safer deploy: export TWINE_USERNAME / TWINE_PASSWORD (or token) before `make deploy`
# Examples:
#   make install
#   make update
#   make test-coverage
#   make build && make twine-check && make deploy
