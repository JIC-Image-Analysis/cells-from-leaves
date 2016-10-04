"""Module for generating surfaces and projecting stacks based on surfaces."""

import numpy as np
from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation


@transformation
def surface_from_stack(stack, **kwargs):
    """Return surface as 2D image where intensity represents z-depth."""
    ydim, xdim, zdim = stack.shape
    cutoff = np.percentile(stack, 95, axis=2)
    surface = np.zeros((ydim, xdim), dtype=np.uint8)
    for zi in range(0, zdim):
        mask = stack[:, :, zi] > cutoff
        not_done = surface == 0
        mask = mask * not_done
        surface[mask] = zi
    return surface.view(Image)


@transformation
def mean_project(stack, surface, zabove, zbelow):
    """Return mean intensity from stack based on surface."""
    projection = np.zeros(surface.shape, dtype=np.uint8)
    xdim, ydim, zdim = stack.shape
    for x in range(xdim):
        for y in range(ydim):
            z_index = surface[x, y]
            z_min = z_index - zabove
            z_min = max(0, z_min)
            z_max = z_index + 1 + zbelow
            z_max = min(z_max, zdim)
            value = np.mean(stack[x, y, z_min:z_max])
            projection[x, y] = value
    return projection.view(Image)


def test_mean_project():
    stack = np.ones((1, 1, 10))
    for i in range(10):
        stack[:, :, i] = stack[:, :, i] * i
    surface = np.ones((1,1)) * 5
    assert np.array_equal(mean_project(stack, surface, 0, 0),
                          [[5]])
    assert np.array_equal(mean_project(stack, surface, 2, 0),
                          [[4]])
    assert np.array_equal(mean_project(stack, surface, 0, 2),
                          [[6]])
    assert np.array_equal(mean_project(stack, surface, 7, 0),
                          [[2]])
    assert np.array_equal(mean_project(stack, surface, -1, 7),
                          [[7]]), mean_project(stack, surface, -1, 7)
