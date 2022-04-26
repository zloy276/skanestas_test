build:
	export PYTHONPATH=.
	cat .env.example > .env
	pip install poetry
	poetry shell
	poetry install

migrate:
	export PYTHONPATH=.
	dotenv -f ./.env run alembic revision --autogenerate
	dotenv -f ./.env run alembic upgrade head

run:
	export PYTHONPATH=.
	dotenv -f ./.env run uvicorn ./backend/app/main:create_app --factory --reload --bind 0.0.0.0:8000