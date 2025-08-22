.PHONY: install test test-coverage run pre-commit build deploy version help

# ATTENTION: It must be TABS AND NOT SPACES before the commands, otherwise it will not work.

install:
	pip install -e .

test:
	pytest --verbose

test-coverage:
	pytest --cov=s2c2rfams --verbose --html=report.html --self-contained-html

run:
	python3 -m PythonRuns

pre-commit:
	pre-commit run --all-files

build:
	rm -rf ./dist
	python3 -m build

deploy:
	twine upload --repository-url https://nexus.myrepo.net/repository/pypi-releases/ dist/* -u <user> -p <pass>

version:
	PythonRuns -v

help:
	PythonRuns -h

# USAGE:
# make install
# make test
# make test-coverage
# make run
# make pre-commit
# make build
# make deploy
# make version
# make help
