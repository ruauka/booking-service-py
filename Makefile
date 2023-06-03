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
 			-e POSTGRES_USER=user \
 			-e POSTGRES_PASSWORD=password \
 			-e POSTGRES_DB=hotels \
 			postgres:latest

pytest_db_stop:
	docker stop pytest_db

test:
	pytest -v -s

#pytest_db:
#	docker-compose -f docker-compose.pytest.yml up -d --remove-orphans
#
#pytest_db_down:
#	docker-compose down
