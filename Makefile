migrate_create:
	alembic init migrations

migrate:
	alembic revision --autogenerate -m "Next migrations"

migrate_up:
	alembic upgrade head

migrate_down:
	alembic downgrade -1
