.PHONY: freeze install setup-db reset format test coverage docker-build docker-run docker-clean up down

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

docker-run:
	docker build -t school-flask-api .
	docker run -d --name school-flask-api-container -p 5000:5000 school-flask-api

docker-clean:
	docker stop school-flask-api-container || true
	docker rm school-flask-api-container || true
	docker rmi school-flask-api || true

up:
	docker compose up -d

down:
	docker compose down