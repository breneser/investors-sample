FROM python:3.13-slim

# This is a quick Docker file that is not production quality
# TODO: A layered build that could build dev layer for building and testing
# and final production layer without any test/dev dependencies would be ideal.

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "fastapi","dev", "main.py"]
