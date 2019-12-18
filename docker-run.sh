docker build -t fastapi-skeleton:latest .
docker run --rm -p 8000:8000 --name fastapi fastapi-skeleton:latest