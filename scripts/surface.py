"""Module for generating surfaces and projecting stacks based on surfaces."""

import numpy as np
from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation


@transformation
def surface_from_stack(stack, **kwargs):
    """Return surface as 2D image where intensity represents z-depth."""
    ydim, xdim, zdim = stack.shape
    cutoff = np.percentile(stack, kwargs["surface_percentile"], axis=2)
    surface = np.zeros((ydim, xdim), dtype=np.uint8)
    for zi in range(0, zdim):
        mask = stack[:, :, zi] > cutoff
        not_done = surface == 0
        mask = mask * not_done
        surface[mask] = zi
    return surface.view(Image)
