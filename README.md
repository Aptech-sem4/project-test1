# Server build docker container
docker build --no-cache -t prj_sem4 .

# Run container
docker run -d --network=host -v /home/is_eman/test/app_test/project-test1:/sites/aptech-s4 prj_sem4

# Docker
docker exec -it container_id /bin/bash

# Run Flask
- cd sources/
- py run.py

# Requirements 
Flask==3.0.0
tensorflow==2.14.0
pillow==8.4.0
