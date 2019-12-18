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


