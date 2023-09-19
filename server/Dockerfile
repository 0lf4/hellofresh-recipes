FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction

COPY . /app/server

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
