"""Generate tensor csv file."""

import argparse
import os
import json

from geometry_mapper import original_image_point


def write_csv(input_dir, output_file):
    """Write csv file."""
    csv_lines = ["id,mx,my,cx,cy", ]
    json_fpaths = [os.path.join(input_dir, f)
                   for f in os.listdir(input_dir)
                   if f.endswith(".json")]

    y_key = "normalised_marker_y_coord"
    x_key = "normalised_marker_x_coord"
    identifier = 1
    for fpath in json_fpaths:
        with open(fpath) as fh:
            celldata = json.load(fh)

        if y_key not in celldata:
            continue
        if x_key not in celldata:
            continue
        print(fpath)
        frac_pt = celldata[y_key], celldata[x_key]
        rel_pt = tuple([i - 0.5 for i in frac_pt])

        rotation = celldata["rotation"]
        marker_pt = original_image_point(rel_point=rel_pt,
                                         rotation=rotation,
                                         ydim=celldata["ydim"],
                                         xdim=celldata["xdim"],
                                         dy_offset=celldata["dy_offset"],
                                         dx_offset=celldata["dx_offset"])
        my, mx = marker_pt
        cy, cx = celldata["centroid"]
        csv_lines.append("{},{},{},{},{}".format(identifier, mx, my, cx, cy))
        identifier += 1

    with open(output_file, "w") as fh:
        fh.write("\n".join(csv_lines))


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", help="Input directory (with json files)")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    # Check that the input directory and files exists.
    if not os.path.isdir(args.input_dir):
        parser.error("{} not a directory".format(args.input_dir))

    # Run the analysis.
    write_csv(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
