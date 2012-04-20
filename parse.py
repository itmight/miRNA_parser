#!/usr/bin/python
"""Interactive script for ATLAS miRNA parser.

USE:
$ python parse.py [path_to_data_dir] > miRNA.tab 2> log.txt
"""
import sys
from __init__ import *


def main(dir_name):
  """Compile all miRNA files from a directory into a single matrix."""
  maps = compile_directory(dir_name)
  print_matrix(maps, out=sys.stdout, err=sys.stderr)


if __name__ == "__main__":
  main(sys.argv[1])
