.PHONY: default install

default: install

install:
	pipenv install --dev --skip-lock
