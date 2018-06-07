#!/bin/bash

echo "Running on port 80"
docker build --rm -t nginx:latest . && docker run --rm -ti -p 80:80 --name nginx nginx:latest
