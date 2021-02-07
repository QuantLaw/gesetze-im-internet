#!/bin/bash

docker build . --tag scraper
docker stack deploy gii_scraper -c docker-compose.yml
