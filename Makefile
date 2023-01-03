SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: clean install

.PHONY: clean
clean: ## Removes project virtual env
	rm -rf .venv build dist **/*.egg-info .pytest_cache node_modules .coverage

.PHONY: install
install: ## Install the project dependencies and pre-commit using Poetry.
	poetry install
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push

.PHONY: test
test: ## Run tests
	poetry run python -m pytest --cov=data_api_project --cov-report html

.PHONY: update
update: ## Run update poetry
	poetry update

.PHONY: api
start-api: ## Start api
	cd ./cdc_airbyte_pipeline/api/ && gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:5050

.PHONY: build-api
build-api: ## Build API
	cp poetry.lock pyproject.toml ./cdc_airbyte_pipeline/api/ && cd ./cdc_airbyte_pipeline/api/ && docker build . -t loja-fake-api:latest && rm -rf poetry.lock pyproject.toml

.PHONY: start-container-api
start-container-api: ## Start API
	docker run --name loja-fake -p 7990:7990 loja-fake-api

.PHONY: down-container-api
down-container-api: ## Start API
	docker stop loja-fake && docker rm loja-fake

.PHONY: start-superset
start_superset: ##superset
	git clone https://github.com/apache/superset.git && docker-compose -f ./superset/docker-compose-non-dev.yml up -d

.PHONY: stop-superset
stop_superset: ##superset
	docker-compose -f ./superset/docker-compose-non-dev.yml down --remove-orphans && rm -rf ./superset

.PHONY: start-airbyte
start-airbyte: ##airbyte
	git clone https://github.com/airbytehq/airbyte.git && cd airbyte && docker-compose up -d

.PHONY: down-airbyte
down-airbyte: ##airbyte
	docker-compose -f ./airbyte/docker-compose.yaml down --remove-orphans && rm -rf ./airbyte

.PHONY: start-db
start-db: ##postgresql
	docker pull postgres && docker run --name postgres-lucas -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

.PHONY: down-db
down-db: ##postgresql
	docker stop postgres-lucas && docker rm postgres-lucas
