"""Module for segmenting leaves into cells."""

import skimage.filters

from jicbioimage.core.transform import transformation
from jicbioimage.transform import (
    invert,
    remove_small_objects,
    erode_binary,
    dilate_binary,
)
from jicbioimage.segment import connected_components, watershed_with_seeds


@transformation
def threshold_adaptive_median(image, block_size):
    return skimage.filters.threshold_adaptive(image, block_size=block_size)


def segment_cells(wall_projection, surface, **kwargs):
    """Return segmented cells as SegmentedImage."""

    seeds = threshold_adaptive_median(wall_projection,
                                      block_size=kwargs["wall_threshold_adaptive_block_size"])
    seeds = remove_small_objects(seeds,
                                 min_size=kwargs["wall_remove_small_objects_min_size"])
    seeds = invert(seeds)
    seeds = remove_small_objects(seeds,
                                 min_size=kwargs["wall_remove_small_objects_min_size"])
    seeds = connected_components(seeds,
                                 connectivity=1,
                                 background=0)

    segmentation = watershed_with_seeds(-wall_projection,
                                        seeds=seeds)
    return segmentation
