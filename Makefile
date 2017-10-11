
dev: migrate
	flask run --host 0.0.0.0 --port 8000 --reload --debugger

migrate:
	flask db upgrade

lint:
	flake8 --exclude ./migrations
