.PHONY: freeze install setup-db reset format test coverage up down

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

setup-db:
	python3 db/init_db.py && python3 db/populate_db.py

reset:
	rm db/school.db && make setup-db

format:
	ruff format run.py db/ tests/ app/

test:
	pytest --maxfail=1 -q

coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing --maxfail=1 -q

up:
	docker compose up -d

# make down  -> dont remove volume
# make down V=1 -> remove volume
down:
	docker compose down$(if $(V), -v)