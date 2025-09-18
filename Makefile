.PHONY: freeze install format format-md test coverage up down single multi

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

format:
	ruff format run.py db/ tests/ app/

format-md:
	npx markdownlint-cli '**/*.md' --fix

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

# for testing the time it takes to build each Dockerfile
single:
	docker build --network=host -f Dockerfile -t single-api .

multi:
	docker build --network=host -f Dockerfile.multi-stage -t multi-api .