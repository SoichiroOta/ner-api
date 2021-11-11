build:
	docker-compose build

update:
	docker-compose run --rm demo-app poetry update

install:
	docker-compose run --rm demo-app poetry install

up:
	docker-compose up

up-build:
	docker-compose up --build

down:
	docker-compose down

test:
	make install
	docker-compose run --rm demo-app poetry run pytest --cov=app tests

lint:
	make install
	docker-compose run --rm demo-app poetry run flake8 tests
	docker-compose run --rm demo-app poetry run isort --check --diff tests app
	docker-compose run --rm demo-app poetry run black --check tests app
	docker-compose run --rm demo-app poetry run mypy tests app

format:
	make install
	docker-compose run --rm demo-app poetry run isort tests app
	docker-compose run --rm demo-app poetry run black tests app
