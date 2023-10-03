#! /usr/bin/env python3

import os
from sys import argv

BASENAME_NUM_BYTES = 4
FILE_NUM_BYTES = 8


def create(paths: list[str]) -> None:
    for path in paths:
        if os.path.isfile(path):
            fd = os.open(path, os.O_RDONLY)
            basename = str(os.path.basename(path))
            basename_size = len(basename)
            file_size = os.path.getsize(path)
            file_contents = os.read(fd, file_size)

            os.write(1, basename_size.to_bytes(BASENAME_NUM_BYTES, "big"))
            os.write(1, basename.encode())
            os.write(1, file_size.to_bytes(FILE_NUM_BYTES, "big"))
            os.write(1, file_contents)


def extract() -> None:
    while basename_size := int.from_bytes(os.read(0, BASENAME_NUM_BYTES), "big"):
        basename = os.read(0, basename_size).decode()
        file_size = int.from_bytes(os.read(0, FILE_NUM_BYTES), "big")
        file_contents = os.read(0, file_size)

        fd = os.open(basename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        os.write(fd, file_contents)


if __name__ == "__main__":
    if argv[1] == "c":
        create(argv[2:])
    elif argv[1] == "x":
        extract()
