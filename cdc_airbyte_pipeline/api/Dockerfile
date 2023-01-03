# syntax=docker/dockerfile:1

FROM python:3.9.15-slim-buster

ENV POETRY_VERSION=1.2.2 \
  PORT=9090

RUN apt-get update && apt-get install

RUN apt-get update && \
    apt-get install -y libpq-dev gcc dos2unix && \
    apt-get install -y python3-psycopg2 && \
    apt-get clean

RUN python -m pip install --upgrade pip
RUN python -m pip install "psycopg2==2.8.6"
# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Copy our Flask app to the Docker image
COPY app.py /code/
COPY . /code/
CMD ["python3", "app.py"]
