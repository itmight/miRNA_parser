#!/usr/bin/python
"""Interactive script for ATLAS miRNA parser.

USE:
$ python parse.py [path_to_data_dir] > miRNA.tab 2> log.txt

e.g.
$ python script.py ~/Dropbox/biostat/miRNA_data/June_colon\ adenocarcinoma_COAD_miRNA/Level_3 > ~/Dropbox/biostat/miRNA_data/June_colon\ adenocarcinoma_COAD_miRNA/miRNA_coad_matrix.tab 2> ~/Dropbox/biostat/miRNA_data/June_colon\ adenocarcinoma_COAD_miRNA/miRNA_coad_log.txt
"""
import sys
from __init__ import *


def main(dir_name):
  """Compile all miRNA files from a directory into a single matrix."""
  maps = compile_directory(dir_name)
  print_matrix(maps, out=sys.stdout, err=sys.stderr)


if __name__ == "__main__":
  main(sys.argv[1])
