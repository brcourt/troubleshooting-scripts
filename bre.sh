#! /bin/bash

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
# BRE is a script that Builds, Runs, and Execs to a container automatically.  #
# This script must be run in a directory containing a Dockerfile. It will     #
# build an image, then run a container based on that image, and then exec     #
# to that container automatically. It always maps 80:80 on the host. If a     #
# container is running that maps port 80, that container will be killed.      #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

set -e

# check if the new container will collide with a currently running container, so it will kill that container
port_collision=$(docker ps | grep "0.0.0.0:80" | awk '{print $1}')
if ! [ -z $port_collision ]
    then
        docker kill $port_collision
fi

# build the docker image, this will not create a tag
docker build .

# Checks the last created image (which will be from the line above) and then run the container
last_image=$(docker images -a --quiet | awk 'NR==1{print $1}')
docker run -d -p 80:80 $last_image

# Take the last run container (which will be from the line above) and then exec into that container
last_container=$(docker ps --latest --quiet)
docker exec -it $last_container bash
