from pathlib import Path

import click
import humanfriendly
from rsyncwrap import rsyncwrap
from halo import Halo
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TimeRemainingColumn,
    TotalFileSizeColumn,
    TransferSpeedColumn,
)

from ksink.helpers import PathPath


@click.command()
@click.argument("source", type=PathPath(require_dir=True, make_absolute=True))
@click.argument("dest", type=PathPath(require_dir=True, make_absolute=True))
def transfer(source: Path, dest: Path):
    """
    Transfers the directory `source` into the existing directory `dest`.

    Unlike rsync, we walk the entire source at the start and sum up the total size we
    will be transferring. If there's lots of files this can take awhile!

    We don't have anyway of knowing if some of the source is already at the
    destination (for example, if there is a previously-interrupted rsync operation).
    If there is already some of the source data there, the progress bar will not be
    accurate until the very end where rsync tells us the operation is complete.
    """
    source_size = get_file_sizes(source)

    with Progress(
        "{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        TransferSpeedColumn(),
        FileSizeColumn(),
        "/",
        TotalFileSizeColumn(),
        auto_refresh=False,
    ) as progress:
        transfer_task = progress.add_task("Transferring...", total=source_size)

        for stats in rsyncwrap(source, dest, include_raw_output=True):
            if not isinstance(stats, int):
                progress.update(transfer_task, completed=stats.total_transferred)
                progress.refresh()

        # Since rsync doesn't necessarily transfer every byte when destination files
        # already exist, we finally update progress...as long as there wasn't a
        # problem return code from rsync.
        if stats == 0:
            # TODO: This last update seems to throw the transfer rate figure way off?
            progress.update(transfer_task, completed=source_size)
            progress.refresh()
        assert stats == 0, f"Received error return code from rsync: {stats}"


def get_file_sizes(source):
    spinner = Halo(text="Getting source file data...")
    spinner.start()
    source_size = 0
    file_count = 0
    for f in source.glob("**/*"):
        spinner.text = str(f)
        if f.is_file():
            source_size += f.stat().st_size
            file_count += 1

    spinner.succeed(f"Found {file_count} source files with a total size of "
                    f"{humanfriendly.format_size(source_size, binary=True)}.")
    return source_size


if __name__ == "__main__":
    transfer()
