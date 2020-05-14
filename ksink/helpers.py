from pathlib import Path

import click


class PathPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def __init__(
        self, *args, require_dir: bool = False, make_absolute: bool = True, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.require_dir = require_dir
        self.make_absolute = make_absolute

    def convert(self, value, param, ctx):
        p = Path(super().convert(value, param, ctx))
        if self.make_absolute:
            p = p.absolute()
        if self.require_dir and not p.is_dir():
            self.fail(f"{self.path_type} '{p}' is not a directory.", param, ctx)
        return p
