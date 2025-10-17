# Quick Reference: uv Commands

## Initial Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone project and sync dependencies (automatic venv creation)
uv sync

# Or manually create venv first
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
uv sync

# Sync with all dependency groups (including dev)
uv sync --all-groups
```

## Common Commands

```bash
# Sync dependencies from lockfile (fastest, recommended)
uv sync

# Sync with all groups (including dev)
uv sync --all-groups

# Sync specific group
uv sync --group dev

# Update lockfile
uv lock

# Update and upgrade all dependencies
uv lock --upgrade

# Show dependency tree
uv tree

# Run a command in the virtual environment
uv run python script.py
uv run pytest

# Use pip for one-off packages (not added to pyproject.toml)
uv pip install package-name

# Generate requirements.txt for legacy compatibility (optional)
uv pip compile pyproject.toml -o requirements.txt

# Export dependencies from lockfile to requirements format
uv export --format requirements-txt > requirements.txt
```

## Using Makefile

```bash
# Sync dependencies (recommended)
make sync

# Install project (creates venv + syncs)
make install

# Update all dependencies
make update

# Run tests
make test

# Run tests with coverage
make test-coverage

# Build package
make build

# Run pre-commit hooks
make pre-commit

# Clean build artifacts
make clean
```

## Updating Dependencies

### Adding a new dependency:

1. Edit `pyproject.toml` and add to `dependencies` list
2. Run: `uv lock`
3. Run: `uv sync`

### Updating a specific package:

1. Edit version in `pyproject.toml`
2. Run: `uv lock`
3. Run: `uv sync`

### Updating all packages:

```bash
uv lock --upgrade
uv sync
```

## Development Workflow

```bash
# After cloning the repository
uv sync

# After pulling changes
uv sync

# Before committing
make pre-commit
make test

# To build for distribution
make build
```

## Troubleshooting

### Clear cache

```bash
rm -rf .uv/
uv cache clean
```

### Regenerate lockfile

```bash
rm uv.lock
uv lock
uv sync
```

### Force reinstall

```bash
uv sync --reinstall
```

### Check for outdated packages

```bash
uv lock --upgrade --dry-run
```

## pip Compatibility

uv provides `uv pip` for pip-compatible operations:

```bash
# Install a package (like pip install)
uv pip install package-name

# Uninstall a package
uv pip uninstall package-name

# List installed packages
uv pip list

# Show package info
uv pip show package-name

# Freeze installed packages
uv pip freeze

# Compile requirements from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt
```

## Comparison with Poetry

| Poetry Command       | uv Equivalent                               |
| -------------------- | ------------------------------------------- |
| `poetry install`     | `uv sync`                                   |
| `poetry add package` | Edit pyproject.toml + `uv lock` + `uv sync` |
| `poetry update`      | `uv lock --upgrade` + `uv sync`             |
| `poetry run cmd`     | `uv run cmd`                                |
| `poetry shell`       | `source .venv/bin/activate`                 |
| `poetry export`      | `uv pip compile pyproject.toml`             |
| `poetry lock`        | `uv lock`                                   |

## Links

- uv Documentation: https://docs.astral.sh/uv/
- uv GitHub: https://github.com/astral-sh/uv
- Project Repository: https://github.com/wallaceespindola/PythonRuns
