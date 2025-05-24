#!/bin/bash

docker rm -f account

docker run -d -p 7777:7777 --name account --restart unless-stopped account
