"""Module for segmenting leaves into cells."""

import scipy.ndimage as nd
import skimage.filters

from jicbioimage.core.transform import transformation
from jicbioimage.transform import (
    invert,
    remove_small_objects,
    erode_binary,
    dilate_binary,
)
from jicbioimage.segment import connected_components, watershed_with_seeds

from surface import mean_project


@transformation
def percentile_filter(stack, p, size):
    return nd.percentile_filter(stack, p, size).view(stack.__class__)


@transformation
def threshold_adaptive_median(image, block_size):
    return skimage.filters.threshold_adaptive(image, block_size=block_size)


def segment_cells(wall_stack, surface, **kwargs):
    """Return segmented cells as SegmentedImage."""
    wall_signal = percentile_filter(wall_stack,
                                    kwargs["wall_percentile_filter_percentile"],
                                    kwargs["wall_percentile_filter_size"])
    wall_projection = mean_project(wall_signal,
                                   surface,
                                   zabove=kwargs["wall_zabove"],
                                   zbelow=kwargs["wall_zbelow"])

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
