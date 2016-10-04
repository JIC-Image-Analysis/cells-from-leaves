"""Module to make it easier to work with lots of parameters."""

import yaml


class Parameters(dict):
    """Class for storing, reading in and writing out parameters."""

    @classmethod
    def from_yaml(cls, string):
        """Return Parameter instance from yaml string."""
        p = cls()
        d = yaml.load(string)
        p.update(d)
        return p

    @classmethod
    def from_file(cls, fpath):
        """Read parameters from file."""
        with open(fpath, "r") as fh:
            return cls.from_yaml(fh.read())

    def to_yaml(self):
        """Return yaml string representation."""
        return yaml.dump(dict(self),
                         explicit_start=True,
                         default_flow_style=False)

    def to_file(self, fpath):
        """Write parameters to file."""
        with open(fpath, "w") as fh:
            fh.write(self.to_yaml())


def test_from_yaml():
    p = Parameters.from_yaml("---\npi: 3.14\n")
    assert isinstance(p, Parameters)
    assert p["pi"] == 3.14

def test_to_yaml():
    p = Parameters()
    p["pi"] = 3.14
    assert p.to_yaml() == "---\npi: 3.14\n", p.to_yaml()
