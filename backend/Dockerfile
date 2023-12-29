FROM python:3.12-bookworm as builder

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY switchManagerAPI/pyproject.toml switchManagerAPI/poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.12-slim-bookworm as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY switchManagerAPI ./switchManagerAPI

WORKDIR /switchManagerAPI

RUN pip3 install faker==20.1.0

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "switchmanagerapi.main:app"]
