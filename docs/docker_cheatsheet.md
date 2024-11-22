#### Installation guide:
https://docs.docker.com/desktop/install/

#### Build&run container manually
##### Backend
sudo docker build -t backend ./
sudo docker run -e HOST=0.0.0.0 -e PORT=8000 -it -p 8000:8000 backend
##### Frontend
sudo docker build -t frontend ./frontend/my_first_app
sudo docker run -it --rm -p 8080:8080 frontend

#### Build&run container using docker compose
sudo docker compose build
sudo docker compose up
