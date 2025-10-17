# Post-Migration Verification Checklist

Use this checklist to verify the migration from Poetry to uv was successful.

## ✅ Pre-Commit Checks

- [ ] Review changes: `git diff`
- [ ] Check modified files: `git status`
- [ ] Validate pyproject.toml syntax: `python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"`
- [ ] Check uv.lock exists: `ls -lh uv.lock`
- [ ] Verify requirements.txt is removed: `test ! -f requirements.txt && echo "OK"`
- [ ] Verify Poetry removed from project: `grep -ir poetry pyproject.toml makefile* .github/workflows/*.yml || echo "Clean"`

## ✅ Functional Tests

- [ ] Lock file generation: `uv lock`
- [ ] Dependency resolution: `uv tree | head -20`
- [ ] Dry-run sync: `uv sync --dry-run`
- [ ] Sync dependencies: `uv sync`
- [ ] Sync with dev group: `uv sync --all-groups`
- [ ] Run tests: `uv run pytest` or `make test`
- [ ] Check imports: `uv run python -c "import pythonruns; print('OK')"`

## ✅ CI/CD Verification

- [ ] GitHub Actions workflows use `astral-sh/setup-uv@v5`
- [ ] All workflows use `uv sync` instead of pip/requirements.txt
- [ ] No `cache: "pip"` in workflow files
- [ ] Pre-commit workflow includes uv setup

## ✅ Configuration Files

- [ ] pyproject.toml has `[dependency-groups]` section
- [ ] pyproject.toml dependencies use PEP 508 syntax (no parentheses)
- [ ] No poetry-plugin-export in dependencies
- [ ] makefile uses `uv sync` and `uv lock` commands
- [ ] makefile has `sync` target
- [ ] makefile removed REQUIREMENTS_MAIN and REQUIREMENTS_DEV variables
- [ ] makefile.windows uses `uv sync` and `uv lock`
- [ ] .gitignore includes uv patterns
- [ ] .gitignore explicitly ignores poetry.lock
- [ ] .gitignore tracks uv.lock (not ignored)
- [ ] requirements.txt removed (or optional)

## ✅ Documentation

- [ ] README.md has uv installation instructions
- [ ] README.md has "Working with uv" section
- [ ] MIGRATION_SUMMARY.md exists
- [ ] UV_QUICK_REFERENCE.md exists

## ✅ Build and Deploy

- [ ] Clean build: `make clean`
- [ ] Build package: `make build` or `python -m build`
- [ ] Check distribution: `twine check dist/*` (after build)

## ✅ Team Communication

- [ ] Update team about the change
- [ ] Share UV_QUICK_REFERENCE.md with team
- [ ] Update any project documentation
- [ ] Update developer onboarding docs

## 🔧 Common Issues

### If uv is not installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

### If dependencies don't resolve:
```bash
rm uv.lock
uv lock
uv sync
```

### If CI fails:
- Check GitHub Actions logs
- Verify `astral-sh/setup-uv@v5` is used
- Ensure `uv sync` is used instead of pip install

### If old .venv causes issues:
```bash
rm -rf .venv
uv sync
```

### Need requirements.txt for a legacy tool:
```bash
# Generate from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt

# Or export from lockfile
uv export --format requirements-txt > requirements.txt
```

## 📝 Final Steps

- [ ] Commit all changes: `git add -A`
- [ ] Create meaningful commit message
- [ ] Push to remote: `git push`
- [ ] Update any CI/CD secrets if needed
- [ ] Monitor first CI/CD run with uv
- [ ] Update project wiki/docs if applicable

## ✨ Migration Complete!

Once all items are checked, the migration is complete and verified.

---

For questions or issues, refer to:
- MIGRATION_SUMMARY.md - Detailed migration documentation
- UV_QUICK_REFERENCE.md - Command reference
- https://docs.astral.sh/uv/ - Official uv documentation
