"""
Override the data on a disk with random data.

1. Remove all the contents on the disk;
2. Fill the disk with random data;
3. Repeat step-1 and step-2 several times;
4. Remove all the contents on the disk.
"""


__all__ = ["RemoveAll", "Erase"]


from pathlib import Path
from shutil import disk_usage
from time import sleep

import numpy as np


def RemoveAll(path):
    """
    Delete all the contents in the given `path`.

    Parameters
    ----------
    path: str or Path
        The directory whose contents to be removed.
        `path` must be a directory.
    """

    for item in Path(path).iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                RemoveAll(item)
                item.rmdir()
            else:
                print("Failed to delete {0}, unsupported type.".format(item))
        except Exception as e:
            print("Failed to delete {0}, {1}.".format(item, e))


def Erase(path, cycles=10, max_size=1024, interval=60):
    """
    Remove all the contents in the given `path`.

    This function performs the following operations:
    1. Remove all the contents in the given `path`;
    2. Fill the disk where `path` is located with random data;
    3. Repeat step-1 and step-2 several times;
    4. Remove all the contents in the given `path`.

    Parameters
    ----------
    path: str
        The directory whose contents to be removed.
        `path` must be a directory.
        Generally `path` is the root directory of on a disk.
    cycles : int, optional
        The number of times for repeating step-1 and step2.
        Default: 10.
    max_size : int
        The maximum size of a single file to write to `path`.
        The unit of `max_size` is MB.
        Default: 1024.
    interval : int
        The time interval between two cycle.
        The unit of `interval` is second.
        Default: 60.
    """

    for cycle in range(cycles):
        RemoveAll(path)
        print("Remove all contents on {0}.".format(path))

        count = 0
        max_length = 128 * 1024 * max_size
        while disk_usage(path).free >= 1024:
            name = "{0:0>10d}.npy".format(count)
            length = np.random.randint(1, max_length + 2)
            data = np.random.random(length)
            try:
                np.save(path + name, data)
                print("Save {0} to {1}.".format(name, path))
                count += 1
            # If not enough space to save the data, the above `save` command
            # would raise `OSError`, then reduce `max_length` and re-generate
            # random data.
            except OSError:
                max_length = max_length // 2
        sleep(interval)

    RemoveAll(path)
    print("Remove all contents on {0}.".format(path))
