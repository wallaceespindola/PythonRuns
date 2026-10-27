# CLAUDE.md

Python playground: small standalone scripts and proofs of concept, not one app.

## Commands

- `make install` / `make sync` — create `.venv` and sync from `uv.lock` (uv only, no pip)
- `make test` — `pytest` on `tests/`; single test: `uv run pytest tests/mytests/test_jwt_manager.py -k expired`
- `make test-coverage`, `make pre-commit`, `make help` for the rest
- Lint/format: `uv run ruff check .`, `uv run black -l 120`, `uv run isort`

## Layout

- `pythonruns/src/mytests/` — independent example scripts (each runnable via `__main__`)
- `scripts/` — ops/utility scripts (shell + Python), not imported by the package
- `tests/` — pytest suite; mirrors `pythonruns/src/mytests` under `tests/mytests`
- `resources/` inputs, `output/` generated files

## Dependencies

- `pyproject.toml` is the source of truth; always commit the regenerated `uv.lock`.
- Python `>=3.14` (CI on 3.14).
- Dependabot alerts target `uv.lock`; fix by raising the floor in `pyproject.toml`, then `uv lock --upgrade`.
- JWT uses PyJWT (python-jose was dropped: unpatched critical CVE). Secrets come from env (`.env.example`).
- `numpy>=2.3` is required by current `rembg`; don't re-pin `numpy<2`.
- Runtime deps = only packages actually imported; tooling (pytest, build, twine, pre-commit, linters) lives in the `dev` group.
  Don't re-add PyPI `argparse`/`pathlib` backports (they shadow stdlib) or jupyterlab (unused, large CVE surface).
- CI `security` job blocks on `pip-audit` (locked deps) and bandit high/high. Actions are pinned to commit SHAs.

## Security conventions

- SSH (paramiko): known_hosts + `RejectPolicy`, never `AutoAddPolicy`; `ssh-rsa` (SHA-1) disabled.
- Pass DB/sudo passwords via stdin or `MYSQL_PWD`, never argv; no `shell=True` with interpolated values.
- HTTP: always `timeout=`, never `verify=False`; API keys from env.
