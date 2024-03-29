migrate_create:
	alembic init migrations

migrate:
	alembic revision --autogenerate -m "Next migrations"

migrate_up:
	alembic upgrade head

migrate_down:
	alembic downgrade -1

celery:
	celery -A app.tasks.engine:celery worker --loglevel=INFO

flower:
	celery -A app.tasks.engine:celery flower

pytest_db_up:
	@docker run -d --rm \
			--name=pytest_db \
 			-p 5432:5432 \
 			-e POSTGRES_USER=test \
 			-e POSTGRES_PASSWORD=test \
 			-e POSTGRES_DB=test \
 			postgres:latest

pytest_db_stop:
	docker stop pytest_db

test:
	@pytest -v -s

test_cov:
	pytest -v -s --cov=app --cov-report=html && open htmlcov/index.html
	#pip install gevent

black:
	black app --diff --color

lint:
	@flake8 app --count --statistics

isort:
	isort .

docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_dev_up:
	docker-compose -f docker-compose.dev.yml up -d --remove-orphans

ip:
	ipconfig getifaddr en0

check:
	@coverage run -m pytest -v -s && coverage report && flake8 app --count --statistics