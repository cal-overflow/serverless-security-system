#!/bin/bash

# run the program with the following arguments (or none to use default values)
# $ ./client.sh <image version> <env file>
#
# The default values are
# $ ./client.sh latest .env

if [ $# -eq 0 ]; then
  DOCKER_IMAGE="caloverflow/security-system-client:latest"
else
  DOCKER_IMAGE="caloverflow/security-system-client:$1"
fi

ENVIRONMENT_VARIABLE_FILE=".env"

if [ $# -ge 2 ]; then
  ENVIRONMENT_VARIABLE_FILE="$2"
fi

docker run --env-file=$ENVIRONMENT_VARIABLE_FILE -it --privileged --device="/dev/video0:/dev/video0" -v $(pwd):/app --restart=unless-stopped $DOCKER_IMAGE 

