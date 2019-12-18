FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction

COPY . .

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

