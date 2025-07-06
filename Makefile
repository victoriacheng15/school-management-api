.PHONY: freeze install init_db populate_db format docker-build docker-run docker-clean

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

setup-db:
	python3 db/init_db.py && python3 db/populate_db.py

format:
	ruff format run.py db/ tests/ app/

docker-run:
	docker build -t school-flask-api .
	docker run -d --name school-flask-api-container -p 5000:5000 school-flask-api

docker-clean:
	docker stop school-flask-api-container || true
	docker rm school-flask-api-container || true
	docker rmi school-flask-api || true