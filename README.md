![Python](https://www.python.org/static/community_logos/python-logo-generic.svg)

# PythonRuns

![Apache 2.0 License](https://img.shields.io/badge/License-Apache2.0-orange)
![Python](https://img.shields.io/badge/Built_with-Python-blue)
![Pytest](https://img.shields.io/badge/Powered_by-Pytest-green)
[![CI](https://github.com/wallaceespindola/PythonRuns/actions/workflows/ci.yml/badge.svg)](https://github.com/wallaceespindola/PythonRuns/actions/workflows/ci.yml)

Tests on Python Code Examples.

A collection of small, self-contained Python scripts and proofs of concept: formatting and language
features, file and image utilities, SQLite/PostgreSQL persistence with Tkinter UIs, calls to public
Brazilian government APIs, JWT handling and more. Each example is a standalone module under
[`pythonruns/src/mytests/`](pythonruns/src/mytests), runnable on its own with `python -m`.

## Table of Contents

- [What's Inside](#whats-inside)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Latest Articles, Publications and Tech-Talks](#-latest-articles-publications-and-tech-talks)
- [Author](#author)
- [License](#license)

## What's Inside

All examples live in [`pythonruns/src/mytests/`](pythonruns/src/mytests).

### Language basics and formatting

- [calculate_power.py](pythonruns/src/mytests/calculate_power.py): calculate a power x^y of a number.
- [float_format.py](pythonruns/src/mytests/float_format.py): tests and prints multiple float formats.
- [boolean_number.py](pythonruns/src/mytests/boolean_number.py): converting numbers to booleans.
- [sort_list.py](pythonruns/src/mytests/sort_list.py): sorting a list of numbers ascending and descending.
- [switch_case.py](pythonruns/src/mytests/switch_case.py): `match`/`case` statement driven by console input.
- [input_console.py](pythonruns/src/mytests/input_console.py): reading values from the console and combining
  `and`/`or` conditions.
- [future/with_future.py](pythonruns/src/mytests/future/with_future.py) and
  [future/without_future.py](pythonruns/src/mytests/future/without_future.py): effect of
  `from __future__ import annotations` on `__annotations__`.
- [app_logging.py](pythonruns/src/mytests/app_logging.py): the basics of logging in Python.
- [happy_teacher_day.py](pythonruns/src/mytests/happy_teacher_day.py): prints a heart in the console with the word
  Teachers, for happy teachers day.
- [I_love_you.py](pythonruns/src/mytests/I_love_you.py): prints a heart in the console with a given 8-character word.

### Files, text and data

- [camel_2_snake_case.py](pythonruns/src/mytests/camel_2_snake_case.py): converts a file text content from camel case
  to snake case.
- [split_files.py](pythonruns/src/mytests/split_files.py): splits a text input file (like a log) into a given number
  of chunks.
- [convert_pdf_to_docx.py](pythonruns/src/mytests/convert_pdf_to_docx.py): converts a pdf file to a docx file.
- [fake_data.py](pythonruns/src/mytests/fake_data.py): creates fake test data using Faker.
- [short_uuid.py](pythonruns/src/mytests/short_uuid.py): generates short UUIDs and converts standard UUIDs with
  `shortuuid`.
- [pickle/pickle_serialize_load.py](pythonruns/src/mytests/pickle/pickle_serialize_load.py): serializing and loading
  objects with `pickle`.
- [progress_bar.py](pythonruns/src/mytests/progress_bar.py): console progress bars with `progress` and `tqdm`.
- [plot_graph.py](pythonruns/src/mytests/plot_graph.py): sin/cos/tan subplots with Matplotlib and NumPy.

### Images and QR codes

- [remove_background.py](pythonruns/src/mytests/remove_background.py): removes background from images, letting only
  the main subject.
- [resize_images.py](pythonruns/src/mytests/resize_images.py) and
  [compress_images.py](pythonruns/src/mytests/compress_images.py): resize/compress image files down to a target size
  in KB.
- [qrcode/generate_qrcode.py](pythonruns/src/mytests/qrcode/generate_qrcode.py): creates a QR-Code from your data.
- [qrcode/generate_qrcode_with_midle_empty.py](pythonruns/src/mytests/qrcode/generate_qrcode_with_midle_empty.py):
  QR code with a transparent hole in the center for a logo.

### Databases (Tkinter UIs)

- [database/save_to_mem_db.py](pythonruns/src/mytests/database/save_to_mem_db.py),
  [persist_json_in_memory.py](pythonruns/src/mytests/database/persist_json_in_memory.py),
  [persist_json_to_db.py](pythonruns/src/mytests/database/persist_json_to_db.py),
  [persist_json_to_db_visualize.py](pythonruns/src/mytests/database/persist_json_to_db_visualize.py),
  [persist_json_disk_to_db_visualize.py](pythonruns/src/mytests/database/persist_json_disk_to_db_visualize.py):
  storing and viewing JSON data in memory or an in-memory SQLite database through a Tkinter window.
- [database/persist_with_postgres.py](pythonruns/src/mytests/database/persist_with_postgres.py): the same idea backed
  by PostgreSQL via `psycopg2` (requires a running PostgreSQL instance).

### Public APIs, security and ops

- [jusbr/call_api_fines_ibama_brazil.py](pythonruns/src/mytests/jusbr/call_api_fines_ibama_brazil.py): Environmental
  fines research in Brazil's government site.
- [jusbr/call_api_tjmg.py](pythonruns/src/mytests/jusbr/call_api_tjmg.py),
  [call_api_trf_proc.py](pythonruns/src/mytests/jusbr/call_api_trf_proc.py),
  [call_api_trf_classe_orgao.py](pythonruns/src/mytests/jusbr/call_api_trf_classe_orgao.py): queries against the CNJ
  DataJud public API (by process number, or by class/court body).
- [jwt_test.py](pythonruns/src/mytests/jwt_test.py): `JWTManager` class to create and decode JWT tokens with
  `python-jose`.
- [backup_restore_wordpress.py](pythonruns/src/mytests/backup_restore_wordpress.py): backup/restore of a WordPress
  site (database and files) between a local machine and a remote server over SSH/SFTP with `paramiko`.

### Tests

- [tests/mytests/test_jwt_manager.py](tests/mytests/test_jwt_manager.py): pytest suite for `JWTManager` (token
  creation, decoding, expiry, invalid signatures, multiple HMAC algorithms).
- [tests/test_examples.py](tests/test_examples.py): `unittest` check of OS path separators.

The [`scripts/`](scripts) folder holds standalone shell/Python utilities (server install, disk cleanup, git helpers,
app monitoring) that are not part of the package.

## Tech Stack

- Python 3.11 / 3.12 (`requires-python = ">=3.11,<3.13"`), managed with [uv](https://docs.astral.sh/uv/)
- pytest, pytest-cov, pytest-html
- Main libraries used by the examples: Faker, python-jose, pdf2docx, Pillow, rembg, OpenCV, qrcode, Matplotlib,
  NumPy, pandas, requests, paramiko, psycopg2, shortuuid, tqdm, progress
- Code quality: ruff, black, isort, mypy, pre-commit
- CI: GitHub Actions ([ci.yml](.github/workflows/ci.yml)) running tests on Python 3.11 and 3.12

## Prerequisites

- Python 3.11 or 3.12
- [uv](https://docs.astral.sh/uv/)
- Tkinter (bundled with most Python installs) for the `database/` examples
- A PostgreSQL instance only for `persist_with_postgres.py`

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast and reliable Python package management.

### Installing uv

If you don't have uv installed yet:

```sh
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Setting up the project

Create and activate a virtual environment, then install dependencies:

```sh
# Create a virtual environment and install dependencies (one step)
uv sync

# Or manually:
# 1. Create a virtual environment
uv venv

# 2. Activate it
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 3. Sync all dependencies
uv sync
```

Alternatively, you can use the provided makefile:

```sh
make install
```

### Working with uv

Common uv commands:

```sh
# Sync dependencies from uv.lock (recommended for consistent environments)
uv sync

# Sync with all dependency groups (including dev)
uv sync --all-groups

# Update dependencies and regenerate lockfile
uv lock --upgrade
uv sync

# Add a new dependency
# (Edit pyproject.toml, then run:)
uv lock
uv sync

# Run a command in the virtual environment
uv run python -m pythonruns
uv run pytest

# Use pip if needed for one-off packages (not recommended for project deps)
uv pip install package-name
```

## How to Run

Run any example as a module from the repository root:

```sh
uv run python -m pythonruns.src.mytests.fake_data
uv run python -m pythonruns.src.mytests.jwt_test
uv run python -m pythonruns.src.mytests.split_files /path/to/app.log 5
```

The general form is:

```sh
python3 -m pythonruns.src.mytests.file_to_run
```

Some examples read from [`resources/`](resources) and write to [`output/`](output) using relative paths
(`../resources`, `../output`), so check the paths at the top of a script before running it.

## Running Tests

```sh
# Run all tests (same command as CI)
uv run pytest tests/ -v

# With coverage (HTML report in ./htmlcov)
uv run pytest tests/ --cov=pythonruns --cov-report=html

# Or via the makefile (requires the virtual environment to be activated)
make test
```

Other makefile targets: `make help` lists them all (`install`, `sync`, `update`, `pre-commit`, `build`, `clean`, ...).

## Project Structure

```text
PythonRuns/
├── pythonruns/
│   ├── hello_world.py
│   └── src/mytests/        # example modules (database/, future/, jusbr/, pickle/, qrcode/, ...)
├── tests/                  # pytest / unittest tests
├── resources/              # sample inputs (images, sample.pdf)
├── output/                 # generated outputs (images, CSV, docx)
├── scripts/                # standalone shell/Python utilities
├── docs/                   # uv migration notes and quick reference
├── pyproject.toml          # project metadata and dependencies
├── uv.lock
└── makefile
```

## 📝 Latest Articles, Publications and Tech-Talks

- **[[Code & Coffee - Substack] Java turns 30: An Innovation Journey Through Time and Technology](https://wallaceespindola.substack.com/p/java-turns-30-an-innovation-journey)** - What 30 years of Java can teach us about building tech that lasts.
  A timeline on what happened to **Java** from May 23rd 1995, when **Sun Microsystems** introduced Java 1.0 to the world, until modern days that made Java essentially great.
- **[[Dev Community] FastAPI Unleashed: Building Modern and High-Performance APIs](https://dev.to/wallaceespindola/fastapi-your-fast-and-modern-framework-for-apis-3mmo)** - Demostranting FastAPI, a web framework designed for building APIs quickly and efficiently. Python based natively async, it takes advantage of non-blocking I/O to handle high loads, with extra features such as embedded data validation with Pydantic and auto-documentation with Swagger/Redoc.
- **[[Dev Community] NoSQL Fighters Arena: The Battle of Data Titans](https://bit.ly/nosql-db-fighters-arena)** - Explore NoSQL databases reimagined as superheroes, each with unique powers and weaknesses, in a fun and visual battle-style format.
- **[[LinkedIn Pulse] Java is turning 30 soon! Here's Why You Should Care, Even if You're Not a Tech Person](https://bit.ly/java-turning-30-soon-why-care)** - Java is a super famous programming language, and it is almost turning 30. But wait, what exactly is Java, and why should it matter to you?
- **[[DZone] Top NoSQL Databases and When to Use Each](https://bit.ly/top-nosql-databases-and-use)** - A practical guide comparing NoSQL technologies like MongoDB, Cassandra, Redis, and more, highlighting their strengths, limitations, and best use cases.
- **[[Dev Community] Test Python Code Like a Pro with Poetry, Tox, Nox and CI/CD](https://bit.ly/test-python-poetry-tox-nox-cicd)** - Improving your test coverage with multiple python versions through the use of of tools like Poetry, Pytest, Tox, Nox and CI/CD.
- **[[Dev Community] Python Multithreading: Unlocking Concurrency for Better Performance](https://bit.ly/python-multithreading)** - The essentials of Python multithreading with practical examples and best practices to enhance application performance through concurrency. A must-read, to understand threading application performance in deep.
- **[[DZone] Secure Password Hashing in Java: Best Practices and Code Examples](https://bit.ly/secure-password-hashing-in-java)** - Secure password hashing using modern algorithms like BCrypt, Argon2, and PBKDF2 with salting and computational intensity for better security, as alternative to SHA-512.
- **More available on [my LinkedIn page](https://www.linkedin.com/in/wallaceespindola)**.

## Author

- Wallace Espindola, Sr. Software Engineer / Solution Architect / Java & Python Dev
- **LinkedIn:** [linkedin.com/in/wallaceespindola/](https://www.linkedin.com/in/wallaceespindola/)
- **GitHub:** [github.com/wallaceespindola](https://github.com/wallaceespindola)
- **E-mail:** [wallace.espindola@gmail.com](mailto:wallace.espindola@gmail.com)
- **Twitter:** [@wsespindola](https://twitter.com/wsespindola)
- **Gravatar:** [gravatar.com/wallacese](https://gravatar.com/wallacese)
- **Dev Community:** [dev.to/wallaceespindola](https://dev.to/wallaceespindola)
- **DZone Articles:** [DZone Profile](https://dzone.com/users/1254611/wallacese.html)
- **Pulse Linkedin:** [LinkedIn Articles](https://www.linkedin.com/in/wallaceespindola/recent-activity/articles/)
- **Website:** [W-Tech IT Solutions](https://www.wtechitsolutions.com/)
- **Substack:** [wallaceespindola.substack.com](https://wallaceespindola.substack.com/)
- **Medium:** [medium.com/@wallaceespindola](https://medium.com/@wallaceespindola)
- **Slides:** [speakerdeck.com/wallacese](https://speakerdeck.com/wallacese)

## License

- This project is released under the Apache 2.0 License.
- See the [LICENSE](LICENSE) file for details.
- Copyright © 2025 [Wallace Espindola](https://github.com/wallaceespindola/).
