#!/bin/bash

IMAGE_NAME="cells-from-leaves"

cp ../requirements.txt $IMAGE_NAME
cd $IMAGE_NAME
docker build --no-cache -t $IMAGE_NAME .
docker run --rm $IMAGE_NAME pip freeze > requirements.txt
mv requirements.txt ../..
cd ../
