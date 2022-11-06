#!/bin/bash

# run the program with the following arguments (or none to use default values)
# $ ./client.sh <image version> <clip length (in seconds)>
#
# The default values are
# $ ./client.sh latest 30

if [ $# -eq 0 ]; then
  DOCKER_IMAGE="caloverflow/security-system-client:latest"
else
  DOCKER_IMAGE="caloverflow/security-system-client:$1"
fi

ENVIRONMENT_VARIABLE_ARGUMENTS=""

if [ $# -ge 2 ]; then
  ENVIRONMENT_VARIABLE_ARGUMENTS="$ENVIRONMENT_VARIABLE_ARGUMENTS -e CLIP_LENGTH=$2"
fi

docker run $ENVIRONMENT_VARIABLE_ARGUMENTS -it --privileged --device="/dev/video0:/dev/video0" -v $(pwd):/app $DOCKER_IMAGE 

