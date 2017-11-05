COMMIT=$(shell git rev-parse --short HEAD)

.PHONY: run
run: migrate
	gunicorn --config gunicorn.py -b ":8000" application:app

.PHONY: docker-build
docker-build:
	docker build -t mind:$(COMMIT) .
	docker tag mind:$(COMMIT) mind:latest
	docker build -t mind-cronjob:$(COMMIT) cronjob
	docker tag mind-cronjob:$(COMMIT) mind-cronjob:latest

.PHONY: gke-tag
gke-tag: docker-build
	docker tag mind eu.gcr.io/rob-young-digital/mind
	docker tag mind:$(COMMIT) eu.gcr.io/rob-young-digital/mind:$(COMMIT)
	docker tag mind-cronjob eu.gcr.io/rob-young-digital/mind-cronjob
	docker tag mind-cronjob:$(COMMIT) eu.gcr.io/rob-young-digital/mind-cronjob:$(COMMIT)

.PHONY: gke-push
gke-push: gke-tag
	gcloud docker -- push eu.gcr.io/rob-young-digital/mind
	gcloud docker -- push eu.gcr.io/rob-young-digital/mind-cronjob

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
