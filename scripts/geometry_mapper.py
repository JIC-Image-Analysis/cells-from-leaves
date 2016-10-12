"""Module converting points from relative to image geometry.

Imagine cutting a region, e.g. a cell, out of an image.
The region might be scaled up to make it easier to view.
The region might be rotated, anti-clockwise (as in scipy.ndimage.rotate),
to remove chances of bias when looking at polarity.
The user might click on the region and want to know the coordinates in
the original image.

This is possible by converting point to fit into relative coordinates
ranging from -0.5 to 0.5, i.e. origin of region is 0, 0), and
passing the relative point along with the rotation (in degrees) and
the dimensions of the region and the offset to the top left corner
of the region within to original image to the :func:`original_image_point`.

>>> rel_pt = (-0.5, 0)
>>> rot_degrees = 90
>>> region_ydim = 10
>>> region_xdim = 50
>>> y_pos_region_top_left_corner = 3
>>> x_pos_region_top_left_corner = 20
>>> original_image_point(rel_pt,
...                      rot_degrees,
...                      region_ydim,
...                      region_xdim,
...                      y_pos_region_top_left_corner,
...                      x_pos_region_top_left_corner)
...
(8, 70)

"""

import math


def degrees2radians(rotation):
    """Return rotation in radians."""
    return (math.pi * rotation) / 180.


def test_degrees2radians():
    assert degrees2radians(0) == 0
    assert degrees2radians(180) == math.pi


def relative_to_fraction(rel_dim):
    """Return dim in 0 to 1 scale."""
    return rel_dim + 0.5


def test_relative_to_fraction():
    assert relative_to_fraction(-.5) == 0.
    assert relative_to_fraction(.0) == .5
    assert relative_to_fraction(.5) == 1.


def rotate(point, degrees):
    """Rotate point clockwise around origin."""
    y, x = point
    rads = degrees2radians(degrees)
    s = math.sin(rads)
    c = math.cos(rads)
    rot_y = (x * s) + (y * c)
    rot_x = (x * c) - (y * s)
    return rot_y, rot_x


def test_rotate():
    def points_almost_equal(pt1, pt2):
        y1, x1 = pt1
        y2, x2 = pt2
        if y1 + 0.0000000001 < y2:
            return False
        if y1 - 0.0000000001 > y2:
            return False
        if x1 + 0.0000000001 < x2:
            return False
        if x1 - 0.0000000001 > x2:
            return False
        return True
    origin = (0., 0.)
    north = (-0.5, 0.)
    east = (0., 0.5)
    south = (0.5, 0.)
    west = (0., -0.5)
    assert rotate(origin, 90) == origin
    assert points_almost_equal(rotate(north, 90), east)
    assert points_almost_equal(rotate(east, 90), south)
    assert points_almost_equal(rotate(south, 90), west)


def relative_pt_in_region(rel_point, ydim, xdim):
    """Return point in original region's geometry."""
    y, x = rel_point
    y_scale = relative_to_fraction(y)
    x_scale = relative_to_fraction(x)
    region_y = ydim * y_scale
    region_x = xdim * x_scale
    return region_y, region_x


def test_relative_pt_in_region():
    region_pt = relative_pt_in_region((-0.5, -0.5), 10, 20)
    assert region_pt == (0, 0)
    region_pt = relative_pt_in_region((0.5, 0.5), 10, 20)
    assert region_pt == (10, 20)
    region_pt = relative_pt_in_region((0., 0.), 10, 20)
    assert region_pt == (5, 10), region_pt


def region_pt_in_image(region_pt, dy_offset, dx_offset):
    """Return point in original image's geometry."""
    y, x = region_pt
    return y + dy_offset, x + dx_offset


def test_region_pt_in_image():
    assert region_pt_in_image((5, 11), 5, 9) == (10, 20)


def point_as_int(point):
    """Return point as tuple of integers."""
    return tuple([int(round(i, 0)) for i in point])


def test_point_as_int():
    assert point_as_int((4.4, 4.5)) == (4, 5)


def original_image_point(rel_point, rotation, ydim, xdim,
                         dy_offset, dx_offset):
    """Return point in original image's geometry.

    :param rel_point: point in -0.5 to 0.5 geometry
    :param rotation: rotation angle in degrees
    :param ydim: ydim of cropped region from original image
    :param xdim: xdim of cropped region from original image
    :param dy_offset: y coordinate of region top left corner
    :param dx_offset: x coordinate of region top left corner
    :returns: (y, x) tuple
    """
    rotated_point = rotate(rel_point, rotation)
    region_point = relative_pt_in_region(rotated_point, ydim, xdim)
    image_point = region_pt_in_image(region_point, dy_offset, dx_offset)
    return point_as_int(image_point)


def test_original_image_point():
    im_pt = original_image_point((-0.5, 0), 90, 10, 50, 3, 20)
    assert im_pt == (8, 70), im_pt
    im_pt = original_image_point((0, 0.5), 90, 10, 50, 3, 20)
    assert im_pt == (13, 45), im_pt
