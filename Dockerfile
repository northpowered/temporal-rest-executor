# syntax=docker/dockerfile:1

FROM python:3.10-slim

LABEL org.opencontainers.image.source="https://github.com/northpowered/temporal-rest-executor"

LABEL version="0.3.0"

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY poetry.lock poetry.lock 

COPY pyproject.toml pyproject.toml

RUN pip install poetry

RUN poetry install --no-root

COPY src/ .

CMD [ "python3", "run.py"]