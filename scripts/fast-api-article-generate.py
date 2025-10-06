import os
import zipfile
from pathlib import Path

# Define project root
project_root = Path("fastapi_article_project")

# Safety cleanup: remove any old project
if project_root.exists():
    import shutil

    shutil.rmtree(project_root)

# Recreate directories
(project_root / "app" / "routes").mkdir(parents=True, exist_ok=True)
(project_root / "tests").mkdir(parents=True, exist_ok=True)
(project_root / ".github" / "workflows").mkdir(parents=True, exist_ok=True)

# ---------- Files content ----------

article_md = """# FastAPI in Action: Modern and Asynchronous API Development

FastAPI has been one of the fastest-rising stars in the Python ecosystem...
"""

readme_md = """# FastAPI Article Project (uv-based)

[![CI](https://github.com/wallaceespindola/fastapi-article-project/actions/workflows/ci.yml/badge.svg)](https://github.com/wallaceespindola/fastapi-article-project/actions/workflows/ci.yml)

This project accompanies the article **FastAPI in Action: Modern and Asynchronous API Development**...
"""

pyproject_toml = """[project]
name = "fastapi-article-project"
version = "0.1.0"
description = "Demo FastAPI project accompanying the article 'FastAPI in Action'"
readme = "README.md"
requires-python = ">=3.10"
authors = [{name = "Wallace Espindola"}]

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "pydantic>=2.9.0",
    "sqlmodel>=0.0.22",
    "httpx>=0.27.0",
    "python-jose>=3.3.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.10.0",
    "ruff>=0.6.0",
    "pre-commit>=3.7.0",
    "types-python-jose>=3.3.4.9"
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "ANN", "N", "PL", "RUF"]
ignore = ["ANN101", "ANN102"]
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ANN"]
[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.10"
packages = ["app", "tests"]
show_error_codes = true
warn_return_any = true
warn_unused_ignores = true
no_implicit_optional = true
disallow_untyped_defs = true
strict_optional = true
"""

makefile_content = """
# FastAPI Article Project — Makefile (uv-based)
.PHONY: help venv install run test lint format typecheck check lock clean pre-commit-install pre-commit-run pre-commit-autoupdate

help:
\t@echo "Common commands: run, test, lint, format, typecheck, check, pre-commit-install"

venv:
\tuv venv

install:
\tuv pip install -e ".[dev]"

run:
\tuv run uvicorn app.main:app --reload

test:
\tuv run pytest -q

lint:
\tuv run ruff check .

format:
\tuv run ruff format .

typecheck:
\tuv run mypy app tests

check: lint typecheck

lock:
\tuv lock

clean:
\trm -rf .pytest_cache .ruff_cache .mypy_cache dist build **/__pycache__ *.egg-info

pre-commit-install:
\tuv run pre-commit install

pre-commit-run:
\tuv run pre-commit run --all-files

pre-commit-autoupdate:
\tuv run pre-commit autoupdate
"""

precommit_yaml = """repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        additional_dependencies: []
        files: ^(app|tests)/

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
      - id: detect-private-key
      - id: check-merge-conflict
"""

ci_yaml = """name: CI
on:
  push: {branches: [ main, master ]}
  pull_request: {branches: [ main, master ]}
jobs:
  build-test-lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: {python-version: [ '3.10', '3.11', '3.12' ]}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "${{ matrix.python-version }}"}
      - run: curl -LsSf https://astral.sh/uv/install.sh | sh && echo "${HOME}/.local/bin" >> $GITHUB_PATH
      - uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            .venv
          key: uv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('pyproject.toml') }}
          restore-keys: uv-${{ runner.os }}-${{ matrix.python-version }}-
      - run: uv venv && uv pip install -e ".[dev]"
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy app tests
      - run: uv run pytest -q
"""

main_py = """from fastapi import FastAPI
from app.routes import users, items

app = FastAPI(title="FastAPI Article Demo")
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI Article Project!"}
"""

models_py = """from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
"""

users_py = """from fastapi import APIRouter, HTTPException
from app.models import User

router = APIRouter()
_fake_users = {}

@router.post("/", response_model=User)
async def create_user(user: User):
    if user.email in _fake_users:
        raise HTTPException(status_code=400, detail="User already exists")
    _fake_users[user.email] = user
    return user

@router.get("/{email}", response_model=User)
async def get_user(email: str):
    user = _fake_users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""

items_py = """from fastapi import APIRouter, HTTPException
from app.models import Item

router = APIRouter()
_fake_items = {}

@router.post("/", response_model=Item)
async def create_item(item: Item):
    if item.name in _fake_items:
        raise HTTPException(status_code=400, detail="Item already exists")
    _fake_items[item.name] = item
    return item

@router.get("/{name}", response_model=Item)
async def get_item(name: str):
    item = _fake_items.get(name)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
"""

test_main = """from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, FastAPI Article Project!"}
"""

# ---------- Write files ----------

(project_root / "FastAPI_in_Action.md").write_text(article_md, encoding="utf-8")
(project_root / "README.md").write_text(readme_md, encoding="utf-8")
(project_root / "pyproject.toml").write_text(pyproject_toml, encoding="utf-8")
(project_root / "Makefile").write_text(makefile_content, encoding="utf-8")
(project_root / ".pre-commit-config.yaml").write_text(precommit_yaml, encoding="utf-8")
(project_root / ".github" / "workflows" / "ci.yml").write_text(ci_yaml, encoding="utf-8")

(project_root / "app" / "__init__.py").write_text("", encoding="utf-8")
(project_root / "app" / "main.py").write_text(main_py, encoding="utf-8")
(project_root / "app" / "models.py").write_text(models_py, encoding="utf-8")
(project_root / "app" / "routes" / "__init__.py").write_text("", encoding="utf-8")
(project_root / "app" / "routes" / "users.py").write_text(users_py, encoding="utf-8")
(project_root / "app" / "routes" / "items.py").write_text(items_py, encoding="utf-8")

(project_root / "tests" / "__init__.py").write_text("", encoding="utf-8")
(project_root / "tests" / "test_main.py").write_text(test_main, encoding="utf-8")

# ---------- Package to zip ----------

zip_path = Path("fastapi_article_project.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_root):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(project_root)
            zipf.write(file_path, arcname)

zip_path
