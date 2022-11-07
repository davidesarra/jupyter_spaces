SHELL := /usr/bin/env bash

install:
	@ pip install --upgrade build pip setuptools twine && \
	pip install -e .[lint,test]

build: install
	@ python -m build

publish: build
	@ python -m twine upload dist/*

publish-test: build
	@ python -m twine upload --repository testpypi dist/*

test: lint
	@ pytest

test-all: lint
	@ tox

lint:
	@ isort --check-only --diff --quiet . && \
	black --check --diff .

format:
	@ isort . && \
	black .
