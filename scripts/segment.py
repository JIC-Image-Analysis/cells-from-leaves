"""Module for segmenting leaves into cells."""

from surface import mean_project

def segment_cells(wall_stack, surface, **kwargs):
    """Return segmented cells as SegmentedImage."""
    wall_projection = mean_project(wall_stack,
                                   surface,
                                   zabove=kwargs["wall_zabove"],
                                   zbelow=kwargs["wall_zbelow"])
