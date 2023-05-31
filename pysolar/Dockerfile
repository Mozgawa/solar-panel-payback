FROM python:3.10.8-slim-buster

ENV PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true \
    PYTHONPATH=${PYTHONPATH}:${PWD}

WORKDIR /app

COPY /pysolar pysolar
COPY pyproject.toml README.md ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD ["poetry", "run", "uvicorn", "pysolar.server:app", "--host", "0.0.0.0"]
