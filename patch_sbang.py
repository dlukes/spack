#!/usr/bin/env python3

"""Recursively patch overlong shebangs in a directory tree.

Usage: {__file__} DIR

DIR is the directory to search for executable files to patch.

This is useful e.g. for pip-installed scripts.

"""
import os
import sys
import logging as log
from pathlib import Path

SBANG = Path(__file__).parent.joinpath("bin", "sbang")


def patch(fpath):
    needs_sbang = False
    needs_new_sbang = False
    with open(fpath, "rt") as file:
        first_line = file.readline()
        if len(first_line) > 128:
            needs_sbang = True
        elif first_line.strip().endswith("sbang"):
            needs_new_sbang = True
        else:
            return
        rest = file.read()
    if needs_sbang or needs_new_sbang:
        with open(fpath, "wt") as file:
            file.write("#!{}\n".format(SBANG))
            if needs_sbang:
                file.write(first_line)
            file.write(rest)


def parse_argv(argv):
    if len(argv) != 2:
        print(__doc__.strip().format(**globals()), file=sys.stderr)
        sys.exit(1)
    return argv[1]


def main():
    dirname = parse_argv(sys.argv)
    for root, _, fnames in os.walk(sys.argv[1]):
        for fname in fnames:
            fpath = os.path.join(root, fname)
            if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
                try:
                    patch(fpath)
                except KeyboardInterrupt as e:
                    raise e
                except Exception as e:
                    log.warn("Error trying to patch {!r}: {}".format(fpath, e))


if __name__ == "__main__":
    main()
