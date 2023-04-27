#!/bin/bash

CONTAINER_NAME="hackergram"

printf "Stopping old image %s...\n" "${CONTAINER_NAME}"
docker stop "${CONTAINER_NAME}"

printf "Removing old image %s...\n" "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

printf "Creating docker image %s...\n" "${CONTAINER_NAME}"
docker build -t ${CONTAINER_NAME} . --no-cache

i_EXIT_CODE=$?
if [ $i_EXIT_CODE -ne 0 ]; then
    printf "Error. Exit code %s\n" ${i_EXIT_CODE}
    exit
fi

docker run -d -p 5000:80 --name ${CONTAINER_NAME} ${CONTAINER_NAME}

echo "Container is running!"
