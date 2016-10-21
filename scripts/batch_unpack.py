"""Script to unpack all images; to make the analysis scripts run faster."""

import os
import argparse
from time import time

from utils import get_microscopy_collection

def unpack_all(input_dir):
    for fname in os.listdir(input_dir):
        fpath = os.path.join(input_dir, fname)
        print("Processing {}...".format(fpath))
        start = time()
        mc = get_microscopy_collection(fpath)
        end = time()
        print("time elapsed {} seconds.".format(end-start))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", help="Input directory")
    args = parser.parse_args()
    if not os.path.isdir(args.input_dir):
        parser.error("{} not a directory".format(args.input_dir))
    unpack_all(args.input_dir)
