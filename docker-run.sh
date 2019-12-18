docker build -t fastapi .
docker run --rm -p 8000:8000 --name fastapi fastapi