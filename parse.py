#!/usr/bin/python
"""Compile a list of miRNA sample files into a MIC ready matrix.

USE:
$ python parse.py [path_to_data_dir] > miRNA.tab
"""
import os
import re
import sys

# bcgsc.ca__IlluminaGA_miRNASeq__TCGA-A6-2672-01A-01T-0827-13__mirna_quantification.txt
RX_DATAFILE = re.compile('bcgsc\.ca__IlluminaGA_miRNASeq__TCGA-([^_]+)__mirna_quantification\.txt', re.I)
warn = sys.stderr.write


def main(dir_name):
  filelist = os.listdir(dir_name)
  # Parse all data files.
  maps = mapping_from_filelist(dir_name, filelist)
  # Get set of all miRNA_IDs
  a = set()
  a = a.union(*[b for b in map(set, maps.values())])
  rna_ids = sorted(a)
  sample_ids = sorted(maps.keys())

  # Header of samples
  print "\t".join(["miRNA_ID"] + sample_ids)

  for rna_id in rna_ids:
    row = [rna_id]
    for sample_id in sample_ids:
      try:
	value = maps[sample_id][rna_id]
      except KeyError:
	value = ""
      row.append(value)
    # filter rows without at least 2 distinct values
    if len(set(row)) <= 2:
      warn("Removed row %s because it contains only one value.\n" % rna_id)
      continue
    print "\t".join(row)


def mapping_from_filelist(dir_name, filelist):
  """Return {str: {str: str}} of {sample_id => {miRNA_ID => reads_per_million}}
  """
  maps = {}

  for filename in filelist:
    d = {}
    m = RX_DATAFILE.match(filename)
    if not m: continue
    sample_id = m.group(1)
    fp = open(os.path.join(dir_name, filename), "r")

    # Get header.
    headers = fp.next().strip().split('\t')
    # Skip files with unrecognized headers
    if headers[1] != "miRNA_ID" or headers[3] != "reads_per_million_miRNA_mapped":
      warn("%s headers [%s] unexpected. Skipping..." % (filename, ",".join(headers)))
      continue
    
    # Read data lines. Col 1 is variable, Col 3 is data entry
    for line in fp:
      row = line.strip().split('\t')
      if not row: continue
      rna_id, datum = row[1], row[2]
      # Non-float values are assigned empty string
      try: 
	value = float(datum)
      except ValueError:
	value = ""
      else:
	value = datum
      d[rna_id] = value

    # Add variable mapping.
    maps[sample_id] = d
    fp.close()

  return maps


if __name__ == "__main__":
  main(sys.argv[1])
