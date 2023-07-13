# Booking service

[![build](https://github.com/ruauka/booking-service-py/actions/workflows/pipeline.yml/badge.svg)](https://github.com/ruauka/booking-service-py/actions/workflows/pipeline.yml)

## Overview
Booking hotels pet-project service.

## Content
- [Description](#description)
  - [Router](#router)
  - [Database](#database)
  - [Entities](#entities)
  - [Auth](#auth)
  - [Cache](#cache)
  - [Background-tasks](#background-tasks)
      - [Celery](#celery)
      - [Flower](#flower)
  - [Logging](#logging)
  - [Admin-panel](#admin-panel)
  - [Monitoring](#monitoring)

### Description
The service allows:
- CRUD users, admins, hotels, rooms, bookings
- notify the customer about the booking by Email
- manage booking orders using Admin Panel

### Router
It is based on the Fastapi framework and Gunicorn as WSGI server.
Pydantic validation.

Lib - https://fastapi.tiangolo.com/

### Database
PostgreSQL is used as the database. All interactions with the database are executed with ORM sqlalchemy.

Lib - https://www.sqlalchemy.org/

### Entities
<p align="left">
    <img src="assets/er.png" width="700">
</p>

### Auth
Authorization using a JWT is applied.
The user can have an administrator role, which gives the opportunity to edit entities.

Lib - https://pypi.org/project/python-jose/

### Cache
`Redis` is used for caching:
- To cache heavy requests: Getting a list of hotels according to the specified parameters
- For background tasks

Lib - https://pypi.org/project/fastapi-cache2/

### Background tasks
### Celery
Celery is used to execute a background task: send an email notification to the client after booking a room.

Lib - https://pypi.org/project/celery/

### Flower
Flower is used for administration of background tasks.
<p align="left">
    <img src="assets/flower.png" width="700">
</p>


Lib - https://pypi.org/project/flower/

### Logging
Logger can be configured by log-levels:
 - DEBUG
 - INFO
 - WARNING
 - ERROR
 - CRITICAL

Logs are output to the console.

Lib - https://pypi.org/project/python-json-logger/

### Admin-panel
Admin-panel is used for database administration.
Only for a user with the `admin` role.
<p align="left">
    <img src="assets/admin_panel.png" width="700">
</p>

Lib - https://aminalaee.dev/sqladmin

### Monitoring
To monitor the operation of the service are used `Prometheus` and `Grafana`.
<p align="left">
    <img src="assets/dashboard.png" width="700">
</p>

Lib - https://pypi.org/project/prometheus-fastapi-instrumentator/


### FOO
Grafana with pre-configured dashboards available at the link: 
http://localhost/grafana/d/_eX4mpl312/hotels-booking?orgId=1&refresh=5s

Available at link - http://localhost/flower/
Available at link - `http://localhost/admin`