#!/bin/bash

CONTAINER="cells-from-leaves"
INPUT_DIR="/usr/users/JIC_a5/olssont/group_data/scicomp/incoming/mansfiec/2017-05-18-analysis-begins/data"
OUTPUT_DIR="/usr/users/JIC_a5/olssont/group_data/scicomp/incoming/mansfiec/2017-05-18-analysis-begins/results"
touch `pwd`/bash_history
docker run -it --rm -v `pwd`/bash_history:/root/.bash_history -v $INPUT_DIR:/data:ro -v `pwd`/parameters:/parameters:ro  -v `pwd`/scripts:/scripts:ro -v $OUTPUT_DIR:/output $CONTAINER
