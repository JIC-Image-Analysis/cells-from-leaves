"""Module for creating projections from stacks and surfaces."""

import numpy as np
import scipy.ndimage as nd

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation


def _project(stack, surface, zabove, zbelow, proj_method):
    projection = np.zeros(surface.shape, dtype=np.uint8)
    xdim, ydim, zdim = stack.shape
    for x in range(xdim):
        for y in range(ydim):
            z_index = surface[x, y]
            z_min = z_index - zabove
            z_min = max(0, z_min)
            if z_min >= zdim:
                z_min = zdim - 1
            z_max = z_index + 1 + zbelow
            z_max = min(z_max, zdim)
            if z_max <= z_min:
                z_max = z_min + 1
            value = proj_method(stack[x, y, z_min:z_max])
            projection[x, y] = value
    return projection.view(Image)


@transformation
def mean_project(stack, surface, zabove, zbelow):
    """Return mean intensity from stack based on surface."""
    return _project(stack, surface, zabove, zbelow, np.mean)


@transformation
def max_project(stack, surface, zabove, zbelow):
    """Return max intensity from stack based on surface."""
    return _project(stack, surface, zabove, zbelow, np.max)


@transformation
def percentile_filter(stack, p, size):
    return nd.percentile_filter(stack, p, size).view(stack.__class__)


@transformation
def project_wall(wall_stack, surface, **kwargs):
    """Return wall signal projected from surface."""
    wall_signal = percentile_filter(wall_stack,
                                    kwargs["wall_percentile_filter_percentile"],
                                    kwargs["wall_percentile_filter_size"])
    return mean_project(wall_signal,
                        surface,
                        zabove=kwargs["wall_zabove"],
                        zbelow=kwargs["wall_zbelow"])


@transformation
def project_marker(marker_stack, surface, **kwargs):
    """Return marker signal projected from surface."""
    marker_stack = percentile_filter(marker_stack,
                                     kwargs["marker_percentile_filter_percentile"],
                                     kwargs["marker_percentile_filter_size"])
    return max_project(marker_stack,
                       surface,
                       zabove=kwargs["marker_zabove"],
                       zbelow=kwargs["marker_zbelow"])


def test_mean_project():
    stack = np.ones((1, 1, 10))
    for i in range(10):
        stack[:, :, i] = stack[:, :, i] * i
    surface = np.ones((1, 1)) * 5
    assert np.array_equal(mean_project(stack, surface, 0, 0),
                          [[5]])
    assert np.array_equal(mean_project(stack, surface, 2, 0),
                          [[4]])
    assert np.array_equal(mean_project(stack, surface, 0, 2),
                          [[6]])
    assert np.array_equal(mean_project(stack, surface, 7, 0),
                          [[2]])
    assert np.array_equal(mean_project(stack, surface, -1, 7),
                          [[7]])
    assert np.array_equal(mean_project(stack, surface, -6, 7),
                          [[9]])
    assert np.array_equal(mean_project(stack, surface, 7, -6),
                          [[0]])
