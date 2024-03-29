.SILENT:
BUILD = .
SHELL = bash
C_DIR := $(lastword $(subst /, ,$(CURDIR)))

init:
	echo "Init Git and Python inside" $(C_DIR)
#	git init
	python3 -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	touch requirements.txt
	pip install -r requirements.txt
	pre-commit install

.env:
	echo "Create $@ from template"
	SPL_A=$(C_DIR)  envsubst < tpl.env | op inject -f > $@ && chmod 600 $@

env: .env

up: env
	echo "Powering up"
	./up.sh

down:
	echo "Powering down"
	docker compose down

clean:
	echo "Powering down and removing volumes"
	docker compose down -v
	rm -f .env

spl:
	echo "Downloading latest app version from container"
	./get-spl.sh

token:
	echo "Creating Admin token"
	./token.sh

.PHONY: init up down clean spl token
