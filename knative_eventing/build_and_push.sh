#!/bin/bash
cd ../user-service && docker build . -t smixi/user-service:runner -f Dockerfile.runner
docker build . -t smixi/user-service
cd ../mail-service && docker build . -t smixi/mail-service

docker push smixi/mail-service
docker push smixi/user-service
docker push smixi/user-service:runner