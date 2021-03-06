# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 11:16:34 2016

@author: Lucas Boatwright
"""

from sys import argv, stderr, exit
import argparse
from datetime import datetime

def parse_arguments():
    """Parse arguments passed to script"""
    parser = argparse.ArgumentParser(description=
    "This script is designed to identify reciprocal best-hits given two \
    \nparsed LAST files. Output includes reciprocated_last_hits.txt and \
    \ntwo BED files representing HSP coordinates from LAST_A for query \
    \nand subject.\n\
    \n\tUsage: python {0} -a A_to_B_LAST -b B_to_A_LAST\
    \n".format(
    argv[0]), formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-a", "--LAST_A", type=str, required=True,
    help="Parsed LAST file from species A in tab-separated format.", 
        action="store")
        
    parser.add_argument("-b", "--LAST_B", type=str, required=True,
    help="Parsed LAST file from species B in tab-separated format.", 
        action="store")
        
    return parser.parse_args() 


def get_dict_from_last(file_name, subject_index):
    """Generate a dictionary from tabular LAST (one-one) output"""
    last_dict = {}
    with open(file_name) as f:
        for line in f.read().splitlines():
            if not line.startswith("#"):
                split_line = line.split()
                if split_line[0] not in last_dict.keys():
                    last_dict[split_line[0]] = split_line[subject_index]
    return last_dict

    
def check_reciprocity(dict_a, dict_b):
    """Check to see LAST homology is reciprocated""" 
    reciprocated = {}
    for key, value in dict_a.items():               
        try:
            if dict_b[value]==key:
                reciprocated[key] = value
            else:
                continue
        except KeyError:
            continue
    output = open("reciprocated_last_hits.txt","w")
    for key, value in reciprocated.items():
        if value != []:
            output.write(key + "\t" + value + "\n")
            # output.flush()
    output.close()


def get_reciprocated_table():
    """Get reciprocated orthologs"""
    with open("reciprocated_last_hits.txt") as f:
        reciprocated_file = f.readlines()
    reciprocated_table = []
    for line in reciprocated_file:
        split_line = line.split()
        reciprocated_table.append((split_line[0], split_line[1]))
    return reciprocated_table    
        
        
def filter_last_file(last_file, reciprocated_table, subject_index):
    """Filter last file by reciprocal orthologs"""       
    filtered_last = []
    written_pairs = []
    with open(last_file) as last:
        for x, line in enumerate(last.read().splitlines()):
            if not line.startswith("#"):
                if ( (x+1)%10000 == 0 ):
                    stderr.write("\tProcessed {0} lines.\n".format(str(x+1)))
                split_line = line.split()
                if (((split_line[0], split_line[subject_index]) in reciprocated_table) and 
                        ((split_line[0], split_line[subject_index]) not in written_pairs)):
                    filtered_last.append(line)
                    written_pairs.append((split_line[0], split_line[subject_index]))
    return filtered_last
        

def generate_S_and_Q_BEDs(filtered_last, last_file_name, subject_index):
    """Generate bed files for Queries and Subjects"""
    if subject_index == 1:
        q_start = 6
        q_stop = 7
        s_start = 8
        s_stop = 9
    elif subject_index == 2:
        q_start = 9
        q_stop = 10
        s_start = 11
        s_stop = 12
    output = open(last_file_name + ".filtered_S.bed", "w")
    # write B
    for line in filtered_last:
        split_line = line.split()
        output.write("\t".join([split_line[subject_index], 
            str(min(int(split_line[s_start])-1, int(split_line[s_stop])-1)), 
            str(max(int(split_line[s_start])-1, int(split_line[s_stop])-1)),
            ",".join([split_line[0],split_line[subject_index]]),".", "+\n"]))
    output.close()
    
    output = open(last_file_name + ".filtered_Q.bed", "w")
    #write A
    for line in filtered_last:
        split_line = line.split()
        output.write("\t".join([split_line[0], 
            str(min(int(split_line[q_start])-1, int(split_line[q_stop])-1)), 
            str(max(int(split_line[q_start])-1, int(split_line[q_stop])-1)),
            ",".join([split_line[0],split_line[subject_index]]),".", "+\n"]))
    output.close()
    
    
if __name__ == "__main__":
    start = datetime.now()
    args = parse_arguments()
    subject_index = 1
    stderr.write("Generating dictionary from Species A LAST to B.\n")
    dict_a = get_dict_from_last(args.LAST_A, subject_index)
    stderr.write("Generating dictionary from Species B LAST to A.\n")
    dict_b = get_dict_from_last(args.LAST_B, subject_index)
    stderr.write("Identifying reciprocated hits.\n")
    check_reciprocity(dict_a, dict_b)
    stderr.write("Generating BED files from gene-transcript map.\n")
    reciprocated_table = get_reciprocated_table()
    filtered_last = filter_last_file(args.LAST_A, reciprocated_table, 
                                       subject_index)
    generate_S_and_Q_BEDs(filtered_last, args.LAST_A, subject_index)
    stop = datetime.now()
    stderr.write("Runtime: {0}".format(str(stop - start)))
