.PHONY: freeze init_db populate_db format

freeze:
	pip freeze > requirements.txt

init:
	pip install -r requirements.txt

init_db:
	python3 db/init_db.py

format:
	ruff format app.py db/