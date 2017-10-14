COMMIT=$(shell git rev-parse --short HEAD)

.PHONY: run
run: migrate
	gunicorn --config gunicorn.conf -b ":8000" application:app

.PHONY: docker-build
docker-build:
	docker build -t mind:$(COMMIT) .
	docker tag mind:$(COMMIT) mind:latest

.PHONY: gke-tag
gke-tag:
	docker tag mind eu.gcr.io/rob-young-digital/mind
	docker tag mind:$(COMMIT) eu.gcr.io/rob-young-digital/mind:$(COMMIT)

.PHONY: gke-push
gke-push:
	gcloud docker -- push eu.gcr.io/rob-young-digital/mind

.PHONY: dev
dev: migrate
	flask run --host 0.0.0.0 --port 8000 --reload --debugger

.PHONY: migrate
migrate:
	flask db upgrade

.PHONY: lint
lint:
	flake8 --exclude ./migrations

.PHONY: test
test: lint
	pytest -vs tests
