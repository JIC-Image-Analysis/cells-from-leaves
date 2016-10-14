"""Module for persisting cell data as json."""

from parameters import Parameters

class CellData(Parameters):
    """Class for storing, reading in and writing out cell data."""


def test_celldata_init():
    celldata = CellData(cell_id=1)
    assert celldata["cell_id"] == 1

    celldata = CellData(cell_id=1,
                        rotation=0,
                        ydim=30,
                        xdim=50,
                        dy_offset=100,
                        dx_offset=75)
    assert celldata["cell_id"] == 1
    assert celldata["rotation"] == 0
    assert celldata["ydim"] == 30
    assert celldata["xdim"] == 50
    assert celldata["dy_offset"] == 100
    assert celldata["dx_offset"] == 75
