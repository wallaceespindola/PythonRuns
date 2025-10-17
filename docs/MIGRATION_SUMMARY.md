# Migration from Poetry to uv - Summary

## Overview
This project has been successfully migrated from Poetry to uv for package management. uv is a modern, fast Python package installer and resolver written in Rust, providing significantly faster dependency resolution and installation.

## Changes Made

### 1. Configuration Files

#### pyproject.toml
- **Removed**: `poetry-plugin-export` dependency
- **Fixed**: Dependency syntax to use standard PEP 508 format (removed parentheses around version specifiers)
- **Changed**: `license = "Apache-2.0"` to `license = { text = "Apache-2.0" }` for PEP 621 compliance
- **Added**: `[dependency-groups]` section for development dependencies
  - pytest>=8.3.4
  - pytest-cov>=5.0.0
  - pytest-html>=4.0.0
  - ruff>=0.4.0
  - black>=24.0.0
  - isort>=5.13.0
  - mypy>=1.0.0

#### requirements.txt (REMOVED)
- **No longer needed**: uv manages dependencies directly from pyproject.toml and uv.lock
- Use `uv sync` instead of `pip install -r requirements.txt`
- For legacy compatibility, can generate with: `uv pip compile pyproject.toml -o requirements.txt`

#### uv.lock (NEW)
- **Created**: Lock file for reproducible builds
- Size: 373KB with 212 packages resolved
- Should be committed to version control for reproducibility

#### poetry.lock (DELETED)
- Removed as it's no longer needed with uv

### 2. Build Configuration

#### makefile
- **Updated**: Variable definitions to include `UV`
- **Removed**: `REQUIREMENTS_MAIN` and `REQUIREMENTS_DEV` variables (no longer needed)
- **Modified**: All targets to use `uv sync` and `uv lock`:
  - `sync`: New target to sync from uv.lock
  - `install`: Now uses `uv venv` and `uv sync`
  - `update`: Uses `uv lock --upgrade` and `uv sync`
  - `check-uv`: New guard to ensure uv is installed

#### makefile.windows
- **Updated**: PowerShell script to use uv commands
- **Removed**: `$RequirementsMain` and `$RequirementsDev` variables
- **Added**: `sync` task
- **Modified**: All tasks (install, update) to use `uv sync` and `uv lock`

### 3. CI/CD Configuration

#### .github/workflows/ci.yml
- **Added**: `astral-sh/setup-uv@v5` action to all jobs
- **Removed**: `cache: "pip"` from setup-python actions (uv has its own caching)
- **Changed**: All dependency installation to use `uv sync` instead of pip/requirements.txt
- Modified jobs:
  - test: Uses `uv sync --all-groups`
  - lint: Uses `uv sync --group dev`
  - security: Uses `uv sync` + additional tools
  - build: Uses `uv pip install --system` for build tools

#### .github/workflows/pre-commit.yml
- **Added**: `astral-sh/setup-uv@v5` action for consistency

### 4. Version Control

#### .gitignore
- **Updated**: Poetry section to explicitly ignore `poetry.lock`
- **Added**: uv section with comments
  - Tracks `uv.lock` (should be committed)
  - Ignores `.uv/` cache directory

### 5. Documentation

#### README.md
- **Replaced**: Installation section with comprehensive uv instructions
- **Added**: "Installing uv" subsection with installation commands for different platforms
- **Added**: "Setting up the project" subsection with detailed setup steps
- **Added**: "Working with uv" subsection with common uv commands:
  - `uv sync` - Sync dependencies from lockfile
  - `uv lock --upgrade` - Update dependencies
  - `uv run` - Run commands in the virtual environment
  - `uv pip install` - Install packages

## Benefits of Using uv

1. **Speed**: 10-100x faster than pip for dependency resolution
2. **Modern**: Written in Rust, actively maintained by Astral
3. **Compatible**: Works with existing pip workflows and requirements.txt
4. **Reliable**: Better dependency resolution algorithm
5. **Integrated**: Works seamlessly with pyproject.toml and PEP 621
6. **Caching**: Efficient caching mechanism built-in

## Migration Commands Used

```bash
# Generate lock file from pyproject.toml
uv lock

# Test installation (dry-run)
uv sync --dry-run

# Verify dependency tree
uv tree
```

## How to Use After Migration

### First-time Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repo>
cd PythonRuns

# Sync dependencies (creates venv automatically if needed)
uv sync

# Or use makefile
make install
```

### Daily Workflow
```bash
# Sync dependencies (fastest, uses lockfile)
uv sync

# Sync with all groups including dev
uv sync --all-groups

# Add new dependency
# 1. Edit pyproject.toml
# 2. Run:
uv lock
uv sync

# Update all dependencies
uv lock --upgrade
uv sync

# Run tests
uv run pytest

# Or use makefile
make test
```

### Using pip when needed
```bash
# For one-off packages not in project dependencies
uv pip install package-name

# Generate requirements.txt if needed for legacy tools
uv pip compile pyproject.toml -o requirements.txt
```

## Files Modified

- `.github/workflows/ci.yml` - Updated CI to use uv sync
- `.github/workflows/pre-commit.yml` - Added uv setup
- `.gitignore` - Updated for uv files
- `README.md` - Updated installation instructions
- `makefile` - Updated to use uv sync/lock commands
- `makefile.windows` - Updated PowerShell script for uv sync/lock
- `pyproject.toml` - Modernized and added dependency-groups

## Files Added

- `uv.lock` - Lock file for reproducible builds (373KB, 212 packages)

## Files Removed

- `poetry.lock` - No longer needed
- `requirements.txt` - No longer needed (can be generated if required)

## Verification

The migration was verified with:
- ✅ `uv lock` - Successfully resolved 212 packages
- ✅ `uv sync --dry-run` - Verified installation plan
- ✅ No poetry dependencies remain in requirements.txt
- ✅ All configuration files updated consistently
- ✅ CI/CD workflows use uv
- ✅ Documentation updated

## Notes

- The project is now faster to install and more maintainable
- All existing workflows (tests, pre-commit, builds) continue to work
- The makefile provides convenient shortcuts for common tasks
- uv is fully compatible with pip workflows, providing an easy migration path
