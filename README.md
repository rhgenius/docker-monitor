# docker-monitoring

## create docker image

docker build --tag docker-monitor:1.0.0 --platform linux/amd64 --file Dockerfile .

## compress docker image

docker save docker-monitor:1.0.0 | gzip > docker-monitor_1.0.0.tar.gz

## deploy on instance

docker load -i docker-monitor.tar.gz
docker tag docker-monitor:1.0.0 docker-monitor:latest
sudo mkdir /data/container-info
sudo chown kbij:kbij /data/container-info
cd /data/container-info/
vim docker-compose.yml

    version: '3'

    services:
    docker-monitor:
        image: docker-monitor:latest
        container_name: docker-monitor
        ports:
        - "8088:8000"
        volumes:
        - /var/run/docker.sock:/var/run/docker.sock
        restart: unless-stopped
        networks:
        - monitoring-network

    networks:
    monitoring-network:
        driver: bridge

docker compose up -d
