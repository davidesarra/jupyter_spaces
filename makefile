SHELL := /usr/bin/env bash

install:
	@ pip install --upgrade build pip setuptools twine && \
	pip install -e . -r requirements/lint.txt -r requirements/test.txt

build: install
	@ python -m build

publish: build
	@ python -m twine upload dist/*

publish-test: build
	@ python -m twine upload --repository testpypi dist/*

test: lint
	@ pytest -vvv

test-all: lint
	@ tox

lint:
	@ isort --check-only --diff --quiet . && \
	black --check --diff .

format:
	@ isort . && \
	black .
