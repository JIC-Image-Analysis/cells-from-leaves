#!/bin/bash

CONTAINER="cells-from-leaves"
touch `pwd`/bash_history
docker run -it --rm -v `pwd`/bash_history:/root/.bash_history -v `pwd`/data:/data:ro -v `pwd`/parameters:/parameters:ro  -v `pwd`/scripts:/scripts:ro -v `pwd`/output:/output $CONTAINER
