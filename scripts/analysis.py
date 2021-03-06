"""cells-from-leaves analysis."""

import os
import logging
import argparse
import json

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite
from jicbioimage.segment import Region

from utils import get_microscopy_collection
from parameters import Parameters
from surface import surface_from_stack
from segment import segment_cells
from projection import (
    project_wall,
    project_marker,
)
from annotation import write_cell_views

__version__ = "0.5.0"

AutoName.prefix_format = "{:03d}_"


@transformation
def identity(image):
    """Return the image as is."""
    return image


def save_cells(cells, wall_projection, marker_projection, output_directory):
    d = os.path.join(output_directory, "annotated-cells")
    if not os.path.isdir(d):
        os.mkdir(d)
    for i in cells.identifiers:
        region = cells.region_by_identifier(i)
        celldata = dict(cell_id=i, centroid=list(region.centroid), area=region.area)
        fpath_prefix = os.path.join(d, "cell-{:05d}".format(i))
        write_cell_views(fpath_prefix, wall_projection, marker_projection, region, celldata)
        with open(fpath_prefix + ".json", "w") as fh:
            json.dump(celldata, fh)


def analyse_file(fpath, mask, output_directory, **kwargs):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))

    microscopy_collection = get_microscopy_collection(fpath)

    wall_stack = microscopy_collection.zstack(c=kwargs["wall_channel"])
    wall_stack = identity(wall_stack)
    surface = surface_from_stack(wall_stack, **kwargs)
    wall_projection = project_wall(wall_stack, surface, **kwargs)

    cells = segment_cells(wall_projection, surface, mask, **kwargs)

    marker_stack = microscopy_collection.zstack(c=kwargs["marker_channel"])
    marker_stack = identity(marker_stack)
    marker_projection = project_marker(marker_stack, surface, **kwargs)

    save_cells(cells, wall_projection, marker_projection, output_directory)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("mask_file", help="Mask file")
    parser.add_argument("parameters_file", help="Parameters file")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Write out intermediate images")
    args = parser.parse_args()

    # Check that the input file exists.
    if not os.path.isfile(args.input_file):
        parser.error("{} not a file".format(args.input_file))
    if not os.path.isfile(args.parameters_file):
        parser.error("{} not a file".format(args.parameters_file))

    # Read in the parameters.
    params = Parameters.from_file(args.parameters_file)

    # Create the output directory if it does not exist.
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    AutoName.directory = args.output_dir

    # Only write out intermediate images in debug mode.
    if not args.debug:
        AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = os.path.join(args.output_dir, log_fname)
    logging_level = logging.INFO
    if args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))
    logging.info("Parameters: {}".format(params))

    # Run the analysis.
    mask_im = Image.from_file(args.mask_file)
    mask = Region.select_from_array(mask_im, 0)
    identity(mask)
    analyse_file(args.input_file, mask, args.output_dir, **params)

if __name__ == "__main__":
    main()
