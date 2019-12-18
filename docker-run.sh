docker build -t fastapi-skeleton:latest .
docker run --rm -p 8080:8080 --name fastapi-skeleton fastapi-skeleton:latest