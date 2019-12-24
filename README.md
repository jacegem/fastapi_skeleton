# fastapi-skeleton

## 로컬 실행

```shell
pip install poetry
poetry config settings.virtualenvs.create false
poetry install
poetry shell
uvicorn app.main:app --reload
```

## docker 실행

```shell
chmod u+x docker-run.sh
./docker-run.sh
```

## 출처

- https://fastapi.tiangolo.com/tutorial/first-steps/
- https://github.com/tiangolo/full-stack-fastapi-couchbase/
- https://github.com/tiangolo/full-stack-fastapi-postgresql
- https://github.com/markqiu/fastapi-mongodb-realworld-example-app/

