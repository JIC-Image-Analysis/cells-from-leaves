# cells-from-leaves

## Introduction

This repository contains code to aid the annotation of cells in leafs with
vectors from the centroid to a marker in the cell membrane.

The code segments leafs into cells, producing a number of cell images to check
the quality of the segmentation and for identifying the marker of interest.

In order to make the analysis less biased the orientation of cell images are
randomly rotated by 0, 90, 270 degrees. This, along with the fact that the
cell images are cropped from the original leaf image, obfuscates the direction
of the vector with regards to the context of the whole leaf.

The centroid of the cells are determined programatically from the segmentation
and the user can use the 
[cells-from-leaves-tagger](https://github.com/JIC-Image-Analysis/cells-from-leaves-tagger)
to manually annotate the location of the marker of interest in the cell membrane.
The manual step is also used to validate the correctness of the cell segmentation.

After manually annotating the segmented cells there is a post processing step for
converting the annotations into a CSV file for further analysis.


## Technology dependencies

This image analysis project has been setup to take advantage of a technology
known as Docker.

This means that you will need to:

1. Download and install the [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
2. Build a docker image

Before you can run the image analysis in a docker container.


## Build a Docker image

Before you can run your analysis you need to build your docker image.  Once you
have built the docker image you should not need to do this step again.

A docker image is basically a binary blob that contains all the dependencies
required for the analysis scripts. In other words the docker image has got no
relation to the types of images that we want to analyse, it is simply a
technology that we use to make it easier to run the analysis scripts.

```
$ cd docker
$ bash build_docker_image.sh
$ cd ..
```

## Run the image analysis in a Docker container

The image analysis will be run in a Docker container.  The script
``run_docker_container.sh`` will drop you into an interactive Docker session.

```
$ bash run_docker_container.sh
[root@048bd4bd961c /]#
```

Now you can run the image analysis. Initially this will involve several rounds of
finding suitable parameters.

For this specific data analysis the parameters found have been saved in the
``parameters`` directory.

Below is an example command.

```
[root@048bd4bd961c /]# python scripts/analysis.py --debug data/ output/
python scripts/analysis.py data/leaf.tif data/mask.tif parameters/params.yml output/ --debug
```

## Post processing: manual point picking

Post process the data in the ``output/annotated-cells`` directory using
the [cells-from-leaves-tagger](https://github.com/JIC-Image-Analysis/cells-from-leaves-tagger).


## Post processing: generate summary data

Run the ``scripts/post_tagging_processing.py`` script.


## Post processing: generate figures

Figures for the paper were generated using the Matlab scripts stored in the
``matlab_scripts`` directory.
