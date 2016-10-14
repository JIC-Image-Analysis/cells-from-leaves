"""Module for generating annotated cells."""

import os
import random

import numpy as np
import scipy.misc
import scipy.ndimage

from jicbioimage.illustrate import AnnotatedImage


def post_process_annotation(ann, dilated_region, celldata, crop=True, rotate=True,
                            enlarge=True, padding=True):

    if crop:
        yis, xis = dilated_region.index_arrays
        ymin, ymax = np.min(yis), np.max(yis)
        xmin, xmax = np.min(xis), np.max(xis)
        ann = ann[ymin:ymax,
                  xmin:xmax]
        celldata["dy_offset"] = ymin
        celldata["dx_offset"] = xmin

    if padding:
        ydim, xdim, zdim = ann.shape
        p = 25
        pydim = ydim + p + p
        pxdim = xdim + p + p
        padded = AnnotatedImage.blank_canvas(width=pxdim, height=pydim)
        padded[p:ydim+p, p:xdim+p] = ann
        ann = padded
        celldata["dy_offset"] -= p
        celldata["dx_offset"] -= p
        celldata["ydim"] = pydim
        celldata["xdim"] = pxdim

    if enlarge:
        ann = scipy.misc.imresize(ann, 3.0, "nearest").view(AnnotatedImage)

    if rotate:
        rotation = random.randrange(0, 360)
        ann = scipy.ndimage.rotate(ann, rotation, order=0).view(AnnotatedImage)
        celldata["rotation"] = rotation

    return ann


def write_cell_views(fpath_prefix, wall_projection, marker_projection, region, celldata,
                     crop=True, rotate=True, enlarge=True, padding=True):
    wall_ann = AnnotatedImage.from_grayscale(wall_projection, (1, 0, 0))
    marker_ann = AnnotatedImage.from_grayscale(marker_projection, (0, 1, 0))
    ann = wall_ann + marker_ann
    ann.mask_region(region.border, (200, 200, 200))
    dilated_region = region.dilate(20)
    wall_ann[np.logical_not(dilated_region)] = (0, 0, 0)
    marker_ann[np.logical_not(dilated_region)] = (0, 0, 0)
    ann[np.logical_not(dilated_region)] = (0, 0, 0)

    for suffix, annotation in [("-wall", wall_ann),
                               ("-marker", marker_ann),
                               ("-combined", ann)]:
        fpath = fpath_prefix + suffix + ".png"
        annotation = post_process_annotation(annotation, dilated_region, celldata, crop,
                                             rotate, enlarge, padding)

        scipy.misc.imsave(fpath, annotation)
