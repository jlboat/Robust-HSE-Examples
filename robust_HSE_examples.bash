#!/usr/bin/env bash

## Optional Installation Directions for Linux Operating Systems
## May alternatively pull singularity containers for all programs
# sudo apt-get install -y libssl-dev git build-essential autoconf \
# 	zlib1g pkg-config zlib1g-dev samtools bcftools bwa tabix bedtools

# Clone the BayesASE git repository
git clone https://github.com/McIntyre-Lab/BayesASE

## LAST ALIGNMENTS
# Pull singularity container for Last
singularity pull docker://biocontainers/last-align:v963-2-deb_cv1

# Extract sequences from reference A
bedtools getfasta -fi ./BayesASE/example_in/reference/dmel_r551_chromosome_2R_X.fasta -bed BayesASE/galaxy/test-data/align_and_counts_test_data/BASE_testData_BEDfile.bed > W55.fa

# Extract sequences from reference B
bedtools getfasta -fi ./BayesASE/example_in/reference/updated_genomes_vcfConsensus/W1118_snp_upd_genome.fasta -bed ./BayesASE/galaxy/test-data/align_and_counts_test_data/BASE_testData_BEDfile.bed > W1118.fa

# Index reference A
singularity run last-align_v963-2-deb_cv1.sif \
  lastdb W55_db W55.fa

# Index reference B
singularity run last-align_v963-2-deb_cv1.sif \
  lastdb W1118_db W1118.fa

# Align reference B sequences to database A
singularity run last-align_v963-2-deb_cv1.sif \
  lastal -f BlastTab+ -P 4 -E0.00005 W55_db W1118.fa > W1118_To_W55.maf

# Align reference A sequences to database B
singularity run last-align_v963-2-deb_cv1.sif \
  lastal -f BlastTab+ -P 4 -E0.00005 W1118_db W55.fa > W55_To_W1118.maf

# Identify reciprocal-best hits
python LAST_COREs.py -a W55_To_W1118.maf -b W1118_To_W55.maf

## FASTP AND MULTIQC
# Make a directory for fastp output
mkdir fastp

# Run fastp on all example FASTQ files
while read p
do 
  fastp -i ./BayesASE/example_in/reads/${p}.fastq -o ./fastp/${p}.trimmed -j ./fastp/${p}_fastp.json -h ./fastp/${p}_fastp.html
done < <(ls -1 ./BayesASE/example_in/reads/*.fastq | cut -f 2 -d '.' | cut -f 5 -d '/')

# Accumulate fastp results into a MultiQC report
multiqc ./fastp/

# BayesASE
# Follow BayesASE documentation: https://github.com/McIntyre-Lab/BayesASE
# Optionally use Ortholog COREs for example
