"""Script for generating annotated leaf."""

import argparse
import os

from jicbioimage.core.io import AutoWrite

from parameters import Parameters
from leaf_annotation import save_annotated_leaf
from tensor_csv import write_csv


__version__ = "0.1.0"


def post_tagging_processing(input_dir, input_image, params):
    ann_cells_dir = os.path.join(input_dir, "annotated-cells")
    save_annotated_leaf(ann_cells_dir,
                        input_image,
                        os.path.join(input_dir, "annotated-leaf.png"),
                        random=False,
                        **params)
    save_annotated_leaf(ann_cells_dir,
                        input_image,
                        os.path.join(input_dir, "annotated-leaf-random.png"),
                        random=True,
                        **params)
    write_csv(ann_cells_dir,
              os.path.join(input_dir, "tensors.csv"),
              random=False)
    write_csv(ann_cells_dir,
              os.path.join(input_dir, "tensors-random.csv"),
              random=True)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", help="Leaf directory")
    parser.add_argument("input_image", help="Input image")
    parser.add_argument("parameters_file", help="Parameters file")
    args = parser.parse_args()

    # Check that the input directory and files exists.
    if not os.path.isdir(args.input_dir):
        parser.error("{} not a directory".format(args.input_dir))
    if not os.path.isfile(args.input_image):
        parser.error("{} not a file".format(args.input_image))
    if not os.path.isfile(args.parameters_file):
        parser.error("{} not a file".format(args.parameters_file))

    # Read in the parameters.
    params = Parameters.from_file(args.parameters_file)

    # Don't write out intermediate images.
    AutoWrite.on = False

    # Run the post tagging processing.
    post_tagging_processing(args.input_dir, args.input_image, params)


if __name__ == "__main__":
    main()
