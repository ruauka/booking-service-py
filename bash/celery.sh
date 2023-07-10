#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=app.tasks.engine:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.engine:celery flower
elif [[ "${1}" == "flower_nginx" ]]; then
    celery --app=app.tasks.engine:celery flower --url_prefix=/flower
fi