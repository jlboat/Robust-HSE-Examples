# Robust-HSE-Examples
A robust methodology for assessing homoeolog-specific expression

This code was developed for educational purposes. To execute the pipeline, install the required software and run 'bash robust_HSE_examples.bash'

# Example usage for LAST_COREs.py
'''bash
usage: LAST_COREs.py [-h] -a LAST_A -b LAST_B

This script is designed to identify reciprocal best-hits given two
parsed LAST files. Output includes reciprocated_last_hits.txt and
two BED files representing HSP coordinates from LAST_A for query
and subject.

        Usage: python LAST_COREs.py -a A_to_B_LAST -b B_to_A_LAST

optional arguments:
  -h, --help            show this help message and exit
  -a LAST_A, --LAST_A LAST_A
                        Parsed LAST file from species A in tab-separated
                        format.
  -b LAST_B, --LAST_B LAST_B
                        Parsed LAST file from species B in tab-separated
                        format.
'''
