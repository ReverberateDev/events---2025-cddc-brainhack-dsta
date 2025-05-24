#!/bin/bash

docker rm -f account
docker rmi -f account

docker build -t account .
docker run -d --name account account tail -f /dev/null

docker cp account:/jail/account ./account

docker rm -f account