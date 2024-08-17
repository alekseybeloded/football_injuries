FROM python:3.11.6-alpine3.18

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install

COPY . .
