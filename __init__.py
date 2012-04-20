#!/usr/bin/python
"""ATLAS miRNA parser.
Compile a list of miRNA sample files into a MIC ready matrix.
Andrew D. Yates 2012

Removes lines with only one variable because MINE.jar fails for these lines.

USE:
$ python parse.py [path_to_data_dir] > miRNA.tab 2> log.txt
"""
import os
import re
import sys


# bcgsc.ca__IlluminaGA_miRNASeq__TCGA-A6-2672-01A-01T-0827-13__mirna_quantification.txt
RX_DATAFILE = re.compile('bcgsc\.ca__IlluminaGA_miRNASeq__([^_]+)__mirna_quantification\.txt', re.I)
warn = sys.stderr.write
  

def print_matrix(maps, out, err, print_header=False, delimiter="\t"):
  """Print MINE.jar-ready delimited matrix from data map to `out`. 

  MINE.jar Input Format (to print):
    -) row: miRNA variable
    -) column: sample ID
    -) no column headers
    -) rows with only one value removed
    -) present values as floats, missing values as ""

  Intended to process `maps` output from `compile_directory()`

  Args:
    maps: {str: {str: str}} of {sample_id => {miRNA_ID => reads_per_million}}
    out: fp of write buffer for printed matrix output
    err: fp of write buffer for list of removed rows.
    print_header: bool if print column titles as first row (not MINE.jar format)
    delimiter: str of character to separate columns
  """
  # Get sorted list of all miRNA_IDs
  a = set()
  a = a.union(*[b for b in map(set, maps.values())])
  rna_ids = sorted(a)
  c = delimiter
  
  # Get sorted list of all sample_ids
  sample_ids = sorted(maps.keys())

  # Header of samples
  if print_header:
    out.write(c.join(["miRNA_ID"] + sample_ids) + "\n")

  # Print Matrix: row is variable, column is sample
  for rna_id in rna_ids:
    row = [rna_id]
    for sample_id in sample_ids:
      # If a variable value is missing for a sample, print ""
      try:
	value = maps[sample_id][rna_id]
      except KeyError:
	value = ""
      row.append(value)

    if len(set(row)) <= 2:
      err.write("%s row removed because it contains only one value.\n" % rna_id)
      continue
    # Write tab-delimited row
    out.write(c.join(row) + "\n")



def compile_directory(dir_name):
  """Parse all miRNA files in a directory as a single study.

  Args:
    dir_name: str of path to directory containing miRNA data files
  Returns:
    {str: {str: str}} of {sample_id => {miRNA_ID => reads_per_million}}
  """
  maps = {}

  # select all files in a directory
  filelist = os.listdir(dir_name)

  for filename in filelist:
    # Verify that filename matches miRNA data file pattern.
    m = RX_DATAFILE.match(filename)
    if not m: continue
    # Select sample ID from group
    sample_id = m.group(1)
    # Parse file contents as a dictionary of variables to values
    fp = open(os.path.join(dir_name, filename), "r")
    d = parse_file(fp, sample_id)
    fp.close()

    # Add variable mapping.
    if d is not None:
      maps[sample_id] = d
    else:
      warn("%s in unexpected format. Skipping..." % (filename))

  return maps


def parse_file(fp, sample_id=None):
  """Parse ATLAS single sample, column of variables miRNA data file.

  Args:
    fp: [*str] of open file pointer to datafile
    sample_id: str of sample_id to verify for these file contents
  Returns:
    {str: str} of {variable_name => [value as float or ""] 
      or None if invalid file
  """
  d = {}
  # Get header.
  headers = fp.next().strip().split('\t')
  # Skip files with unrecognized headers
  try:
    if headers[1] != "miRNA_ID" or headers[3] != "reads_per_million_miRNA_mapped":
      return None
  except IndexError:
    return None
    
  # Read remaining data lines. 2nd column is variable, 4th column is data
  for line in fp:
    row = line.strip().split('\t')
    if not row: continue

    row_id, rna_id, datum = row[0], row[1], row[3]
    if sample_id:
      assert row_id == sample_id, "%s != %s" % (row_id, sample_id)
      
    # Non-float values are assigned empty string
    try: 
      float(datum)
    except ValueError:
      value = ""
    else:
      value = datum
    d[rna_id] = value

  return d

