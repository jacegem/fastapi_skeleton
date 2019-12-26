#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
FROM python:3.7

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /app

RUN pip install poetry
RUN poetry config --local virtualenvs.in-project true
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction

COPY . .

EXPOSE 8080
#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080

