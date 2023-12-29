# Server build docker container
docker build --no-cache -t prj_sem4 .

# Run container
docker run -d -p 8080:5000 prj_sem4

# Docker
docker exec -it b9990a5e821a /bin/bash

# Run Flask
cd app/
flask --app index run --host=0.0.0.0 --port=80