#!/bin/bash

#PBS -l nodes=1:ppn=8,walltime=24:00:00,vmem=40gb
#PBS -j oe
#PBS -m abe
#PBS -d /N/slate/sialsaff/code4Rice3K/

module load java/1.8.0_131

./gatk GenotypeGVCFs -R reference.fasta -V gendb://path_to_genomicsdbdir -O ADM-chr01.vcf.gz -L chr01 -all-sites
