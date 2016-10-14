"""Script for generating annotated leaf."""

import argparse
import os
import logging
import json

from jicbioimage.core.io import AutoWrite
from jicbioimage.illustrate import AnnotatedImage

from utils import get_microscopy_collection
from parameters import Parameters
from surface import surface_from_stack
from projection import (
    project_wall,
    project_marker,
)
from geometry_mapper import original_image_point
from analysis import remove_noise


__version__ = "0.1.0"


def save_annotated_leaf(input_image, output_file, **kwargs):
    """Write out annotated leaf image."""
    microscopy_collection = get_microscopy_collection(input_image)

    wall_stack = microscopy_collection.zstack(c=kwargs["wall_channel"])
    surface = surface_from_stack(wall_stack, **kwargs)
    wall_projection = project_wall(wall_stack, surface, **kwargs)

    marker_stack = microscopy_collection.zstack(c=kwargs["marker_channel"])
    # Refactor with analysis script to ensure always in sync.
    marker_projection = project_marker(marker_stack, surface, **kwargs)
    marker_projection = remove_noise(marker_projection, kwargs["marker_min_intensity"])

    wall_ann = AnnotatedImage.from_grayscale(wall_projection, (1, 0, 0))
    marker_ann = AnnotatedImage.from_grayscale(marker_projection, (0, 1, 0))
    ann = wall_ann + marker_ann

    with open("output/cell-00010.json") as fh:
        celldata = json.load(fh)

    frac_pt = celldata["clicked_y"], celldata["clicked_x"]
    rel_pt = tuple([i - 0.5 for i in frac_pt])

    marker_pt = original_image_point(rel_point=rel_pt,
                                     rotation=celldata["rotation"],
                                     ydim=celldata["ydim"],
                                     xdim=celldata["xdim"],
                                     dy_offset=celldata["dy_offset"],
                                     dx_offset=celldata["dx_offset"])
    print(marker_pt)

    ann.draw_line(marker_pt, celldata["centroid"], (255, 255, 255))

    with open(output_file, "wb") as fh:
        fh.write(ann.png())

def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_image", help="Input image")
    parser.add_argument("parameters_file", help="Parameters file")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    # Check that the input file exists.
    if not os.path.isfile(args.input_image):
        parser.error("{} not a file".format(args.input_image))
    if not os.path.isfile(args.parameters_file):
        parser.error("{} not a file".format(args.parameters_file))

    # Read in the parameters.
    params = Parameters.from_file(args.parameters_file)

    # Don't write out intermediate images.
    AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = log_fname
    logging_level = logging.INFO
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))
    logging.info("Parameters: {}".format(params))

    # Run the analysis.
    save_annotated_leaf(args.input_image, args.output_file, **params)


if __name__ == "__main__":
    main()
