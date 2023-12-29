# Server build docker container
docker build --no-cache -t prj_sem4 .

# Run container
docker run -d -p 80:5000 prj_sem4

# Docker
docker exec -it aec506454e3e /bin/bash

# Run Flask
cd app/
flask --app index run --host=0.0.0.0 --port=80