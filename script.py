#!/usr/bin/python
"""Interactive script for ATLAS miRNA parser.

USE:
$ python script.py [path_to_data_dir] > miRNA.tab 2> log.txt

e.g.
$ python script.py ~/Dropbox/biostat/miRNA_data/June_colon_adenocarcinoma_COAD_miRNA/raw > ~/Dropbox/biostat/miRNA_data/June_colon_adenocarcinoma_COAD_miRNA/miRNA_coad_matrix.tab 2> ~/Dropbox/biostat/miRNA_data/June_colon_adenocarcinoma_COAD_miRNA/miRNA_coad_matrix.log
"""
USE_MSG = "USE: $ python script.py [path_to_data_dir] > miRNA.tab 2> log.txt"

import sys
import os
from __init__ import *


def main(dir_name):
  """Compile all miRNA files from a directory into a single matrix.

  Args:
    dir_name: name of directory containing miRNA sample files to parse
  """
  maps = compile_directory(dir_name)
  sys.stderr.write("#Parsed directory %s using module %s at %s.\n" % \
    (dir_name, os.getcwd(), timestamp()))

  desc = "Files parsed from %s" % (dir_name)
  print_matrix(maps, desc=desc, out=sys.stdout, err=sys.stderr)


if __name__ == "__main__":
  try:
    dir_name = sys.argv[1]
  except:
    print USE_MSG
    sys.exit(1)
  main(dir_name)
    
