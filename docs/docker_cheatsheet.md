#### Installation guide:
https://docs.docker.com/desktop/install/

#### Build&run container manually
sudo docker build -t cognitive_image ./
sudo docker run -e HOST=0.0.0.0 -e PORT=8000 -it -p 8000:8000 cognitive_image

#### Build&run container using docker compose
sudo docker compose build
sudo docker compose up
