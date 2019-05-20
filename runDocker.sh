#!/bin/bash

if [ -f .apikeys ]; then
    source .apikeys
fi
DOCKER_NAME="event_stats"
echo "Running nginx on port 9000: http://localhost"
docker build -t $DOCKER_NAME:latest . && docker run --rm --name $DOCKER_NAME -p 9000:9000 -e eventbrite_key=$eventbrite_key $DOCKER_NAME:latest
