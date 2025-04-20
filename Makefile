.PHONY: freeze init_db populate_db format

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

init_db:
	python3 db/init_db.py

populate_db:
	python3 db/populate_db.py

format:
	ruff format app.py db/